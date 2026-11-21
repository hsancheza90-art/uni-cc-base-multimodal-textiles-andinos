"""Ejecución única del test: comprobación previa, rankings, juicios ciegos y evaluación final.

Uso desde la raíz del repositorio, en este orden (protocolo experimental v2, secciones 6 a 9):

    python -m src.experimento.ejecucion_prueba --comprobar       # condiciones de suspensión; no ejecuta nada
    python -m src.modelos.m2_openclip --textos-t1                # vectores de texto de las consultas T1 (torch)
    python -m src.experimento.ejecucion_prueba --rankings        # una sola vez: manifiesto y rankings de prueba
    python -m src.experimento.ejecucion_prueba --crear-juicios   # libros ciegos de juicios de prueba (T3 y T1)
    python -m src.experimento.ejecucion_prueba --evaluar         # H1, H2, H3, ablaciones, control y robustez

Ningún paso de este módulo forma parte del flujo, y `--rankings` se niega a ejecutar si la
comprobación previa encuentra un problema. La primera condición es que el protocolo esté aprobado:
`[ejecucion] aprobacion_protocolo` de config/experimento.toml no puede estar vacío, y la suma
SHA-256 del protocolo debe coincidir con la registrada al aprobarlo (decisión R30).

Las funciones de cálculo reciben la partición como parámetro para poder probarse con los datos de
desarrollo. La línea de órdenes solo usa la partición de prueba.

El evaluador no abre los rankings, el pool ni el informe de resultados hasta terminar todos los
juicios de prueba.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

from src.anotacion import aplicar_anotaciones_v2 as exportacion
from src.anotacion import buena_formacion, congelacion_v21
from src.anotacion.aplicar_anotaciones import fecha_valida
from src.anotacion.corpus_v2 import SALIDA_PRINCIPAL_V2
from src.experimento import evaluacion, juicios, rankings
from src.experimento.consultas_t1 import SALIDA_T1
from src.experimento.libro import escribir_libro
from src.experimento.potencia import consultas_con_palabra
from src.experimento.snapshot import SALIDA_CONSULTAS, SALIDA_PARTICIONES
from src.experimento.snapshot import comprobar as comprobar_particiones
from src.imagenes.descargar_evaluacion import MANIFIESTO_EVALUACION
from src.imagenes.motivos import analizar_motivo
from src.modelos import m0_texto, m1_vision, m3_estructura, m4_fusion
from src.modelos.embeddings import EMBEDDINGS_M2, INDICE_M2, MANIFIESTO_M2, leer_embeddings
from src.review.galerias import CARPETA, esc, escribir_pagina, imagen_evaluacion, tarjeta
from src.utils.archivos import escribir_csv, escribir_json, escribir_texto, indexar, leer_csv
from src.utils.config import CONFIG_EXPERIMENTO, CONFIG_MODELOS, leer_config_experimento, leer_config_modelos
from src.utils.fuentes import FUENTES
from src.utils.libros import leer_hoja
from src.utils.metricas import tabla
from src.utils.vocabulario import leer_vocabulario

PROTOCOLO = Path("docs/protocolo_experimental_v2.md")
RANKINGS_PRUEBA = "data/processed/experimento_v2_rankings_prueba.csv"
RANKINGS_T1 = "data/processed/experimento_v2_rankings_t1.csv"
MANIFIESTO_EJECUCION = "data/processed/experimento_v2_manifiesto_ejecucion.json"
EMBEDDINGS_T1 = Path("data/metadata/m2_openclip_t1_v2.npy")
INDICE_T1 = Path("data/metadata/m2_openclip_t1_indice_v2.csv")
METRICAS = "data/processed/experimento_v2_metricas_por_consulta.csv"
REPORTE = "outputs/reports/experimento_v2_resultados.md"
WORKBOOK_REVISION_H3 = Path("data/metadata/revision_h3_v2.xlsx")
COLUMNAS_METRICAS = ["tarea", "consulta", "sistema", "ndcg10", "p10", "mrr", "juzgada10"]
SISTEMAS_T1 = ("M0", "M2", "M3", "M4")


@dataclass(frozen=True)
class Tarea:
    """Rutas y textos de los juicios de una tarea (T3 o T1)."""

    nombre: str
    rankings: str
    pool: str
    workbook: Path
    salida: str
    galeria: Path
    guia: list[str]


GUIA_T3 = [
    "Juicios de relevancia de PRUEBA, tarea T3 (protocolo experimental v2, seccion 6)",
    "",
    "Misma escala y mismas reglas que los juicios de desarrollo. Juzgue solo, sin ninguna asistencia (decision R27).",
    "Cada fila es un par: la pieza consultada y un candidato. Juzgue si el candidato tiene la MISMA ORGANIZACION",
    "visible que la consulta, mirando solo las dos imagenes (galeria local outputs/review/juicios_prueba_v2_galeria.html).",
    "",
    "  3 = misma organizacion: tipo de composicion, secuencia de bandas o regiones y relaciones, aunque cambien colores",
    "      y motivos.",
    "  2 = misma composicion con diferencias en la secuencia o en las relaciones.",
    "  1 = comparte un rasgo estructural parcial.",
    "  0 = organizacion distinta.",
    "  no_evaluable = la imagen no deja juzgar (no es 0).",
    "",
    "Reglas: el color no cuenta; no abra la anotacion, los rankings, el pool ni ningun informe de resultados; el orden",
    "de las filas es al azar y no dice nada del sistema. Un juicio 2 o 3 lleva una justificacion breve con la evidencia",
    "visible. Complete evaluador y fecha_juicio (AAAA-MM-DD).",
    "",
    "Despues: python -m src.experimento.ejecucion_prueba --evaluar valida los juicios y calcula los resultados.",
]

GUIA_T1 = [
    "Juicios de relevancia de PRUEBA, tarea T1: texto a imagen (protocolo experimental v2, seccion 6)",
    "",
    "Juzgue solo, sin ninguna asistencia (decision R27). Cada fila es un par: una consulta escrita y un candidato.",
    "Juzgue si la imagen del candidato cumple la descripcion (galeria local outputs/review/juicios_t1_v2_galeria.html).",
    "",
    "  3 = cumple toda la descripcion.",
    "  2 = cumple lo principal.",
    "  1 = cumple un rasgo.",
    "  0 = no la cumple.",
    "  no_evaluable = la imagen no deja juzgar (no es 0).",
    "",
    "Un juicio 2 o 3 lleva una justificacion breve. Complete evaluador y fecha_juicio (AAAA-MM-DD).",
]

TAREAS = {
    "T3": Tarea("T3", RANKINGS_PRUEBA, "data/processed/experimento_v2_pool_prueba.csv",
                Path("data/metadata/juicios_prueba_v2.xlsx"), "data/metadata/juicios_prueba_v2.csv",
                Path(CARPETA) / "juicios_prueba_v2_galeria.html", GUIA_T3),
    "T1": Tarea("T1", RANKINGS_T1, "data/processed/experimento_v2_pool_t1.csv",
                Path("data/metadata/juicios_t1_v2.xlsx"), "data/metadata/juicios_t1_v2.csv",
                Path(CARPETA) / "juicios_t1_v2_galeria.html", GUIA_T1),
}


def sha256(ruta: Path) -> str:
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def fmt(x: float | None, d: int = 3) -> str:
    return "—" if x is None or x != x else f"{x:.{d}f}"


# --------------------------------------------------------------------------- comprobacion previa


def aprobado(raiz: Path) -> bool:
    """El protocolo está aprobado y no cambió después de aprobarlo."""
    ejecucion = leer_config_experimento(raiz).get("ejecucion", {})
    return bool(ejecucion.get("aprobacion_protocolo")) and ejecucion.get("sha256_protocolo") == sha256(raiz / PROTOCOLO)


def comprobar(raiz: Path, antes_de_rankings: bool = True) -> list[str]:
    """Condiciones de suspensión del protocolo (sección 9) que pueden verificarse en el repositorio."""
    config = leer_config_experimento(raiz)
    ejecucion = config.get("ejecucion", {})
    problemas: list[str] = []
    if not ejecucion.get("aprobacion_protocolo"):
        problemas.append("El protocolo no esta aprobado: [ejecucion] aprobacion_protocolo esta vacio (decision R30).")
    elif ejecucion.get("sha256_protocolo") != sha256(raiz / PROTOCOLO):
        problemas.append("El protocolo cambio despues de su aprobacion: su suma no coincide con [ejecucion] sha256_protocolo.")
    errores, _ = comprobar_particiones(raiz, config)
    problemas += [f"Particiones y consultas: {e}" for e in errores]
    congelada, exportada = congelacion_v21.ruta_congelada(raiz), raiz / exportacion.SALIDA_ANOTACIONES_V2
    if not congelada.exists():
        problemas.append("La anotacion v2.1 no esta congelada.")
    else:
        if not exportada.exists() or exportada.read_bytes() != congelada.read_bytes():
            problemas.append("La anotacion exportada no coincide con la copia congelada v2.1.")
        incumplidas = {c: ids for c, ids in buena_formacion.revisar(leer_csv(congelada), leer_vocabulario(raiz)).items() if ids}
        problemas += [f"La anotacion congelada incumple {c}: {', '.join(ids)}" for c, ids in incumplidas.items()]
    if not leer_config_modelos(raiz).get("m4", {}).get("pesos"):
        problemas.append("Los pesos de M4 no estan fijados en [m4.pesos].")
    problemas += imagenes_no_verificadas(raiz)
    t1 = [f for f in leer_csv(raiz / SALIDA_T1)] if (raiz / SALIDA_T1).exists() else []
    if len(t1) != int(config["consultas_t1"]["prueba"]) or not all(f["descripcion"] for f in t1):
        problemas.append("Las consultas T1 no estan todas redactadas y validadas.")
    if antes_de_rankings and (raiz / RANKINGS_PRUEBA).exists():
        problemas.append(f"Ya existe {RANKINGS_PRUEBA}: el test se ejecuta una sola vez.")
    return problemas


def imagenes_no_verificadas(raiz: Path) -> list[str]:
    """Piezas de la galería cuyos vectores de M1 o M2 no proceden de la copia verificada del manifiesto."""
    manifiesto = {f["id_global"]: f["sha256_copia"] for f in leer_csv(raiz / MANIFIESTO_EVALUACION)
                  if f["estado_descarga"] == "ok"}
    galeria = [f["id_global"] for f in leer_csv(raiz / SALIDA_PARTICIONES)]
    problemas = []
    for nombre, indice in (("M1", m1_vision.INDICE_M1), ("M2", INDICE_M2)):
        sumas = {f["id_global"]: f["sha256_copia"] for f in leer_csv(raiz / indice)}
        malas = [i for i in galeria if i not in manifiesto or sumas.get(i) != manifiesto[i]]
        if malas:
            problemas.append(f"Imagenes no verificadas para {nombre}: {', '.join(malas[:10])}")
    return problemas


# --------------------------------------------------------------------------- manifiesto y rankings


def git(raiz: Path, *argumentos: str) -> str:
    try:
        return subprocess.run(["git", *argumentos], cwd=raiz, capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return ""


def manifiesto(raiz: Path) -> dict[str, Any]:
    """Registro de la ejecución: commit, sumas de los insumos, checkpoint, parámetros, equipo y semillas."""
    config, modelos = leer_config_experimento(raiz), leer_config_modelos(raiz)
    insumos = [SALIDA_PARTICIONES, SALIDA_CONSULTAS, SALIDA_T1, SALIDA_PRINCIPAL_V2, MANIFIESTO_EVALUACION,
               congelacion_v21.ruta_congelada(raiz).relative_to(raiz).as_posix(), str(m1_vision.CARACTERISTICAS_M1),
               str(m1_vision.INDICE_M1), str(EMBEDDINGS_M2), str(INDICE_M2), str(MANIFIESTO_M2), str(EMBEDDINGS_T1),
               str(INDICE_T1), juicios.SALIDA_JUICIOS, PROTOCOLO.as_posix(), CONFIG_EXPERIMENTO.as_posix(),
               CONFIG_MODELOS.as_posix()]
    insumos = [Path(r).as_posix() for r in insumos]
    m2 = json.loads((raiz / MANIFIESTO_M2).read_text(encoding="utf-8"))
    return {
        "aprobacion_protocolo": config["ejecucion"]["aprobacion_protocolo"],
        "commit": git(raiz, "rev-parse", "HEAD"),
        "arbol_limpio": git(raiz, "status", "--porcelain") == "",
        "sha256_insumos": {r: sha256(raiz / r) for r in insumos if (raiz / r).exists()},
        "checkpoint_m2": {c: m2.get(c, "") for c in ("arquitectura", "pesos", "sha256_pesos", "encuadre", "precision")},
        "parametros": {"experimento": config, "modelos": modelos},
        "entorno": {"python": sys.version.split()[0], "plataforma": platform.platform(), "numpy": np.__version__},
    }


def leer_embeddings_t1(raiz: Path) -> dict[str, np.ndarray]:
    """Vectores de texto de las consultas T1, por consulta (los calcula m2_openclip --textos-t1)."""
    matriz = np.load(raiz / EMBEDDINGS_T1).astype(np.float64)
    return {f["consulta"]: matriz[int(f["fila"])] for f in leer_csv(raiz / INDICE_T1)}


def rankings_t1(raiz: Path) -> list[dict[str, str]]:
    """Rankings T1: cada consulta escrita contra toda la galería (protocolo, sección 3).

    M0 compara la descripción con el texto de las fichas; M2, su vector de texto con los vectores de
    imagen; M3 solo participa si la consulta trae especificación estructural (composición o palabra
    de bandas), y entonces compara solo esos bloques; M4 fusiona los componentes disponibles con los
    pesos fijados en desarrollo. M1 no procesa texto y no participa."""
    modelos = leer_config_modelos(raiz)
    galeria = [f["id_global"] for f in leer_csv(raiz / SALIDA_PARTICIONES)]
    fichas = [f for f in leer_csv(raiz / SALIDA_PRINCIPAL_V2) if f["id_global"] in set(galeria)]
    bm25, _ = m0_texto.indice(fichas, modelos["m0"])
    embeddings = leer_embeddings(raiz)
    posicion, m2 = embeddings.posicion(), embeddings.matriz.astype(np.float64)
    textos = leer_embeddings_t1(raiz)
    anotadas = indexar(leer_csv(congelacion_v21.ruta_congelada(raiz)), "id_global")
    descriptores = {i: m3_estructura.descriptor(anotadas[i]) for i in galeria}
    pesos_m3 = {b: float(p) for b, p in modelos["m3"]["pesos"].items()}
    pesos_m4 = {c: float(p) for c, p in modelos["m4"]["pesos"].items()}
    filas = []
    for consulta in [f for f in leer_csv(raiz / SALIDA_T1) if f["descripcion"]]:
        codigo = consulta["consulta"]
        terminos = m0_texto.tokenizar(consulta["descripcion"], int(modelos["m0"]["longitud_minima_termino"]))
        por_sistema: dict[str, dict[str, float | None]] = {
            "M0": {c: bm25.puntuar(terminos, c) for c in galeria},
            "M2": {c: float(textos[codigo] @ m2[posicion[c]]) for c in galeria},
        }
        especificada = bool(consulta["composicion"] or consulta["secuencia_bandas"])
        if especificada:
            pedida = m3_estructura.Descriptor(
                composicion=consulta["composicion"] or None,
                bandas=m3_estructura.palabra_de_bandas(consulta["secuencia_bandas"]) if consulta["secuencia_bandas"] else None)
            por_sistema["M3"] = {}
            for c in galeria:
                d = m3_estructura.comparar(pedida, descriptores[c], pesos_m3).disimilitud
                por_sistema["M3"][c] = None if d is None else 1 - d
        redondeados = {s: {i: None if v is None else round(v, 6) for i, v in v_s.items()} for s, v_s in por_sistema.items()}
        excluir = frozenset() if especificada else frozenset({"M3"})
        fusion = m4_fusion.fusionar(redondeados, pesos_m4, excluir=excluir)
        por_sistema["M4"] = {i: f.score for i, f in fusion.items()}
        filas += rankings.filas_ranking(codigo, por_sistema, tuple(s for s in SISTEMAS_T1 if s in por_sistema))
    return filas


def ejecutar_rankings(raiz: Path) -> int:
    problemas = comprobar(raiz)
    if not (raiz / EMBEDDINGS_T1).exists():
        problemas.append(f"Faltan los vectores de texto de T1 ({EMBEDDINGS_T1}): python -m src.modelos.m2_openclip --textos-t1")
    if problemas:
        print("El test no se abre:")
        for problema in problemas:
            print(f"- {problema}")
        return 1
    filas, sistemas, _ = rankings.rankings_t3(raiz, "prueba")
    escribir_csv(raiz / RANKINGS_PRUEBA, rankings.COLUMNAS, filas)
    escribir_csv(raiz / RANKINGS_T1, rankings.COLUMNAS, rankings_t1(raiz))
    escribir_json(raiz / MANIFIESTO_EJECUCION, manifiesto(raiz))
    print(f"Rankings de prueba: T3 ({', '.join(sistemas)}) -> {RANKINGS_PRUEBA}; T1 -> {RANKINGS_T1}")
    print(f"Manifiesto de ejecucion -> {MANIFIESTO_EJECUCION}. No abra los rankings: siga con --crear-juicios.")
    return 0


# --------------------------------------------------------------------------- juicios de prueba


def pool(raiz: Path, tarea: Tarea, config: dict[str, Any]) -> list[dict[str, str]]:
    base = set(config["ejecucion"]["sistemas_muestra_azar_t1"]) if tarea.nombre == "T1" else None
    return juicios.construir_pool(raiz, config, tarea.rankings, base)


def leer_libro(raiz: Path, tarea: Tarea) -> dict[str, dict[str, str]]:
    ruta = raiz / tarea.workbook
    if not ruta.exists():
        return {}
    return {juicios.clave(f["consulta"], f["id_candidato"]): f for f in leer_hoja(ruta, juicios.HOJA_JUICIOS, clave="consulta")}


def crear_juicios(raiz: Path) -> int:
    config = leer_config_experimento(raiz)
    if not (raiz / RANKINGS_PRUEBA).exists():
        print(f"No existe {RANKINGS_PRUEBA}: ejecute antes --rankings.")
        return 1
    manifiesto_imagenes = indexar(leer_csv(raiz / MANIFIESTO_EVALUACION), "id_global")
    ruta_imagen = lambda i: "../" + manifiesto_imagenes.get(i, {}).get("ruta_copia_evaluacion", "").removeprefix("data/")  # noqa: E731
    descripciones = {f["consulta"]: f["descripcion"] for f in leer_csv(raiz / SALIDA_T1)}
    consultas_t3 = indexar(leer_csv(raiz / SALIDA_CONSULTAS), "consulta")
    escala = [str(g) for g in config["juicios"]["escala"]] + [juicios.NO_EVALUABLE]
    for tarea in TAREAS.values():
        if not (raiz / tarea.rankings).exists():
            continue
        previos, filas, orden = leer_libro(raiz, tarea), [], Counter()
        for par in pool(raiz, tarea, config):
            orden[par["consulta"]] += 1
            previo = previos.get(juicios.clave(par["consulta"], par["id_global"]), {})
            contexto = ({"id_consulta": consultas_t3[par["consulta"]]["id_global"],
                         "imagen_consulta": ruta_imagen(consultas_t3[par["consulta"]]["id_global"])}
                        if tarea.nombre == "T3" else {"id_consulta": descripciones[par["consulta"]], "imagen_consulta": ""})
            filas.append({**{c: previo.get(c, "") for c in juicios.EDITABLES}, "consulta": par["consulta"],
                          "orden": str(orden[par["consulta"]]), **contexto, "id_candidato": par["id_global"],
                          "imagen_candidato": ruta_imagen(par["id_global"])})
        try:
            escribir_libro(raiz / tarea.workbook, tarea.guia, juicios.HOJA_JUICIOS, juicios.EDITABLES + juicios.CONTEXTO,
                           filas, juicios.EDITABLES, {"justificacion": 50, "id_consulta": 40, "orden": 7},
                           {"relevancia": escala}, juicios.EJEMPLOS if tarea.nombre == "T3" else (["nota"], []),
                           enlaces=("imagen_consulta", "imagen_candidato"))
        except PermissionError:
            print(f"No se pudo escribir {tarea.workbook}: cierre el archivo en Excel.")
            return 1
        escribir_galeria(raiz, tarea, filas, manifiesto_imagenes)
        print(f"Juicios de prueba {tarea.nombre}: {raiz / tarea.workbook} | pares: {len(filas)}, "
              f"juzgados: {sum(bool(f['relevancia']) for f in filas)}")
    return 0


def escribir_galeria(raiz: Path, tarea: Tarea, filas: list[dict[str, str]], manifiesto_imagenes) -> None:
    salida = raiz / tarea.galeria
    secciones = []
    for consulta in sorted({f["consulta"] for f in filas}):
        propias = [f for f in filas if f["consulta"] == consulta]
        if tarea.nombre == "T3":
            q = propias[0]["id_consulta"]
            cabecera = [tarjeta(imagen_evaluacion(raiz, manifiesto_imagenes, q, salida), "", q,
                                [f"<b>CONSULTA {esc(consulta)}</b>", ("m", esc(q))])]
            titulo = f"{consulta}: la primera imagen es la consulta"
        else:
            cabecera, titulo = [], f"{consulta}: {propias[0]['id_consulta']}"
        tarjetas = cabecera + [tarjeta(imagen_evaluacion(raiz, manifiesto_imagenes, f["id_candidato"], salida), "",
                                       f["id_candidato"], [f"<b>orden {esc(f['orden'])}</b>", ("m", esc(f["id_candidato"]))])
                               for f in propias]
        secciones.append((titulo, tarjetas))
    escribir_pagina(salida, f"Juicios de prueba {tarea.nombre}", "Orden al azar, sin sistema ni posicion. Galeria local, no se versiona.",
                    secciones)


def validar_juicios(raiz: Path, tarea: Tarea, config: dict[str, Any]) -> tuple[dict[str, dict[str, int | None]], list[str], int]:
    """Juicios por consulta, errores de validación y pares pendientes. Exporta el CSV si no hay errores."""
    escala = {str(g) for g in config["juicios"]["escala"]} | {juicios.NO_EVALUABLE}
    libro, errores, salida, pendientes = leer_libro(raiz, tarea), [], [], 0
    por_consulta: dict[str, dict[str, int | None]] = defaultdict(dict)
    for par in pool(raiz, tarea, config):
        j = libro.get(juicios.clave(par["consulta"], par["id_global"]), {})
        grado = juicios.relevancia(j.get("relevancia", ""))
        etiqueta = f"{tarea.nombre} {par['consulta']} orden {j.get('orden', '?')}"
        if not grado:
            pendientes += 1
        else:
            if grado not in escala:
                errores.append(f"{etiqueta}: relevancia '{grado}' no es de la escala")
            if grado in ("2", "3") and not j.get("justificacion"):
                errores.append(f"{etiqueta}: un juicio {grado} lleva justificacion")
            if not j.get("evaluador"):
                errores.append(f"{etiqueta}: evaluador vacio")
            if not fecha_valida(j.get("fecha_juicio", "")):
                errores.append(f"{etiqueta}: fecha_juicio vacia o invalida (AAAA-MM-DD)")
            if grado in escala:
                por_consulta[par["consulta"]][par["id_global"]] = None if grado == juicios.NO_EVALUABLE else int(grado)
        salida.append({"consulta": par["consulta"], "id_global": par["id_global"], "relevancia": grado,
                       **{c: j.get(c, "") for c in ("justificacion", "evaluador", "fecha_juicio")}})
    if not errores:
        escribir_csv(raiz / tarea.salida, juicios.COLUMNAS_JUICIOS, salida)
    return por_consulta, errores, pendientes


# --------------------------------------------------------------------------- calculo de resultados


def leer_rankings(ruta: Path) -> dict[str, dict[str, list[tuple[str, float | None]]]]:
    """rankings[consulta][sistema] = [(candidato, score)] en el orden del ranking."""
    salida: dict[str, dict[str, list]] = defaultdict(lambda: defaultdict(list))
    for fila in sorted(leer_csv(ruta), key=lambda f: (f["consulta"], f["sistema"], int(f["rango"]))):
        salida[fila["consulta"]][fila["sistema"]].append((fila["id_global"], float(fila["score"]) if fila["score"] else None))
    return salida


def ordenar(puntajes: dict[str, float | None]) -> list[str]:
    return [i for i, _ in rankings.ordenar(puntajes)]


def variantes(raiz: Path, particion: str, rk: dict[str, dict[str, list]]) -> dict[str, dict[str, list[str]]]:
    """Rankings de las ablaciones y del control negativo (protocolo, sección 7; decisión R32).

    Se calculan sobre las mismas consultas y candidatos que la comparación principal, con los
    scores de los componentes redondeados como se versionan."""
    config, modelos = leer_config_experimento(raiz), leer_config_modelos(raiz)
    pesos_m4 = {c: float(p) for c, p in modelos["m4"]["pesos"].items()}
    pesos_m3 = {b: float(p) for b, p in modelos["m3"]["pesos"].items()}
    bandas = set(config["ejecucion"]["bloques_bandas"])
    galeria = [f["id_global"] for f in leer_csv(raiz / SALIDA_PARTICIONES)]
    anotadas = indexar(leer_csv(congelacion_v21.ruta_congelada(raiz)), "id_global")
    descriptores = {i: m3_estructura.descriptor(anotadas[i]) for i in galeria}
    # Control negativo: cada pieza recibe el descriptor de otra del mismo museo, por una permutación fija.
    generador = np.random.default_rng(int(config["ejecucion"]["semilla_control_negativo"]))
    permutados: dict[str, m3_estructura.Descriptor] = {}
    for museo in sorted({i.split(":")[0] for i in galeria}):
        propias = sorted(i for i in galeria if i.split(":")[0] == museo)
        for origen, destino in zip(propias, generador.permutation(propias)):
            permutados[origen] = descriptores[str(destino)]
    funciones_m3 = {
        "M3 solo bandas": rankings.similitud_m3(descriptores, {b: p if b in bandas else 0.0 for b, p in pesos_m3.items()}, False),
        "M3 sin bandas": rankings.similitud_m3(descriptores, {b: 0.0 if b in bandas else p for b, p in pesos_m3.items()}, False),
        "M3 permutado": rankings.similitud_m3(permutados, pesos_m3, False),
    }
    consultas = indexar([c for c in leer_csv(raiz / SALIDA_CONSULTAS) if c["particion"] == particion], "consulta")
    salida: dict[str, dict[str, list[str]]] = defaultdict(dict)
    for consulta, por_sistema in rk.items():
        q = consultas[consulta]["id_global"]
        componentes = {s: dict(por_sistema[s]) for s in ("M0", "M2", "M3", "M3-sin-orden")}
        candidatos = list(componentes["M2"])
        extra = {}
        for nombre, funcion in funciones_m3.items():
            valores = {c: funcion(q, c) for c in candidatos}
            extra[nombre] = {c: None if v is None else round(v, 6) for c, v in valores.items()}
        base = {c: componentes[c] for c in m4_fusion.COMPONENTES}
        fusiones = {
            "M4 sin M3": m4_fusion.fusionar(base, pesos_m4, excluir=frozenset({"M3"})),
            "M4 sin M0": m4_fusion.fusionar(base, pesos_m4, excluir=frozenset({"M0"})),
            "M4 con M3-sin-orden": m4_fusion.fusionar({**base, "M3": componentes["M3-sin-orden"]}, pesos_m4),
            "Control negativo": m4_fusion.fusionar({**base, "M3": extra["M3 permutado"]}, pesos_m4),
        }
        for nombre, fusion in fusiones.items():
            salida[consulta][nombre] = ordenar({i: f.score for i, f in fusion.items()})
        salida[consulta]["M3 solo bandas"] = ordenar(extra["M3 solo bandas"])
        salida[consulta]["M3 sin bandas"] = ordenar(extra["M3 sin bandas"])
    return salida


def comprobar_h3(rk: dict[str, dict[str, list]], pesos: dict[str, float], k: int, tolerancia: float) -> dict[str, Any]:
    """Reconstrucción e intervención (protocolo, sección 8) en el top k de M4 de cada consulta.

    La intervención se comprueba contra la fórmula escrita aparte: sin el componente retirado, cada
    contribución es α_c / Σ α (de los componentes con evidencia) por el score normalizado."""
    error_reconstruccion = error_version = error_intervencion = 0.0
    resultados = 0
    for consulta, por_sistema in rk.items():
        componentes = {c: dict(por_sistema[c]) for c in m4_fusion.COMPONENTES}
        fusion = m4_fusion.fusionar(componentes, pesos)
        normalizados = {c: m4_fusion.normalizar(componentes[c]) for c in m4_fusion.COMPONENTES}
        versionado = dict(por_sistema["M4"])
        for candidato, _ in por_sistema["M4"][:k]:
            resultados += 1
            f = fusion[candidato]
            error_reconstruccion = max(error_reconstruccion, abs(f.score - sum(f.contribuciones.values())))
            error_version = max(error_version, abs(round(f.score, 6) - (versionado[candidato] or 0.0)))
            for retirado in m4_fusion.COMPONENTES:
                intervenida = m4_fusion.fusionar(componentes, pesos, excluir=frozenset({retirado}))[candidato].score
                disponibles = [c for c in m4_fusion.COMPONENTES if c != retirado and normalizados[c][candidato] is not None]
                total = sum(pesos[c] for c in disponibles)
                esperada = sum(pesos[c] / total * normalizados[c][candidato] for c in disponibles) if total else 0.0
                error_intervencion = max(error_intervencion, abs(intervenida - esperada))
    return {"resultados": resultados, "reconstruccion": error_reconstruccion, "version": error_version,
            "intervencion": error_intervencion,
            "cumple": error_reconstruccion <= tolerancia and error_intervencion <= tolerancia and error_version <= 5e-7}


def completitud(raiz: Path) -> dict[str, str]:
    """Estado de cada pieza según el motivo del revisor: completo, incompleto o sin dato (decisión R32)."""
    estado = {}
    for codigo, fuente in FUENTES.items():
        ruta = raiz / fuente.workbook
        if not ruta.exists():
            continue
        for fila in leer_hoja(ruta, fuente.hoja):
            motivo = fila.get("motivo_revision_original") or fila.get("motivo_revision") or ""
            estado[f"{codigo}:{fila['id_fuente']}"] = analizar_motivo(motivo)["completitud"] or "sin dato"
    return estado


def calcular(raiz: Path, particion: str, rk: dict[str, dict[str, list]],
             juicios_t3: dict[str, dict[str, int | None]]) -> dict[str, Any]:
    """Métricas por consulta, hipótesis, ablaciones, control negativo, H3 y robustez de la tarea T3."""
    config, modelos = leer_config_experimento(raiz), leer_config_modelos(raiz)
    metricas_cfg, ejecucion = config["metricas"], config["ejecucion"]
    k = int(metricas_cfg["k"])
    sistemas = {consulta: {s: [i for i, _ in lista] for s, lista in por_sistema.items()} for consulta, por_sistema in rk.items()}
    for consulta, extra in variantes(raiz, particion, rk).items():
        sistemas[consulta].update(extra)
    nombres = sorted({s for por_sistema in sistemas.values() for s in por_sistema})
    filas, ndcg = [], defaultdict(dict)
    for consulta in sorted(sistemas):
        j = juicios_t3.get(consulta, {})
        for s in nombres:
            ranking = sistemas[consulta][s]
            valor = evaluacion.ndcg(ranking, j, k)
            ndcg[s][consulta] = valor
            filas.append({"tarea": "T3", "consulta": consulta, "sistema": s, "ndcg10": fmt(valor, 6),
                          "p10": fmt(evaluacion.precision(ranking, j, k), 6), "mrr": fmt(evaluacion.rango_reciproco(ranking, j), 6),
                          "juzgada10": fmt(evaluacion.proporcion_juzgada(ranking, j, k), 6)})
    opciones = dict(umbral=float(metricas_cfg["umbral_practico"]), alfa=float(metricas_cfg["alfa"]),
                    confianza=float(metricas_cfg["confianza"]), replicas=int(metricas_cfg["replicas_permutacion"]),
                    semilla_permutacion=int(metricas_cfg["semilla_permutacion"]),
                    semilla_bootstrap=int(metricas_cfg["semilla_bootstrap"]))
    con_bandas = consultas_con_palabra(raiz, particion)
    filtrar = lambda d: {c: v for c, v in d.items() if c in con_bandas}  # noqa: E731
    comparaciones = {
        "H1: M4 frente a M2": evaluacion.comparar(ndcg["M4"], ndcg["M2"], **opciones),
        "H2: M3 frente a M3-sin-orden": evaluacion.comparar(ndcg["M3"], ndcg["M3-sin-orden"], **opciones),
        "H2 secundario: consultas con palabra de bandas": evaluacion.comparar(filtrar(ndcg["M3"]), filtrar(ndcg["M3-sin-orden"]), **opciones),
    }
    exploratorias = {f"M4 frente a {s}": evaluacion.comparar(ndcg["M4"], ndcg[s], **opciones)
                     for s in ("M0", "M1", "M3", "M4-RRF", "M4 sin M3", "M4 sin M0", "M4 con M3-sin-orden", "Control negativo")}
    exploratorias["M3 solo bandas frente a M3 sin bandas"] = evaluacion.comparar(ndcg["M3 solo bandas"], ndcg["M3 sin bandas"], **opciones)
    pesos_m4 = {c: float(p) for c, p in modelos["m4"]["pesos"].items()}
    h3 = comprobar_h3(rk, pesos_m4, k, float(ejecucion["tolerancia_h3"]))
    # Robustez descriptiva: nDCG@10 medio por museo y por completitud de la pieza consultada.
    consultas = indexar([c for c in leer_csv(raiz / SALIDA_CONSULTAS) if c["particion"] == particion], "consulta")
    estado = completitud(raiz)
    grupos = {"museo": {c: consultas[c]["id_global"].split(":")[0] for c in sistemas},
              "completitud": {c: estado.get(consultas[c]["id_global"], "sin dato") for c in sistemas}}
    robustez = {}
    for criterio, asignacion in grupos.items():
        for valor in sorted(set(asignacion.values())):
            propias = [c for c, v in asignacion.items() if v == valor]
            robustez[(criterio, valor)] = (len(propias), {s: media([ndcg[s][c] for c in propias]) for s in ("M2", "M3", "M3-sin-orden", "M4")})
    return {"filas": filas, "ndcg": ndcg, "comparaciones": comparaciones, "exploratorias": exploratorias, "h3": h3,
            "robustez": robustez, "nombres": nombres, "con_bandas": sorted(con_bandas & set(sistemas))}


def media(valores: list[float | None]) -> float | None:
    presentes = [v for v in valores if v is not None]
    return sum(presentes) / len(presentes) if presentes else None


def lineas_comparacion(nombre: str, c: evaluacion.Comparacion) -> list[str]:
    return [nombre, str(c.n), fmt(c.media), fmt(c.intervalo[0]) + " a " + fmt(c.intervalo[1]), fmt(c.p_permutacion, 4),
            fmt(c.p_t, 4), c.decision]


def informe(raiz: Path, r: dict[str, Any], config: dict[str, Any], juicios_t1: dict | None, rk_t1: dict | None,
            pendientes: int) -> list[str]:
    k = config["metricas"]["k"]
    lineas = [
        "# Resultados del test (T3 y T1)",
        "",
        "Generado por `python -m src.experimento.ejecucion_prueba --evaluar`, una sola vez, con los sistemas congelados y los "
        "juicios de prueba hechos sin asistencia (decisiones R27 y R30). Regla de decision del protocolo (seccion 1): una "
        f"hipotesis se sostiene si la diferencia media de nDCG@{k} es >= {config['metricas']['umbral_practico']} y la permutacion "
        f"pareada da p < {config['metricas']['alfa']}; si la diferencia es positiva y p >= {config['metricas']['alfa']}, "
        "«direccion favorable sin evidencia suficiente». El intervalo es descriptivo.",
        "",
        "## Hipotesis confirmatorias",
        "",
    ]
    columnas = ["Comparacion", "Consultas", "Diferencia media", "IC 95 % (bootstrap)", "p permutacion", "p t pareada", "Veredicto"]
    lineas += tabla([lineas_comparacion(n, c) for n, c in r["comparaciones"].items()], columnas)
    excluidas = sorted({e for c in r["comparaciones"].values() for e in c.excluidas})
    lineas += [
        "",
        f"- Consultas sin ningun relevante, excluidas de la media: {len(excluidas)} ({', '.join(excluidas) or 'ninguna'}).",
        f"- Consultas con palabra de bandas (analisis secundario de H2, R27): {len(r['con_bandas'])}.",
        "- Efecto minimo detectable fijado antes del test (R29): 0,087 en H1 (rango 0,060 a 0,159) y 0,026 en H2. Un resultado "
        "no significativo se lee como «no se detecto una mejora de la magnitud detectable», no como ausencia de efecto.",
        "",
        "## H3: fidelidad de la explicacion",
        "",
        f"- Resultados comprobados (top {k} de M4 en cada consulta): {r['h3']['resultados']}.",
        f"- Error maximo de reconstruccion (suma de contribuciones frente a la puntuacion): {r['h3']['reconstruccion']:.2e}.",
        f"- Error maximo de la intervencion (retirar un componente frente a la formula): {r['h3']['intervencion']:.2e}.",
        f"- Diferencia maxima con la puntuacion versionada (redondeada a 6 decimales): {r['h3']['version']:.2e}.",
        f"- Reconstruccion e intervencion: {'se cumplen' if r['h3']['cumple'] else 'NO se cumplen'} con la tolerancia "
        f"{config['ejecucion']['tolerancia_h3']}. La revision humana de 10 resultados se registra en "
        f"`{WORKBOOK_REVISION_H3.as_posix()}` y completa la tercera comprobacion.",
        "",
        "## Comparaciones exploratorias",
        "",
        "Se informan con su intervalo; su valor p no se interpreta como confirmacion.",
        "",
    ]
    lineas += tabla([lineas_comparacion(n, c) for n, c in r["exploratorias"].items()], columnas)
    lineas += ["", f"## nDCG@{k} medio por sistema", ""]
    lineas += tabla([[s, fmt(media(list(r["ndcg"][s].values())))] for s in r["nombres"]], ["Sistema o variante", f"nDCG@{k} medio"])
    lineas += ["", "## Robustez (descriptiva)", ""]
    lineas += tabla([[criterio, valor, str(n)] + [fmt(v) for v in medias.values()]
                     for (criterio, valor), (n, medias) in r["robustez"].items()],
                    ["Criterio", "Grupo", "Consultas", "M2", "M3", "M3-sin-orden", "M4"])
    if rk_t1 is not None:
        lineas += ["", "## T1: texto a imagen (exploratoria, descriptiva)", ""]
        if juicios_t1 is None:
            lineas.append("Los juicios de T1 no estan completos.")
        else:
            filas_t1 = []
            for s in SISTEMAS_T1:
                valores = [evaluacion.ndcg([i for i, _ in rk_t1[c][s]], juicios_t1.get(c, {}), int(k)) for c in rk_t1 if s in rk_t1[c]]
                filas_t1.append([s, str(len(valores)), fmt(media(valores))])
            lineas += tabla(filas_t1, ["Sistema", "Consultas", f"nDCG@{k} medio"])
    lineas += ["", f"Pares de prueba pendientes de juicio: {pendientes}. Metricas por consulta en `{METRICAS}`."]
    return lineas


def evaluar(raiz: Path) -> int:
    config = leer_config_experimento(raiz)
    if not (raiz / RANKINGS_PRUEBA).exists():
        print(f"No existe {RANKINGS_PRUEBA}: el test no se ha ejecutado.")
        return 1
    juicios_t3, errores, pendientes = validar_juicios(raiz, TAREAS["T3"], config)
    juicios_t1, rk_t1 = None, None
    if (raiz / RANKINGS_T1).exists():
        rk_t1 = leer_rankings(raiz / RANKINGS_T1)
        por_t1, errores_t1, pendientes_t1 = validar_juicios(raiz, TAREAS["T1"], config)
        errores += errores_t1
        juicios_t1 = por_t1 if not pendientes_t1 else None
    if errores or pendientes:
        print(f"Juicios de prueba con {len(errores)} errores y {pendientes} pares de T3 pendientes: no se calculan resultados.")
        for error in errores[:20]:
            print(f"- {error}")
        return 1
    r = calcular(raiz, "prueba", leer_rankings(raiz / RANKINGS_PRUEBA), juicios_t3)
    escribir_csv(raiz / METRICAS, COLUMNAS_METRICAS, r["filas"])
    escribir_texto(raiz / REPORTE, informe(raiz, r, config, juicios_t1, rk_t1, pendientes))
    print(f"Resultados del test -> {REPORTE}")
    return 0


# --------------------------------------------------------------------------- principal


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Ejecucion unica del test del protocolo experimental v2.")
    parser.add_argument("--root", default=".", help="Raiz del repositorio.")
    grupo = parser.add_mutually_exclusive_group(required=True)
    grupo.add_argument("--comprobar", action="store_true", help="Condiciones de suspension, sin ejecutar nada.")
    grupo.add_argument("--rankings", action="store_true", help="Una sola vez: manifiesto y rankings de prueba.")
    grupo.add_argument("--crear-juicios", action="store_true", help="Libros ciegos de juicios de prueba (conserva lo juzgado).")
    grupo.add_argument("--evaluar", action="store_true", help="Valida los juicios y calcula los resultados.")
    args = parser.parse_args(argv)
    raiz = Path(args.root).resolve()
    if args.comprobar:
        problemas = comprobar(raiz)
        print("Comprobacion previa del test: " + ("sin problemas." if not problemas else f"{len(problemas)} problemas."))
        for problema in problemas:
            print(f"- {problema}")
        return 0 if not problemas else 1
    if args.rankings:
        return ejecutar_rankings(raiz)
    if args.crear_juicios:
        return crear_juicios(raiz)
    return evaluar(raiz)


if __name__ == "__main__":
    raise SystemExit(main())
