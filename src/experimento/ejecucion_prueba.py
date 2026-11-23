"""Ejecución única del test: comprobación previa, corrida sellada por estados, juicios ciegos y evaluación.

Uso desde la raíz del repositorio, en este orden (protocolo experimental v2, secciones 6 a 9):

    python -m src.experimento.ejecucion_prueba --comprobar           # condiciones de suspensión; no ejecuta nada
    python -m src.modelos.m2_openclip --textos-t1                    # vectores de texto de las consultas T1 (torch)
    python -m src.experimento.ejecucion_prueba --rankings            # sella los insumos; luego rankings y pool
    python -m src.experimento.ejecucion_prueba --crear-juicios       # libros ciegos de juicios de prueba (T3 y T1)
    python -m src.experimento.ejecucion_prueba --cerrar-juicios      # valida, exporta y sella los juicios
    python -m src.experimento.ejecucion_prueba --crear-revision-h3   # fichas ciegas de la revisión descriptiva
    python -m src.experimento.ejecucion_prueba --evaluar             # comprueba las huellas y calcula los resultados

Ningún paso de este módulo forma parte del flujo. La primera condición es que el protocolo esté
autorizado: `[ejecucion] aprobacion_protocolo` de config/experimento.toml no puede estar vacío, y
la suma SHA-256 del protocolo debe coincidir con la registrada al autorizarlo (decisión R30).

La corrida avanza por estados (decisión R37), registrados en el manifiesto de ejecución:
`autorizada`, `insumos_sellados`, `rankings_sellados`, `juicios_cerrados` y `evaluada`. El
manifiesto se escribe antes de calcular ningún ranking. Cada paso escribe en archivos temporales y
los publica al terminar, junto con el manifiesto actualizado; un fallo no deja salidas parciales con
el nombre definitivo. Si una huella sellada no coincide, la corrida queda `suspendida`.

Las funciones de cálculo reciben la partición como parámetro para poder probarse con los datos de
desarrollo. La línea de órdenes solo usa la partición de prueba. El evaluador no abre los rankings,
el pool, la muestra de la revisión de H3 ni el informe de resultados hasta terminar todos los juicios.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
from collections import Counter, defaultdict
from collections.abc import Callable, Iterable
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any

import numpy as np
from openpyxl import load_workbook

from src.anotacion import aplicar_anotaciones_v2 as exportacion
from src.anotacion import buena_formacion, congelacion_v21
from src.anotacion.aplicar_anotaciones import fecha_valida
from src.anotacion.corpus_v2 import SALIDA_PRINCIPAL_V2
from src.anotacion.nucleo import huella
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
POOL_PRUEBA = "data/processed/experimento_v2_pool_prueba.csv"
POOL_T1 = "data/processed/experimento_v2_pool_t1.csv"
MANIFIESTO_EJECUCION = "data/processed/experimento_v2_manifiesto_ejecucion.json"
EMBEDDINGS_T1 = Path("data/metadata/m2_openclip_t1_v2.npy")
INDICE_T1 = Path("data/metadata/m2_openclip_t1_indice_v2.csv")
METRICAS = "data/processed/experimento_v2_metricas_por_consulta.csv"
REPORTE = "outputs/reports/experimento_v2_resultados.md"
WORKBOOK_REVISION_H3 = Path("data/metadata/revision_h3_v2.xlsx")
SALIDA_REVISION_H3 = "data/metadata/revision_h3_v2.csv"
MUESTRA_H3 = "data/processed/experimento_v2_revision_h3_muestra.csv"
REGISTRO_CUSTODIA = "docs/registro_custodia.md"
COLUMNAS_METRICAS = ["tarea", "consulta", "sistema", "ndcg10", "p10", "mrr", "juzgada10"]
COLUMNAS_POOL = ["consulta", "id_global", "origen"]
SISTEMAS_T1 = ("M0", "M2", "M3", "M4")
SISTEMAS_POOL = ("M0", "M1", "M2", "M3", "M3-sin-orden", "M4", "M4-RRF")

ESTADOS = ("autorizada", "insumos_sellados", "rankings_sellados", "juicios_cerrados", "evaluada")
SUSPENDIDA = "suspendida"
DESCRIPTIVA = "descriptiva: subgrupo de bandas (R33)"

# Cegamiento (R38): columnas que un libro de juicios nunca puede tener.
PROHIBIDAS = ("sistema", "origen", "score", "puntuacion", "rango", "posicion", "clase", "grado")

# Revisión humana de las explicaciones de M4 (R36): descriptiva, ciega a la clase, al grado y a la posición.
VALORACIONES_H3 = ("correcta", "incorrecta", "especulativa", "no_evaluable")
EDITABLES_H3 = ["valoracion", "comentario", "evaluador", "fecha_revision"]
CONTEXTO_H3 = ["ficha", "id_consulta", "imagen_consulta", "id_candidato", "imagen_candidato", "explicacion"]
PROCEDENCIA = {"M0": "texto de la ficha (BM25)", "M2": "imagen y texto (OpenCLIP)", "M3": "anotacion congelada v2.1"}


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
    "Despues: python -m src.experimento.ejecucion_prueba --cerrar-juicios valida los juicios y los sella.",
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

GUIA_H3 = [
    "Revision de las explicaciones de M4 (protocolo experimental v2, seccion 8; decision R36)",
    "",
    "Analisis descriptivo: no interviene en el veredicto de H3. Cada ficha muestra una consulta, un candidato y como",
    "se compone su puntuacion: el peso efectivo de cada componente por su puntuacion normalizada. La ficha no dice si",
    "el candidato fue juzgado relevante ni en que posicion quedo; el orden es al azar.",
    "",
    "  correcta     = las contribuciones corresponden a lo que se ve en las dos imagenes.",
    "  incorrecta   = alguna contribucion alta o baja contradice lo que se ve.",
    "  especulativa = la explicacion atribuye a un componente un rasgo que no se puede verificar en las imagenes.",
    "  no_evaluable = las imagenes no permiten decidir.",
    "",
    "Complete evaluador y fecha_revision (AAAA-MM-DD). Despues: python -m src.experimento.ejecucion_prueba --evaluar.",
]

TAREAS = {
    "T3": Tarea("T3", RANKINGS_PRUEBA, POOL_PRUEBA,
                Path("data/metadata/juicios_prueba_v2.xlsx"), "data/metadata/juicios_prueba_v2.csv",
                Path(CARPETA) / "juicios_prueba_v2_galeria.html", GUIA_T3),
    "T1": Tarea("T1", RANKINGS_T1, POOL_T1,
                Path("data/metadata/juicios_t1_v2.xlsx"), "data/metadata/juicios_t1_v2.csv",
                Path(CARPETA) / "juicios_t1_v2_galeria.html", GUIA_T1),
}


def sha256(ruta: Path) -> str:
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def fmt(x: float | None, d: int = 3) -> str:
    return "—" if x is None or x != x else f"{x:.{d}f}"


# --------------------------------------------------------------------------- comprobacion previa


def aprobado(raiz: Path) -> bool:
    """El protocolo está autorizado y no cambió después de autorizarlo."""
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
    if antes_de_rankings:
        man = leer_manifiesto(raiz)
        if man is not None and estado_actual(man) == SUSPENDIDA:
            problemas.append(f"La corrida {man.get('corrida', '')} esta suspendida: {man['estados'][-1].get('motivo', '')}")
        elif man is not None and estado_actual(man) not in ESTADOS[:2]:
            problemas.append(f"La corrida {man.get('corrida', '')} ya paso por {estado_actual(man)}: el test se ejecuta una sola vez.")
        if (raiz / RANKINGS_PRUEBA).exists():
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


# --------------------------------------------------------------------------- corrida, manifiesto y custodia


def git(raiz: Path, *argumentos: str) -> str:
    ejecutable = shutil.which("git")
    if ejecutable is None:
        return ""
    try:
        return subprocess.run([ejecutable, *argumentos], cwd=raiz, capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return ""


def identificador_corrida(config: dict[str, Any]) -> str:
    """Identificador estable de la corrida: depende solo de la autorización registrada."""
    ejecucion = config.get("ejecucion", {})
    base = f"{ejecucion.get('aprobacion_protocolo', '')}|{ejecucion.get('sha256_protocolo', '')}"
    return "corrida-" + hashlib.sha256(base.encode("utf-8")).hexdigest()[:12]


def insumos_obligatorios(raiz: Path) -> list[str]:
    """Insumos que se sellan antes de los rankings. Todos son obligatorios: ninguno se omite en silencio."""
    rutas = [SALIDA_PARTICIONES, SALIDA_CONSULTAS, SALIDA_T1, SALIDA_PRINCIPAL_V2, MANIFIESTO_EVALUACION,
             congelacion_v21.ruta_congelada(raiz).relative_to(raiz).as_posix(), str(m1_vision.CARACTERISTICAS_M1),
             str(m1_vision.INDICE_M1), str(EMBEDDINGS_M2), str(INDICE_M2), str(MANIFIESTO_M2), str(EMBEDDINGS_T1),
             str(INDICE_T1), juicios.SALIDA_JUICIOS, PROTOCOLO.as_posix(), CONFIG_EXPERIMENTO.as_posix(),
             CONFIG_MODELOS.as_posix()]
    return [Path(r).as_posix() for r in rutas]


def huellas(raiz: Path, rutas: Iterable[str]) -> dict[str, str]:
    """Suma SHA-256 de cada ruta; un archivo ausente es un error, no se omite."""
    faltan = [r for r in rutas if not (raiz / r).exists()]
    if faltan:
        raise FileNotFoundError("Faltan insumos obligatorios: " + ", ".join(faltan))
    return {r: sha256(raiz / r) for r in rutas}


def leer_manifiesto(raiz: Path) -> dict[str, Any] | None:
    ruta = raiz / MANIFIESTO_EJECUCION
    return json.loads(ruta.read_text(encoding="utf-8")) if ruta.exists() else None


def estado_actual(man: dict[str, Any]) -> str:
    return man["estados"][-1]["estado"] if man.get("estados") else ""


def sellados(man: dict[str, Any]) -> dict[str, str]:
    """Todas las huellas registradas en los estados de la corrida."""
    salida: dict[str, str] = {}
    for estado in man.get("estados", []):
        salida.update(estado.get("sha256", {}))
    return salida


def verificar(raiz: Path, requerido: str) -> tuple[dict[str, Any] | None, list[str]]:
    """Comprueba que la corrida existe, no está suspendida, llegó a `requerido` y que cada huella coincide."""
    config = leer_config_experimento(raiz)
    man = leer_manifiesto(raiz)
    if man is None:
        return None, [f"Falta el manifiesto de ejecucion ({MANIFIESTO_EJECUCION}): la corrida no se puede continuar."]
    problemas = []
    actual = estado_actual(man)
    if actual == SUSPENDIDA:
        return man, [f"La corrida esta suspendida: {man['estados'][-1].get('motivo', '')}"]
    nombres = [e["estado"] for e in man.get("estados", [])]
    if nombres != list(ESTADOS[:len(nombres)]):
        problemas.append(f"Los estados de la corrida no siguen el orden del protocolo: {', '.join(nombres)}.")
    if requerido not in nombres:
        problemas.append(f"La corrida esta en {actual or 'ningun estado'}; este paso exige {requerido}.")
    if man.get("corrida") != identificador_corrida(config):
        problemas.append("El manifiesto es de otra corrida: su identificador no coincide con la autorizacion registrada.")
    for ruta, suma in sorted(sellados(man).items()):
        if not (raiz / ruta).exists():
            problemas.append(f"Falta un archivo sellado: {ruta}")
        elif sha256(raiz / ruta) != suma:
            problemas.append(f"La huella de {ruta} no coincide con la sellada.")
    return man, problemas


def temporal(destino: Path) -> Path:
    """Archivo temporal junto al destino, con la misma extensión (openpyxl la exige al leer)."""
    return destino.with_name(destino.stem + ".tmp" + destino.suffix)


def publicar(raiz: Path, escrituras: list[tuple[str, Callable[[Path], None]]],
             manifiesto_nuevo: Callable[[dict[str, str]], dict[str, Any]] | None = None) -> None:
    """Escribe cada salida en un temporal y, si todas se escriben, las publica y luego el manifiesto.

    `manifiesto_nuevo` recibe las huellas de las salidas (calculadas sobre los temporales) y devuelve
    el manifiesto actualizado, que se publica al final. Si algo falla antes de publicar, se borran
    los temporales y ningún archivo definitivo cambia (gestión de fallos, protocolo sección 9)."""
    temporales: list[tuple[Path, Path]] = []
    try:
        for ruta, escribir in escrituras:
            destino = raiz / ruta
            destino.parent.mkdir(parents=True, exist_ok=True)
            tmp = temporal(destino)
            escribir(tmp)
            temporales.append((tmp, destino))
        if manifiesto_nuevo is not None:
            sumas = {ruta: sha256(tmp) for (ruta, _), (tmp, _) in zip(escrituras, temporales)}
            destino = raiz / MANIFIESTO_EJECUCION
            tmp = temporal(destino)
            escribir_json(tmp, manifiesto_nuevo(sumas))
            temporales.append((tmp, destino))
    except BaseException:
        for tmp, _ in temporales:
            tmp.unlink(missing_ok=True)
        raise
    for tmp, destino in temporales:
        os.replace(tmp, destino)


def con_estado(man: dict[str, Any], estado: str, sumas: dict[str, str], **extra: Any) -> dict[str, Any]:
    return {**man, "estados": [*man["estados"], {"estado": estado, "sha256": dict(sorted(sumas.items())), **extra}]}


def suspender(raiz: Path, man: dict[str, Any], motivo: str) -> None:
    """Marca la corrida como suspendida; ningún paso posterior se ejecuta sin la conformidad del asesor."""
    publicar(raiz, [], lambda _: {**man, "estados": [*man["estados"], {"estado": SUSPENDIDA, "motivo": motivo}]})


def manifiesto_inicial(raiz: Path) -> dict[str, Any]:
    """Estados `autorizada` e `insumos_sellados`: commit, huellas de los insumos, checkpoint, parámetros y equipo."""
    config, modelos = leer_config_experimento(raiz), leer_config_modelos(raiz)
    m2 = json.loads((raiz / MANIFIESTO_M2).read_text(encoding="utf-8"))
    commit = git(raiz, "rev-parse", "HEAD")
    return {
        "corrida": identificador_corrida(config),
        "estados": [
            {"estado": "autorizada", "aprobacion_protocolo": config["ejecucion"]["aprobacion_protocolo"],
             "sha256": {PROTOCOLO.as_posix(): config["ejecucion"]["sha256_protocolo"]}},
            {"estado": "insumos_sellados", "commit": commit,
             "arbol_limpio": git(raiz, "status", "--porcelain", "--untracked-files=no") == "",
             "sha256": huellas(raiz, insumos_obligatorios(raiz))},
        ],
        "checkpoint_m2": {c: m2.get(c, "") for c in ("arquitectura", "pesos", "sha256_pesos", "encuadre", "precision")},
        "parametros": {"experimento": config, "modelos": modelos},
        "entorno": {"python": sys.version.split()[0], "plataforma": platform.platform(), "numpy": np.__version__},
    }


def imprimir_custodia(man: dict[str, Any]) -> None:
    """Líneas para docs/registro_custodia.md y para el correo al asesor (R37)."""
    ultimo = man["estados"][-1]
    print(f"Para {REGISTRO_CUSTODIA} y el correo al asesor: corrida {man['corrida']}, estado {ultimo['estado']}.")
    for ruta, suma in ultimo.get("sha256", {}).items():
        print(f"  {suma}  {ruta}")


# --------------------------------------------------------------------------- rankings


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


def pool(raiz: Path, tarea: Tarea, config: dict[str, Any], ruta_rankings: str | None = None) -> list[dict[str, str]]:
    """Pool de una tarea a partir de un archivo de rankings (por defecto, el publicado)."""
    base = set(config["ejecucion"]["sistemas_muestra_azar_t1"]) if tarea.nombre == "T1" else None
    return juicios.construir_pool(raiz, config, ruta_rankings or tarea.rankings, base)


def ejecutar_rankings(raiz: Path) -> int:
    """Sella los insumos (manifiesto antes que nada), calcula los rankings y el pool y los sella."""
    problemas = comprobar(raiz)
    faltan = [r for r in insumos_obligatorios(raiz) if not (raiz / r).exists()]
    if faltan:
        problemas.append(f"Faltan insumos obligatorios: {', '.join(faltan)}"
                         + (" (vectores T1: python -m src.modelos.m2_openclip --textos-t1)" if str(EMBEDDINGS_T1.as_posix()) in faltan else ""))
    if not problemas and not git(raiz, "rev-parse", "HEAD"):
        problemas.append("No se pudo leer el commit: el manifiesto debe registrarlo.")
    if problemas:
        print("El test no se abre:")
        for problema in problemas:
            print(f"- {problema}")
        return 1
    config = leer_config_experimento(raiz)
    man = leer_manifiesto(raiz)
    if man is None:
        man = manifiesto_inicial(raiz)
        if not man["estados"][1]["arbol_limpio"]:
            print("El test no se abre: hay cambios sin commit en archivos versionados; el commit sellado no los incluiria.")
            return 1
        publicar(raiz, [], lambda _: man)
        print(f"Insumos sellados -> {MANIFIESTO_EJECUCION}")
        imprimir_custodia(man)
    else:
        # Un fallo anterior dejó la corrida en insumos_sellados: se repite con los mismos insumos.
        man, problemas = verificar(raiz, "insumos_sellados")
        if problemas:
            print("El test no se abre:")
            for problema in problemas:
                print(f"- {problema}")
            return 1
    filas_t3, sistemas, _ = rankings.rankings_t3(raiz, "prueba")
    filas_t1 = rankings_t1(raiz)
    escribir = lambda filas, columnas: (lambda ruta: escribir_csv(ruta, columnas, filas))  # noqa: E731

    def escribir_pool(tarea: Tarea) -> Callable[[Path], None]:
        # El pool se construye con el temporal de los rankings, ya escrito en el paso anterior de `publicar`.
        rk_temporal = temporal(raiz / tarea.rankings).relative_to(raiz).as_posix()
        return lambda ruta: escribir_csv(ruta, COLUMNAS_POOL, pool(raiz, tarea, config, rk_temporal))

    publicar(raiz, [(RANKINGS_PRUEBA, escribir(filas_t3, rankings.COLUMNAS)), (RANKINGS_T1, escribir(filas_t1, rankings.COLUMNAS)),
                    (POOL_PRUEBA, escribir_pool(TAREAS["T3"])), (POOL_T1, escribir_pool(TAREAS["T1"]))],
             lambda sumas: con_estado(man, "rankings_sellados", sumas))
    man = leer_manifiesto(raiz)
    print(f"Rankings de prueba sellados: T3 ({', '.join(sistemas)}) y T1. No abra los rankings ni el pool: siga con --crear-juicios.")
    imprimir_custodia(man)
    return 0


def abortar(raiz: Path, man: dict[str, Any] | None, problemas: list[str], suspendible: bool = True) -> int:
    """Informa los problemas y, si una huella no coincide o falta un archivo sellado, suspende la corrida."""
    print("La corrida no puede continuar:")
    for problema in problemas:
        print(f"- {problema}")
    if suspendible and man is not None and estado_actual(man) != SUSPENDIDA and any(
            "huella" in p or "Falta un archivo sellado" in p or "otra corrida" in p or "orden del protocolo" in p for p in problemas):
        suspender(raiz, man, "; ".join(problemas))
        print("Corrida suspendida: informe al asesor antes de repetir ningun paso (protocolo, seccion 9).")
    return 1


# --------------------------------------------------------------------------- juicios de prueba y cegamiento


def leer_libro(raiz: Path, tarea: Tarea) -> dict[str, dict[str, str]]:
    ruta = raiz / tarea.workbook
    if not ruta.exists():
        return {}
    return {juicios.clave(f["consulta"], f["id_candidato"]): f for f in leer_hoja(ruta, juicios.HOJA_JUICIOS, clave="consulta")}


def encabezados_libro(ruta: Path, hoja: str) -> list[str]:
    libro = load_workbook(ruta, read_only=True)
    try:
        return [str(c) for c in next(libro[hoja].iter_rows(values_only=True)) if c is not None]
    finally:
        libro.close()


def validar_cegamiento(encabezados: list[str], filas: list[dict[str, str]], pares: list[dict[str, str]]) -> list[str]:
    """El libro no lleva sistema, puntuación ni posición, y conserva el orden de presentación sorteado (R38).

    `pares` es el pool sellado, en el orden sorteado; `filas`, las filas del libro en su orden."""
    errores = []
    prohibidas = [c for c in encabezados if any(p in c.lower() for p in PROHIBIDAS)]
    if prohibidas:
        errores.append(f"El libro tiene columnas que rompen el cegamiento: {', '.join(prohibidas)}")
    ajenas = [c for c in encabezados if c not in juicios.EDITABLES + juicios.CONTEXTO]
    if ajenas:
        errores.append(f"El libro tiene columnas no previstas: {', '.join(ajenas)}")
    esperado: dict[str, list[str]] = defaultdict(list)
    for par in pares:
        esperado[par["consulta"]].append(par["id_global"])
    presentes: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for fila in filas:
        presentes[fila["consulta"]].append((fila["id_candidato"], str(fila["orden"])))
    for consulta in sorted(set(esperado) | set(presentes)):
        ids = [i for i, _ in presentes[consulta]]
        if ids != esperado[consulta]:
            errores.append(f"{consulta}: el orden de presentacion no es el sorteado o faltan pares.")
        if [o for _, o in presentes[consulta]] != [str(n) for n in range(1, len(ids) + 1)]:
            errores.append(f"{consulta}: la columna orden no numera 1..n en el orden de presentacion.")
    return errores


def filas_libro(raiz: Path, tarea: Tarea, pares: list[dict[str, str]]) -> list[dict[str, str]]:
    """Filas del libro ciego: solo la consulta, las imágenes, el orden sorteado y lo ya juzgado."""
    manifiesto_imagenes = indexar(leer_csv(raiz / MANIFIESTO_EVALUACION), "id_global")
    ruta_imagen = lambda i: "../" + manifiesto_imagenes.get(i, {}).get("ruta_copia_evaluacion", "").removeprefix("data/")  # noqa: E731
    descripciones = {f["consulta"]: f["descripcion"] for f in leer_csv(raiz / SALIDA_T1)} if tarea.nombre == "T1" else {}
    consultas_t3 = indexar(leer_csv(raiz / SALIDA_CONSULTAS), "consulta") if tarea.nombre == "T3" else {}
    previos, filas, orden = leer_libro(raiz, tarea), [], Counter()
    for par in pares:
        orden[par["consulta"]] += 1
        previo = previos.get(juicios.clave(par["consulta"], par["id_global"]), {})
        contexto = ({"id_consulta": consultas_t3[par["consulta"]]["id_global"],
                     "imagen_consulta": ruta_imagen(consultas_t3[par["consulta"]]["id_global"])}
                    if tarea.nombre == "T3" else {"id_consulta": descripciones[par["consulta"]], "imagen_consulta": ""})
        filas.append({**{c: previo.get(c, "") for c in juicios.EDITABLES}, "consulta": par["consulta"],
                      "orden": str(orden[par["consulta"]]), **contexto, "id_candidato": par["id_global"],
                      "imagen_candidato": ruta_imagen(par["id_global"])})
    return filas


def escribir_libro_juicios(raiz: Path, tarea: Tarea, filas: list[dict[str, str]], config: dict[str, Any], ruta: Path) -> None:
    escala = [str(g) for g in config["juicios"]["escala"]] + [juicios.NO_EVALUABLE]
    escribir_libro(ruta, tarea.guia, juicios.HOJA_JUICIOS, juicios.EDITABLES + juicios.CONTEXTO,
                   filas, juicios.EDITABLES, {"justificacion": 50, "id_consulta": 40, "orden": 7},
                   {"relevancia": escala}, juicios.EJEMPLOS if tarea.nombre == "T3" else (["nota"], []),
                   enlaces=("imagen_consulta", "imagen_candidato"))


def cegamiento_del_libro(raiz: Path, tarea: Tarea, ruta: Path | None = None) -> list[str]:
    """Valida el libro escrito en disco contra el pool sellado."""
    ruta = ruta or raiz / tarea.workbook
    filas = leer_hoja(ruta, juicios.HOJA_JUICIOS, clave="consulta")
    return validar_cegamiento(encabezados_libro(ruta, juicios.HOJA_JUICIOS), filas, leer_csv(raiz / tarea.pool))


def crear_juicios(raiz: Path) -> int:
    man, problemas = verificar(raiz, "rankings_sellados")
    if not problemas and estado_actual(man) != "rankings_sellados":
        problemas.append(f"La corrida ya esta en {estado_actual(man)}: los libros de juicios ya se cerraron.")
    if problemas:
        return abortar(raiz, man, problemas)
    config = leer_config_experimento(raiz)
    manifiesto_imagenes = indexar(leer_csv(raiz / MANIFIESTO_EVALUACION), "id_global")
    for tarea in TAREAS.values():
        pares = leer_csv(raiz / tarea.pool)
        filas = filas_libro(raiz, tarea, pares)
        errores = validar_cegamiento(juicios.EDITABLES + juicios.CONTEXTO, filas, pares)
        if errores:
            return abortar(raiz, man, errores, suspendible=False)
        try:
            publicar(raiz, [(tarea.workbook.as_posix(), lambda ruta, f=filas, t=tarea: escribir_libro_juicios(raiz, t, f, config, ruta))])
        except PermissionError:
            print(f"No se pudo escribir {tarea.workbook}: cierre el archivo en Excel.")
            return 1
        errores = cegamiento_del_libro(raiz, tarea)
        if errores:
            return abortar(raiz, man, errores, suspendible=False)
        escribir_galeria(raiz, tarea, filas, manifiesto_imagenes)
        print(f"Juicios de prueba {tarea.nombre}: {raiz / tarea.workbook} | pares: {len(filas)}, "
              f"juzgados: {sum(bool(f['relevancia']) for f in filas)}. Cegamiento comprobado.")
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


def validar_juicios(raiz: Path, tarea: Tarea, config: dict[str, Any]) -> tuple[list[dict[str, str]], list[str], int]:
    """Filas exportables de los juicios de una tarea, errores de validación y pares pendientes."""
    escala = {str(g) for g in config["juicios"]["escala"]} | {juicios.NO_EVALUABLE}
    libro, errores, salida, pendientes = leer_libro(raiz, tarea), [], [], 0
    for par in leer_csv(raiz / tarea.pool):
        j = libro.get(juicios.clave(par["consulta"], par["id_global"]), {})
        grado = juicios.relevancia(j.get("relevancia", ""))
        etiqueta = f"{tarea.nombre} {par['consulta']} orden {j.get('orden', '?')}"
        if not j:
            errores.append(f"{etiqueta}: el par {par['id_global']} del pool sellado no esta en el libro")
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
        salida.append({"consulta": par["consulta"], "id_global": par["id_global"], "relevancia": grado,
                       **{c: j.get(c, "") for c in ("justificacion", "evaluador", "fecha_juicio")}})
    return salida, errores, pendientes


def leer_juicios_sellados(ruta: Path) -> dict[str, dict[str, int | None]]:
    """Juicios exportados por consulta: grado entero, o None si el par es `no_evaluable`."""
    por_consulta: dict[str, dict[str, int | None]] = defaultdict(dict)
    for f in leer_csv(ruta):
        por_consulta[f["consulta"]][f["id_global"]] = None if f["relevancia"] == juicios.NO_EVALUABLE else int(f["relevancia"])
    return por_consulta


def cerrar_juicios(raiz: Path) -> int:
    """Valida los libros completos, comprueba de nuevo el cegamiento, exporta y sella los juicios."""
    man, problemas = verificar(raiz, "rankings_sellados")
    if not problemas and estado_actual(man) != "rankings_sellados":
        problemas.append(f"La corrida ya esta en {estado_actual(man)}.")
    if problemas:
        return abortar(raiz, man, problemas)
    config = leer_config_experimento(raiz)
    escrituras, errores_totales, cegamiento = [], [], {}
    for tarea in TAREAS.values():
        if not (raiz / tarea.workbook).exists():
            errores_totales.append(f"No existe {tarea.workbook}: ejecute antes --crear-juicios.")
            continue
        filas, errores, pendientes = validar_juicios(raiz, tarea, config)
        errores += cegamiento_del_libro(raiz, tarea)
        if pendientes:
            errores.append(f"{tarea.nombre}: {pendientes} pares sin juicio.")
        errores_totales += errores
        cegamiento[tarea.nombre] = "sin problemas" if not errores else "con problemas"
        escrituras.append((tarea.salida, lambda ruta, f=filas: escribir_csv(ruta, juicios.COLUMNAS_JUICIOS, f)))
    if errores_totales:
        print(f"Juicios de prueba con {len(errores_totales)} problemas: no se cierran.")
        for error in errores_totales[:20]:
            print(f"- {error}")
        return 1
    libros = huellas(raiz, [t.workbook.as_posix() for t in TAREAS.values()])
    publicar(raiz, escrituras, lambda sumas: con_estado(man, "juicios_cerrados", {**sumas, **libros}, cegamiento=cegamiento))
    print("Juicios de prueba cerrados y sellados. Siga con --crear-revision-h3 y luego --evaluar.")
    imprimir_custodia(leer_manifiesto(raiz))
    return 0


# --------------------------------------------------------------------------- revision humana de H3 (descriptiva)


def clase_h3(grado: int | None) -> str | None:
    """Acierto: top 10 de M4 con grado >= 2; error: grado 0 o 1; `no_evaluable` no entra (R36)."""
    if grado is None:
        return None
    return "acierto" if grado >= 2 else "error"


def muestra_revision_h3(rk: dict[str, dict[str, list]], juicios_t3: dict[str, dict[str, int | None]],
                        config: dict[str, Any]) -> tuple[list[dict[str, str]], dict[str, int]]:
    """Sorteo de aciertos y errores del top k de M4, con semilla; si una clase tiene menos, se usan todos.

    Devuelve la muestra en orden de presentación aleatorio y el número disponible en cada clase."""
    ejecucion, k = config["ejecucion"], int(config["metricas"]["k"])
    semilla = int(ejecucion["semilla_revision_h3"])
    cuotas = {"acierto": int(ejecucion["revision_h3_aciertos"]), "error": int(ejecucion["revision_h3_errores"])}
    por_clase: dict[str, list[tuple[str, str]]] = {"acierto": [], "error": []}
    for consulta in sorted(rk):
        for candidato, _ in rk[consulta]["M4"][:k]:
            if candidato not in juicios_t3.get(consulta, {}):
                continue
            clase = clase_h3(juicios_t3[consulta][candidato])
            if clase is not None:
                por_clase[clase].append((consulta, candidato))
    muestra = []
    for clase, pares in por_clase.items():
        sorteados = sorted(pares, key=lambda p: huella(semilla, f"h3:{clase}", f"{p[0]}|{p[1]}"))[:cuotas[clase]]
        muestra += [{"consulta": c, "id_global": i, "clase": clase} for c, i in sorteados]
    muestra.sort(key=lambda f: huella(semilla, "h3:orden", f"{f['consulta']}|{f['id_global']}"))
    for n, fila in enumerate(muestra, start=1):
        fila["ficha"] = f"F{n:02d}"
    return muestra, {c: len(p) for c, p in por_clase.items()}


def explicacion(por_sistema: dict[str, list], candidato: str, pesos: dict[str, float]) -> str:
    """Descomposición de la puntuación de M4 de un candidato: peso efectivo por puntuación normalizada."""
    componentes = {c: dict(por_sistema[c]) for c in m4_fusion.COMPONENTES}
    normalizados = {c: m4_fusion.normalizar(componentes[c]) for c in m4_fusion.COMPONENTES}
    fusion = m4_fusion.fusionar(componentes, pesos)[candidato]
    partes = []
    for c in m4_fusion.COMPONENTES:
        if c in fusion.contribuciones:
            partes.append(f"{c} ({PROCEDENCIA[c]}): {fusion.pesos[c]:.3f} x {normalizados[c][candidato]:.3f} = "
                          f"{fusion.contribuciones[c]:.3f}")
        else:
            partes.append(f"{c} ({PROCEDENCIA[c]}): sin evidencia; su peso se reparte entre los demas")
    return "; ".join(partes) + f". Total: {fusion.score:.3f}"


def crear_revision_h3(raiz: Path) -> int:
    man, problemas = verificar(raiz, "juicios_cerrados")
    if not problemas and estado_actual(man) != "juicios_cerrados":
        problemas.append(f"La corrida ya esta en {estado_actual(man)}.")
    if problemas:
        return abortar(raiz, man, problemas)
    config, modelos = leer_config_experimento(raiz), leer_config_modelos(raiz)
    rk = leer_rankings(raiz / RANKINGS_PRUEBA)
    muestra, disponibles = muestra_revision_h3(rk, leer_juicios_sellados(raiz / TAREAS["T3"].salida), config)
    pesos = {c: float(p) for c, p in modelos["m4"]["pesos"].items()}
    consultas = indexar(leer_csv(raiz / SALIDA_CONSULTAS), "consulta")
    manifiesto_imagenes = indexar(leer_csv(raiz / MANIFIESTO_EVALUACION), "id_global")
    ruta_imagen = lambda i: "../" + manifiesto_imagenes.get(i, {}).get("ruta_copia_evaluacion", "").removeprefix("data/")  # noqa: E731
    previos = ({f["ficha"]: f for f in leer_hoja(raiz / WORKBOOK_REVISION_H3, "revision", clave="ficha")}
               if (raiz / WORKBOOK_REVISION_H3).exists() else {})
    fichas = []
    for fila in muestra:
        q = consultas[fila["consulta"]]["id_global"]
        fichas.append({**{c: previos.get(fila["ficha"], {}).get(c, "") for c in EDITABLES_H3}, "ficha": fila["ficha"],
                       "id_consulta": q, "imagen_consulta": ruta_imagen(q), "id_candidato": fila["id_global"],
                       "imagen_candidato": ruta_imagen(fila["id_global"]),
                       "explicacion": explicacion(rk[fila["consulta"]], fila["id_global"], pesos)})
    publicar(raiz, [
        (MUESTRA_H3, lambda ruta: escribir_csv(ruta, ["ficha", "consulta", "id_global", "clase"], muestra)),
        (WORKBOOK_REVISION_H3.as_posix(), lambda ruta: escribir_libro(
            ruta, GUIA_H3, "revision", EDITABLES_H3 + CONTEXTO_H3, fichas, EDITABLES_H3,
            {"explicacion": 90, "comentario": 50}, {"valoracion": list(VALORACIONES_H3)}, (["nota"], []),
            enlaces=("imagen_consulta", "imagen_candidato"))),
    ])
    print(f"Revision de H3: {len(fichas)} fichas en {WORKBOOK_REVISION_H3} (aciertos disponibles: {disponibles['acierto']}, "
          f"errores disponibles: {disponibles['error']}). No abra {MUESTRA_H3}.")
    return 0


def validar_revision_h3(filas: list[dict[str, str]]) -> tuple[list[str], int]:
    """Errores de las fichas completadas y número de fichas pendientes."""
    errores, pendientes = [], 0
    for f in filas:
        if not f.get("valoracion"):
            pendientes += 1
            continue
        if f["valoracion"] not in VALORACIONES_H3:
            errores.append(f"{f['ficha']}: valoracion '{f['valoracion']}' no prevista")
        if not f.get("evaluador"):
            errores.append(f"{f['ficha']}: evaluador vacio")
        if not fecha_valida(f.get("fecha_revision", "")):
            errores.append(f"{f['ficha']}: fecha_revision vacia o invalida (AAAA-MM-DD)")
    return errores, pendientes


def resumen_revision_h3(raiz: Path) -> tuple[dict[tuple[str, str], int] | None, str]:
    """Conteos por clase y valoración, o None con el motivo si la revisión no se hizo o está incompleta."""
    if not (raiz / WORKBOOK_REVISION_H3).exists():
        return None, "no realizada"
    filas = leer_hoja(raiz / WORKBOOK_REVISION_H3, "revision", clave="ficha")
    errores, pendientes = validar_revision_h3(filas)
    if errores or pendientes:
        return None, f"incompleta ({pendientes} fichas pendientes, {len(errores)} errores)"
    clases = {f["ficha"]: f["clase"] for f in leer_csv(raiz / MUESTRA_H3)}
    escribir_csv(raiz / SALIDA_REVISION_H3, ["ficha"] + EDITABLES_H3, [{c: f.get(c, "") for c in ["ficha"] + EDITABLES_H3} for f in filas])
    return dict(Counter((clases[f["ficha"]], f["valoracion"]) for f in filas)), "completa"


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


def no_evaluables(sistemas: dict[str, dict[str, list[str]]], juicios_t3: dict[str, dict[str, int | None]],
                  k: int) -> dict[str, dict[str, int]]:
    """Pares `no_evaluable` en el top k de cada sistema del pool, por consulta (protocolo, sección 6)."""
    return {s: {c: sum(1 for i in sistemas[c][s][:k] if i in juicios_t3.get(c, {}) and juicios_t3[c][i] is None)
                for c in sorted(sistemas) if s in sistemas[c]}
            for s in SISTEMAS_POOL}


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
    filas, ndcg, juzgada = [], defaultdict(dict), defaultdict(dict)
    for consulta in sorted(sistemas):
        j = juicios_t3.get(consulta, {})
        for s in nombres:
            ranking = sistemas[consulta][s]
            valor = evaluacion.ndcg(ranking, j, k)
            ndcg[s][consulta] = valor
            juzgada[s][consulta] = evaluacion.proporcion_juzgada(ranking, j, k)
            filas.append({"tarea": "T3", "consulta": consulta, "sistema": s, "ndcg10": fmt(valor, 6),
                          "p10": fmt(evaluacion.precision(ranking, j, k), 6), "mrr": fmt(evaluacion.rango_reciproco(ranking, j), 6),
                          "juzgada10": fmt(juzgada[s][consulta], 6)})
    opciones = dict(umbral=float(metricas_cfg["umbral_practico"]), alfa=float(metricas_cfg["alfa"]),
                    confianza=float(metricas_cfg["confianza"]), replicas_permutacion=int(metricas_cfg["replicas_permutacion"]),
                    replicas_bootstrap=int(metricas_cfg["replicas_bootstrap"]),
                    semilla_permutacion=int(metricas_cfg["semilla_permutacion"]),
                    semilla_bootstrap=int(metricas_cfg["semilla_bootstrap"]),
                    tolerancia=float(metricas_cfg["tolerancia_empates"]))
    con_bandas = consultas_con_palabra(raiz, particion)
    filtrar = lambda d: {c: v for c, v in d.items() if c in con_bandas}  # noqa: E731
    h1 = evaluacion.comparar(ndcg["M4"], ndcg["M2"], **opciones)
    h2 = evaluacion.compuerta(h1, evaluacion.comparar(ndcg["M3"], ndcg["M3-sin-orden"], **opciones, exacta=True))
    subgrupo = replace(evaluacion.comparar(filtrar(ndcg["M3"]), filtrar(ndcg["M3-sin-orden"]), **opciones, exacta=True),
                       decision=DESCRIPTIVA)
    comparaciones = {"H1: M4 frente a M2": h1, "H2: M3 frente a M3-sin-orden": h2,
                     "H2, subgrupo: consultas con palabra de bandas": subgrupo}
    evaluables_h2 = [c for c in sorted(sistemas) if ndcg["M3"][c] is not None and ndcg["M3-sin-orden"][c] is not None]
    b = sum(1 for c in evaluables_h2 if c in con_bandas)
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
    return {"filas": filas, "ndcg": ndcg, "juzgada": juzgada, "comparaciones": comparaciones, "exploratorias": exploratorias,
            "h3": h3, "robustez": robustez, "nombres": nombres, "con_bandas": sorted(con_bandas & set(sistemas)), "b": b,
            "no_evaluables": no_evaluables(sistemas, juicios_t3, k),
            "sin_relevantes": sorted({e for c in (h1, h2) for e in c.excluidas})}


def media(valores: list[float | None]) -> float | None:
    presentes = [v for v in valores if v is not None]
    return sum(presentes) / len(presentes) if presentes else None


def si_no(valor: bool) -> str:
    return "si" if valor else "no"


def informe(r: dict[str, Any], config: dict[str, Any], integridad: dict[str, Any], revision_h3: tuple,
            juicios_t1: dict | None, rk_t1: dict | None) -> list[str]:
    """Informe de resultados con la plantilla fijada en el protocolo (sección 7), tablas 1 a 10."""
    k, metricas_cfg = config["metricas"]["k"], config["metricas"]
    umbral, alfa = metricas_cfg["umbral_practico"], metricas_cfg["alfa"]
    h1 = r["comparaciones"]["H1: M4 frente a M2"]
    h2 = r["comparaciones"]["H2: M3 frente a M3-sin-orden"]
    sub = r["comparaciones"]["H2, subgrupo: consultas con palabra de bandas"]
    n_h2 = h2.n
    equivalente = fmt(umbral * n_h2 / r["b"]) if r["b"] else "no estimable"
    lineas = [
        "# Resultados del test (T3 y T1)",
        "",
        "Generado por `python -m src.experimento.ejecucion_prueba --evaluar`, una sola vez, con los sistemas congelados y los "
        "juicios de prueba hechos sin asistencia (decisiones R27, R30 y R37). Reglas de decision: protocolo, secciones 1 y 7 "
        "(R33 a R35). El intervalo es descriptivo.",
        "",
        "## 1. Integridad de la corrida",
        "",
    ]
    lineas += tabla([["Corrida", integridad["corrida"]], ["Estados", " > ".join(integridad["estados"])],
                     ["Commit sellado", integridad["commit"] or "—"],
                     ["Huellas comprobadas", f"{integridad['huellas']} (todas coinciden)"],
                     ["Comprobacion de fugas", "sin problemas (comprobacion previa)"],
                     ["Cegamiento de los libros", ", ".join(f"{t}: {v}" for t, v in integridad["cegamiento"].items())]],
                    ["Elemento", "Valor"])
    lineas += ["", "## 2. Pool y juicios", ""]
    lineas += [f"- Consultas sin ningun relevante, excluidas de la media: {len(r['sin_relevantes'])} "
               f"({', '.join(r['sin_relevantes']) or 'ninguna'}).", ""]
    filas_ne = [[s, str(sum(r["no_evaluables"][s].values())),
                 ", ".join(f"{c}: {v}" for c, v in r["no_evaluables"][s].items() if v) or "ninguna",
                 fmt(media(list(r["juzgada"][s].values())))] for s in SISTEMAS_POOL if s in r["juzgada"]]
    lineas += tabla(filas_ne, ["Sistema", f"no_evaluable en el top {k}", "Consultas con no_evaluable", f"Proporcion juzgada del top {k}"])
    lineas += ["", "## 3. H1: M4 frente a M2", ""]
    a = h1.afirmaciones
    lineas += tabla([["Consultas (n)", str(h1.n)], ["Diferencia media", fmt(h1.media)],
                     ["IC 95 % (bootstrap)", f"{fmt(h1.intervalo[0])} a {fmt(h1.intervalo[1])}"],
                     [f"p (permutacion, B = {h1.replicas})", fmt(h1.p_permutacion, 5)],
                     ["Error de Monte Carlo de la p", fmt(h1.error_mc, 5)], ["t pareada (p)", f"{fmt(h1.t)} ({fmt(h1.p_t, 4)})"],
                     [f"(a) Frente a cero: p < {alfa}", si_no(a.frente_a_cero)],
                     [f"(c) Relevancia practica: diferencia >= {umbral}", si_no(a.relevancia_practica)],
                     ["Lectura y veredicto", h1.decision]], ["Elemento", "Valor"])
    lineas += ["", "Una p no significativa no demuestra que no haya mejora (protocolo, seccion 7).", "",
               "## 4. H2: M3 frente a M3-sin-orden", ""]
    lineas += tabla([["Consultas (n)", str(h2.n)], ["b: consultas evaluables con palabra de bandas", str(r["b"])],
                     ["m: diferencias distintas de cero", str(h2.m)], ["p exacta (2^m vectores)", fmt(h2.p_permutacion, 5)],
                     ["p minima alcanzable", fmt(h2.p_minima, 5)], ["Diferencia media", fmt(h2.media)],
                     ["IC 95 % (bootstrap)", f"{fmt(h2.intervalo[0])} a {fmt(h2.intervalo[1])}"],
                     ["Compuerta de H1 (secuencia fija)", "abierta" if h1.sostiene else "cerrada"],
                     ["Lectura y veredicto", h2.decision]], ["Elemento", "Valor"])
    lineas += ["", "Subgrupo de bandas (descriptivo; no puede confirmar H2):", ""]
    lineas += tabla([["Consultas", str(sub.n)], ["Diferencia media", fmt(sub.media)],
                     ["IC 95 % (bootstrap)", f"{fmt(sub.intervalo[0])} a {fmt(sub.intervalo[1])}"],
                     ["p exacta", fmt(sub.p_permutacion, 5)], [f"Umbral equivalente ({umbral} · n / b)", equivalente]],
                    ["Elemento", "Valor"])
    conteos, estado_revision = revision_h3
    lineas += ["", "## 5. H3: fidelidad computacional de M4", ""]
    lineas += tabla([[f"Resultados comprobados (top {k} de M4)", str(r["h3"]["resultados"])],
                     ["Error maximo de reconstruccion", f"{r['h3']['reconstruccion']:.2e}"],
                     ["Error maximo de intervencion", f"{r['h3']['intervencion']:.2e}"],
                     ["Diferencia maxima con la puntuacion versionada (6 decimales)", f"{r['h3']['version']:.2e}"],
                     [f"Veredicto (tolerancia {config['ejecucion']['tolerancia_h3']})",
                      evaluacion.SE_SOSTIENE if r["h3"]["cumple"] else "no se sostiene"]], ["Elemento", "Valor"])
    lineas += ["", f"Revision humana de las explicaciones (descriptiva, no independiente, no interviene en H3): {estado_revision}.", ""]
    if conteos:
        lineas += tabla([[clase] + [str(conteos.get((clase, v), 0)) for v in VALORACIONES_H3] for clase in ("acierto", "error")],
                        ["Clase"] + list(VALORACIONES_H3))
    lineas += ["", f"## 6. Metricas de todos los sistemas (media sobre las consultas; por consulta en `{METRICAS}`)", ""]
    lineas += tabla([[s, fmt(media(list(r["ndcg"][s].values())))] for s in r["nombres"]], ["Sistema o variante", f"nDCG@{k} medio"])
    lineas += ["", "## 7. Ablaciones, control negativo y M4-RRF (exploratorias)", "",
               "Diferencias pareadas con su intervalo; su p no se interpreta como confirmacion. El control negativo usa una sola "
               "permutacion y es descriptivo.", ""]
    lineas += tabla([[n, str(c.n), fmt(c.media), f"{fmt(c.intervalo[0])} a {fmt(c.intervalo[1])}", fmt(c.p_permutacion, 4), c.decision]
                     for n, c in r["exploratorias"].items()],
                    ["Comparacion", "Consultas", "Diferencia media", "IC 95 %", "p permutacion", "Lectura"])
    lineas += ["", "## 8. Robustez por museo y por estado de la pieza (descriptiva)", ""]
    lineas += tabla([[criterio, valor, str(n)] + [fmt(v) for v in medias.values()]
                     for (criterio, valor), (n, medias) in r["robustez"].items()],
                    ["Criterio", "Grupo", "Consultas", "M2", "M3", "M3-sin-orden", "M4"])
    lineas += ["", "## 9. T1: texto a imagen (exploratoria, descriptiva)", ""]
    if rk_t1 is None or juicios_t1 is None:
        lineas.append("Sin rankings o juicios de T1.")
    else:
        filas_t1 = []
        for s in SISTEMAS_T1:
            valores = [evaluacion.ndcg([i for i, _ in rk_t1[c][s]], juicios_t1.get(c, {}), int(k)) for c in rk_t1 if s in rk_t1[c]]
            filas_t1.append([s, str(len(valores)), fmt(media(valores))])
        lineas += tabla(filas_t1, ["Sistema", "Consultas", f"nDCG@{k} medio"])
    lineas += ["", "## 10. Desviaciones del protocolo", "",
               f"Se registran, con su motivo, en `{REGISTRO_CUSTODIA}`. Este informe no las infiere."]
    return lineas


def evaluar(raiz: Path) -> int:
    man, problemas = verificar(raiz, "juicios_cerrados")
    if not problemas and estado_actual(man) != "juicios_cerrados":
        problemas.append(f"La corrida ya esta en {estado_actual(man)}: la evaluacion es unica.")
    if problemas:
        return abortar(raiz, man, problemas)
    config = leer_config_experimento(raiz)
    revision = resumen_revision_h3(raiz)
    if revision[1].startswith("incompleta"):
        print(f"La revision de H3 esta {revision[1]}: completela o retire {WORKBOOK_REVISION_H3} antes de evaluar.")
        return 1
    juicios_t3 = leer_juicios_sellados(raiz / TAREAS["T3"].salida)
    juicios_t1 = leer_juicios_sellados(raiz / TAREAS["T1"].salida)
    rk_t1 = leer_rankings(raiz / RANKINGS_T1)
    r = calcular(raiz, "prueba", leer_rankings(raiz / RANKINGS_PRUEBA), juicios_t3)
    estados = [e["estado"] for e in man["estados"]]
    integridad = {"corrida": man["corrida"], "estados": estados + ["evaluada"], "huellas": len(sellados(man)),
                  "commit": next((e.get("commit", "") for e in man["estados"] if e["estado"] == "insumos_sellados"), ""),
                  "cegamiento": next((e.get("cegamiento", {}) for e in man["estados"] if e["estado"] == "juicios_cerrados"), {})}
    escrituras = [(METRICAS, lambda ruta: escribir_csv(ruta, COLUMNAS_METRICAS, r["filas"])),
                  (REPORTE, lambda ruta: escribir_texto(ruta, informe(r, config, integridad, revision, juicios_t1, rk_t1)))]
    revision_sellada = huellas(raiz, [WORKBOOK_REVISION_H3.as_posix(), MUESTRA_H3, SALIDA_REVISION_H3]) if revision[0] else {}
    publicar(raiz, escrituras, lambda sumas: con_estado(man, "evaluada", {**sumas, **revision_sellada}))
    print(f"Resultados del test -> {REPORTE}")
    imprimir_custodia(leer_manifiesto(raiz))
    return 0


# --------------------------------------------------------------------------- principal


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Ejecucion unica del test del protocolo experimental v2.")
    parser.add_argument("--root", default=".", help="Raiz del repositorio.")
    grupo = parser.add_mutually_exclusive_group(required=True)
    grupo.add_argument("--comprobar", action="store_true", help="Condiciones de suspension, sin ejecutar nada.")
    grupo.add_argument("--rankings", action="store_true", help="Una sola vez: sella los insumos, luego rankings y pool.")
    grupo.add_argument("--crear-juicios", action="store_true", help="Libros ciegos de juicios de prueba (conserva lo juzgado).")
    grupo.add_argument("--cerrar-juicios", action="store_true", help="Valida, exporta y sella los juicios de prueba.")
    grupo.add_argument("--crear-revision-h3", action="store_true", help="Fichas ciegas de la revision descriptiva de H3.")
    grupo.add_argument("--evaluar", action="store_true", help="Comprueba las huellas y calcula los resultados.")
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
    if args.cerrar_juicios:
        return cerrar_juicios(raiz)
    if args.crear_revision_h3:
        return crear_revision_h3(raiz)
    return evaluar(raiz)


if __name__ == "__main__":
    raise SystemExit(main())
