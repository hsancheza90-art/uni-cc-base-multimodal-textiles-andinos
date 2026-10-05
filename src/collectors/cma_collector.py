"""Recolecta candidatos textiles andinos desde la API Open Access del Cleveland Museum of Art.

Por defecto escribe en data/raw/cma/ (fuera de git). La lista curada
data/metadata/cma_andes_textiles_candidates.csv es insumo del corpus y solo se
reemplaza con --salida apuntando a ella y --forzar.
"""

from __future__ import annotations

import argparse
import csv
import json
import time
from collections import defaultdict
from pathlib import Path

import requests

from src.utils.http import crear_sesion
from src.utils.texto import buscar_terminos

API_URL = "https://openaccess-api.clevelandart.org/api/artworks/"
INSUMO_CURADO = Path("data/metadata/cma_andes_textiles_candidates.csv")
REPORTE_INSUMO = Path("outputs/reports/cma_collection_summary.md")
SALIDA_DEFECTO = Path("data/raw/cma/cma_andes_textiles_candidates.csv")

DEFAULT_QUERIES = [
    "Andes textile",
    "Andean textile",
    "Peru textile",
    "Peruvian textile",
    "Inca textile",
    "Wari textile",
    "Huari textile",
    "Chancay textile",
    "Nazca textile",
    "Nasca textile",
    "Paracas textile",
    "Moche textile",
    "Chimu textile",
    "Tiwanaku textile",
    "South Coast textile",
    "North Coast textile",
]

TEXTILE_TERMS = [
    "textile", "woven", "weaving", "cotton", "camelid", "wool",
    "fiber", "cloth", "tunic", "mantle", "shirt", "garment",
]

ANDEAN_TERMS = [
    "andes", "andean", "peru", "peruvian", "inca", "wari", "huari",
    "chancay", "nazca", "nasca", "paracas", "moche", "chimu",
    "tiwanaku", "tiahuanaco", "south coast", "north coast",
]

OUTPUT_COLUMNS = [
    "source",
    "source_id",
    "accession_number",
    "title",
    "culture",
    "creation_date",
    "classification",
    "technique",
    "medium",
    "department",
    "description",
    "url",
    "image_url",
    "share_license_status",
    "has_image",
    "andean_terms",
    "textile_terms",
    "curation_status",
    "curation_notes",
    "raw_queries",
]


def clean_text(value) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return " ".join(value.split())
    if isinstance(value, list):
        return "; ".join(clean_text(item) for item in value if item)
    if isinstance(value, dict):
        return "; ".join(f"{k}: {clean_text(v)}" for k, v in value.items() if v)
    return str(value)


def get_image_url(record: dict) -> str:
    images = record.get("images") or {}
    if not isinstance(images, dict):
        return ""

    for key in ["web", "print", "full"]:
        image_data = images.get(key)
        if isinstance(image_data, dict) and image_data.get("url"):
            return image_data["url"]
        if isinstance(image_data, str):
            return image_data

    return ""


def searchable_text(record: dict) -> str:
    fields = [
        "title",
        "culture",
        "creation_date",
        "type",
        "technique",
        "medium",
        "department",
        "description",
        "tombstone",
    ]
    return " ".join(clean_text(record.get(field)).lower() for field in fields)


def find_terms(text: str, terms: list[str]) -> str:
    return "; ".join(sorted(set(buscar_terminos(text, terms))))


def normalize_record(record: dict, queries: list[str]) -> dict:
    text = searchable_text(record)

    andean_terms = find_terms(text, ANDEAN_TERMS)
    textile_terms = find_terms(text, TEXTILE_TERMS)
    image_url = get_image_url(record)

    if image_url and andean_terms and textile_terms:
        status = "candidate"
        notes = "Pendiente de revision visual."
    elif not image_url:
        status = "excluded_no_image"
        notes = "Registro sin URL de imagen."
    elif not andean_terms:
        status = "excluded_no_andean_evidence"
        notes = "Sin evidencia andina suficiente en metadatos."
    else:
        status = "excluded_no_textile_evidence"
        notes = "Sin evidencia textil suficiente en metadatos."

    return {
        "source": "Cleveland Museum of Art",
        "source_id": clean_text(record.get("id")),
        "accession_number": clean_text(record.get("accession_number")),
        "title": clean_text(record.get("title")),
        "culture": clean_text(record.get("culture")),
        "creation_date": clean_text(record.get("creation_date")),
        "classification": clean_text(record.get("type")),
        "technique": clean_text(record.get("technique")),
        "medium": clean_text(record.get("medium")),
        "department": clean_text(record.get("department")),
        "description": clean_text(record.get("description")),
        "url": clean_text(record.get("url")),
        "image_url": image_url,
        "share_license_status": clean_text(record.get("share_license_status")),
        "has_image": str(bool(image_url)),
        "andean_terms": andean_terms,
        "textile_terms": textile_terms,
        "curation_status": status,
        "curation_notes": notes,
        "raw_queries": "; ".join(sorted(set(queries))),
    }


def fetch_cma_records(
    queries: list[str],
    limit_per_query: int,
    sleep_seconds: float,
    session: requests.Session | None = None,
    max_per_query: int = 1000,
) -> tuple[dict, dict, list[str]]:
    """Pagina cada consulta hasta agotar `info.total` (o `max_per_query`) y avisa si queda truncada."""
    session = session or crear_sesion()
    records = {}
    query_map = defaultdict(list)
    warnings: list[str] = []

    for query in queries:
        skip = 0
        total = None
        while True:
            params = {"q": query, "has_image": 1, "limit": limit_per_query, "skip": skip}
            response = session.get(API_URL, params=params, timeout=30)
            response.raise_for_status()
            payload = response.json()

            page = payload.get("data", [])
            total = (payload.get("info") or {}).get("total", total)
            for record in page:
                source_id = clean_text(record.get("id"))
                if not source_id:
                    continue
                records[source_id] = record
                query_map[source_id].append(query)

            skip += len(page)
            time.sleep(sleep_seconds)
            if not page or len(page) < limit_per_query or (total is not None and skip >= total):
                break
            if skip >= max_per_query:
                warnings.append(f"{query}: truncada en {skip} de {total} resultados (max_per_query={max_per_query})")
                break

        if total is not None and skip < total and not any(w.startswith(f"{query}:") for w in warnings):
            warnings.append(f"{query}: la API anuncio {total} resultados y entrego {skip}")

    return records, query_map, warnings


def write_jsonl(path: Path, records: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        for record in records.values():
            file.write(json.dumps(record, ensure_ascii=False) + "\n")


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_report(path: Path, rows: list[dict], warnings: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    total = len(rows)
    candidates = sum(row["curation_status"] == "candidate" for row in rows)

    lines = [
        "# Reporte de recoleccion CMA",
        "",
        f"- Registros normalizados: {total}",
        f"- Candidatos para revision visual: {candidates}",
        "",
        "## Estados de curacion",
        "",
    ]

    statuses = {}
    for row in rows:
        statuses[row["curation_status"]] = statuses.get(row["curation_status"], 0) + 1

    for status, count in sorted(statuses.items()):
        lines.append(f"- {status}: {count}")

    if warnings:
        lines.extend(["", "## Avisos de paginacion", ""])
        lines.extend(f"- {warning}" for warning in warnings)

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(("\n".join(lines) + "\n").encode("utf-8"))


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Recolecta candidatos textiles andinos desde CMA.")
    parser.add_argument("--root", default=".", help="Raiz del repositorio.")
    parser.add_argument("--query", action="append", dest="queries", help="Consulta especifica.")
    parser.add_argument("--limit-per-query", type=int, default=100, help="Resultados por pagina.")
    parser.add_argument("--max-per-query", type=int, default=1000, help="Tope de resultados por consulta.")
    parser.add_argument("--sleep", type=float, default=0.25)
    parser.add_argument("--salida", default=str(SALIDA_DEFECTO), help="CSV de salida, relativo a la raiz.")
    parser.add_argument(
        "--forzar",
        action="store_true",
        help=f"Permite reemplazar el insumo curado {INSUMO_CURADO.as_posix()}.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    root = Path(args.root).resolve()
    queries = args.queries or DEFAULT_QUERIES

    salida = Path(args.salida)
    es_insumo = salida.as_posix() == INSUMO_CURADO.as_posix()
    if es_insumo and (root / salida).exists() and not args.forzar:
        print(f"{salida.as_posix()} es insumo curado del corpus y no se sobrescribio. Use --forzar si es intencional.")
        return 1

    records, query_map, warnings = fetch_cma_records(
        queries=queries,
        limit_per_query=args.limit_per_query,
        sleep_seconds=args.sleep,
        max_per_query=args.max_per_query,
    )

    rows = [
        normalize_record(record, query_map[source_id])
        for source_id, record in sorted(records.items())
    ]

    raw_path = root / "data/raw/cma/cma_andes_textiles_raw.jsonl"
    csv_path = root / salida
    report_path = root / (REPORTE_INSUMO if es_insumo else salida.with_name(salida.stem + "_resumen.md"))

    write_jsonl(raw_path, records)
    write_csv(csv_path, rows)
    write_report(report_path, rows, warnings)

    print(f"Registros unicos CMA: {len(records)}")
    for warning in warnings:
        print(f"Aviso: {warning}")
    print(f"CSV normalizado: {csv_path}")
    print(f"JSONL crudo: {raw_path}")
    print(f"Reporte: {report_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())