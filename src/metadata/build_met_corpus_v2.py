"""Construye las salidas base MET v2 desde el corpus MET v1 congelado.

Uso desde la raiz del repositorio (lo ejecuta tambien python -m src.flujo):

    python -m src.metadata.build_met_corpus_v2

Reorganiza el corpus MET v1 (data/processed/corpus_met_textiles_andinos_v1_*.csv) en el
esquema v2: un CSV por subconjunto (principal, secundario, descartados) con el estado y
el destino de la curacion. Estas salidas sembraron el workbook de revision MET
(src/preprocessing/create_met_review_workbook_v2.py), donde quedan las decisiones vigentes.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from src.utils.archivos import escribir_csv, escribir_texto, leer_csv
from src.utils.libros import lector

COLUMNAS_V2 = [
    "fuente",
    "id_fuente",
    "id_registro",
    "institucion",
    "titulo_original",
    "titulo_es_sugerido",
    "cultura",
    "periodo",
    "fecha_objeto",
    "procedencia",
    "clasificacion_original",
    "tipo_objeto",
    "tipo_superficie",
    "material",
    "material_normalizado",
    "tecnica",
    "descripcion",
    "url_objeto",
    "url_imagen",
    "ruta_imagen_local",
    "licencia",
    "estado_curacion",
    "destino_curacion",
    "origen_curacion",
    "motivo_curacion",
    "decision_filtro",
    "puntaje_filtro",
    "motivo_filtrado",
    "decision_auditoria",
    "motivo_auditoria",
    "observacion_auditoria",
    "posible_duplicado_suave",
    "estado_metadata",
    "estado_anotacion",
]


def motivo_principal(fila: dict[str, str]) -> str:
    leer = lector(fila)
    candidatos = [
        leer("motivo_curacion_final"),
        leer("motivo_revision_v2"),
        leer("motivo_superficie"),
        leer("motivo_filtrado"),
    ]
    return next((texto for texto in candidatos if texto), "")


def normalizar_fila(
    fila: dict[str, str],
    estado_curacion: str,
    destino_curacion: str,
) -> dict[str, str]:
    leer = lector(fila)
    return {
        "fuente": leer("fuente") or "met",
        "id_fuente": leer("id_objeto"),
        "id_registro": leer("id_registro") or f"MET-{leer('id_objeto')}",
        "institucion": leer("institucion") or "The Metropolitan Museum of Art",
        "titulo_original": leer("titulo_original"),
        "titulo_es_sugerido": leer("titulo_es_sugerido"),
        "cultura": leer("cultura"),
        "periodo": leer("periodo"),
        "fecha_objeto": leer("fecha_objeto"),
        "procedencia": leer("procedencia"),
        "clasificacion_original": leer("clasificacion_original"),
        "tipo_objeto": leer("tipo_objeto"),
        "tipo_superficie": leer("tipo_superficie"),
        "material": leer("material") or leer("material_original"),
        "material_normalizado": leer("material_normalizado"),
        "tecnica": leer("tecnica"),
        "descripcion": leer("descripcion") or leer("descripcion_oficial"),
        "url_objeto": leer("url_objeto"),
        "url_imagen": leer("url_imagen"),
        "ruta_imagen_local": leer("imagen_local"),
        "licencia": leer("licencia"),
        "estado_curacion": estado_curacion,
        "destino_curacion": destino_curacion,
        "origen_curacion": leer("origen_curacion"),
        "motivo_curacion": motivo_principal(fila),
        "decision_filtro": leer("decision_filtro"),
        "puntaje_filtro": leer("puntaje_filtro"),
        "motivo_filtrado": leer("motivo_filtrado"),
        "decision_auditoria": leer("decision_auditoria"),
        "motivo_auditoria": leer("motivo_auditoria"),
        "observacion_auditoria": leer("observacion_auditoria"),
        "posible_duplicado_suave": leer("posible_duplicado_suave"),
        "estado_metadata": leer("estado_metadata"),
        "estado_anotacion": leer("estado_anotacion"),
    }


def escribir_reporte(
    ruta: Path,
    principal: list[dict[str, str]],
    secundario: list[dict[str, str]],
    descartados: list[dict[str, str]],
) -> None:
    total = len(principal) + len(secundario) + len(descartados)

    lineas = [
        "# Resumen de curacion MET v2",
        "",
        "Fuente: The Metropolitan Museum of Art.",
        "",
        "La version MET v2 reorganiza las salidas curatoriales ya trabajadas en la version v1, sin sobrescribir los archivos historicos. El objetivo es presentar un flujo mas claro, reproducible y legible para la primera entrega del corpus multimodal de textiles andinos.",
        "",
        "## Conteos consolidados",
        "",
        f"- Corpus principal: {len(principal)} registros",
        f"- Corpus secundario: {len(secundario)} registros",
        f"- Registros descartados: {len(descartados)} registros",
        f"- Total revisado: {total} registros",
        "",
        "## Interpretacion curatorial",
        "",
        "El corpus principal agrupa objetos textiles andinos con valor visual suficiente para analisis computacional. El corpus secundario conserva piezas pertinentes pero menos adecuadas para el primer nucleo de analisis, por ejemplo fragmentos, materialidades mixtas o casos que requieren revision posterior. Los descartados mantienen trazabilidad de exclusion para evitar perdida de informacion metodologica.",
        "",
        "## Archivos generados",
        "",
        "- `data/metadata/met_corpus_principal_v2.csv`",
        "- `data/metadata/met_corpus_secundario_v2.csv`",
        "- `data/metadata/met_descartados_v2.csv`",
    ]

    escribir_texto(ruta, lineas)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Construye salidas MET v2 a partir de los archivos curatoriales MET v1."
    )
    parser.add_argument("--root", default=".", help="Raiz del repositorio.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    raiz = Path(args.root).resolve()

    ruta_principal = raiz / "data/processed/corpus_met_textiles_andinos_v1_principal.csv"
    ruta_secundario = raiz / "data/processed/corpus_met_textiles_andinos_v1_complementario.csv"
    ruta_descartados = raiz / "data/processed/corpus_met_textiles_andinos_v1_exclusiones_curatoriales.csv"

    principal_base = leer_csv(ruta_principal)
    secundario_base = leer_csv(ruta_secundario)
    descartados_base = leer_csv(ruta_descartados)

    principal = [
        normalizar_fila(fila, "corpus_principal", "principal")
        for fila in principal_base
    ]
    secundario = [
        normalizar_fila(fila, "corpus_secundario", "secundario")
        for fila in secundario_base
    ]
    descartados = [
        normalizar_fila(fila, "descartado", "exclusion_curatorial")
        for fila in descartados_base
    ]

    escribir_csv(raiz / "data/metadata/met_corpus_principal_v2.csv", COLUMNAS_V2, principal)
    escribir_csv(raiz / "data/metadata/met_corpus_secundario_v2.csv", COLUMNAS_V2, secundario)
    escribir_csv(raiz / "data/metadata/met_descartados_v2.csv", COLUMNAS_V2, descartados)
    escribir_reporte(
        raiz / "outputs/reports/met_resumen_curacion_v2.md",
        principal,
        secundario,
        descartados,
    )

    print(f"Corpus principal MET v2: {len(principal)}")
    print(f"Corpus secundario MET v2: {len(secundario)}")
    print(f"Descartados MET v2: {len(descartados)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
