"""Métricas e inferencia del experimento de recuperación (protocolo experimental v2, secciones 6 a 8).

Funciones puras, sin lectura ni escritura de archivos: reciben rankings y juicios ya cargados y
devuelven números. No leen consultas ni juicios de prueba por su cuenta; quien las llama decide
qué datos pasa. Definiciones:

- nDCG@k con ganancia 2^rel - 1 y descuento log2(r + 1); el ideal se calcula con todos los
  juicios de la consulta. Un candidato sin juicio cuenta como 0. Un par `no_evaluable` no equivale
  a 0: se retira del ranking y del ideal.
- H1 y H2 se deciden con una prueba de permutación pareada por cambio de signo, bilateral
  (decisión R01 de docs/registro_decisiones.md); la t de Student pareada es la comprobación y el
  bootstrap pareado da solo el intervalo.
- El efecto mínimo detectable se calcula antes del test con la desviación estándar de las
  diferencias en desarrollo (decisión R04).
"""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from statistics import NormalDist

import numpy as np

NO_EVALUABLE = None
"""Valor de un juicio `no_evaluable` en los mapas de juicios (los grados son 0, 1, 2 y 3)."""

SE_SOSTIENE = "se sostiene"
FAVORABLE = "dirección favorable sin evidencia suficiente"
NO_SE_SOSTIENE = "no se sostiene"

Juicios = Mapping[str, int | None]


def evaluables(ranking: Sequence[str], juicios: Juicios) -> list[str]:
    """El ranking sin los candidatos juzgados como `no_evaluable`, en el mismo orden."""
    return [i for i in ranking if not (i in juicios and juicios[i] is NO_EVALUABLE)]


def grado(candidato: str, juicios: Juicios) -> int:
    """Grado de relevancia de un candidato; sin juicio cuenta como 0 (protocolo, sección 6)."""
    valor = juicios.get(candidato, 0)
    return 0 if valor is NO_EVALUABLE else int(valor)


def dcg(grados: Sequence[int]) -> float:
    """Ganancia acumulada con descuento: suma de (2^rel - 1) / log2(r + 1), con r desde 1."""
    return sum((2**g - 1) / math.log2(r + 1) for r, g in enumerate(grados, start=1))


def ndcg(ranking: Sequence[str], juicios: Juicios, k: int) -> float | None:
    """nDCG@k de una consulta, o None si ningún candidato juzgado alcanza el grado 1.

    El ideal ordena todos los juicios de la consulta, estén o no en el ranking: un relevante que
    el sistema dejó fuera de los k primeros baja la medida.
    """
    ideal = dcg(sorted((g for g in juicios.values() if g is not NO_EVALUABLE), reverse=True)[:k])
    if ideal == 0:
        return None
    return dcg([grado(i, juicios) for i in evaluables(ranking, juicios)[:k]]) / ideal


def precision(ranking: Sequence[str], juicios: Juicios, k: int, umbral: int = 2) -> float:
    """P@k con la relevancia binarizada en `umbral`; el denominador es siempre k."""
    return sum(grado(i, juicios) >= umbral for i in evaluables(ranking, juicios)[:k]) / k


def rango_reciproco(ranking: Sequence[str], juicios: Juicios, umbral: int = 2) -> float:
    """1 / posición del primer candidato con grado >= umbral; 0 si no hay ninguno."""
    for r, i in enumerate(evaluables(ranking, juicios), start=1):
        if grado(i, juicios) >= umbral:
            return 1 / r
    return 0.0


def proporcion_juzgada(ranking: Sequence[str], juicios: Juicios, k: int) -> float:
    """Parte de los k primeros del ranking que tiene juicio (los `no_evaluable` cuentan como juzgados)."""
    primeros = list(ranking)[:k]
    return sum(i in juicios for i in primeros) / len(primeros) if primeros else float("nan")


def sin_aportes_unicos(juicios: Juicios, procedencia: Mapping[str, set[str]], sistema: str) -> dict[str, int | None]:
    """Los juicios de una consulta sin los candidatos que solo `sistema` aportó al pool.

    Es la prueba de retirar los aportes únicos (Buckley et al., 2007): al recalcular la métrica de
    `sistema` con estos juicios, sus aportes únicos pasan a contar como no juzgados. La diferencia
    con la métrica original mide cuánto depende el sistema de haber contribuido al pool.
    """
    return {i: g for i, g in juicios.items() if procedencia.get(i, set()) != {sistema}}


def diferencias(a: Mapping[str, float | None], b: Mapping[str, float | None]) -> tuple[list[float], list[str]]:
    """Diferencias pareadas a - b por consulta y las consultas excluidas por no tener valor en alguna.

    Las consultas se recorren en orden alfabético para que el resultado no dependa del orden de
    entrada. Una consulta sin relevantes (None) se excluye y se informa; no se reemplaza.
    """
    comunes = sorted(set(a) | set(b))
    excluidas = [c for c in comunes if a.get(c) is None or b.get(c) is None]
    return [a[c] - b[c] for c in comunes if c not in excluidas], excluidas


def permutacion_pareada(d: Sequence[float], replicas: int, semilla: int) -> float:
    """Valor p bilateral de la prueba de permutación pareada por cambio de signo sobre la media.

    Bajo la hipótesis nula, el signo de cada diferencia es intercambiable. Se estima con `replicas`
    asignaciones aleatorias de signos y la corrección (1 + casos) / (1 + replicas), que nunca da 0.
    """
    x = np.asarray(d, dtype=float)
    if x.size == 0:
        return float("nan")
    signos = np.random.default_rng(semilla).choice((-1.0, 1.0), size=(replicas, x.size))
    medias = np.abs((signos * x).mean(axis=1))
    extremas = int((medias >= abs(x.mean()) - 1e-12).sum())
    return (1 + extremas) / (1 + replicas)


def beta_incompleta(a: float, b: float, x: float) -> float:
    """Función beta incompleta regularizada I_x(a, b), por fracción continua (método de Lentz)."""
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    if x > (a + 1) / (a + b + 2):
        return 1 - beta_incompleta(b, a, 1 - x)
    frente = math.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log(1 - x)) / a
    minimo = 1e-300
    c, e = 1.0, 1 - (a + b) * x / (a + 1)
    e = 1 / (e if abs(e) > minimo else minimo)
    f = e
    for m in range(1, 300):
        for numerador in (m * (b - m) * x / ((a + 2 * m - 1) * (a + 2 * m)),
                          -(a + m) * (a + b + m) * x / ((a + 2 * m) * (a + 2 * m + 1))):
            e = 1 + numerador * e
            e = 1 / (e if abs(e) > minimo else minimo)
            c = 1 + numerador / c
            c = c if abs(c) > minimo else minimo
            f *= e * c
        if abs(e * c - 1) < 1e-14:
            break
    return frente * f


def t_pareada(d: Sequence[float]) -> tuple[float, float]:
    """Estadístico t de Student pareado y su valor p bilateral, con n - 1 grados de libertad.

    Si las diferencias no varían, el estadístico no está definido: devuelve (nan, nan).
    """
    x = np.asarray(d, dtype=float)
    if x.size < 2 or np.ptp(x) == 0:
        return float("nan"), float("nan")
    gl = x.size - 1
    t = float(x.mean() / (x.std(ddof=1) / math.sqrt(x.size)))
    return t, beta_incompleta(gl / 2, 0.5, gl / (gl + t * t))


def intervalo_bootstrap(d: Sequence[float], replicas: int, confianza: float, semilla: int) -> tuple[float, float]:
    """Intervalo de confianza de la media por bootstrap pareado de consultas (percentiles).

    Se remuestrean las consultas con reemplazo; al trabajar sobre las diferencias, el remuestreo
    es el mismo para los dos sistemas. Describe la magnitud; no decide las hipótesis.
    """
    x = np.asarray(d, dtype=float)
    if x.size == 0:
        return float("nan"), float("nan")
    indices = np.random.default_rng(semilla).integers(0, x.size, size=(replicas, x.size))
    medias = x[indices].mean(axis=1)
    cola = (1 - confianza) / 2
    return float(np.quantile(medias, cola)), float(np.quantile(medias, 1 - cola))


def decidir(media: float, p: float, umbral: float, alfa: float) -> str:
    """Regla de decisión de H1 y H2 (protocolo, sección 1)."""
    if media >= umbral and p < alfa:
        return SE_SOSTIENE
    if media > 0 and p >= alfa:
        return FAVORABLE
    return NO_SE_SOSTIENE


@dataclass(frozen=True)
class Comparacion:
    """Comparación pareada de dos sistemas sobre las mismas consultas."""

    n: int
    excluidas: list[str]
    media: float
    desviacion: float
    p_permutacion: float
    t: float
    p_t: float
    intervalo: tuple[float, float]
    decision: str


def comparar(a: Mapping[str, float | None], b: Mapping[str, float | None], *, umbral: float, alfa: float,
             confianza: float, replicas: int, semilla_permutacion: int, semilla_bootstrap: int) -> Comparacion:
    """Compara el sistema a con el b: diferencia media, contraste, comprobación, intervalo y decisión."""
    d, excluidas = diferencias(a, b)
    x = np.asarray(d, dtype=float)
    media = float(x.mean()) if x.size else float("nan")
    p = permutacion_pareada(d, replicas, semilla_permutacion)
    t, p_t = t_pareada(d)
    return Comparacion(
        n=len(d), excluidas=excluidas, media=media,
        desviacion=float(x.std(ddof=1)) if x.size > 1 else float("nan"),
        p_permutacion=p, t=t, p_t=p_t,
        intervalo=intervalo_bootstrap(d, replicas, confianza, semilla_bootstrap),
        decision=decidir(media, p, umbral, alfa) if x.size else NO_SE_SOSTIENE,
    )


def efecto_minimo_detectable(desviacion: float, n: int, alfa: float = 0.05, potencia: float = 0.8) -> float:
    """Diferencia media que una prueba pareada bilateral detectaría con la potencia dada.

    (z_{1 - alfa/2} + z_{potencia}) · DE / raíz(n), con la aproximación normal del protocolo. Se
    calcula antes de abrir el test, con la desviación estándar de las diferencias en desarrollo.
    """
    normal = NormalDist()
    return (normal.inv_cdf(1 - alfa / 2) + normal.inv_cdf(potencia)) * desviacion / math.sqrt(n)


def consultas_necesarias(desviacion: float, umbral: float, alfa: float = 0.05, potencia: float = 0.8) -> int:
    """Número de consultas para detectar `umbral` con la potencia dada (fórmula del protocolo, sección 7)."""
    return math.ceil((efecto_minimo_detectable(desviacion, 1, alfa, potencia) / umbral) ** 2)


def rango_desviacion(desviacion: float, n: int, confianza: float = 0.95) -> tuple[float, float]:
    """Intervalo de confianza de una desviación estándar estimada con n diferencias.

    Supone diferencias aproximadamente normales y usa la aproximación de Wilson y Hilferty a los
    cuantiles de ji cuadrado. Con 10 consultas de desarrollo el rango es amplio: por eso el efecto
    mínimo detectable se informa con sus dos extremos y no como un solo número.
    """
    gl = n - 1
    normal = NormalDist()

    def ji_cuadrado(p: float) -> float:
        return gl * (1 - 2 / (9 * gl) + normal.inv_cdf(p) * math.sqrt(2 / (9 * gl))) ** 3

    cola = (1 - confianza) / 2
    return desviacion * math.sqrt(gl / ji_cuadrado(1 - cola)), desviacion * math.sqrt(gl / ji_cuadrado(cola))
