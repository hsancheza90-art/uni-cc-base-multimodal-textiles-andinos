from __future__ import annotations

from pathlib import Path

import pandas as pd


CORPUS_PATH = Path("data/metadata/corpus_piloto.csv")
OUTPUT_REPORT = Path("outputs/reports/corpus_piloto_validation.md")


REQUIRED_COLUMNS = [
    "id_registro",
    "id_objeto",
    "fuente",
    "institucion",
    "url",
    "imagen_url",
    "imagen_local",
    "cultura",
    "periodo",
    "procedencia",
    "tipo_objeto",
    "material",
    "tecnica",
    "colores",
    "motivos",
    "simetria",
    "composicion",
    "descripcion",
    "licencia",
    "estado_metadata",
    "estado_anotacion",
]


IMPORTANT_COLUMNS = [
    "id_objeto",
    "fuente",
    "url",
    "imagen_url",
    "cultura",
    "periodo",
    "tipo_objeto",
    "material",
    "descripcion",
    "licencia",
]


NARROW_TERMS = [
    "sash",
    "belt",
    "band",
    "headband",
    "strap",
    "cord",
    "ribbon",
    "faja",
    "banda",
    "vincha",
    "cinturón",
]


def value_counts_md(series: pd.Series, col_name: str, count_name: str = "conteo") -> str:
    lines = [
        f"| {col_name} | {count_name} |",
        "|---|---:|",
    ]

    for key, value in series.items():
        key_text = str(key).replace("|", "/").replace("\n", " ")
        lines.append(f"| {key_text} | {value} |")

    return "\n".join(lines)


def detect_narrow_formats(df: pd.DataFrame) -> pd.DataFrame:
    text_cols = [
        "titulo_original",
        "titulo_es_sugerido",
        "tipo_objeto",
        "tipo_superficie",
        "motivo_superficie",
    ]

    available_cols = [col for col in text_cols if col in df.columns]

    if not available_cols:
        return pd.DataFrame()

    combined = df[available_cols].fillna("").astype(str).agg(" ".join, axis=1).str.lower()

    mask = combined.apply(lambda text: any(term in text for term in NARROW_TERMS))

    return df[mask].copy()


def validate_required_columns(df: pd.DataFrame) -> tuple[list[str], list[str]]:
    existing = list(df.columns)
    missing = [col for col in REQUIRED_COLUMNS if col not in existing]
    present = [col for col in REQUIRED_COLUMNS if col in existing]

    return present, missing


def validate_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    rows = []

    for col in IMPORTANT_COLUMNS:
        if col in df.columns:
            total = len(df)
            missing = df[col].isna().sum() + (df[col].astype(str).str.strip() == "").sum()
            rows.append(
                {
                    "campo": col,
                    "total": total,
                    "faltantes": int(missing),
                    "porcentaje_faltante": round((missing / total) * 100, 2) if total else 0,
                }
            )

    return pd.DataFrame(rows)


def validate_local_images(df: pd.DataFrame) -> tuple[int, int]:
    if "imagen_local" not in df.columns:
        return 0, 0

    existing = 0
    total = 0

    for path in df["imagen_local"].fillna("").astype(str):
        if not path.strip():
            continue

        total += 1

        if Path(path).exists():
            existing += 1

    return existing, total


def build_validation_report() -> None:
    if not CORPUS_PATH.exists():
        raise FileNotFoundError(f"No existe el archivo: {CORPUS_PATH}")

    OUTPUT_REPORT.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(CORPUS_PATH)

    present_cols, missing_cols = validate_required_columns(df)
    missing_values_df = validate_missing_values(df)
    narrow_df = detect_narrow_formats(df)
    existing_images, total_image_paths = validate_local_images(df)

    lines = []

    lines.append("# Reporte de validación del corpus piloto\n")

    lines.append("## Resumen general\n")
    lines.append(f"- Archivo evaluado: `{CORPUS_PATH}`")
    lines.append(f"- Total de registros: {len(df)}")
    lines.append(f"- Columnas requeridas presentes: {len(present_cols)}")
    lines.append(f"- Columnas requeridas faltantes: {len(missing_cols)}")
    lines.append(f"- Rutas locales de imagen existentes: {existing_images} de {total_image_paths}")

    lines.append("\n## Columnas requeridas faltantes\n")
    if missing_cols:
        for col in missing_cols:
            lines.append(f"- `{col}`")
    else:
        lines.append("- No se encontraron columnas requeridas faltantes.")

    lines.append("\n## Valores faltantes en campos importantes\n")
    if not missing_values_df.empty:
        lines.append("| campo | total | faltantes | porcentaje_faltante |")
        lines.append("|---|---:|---:|---:|")
        for _, row in missing_values_df.iterrows():
            lines.append(
                f"| {row['campo']} | {row['total']} | {row['faltantes']} | {row['porcentaje_faltante']}% |"
            )
    else:
        lines.append("- No se pudo evaluar campos importantes.")

    if "tipo_objeto" in df.columns:
        lines.append("\n## Distribución por tipo de objeto\n")
        lines.append(value_counts_md(df["tipo_objeto"].value_counts(dropna=False), "tipo_objeto"))

    if "tipo_superficie" in df.columns:
        lines.append("\n## Distribución por tipo de superficie\n")
        lines.append(value_counts_md(df["tipo_superficie"].value_counts(dropna=False), "tipo_superficie"))

    if "corpus_analisis" in df.columns:
        lines.append("\n## Distribución por corpus de análisis\n")
        lines.append(value_counts_md(df["corpus_analisis"].value_counts(dropna=False), "corpus_analisis"))

    lines.append("\n## Posibles formatos estrechos detectados\n")
    if narrow_df.empty:
        lines.append("- No se detectaron posibles fajas, bandas o formatos estrechos dentro del corpus piloto.")
    else:
        lines.append(f"- Registros detectados para revisión: {len(narrow_df)}")
        preview_cols = [
            col for col in [
                "id_objeto",
                "titulo_original",
                "tipo_objeto",
                "tipo_superficie",
                "motivo_superficie",
            ]
            if col in narrow_df.columns
        ]

        lines.append("")
        lines.append("| id_objeto | titulo_original | tipo_objeto | tipo_superficie | motivo_superficie |")
        lines.append("|---|---|---|---|---|")

        for _, row in narrow_df[preview_cols].head(20).iterrows():
            lines.append(
                f"| {row.get('id_objeto', '')} | {str(row.get('titulo_original', '')).replace('|', '/')} | "
                f"{row.get('tipo_objeto', '')} | {row.get('tipo_superficie', '')} | "
                f"{str(row.get('motivo_superficie', '')).replace('|', '/')} |"
            )

    lines.append("\n## Conclusión preliminar\n")
    lines.append(
        "El corpus piloto queda preparado para una siguiente fase de revisión visual y anotación manual controlada. "
        "Los campos curatoriales provienen de la fuente oficial; los campos visuales, composicionales e iconográficos "
        "se mantienen vacíos hasta su anotación controlada."
    )

    with open(OUTPUT_REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Reporte de validación generado: {OUTPUT_REPORT}")


if __name__ == "__main__":
    build_validation_report()