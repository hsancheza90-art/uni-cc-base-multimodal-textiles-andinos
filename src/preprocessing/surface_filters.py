from __future__ import annotations

import re
import unicodedata
from typing import Any, Dict, List


SURFACE_OBJECT_TERMS = [
    "mantle",
    "tunic",
    "shirt",
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
    "sling",
    "sling shot",
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


def normalize_text(value: Any) -> str:
    if value is None:
        return ""

    text = str(value).lower().strip()
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    text = re.sub(r"\s+", " ", text)

    return text


def contains_any(value: Any, terms: List[str]) -> List[str]:
    text = normalize_text(value)
    hits = []

    for term in terms:
        term_norm = normalize_text(term)
        if term_norm in text:
            hits.append(term)

    return hits


def build_combined_text(row: Dict[str, Any]) -> str:
    fields = [
        row.get("titulo_original", ""),
        row.get("titulo_es_sugerido", ""),
        row.get("nombre_objeto_original", ""),
        row.get("material_original", ""),
        row.get("clasificacion_original", ""),
        row.get("cultura", ""),
        row.get("periodo", ""),
        row.get("pais", ""),
        row.get("region", ""),
        row.get("subregion", ""),
        row.get("etiquetas_originales", ""),
    ]

    return " ".join(str(field) for field in fields if field)


def is_wari_related(row: Dict[str, Any]) -> bool:
    combined = build_combined_text(row)
    return bool(contains_any(combined, WARI_TERMS))


def classify_surface_type(row: Dict[str, Any]) -> Dict[str, Any]:
    """
    Clasifica si el textil es útil para la primera etapa de análisis iconográfico.

    Regla general:
    - Se priorizan objetos con superficie amplia o composición visible.
    - Se excluyen formatos estrechos o longitudinales.
    - Se conserva como excepción el sombrero Wari/Huari cuando muestra potencial iconográfico.
    """
    combined = build_combined_text(row)

    narrow_hits = contains_any(combined, NARROW_OBJECT_TERMS)
    border_hits = contains_any(combined, BORDER_TERMS)
    surface_hits = contains_any(combined, SURFACE_OBJECT_TERMS)
    fragment_hits = contains_any(combined, FRAGMENT_TERMS)
    hat_hits = contains_any(combined, HAT_TERMS)
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
    text = normalize_text(build_combined_text(row))

    if ("hat" in text or "cap" in text) and ("wari" in text or "huari" in text):
        return "sombrero_wari_iconografico"
    if "hat" in text or "cap" in text:
        return "sombrero_o_gorro"
    if "mantle" in text or "manto" in text:
        return "manto"
    if "tunic" in text or "shirt" in text or "tunica" in text or "túnica" in text:
        return "tunica"
    if "dress" in text:
        return "vestimenta_textil"
    if "bag" in text or "pouch" in text or "bolso" in text:
        return "bolso_textil"
    if "panel" in text:
        return "panel_textil"
    if "tapestry" in text or "tapiz" in text:
        return "tapiz_textil"
    if "border" in text:
        return "borde_textil"
    if "sling" in text:
        return "honda_textil"
    if "headband" in text:
        return "vincha_textil"
    if "sash" in text or "belt" in text:
        return "faja"
    if "band" in text:
        return "banda"
    if "fragment" in text or "fragmento" in text:
        return "fragmento_textil"
    if "textile" in text or "textil" in text:
        return "objeto_textil"

    return "tipo_no_determinado"