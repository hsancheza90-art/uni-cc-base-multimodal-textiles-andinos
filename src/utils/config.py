"""Rutas y configuracion compartidas por el flujo del corpus."""

from __future__ import annotations

import csv
import tomllib
from pathlib import Path
from typing import Any

RAIZ_REPO = Path(__file__).resolve().parents[2]
RUTA_CONFIG = Path("config/corpus.toml")


def leer_config(raiz: Path = RAIZ_REPO) -> dict[str, Any]:
    with (raiz / RUTA_CONFIG).open("rb") as archivo:
        return tomllib.load(archivo)


def conjuntos_esperados(config: dict[str, Any]) -> list[tuple[str, str, Path, int]]:
    """Devuelve (fuente.etapa, conjunto, ruta relativa, filas esperadas) para cada salida."""
    salida: list[tuple[str, str, Path, int]] = []
    for fuente, etapas in config.items():
        for etapa, conjuntos in etapas.items():
            for conjunto, datos in conjuntos.items():
                if isinstance(datos, dict):
                    salida.append((f"{fuente}.{etapa}", conjunto, Path(datos["ruta"]), int(datos["filas"])))
    return salida


def contar_filas_csv(ruta: Path) -> int:
    with ruta.open(newline="", encoding="utf-8-sig") as archivo:
        return sum(1 for _ in csv.DictReader(archivo))
