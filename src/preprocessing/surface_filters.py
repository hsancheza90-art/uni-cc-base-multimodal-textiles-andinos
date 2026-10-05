from __future__ import annotations

import re
from typing import Any, Dict, List

from src.utils.texto import buscar_terminos, normalizar_texto, unir_textos

SURFACE_OBJECT_TERMS = [
    "mantle",
    "tunic",
    "shirt",
    "tabard",
    "dress",
    "miniature dress",
    "garment",
    "bag",
    "pouch",
    "panel",
    "cloth",
    "hanging",
    "poncho",
    "tapestry",
    "featherwork",
]

FRAGMENT_TERMS = [
    "textile fragment",
    "fragment",
    "fragments",
]

NARROW_OBJECT_TERMS = [
    "headband",
    "sash",
    "belt",
    "band",
    "strap",
    "cord",
    "ribbon",
    "strip",
    "strips",
    "sling",
    "sling shot",
    "tassel",
    "tassels",
    "ornamental tassels",
]

BORDER_TERMS = [
    "border",
    "border fragment",
]

HAT_TERMS = [
    "hat",
    "cap",
    "openweave cap",
    "four-cornered hat",
]

WARI_TERMS = [
    "wari",
    "huari",
]

# Tipo de objeto normalizado: (codigo, terminos). El orden es la prioridad y
# reproduce la de la curacion MET v2 (familia del objeto antes que "fragmento").
# "tapestry" va despues de bordes y bandas porque suele ser adjetivo de tecnica
# ("Tapestry Border Fragment").
TIPOS_OBJETO: list[tuple[str, list[str]]] = [
    ("borla_textil", ["tassel", "tassels"]),
    ("manto", ["mantle", "mantles", "manto"]),
    ("tunica", ["tunic", "tunics", "shirt", "tabard", "tunica"]),
    ("vestimenta_textil", ["dress", "garment"]),
    ("bolso_textil", ["bag", "bags", "pouch", "bolso", "bolsa"]),
    ("panel_textil", ["panel", "panels"]),
    ("tocado", ["headdress", "crown"]),
    ("mascara_textil", ["mask", "false face"]),
    ("borde_textil", ["border", "borders"]),
    ("honda_textil", ["sling", "sling shot"]),
    ("vincha_textil", ["headband", "vincha"]),
    ("faja", ["sash", "belt", "faja"]),
    ("banda", ["band", "bands", "strip", "strips", "banda"]),
    ("tapiz_textil", ["tapestry", "hanging", "tapiz"]),
    ("tela",["cloth", "fabric", "fabrics"]),
    ("fragmento_textil", ["fragment", "fragments", "fragmento"]),
    ("objeto_textil", ["textile", "textiles", "textil"]),
]


def normalize_text(value: Any) -> str:
    """Compatibilidad: ver src.utils.texto.normalizar_texto."""
    return normalizar_texto(value)


def contains_any(value: Any, terms: List[str]) -> List[str]:
    return buscar_terminos(value, terms)


def nucleo_titulo(titulo: Any) -> str:
    """Parte del titulo que nombra al objeto: "Tunic with Diamond Band" -> "tunic"."""
    return re.split(r"\b(?:with|depicting|showing)\b", normalizar_texto(titulo), maxsplit=1)[0]


def build_combined_text(row: Dict[str, Any]) -> str:
    return unir_textos(
        row.get("titulo_original"),
        row.get("titulo_es_sugerido"),
        row.get("nombre_objeto_original"),
        row.get("material_original"),
        row.get("clasificacion_original"),
        row.get("cultura"),
        row.get("periodo"),
        row.get("pais"),
        row.get("region"),
        row.get("subregion"),
        row.get("etiquetas_originales"),
    )


def build_object_text(row: Dict[str, Any]) -> str:
    """Texto que nombra al objeto, sin material ni contexto cultural."""
    return unir_textos(
        nucleo_titulo(row.get("titulo_original")),
        row.get("titulo_es_sugerido"),
        row.get("nombre_objeto_original"),
    )


def is_wari_related(row: Dict[str, Any]) -> bool:
    return bool(contains_any(build_combined_text(row), WARI_TERMS))


def classify_surface_type(row: Dict[str, Any]) -> Dict[str, Any]:
    """
    Clasifica si el textil es útil para la primera etapa de análisis iconográfico.

    Regla general:
    - Se priorizan objetos con superficie amplia o composición visible.
    - Se excluyen formatos estrechos o longitudinales.
    - Se conserva como excepción el sombrero Wari/Huari cuando muestra potencial iconográfico.

    Los formatos estrechos, bordes y sombreros se buscan solo en el texto que
    nombra al objeto, para que "Tunic with Diamond Band" no se tome por una banda.
    """
    objeto = build_object_text(row)
    narrow_hits = contains_any(objeto, NARROW_OBJECT_TERMS)
    border_hits = contains_any(objeto, BORDER_TERMS)
    hat_hits = contains_any(objeto, HAT_TERMS)
    surface_hits = contains_any(build_combined_text(row), SURFACE_OBJECT_TERMS)
    fragment_hits = contains_any(objeto, FRAGMENT_TERMS)
    wari_related = is_wari_related(row)

    # 1. Excepción: sombreros Wari/Huari con potencial iconográfico.
    if hat_hits and wari_related:
        return {
            "tipo_superficie": "objeto_tridimensional_iconografico",
            "corpus_analisis": "corpus_principal_iconografia_wari",
            "motivo_superficie": f"sombrero/cap Wari-Huari conservado por potencial iconográfico: {hat_hits}",
        }

    # 2. Excluir formatos estrechos o longitudinales.
    if narrow_hits:
        return {
            "tipo_superficie": "formato_estrecho",
            "corpus_analisis": "corpus_secundario_formato_estrecho",
            "motivo_superficie": f"formato estrecho o longitudinal detectado: {narrow_hits}",
        }

    # 3. Excluir bordes lineales en esta primera etapa.
    if border_hits:
        return {
            "tipo_superficie": "borde_o_fragmento_lineal",
            "corpus_analisis": "corpus_secundario_borde_lineal",
            "motivo_superficie": f"borde o fragmento lineal detectado: {border_hits}",
        }

    # 4. Hats/caps no Wari: textiles válidos, pero no prioritarios para la fase inicial.
    if hat_hits:
        return {
            "tipo_superficie": "objeto_tridimensional_no_prioritario",
            "corpus_analisis": "corpus_secundario_tridimensional",
            "motivo_superficie": f"sombrero/cap no Wari-Huari enviado a corpus secundario: {hat_hits}",
        }

    # 5. Objetos con superficie amplia o iconografía visible.
    if surface_hits:
        return {
            "tipo_superficie": "superficie_amplia",
            "corpus_analisis": "corpus_principal_superficie_amplia",
            "motivo_superficie": f"superficie amplia o composición visual útil detectada: {surface_hits}",
        }

    # 6. Fragmentos: no todos son útiles, quedan para revisión morfológica.
    if fragment_hits:
        return {
            "tipo_superficie": "fragmento_para_revision",
            "corpus_analisis": "revision_morfologica",
            "motivo_superficie": f"fragmento textil requiere revisión visual: {fragment_hits}",
        }

    return {
        "tipo_superficie": "revision_morfologica",
        "corpus_analisis": "revision_morfologica",
        "motivo_superficie": "no se detectó con claridad si el objeto tiene superficie amplia, formato estrecho o valor iconográfico prioritario",
    }


def normalize_object_type(row: Dict[str, Any]) -> str:
    objeto = build_object_text(row)

    if contains_any(objeto, HAT_TERMS):
        return "sombrero_wari_iconografico" if is_wari_related(row) else "sombrero_o_gorro"

    for codigo, terminos in TIPOS_OBJETO:
        if contains_any(objeto, terminos):
            return codigo

    return "tipo_no_determinado"
