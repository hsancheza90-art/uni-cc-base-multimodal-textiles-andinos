"""Medidas de acuerdo y separacion: calibracion y validacion del puntaje de aptitud y acuerdo entre anotadores.

Se implementan aqui, sin dependencias, porque son pocas y conviene que su definicion
sea explicita en el texto de la tesis.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

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


@dataclass(frozen=True)
class Acuerdo:
    """Acuerdo entre dos anotadores sobre n piezas; kappa es None cuando no se puede estimar."""

    n: int
    observado: float | None
    esperado: float | None
    kappa: float | None
    motivo: str = ""  # por que no se pudo estimar


def kappa_detalle(
    pares: list[tuple[str, str]], categorias: list[str] | None = None, ponderado: bool = False
) -> Acuerdo:
    """Kappa de Cohen con sus acuerdos observado y esperado, simple o ponderado lineal.

    Con la tabla de contingencia p (proporciones) y los marginales a y b de cada anotador:

        observado = sum_ij w_ij p_ij,  esperado = sum_ij w_ij a_i b_j,
        kappa = (observado - esperado) / (1 - esperado),

    con w_ij = 1 si i = j y 0 si no (simple), o w_ij = 1 - |i - j| / (k - 1) (ponderado
    lineal, Cohen 1968), que cuenta como acuerdo parcial un desacuerdo entre categorias
    vecinas. El ponderado exige `categorias` en su orden. Si los dos anotadores usan una
    sola categoria, el acuerdo esperado es 1 y kappa no esta definido: se devuelve None
    con el motivo, nunca 1 ni 0.
    """
    if not pares:
        return Acuerdo(0, None, None, None, "sin piezas comparables")
    observadas = sorted({valor for par in pares for valor in par})
    if categorias is None:
        if ponderado:
            raise ValueError("El kappa ponderado necesita el orden de las categorias.")
        categorias = observadas
    fuera = [valor for valor in observadas if valor not in categorias]
    if fuera:
        raise ValueError(f"Valores fuera de las categorias declaradas: {fuera}")
    indice = {categoria: i for i, categoria in enumerate(categorias)}
    k = len(categorias)
    tabla_p = np.zeros((k, k))
    for a, b in pares:
        tabla_p[indice[a], indice[b]] += 1
    tabla_p /= len(pares)
    if ponderado and k > 1:
        i, j = np.indices((k, k))
        pesos = 1 - np.abs(i - j) / (k - 1)
    else:
        pesos = np.eye(k)
    observado = float((pesos * tabla_p).sum())
    esperado = float((pesos * np.outer(tabla_p.sum(axis=1), tabla_p.sum(axis=0))).sum())
    if len(observadas) == 1 or np.isclose(esperado, 1.0):
        return Acuerdo(len(pares), observado, esperado, None, f"una sola categoria observada ({observadas[0]})")
    return Acuerdo(len(pares), observado, esperado, (observado - esperado) / (1 - esperado))


def jaccard(a: set[str], b: set[str]) -> float:
    """Indice de Jaccard |a ∩ b| / |a ∪ b|; dos conjuntos vacios coinciden (1)."""
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b)


def tabla(filas: list[list[str]], encabezado: list[str]) -> list[str]:
    """Tabla en Markdown para los informes de outputs/reports/."""
    lineas = ["| " + " | ".join(encabezado) + " |", "|" + "---|" * len(encabezado)]
    lineas += ["| " + " | ".join(str(celda) for celda in fila) + " |" for fila in filas]
    return lineas
