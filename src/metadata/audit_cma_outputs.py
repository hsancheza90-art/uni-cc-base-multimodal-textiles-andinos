from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


FORBIDDEN_MARKER = "Forbidden. Calls to this URL via the terminal are not allowed."

REQUIRED_COLUMNS = [
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

VALID_STATUSES = {
    "candidate",
    "excluded_no_image",
    "excluded_no_andean_evidence",
    "excluded_no_textile_evidence",
}


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        return list(reader.fieldnames or []), list(reader)


def audit_csv(path: Path) -> list[str]:
    issues: list[str] = []

    if not path.exists():
        return [f"FALTA: {path}"]

    text = path.read_text(encoding="utf-8", errors="replace")
    if FORBIDDEN_MARKER in text:
        return [f"CORRUPTO: {path} contiene mensaje Forbidden"]

    fields, rows = read_csv_rows(path)

    if not fields:
        issues.append(f"VACIO: {path} no tiene encabezados")
        return issues

    missing_columns = [column for column in REQUIRED_COLUMNS if column not in fields]
    if missing_columns:
        issues.append(f"COLUMNAS: faltan columnas requeridas: {', '.join(missing_columns)}")

    if not rows:
        issues.append(f"VACIO: {path} no tiene registros")
        return issues

    seen_ids: set[str] = set()
    duplicate_ids: set[str] = set()

    for index, row in enumerate(rows, start=2):
        source_id = row.get("source_id", "").strip()
        title = row.get("title", "").strip()
        image_url = row.get("image_url", "").strip()
        has_image = row.get("has_image", "").strip()
        status = row.get("curation_status", "").strip()
        andean_terms = row.get("andean_terms", "").strip()
        textile_terms = row.get("textile_terms", "").strip()

        if not source_id:
            issues.append(f"FILA {index}: source_id vacio")
        elif source_id in seen_ids:
            duplicate_ids.add(source_id)
        seen_ids.add(source_id)

        if not title:
            issues.append(f"FILA {index}: title vacio")

        if status not in VALID_STATUSES:
            issues.append(f"FILA {index}: curation_status invalido: {status}")

        if has_image == "True" and not image_url:
            issues.append(f"FILA {index}: has_image=True pero image_url vacio")

        if status == "candidate":
            if not image_url:
                issues.append(f"FILA {index}: candidato sin image_url")
            if not andean_terms:
                issues.append(f"FILA {index}: candidato sin andean_terms")
            if not textile_terms:
                issues.append(f"FILA {index}: candidato sin textile_terms")

    if duplicate_ids:
        sample = ", ".join(sorted(duplicate_ids)[:10])
        issues.append(f"DUPLICADOS: source_id repetidos: {sample}")

    return issues


def summarize_csv(path: Path) -> list[str]:
    if not path.exists():
        return []

    _, rows = read_csv_rows(path)
    status_counts: dict[str, int] = {}

    for row in rows:
        status = row.get("curation_status", "SIN_ESTADO")
        status_counts[status] = status_counts.get(status, 0) + 1

    lines = [
        f"Registros auditados: {len(rows)}",
        "Estados detectados:",
    ]

    for status, count in sorted(status_counts.items()):
        lines.append(f"- {status}: {count}")

    return lines


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audita el CSV normalizado de Cleveland Museum of Art."
    )
    parser.add_argument("--root", default=".", help="Raiz del repositorio.")
    parser.add_argument(
        "--csv",
        default="data/metadata/cma_andes_textiles_candidates.csv",
        help="Ruta relativa del CSV CMA normalizado.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    csv_path = root / args.csv

    print(f"Archivo auditado: {csv_path}")

    for line in summarize_csv(csv_path):
        print(line)

    issues = audit_csv(csv_path)

    if issues:
        print("\nHallazgos")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print("\nSin hallazgos criticos.")
    return 0


if __name__ == "__main__":
    sys.exit(main())