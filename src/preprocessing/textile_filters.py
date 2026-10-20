"""Filtro textil andino por metadatos: decide si un registro es un textil andino analizable.

evaluate_met_record suma evidencias (clasificacion, nombre del objeto, materiales,
titulo, etiquetas y terminos culturales andinos), resta las de objetos no textiles y
herramientas de hilado o tejido, y devuelve la decision, el puntaje y el motivo. Lo
usan los colectores y la auditoria del filtro (src/metadata/auditar_filtros.py). Los
nombres en ingles se conservan porque figuran en los informes versionados de la serie v1.
"""

from __future__ import annotations

from typing import Any

from src.utils.texto import buscar_terminos

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
    "tabard",
    "featherwork",
]

TEXTILE_FIBER_TERMS = [
    "cotton",
    "wool",
    "camelid",
    "fiber",
    "fibre",
    "alpaca",
    "llama",
    "vicuña",
    "vicuna",
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

# Herramientas de hilado y tejido: se catalogan como "textile working equipment",
# pero no son superficies textiles y se excluyen siempre (como en la curacion CMA).
TEXTILE_TOOL_TERMS = [
    "spindle",
    "spindles",
    "whorl",
    "whorls",
    "textile working equipment",
    "weaving comb",
    "weaving combs",
    "weaving sword",
    "loom",
    "shed stick",
    "shed sticks",
    "bone pick",
    "bobbin",
    "work basket",
    "workbasket",
    "textiles-implements",
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


def get_tags_text(record: dict[str, Any]) -> str:
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


def evaluate_met_record(record: dict[str, Any]) -> dict[str, Any]:
    """
    Evaluate whether a The Met object is likely to be an Andean textile.

    The logic is intentionally transparent and rule-based. This is useful
    for academic traceability because each accepted or excluded record
    receives a score and a reason.
    """
    title = record.get("title") or ""
    classification = record.get("classification") or ""
    medium = record.get("medium") or ""
    object_name = record.get("objectName") or ""
    culture = record.get("culture") or ""
    country = record.get("country") or ""
    region = record.get("region") or ""
    department = record.get("department") or ""
    tags_text = get_tags_text(record)

    primary_image = record.get("primaryImage") or record.get("primaryImageSmall")

    score = 0
    reasons: list[str] = []
    textile_evidence_count = 0
    exclusion_evidence_count = 0

    # Strong textile evidence
    classification_hits = buscar_terminos(classification, ["textile", "textiles"])
    if classification_hits:
        score += 5
        textile_evidence_count += 1
        reasons.append(f"clasificación contiene evidencia textil: {classification_hits}")

    object_name_hits = buscar_terminos(object_name, TEXTILE_STRONG_TERMS)
    if object_name_hits:
        score += 4
        textile_evidence_count += 1
        reasons.append(f"nombre de objeto contiene términos textiles: {object_name_hits}")

    medium_hits = buscar_terminos(medium, TEXTILE_FIBER_TERMS)
    if medium_hits:
        score += 4
        textile_evidence_count += 1
        reasons.append(f"material contiene fibras o soporte textil: {medium_hits}")

    title_strong_hits = buscar_terminos(title, TEXTILE_STRONG_TERMS)
    if title_strong_hits:
        score += 3
        textile_evidence_count += 1
        reasons.append(f"título contiene términos textiles: {title_strong_hits}")

    tags_hits = buscar_terminos(tags_text, TEXTILE_STRONG_TERMS)
    if tags_hits:
        score += 2
        textile_evidence_count += 1
        reasons.append(f"etiquetas contienen términos textiles: {tags_hits}")

    title_weak_hits = buscar_terminos(title, TEXTILE_WEAK_TERMS)
    if title_weak_hits:
        score += 1
        reasons.append(f"título contiene términos débiles asociados a fragmentos o paneles: {title_weak_hits}")

    # Andean evidence: useful but not sufficient alone
    cultural_text = " ".join([culture, country, region, department, title, medium])
    cultural_hits = buscar_terminos(cultural_text, ANDEAN_CULTURAL_TERMS)
    if cultural_hits:
        score += 1
        reasons.append(f"evidencia cultural/geográfica andina: {cultural_hits}")

    # Non-textile evidence. Una clasificacion o un material con evidencia textil
    # explicita (p. ej. "Textiles-Sculpture" o "Cotton, silk, metal") no se penaliza:
    # describe un textil con componentes o motivos no textiles.
    non_textile_class_hits = buscar_terminos(classification, NON_TEXTILE_CLASSIFICATION_TERMS)
    if non_textile_class_hits and classification_hits:
        reasons.append(f"clasificación mixta textil/no textil, sin penalización: {non_textile_class_hits}")
    elif non_textile_class_hits:
        score -= 5
        exclusion_evidence_count += 1
        reasons.append(f"clasificación sugiere objeto no textil: {non_textile_class_hits}")

    non_textile_medium_hits = buscar_terminos(medium, NON_TEXTILE_MEDIUM_TERMS)
    if non_textile_medium_hits and medium_hits:
        reasons.append(f"material mixto con fibras textiles, sin penalización: {non_textile_medium_hits}")
    elif non_textile_medium_hits:
        score -= 4
        exclusion_evidence_count += 1
        reasons.append(f"material sugiere objeto no textil: {non_textile_medium_hits}")

    # Los terminos no textiles del titulo (p. ej. "figure") solo penalizan si ni la
    # clasificacion ni el material aportan evidencia textil.
    sin_evidencia_material = not (classification_hits or medium_hits)

    non_textile_title_hits = buscar_terminos(title, NON_TEXTILE_TITLE_TERMS)
    if non_textile_title_hits and sin_evidencia_material:
        score -= 4
        exclusion_evidence_count += 1
        reasons.append(f"título sugiere objeto no textil: {non_textile_title_hits}")
    elif non_textile_title_hits:
        reasons.append(f"título con término no textil, sin penalización por evidencia textil: {non_textile_title_hits}")

    non_textile_object_hits = buscar_terminos(object_name, NON_TEXTILE_TITLE_TERMS)
    if non_textile_object_hits and sin_evidencia_material:
        score -= 4
        exclusion_evidence_count += 1
        reasons.append(f"nombre de objeto sugiere objeto no textil: {non_textile_object_hits}")

    tool_hits = buscar_terminos(" ".join([title, object_name, classification]), TEXTILE_TOOL_TERMS)
    if tool_hits:
        score -= 5
        exclusion_evidence_count += 1
        reasons.append(f"herramienta textil, no superficie textil: {tool_hits}")

    # Curation status
    if not primary_image:
        estado = "excluido_sin_imagen"
    elif tool_hits:
        estado = "excluido_no_textil"
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
