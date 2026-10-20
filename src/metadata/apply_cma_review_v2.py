"""Aplica la revision manual CMA v2 con el mismo procedimiento y esquema que MET v2.

Uso: python -m src.metadata.apply_cma_review_v2 [--root .]

Hasta octubre de 2026 los CSV revisados de CMA conservaban el esquema de la curacion
CMA v1 (id_objeto, decision_auditoria...). El consolidado v1 lee sus copias congeladas
(data/metadata/v1_congelado/), por lo que la serie v1 no cambia con la unificacion.
"""

from __future__ import annotations

from src.metadata.apply_met_review_v2 import main as aplicar


def main(argv: list[str] | None = None) -> int:
    return aplicar(argv, fuente="CMA")


if __name__ == "__main__":
    raise SystemExit(main())
