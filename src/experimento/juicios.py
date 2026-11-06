"""Juicios de relevancia de desarrollo de la tarea T3: pool ciego, workbook del evaluador y validación.

Uso desde la raíz del repositorio:

    python -m src.experimento.juicios --crear   # crea o actualiza el workbook y la galería (conserva los juicios)
    python -m src.experimento.juicios           # pool, validación y exportación (paso del flujo)

Pool de cada consulta de desarrollo ([juicios] de config/experimento.toml): los primeros
profundidad_pool de cada sistema de data/processed/experimento_v2_rankings_desarrollo.csv, sin
repetir, más aleatorios_pool candidatos elegidos al azar con semilla_pool entre los demás. Si se
agregan sistemas (M3, M3-sin-orden, M4), el pool crece y los pares ya juzgados se conservan.

El workbook data/metadata/juicios_desarrollo_v2.xlsx muestra cada par en un orden barajado por la
semilla, sin el sistema ni la posición que lo propusieron (protocolo, sección 6). El origen de cada
par queda en data/processed/experimento_v2_pool_desarrollo.csv, que el evaluador no abre.

Escala: 0 a 3 y no_evaluable (estado aparte). Un juicio 2 o 3 exige justificación con la evidencia
visible, y todo juicio exige evaluador y fecha. Con errores termina con código 1 y no actualiza
data/metadata/juicios_desarrollo_v2.csv, que tiene siempre una fila por par del pool.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from src.anotacion.aplicar_anotaciones import fecha_valida
from src.anotacion.nucleo import huella
from src.experimento.libro import escribir_libro
from src.experimento.rankings import SALIDA_RANKINGS
from src.experimento.snapshot import SALIDA_CONSULTAS, SALIDA_PARTICIONES
from src.imagenes.descargar_evaluacion import MANIFIESTO_EVALUACION
from src.review.galerias import CARPETA, esc, escribir_pagina, imagen_evaluacion, tarjeta
from src.utils.archivos import escribir_csv, escribir_texto, indexar, leer_csv
from src.utils.config import CONFIG_EXPERIMENTO, leer_config_experimento
from src.utils.libros import leer_hoja
from src.utils.metricas import tabla

WORKBOOK_JUICIOS = Path("data/metadata/juicios_desarrollo_v2.xlsx")
HOJA_JUICIOS = "juicios"
SALIDA_POOL = "data/processed/experimento_v2_pool_desarrollo.csv"
SALIDA_JUICIOS = "data/metadata/juicios_desarrollo_v2.csv"
REPORTE_JUICIOS = "outputs/reports/experimento_v2_juicios_desarrollo.md"
GALERIA = Path(CARPETA) / "juicios_desarrollo_v2_galeria.html"
NO_EVALUABLE = "no_evaluable"
EDITABLES = ["relevancia", "justificacion", "evaluador", "fecha_juicio"]
CONTEXTO = ["consulta", "orden", "id_consulta", "imagen_consulta", "id_candidato", "imagen_candidato"]
COLUMNAS_POOL = ["consulta", "id_global", "origen"]
COLUMNAS_JUICIOS = ["consulta", "id_global", "relevancia", "justificacion", "evaluador", "fecha_juicio"]

EJEMPLOS = (
    ["ejemplo", "consulta", "candidato", "relevancia", "justificacion"],
    [
        {"ejemplo": "E1", "consulta": "Faja con bandas lisa > geometrica > lisa", "relevancia": "3",
         "candidato": "Tunica con la misma secuencia de bandas, en otros colores y con otros motivos geometricos",
         "justificacion": "Misma organizacion: tres bandas en el mismo orden; el color no cuenta."},
        {"ejemplo": "E2", "consulta": "Faja con bandas lisa > geometrica > lisa", "relevancia": "2",
         "candidato": "Pano en bandas con una banda figurativa de mas entre las geometricas",
         "justificacion": "Misma composicion en bandas; la secuencia cambia en una banda."},
        {"ejemplo": "E3", "consulta": "Campo central liso con borde de aves", "relevancia": "1",
         "candidato": "Reticula de cuadros con un borde decorado alrededor",
         "justificacion": "Comparte solo el borde decorado; la organizacion del campo es otra."},
        {"ejemplo": "E4", "consulta": "Tela en reticula de cuadros alternados", "relevancia": "0",
         "candidato": "Faja de bandas horizontales", "justificacion": "Organizacion distinta."},
        {"ejemplo": "E5", "consulta": "Cualquiera", "relevancia": NO_EVALUABLE,
         "candidato": "Fotografia tan oscura o recortada que no deja ver la organizacion",
         "justificacion": "No cuenta como 0: se excluye del calculo y se informa."},
    ],
)

GUIA = [
    "Juicios de relevancia de desarrollo, tarea T3 (protocolo experimental v2, seccion 6)",
    "",
    "Cada fila es un par: la pieza consultada y un candidato. Juzgue si el candidato tiene la MISMA ORGANIZACION",
    "visible que la consulta, mirando solo las dos imagenes (galeria local outputs/review/juicios_desarrollo_v2_galeria.html).",
    "",
    "  3 = misma organizacion: tipo de composicion, secuencia de bandas o regiones y relaciones, aunque cambien colores",
    "      y motivos.",
    "  2 = misma composicion con diferencias en la secuencia o en las relaciones.",
    "  1 = comparte un rasgo estructural parcial.",
    "  0 = organizacion distinta.",
    "  no_evaluable = la imagen no deja juzgar (no es 0).",
    "",
    "Reglas: el color no cuenta; no abra los workbooks de anotacion ni los rankings; el orden de las filas es al azar y",
    "no dice nada del sistema. Un juicio 2 o 3 lleva una justificacion breve con la evidencia visible. Complete",
    "evaluador y fecha_juicio (AAAA-MM-DD). Unos 30 segundos por par. La hoja 'ejemplos' tiene casos hipoteticos.",
    "",
    "Despues: python -m src.flujo valida los juicios y los exporta a data/metadata/juicios_desarrollo_v2.csv.",
]


def clave(consulta: str, id_global: str) -> str:
    return f"{consulta}|{id_global}"


def construir_pool(raiz: Path, config: dict[str, Any]) -> list[dict[str, str]]:
    """Pares del pool de cada consulta de desarrollo, con los sistemas que los propusieron."""
    profundidad, aleatorios = int(config["juicios"]["profundidad_pool"]), int(config["juicios"]["aleatorios_pool"])
    semilla = int(config["juicios"]["semilla_pool"])
    origen: dict[tuple[str, str], set[str]] = defaultdict(set)
    candidatos: dict[str, set[str]] = defaultdict(set)
    for fila in leer_csv(raiz / SALIDA_RANKINGS):
        candidatos[fila["consulta"]].add(fila["id_global"])
        if int(fila["rango"]) <= profundidad:
            origen[(fila["consulta"], fila["id_global"])].add(fila["sistema"])
    pool = []
    for consulta in sorted(candidatos):
        propuestos = {i for (c, i) in origen if c == consulta}
        resto = sorted(candidatos[consulta] - propuestos, key=lambda i: huella(semilla, f"pool:{consulta}", i))
        for id_global in resto[:aleatorios]:
            origen[(consulta, id_global)].add("azar")
        for (c, id_global), sistemas in origen.items():
            if c == consulta:
                pool.append({"consulta": c, "id_global": id_global, "origen": "; ".join(sorted(sistemas))})
    return sorted(pool, key=lambda f: (f["consulta"], huella(semilla, f"orden:{f['consulta']}", f["id_global"])))


def leer_juicios(raiz: Path) -> dict[str, dict[str, str]]:
    ruta = raiz / WORKBOOK_JUICIOS
    if not ruta.exists():
        return {}
    return {clave(f["consulta"], f["id_candidato"]): f for f in leer_hoja(ruta, HOJA_JUICIOS, clave="consulta")}


def relevancia(texto: str) -> str:
    """Normaliza 3, 3.0 o '3' a '3'; deja no_evaluable y vacio como estan."""
    if texto in ("", NO_EVALUABLE):
        return texto
    try:
        numero = float(texto)
    except ValueError:
        return texto
    return str(int(numero)) if numero.is_integer() else texto


# --------------------------------------------------------------------------- creacion


def crear(raiz: Path) -> int:
    config = leer_config_experimento(raiz)
    pool = construir_pool(raiz, config)
    previos = leer_juicios(raiz)
    consultas = indexar(leer_csv(raiz / SALIDA_CONSULTAS), "consulta")
    manifiesto = indexar(leer_csv(raiz / MANIFIESTO_EVALUACION), "id_global")
    ruta_imagen = lambda i: "../" + manifiesto.get(i, {}).get("ruta_copia_evaluacion", "").removeprefix("data/")  # noqa: E731
    filas, orden = [], Counter()
    for par in pool:
        orden[par["consulta"]] += 1
        q = consultas[par["consulta"]]["id_global"]
        previo = previos.get(clave(par["consulta"], par["id_global"]), {})
        filas.append({**{c: previo.get(c, "") for c in EDITABLES}, "consulta": par["consulta"],
                      "orden": str(orden[par["consulta"]]), "id_consulta": q, "imagen_consulta": ruta_imagen(q),
                      "id_candidato": par["id_global"], "imagen_candidato": ruta_imagen(par["id_global"])})
    vigentes = {clave(f["consulta"], f["id_candidato"]) for f in filas}
    conservados = [f for k, f in previos.items() if k not in vigentes and f.get("relevancia")]
    filas += [{c: f.get(c, "") for c in EDITABLES + CONTEXTO} for f in conservados]
    escala = [str(g) for g in config["juicios"]["escala"]] + [NO_EVALUABLE]
    try:
        escribir_libro(raiz / WORKBOOK_JUICIOS, GUIA, HOJA_JUICIOS, EDITABLES + CONTEXTO, filas, EDITABLES,
                       {"justificacion": 50, "imagen_consulta": 14, "imagen_candidato": 14, "orden": 7},
                       {"relevancia": escala}, EJEMPLOS, enlaces=("imagen_consulta", "imagen_candidato"))
    except PermissionError:
        print(f"No se pudo escribir {WORKBOOK_JUICIOS}: cierre el archivo en Excel.")
        return 1
    escribir_galeria(raiz, filas, manifiesto)
    print(f"Workbook de juicios de desarrollo: {raiz / WORKBOOK_JUICIOS} | pares: {len(filas)}, "
          f"juzgados: {sum(bool(f['relevancia']) for f in filas)}")
    print(f"Galeria: {raiz / GALERIA}")
    return 0


def escribir_galeria(raiz: Path, filas: list[dict[str, str]], manifiesto: dict[str, dict[str, str]]) -> None:
    salida = raiz / GALERIA
    secciones = []
    for consulta in sorted({f["consulta"] for f in filas}):
        propias = [f for f in filas if f["consulta"] == consulta]
        q = propias[0]["id_consulta"]
        tarjetas = [tarjeta(imagen_evaluacion(raiz, manifiesto, q, salida), "", q,
                            [f"<b>CONSULTA {esc(consulta)}</b>", ("m", esc(q))])]
        tarjetas += [tarjeta(imagen_evaluacion(raiz, manifiesto, f["id_candidato"], salida), "", f["id_candidato"],
                             [f"<b>orden {esc(f['orden'])}</b>", ("m", esc(f["id_candidato"]))]) for f in propias]
        secciones.append((f"{consulta}: la primera imagen es la consulta", tarjetas))
    escribir_pagina(salida, "Juicios de desarrollo T3", "Orden al azar, sin sistema ni posicion. Galeria local, no se versiona.",
                    secciones)


# --------------------------------------------------------------------------- validacion


def validar(raiz: Path) -> int:
    if not (raiz / SALIDA_RANKINGS).exists():
        print(f"No existe {SALIDA_RANKINGS}: no hay pool de desarrollo.")
        return 0
    config = leer_config_experimento(raiz)
    pool = construir_pool(raiz, config)
    escribir_csv(raiz / SALIDA_POOL, COLUMNAS_POOL, pool)
    escala = {str(g) for g in config["juicios"]["escala"]} | {NO_EVALUABLE}
    juicios = leer_juicios(raiz)
    errores, salida = [], []
    for par in pool:
        j = juicios.get(clave(par["consulta"], par["id_global"]), {})
        fila = {"consulta": par["consulta"], "id_global": par["id_global"], "relevancia": relevancia(j.get("relevancia", "")),
                "justificacion": j.get("justificacion", ""), "evaluador": j.get("evaluador", ""),
                "fecha_juicio": j.get("fecha_juicio", "")}
        etiqueta = f"{par['consulta']} orden {j.get('orden', '?')}"
        if fila["relevancia"]:
            if fila["relevancia"] not in escala:
                errores.append(f"{etiqueta}: relevancia '{fila['relevancia']}' no es de la escala")
            if fila["relevancia"] in ("2", "3") and not fila["justificacion"]:
                errores.append(f"{etiqueta}: un juicio {fila['relevancia']} lleva justificacion")
            if not fila["evaluador"]:
                errores.append(f"{etiqueta}: evaluador vacio")
            if not fecha_valida(fila["fecha_juicio"]):
                errores.append(f"{etiqueta}: fecha_juicio vacia o invalida (AAAA-MM-DD)")
        salida.append(fila)
    por_consulta = defaultdict(Counter)
    for fila in salida:
        por_consulta[fila["consulta"]][fila["relevancia"] or "pendiente"] += 1
    columnas = [str(g) for g in config["juicios"]["escala"]] + [NO_EVALUABLE, "pendiente"]
    lineas = [
        "# Juicios de relevancia de desarrollo (T3)",
        "",
        f"Generado por `python -m src.experimento.juicios`, paso del flujo. Workbook: `{WORKBOOK_JUICIOS.as_posix()}`; "
        f"pool en `{SALIDA_POOL}` (el evaluador no lo abre); parametros en `{CONFIG_EXPERIMENTO.as_posix()}` ([juicios]).",
        "",
        f"- Pares en el pool: {len(pool)}; juzgados: {sum(bool(f['relevancia']) for f in salida)}.",
        f"- Pool: los {config['juicios']['profundidad_pool']} primeros de cada sistema ("
        + ", ".join(sorted({s for p in pool for s in p['origen'].split('; ') if s != 'azar'}))
        + f") y {config['juicios']['aleatorios_pool']} al azar por consulta.",
        "",
    ]
    lineas += tabla([[c] + [str(por_consulta[c][k]) for k in columnas] for c in sorted(por_consulta)],
                    ["Consulta"] + columnas)
    lineas += ["", "## Errores", ""] + ([f"- {e}" for e in errores] if errores else ["Ninguno."])
    escribir_texto(raiz / REPORTE_JUICIOS, lineas)
    if errores:
        print(f"Juicios de desarrollo con {len(errores)} errores; no se actualizo {SALIDA_JUICIOS}.")
        for error in errores[:20]:
            print(f"- {error}")
        return 1
    escribir_csv(raiz / SALIDA_JUICIOS, COLUMNAS_JUICIOS, salida)
    print(f"Juicios de desarrollo: {len(pool)} pares, {sum(bool(f['relevancia']) for f in salida)} juzgados -> {SALIDA_JUICIOS}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Juicios de relevancia de desarrollo T3.")
    parser.add_argument("--root", default=".", help="Raiz del repositorio.")
    parser.add_argument("--crear", action="store_true", help="Crea o actualiza el workbook y la galeria (conserva los juicios).")
    args = parser.parse_args(argv)
    raiz = Path(args.root).resolve()
    return crear(raiz) if args.crear else validar(raiz)


if __name__ == "__main__":
    raise SystemExit(main())
