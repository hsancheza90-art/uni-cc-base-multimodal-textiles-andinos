from __future__ import annotations

import re
import unicodedata
from typing import Any, Dict, List


SURFACE_OBJECT_TERMS = [
    "mantle",
    "tunic",
    "shirt",
    "garment",
    "bag",
    "pouch",
    "panel",
    "textile fragment",
    "fragment",
    "cloth",
    "hanging",
    "poncho",
    "tapestry",
]

NARROW_OBJECT_TERMS = [
    "sash",
    "belt",
    "band",
    "headband",
    "strap",
    "cord",
    "ribbon",
    "border",
    "strip",
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


def classify_surface_type(row: Dict[str, Any]) -> Dict[str, Any]:
    title = row.get("titulo_original", "")
    title_es = row.get("titulo_es_sugerido", "")
    object_name = row.get("nombre_objeto_original", "")
    material = row.get("material_original", "")
    classification = row.get("clasificacion_original", "")

    combined = " ".join([
        str(title),
        str(title_es),
        str(object_name),
        str(material),
        str(classification),
    ])

    narrow_hits = contains_any(combined, NARROW_OBJECT_TERMS)
    surface_hits = contains_any(combined, SURFACE_OBJECT_TERMS)

    if narrow_hits:
        return {
            "tipo_superficie": "formato_estrecho",
            "corpus_analisis": "corpus_secundario_formato_estrecho",
            "motivo_superficie": f"formato estrecho detectado: {narrow_hits}",
        }

    if surface_hits:
        return {
            "tipo_superficie": "superficie_amplia",
            "corpus_analisis": "corpus_principal_superficie_amplia",
            "motivo_superficie": f"superficie amplia o plana detectada: {surface_hits}",
        }

    return {
        "tipo_superficie": "revision_morfologica",
        "corpus_analisis": "revision_morfologica",
        "motivo_superficie": "no se detectó con claridad si el objeto tiene superficie amplia o formato estrecho",
    }


def normalize_object_type(row: Dict[str, Any]) -> str:
    text = normalize_text(" ".join([
        str(row.get("titulo_original", "")),
        str(row.get("titulo_es_sugerido", "")),
        str(row.get("nombre_objeto_original", "")),
    ]))

    if "mantle" in text or "manto" in text:
        return "manto"
    if "tunic" in text or "shirt" in text or "tunica" in text or "túnica" in text:
        return "tunica"
    if "bag" in text or "pouch" in text or "bolso" in text:
        return "bolso_textil"
    if "panel" in text:
        return "panel_textil"
    if "fragment" in text or "fragmento" in text:
        return "fragmento_textil"
    if "tapestry" in text or "tapiz" in text:
        return "tapiz_textil"
    if "sash" in text or "belt" in text:
        return "faja"
    if "band" in text or "headband" in text:
        return "banda"
    if "textile" in text or "textil" in text:
        return "objeto_textil"

    return "tipo_no_determinado"