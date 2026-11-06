"""M3: descriptor estructural desde la anotación v2 y su disimilitud mixta (docs/especificacion_m3.md).

Funciones puras (solo la biblioteca estándar): el descriptor de una pieza se arma con su fila de
data/metadata/anotaciones_v2.csv (códigos ya validados contra el vocabulario) y dos piezas se
comparan bloque a bloque, con una máscara de observabilidad:

    D(i, j) = Σ_b λ_b m_ib m_jb d_b(i, j) / Σ_b λ_b m_ib m_jb,

con λ_b los pesos de [m3.pesos] en config/modelos.toml, m_ib = 1 si el bloque b se observó en la
pieza i y d_b en [0, 1]. Si ningún bloque es observable en las dos, D no existe: el par queda «sin
evidencia estructural» (None), nunca con similitud máxima. La cobertura es Σ λ m m / Σ λ.

Los estados no_observable y desconocido (y no_visible en borde y centro) apagan el bloque;
ausente es una observación y se compara como un valor. M3-sin-orden (control del mecanismo)
reemplaza la palabra de bandas por el histograma de sus tipos y no usa adyacencias.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Any

SIN_OBSERVACION = {"", "no_observable", "desconocido", "no_visible"}
LAGUNA = "laguna"
ORDEN_REPETICION = ["no", "parcial", "si"]
SEPARADOR_SECUENCIA = " > "
SEPARADOR_MULTIPLE = "; "


# --------------------------------------------------------------------------- palabras de bandas


def reverso(palabra: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(reversed(palabra))


def canonizar(palabra: tuple[str, ...], alfabeto: list[str]) -> tuple[str, ...]:
    """Mínimo lexicográfico de {w, rev(w)} con el orden del alfabeto: c(rev(w)) = c(w)."""
    rango = {simbolo: i for i, simbolo in enumerate(alfabeto)}
    clave = lambda w: [rango.get(s, len(alfabeto)) for s in w]  # noqa: E731
    return min(palabra, reverso(palabra), key=clave)


def tramos(palabra: tuple[str, ...]) -> list[tuple[str, ...]]:
    """Tramos observados de la palabra: las lagunas la cortan y no son un símbolo."""
    salida, actual = [], []
    for simbolo in palabra:
        if simbolo == LAGUNA:
            if actual:
                salida.append(tuple(actual))
            actual = []
        else:
            actual.append(simbolo)
    if actual:
        salida.append(tuple(actual))
    return salida


def sin_lagunas(palabra: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(s for s in palabra if s != LAGUNA)


def histograma(conteo: Counter) -> dict[Any, float]:
    total = sum(conteo.values())
    return {clave: n / total for clave, n in conteo.items()} if total else {}


def histograma_tipos(palabra: tuple[str, ...]) -> dict[str, float]:
    """Proporción de cada tipo de banda, sin orden (control de M3-sin-orden)."""
    return histograma(Counter(sin_lagunas(palabra)))


def histograma_adyacencias(palabra: tuple[str, ...]) -> dict[tuple[str, str], float]:
    """Proporción de cada par no dirigido de bandas contiguas, dentro de cada tramo observado.

    El par no dirigido hace al histograma invariante a la reversión sin elegir un sentido."""
    pares = Counter(tuple(sorted(par)) for tramo in tramos(palabra) for par in zip(tramo, tramo[1:]))
    return histograma(pares)


def distancia_l1_media(a: dict, b: dict) -> float:
    """Mitad de la distancia L1 entre dos histogramas normalizados: en [0, 1]."""
    return 0.5 * sum(abs(a.get(k, 0.0) - b.get(k, 0.0)) for k in set(a) | set(b))


def distancia_edicion(a: tuple[str, ...], b: tuple[str, ...]) -> int:
    previa = list(range(len(b) + 1))
    for i, x in enumerate(a, start=1):
        actual = [i]
        for j, y in enumerate(b, start=1):
            actual.append(min(previa[j] + 1, actual[j - 1] + 1, previa[j - 1] + (x != y)))
        previa = actual
    return previa[-1]


def distancia_palabras(a: tuple[str, ...], b: tuple[str, ...]) -> float:
    """Edición normalizada en la órbita de la reversión: min(d(a, b), d(a, rev b)) / max(|a|, |b|).

    Las lagunas se quitan antes de comparar (enmascaradas). Dos palabras vacías (sin bandas) son
    iguales; una vacía y otra no están a distancia 1."""
    a, b = sin_lagunas(a), sin_lagunas(b)
    largo = max(len(a), len(b))
    if largo == 0:
        return 0.0
    return min(distancia_edicion(a, b), distancia_edicion(a, reverso(b))) / largo


def periodo(palabra: tuple[str, ...]) -> int:
    """p*(w) = mínimo p en 1..l con w_j = w_{j+p} para todo j <= l - p. p* = l no es repetición."""
    largo = len(palabra)
    for p in range(1, largo + 1):
        if all(palabra[j] == palabra[j + p] for j in range(largo - p)):
            return p
    return largo


# --------------------------------------------------------------------------- descriptor


@dataclass(frozen=True)
class Descriptor:
    """Bloques del descriptor de una pieza; None marca un bloque no observable."""

    composicion: str | None = None
    bandas: tuple[str, ...] | None = None  # () si la pieza no tiene bandas (ausente)
    borde: str | None = None
    centro: str | None = None
    simetria: str | None = None
    repeticion: str | None = None
    motivos: frozenset[str] | None = None  # frozenset() si los motivos están ausentes
    familia_iconografica: str | None = None
    extra: dict[str, Any] = field(default_factory=dict, compare=False)


def valor(texto: str) -> str | None:
    return None if texto in SIN_OBSERVACION else texto


def palabra_de_bandas(secuencia: str) -> tuple[str, ...] | None:
    if secuencia in SIN_OBSERVACION:
        return None
    if secuencia == "ausente":
        return ()
    return tuple(s.strip() for s in secuencia.split(">") if s.strip())


def descriptor(fila: dict[str, str]) -> Descriptor:
    """Descriptor de una fila de anotaciones_v2.csv (códigos del vocabulario, estados en la celda)."""
    motivos = fila.get("motivos", "")
    return Descriptor(
        composicion=valor(fila.get("composicion", "")),
        bandas=palabra_de_bandas(fila.get("secuencia_bandas", "")),
        borde=valor(fila.get("borde", "")),
        centro=valor(fila.get("centro", "")),
        simetria=valor(fila.get("simetria", "")),
        repeticion=valor(fila.get("repeticion", "")),
        motivos=None if motivos in SIN_OBSERVACION else frozenset() if motivos == "ausente" else frozenset(
            m.strip() for m in motivos.split(";") if m.strip()),
        familia_iconografica=valor(fila.get("familia_iconografica", "")),
    )


# --------------------------------------------------------------------------- disimilitud


def nominal(a: str, b: str) -> float:
    return 0.0 if a == b else 1.0


def distancias_por_bloque(i: Descriptor, j: Descriptor, sin_orden: bool = False) -> dict[str, float]:
    """d_b(i, j) de cada bloque observable en las dos piezas (los demás no aparecen)."""
    d: dict[str, float] = {}
    for bloque in ("composicion", "borde", "centro", "simetria", "familia_iconografica"):
        a, b = getattr(i, bloque), getattr(j, bloque)
        if a is not None and b is not None:
            d[bloque] = nominal(a, b)
    if i.repeticion in ORDEN_REPETICION and j.repeticion in ORDEN_REPETICION:
        d["repeticion"] = abs(ORDEN_REPETICION.index(i.repeticion) - ORDEN_REPETICION.index(j.repeticion)) / 2
    if i.motivos is not None and j.motivos is not None:
        union = i.motivos | j.motivos
        d["motivos"] = 1 - len(i.motivos & j.motivos) / len(union) if union else 0.0
    if i.bandas is not None and j.bandas is not None:
        if sin_orden:
            ti, tj = histograma_tipos(i.bandas), histograma_tipos(j.bandas)
            d["bandas"] = distancia_l1_media(ti, tj) if ti and tj else float(bool(ti) != bool(tj))
        else:
            d["bandas"] = distancia_palabras(i.bandas, j.bandas)
            ai, aj = histograma_adyacencias(i.bandas), histograma_adyacencias(j.bandas)
            if ai and aj:  # sin un par contiguo en alguna, el bloque no es observable
                d["adyacencias"] = distancia_l1_media(ai, aj)
    return d


@dataclass(frozen=True)
class Comparacion:
    disimilitud: float | None  # None: sin evidencia estructural
    cobertura: float
    contribuciones: dict[str, float]  # λ_b d_b / Σ λ m m por bloque: su suma es D


def comparar(i: Descriptor, j: Descriptor, pesos: dict[str, float], sin_orden: bool = False) -> Comparacion:
    d = distancias_por_bloque(i, j, sin_orden)
    usados = {b: float(pesos[b]) for b in d if float(pesos.get(b, 0.0)) > 0}
    total = sum(float(p) for b, p in pesos.items() if not (sin_orden and b == "adyacencias"))
    denominador = sum(usados.values())
    if denominador == 0:
        return Comparacion(None, 0.0, {})
    contribuciones = {b: usados[b] * d[b] / denominador for b in usados}
    return Comparacion(sum(contribuciones.values()), denominador / total if total else 0.0, contribuciones)
