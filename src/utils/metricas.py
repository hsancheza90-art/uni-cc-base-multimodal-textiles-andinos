"""Medidas de acuerdo y separacion usadas para calibrar y validar el puntaje de aptitud.

Se implementan aqui, sin dependencias, porque son pocas y conviene que su definicion
sea explicita en el texto de la tesis.
"""

from __future__ import annotations

from collections import Counter

import numpy as np


def auc(positivos: list[float], negativos: list[float]) -> float:
    """Area bajo la curva ROC como estadistico U de Mann-Whitney (los empates cuentan la mitad).

    Probabilidad de que un caso positivo elegido al azar puntue mas alto que uno negativo:
    0,5 es azar y 1 separacion perfecta. Es independiente del umbral, por eso se usa para
    comparar medidas y modelos antes de fijar las bandas.
    """
    if not positivos or not negativos:
        return float("nan")
    p, n = np.array(positivos)[:, None], np.array(negativos)[None, :]
    return float(((p > n).sum() + 0.5 * (p == n).sum()) / (p.size * n.size))


def kappa(pares: list[tuple[str, str]]) -> float:
    """Kappa de Cohen: acuerdo entre dos clasificaciones corregido por el acuerdo esperado al azar.

    Con la escala usual (Landis y Koch, 1977), 0,41-0,60 es moderado y 0,61-0,80 sustancial;
    el criterio acordado para aplicar el modelo a una fuente nueva es kappa >= 0,6.
    """
    if not pares:
        return float("nan")
    total = len(pares)
    observado = sum(a == b for a, b in pares) / total
    marginal_a, marginal_b = Counter(a for a, _ in pares), Counter(b for _, b in pares)
    esperado = sum(marginal_a[c] * marginal_b[c] for c in set(marginal_a) | set(marginal_b)) / total**2
    return (observado - esperado) / (1 - esperado) if esperado < 1 else float("nan")


def tabla(filas: list[list[str]], encabezado: list[str]) -> list[str]:
    """Tabla en Markdown para los informes de outputs/reports/."""
    lineas = ["| " + " | ".join(encabezado) + " |", "|" + "---|" * len(encabezado)]
    lineas += ["| " + " | ".join(str(celda) for celda in fila) + " |" for fila in filas]
    return lineas
