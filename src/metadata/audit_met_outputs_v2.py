"""Audita las salidas base MET v2: conteos, columnas, identificadores y trazabilidad minima.

Uso desde la raiz del repositorio (lo ejecuta tambien python -m src.flujo):

    python -m src.metadata.audit_met_outputs_v2

Las rutas y los conteos esperados se leen de [met.base] en config/corpus.toml.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from src.utils.archivos import escribir_texto, leer_csv_con_columnas
from src.utils.config import leer_config

# Estado de curacion que debe tener cada fila de cada subconjunto.
ESTADOS = {"principal": "corpus_principal", "secundario": "corpus_secundario", "descartados": "descartado"}

COLUMNAS_REQUERIDAS = [
    "fuente",
    "id_fuente",
    "id_registro",
    "institucion",
    "titulo_original",
    "cultura",
    "material",
    "descripcion",
    "url_objeto",
    "url_imagen",
    "estado_curacion",
    "destino_curacion",
    "origen_curacion",
    "motivo_curacion",
]


def auditar_archivo(nombre: str, config: dict[str, object], raiz: Path) -> list[str]:
    problemas: list[str] = []

    ruta = raiz / str(config["ruta"])
    conteo_esperado = int(config["filas"])
    estado_esperado = ESTADOS[nombre]

    if not ruta.exists():
        return [f"{nombre}: falta archivo {ruta}"]

    texto = ruta.read_text(encoding="utf-8", errors="replace")
    if "Forbidden. Calls to this URL" in texto:
        problemas.append(f"{nombre}: contiene mensaje Forbidden en lugar de datos validos")

    columnas, filas = leer_csv_con_columnas(ruta)

    faltantes = [columna for columna in COLUMNAS_REQUERIDAS if columna not in columnas]
    if faltantes:
        problemas.append(f"{nombre}: faltan columnas requeridas: {', '.join(faltantes)}")
        return problemas

    if len(filas) != conteo_esperado:
        problemas.append(
            f"{nombre}: conteo esperado {conteo_esperado}, conteo observado {len(filas)}"
        )

    ids_vistos: set[str] = set()
    ids_duplicados: set[str] = set()

    for numero_fila, fila in enumerate(filas, start=2):
        id_fuente = (fila.get("id_fuente") or "").strip()
        estado = (fila.get("estado_curacion") or "").strip()
        url_objeto = (fila.get("url_objeto") or "").strip()
        url_imagen = (fila.get("url_imagen") or "").strip()
        motivo = (fila.get("motivo_curacion") or "").strip()

        if not id_fuente:
            problemas.append(f"{nombre}: fila {numero_fila} sin id_fuente")
        elif id_fuente in ids_vistos:
            ids_duplicados.add(id_fuente)
        ids_vistos.add(id_fuente)

        if estado != estado_esperado:
            problemas.append(
                f"{nombre}: fila {numero_fila} tiene estado_curacion={estado}, esperado={estado_esperado}"
            )

        if not url_objeto:
            problemas.append(f"{nombre}: fila {numero_fila} sin url_objeto")

        if nombre != "descartados" and not url_imagen:
            problemas.append(f"{nombre}: fila {numero_fila} sin url_imagen")

        if not motivo:
            problemas.append(f"{nombre}: fila {numero_fila} sin motivo_curacion")

    if ids_duplicados:
        muestra = ", ".join(sorted(ids_duplicados)[:10])
        problemas.append(f"{nombre}: id_fuente duplicados: {muestra}")

    return problemas


def escribir_reporte(ruta: Path, problemas: list[str]) -> None:
    lineas = [
        "# Auditoria tecnica MET v2",
        "",
        "Esta auditoria valida las salidas normalizadas de MET v2: conteos, columnas, identificadores, estados de curacion y trazabilidad minima.",
        "",
    ]

    if problemas:
        lineas.extend(["## Hallazgos", ""])
        lineas.extend(f"- {problema}" for problema in problemas)
    else:
        lineas.extend([
            "## Resultado",
            "",
            "Sin hallazgos criticos. Las salidas MET v2 cumplen los controles definidos.",
        ])

    escribir_texto(ruta, lineas)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audita las salidas curatoriales MET v2.")
    parser.add_argument("--root", default=".", help="Raiz del repositorio.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    raiz = Path(args.root).resolve()

    problemas: list[str] = []
    for nombre, config in leer_config(raiz)["met"]["base"].items():
        if not isinstance(config, dict):
            continue  # descripcion
        problemas.extend(auditar_archivo(nombre, config, raiz))

    escribir_reporte(raiz / "outputs/reports/met_auditoria_tecnica_v2.md", problemas)

    if problemas:
        print("Hallazgos de auditoria:")
        for problema in problemas:
            print(f"- {problema}")
        return 1

    print("Auditoria MET v2 sin hallazgos criticos.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
