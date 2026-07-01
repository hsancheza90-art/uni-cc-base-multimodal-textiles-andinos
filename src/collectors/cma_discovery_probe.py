from __future__ import annotations

import csv
from pathlib import Path

import requests


API_URL = "https://openaccess-api.clevelandart.org/api/artworks/"

STRATEGIES = [
    {"name": "q_andes_textile", "params": {"q": "Andes textile", "has_image": 1, "limit": 1000}},
    {"name": "q_peru_textile", "params": {"q": "Peru textile", "has_image": 1, "limit": 1000}},
    {"name": "q_andean_weaving", "params": {"q": "Andean weaving", "has_image": 1, "limit": 1000}},
    {"name": "type_textile", "params": {"type": "Textile", "has_image": 1, "limit": 1000}},
    {"name": "type_textile_culture_peru", "params": {"type": "Textile", "culture": "Peru", "has_image": 1, "limit": 1000}},
    {"name": "type_textile_culture_andes", "params": {"type": "Textile", "culture": "Andes", "has_image": 1, "limit": 1000}},
    {"name": "type_textile_medium_cotton", "params": {"type": "Textile", "medium": "cotton", "has_image": 1, "limit": 1000}},
    {"name": "type_textile_medium_camelid", "params": {"type": "Textile", "medium": "camelid", "has_image": 1, "limit": 1000}},
    {"name": "technique_woven_peru", "params": {"technique": "woven", "culture": "Peru", "has_image": 1, "limit": 1000}},
    {"name": "medium_camelid_peru", "params": {"medium": "camelid", "culture": "Peru", "has_image": 1, "limit": 1000}},
]


def fetch(params: dict) -> list[dict]:
    response = requests.get(API_URL, params=params, timeout=30)
    response.raise_for_status()
    return response.json().get("data", [])


def main() -> int:
    output_path = Path("outputs/reports/cma_discovery_probe.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    global_ids = set()
    rows = []

    for strategy in STRATEGIES:
        records = fetch(strategy["params"])
        ids = {str(record.get("id")) for record in records if record.get("id")}
        new_ids = ids - global_ids
        global_ids.update(ids)

        rows.append({
            "strategy": strategy["name"],
            "records": len(records),
            "unique_ids": len(ids),
            "new_ids_vs_previous": len(new_ids),
            "params": strategy["params"],
        })

        print(
            f"{strategy['name']}: "
            f"{len(records)} registros, "
            f"{len(ids)} unicos, "
            f"{len(new_ids)} nuevos"
        )

    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["strategy", "records", "unique_ids", "new_ids_vs_previous", "params"],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nTotal unico acumulado: {len(global_ids)}")
    print(f"Reporte: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())