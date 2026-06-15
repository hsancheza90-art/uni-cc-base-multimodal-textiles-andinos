from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from src.preprocessing.surface_filters import classify_surface_type, normalize_object_type


INPUT_CLEAN_PATH = "data/processed/met_textiles_pilot_clean.csv"
OUTPUT_CORPUS_PATH = "data/metadata/corpus_piloto.csv"


def safe_get(row: pd.Series, column: str, default: Any = "") -> Any:
    if column not in row:
        return default

    value = row[column]

    if pd.isna(value):
        return default

    return value


def infer_license(row: pd.Series) -> str:
    public_domain = str(safe_get(row, "es_dominio_publico", "")).lower()
    rights = str(safe_get(row, "derechos_reproduccion", "")).strip()

    if public_domain == "true":
        return "Dominio público / Open Access según metadata de The Met"

    if rights:
        return rights

    return "No especificada en metadata procesada"


def build_description(row: pd.Series) -> str:
    parts = []

    title = safe_get(row, "titulo_original")
    culture = safe_get(row, "cultura")
    period = safe_get(row, "periodo")
    date_obj = safe_get(row, "fecha_objeto")
    material = safe_get(row, "material_original")
    classification = safe_get(row, "clasificacion_original")
    dimensions = safe_get(row, "dimensiones")

    if title:
        parts.append(f"Título oficial: {title}.")
    if culture:
        parts.append(f"Cultura registrada: {culture}.")
    if period:
        parts.append(f"Periodo registrado: {period}.")
    if date_obj:
        parts.append(f"Fecha del objeto: {date_obj}.")
    if material:
        parts.append(f"Material registrado: {material}.")
    if classification:
        parts.append(f"Clasificación museográfica: {classification}.")
    if dimensions:
        parts.append(f"Dimensiones: {dimensions}.")

    return " ".join(parts)


def build_local_image_path(row: pd.Series) -> str:
    object_id = safe_get(row, "id_objeto")
    if not object_id:
        return ""

    return f"outputs/samples/met_textiles_pilot_clean/met_textil_{object_id}.jpg"


def normalize_material(row: pd.Series) -> str:
    text = str(safe_get(row, "material_original", "")).lower()

    materials = []

    if "cotton" in text:
        materials.append("algodón")
    if "camelid" in text:
        materials.append("fibra de camélido")
    if "wool" in text:
        materials.append("lana")
    if "feather" in text:
        materials.append("plumas")
    if "fiber" in text or "fibre" in text:
        materials.append("fibra textil")

    if materials:
        return "; ".join(sorted(set(materials)))

    return ""


def normalize_technique(row: pd.Series) -> str:
    text = " ".join([
        str(safe_get(row, "material_original", "")),
        str(safe_get(row, "clasificacion_original", "")),
        str(safe_get(row, "titulo_original", "")),
    ]).lower()

    techniques = []

    if "woven" in text or "weaving" in text or "textiles-woven" in text:
        techniques.append("tejido")
    if "tapestry" in text:
        techniques.append("tapiz")
    if "embroider" in text or "embroidery" in text:
        techniques.append("bordado")
    if "feather" in text:
        techniques.append("trabajo con plumas")

    if techniques:
        return "; ".join(sorted(set(techniques)))

    return ""


def build_corpus_piloto(
    input_clean_path: str = INPUT_CLEAN_PATH,
    output_corpus_path: str = OUTPUT_CORPUS_PATH,
    max_records: int = 50,
) -> pd.DataFrame:
    input_path = Path(input_clean_path)
    output_path = Path(output_corpus_path)

    if not input_path.exists():
        raise FileNotFoundError(f"No existe el archivo de entrada: {input_path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path)

    rows = []

    for _, row in df.iterrows():
        row_dict = row.to_dict()

        surface_info = classify_surface_type(row_dict)
        tipo_objeto = normalize_object_type(row_dict)

        if surface_info["corpus_analisis"] == "corpus_secundario_formato_estrecho":
            continue

        record = {
            "id_registro": f"MET-{safe_get(row, 'id_objeto')}",
            "id_objeto": safe_get(row, "id_objeto"),
            "fuente": safe_get(row, "fuente"),
            "institucion": safe_get(row, "institucion"),
            "url": safe_get(row, "url_objeto"),
            "imagen_url": safe_get(row, "url_imagen"),
            "imagen_url_miniatura": safe_get(row, "url_imagen_miniatura"),
            "imagen_local": build_local_image_path(row),
            "titulo_original": safe_get(row, "titulo_original"),
            "titulo_es_sugerido": safe_get(row, "titulo_es_sugerido"),
            "descripcion_oficial": build_description(row),
            "cultura": safe_get(row, "cultura"),
            "periodo": safe_get(row, "periodo"),
            "fecha_objeto": safe_get(row, "fecha_objeto"),
            "procedencia": "; ".join(
                item for item in [
                    str(safe_get(row, "pais", "")),
                    str(safe_get(row, "region", "")),
                    str(safe_get(row, "subregion", "")),
                    str(safe_get(row, "localidad", "")),
                ]
                if item and item != "nan"
            ),
            "tipo_objeto": tipo_objeto,
            "tipo_superficie": surface_info["tipo_superficie"],
            "corpus_analisis": surface_info["corpus_analisis"],
            "motivo_superficie": surface_info["motivo_superficie"],
            "material": safe_get(row, "material_original"),
            "material_normalizado": normalize_material(row),
            "tecnica": normalize_technique(row),
            "colores": "",
            "color_dominante": "",
            "contraste": "",
            "densidad_visual": "",
            "motivos": "",
            "familia_iconografica": "",
            "simetria": "",
            "composicion": "",
            "descripcion": build_description(row),
            "licencia": infer_license(row),
            "estado_metadata": "parcial",
            "estado_anotacion": "sin_anotar",
            "observaciones": "",
            "decision_filtro": safe_get(row, "decision_filtro"),
            "puntaje_filtro": safe_get(row, "puntaje_filtro"),
            "motivo_filtrado": safe_get(row, "motivo_filtrado"),
            "fecha_descarga": safe_get(row, "fecha_descarga"),
            "fecha_anotacion": "",
        }

        rows.append(record)

    corpus = pd.DataFrame(rows)

    if not corpus.empty:
        corpus = corpus.head(max_records)

    corpus.to_csv(output_path, index=False, encoding="utf-8-sig")

    print(f"Corpus piloto generado: {output_corpus_path}")
    print(f"Registros en corpus piloto: {len(corpus)}")

    if not corpus.empty:
        print("\nDistribución por tipo_objeto:")
        print(corpus["tipo_objeto"].value_counts(dropna=False))
        print("\nDistribución por corpus_analisis:")
        print(corpus["corpus_analisis"].value_counts(dropna=False))

    return corpus


if __name__ == "__main__":
    build_corpus_piloto()