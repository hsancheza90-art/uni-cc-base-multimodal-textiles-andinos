from __future__ import annotations

import argparse
import csv
from html import escape
from pathlib import Path


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as file:
        return list(csv.DictReader(file))


def card(row: dict[str, str]) -> str:
    title = escape(row.get("title", "Sin titulo"))
    source_id = escape(row.get("source_id", ""))
    accession = escape(row.get("accession_number", ""))
    culture = escape(row.get("culture", ""))
    date = escape(row.get("creation_date", ""))
    medium = escape(row.get("medium", ""))
    technique = escape(row.get("technique", ""))
    image_url = escape(row.get("image_url", ""))
    url = escape(row.get("url", ""))
    andean_terms = escape(row.get("andean_terms", ""))
    textile_terms = escape(row.get("textile_terms", ""))

    return f"""
    <article class="card">
      <a href="{url}" target="_blank" rel="noopener">
        <img src="{image_url}" alt="{title}" loading="lazy">
      </a>
      <div class="body">
        <h2>{title}</h2>
        <p><strong>ID:</strong> {source_id} | <strong>Accession:</strong> {accession}</p>
        <p><strong>Cultura:</strong> {culture}</p>
        <p><strong>Fecha:</strong> {date}</p>
        <p><strong>Medio:</strong> {medium}</p>
        <p><strong>Tecnica:</strong> {technique}</p>
        <p><strong>Evidencia andina:</strong> {andean_terms}</p>
        <p><strong>Evidencia textil:</strong> {textile_terms}</p>
      </div>
    </article>
    """


def build_html(rows: list[dict[str, str]]) -> str:
    cards = "\n".join(card(row) for row in rows)

    return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Revision visual CMA - textiles andinos</title>
  <style>
    body {{
      margin: 0;
      font-family: Arial, sans-serif;
      background: #f5f5f5;
      color: #222;
    }}
    header {{
      padding: 24px 32px;
      background: #111;
      color: white;
    }}
    header h1 {{
      margin: 0 0 8px;
      font-size: 24px;
    }}
    main {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 18px;
      padding: 24px;
    }}
    .card {{
      background: white;
      border: 1px solid #ddd;
      border-radius: 8px;
      overflow: hidden;
    }}
    img {{
      width: 100%;
      height: 280px;
      object-fit: contain;
      background: #eee;
      display: block;
    }}
    .body {{
      padding: 14px;
    }}
    h2 {{
      font-size: 16px;
      margin: 0 0 10px;
    }}
    p {{
      font-size: 13px;
      line-height: 1.35;
      margin: 6px 0;
    }}
  </style>
</head>
<body>
  <header>
    <h1>Revision visual CMA - textiles andinos</h1>
    <p>Total de candidatos: {len(rows)}</p>
  </header>
  <main>
    {cards}
  </main>
</body>
</html>
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Construye galeria HTML para revision visual CMA.")
    parser.add_argument("--root", default=".", help="Raiz del repositorio.")
    parser.add_argument(
        "--csv",
        default="data/metadata/cma_andes_textiles_candidates.csv",
        help="CSV normalizado CMA.",
    )
    parser.add_argument(
        "--output",
        default="outputs/review/cma_andes_textiles_candidates_gallery.html",
        help="HTML de salida.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    rows = read_rows(root / args.csv)
    candidates = [row for row in rows if row.get("curation_status") == "candidate"]

    output_path = root / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(build_html(candidates), encoding="utf-8")

    print(f"Candidatos visualizados: {len(candidates)}")
    print(f"Galeria HTML: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())