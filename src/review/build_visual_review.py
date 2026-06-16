from __future__ import annotations

from pathlib import Path
from html import escape

import pandas as pd


ACCEPTED_PATH = Path("data/processed/met_textiles_pilot_clean.csv")
REJECTED_PATH = Path("data/processed/met_textiles_rejected.csv")
CORPUS_PILOTO_PATH = Path("data/metadata/corpus_piloto.csv")
CORPUS_CLEAN_PATH = Path("data/metadata/corpus_piloto_clean.csv")

OUTPUT_DIR = Path("outputs/review")
ACCEPTED_HTML = OUTPUT_DIR / "aceptados_revision.html"
REJECTED_HTML = OUTPUT_DIR / "rechazados_revision.html"
CORPUS_PILOTO_HTML = OUTPUT_DIR / "corpus_piloto_revision.html"
CORPUS_CLEAN_HTML = OUTPUT_DIR / "corpus_piloto_clean_revision.html"
REVIEW_TEMPLATE = Path("data/metadata/revision_visual_template.csv")


def safe_value(row: pd.Series, col: str) -> str:
    if col not in row:
        return ""
    value = row[col]
    if pd.isna(value):
        return ""
    return str(value)


def get_image_url(row: pd.Series) -> str:
    for col in ["url_imagen_miniatura", "imagen_url_miniatura", "url_imagen", "imagen_url"]:
        value = safe_value(row, col)
        if value:
            return value
    return ""


def get_object_url(row: pd.Series) -> str:
    for col in ["url_objeto", "url"]:
        value = safe_value(row, col)
        if value:
            return value
    return ""


def select_review_columns(df: pd.DataFrame) -> pd.DataFrame:
    cols = [
        "id_objeto",
        "titulo_original",
        "titulo_es_sugerido",
        "cultura",
        "periodo",
        "pais",
        "region",
        "clasificacion_original",
        "nombre_objeto_original",
        "material_original",
        "decision_filtro",
        "estado_filtrado",
        "puntaje_filtro",
        "motivo_filtrado",
        "url_objeto",
        "url_imagen",
        "url_imagen_miniatura",
    ]

    available = [col for col in cols if col in df.columns]
    return df[available].copy()


def build_review_template(df_accepted: pd.DataFrame, df_rejected: pd.DataFrame) -> None:
    REVIEW_TEMPLATE.parent.mkdir(parents=True, exist_ok=True)

    accepted = select_review_columns(df_accepted)
    accepted["grupo_revision"] = "aceptado_por_filtro"

    rejected = select_review_columns(df_rejected)
    rejected["grupo_revision"] = "rechazado_por_filtro"

    df = pd.concat([accepted, rejected], ignore_index=True)

    df["revision_visual"] = ""
    df["accion_sugerida"] = ""
    df["observaciones_revision"] = ""

    # Reorder key columns
    first_cols = [
        "grupo_revision",
        "id_objeto",
        "titulo_original",
        "cultura",
        "clasificacion_original",
        "material_original",
        "puntaje_filtro",
        "revision_visual",
        "accion_sugerida",
        "observaciones_revision",
    ]

    ordered_cols = [col for col in first_cols if col in df.columns]
    remaining_cols = [col for col in df.columns if col not in ordered_cols]

    df = df[ordered_cols + remaining_cols]

    df.to_csv(REVIEW_TEMPLATE, index=False, encoding="utf-8-sig")
    print(f"Plantilla de revisión generada: {REVIEW_TEMPLATE}")


def build_html_card(row: pd.Series, index: int, group: str) -> str:
    object_id = escape(safe_value(row, "id_objeto"))
    title = escape(safe_value(row, "titulo_original"))
    title_es = escape(safe_value(row, "titulo_es_sugerido"))
    culture = escape(safe_value(row, "cultura"))
    period = escape(safe_value(row, "periodo"))
    classification = escape(safe_value(row, "clasificacion_original"))
    object_name = escape(safe_value(row, "nombre_objeto_original"))
    medium = escape(safe_value(row, "material_original"))
    score = escape(safe_value(row, "puntaje_filtro"))
    reason = escape(safe_value(row, "motivo_filtrado"))
    image_url = get_image_url(row)
    object_url = get_object_url(row)

    image_html = (
        f'<img src="{escape(image_url)}" alt="{title}" loading="lazy">'
        if image_url else
        '<div class="no-image">Sin imagen</div>'
    )

    object_link = (
        f'<a href="{escape(object_url)}" target="_blank">Ficha oficial</a>'
        if object_url else
        "Sin URL oficial"
    )

    return f"""
    <article class="card">
        <div class="image-box">
            {image_html}
        </div>
        <div class="content">
            <h2>{index}. {title}</h2>
            <p><strong>ID:</strong> {object_id}</p>
            <p><strong>Título sugerido:</strong> {title_es}</p>
            <p><strong>Cultura:</strong> {culture}</p>
            <p><strong>Periodo:</strong> {period}</p>
            <p><strong>Clasificación:</strong> {classification}</p>
            <p><strong>Nombre objeto:</strong> {object_name}</p>
            <p><strong>Material:</strong> {medium}</p>
            <p><strong>Puntaje:</strong> {score}</p>
            <p><strong>Motivo filtro:</strong> {reason}</p>
            <p><strong>Enlace:</strong> {object_link}</p>
            <div class="review-box">
                <p><strong>Revisión sugerida en CSV:</strong></p>
                <code>revision_visual = correcto / falso_positivo / falso_negativo / revisar</code><br>
                <code>accion_sugerida = mantener / mover_a_rechazados / mover_a_aceptados / revisar_metadata</code>
            </div>
        </div>
    </article>
    """


def build_html_page(df: pd.DataFrame, output_path: Path, title: str, group: str, max_records: int = 120) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df = df.copy()

    if "puntaje_filtro" in df.columns:
        if group == "aceptados":
            df = df.sort_values("puntaje_filtro", ascending=True)
        else:
            df = df.sort_values("puntaje_filtro", ascending=False)

    df = df.head(max_records)

    cards = "\n".join(
        build_html_card(row, i + 1, group)
        for i, (_, row) in enumerate(df.iterrows())
    )

    html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>{escape(title)}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background: #f5f5f5;
            margin: 24px;
            color: #222;
        }}
        h1 {{
            margin-bottom: 8px;
        }}
        .summary {{
            background: #fff;
            border-radius: 10px;
            padding: 16px;
            margin-bottom: 20px;
            border: 1px solid #ddd;
        }}
        .card {{
            display: grid;
            grid-template-columns: 320px 1fr;
            gap: 20px;
            background: #fff;
            border: 1px solid #ddd;
            border-radius: 12px;
            margin-bottom: 18px;
            padding: 16px;
        }}
        .image-box {{
            width: 320px;
            min-height: 220px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #eee;
            border-radius: 8px;
            overflow: hidden;
        }}
        img {{
            max-width: 100%;
            max-height: 320px;
            object-fit: contain;
        }}
        h2 {{
            margin-top: 0;
            font-size: 18px;
        }}
        p {{
            margin: 5px 0;
            line-height: 1.35;
        }}
        .review-box {{
            margin-top: 12px;
            padding: 10px;
            background: #f0f4ff;
            border-left: 4px solid #4f6bed;
        }}
        code {{
            font-size: 13px;
        }}
        .no-image {{
            color: #777;
            font-style: italic;
        }}
    </style>
</head>
<body>
    <h1>{escape(title)}</h1>
    <div class="summary">
        <p><strong>Registros mostrados:</strong> {len(df)}</p>
        <p><strong>Grupo:</strong> {escape(group)}</p>
        <p>Usar esta galería para revisar visualmente los registros y completar la plantilla <code>data/metadata/revision_visual_template.csv</code>.</p>
    </div>
    {cards}
</body>
</html>
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Galería generada: {output_path}")


def main() -> None:
    if not ACCEPTED_PATH.exists():
        raise FileNotFoundError(f"No existe: {ACCEPTED_PATH}")

    if not REJECTED_PATH.exists():
        raise FileNotFoundError(f"No existe: {REJECTED_PATH}")

    accepted = pd.read_csv(ACCEPTED_PATH)
    rejected = pd.read_csv(REJECTED_PATH)

    build_html_page(
        accepted,
        ACCEPTED_HTML,
        title="Revisión visual de registros aceptados",
        group="aceptados",
        max_records=160,
    )

    build_html_page(
        rejected,
        REJECTED_HTML,
        title="Revisión visual de registros rechazados",
        group="rechazados",
        max_records=160,
    )

    if CORPUS_PILOTO_PATH.exists():
        corpus_piloto = pd.read_csv(CORPUS_PILOTO_PATH)

        build_html_page(
            corpus_piloto,
            CORPUS_PILOTO_HTML,
            title="Revisión visual del corpus piloto principal",
            group="corpus_piloto",
            max_records=160,
        )

    if CORPUS_CLEAN_PATH.exists():
        corpus_clean = pd.read_csv(CORPUS_CLEAN_PATH)

        build_html_page(
            corpus_clean,
            CORPUS_CLEAN_HTML,
            title="Revisión visual del corpus piloto limpio",
            group="corpus_piloto_clean",
            max_records=160,
        )

    build_review_template(accepted, rejected)

if __name__ == "__main__":
    main()