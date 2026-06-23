from __future__ import annotations

from pathlib import Path

import pandas as pd


INPUT_XLSX = Path("data/metadata/corpus_piloto_annotation_sheet.xlsx")
OUTPUT_ANNOTATED_CSV = Path("data/metadata/corpus_piloto_annotation_sample_annotated.csv")
OUTPUT_REPORT = Path("outputs/reports/annotation_validation_report.md")


CONTROLLED_VOCABULARY = {
    "color_dominante": {
        "rojo", "azul", "amarillo", "negro", "blanco", "marron", "beige",
        "verde", "naranja", "multicolor", "no_determinado",
    },
    "contraste": {
        "alto", "medio", "bajo", "no_determinado",
    },
    "densidad_visual": {
        "alta", "media", "baja", "no_determinado",
    },
    "familia_iconografica": {
        "geometrica", "zoomorfa", "antropomorfa", "fitomorfa",
        "abstracta", "mixta", "no_determinada",
    },
    "simetria": {
        "bilateral", "radial", "repetitiva", "sin_simetria_clara",
        "no_determinado",
    },
    "composicion": {
        "central", "modular", "franjas", "cuadricula", "paneles",
        "repeticion_lineal", "composicion_libre", "no_determinado",
    },
    "estado_anotacion": {
        "pendiente", "anotado", "revisar", "descartar",
    },
}


ANNOTATION_FIELDS = [
    "color_dominante",
    "colores",
    "contraste",
    "densidad_visual",
    "motivos",
    "familia_iconografica",
    "simetria",
    "composicion",
    "estado_anotacion",
    "observaciones_anotacion",
]


def clean_value(value) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip()


def validate_controlled_values(df: pd.DataFrame) -> list[dict]:
    errors = []

    for field, allowed_values in CONTROLLED_VOCABULARY.items():
        if field not in df.columns:
            continue

        for idx, value in df[field].items():
            value_clean = clean_value(value)

            if value_clean == "":
                continue

            if value_clean not in allowed_values:
                errors.append(
                    {
                        "fila_excel": idx + 2,
                        "id_objeto": df.loc[idx, "id_objeto"] if "id_objeto" in df.columns else "",
                        "campo": field,
                        "valor": value_clean,
                        "valores_permitidos": "; ".join(sorted(allowed_values)),
                    }
                )

    return errors


def count_annotation_status(df: pd.DataFrame) -> dict:
    if "estado_anotacion" not in df.columns:
        return {}

    return df["estado_anotacion"].fillna("sin_estado").astype(str).str.strip().value_counts().to_dict()


def count_completed_fields(df: pd.DataFrame) -> pd.DataFrame:
    rows = []

    for field in ANNOTATION_FIELDS:
        if field not in df.columns:
            continue

        filled = df[field].fillna("").astype(str).str.strip().ne("").sum()
        rows.append(
            {
                "campo": field,
                "completados": int(filled),
                "total": len(df),
                "porcentaje": round((filled / len(df)) * 100, 2) if len(df) else 0,
            }
        )

    return pd.DataFrame(rows)


def write_report(df: pd.DataFrame, errors: list[dict], field_summary: pd.DataFrame) -> None:
    OUTPUT_REPORT.parent.mkdir(parents=True, exist_ok=True)

    status_counts = count_annotation_status(df)

    lines = []
    lines.append("# Reporte de validación de anotaciones\n")

    lines.append("## Archivos\n")
    lines.append(f"- Excel leído: `{INPUT_XLSX}`")
    lines.append(f"- CSV exportado: `{OUTPUT_ANNOTATED_CSV}`")

    lines.append("\n## Resumen general\n")
    lines.append(f"- Registros en la muestra: {len(df)}")
    lines.append(f"- Errores de vocabulario controlado: {len(errors)}")

    lines.append("\n## Estado de anotación\n")
    if status_counts:
        lines.append("| estado_anotacion | conteo |")
        lines.append("|---|---:|")
        for key, value in status_counts.items():
            lines.append(f"| {key} | {value} |")
    else:
        lines.append("- No existe la columna `estado_anotacion`.")

    lines.append("\n## Campos completados\n")
    if not field_summary.empty:
        lines.append("| campo | completados | total | porcentaje |")
        lines.append("|---|---:|---:|---:|")
        for _, row in field_summary.iterrows():
            lines.append(
                f"| {row['campo']} | {row['completados']} | {row['total']} | {row['porcentaje']}% |"
            )

    lines.append("\n## Errores de vocabulario\n")
    if errors:
        lines.append("| fila_excel | id_objeto | campo | valor | valores_permitidos |")
        lines.append("|---:|---|---|---|---|")
        for err in errors:
            lines.append(
                f"| {err['fila_excel']} | {err['id_objeto']} | {err['campo']} | "
                f"{err['valor']} | {err['valores_permitidos']} |"
            )
    else:
        lines.append("- No se encontraron errores de vocabulario controlado.")

    lines.append("\n## Conclusión\n")
    lines.append(
        "La validación permite revisar si las anotaciones iniciales son consistentes. "
        "Si no hay errores de vocabulario y los primeros registros anotados son claros, "
        "se puede continuar con el resto de la muestra."
    )

    with open(OUTPUT_REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Reporte generado: {OUTPUT_REPORT}")


def validate_annotations() -> None:
    if not INPUT_XLSX.exists():
        raise FileNotFoundError(f"No existe el archivo: {INPUT_XLSX}")

    df = pd.read_excel(INPUT_XLSX, sheet_name="Anotacion")

    # Limpiar espacios en campos de texto.
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].apply(clean_value)

    OUTPUT_ANNOTATED_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_ANNOTATED_CSV, index=False, encoding="utf-8-sig")

    errors = validate_controlled_values(df)
    field_summary = count_completed_fields(df)

    print(f"CSV anotado exportado: {OUTPUT_ANNOTATED_CSV}")
    print(f"Registros leídos: {len(df)}")
    print(f"Errores de vocabulario: {len(errors)}")

    write_report(df, errors, field_summary)


if __name__ == "__main__":
    validate_annotations()