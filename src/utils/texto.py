"""Normalizacion de texto y busqueda de terminos por palabra completa."""

from __future__ import annotations

import re
import unicodedata
from collections.abc import Iterable
from functools import lru_cache
from typing import Any


def normalizar_texto(valor: Any) -> str:
    """Minusculas, sin tildes y con espacios simples. None y NaN se tratan como vacio."""
    if valor is None or (isinstance(valor, float) and valor != valor):
        return ""
    if isinstance(valor, (list, tuple)):
        valor = " ".join(str(parte) for parte in valor if parte is not None)
    texto = unicodedata.normalize("NFD", str(valor).lower())
    texto = "".join(ch for ch in texto if unicodedata.category(ch) != "Mn")
    return re.sub(r"\s+", " ", texto).strip()


@lru_cache(maxsize=4096)
def _patron(termino: str) -> re.Pattern[str]:
    # Limites de palabra que no dependen de \b, para que "vicuna" o "south coast" funcionen igual.
    return re.compile(rf"(?<![a-z0-9]){re.escape(normalizar_texto(termino))}(?![a-z0-9])")


def buscar_terminos(texto: Any, terminos: Iterable[str]) -> list[str]:
    """Terminos presentes en el texto como palabra o frase completa, en el orden dado."""
    normalizado = normalizar_texto(texto)
    if not normalizado:
        return []
    return [termino for termino in terminos if _patron(termino).search(normalizado)]


def posicion_termino(texto: Any, termino: str) -> int:
    """Posicion de la primera aparicion del termino como palabra completa, o -1."""
    coincidencia = _patron(termino).search(normalizar_texto(texto))
    return coincidencia.start() if coincidencia else -1


def unir_textos(*valores: Any) -> str:
    return " ".join(normalizar_texto(valor) for valor in valores if normalizar_texto(valor))
