"""Normalizacion de material y tecnica a los valores controlados del Cuadro 6.5.

Las reglas leen el texto de la fuente (material, tecnica, clasificacion y titulo)
y devuelven valores en espanol, ordenados y separados por "; ", con el mismo
formato que la curacion MET v2 (p. ej. "algodón; fibra de camélido").
"""

from __future__ import annotations

import re
from typing import Any

from src.utils.texto import buscar_terminos, unir_textos

# (valor normalizado, terminos de la fuente)
MATERIALES: list[tuple[str, list[str]]] = [
    ("algodón", ["cotton"]),
    ("fibra de camélido", ["camelid", "alpaca", "llama", "vicuna", "vicuña", "camelid wool", "alpaca wool"]),
    ("plumas",["feather", "feathers", "featherwork", "feathered"]),
    ("seda", ["silk"]),
    ("metal", ["metal", "metallic", "gold", "silver", "copper"]),
    ("pelo humano", ["human hair"]),
    ("fibra vegetal", ["plant fiber", "plant fibre", "bast", "maguey", "agave", "reed"]),
    ("pigmento", ["pigment", "paint", "painted", "dye", "dyed"]),
]

# "wool" asociado a camelidos ("alpaca wool", "camelid wool") no se cuenta como lana de oveja.
LANA_DE_CAMELIDO = ["alpaca wool", "camelid wool", "llama wool", "vicuna wool"]

TECNICAS: list[tuple[str, list[str]]] = [
    ("tapiz", ["tapestry", "tapestry-weave", "tapestry-woven", "interlocked"]),
    ("bordado", ["embroidered", "embroidery", "outline stitch", "stem stitch"]),
    ("brocado", ["brocade", "brocaded", "supplementary weft", "supplementary pattern weft"]),
    ("tela doble", ["double cloth", "double-cloth", "triple cloth", "triple-cloth"]),
    ("pintado", ["painted", "paint", "textiles-painted"]),
    ("trabajo con plumas", ["feather", "feathers", "featherwork", "feathered", "textiles-featherwork"]),
    (
        "tejido",
        [
            "woven", "weave", "weaving", "plain weave", "plain cloth", "tabby", "twill",
            "warp-faced", "weft-faced", "compound", "textiles-woven", "cloth",
        ],
    ),
]


def _normalizar(texto: str, reglas: list[tuple[str, list[str]]]) -> list[str]:
    return [valor for valor, terminos in reglas if buscar_terminos(texto, terminos)]


def normalizar_material(*textos: Any) -> str:
    texto = unir_textos(*textos)
    valores = _normalizar(texto, MATERIALES)
    sin_lana_de_camelido = texto
    for frase in LANA_DE_CAMELIDO:
        sin_lana_de_camelido = sin_lana_de_camelido.replace(frase, " ")
    if buscar_terminos(sin_lana_de_camelido, ["wool"]):
        valores.append("lana")
    return "; ".join(sorted(valores))


def normalizar_tecnica(*textos: Any) -> str:
    # "Textiles-Non-Woven" contiene "woven" como palabra completa; no indica tejido.
    texto = re.sub(r"non[- ]?woven", " ", unir_textos(*textos))
    valores = _normalizar(texto, TECNICAS)
    # Las tecnicas de tejido especificas implican tejido, como en la curacion MET v2 ("tapiz; tejido").
    if {"tapiz", "brocado", "tela doble"} & set(valores) and "tejido" not in valores:
        valores.append("tejido")
    return "; ".join(sorted(valores))
