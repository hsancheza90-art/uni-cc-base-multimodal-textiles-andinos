"""Punto de entrada unico del flujo reproducible del corpus MET v2 + CMA v2.

Uso desde la raiz del repositorio:

    python -m src.flujo
    python -m src.flujo --root ruta/a/una/copia

Ejecuta, sin acceso a red, los pasos que regeneran los CSV curados a partir de
los insumos versionados (corpus MET v1 y workbooks de revision manual) y
verifica los conteos esperados de config/corpus.toml.
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Callable
from pathlib import Path

from src.metadata import (
    apply_cma_review_v2,
    apply_met_review_v2,
    audit_cma_outputs,
    audit_met_outputs_v2,
    build_met_corpus_v2,
)
from src.utils.config import RAIZ_REPO, conjuntos_esperados, contar_filas_csv, leer_config

PASOS: list[tuple[str, Callable[[list[str]], int]]] = [
    ("MET v2: construir salidas base", build_met_corpus_v2.main),
    ("MET v2: auditar salidas base", audit_met_outputs_v2.main),
    ("MET v2: aplicar revision manual", apply_met_review_v2.main),
    ("CMA v2: aplicar revision manual", apply_cma_review_v2.main),
    ("CMA v2: auditar candidatos", audit_cma_outputs.main),
]


def verificar_conteos(raiz: Path) -> list[str]:
    problemas: list[str] = []
    for etapa, conjunto, ruta, esperado in conjuntos_esperados(leer_config(raiz)):
        ruta_absoluta = raiz / ruta
        if not ruta_absoluta.exists():
            problemas.append(f"{etapa}.{conjunto}: falta {ruta}")
            continue
        observado = contar_filas_csv(ruta_absoluta)
        estado = "ok" if observado == esperado else "DIFERENTE"
        print(f"  {etapa:<16} {conjunto:<12} {observado:>4} (esperado {esperado:>4})  {estado}")
        if observado != esperado:
            problemas.append(f"{etapa}.{conjunto}: {observado} filas, se esperaban {esperado}")
    return problemas


def ejecutar(raiz: Path) -> int:
    argv = ["--root", str(raiz)]
    for numero, (nombre, paso) in enumerate(PASOS, start=1):
        print(f"\n[{numero}/{len(PASOS)}] {nombre}")
        codigo = paso(argv)
        if codigo != 0:
            print(f"\nEl paso '{nombre}' termino con codigo {codigo}. Flujo detenido.")
            return codigo

    print("\nVerificacion de conteos (config/corpus.toml)")
    problemas = verificar_conteos(raiz)
    if problemas:
        print("\nConteos fuera de lo esperado:")
        for problema in problemas:
            print(f"- {problema}")
        return 1

    print("\nFlujo completado sin hallazgos.")
    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Regenera y verifica el corpus MET v2 + CMA v2.")
    parser.add_argument("--root", default=str(RAIZ_REPO), help="Raiz del repositorio.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    return ejecutar(Path(args.root).resolve())


if __name__ == "__main__":
    sys.exit(main())
