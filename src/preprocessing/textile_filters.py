from __future__ import annotations

import re
import unicodedata
from typing import Any, Dict, List, Tuple


TEXTILE_STRONG_TERMS = [
    "textile",
    "textiles",
    "woven",
    "weaving",
    "cloth",
    "fabric",
    "tapestry",
    "embroidered",
    "embroidery",
    "needlework",
    "fiber",
    "fibre",
    "cotton",
    "wool",
    "camelid",
    "alpaca",
    "llama",
    "vicuña",
    "vicuna",
    "tunic",
    "mantle",
    "shirt",
    "poncho",
    "sash",
    "belt",
    "bag",
    "headband",
    "loincloth",
    "garment",
]

TEXTILE_WEAK_TERMS = [
    "fragment",
    "panel",
    "border",
    "band",
    "strip",
    "decorated band",
]

ANDEAN_CULTURAL_TERMS = [
    "andean",
    "andes",
    "peru",
    "peruvian",
    "inca",
    "paracas",
    "nasca",
    "nazca",
    "wari",
    "huari",
    "chancay",
    "moche",
    "mochica",
    "tiwanaku",
    "tiahuanaco",
    "tihuanaco",
    "chimú",
    "chimu",
]

NON_TEXTILE_CLASSIFICATION_TERMS = [
    "ceramics",
    "ceramic",
    "metalwork",
    "metal",
    "sculpture",
    "stone",
    "woodwork",
    "jewelry",
    "ornaments",
    "musical instruments",
    "tools and equipment",
    "glass",
    "bone",
    "shell",
]

NON_TEXTILE_MEDIUM_TERMS = [
    "ceramic",
    "pottery",
    "terracotta",
    "earthenware",
    "clay",
    "gold",
    "silver",
    "copper",
    "bronze",
    "metal",
    "alloy",
    "stone",
    "wood",
    "bone",
    "shell",
    "turquoise",
    "jade",
    "obsidian",
    "gourd",
]

NON_TEXTILE_TITLE_TERMS = [
    "vessel",
    "bottle",
    "jar",
    "bowl",
    "plate",
    "cup",
    "plaque",
    "ornament",
    "earflare",
    "ear flare",
    "mask",
    "figurine",
    "figure",
    "stirrup",
    "spout",
    "whistle",
    "flute",
    "knife",
    "spoon",
    "pin",
    "beaker",
    "kero",
]


def normalize_text(value: Any) -> str:
    """
    Normalize text for robust keyword matching.
    Converts to lowercase and removes accents.
    """
    if value is None:
        return ""

    text = str(value).lower().strip()
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    text = re.sub(r"\s+", " ", text)

    return text


def contains_any(text: str, terms: List[str]) -> List[str]:
    """
    Return terms found in text.
    """
    normalized = normalize_text(text)
    hits = []

    for term in terms:
        term_norm = normalize_text(term)
        if term_norm in normalized:
            hits.append(term)

    return hits


def get_tags_text(record: Dict[str, Any]) -> str:
    """
    Convert The Met tag list into a single searchable string.
    """
    tags = record.get("tags") or []

    if not isinstance(tags, list):
        return ""

    terms = []
    for tag in tags:
        if isinstance(tag, dict) and tag.get("term"):
            terms.append(str(tag.get("term")))

    return " ".join(terms)


def evaluate_met_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluate whether a The Met object is likely to be an Andean textile.

    The logic is intentionally transparent and rule-based. This is useful
    for academic traceability because each accepted or excluded record
    receives a score and a reason.
    """
    title = record.get("title", "")
    classification = record.get("classification", "")
    medium = record.get("medium", "")
    object_name = record.get("objectName", "")
    culture = record.get("culture", "")
    country = record.get("country", "")
    region = record.get("region", "")
    department = record.get("department", "")
    tags_text = get_tags_text(record)

    primary_image = record.get("primaryImage") or record.get("primaryImageSmall")

    score = 0
    reasons: List[str] = []
    textile_evidence_count = 0
    exclusion_evidence_count = 0

    # Strong textile evidence
    classification_hits = contains_any(classification, ["textile", "textiles"])
    if classification_hits:
        score += 5
        textile_evidence_count += 1
        reasons.append(f"clasificación contiene evidencia textil: {classification_hits}")

    object_name_hits = contains_any(object_name, TEXTILE_STRONG_TERMS)
    if object_name_hits:
        score += 4
        textile_evidence_count += 1
        reasons.append(f"nombre de objeto contiene términos textiles: {object_name_hits}")

    medium_hits = contains_any(medium, [
        "cotton",
        "wool",
        "camelid",
        "fiber",
        "fibre",
        "alpaca",
        "llama",
        "vicuña",
        "vicuna",
    ])
    if medium_hits:
        score += 4
        textile_evidence_count += 1
        reasons.append(f"material contiene fibras o soporte textil: {medium_hits}")

    title_strong_hits = contains_any(title, TEXTILE_STRONG_TERMS)
    if title_strong_hits:
        score += 3
        textile_evidence_count += 1
        reasons.append(f"título contiene términos textiles: {title_strong_hits}")

    tags_hits = contains_any(tags_text, TEXTILE_STRONG_TERMS)
    if tags_hits:
        score += 2
        textile_evidence_count += 1
        reasons.append(f"etiquetas contienen términos textiles: {tags_hits}")

    title_weak_hits = contains_any(title, TEXTILE_WEAK_TERMS)
    if title_weak_hits:
        score += 1
        reasons.append(f"título contiene términos débiles asociados a fragmentos o paneles: {title_weak_hits}")

    # Andean evidence: useful but not sufficient alone
    cultural_text = " ".join([culture, country, region, department, title, medium])
    cultural_hits = contains_any(cultural_text, ANDEAN_CULTURAL_TERMS)
    if cultural_hits:
        score += 1
        reasons.append(f"evidencia cultural/geográfica andina: {cultural_hits}")

    # Non-textile evidence
    non_textile_class_hits = contains_any(classification, NON_TEXTILE_CLASSIFICATION_TERMS)
    if non_textile_class_hits:
        score -= 5
        exclusion_evidence_count += 1
        reasons.append(f"clasificación sugiere objeto no textil: {non_textile_class_hits}")

    non_textile_medium_hits = contains_any(medium, NON_TEXTILE_MEDIUM_TERMS)
    if non_textile_medium_hits:
        score -= 4
        exclusion_evidence_count += 1
        reasons.append(f"material sugiere objeto no textil: {non_textile_medium_hits}")

    non_textile_title_hits = contains_any(title, NON_TEXTILE_TITLE_TERMS)
    if non_textile_title_hits:
        score -= 4
        exclusion_evidence_count += 1
        reasons.append(f"título sugiere objeto no textil: {non_textile_title_hits}")

    non_textile_object_hits = contains_any(object_name, NON_TEXTILE_TITLE_TERMS)
    if non_textile_object_hits:
        score -= 4
        exclusion_evidence_count += 1
        reasons.append(f"nombre de objeto sugiere objeto no textil: {non_textile_object_hits}")

    # Curation status
    if not primary_image:
        estado = "excluido_sin_imagen"
    elif exclusion_evidence_count >= 1 and textile_evidence_count == 0:
        estado = "excluido_no_textil"
    elif score >= 6 and textile_evidence_count >= 2:
        estado = "aceptado_textil"
    elif score >= 4 and textile_evidence_count >= 1:
        estado = "revision_manual"
    else:
        estado = "excluido_no_textil"

    if not reasons:
        reasons.append("sin evidencia suficiente para clasificar como textil andino")

    return {
        "puntaje_textil": score,
        "estado_curacion": estado,
        "motivo_curacion": " | ".join(reasons),
        "conteo_evidencia_textil": textile_evidence_count,
        "conteo_evidencia_exclusion": exclusion_evidence_count,
    }