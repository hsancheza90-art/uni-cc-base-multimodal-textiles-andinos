"""Métricas e inferencia del experimento de recuperación (protocolo experimental v2, secciones 6 a 8).

Funciones puras, sin lectura ni escritura de archivos: reciben rankings y juicios ya cargados y
devuelven números. No leen consultas ni juicios de prueba por su cuenta; quien las llama decide
qué datos pasa. Definiciones:

- nDCG@k con ganancia 2^rel - 1 y descuento log2(r + 1); el ideal se calcula con todos los
  juicios de la consulta. Un candidato sin juicio cuenta como 0. Un par `no_evaluable` no equivale
  a 0: se retira del ranking y del ideal.
- H1 y H2 se deciden con una prueba de permutación pareada por cambio de signo, bilateral
  (decisión R01 de docs/registro_decisiones.md); la t de Student pareada es la comprobación y el
  bootstrap pareado da solo el intervalo. H1 usa B réplicas fijas y se informa el error de Monte
  Carlo (R34); H2 usa la enumeración exacta de los 2^m cambios de signo (R35).
- Una diferencia con |d| ≤ TOLERANCIA_EMPATES cuenta como cero (R35).
- La regla de decisión separa tres afirmaciones (frente a cero, estimación y relevancia práctica)
  y H2 solo es confirmatoria si H1 se sostiene (secuencia fija, R33).
- El efecto mínimo detectable se calcula antes del test con la desviación estándar de las
  diferencias en desarrollo (decisión R04); en H2 no se usa (R35).
"""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, replace
from statistics import NormalDist

import numpy as np

NO_EVALUABLE = None
"""Valor de un juicio `no_evaluable` en los mapas de juicios (los grados son 0, 1, 2 y 3)."""

TOLERANCIA_EMPATES = 1e-12
"""Valor por defecto; el que rige es `[metricas] tolerancia_empates` de config/experimento.toml."""

# Lecturas de una comparación (protocolo, sección 7). Solo SE_SOSTIENE sostiene la hipótesis.
SE_SOSTIENE = "se sostiene"
BAJO_UMBRAL = "mejora distinta de cero, por debajo del umbral práctico"
INFERIOR = "inferior al sistema de referencia"
FAVORABLE = "dirección favorable sin evidencia suficiente"
NO_DETECTADA = "no se detectó una mejora"
EXPLORATORIA = "exploratoria: H1 no se sostiene (secuencia fija)"
LECTURAS = (SE_SOSTIENE, BAJO_UMBRAL, INFERIOR, FAVORABLE, NO_DETECTADA)

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


def sin_empates(d: Sequence[float], tolerancia: float = TOLERANCIA_EMPATES) -> np.ndarray:
    """Las diferencias con |d| ≤ tolerancia pasan a ser exactamente 0 (decisión R35)."""
    x = np.asarray(d, dtype=float)
    return np.where(np.abs(x) <= tolerancia, 0.0, x)


def permutacion_pareada(d: Sequence[float], replicas: int, semilla: int,
                        tolerancia: float = TOLERANCIA_EMPATES) -> float:
    """Valor p bilateral de la prueba de permutación pareada por cambio de signo (H1, decisión R34).

    Bajo la hipótesis nula, el signo de cada diferencia es intercambiable. El estadístico es
    |Σ d|. Se calculan exactamente `replicas` asignaciones aleatorias de signos, en bloques para
    acotar la memoria, sin parada anticipada, y p = (b + 1) / (B + 1), que nunca da 0.
    """
    x = sin_empates(d, tolerancia)
    if x.size == 0:
        return float("nan")
    observado = abs(x.sum())
    generador = np.random.default_rng(semilla)
    extremas, hechas, bloque = 0, 0, 10_000
    while hechas < replicas:
        filas = min(bloque, replicas - hechas)
        signos = generador.choice((-1.0, 1.0), size=(filas, x.size))
        extremas += int((np.abs(signos @ x) >= observado - tolerancia).sum())
        hechas += filas
    return (1 + extremas) / (1 + replicas)


def error_monte_carlo(p: float, replicas: int) -> float:
    """Error estándar de Monte Carlo de una p estimada con `replicas` réplicas: raíz(p(1 - p)/B)."""
    return math.sqrt(p * (1 - p) / replicas) if p == p else float("nan")


def permutacion_exacta(d: Sequence[float], tolerancia: float = TOLERANCIA_EMPATES) -> tuple[float, int]:
    """Valor p bilateral exacto por enumeración de los 2^m cambios de signo (H2, decisión R35).

    Solo las m diferencias distintas de cero cambian el estadístico |Σ d|; las nulas no aportan.
    p es la proporción de los 2^m vectores de signos cuyo estadístico iguala o supera al
    observado, incluido el observado. Con m = 0, p = 1. Devuelve (p, m).
    """
    x = sin_empates(d, tolerancia)
    no_nulas = x[x != 0]
    m = int(no_nulas.size)
    if m == 0:
        return 1.0, 0
    if m > 20:
        raise ValueError(f"La enumeración exacta no está prevista para m = {m} > 20 diferencias distintas de cero.")
    codigos = np.arange(2**m, dtype=np.int64)[:, None]
    signos = 1.0 - 2.0 * ((codigos >> np.arange(m, dtype=np.int64)) & 1)
    estadisticos = np.abs(signos @ no_nulas)
    return float((estadisticos >= abs(no_nulas.sum()) - tolerancia).mean()), m


def p_minima(m: int) -> float:
    """p mínima alcanzable por la prueba exacta bilateral con m diferencias distintas de cero: 2^(1 - m)."""
    return 1.0 if m <= 0 else 2.0 ** (1 - m)


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


@dataclass(frozen=True)
class Afirmaciones:
    """Las tres afirmaciones que componen la regla de decisión (protocolo, sección 7; R34)."""

    frente_a_cero: bool  # la permutación da p < alfa
    relevancia_practica: bool  # la diferencia media es >= umbral
    lectura: str  # una de LECTURAS

    @property
    def sostiene(self) -> bool:
        return self.lectura == SE_SOSTIENE


def decidir(media: float, p: float, umbral: float, alfa: float,
            tolerancia: float = TOLERANCIA_EMPATES) -> Afirmaciones:
    """Regla de decisión de H1 y H2: tres afirmaciones separadas y su lectura conjunta.

    - p < alfa y media >= umbral: se sostiene.
    - p < alfa y 0 < media < umbral: mejora distinta de cero, por debajo del umbral práctico.
    - p < alfa y media < 0: inferior al sistema de referencia.
    - p >= alfa y media > 0: dirección favorable sin evidencia suficiente.
    - p >= alfa y media <= 0: no se detectó una mejora (no demuestra que no haya mejora).
    """
    if media != media or p != p:
        return Afirmaciones(False, False, NO_DETECTADA)
    significativa, relevante = p < alfa, media >= umbral - tolerancia
    if significativa:
        lectura = SE_SOSTIENE if relevante else BAJO_UMBRAL if media > tolerancia else INFERIOR
    else:
        lectura = FAVORABLE if media > tolerancia else NO_DETECTADA
    return Afirmaciones(significativa, relevante, lectura)


@dataclass(frozen=True)
class Comparacion:
    """Comparación pareada de dos sistemas sobre las mismas consultas."""

    n: int
    excluidas: list[str]
    media: float
    desviacion: float
    p_permutacion: float
    exacta: bool  # p exacta por enumeración (H2) o por B réplicas (H1 y exploratorias)
    m: int  # diferencias distintas de cero
    p_minima: float  # p mínima alcanzable (solo con la prueba exacta; nan en otro caso)
    error_mc: float  # error de Monte Carlo de la p (0 con la prueba exacta)
    replicas: int
    t: float
    p_t: float
    intervalo: tuple[float, float]
    afirmaciones: Afirmaciones
    decision: str  # lectura de las afirmaciones, o EXPLORATORIA si la compuerta lo impide

    @property
    def sostiene(self) -> bool:
        return self.decision == SE_SOSTIENE


def comparar(a: Mapping[str, float | None], b: Mapping[str, float | None], *, umbral: float, alfa: float,
             confianza: float, replicas_permutacion: int, replicas_bootstrap: int, semilla_permutacion: int,
             semilla_bootstrap: int, exacta: bool = False, tolerancia: float = TOLERANCIA_EMPATES) -> Comparacion:
    """Compara el sistema a con el b: diferencia media, contraste, comprobación, intervalo y afirmaciones."""
    d, excluidas = diferencias(a, b)
    x = sin_empates(d, tolerancia)
    media = float(x.mean()) if x.size else float("nan")
    m = int((x != 0).sum())
    if exacta:
        p, _ = permutacion_exacta(x, tolerancia) if x.size else (float("nan"), 0)
        minima, error, replicas = p_minima(m), 0.0, 2**m
        t, p_t = float("nan"), float("nan")  # con m <= 9 la aproximación t no es fiable (R35)
    else:
        p = permutacion_pareada(x, replicas_permutacion, semilla_permutacion, tolerancia)
        minima, error, replicas = float("nan"), error_monte_carlo(p, replicas_permutacion), replicas_permutacion
        t, p_t = t_pareada(x)
    afirmaciones = decidir(media, p, umbral, alfa, tolerancia)
    return Comparacion(
        n=len(d), excluidas=excluidas, media=media,
        desviacion=float(x.std(ddof=1)) if x.size > 1 else float("nan"),
        p_permutacion=p, exacta=exacta, m=m, p_minima=minima, error_mc=error, replicas=replicas, t=t, p_t=p_t,
        intervalo=intervalo_bootstrap(x, replicas_bootstrap, confianza, semilla_bootstrap),
        afirmaciones=afirmaciones, decision=afirmaciones.lectura,
    )


def compuerta(h1: Comparacion, h2: Comparacion) -> Comparacion:
    """Secuencia fija (R33): H2 conserva su lectura solo si H1 se sostiene; si no, es exploratoria.

    Las cifras de H2 (estimación, intervalo y p) no cambian: solo deja de tener veredicto."""
    return h2 if h1.sostiene else replace(h2, decision=EXPLORATORIA)


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
