from __future__ import annotations

from datetime import date
from typing import Any, Dict

from src.preprocessing.textile_filters import evaluate_met_record


def join_tags(record: Dict[str, Any]) -> str:
    tags = record.get("tags") or []

    if not isinstance(tags, list):
        return ""

    terms = []
    for tag in tags:
        if isinstance(tag, dict) and tag.get("term"):
            terms.append(str(tag.get("term")))

    return ", ".join(terms)


def suggest_spanish_title(record: Dict[str, Any]) -> str:
    """
    Conservative title suggestion in Spanish.

    We keep the official museum title in 'titulo_original'.
    This field only provides a cautious academic Spanish label.
    """
    title = str(record.get("title") or "").lower()
    classification = str(record.get("classification") or "").lower()
    medium = str(record.get("medium") or "").lower()

    text = " ".join([title, classification, medium])

    if "tunic" in text:
        return "Túnica textil"
    if "mantle" in text:
        return "Manto textil"
    if "textile fragment" in text:
        return "Fragmento textil"
    if "fragment" in text and ("textile" in text or "cotton" in text or "wool" in text or "camelid" in text):
        return "Fragmento textil"
    if "panel" in text and ("textile" in text or "cotton" in text or "wool" in text or "camelid" in text):
        return "Panel textil"
    if "bag" in text and ("textile" in text or "cotton" in text or "wool" in text or "camelid" in text):
        return "Bolsa textil"
    if "belt" in text or "sash" in text:
        return "Faja textil"
    if "headband" in text:
        return "Banda o vincha textil"
    if "textile" in text:
        return "Objeto textil"

    return ""


def normalize_met_record_es(record: Dict[str, Any], termino_busqueda: str) -> Dict[str, Any]:
    """
    Convert The Met API record into a Spanish academic schema.
    """
    curation = evaluate_met_record(record)

    titulo_original = record.get("title")
    titulo_es_sugerido = suggest_spanish_title(record)

    primary_image = record.get("primaryImage") or ""
    primary_image_small = record.get("primaryImageSmall") or ""

    if primary_image:
        url_imagen = primary_image
    else:
        url_imagen = primary_image_small

    estado = curation["estado_curacion"]

    if estado == "aceptado_textil":
        clasificacion_normalizada = "Textil"
    elif estado == "revision_manual":
        clasificacion_normalizada = "Candidato textil para revisión"
    else:
        clasificacion_normalizada = "No textil"

    return {
        "fuente": "met",
        "institucion": "The Metropolitan Museum of Art",
        "id_objeto": record.get("objectID"),
        "titulo_original": titulo_original,
        "titulo_es_sugerido": titulo_es_sugerido,
        "cultura": record.get("culture"),
        "periodo": record.get("period"),
        "fecha_objeto": record.get("objectDate"),
        "pais": record.get("country"),
        "region": record.get("region"),
        "subregion": record.get("subregion"),
        "localidad": record.get("locale"),
        "departamento_museo": record.get("department"),
        "clasificacion_original": record.get("classification"),
        "clasificacion_normalizada": clasificacion_normalizada,
        "nombre_objeto_original": record.get("objectName"),
        "material_original": record.get("medium"),
        "dimensiones": record.get("dimensions"),
        "linea_credito": record.get("creditLine"),
        "repositorio": record.get("repository"),
        "url_objeto": record.get("objectURL"),
        "url_imagen": url_imagen,
        "url_imagen_miniatura": primary_image_small,
        "es_dominio_publico": record.get("isPublicDomain"),
        "derechos_reproduccion": record.get("rightsAndReproduction"),
        "etiquetas_originales": join_tags(record),
        "termino_busqueda": termino_busqueda,
        "puntaje_textil": curation["puntaje_textil"],
        "estado_curacion": curation["estado_curacion"],
        "motivo_curacion": curation["motivo_curacion"],
        "conteo_evidencia_textil": curation["conteo_evidencia_textil"],
        "conteo_evidencia_exclusion": curation["conteo_evidencia_exclusion"],
        "fecha_descarga": date.today().isoformat(),
    }