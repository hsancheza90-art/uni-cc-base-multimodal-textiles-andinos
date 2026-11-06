"""M0: BM25 sobre el texto de la ficha de cada pieza (protocolo experimental, sección 4).

El documento de una pieza es la unión de los campos de [m0] campos en config/modelos.toml,
normalizados con src/utils/texto.py (minúsculas, sin tildes). La descripción de las fuentes de
[m0] excluir_descripcion no entra (en MET es una plantilla armada con los metadatos, no un texto
del museo). Los términos son secuencias de letras y dígitos de al menos longitud_minima_termino
caracteres; no hay lista de palabras vacías.

Okapi BM25 con idf = ln((N - n + 0,5) / (n + 0,5) + 1), donde N es el número de documentos del
índice y n los que contienen el término. En la tarea T3 la consulta es el texto de la pieza
consultada: es una condición de metadatos y se rotula así.
"""

from __future__ import annotations

import math
import re
from collections import Counter
from typing import Any

from src.utils.texto import normalizar_texto

TERMINO = re.compile(r"[a-z0-9]+")


def documento(fila: dict[str, str], config: dict[str, Any]) -> str:
    """Texto de la pieza con los campos de [m0], sin la descripción de las fuentes excluidas."""
    campos = [c for c in config["campos"] if not (c == "descripcion" and fila["fuente"] in config["excluir_descripcion"])]
    return " ".join(normalizar_texto(fila.get(c, "")) for c in campos if fila.get(c))


def tokenizar(texto: str, minimo: int) -> list[str]:
    return [t for t in TERMINO.findall(normalizar_texto(texto)) if len(t) >= minimo]


class Bm25:
    """Índice BM25 sobre documentos ya tokenizados, por id."""

    def __init__(self, documentos: dict[str, list[str]], k1: float, b: float) -> None:
        self.k1, self.b = k1, b
        self.frecuencias = {id_: Counter(terminos) for id_, terminos in documentos.items()}
        self.longitud = {id_: len(terminos) for id_, terminos in documentos.items()}
        self.media = sum(self.longitud.values()) / len(documentos) if documentos else 0.0
        presentes = Counter(t for frecuencia in self.frecuencias.values() for t in frecuencia)
        total = len(documentos)
        self.idf = {t: math.log((total - n + 0.5) / (n + 0.5) + 1) for t, n in presentes.items()}

    def puntuar(self, consulta: list[str], id_documento: str) -> float:
        frecuencia, longitud = self.frecuencias[id_documento], self.longitud[id_documento]
        norma = self.k1 * (1 - self.b + self.b * longitud / self.media) if self.media else self.k1
        return sum(self.idf.get(t, 0.0) * frecuencia[t] * (self.k1 + 1) / (frecuencia[t] + norma)
                   for t in consulta if frecuencia[t])


def indice(filas: list[dict[str, str]], config: dict[str, Any]) -> tuple[Bm25, dict[str, list[str]]]:
    """Índice BM25 de las piezas y sus términos (que sirven también como consulta de cada pieza)."""
    terminos = {f["id_global"]: tokenizar(documento(f, config), int(config["longitud_minima_termino"])) for f in filas}
    return Bm25(terminos, float(config["k1"]), float(config["b"])), terminos
