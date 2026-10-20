"""Aplica la revision manual AIC v2 con el mismo procedimiento que MET v2.

Uso: python -m src.metadata.apply_aic_review_v2 [--root .]
"""

from __future__ import annotations

from src.metadata.apply_met_review_v2 import main as aplicar


def main(argv: list[str] | None = None) -> int:
    return aplicar(argv, fuente="AIC")


if __name__ == "__main__":
    raise SystemExit(main())
