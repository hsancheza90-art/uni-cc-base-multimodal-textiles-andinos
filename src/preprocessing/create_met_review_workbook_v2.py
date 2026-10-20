"""Crea el workbook maestro de revision manual MET v2.

Uso: python -m src.preprocessing.create_met_review_workbook_v2 [--forzar]

Siembra el workbook con las salidas base MET v2 (src/metadata/build_met_corpus_v2.py):
cada registro llega con su subconjunto v1 en corpus_actual y en corpus_final. La
estructura del workbook es comun a las fuentes (src/preprocessing/workbook_revision.py).
"""

from __future__ import annotations

from pathlib import Path

from src.preprocessing.workbook_revision import COLUMNAS, main_fuente
from src.utils.archivos import leer_csv

ENTRADAS = [
    ("principal", "data/metadata/met_corpus_principal_v2.csv"),
    ("secundario", "data/metadata/met_corpus_secundario_v2.csv"),
    ("descartados", "data/metadata/met_descartados_v2.csv"),
]
# Columnas que registra el revisor: el workbook nuevo las deja vacias.
DECISION = {"motivo_revision", "observaciones_revision", "revisor", "fecha_revision"}


def construir_filas(raiz: Path) -> list[dict[str, str]]:
    filas = []
    for corpus_actual, ruta in ENTRADAS:
        for fila in leer_csv(raiz / ruta):
            salida = {columna: "" if columna in DECISION else fila.get(columna, "") for columna in COLUMNAS}
            salida.update(corpus_actual=corpus_actual, corpus_final=corpus_actual, decision_revision="mantener")
            filas.append(salida)
    return filas


def main(argv: list[str] | None = None) -> int:
    return main_fuente(argv, "MET", construir_filas, [])


if __name__ == "__main__":
    raise SystemExit(main())
