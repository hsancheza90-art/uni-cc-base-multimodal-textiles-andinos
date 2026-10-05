"""Pruebas de coincidencia de terminos, filtros textiles y normalizacion."""

from __future__ import annotations

import pytest

from src.preprocessing.normalizacion import normalizar_material, normalizar_tecnica
from src.preprocessing.surface_filters import classify_surface_type, normalize_object_type
from src.preprocessing.textile_filters import evaluate_met_record
from src.utils.texto import buscar_terminos, normalizar_texto

# --------------------------------------------------------------------------- texto


@pytest.mark.parametrize(
    ("texto", "terminos", "esperado"),
    [
        ("Capelet for a statuette", ["cap"], []),
        ("Tupac Capac tunic", ["cap"], []),
        ("that hat", ["hat"], ["hat"]),
        ("Lincoln Center", ["inca"], []),
        ("Inca tunic", ["inca"], ["inca"]),
        ("Peru, South Coast", ["south coast"], ["south coast"]),
        ("Vicuña fiber", ["vicuna"], ["vicuna"]),
        ("Textiles-Woven", ["textiles", "woven"], ["textiles", "woven"]),
        (None, ["cap"], []),
        (float("nan"), ["cap"], []),
    ],
)
def test_buscar_terminos_por_palabra_completa(texto, terminos, esperado) -> None:
    assert buscar_terminos(texto, terminos) == esperado


def test_normalizar_texto() -> None:
    assert normalizar_texto("  Túnica   CHIMÚ ") == "tunica chimu"
    assert normalizar_texto(None) == ""


# --------------------------------------------------------------------------- filtro textil


def registro(**campos):
    base = {"title": "", "classification": "", "medium": "", "objectName": "", "culture": "Peru", "primaryImage": "x"}
    return {**base, **campos}


def test_filtro_tolera_valores_nulos() -> None:
    resultado = evaluate_met_record(registro(title=None, culture=None, medium=None, classification="Textiles"))
    assert resultado["estado_curacion"] in {"aceptado_textil", "revision_manual", "excluido_no_textil"}


def test_figura_textil_de_camelido_no_se_excluye() -> None:
    resultado = evaluate_met_record(
        registro(title="Border Fragment, Figure", classification="Textiles-Sculpture", medium="Camelid hair")
    )
    assert resultado["estado_curacion"] != "excluido_no_textil"


def test_hilo_metalico_no_penaliza_un_textil() -> None:
    resultado = evaluate_met_record(
        registro(title="Miniature tabard", classification="Textiles-Woven", medium="Cotton, camelid hair, silk, metal")
    )
    assert resultado["estado_curacion"] == "aceptado_textil"
    assert "material sugiere objeto no textil" not in resultado["motivo_curacion"]


@pytest.mark.parametrize(
    ("campos", "estado"),
    [
        ({"title": "Stirrup Spout Bottle", "classification": "Ceramics", "medium": "Ceramic"}, "excluido_no_textil"),
        ({"title": "Spindle", "classification": "Textiles-Implements", "medium": "Wood"}, "excluido_no_textil"),
        ({"title": "Tunic", "classification": "Textiles-Woven", "medium": "Camelid hair", "objectName": "Tunic"}, "aceptado_textil"),
    ],
)
def test_filtro_textil_casos_basicos(campos, estado) -> None:
    assert evaluate_met_record(registro(**campos))["estado_curacion"] == estado


# --------------------------------------------------------------------------- superficie y tipo de objeto


@pytest.mark.parametrize(
    ("fila", "tipo_superficie"),
    [
        ({"titulo_original": "Tunic with Diamond Band", "nombre_objeto_original": "Tunic"}, "superficie_amplia"),
        ({"titulo_original": "Bag Tassel", "nombre_objeto_original": "Tassel"}, "formato_estrecho"),
        ({"titulo_original": "Band Fragment", "nombre_objeto_original": "Band fragment"}, "formato_estrecho"),
        ({"titulo_original": "Four-Cornered Hat", "nombre_objeto_original": "Hat", "cultura": "Wari"}, "objeto_tridimensional_iconografico"),
        ({"titulo_original": "Capelet for a statuette", "nombre_objeto_original": "Capelet"}, "revision_morfologica"),
    ],
)
def test_tipo_superficie(fila, tipo_superficie) -> None:
    assert classify_surface_type(fila)["tipo_superficie"] == tipo_superficie


@pytest.mark.parametrize(
    ("fila", "tipo"),
    [
        ({"titulo_original": "Tunic with Diamond Band"}, "tunica"),
        ({"titulo_original": "Bag Tassel"}, "borla_textil"),
        ({"titulo_original": "Tapestry Border Fragment with Tab Fringes"}, "borde_textil"),
        ({"titulo_original": "Tapestry Panel"}, "panel_textil"),
        ({"titulo_original": "Embroidered Mantle Fragment"}, "manto"),
        ({"titulo_original": 'Mummy Bundle "Mask"'}, "mascara_textil"),
        ({"titulo_original": "Four-Cornered Hat", "cultura": "Peru, Wari"}, "sombrero_wari_iconografico"),
        ({"titulo_original": "Capelet for a statuette"}, "tipo_no_determinado"),
        ({"titulo_original": "Fragment", "titulo_es_sugerido": "Faja textil"}, "faja"),
        ({"titulo_original": "Inka Khipu (Fiber Recording Device)"}, "tipo_no_determinado"),
    ],
)
def test_tipo_objeto(fila, tipo) -> None:
    assert normalize_object_type(fila) == tipo


# --------------------------------------------------------------------------- material y tecnica


@pytest.mark.parametrize(
    ("textos", "esperado"),
    [
        (("Camelid hair, cotton",), "algodon; fibra_de_camelido"),
        (("alpaca wool",), "fibra_de_camelido"),
        (("cotton and wool, tapestry weave",), "algodon; lana"),
        (("Cotton, camelid hair, silk, metal",), "algodon; fibra_de_camelido; seda; metal"),
        (("Feathers on cotton, camelid hair",), "algodon; fibra_de_camelido; plumas"),
        (("Cotton, paint",), "algodon; pigmento"),
        (("",), ""),
    ],
)
def test_normalizar_material(textos, esperado) -> None:
    assert normalizar_material(*textos) == esperado


@pytest.mark.parametrize(
    ("textos", "esperado"),
    [
        (("Textiles-Non-Woven",), ""),
        (("Textiles-Woven",), "tejido"),
        (("single-interlocked tapestry; cotton warp",), "tejido; tapiz"),
        (("camelid fiber; double-cloth with structural embroidery",), "tejido; bordado; tela_doble"),
        (("tabby, brocaded; cotton and wool",), "tejido; brocado"),
        (("Textiles-Featherwork", "feathered panel"), "trabajo_con_plumas"),
        (("plain warp-faced cloth, painted: cotton",), "tejido; pintado"),
    ],
)
def test_normalizar_tecnica(textos, esperado) -> None:
    assert normalizar_tecnica(*textos) == esperado
