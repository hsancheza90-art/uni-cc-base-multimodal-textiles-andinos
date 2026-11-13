"""M4: fusión tardía y aditiva de scores, y su variante por posiciones recíprocas.

Protocolo experimental v2, secciones 4, 7 y 8. Funciones puras: reciben los scores que cada
componente dio a los candidatos de una consulta y devuelven el score fusionado con su
descomposición. No leen archivos ni conocen consultas de prueba.

    s(candidato) = Σ_c α'_c · ŝ_c(candidato),   c ∈ {M0, M2, M3}

- ŝ_c es el score de c normalizado por consulta con mínimo y máximo sobre los candidatos que
  tienen valor. Si todos coinciden, ŝ_c = 0 para todos: el componente no ordena esa consulta.
- Un score None significa «sin evidencia» (en M3, ningún bloque observable en las dos piezas).
  El peso de ese componente se reparte, para ese candidato, entre los demás en proporción a sus
  pesos: α'_c = α_c / Σ α de los componentes con evidencia. El par no recibe similitud máxima.
- Las contribuciones α'_c · ŝ_c suman exactamente el score (primera comprobación de H3) y
  retirar un componente equivale a declararlo sin evidencia (segunda comprobación).

La variante por posiciones recíprocas (decisión R03) suma 1 / (k + posición) sobre los rankings
de los componentes. No tiene pesos y no conserva la descomposición del score.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from fractions import Fraction
from itertools import product

COMPONENTES = ("M0", "M2", "M3")

Scores = Mapping[str, float | None]


def normalizar(scores: Scores) -> dict[str, float | None]:
    """Normalización por mínimo y máximo sobre los candidatos con valor; None se conserva."""
    valores = [v for v in scores.values() if v is not None]
    if not valores:
        return dict(scores)
    minimo, rango = min(valores), max(valores) - min(valores)
    return {i: None if v is None else (v - minimo) / rango if rango > 0 else 0.0 for i, v in scores.items()}


def pesos_efectivos(pesos: Mapping[str, float], disponibles: Sequence[str]) -> dict[str, float]:
    """Pesos de los componentes con evidencia, renormalizados a suma 1 (0 si ninguno pesa)."""
    total = sum(pesos[c] for c in disponibles)
    return {c: pesos[c] / total if total > 0 else 0.0 for c in disponibles}


@dataclass(frozen=True)
class Fusion:
    """Score fusionado de un candidato y su explicación."""

    score: float
    contribuciones: dict[str, float]  # α'_c · ŝ_c de cada componente con evidencia: suman el score
    pesos: dict[str, float]  # α'_c efectivamente usados (suman 1 si algún componente pesa)


def fusionar(scores: Mapping[str, Scores], pesos: Mapping[str, float],
             excluir: frozenset[str] = frozenset()) -> dict[str, Fusion]:
    """Fusiona los scores de una consulta: `scores[componente][candidato]`.

    Todos los componentes deben puntuar los mismos candidatos. `excluir` retira componentes como
    si no tuvieran evidencia para ningún candidato: es la intervención de H3 y la forma de
    calcular las ablaciones sin texto o sin estructura.
    """
    componentes = [c for c in pesos if c not in excluir]
    if any(pesos[c] < 0 for c in pesos):
        raise ValueError("Los pesos de M4 no pueden ser negativos.")
    candidatos = set(scores[componentes[0]]) if componentes else set()
    if any(set(scores[c]) != candidatos for c in componentes):
        raise ValueError("Los componentes no puntúan los mismos candidatos.")
    normalizados = {c: normalizar(scores[c]) for c in componentes}
    fusiones = {}
    for i in sorted(candidatos):
        efectivos = pesos_efectivos(pesos, [c for c in componentes if normalizados[c][i] is not None])
        contribuciones = {c: w * normalizados[c][i] for c, w in efectivos.items()}
        fusiones[i] = Fusion(sum(contribuciones.values()), contribuciones, efectivos)
    return fusiones


def ordenar(puntajes: Mapping[str, float]) -> list[tuple[str, float]]:
    """Ranking de mayor a menor score; los empates (a 9 decimales) se resuelven por id ascendente."""
    return sorted(puntajes.items(), key=lambda par: (-round(par[1], 9), par[0]))


def posiciones_reciprocas(rankings: Mapping[str, Sequence[str]], k: int = 60) -> dict[str, float]:
    """Fusión por posiciones recíprocas (Cormack, Clarke y Büttcher, 2009): Σ 1 / (k + posición).

    Cada ranking debe contener a todos los candidatos, una vez. En el de M3, los pares sin
    evidencia estructural ya ocupan las últimas posiciones, por id (decisión R10).
    """
    conjuntos = [set(r) for r in rankings.values()]
    if any(len(r) != len(set(r)) for r in rankings.values()) or any(c != conjuntos[0] for c in conjuntos):
        raise ValueError("Los rankings no contienen los mismos candidatos, una vez cada uno.")
    puntajes = dict.fromkeys(sorted(conjuntos[0]), 0.0) if conjuntos else {}
    for ranking in rankings.values():
        for posicion, i in enumerate(ranking, start=1):
            puntajes[i] += 1 / (k + posicion)
    return puntajes


def rejilla(valores: Sequence[float], componentes: Sequence[str] = COMPONENTES) -> list[dict[str, float]]:
    """Combinaciones de pesos de la rejilla, normalizadas a suma 1 y sin repetir.

    (0,5; 0,5; 0) y (1; 1; 0) son la misma combinación una vez normalizadas. El orden de salida es
    fijo: lexicográfico descendente en el orden de `componentes`.
    """
    unicas = set()
    for combinacion in product([Fraction(str(v)) for v in valores], repeat=len(componentes)):
        if sum(combinacion) > 0:
            unicas.add(tuple(p / sum(combinacion) for p in combinacion))
    return [dict(zip(componentes, map(float, c))) for c in sorted(unicas, reverse=True)]


def elegir(resultados: Sequence[tuple[Mapping[str, float], float]]) -> dict[str, float]:
    """Combinación con mayor valor medio de la métrica en desarrollo.

    Regla de desempate, fijada antes de ver resultados: entre las combinaciones que empatan (a 9
    decimales) se elige la más cercana a pesos iguales y, si persiste el empate, la primera en
    orden lexicográfico descendente. Con 10 consultas los empates son probables.
    """
    if not resultados:
        raise ValueError("No hay combinaciones que comparar.")

    def clave(resultado: tuple[Mapping[str, float], float]):
        pesos, metrica = resultado
        igual = 1 / len(pesos)
        return (-round(metrica, 9), round(sum((p - igual) ** 2 for p in pesos.values()), 12),
                tuple(-p for p in pesos.values()))

    return dict(min(resultados, key=clave)[0])
