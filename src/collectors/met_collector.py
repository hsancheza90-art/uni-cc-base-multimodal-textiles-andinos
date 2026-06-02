from __future__ import annotations

import json
import os
import time
from urllib.parse import quote

import pandas as pd
import requests
from tqdm import tqdm

from src.preprocessing.spanish_schema import normalize_met_record_es


BASE_URL = "https://collectionapi.metmuseum.org/public/collection/v1"

QUERY_TERMS = [
    "Andean textile",
    "Peruvian textile",
    "Peru textile",
    "Inca textile",
    "Paracas textile",
    "Nasca textile",
    "Nazca textile",
    "Wari textile",
    "Huari textile",
    "Chancay textile",
    "Moche textile",
    "Andean weaving",
    "Peru weaving",
    "Inca tunic",
    "Paracas mantle",
    "Wari tapestry",
    "Chancay weaving",
    "textile fragment Peru",
]


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def search_met_objects(query: str, has_images: bool = True) -> list[int]:
    encoded_query = quote(query)
    url = f"{BASE_URL}/search?hasImages={str(has_images).lower()}&q={encoded_query}"

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    data = response.json()
    return data.get("objectIDs") or []


def get_met_object(object_id: int) -> dict:
    url = f"{BASE_URL}/objects/{object_id}"

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    return response.json()


def collect_met_metadata_curated(
    output_raw_dir: str = "data/raw/met",
    output_candidates_path: str = "data/processed/met_candidatos_normalizados.csv",
    output_curated_path: str = "data/processed/met_textiles_curado.csv",
    max_objects_per_query: int = 50,
    sleep_seconds: float = 0.2,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Collect candidate objects from The Met API, normalize to Spanish schema,
    apply textile curation filters, and save both candidate and curated datasets.
    """
    ensure_dir(output_raw_dir)
    ensure_dir(os.path.dirname(output_candidates_path))
    ensure_dir(os.path.dirname(output_curated_path))

    all_rows = []
    seen_ids = set()

    for query in QUERY_TERMS:
        print(f"\nBuscando término: {query}")

        try:
            object_ids = search_met_objects(query=query, has_images=True)
        except Exception as e:
            print(f"Error en búsqueda '{query}': {e}")
            continue

        object_ids = object_ids[:max_objects_per_query]
        print(f"Candidatos recuperados: {len(object_ids)}")

        for object_id in tqdm(object_ids):
            if object_id in seen_ids:
                continue

            try:
                record = get_met_object(object_id)
                seen_ids.add(object_id)

                raw_path = os.path.join(output_raw_dir, f"{object_id}.json")
                with open(raw_path, "w", encoding="utf-8") as f:
                    json.dump(record, f, ensure_ascii=False, indent=2)

                row = normalize_met_record_es(record, termino_busqueda=query)
                all_rows.append(row)

                time.sleep(sleep_seconds)

            except Exception as e:
                print(f"Error procesando objeto {object_id}: {e}")

    df_candidates = pd.DataFrame(all_rows)

    if df_candidates.empty:
        print("\nNo se recolectaron registros.")
        return df_candidates, df_candidates

    df_candidates = df_candidates.drop_duplicates(subset=["fuente", "id_objeto"])

    df_candidates.to_csv(
        output_candidates_path,
        index=False,
        encoding="utf-8-sig",
    )

    df_curated = df_candidates[
        df_candidates["estado_curacion"].isin(
            ["aceptado_textil", "revision_manual"]
        )
    ].copy()

    df_curated = df_curated.sort_values(
        by=["estado_curacion", "puntaje_textil"],
        ascending=[True, False],
    )

    df_curated.to_csv(
        output_curated_path,
        index=False,
        encoding="utf-8-sig",
    )

    print("\nProceso de curaduría terminado.")
    print(f"Total de candidatos: {len(df_candidates)}")
    print("Distribución de estados:")
    print(df_candidates["estado_curacion"].value_counts(dropna=False))
    print(f"\nDataset de candidatos guardado en: {output_candidates_path}")
    print(f"Dataset curado guardado en: {output_curated_path}")

    return df_candidates, df_curated


def download_curated_sample_images(
    metadata_path: str = "data/processed/met_textiles_curado.csv",
    output_image_dir: str = "outputs/samples/met_curado",
    max_images: int = 40,
    sleep_seconds: float = 0.3,
) -> None:
    """
    Download only accepted textile images for visual validation.
    Manual-review records are not downloaded by default.
    """
    ensure_dir(output_image_dir)

    df = pd.read_csv(metadata_path)

    df = df[df["estado_curacion"] == "aceptado_textil"].copy()

    df = df[
        df["url_imagen_miniatura"].notna()
        & (df["url_imagen_miniatura"].astype(str).str.len() > 0)
    ].copy()

    df = df.sort_values("puntaje_textil", ascending=False).head(max_images)

    print(f"\nImágenes aceptadas para descarga: {len(df)}")

    for _, row in tqdm(df.iterrows(), total=len(df)):
        object_id = row["id_objeto"]
        image_url = row["url_imagen_miniatura"]

        try:
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()

            image_path = os.path.join(output_image_dir, f"met_textil_{object_id}.jpg")

            with open(image_path, "wb") as f:
                f.write(response.content)

            time.sleep(sleep_seconds)

        except Exception as e:
            print(f"Error descargando imagen del objeto {object_id}: {e}")


if __name__ == "__main__":
    collect_met_metadata_curated(
        output_raw_dir="data/raw/met",
        output_candidates_path="data/processed/met_candidatos_normalizados.csv",
        output_curated_path="data/processed/met_textiles_curado.csv",
        max_objects_per_query=50,
        sleep_seconds=0.2,
    )

    download_curated_sample_images(
        metadata_path="data/processed/met_textiles_curado.csv",
        output_image_dir="outputs/samples/met_curado",
        max_images=40,
        sleep_seconds=0.3,
    )