"""Atributos estructurados a partir del motivo libre que escribe el revisor.

El revisor describe cada decision con frases como «Textil completo con colores y
formas visibles. La mejor imagen para el proyecto» o «Textil incompleto sin
colores ni formas visibles». Este modulo las convierte en atributos:

- completitud: completo, incompleto o vacio (no se menciona);
- colores: si, parcial, no o vacio;
- formas: si, parcial, no o vacio (formas, figuras, motivos o iconografia);
- referencia: True si el revisor la marca como la mejor imagen para el estudio o si la
  describe como textil completo con colores y formas visibles (criterio del 2026-10-19:
  un textil completo, verificable en la fotografia, es la mejor imagen para el estudio);
  referencia_marcada distingue la marca explicita;
- pertinencia: motivo de descarte ajeno a la imagen (herramienta, plumaria...);
- monocroma: True si menciona fotografia o textil monocromo.

Tolera las variantes de escritura observadas (compelto, incompelto, mayusculas,
tildes). Es independiente de la fuente: sirve igual para AIC, MET, CMA u otras.
"""

from __future__ import annotations

import re

from src.utils.texto import sin_tildes

ATRIBUTOS_VISUALES = {
    "colores": "colores", "color": "colores",
    "formas": "formas", "forma": "formas", "figuras": "formas", "figura": "formas",
    "iconografia": "formas", "motivos": "formas",
}

# Expresion -> codigo de pertinencia (motivos de descarte que no dependen de la imagen).
PERTINENCIA = [
    (r"herramienta", "herramienta_textil"),
    (r"pluma", "plumaria"),
    (r"muneco", "muneco"),
    (r"posterior_inca|reciente|posterior a la epoca inca|moderna|de 1900", "posterior_inca"),
    (r"no es textil andino", "no_andino"),
    (r"\bno es textil\b", "no_textil"),
    (r"multiples textiles", "multiples_piezas"),
    (r"resolucion_insuficiente", "resolucion_insuficiente"),
]

ETIQUETAS = {
    "completitud": {"completo": "textil completo", "incompleto": "textil incompleto"},
    "colores": {"si": "colores visibles", "parcial": "colores parcialmente visibles", "no": "sin colores visibles"},
    "formas": {"si": "formas visibles", "parcial": "formas parcialmente visibles", "no": "sin formas visibles"},
    "pertinencia": {
        "herramienta_textil": "herramienta textil", "plumaria": "textil con plumaria (fuera del estudio)",
        "muneco": "muñeco", "posterior_inca": "posterior a 1532 (fuera del periodo de estudio)",
        "no_andino": "no es textil andino", "no_textil": "no es textil",
        "multiples_piezas": "varias piezas en la imagen", "resolucion_insuficiente": "resolución insuficiente",
    },
}


def analizar_motivo(motivo: str | None) -> dict:
    """Atributos del motivo libre del revisor."""
    texto = sin_tildes((motivo or "").lower()).replace("compelto", "completo").replace("incompelto", "incompleto")
    salida: dict = {"completitud": "", "colores": "", "formas": "", "referencia_marcada": "mejor imagen" in texto,
                    "pertinencia": "", "monocroma": "monocrom" in texto}
    if re.search(r"\bincompleto\b", texto):
        salida["completitud"] = "incompleto"
    elif re.search(r"\bcomplet[oa]\b", texto):
        salida["completitud"] = "completo"

    # «con» abre un grupo afirmativo; «sin», «no» y «ni», uno negativo. «poco» y
    # «parcialmente» rebajan a parcial los atributos afirmados del grupo en curso.
    polaridad, grupo = None, []
    for palabra in re.findall(r"[a-z_]+", texto):
        if palabra == "con":
            polaridad, grupo = "si", []
        elif palabra in ("sin", "no"):
            polaridad, grupo = "no", []
        elif palabra == "ni":
            polaridad = "no"
        elif palabra in ATRIBUTOS_VISUALES:
            salida[ATRIBUTOS_VISUALES[palabra]] = polaridad or "si"
            grupo.append(ATRIBUTOS_VISUALES[palabra])
        elif palabra in ("poco", "parcialmente"):
            for atributo in grupo:
                if salida[atributo] == "si":
                    salida[atributo] = "parcial"
    if "monocromatico" in texto and not salida["colores"]:
        salida["colores"] = "no"

    salida["referencia"] = salida["referencia_marcada"] or (
        salida["completitud"] == "completo" and salida["colores"] == "si" and salida["formas"] == "si")

    for patron, codigo in PERTINENCIA:
        if re.search(patron, texto):
            salida["pertinencia"] = codigo
            break
    return salida


def describir_motivo(atributos: dict) -> str:
    """Texto normalizado del motivo del revisor (sin errores de escritura ni variantes)."""
    partes = [ETIQUETAS[campo][atributos[campo]] for campo in ("completitud", "colores", "formas") if atributos[campo]]
    if atributos["monocroma"]:
        partes.append("fotografía monocroma")
    if atributos["pertinencia"]:
        partes.append(ETIQUETAS["pertinencia"][atributos["pertinencia"]])
    if atributos["referencia_marcada"]:
        partes.append("imagen de referencia para el estudio")
    texto = "; ".join(partes)
    return texto[:1].upper() + texto[1:] if texto else ""
