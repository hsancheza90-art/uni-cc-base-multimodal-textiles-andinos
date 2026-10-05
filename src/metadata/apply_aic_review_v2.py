"""Aplica la revision manual AIC v2 con el mismo procedimiento que MET v2.

Uso: python -m src.metadata.apply_aic_review_v2 [--root .]
"""

from __future__ import annotations

import argparse
from pathlib import Path

from src.metadata.apply_met_review_v2 import FuenteRevision, aplicar_revision

AIC = FuenteRevision(
    nombre="AIC v2",
    workbook="data/metadata/aic_revision_manual_v2.xlsx",
    hoja="revision_aic_v2",
    salidas={
        "principal": "data/metadata/aic_corpus_principal_v2_revisado.csv",
        "secundario": "data/metadata/aic_corpus_secundario_v2_revisado.csv",
        "descartados": "data/metadata/aic_descartados_v2_revisado.csv",
    },
    pendientes="data/metadata/aic_pendientes_revision_v2.csv",
    reporte="outputs/reports/aic_resumen_revision_manual_v2.md",
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Aplica la revision manual AIC v2 desde Excel.")
    parser.add_argument("--root", default=".", help="Raiz del repositorio.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    return aplicar_revision(Path(parse_args(argv).root).resolve(), AIC)


if __name__ == "__main__":
    raise SystemExit(main())
