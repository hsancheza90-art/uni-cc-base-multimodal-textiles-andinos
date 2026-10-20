"""Copia de insumos versionados a un directorio temporal, para regenerar salidas en las pruebas."""

from __future__ import annotations

import shutil
from collections.abc import Iterable
from pathlib import Path

from src.utils.config import RAIZ_REPO


def copiar_insumos(destino: Path, relativas: Iterable[str]) -> None:
    for relativa in relativas:
        (destino / relativa).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(RAIZ_REPO / relativa, destino / relativa)
