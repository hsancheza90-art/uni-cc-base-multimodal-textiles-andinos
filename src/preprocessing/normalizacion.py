"""Normalizacion de material y tecnica a los codigos del vocabulario (Cuadro 6.5).

Las reglas leen el texto de la fuente (material, tecnica, clasificacion y titulo)
y devuelven codigos de config/vocabulario.toml separados por "; ", en el orden
del vocabulario (p. ej. "algodon; fibra_de_camelido").
"""

from __future__ import annotations

import re
from typing import Any

from src.utils.texto import buscar_terminos, unir_textos

# (codigo, terminos de la fuente), en el orden del vocabulario.
MATERIALES: list[tuple[str, list[str]]] = [
    ("algodon", ["cotton"]),
    ("fibra_de_camelido", ["camelid", "alpaca", "llama", "vicuna", "vicuña", "camelid wool", "alpaca wool"]),
    ("lana", ["wool"]),
    ("plumas", ["feather", "feathers", "featherwork", "feathered"]),
    ("seda", ["silk"]),
    ("metal", ["metal", "metallic", "gold", "silver", "copper"]),
    ("pelo_humano", ["human hair"]),
    ("fibra_vegetal", ["plant fiber", "plant fibre", "bast", "maguey", "agave", "reed"]),
    ("pigmento", ["pigment", "paint", "painted", "dye", "dyed"]),
]

# "wool" asociado a camelidos ("alpaca wool", "camelid wool") no se cuenta como lana de oveja.
LANA_DE_CAMELIDO = ["alpaca wool", "camelid wool", "llama wool", "vicuna wool"]

TECNICAS: list[tuple[str, list[str]]] = [
    (
        "tejido",
        [
            "woven", "weave", "weaving", "plain weave", "plain cloth", "tabby", "twill",
            "warp-faced", "weft-faced", "compound", "textiles-woven", "cloth",
        ],
    ),
    ("tapiz", ["tapestry", "tapestry-weave", "tapestry-woven", "interlocked"]),
    ("bordado", ["embroidered", "embroidery", "outline stitch", "stem stitch"]),
    ("trabajo_con_plumas", ["feather", "feathers", "featherwork", "feathered", "textiles-featherwork"]),
    ("brocado", ["brocade", "brocaded", "supplementary weft", "supplementary pattern weft"]),
    ("tela_doble", ["double cloth", "double-cloth", "triple cloth", "triple-cloth"]),
    ("pintado", ["painted", "paint", "textiles-painted"]),
]

# Tecnicas de tejido especificas que implican "tejido", como en la curacion MET v2 ("tapiz; tejido").
IMPLICAN_TEJIDO = {"tapiz", "brocado", "tela_doble"}


def _codigos(texto: str, reglas: list[tuple[str, list[str]]]) -> list[str]:
    return [codigo for codigo, terminos in reglas if buscar_terminos(texto, terminos)]


def normalizar_material(*textos: Any) -> str:
    texto = unir_textos(*textos)
    sin_lana_de_camelido = texto
    for frase in LANA_DE_CAMELIDO:
        sin_lana_de_camelido = sin_lana_de_camelido.replace(frase, " ")
    codigos = _codigos(texto, [regla for regla in MATERIALES if regla[0] != "lana"])
    if buscar_terminos(sin_lana_de_camelido, ["wool"]):
        codigos.append("lana")
    orden = [codigo for codigo, _ in MATERIALES]
    return "; ".join(sorted(codigos, key=orden.index))


def normalizar_tecnica(*textos: Any) -> str:
    # "Textiles-Non-Woven" contiene "woven" como palabra completa; no indica tejido.
    texto = re.sub(r"non[- ]?woven", " ", unir_textos(*textos))
    codigos = _codigos(texto, TECNICAS)
    if IMPLICAN_TEJIDO & set(codigos) and "tejido" not in codigos:
        codigos.append("tejido")
    orden = [codigo for codigo, _ in TECNICAS]
    return "; ".join(sorted(codigos, key=orden.index))
