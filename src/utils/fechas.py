"""Año de inicio de las fechas que las fuentes registran como texto.

MET y CMA describen la fecha del objeto en texto libre («7th–9th century»,
«5th–2nd century BCE», «c. 1400–1532», «400–200 BCE», «1600s–1700s»,
«early 1900s»). anio_inicio devuelve el primer año del intervalo (negativo antes
de la era comun) o None si no se reconoce. Es la cota que usa la regla de
periodo del puntaje de aptitud: inicio posterior a 1532 -> fuera del estudio.
"""

from __future__ import annotations

import re

ERA_ANTES = r"(?:bce|b\.c\.e?\.?|bc)"
ERA_DESPUES = r"(?:ce|c\.e\.|a\.d\.|ad)"
MODIFICADOR = {"early": 0, "mid": 33, "middle": 33, "late": 66}

SIGLO = re.compile(
    rf"(?:(early|mid|middle|late)[\s-]+)?(\d{{1,2}})(?:st|nd|rd|th)\b(?:\s*century)?(?:\s*({ERA_ANTES}|{ERA_DESPUES}))?"
)
ANIO = re.compile(rf"(?:(early|mid|middle|late)[\s-]+)?(\d{{1,4}})(s)?\b(?:\s*({ERA_ANTES}|{ERA_DESPUES}))?")


def era_negativa(marca: str | None) -> bool | None:
    if not marca:
        return None
    return bool(re.fullmatch(ERA_ANTES, marca))


def anio_inicio(texto: str | None) -> int | None:
    """Primer año del intervalo descrito en el texto, o None si no se reconoce."""
    if not texto:
        return None
    t = texto.lower().replace("–", "-").replace("—", "-").replace("−", "-")
    t = re.sub(r"\(.*?\)", " ", t)                 # notas: «(radiocarbon date, 95% probability)», «(?)»
    t = re.sub(r"\bc(?:a|irca)?\.\s*", "", t)      # «c. 1400», «ca. 1400»
    t = re.sub(r"\b(early|mid|middle|late)-", r"\1 ", t)  # «mid-1800s»: ese guion no separa un intervalo
    izquierda, _, derecha = t.partition("-")

    if "century" in t:
        primero = SIGLO.search(izquierda)
        if not primero:
            return None
        negativa = era_negativa(primero.group(3))
        if negativa is None:
            segundo = SIGLO.search(derecha)
            negativa = bool(segundo and era_negativa(segundo.group(3)))
        siglo = int(primero.group(2))
        desplazamiento = MODIFICADOR.get(primero.group(1) or "", 0)
        return -siglo * 100 + desplazamiento if negativa else (siglo - 1) * 100 + desplazamiento

    primero = ANIO.search(izquierda)
    if not primero:
        return None
    negativa = era_negativa(primero.group(4))
    if negativa is None:
        segundo = ANIO.search(derecha)
        negativa = bool(segundo and era_negativa(segundo.group(4)))
    anio = int(primero.group(2)) + (MODIFICADOR.get(primero.group(1) or "", 0) if primero.group(3) else 0)
    return -anio if negativa else anio
