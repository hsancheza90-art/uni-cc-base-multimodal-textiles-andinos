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
    return re.sub(r"\s+", " ", sin_tildes(str(valor).lower())).strip()


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


def texto_plano(valor: Any) -> str:
    """Valor de una respuesta de API como texto de una linea, sin normalizar.

    None -> ""; listas unidas con «; » (sin elementos vacios); diccionarios como
    «clave: valor»; el resto, con los espacios en blanco reducidos a uno.
    """
    if valor is None:
        return ""
    if isinstance(valor, list):
        return "; ".join(parte for parte in (texto_plano(v) for v in valor) if parte)
    if isinstance(valor, dict):
        return "; ".join(f"{clave}: {texto_plano(v)}" for clave, v in valor.items() if v)
    return " ".join(str(valor).split())


def sin_tildes(texto: str) -> str:
    """Quita las marcas diacriticas (á -> a) sin cambiar mayusculas ni espacios."""
    return "".join(ch for ch in unicodedata.normalize("NFD", texto) if unicodedata.category(ch) != "Mn")


def unir_textos(*valores: Any) -> str:
    return " ".join(normalizar_texto(valor) for valor in valores if normalizar_texto(valor))
