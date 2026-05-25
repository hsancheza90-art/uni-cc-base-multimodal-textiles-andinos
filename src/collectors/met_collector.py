import os
import time
import json
import requests
import pandas as pd
from tqdm import tqdm
from urllib.parse import quote


BASE_URL = "https://collectionapi.metmuseum.org/public/collection/v1"


QUERY_TERMS = [
    "Andean textile",
    "Peru textile",
    "Peruvian textile",
    "Inca textile",
    "Paracas textile",
    "Nasca textile",
    "Wari textile",
    "Chancay textile",
    "Moche textile",
    "Andes weaving",
    "tunic Peru",
    "mantle Peru",
    "textile fragment Peru",
    "woven Peru",
    "tapestry Peru",
]


def ensure_dir(path: str) -> None:
    """Create directory if it does not exist."""
    os.makedirs(path, exist_ok=True)


def search_met_objects(query: str, has_images: bool = True) -> list:
    """
    Search objects in The Met Collection API.

    Parameters
    ----------
    query : str
        Search term.
    has_images : bool
        Whether to return only objects with images.

    Returns
    -------
    list
        List of object IDs.
    """
    encoded_query = quote(query)
    url = f"{BASE_URL}/search?hasImages={str(has_images).lower()}&q={encoded_query}"

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    data = response.json()

    if data.get("objectIDs") is None:
        return []

    return data["objectIDs"]


def get_met_object(object_id: int) -> dict:
    """
    Get object details from The Met Collection API.

    Parameters
    ----------
    object_id : int
        The Met object ID.

    Returns
    -------
    dict
        Object metadata.
    """
    url = f"{BASE_URL}/objects/{object_id}"

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    return response.json()


def normalize_met_record(record: dict, query_term: str) -> dict:
    """
    Normalize raw The Met API record into thesis-oriented schema.
    """
    return {
        "source": "met",
        "institution": "The Metropolitan Museum of Art",
        "object_id": record.get("objectID"),
        "title": record.get("title"),
        "culture": record.get("culture"),
        "period": record.get("period"),
        "object_date": record.get("objectDate"),
        "country": record.get("country"),
        "region": record.get("region"),
        "subregion": record.get("subregion"),
        "locale": record.get("locale"),
        "classification": record.get("classification"),
        "department": record.get("department"),
        "medium": record.get("medium"),
        "dimensions": record.get("dimensions"),
        "credit_line": record.get("creditLine"),
        "repository": record.get("repository"),
        "object_url": record.get("objectURL"),
        "primary_image": record.get("primaryImage"),
        "primary_image_small": record.get("primaryImageSmall"),
        "is_public_domain": record.get("isPublicDomain"),
        "rights_and_reproduction": record.get("rightsAndReproduction"),
        "artist_display_name": record.get("artistDisplayName"),
        "artist_culture": record.get("artistCulture"),
        "tags": ", ".join([tag.get("term", "") for tag in record.get("tags", [])]) if record.get("tags") else "",
        "query_term": query_term,
    }


def collect_met_metadata(
    output_raw_dir: str = "data/raw/met",
    output_processed_path: str = "data/processed/met_textiles_pilot.csv",
    max_objects_per_query: int = 40,
    sleep_seconds: float = 0.2,
) -> pd.DataFrame:
    """
    Collect metadata from The Met API using textile-related query terms.
    """
    ensure_dir(output_raw_dir)
    ensure_dir(os.path.dirname(output_processed_path))

    all_rows = []
    seen_ids = set()

    for query in QUERY_TERMS:
        print(f"\nSearching query: {query}")

        try:
            object_ids = search_met_objects(query=query, has_images=True)
        except Exception as e:
            print(f"Search failed for query '{query}': {e}")
            continue

        object_ids = object_ids[:max_objects_per_query]
        print(f"Found {len(object_ids)} candidate objects for query '{query}'")

        for object_id in tqdm(object_ids):
            if object_id in seen_ids:
                continue

            try:
                record = get_met_object(object_id)
                seen_ids.add(object_id)

                raw_path = os.path.join(output_raw_dir, f"{object_id}.json")
                with open(raw_path, "w", encoding="utf-8") as f:
                    json.dump(record, f, ensure_ascii=False, indent=2)

                row = normalize_met_record(record, query_term=query)
                all_rows.append(row)

                time.sleep(sleep_seconds)

            except Exception as e:
                print(f"Failed object {object_id}: {e}")
                continue

    df = pd.DataFrame(all_rows)

    if not df.empty:
        df = df.drop_duplicates(subset=["source", "object_id"])
        df.to_csv(output_processed_path, index=False, encoding="utf-8-sig")

    print(f"\nCollected records: {len(df)}")
    print(f"Saved to: {output_processed_path}")

    return df


def download_sample_images(
    metadata_path: str = "data/processed/met_textiles_pilot.csv",
    output_image_dir: str = "outputs/samples/met",
    max_images: int = 30,
    sleep_seconds: float = 0.3,
) -> None:
    """
    Download a small sample of images for visual validation.
    This is intentionally saved in outputs/samples, not in the full data/images directory.
    """
    ensure_dir(output_image_dir)

    df = pd.read_csv(metadata_path)

    df = df[
        df["primary_image_small"].notna()
        & (df["primary_image_small"].astype(str).str.len() > 0)
    ].copy()

    df = df.head(max_images)

    for _, row in tqdm(df.iterrows(), total=len(df)):
        object_id = row["object_id"]
        image_url = row["primary_image_small"]

        try:
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()

            image_path = os.path.join(output_image_dir, f"met_{object_id}.jpg")

            with open(image_path, "wb") as f:
                f.write(response.content)

            time.sleep(sleep_seconds)

        except Exception as e:
            print(f"Failed image for object {object_id}: {e}")


if __name__ == "__main__":
    df = collect_met_metadata(
        output_raw_dir="data/raw/met",
        output_processed_path="data/processed/met_textiles_pilot.csv",
        max_objects_per_query=40,
        sleep_seconds=0.2,
    )

    download_sample_images(
        metadata_path="data/processed/met_textiles_pilot.csv",
        output_image_dir="outputs/samples/met",
        max_images=30,
        sleep_seconds=0.3,
    )