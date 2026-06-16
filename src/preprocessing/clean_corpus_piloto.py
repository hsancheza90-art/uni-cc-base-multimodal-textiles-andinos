from __future__ import annotations

from pathlib import Path

import pandas as pd


INPUT_CORPUS = Path("data/metadata/corpus_piloto.csv")

OUTPUT_CLEAN = Path("data/metadata/corpus_piloto_clean.csv")
OUTPUT_SECONDARY = Path("data/metadata/corpus_piloto_secondary.csv")
OUTPUT_DUPLICATES = Path("data/metadata/corpus_piloto_duplicates.csv")
OUTPUT_REPORT = Path("outputs/reports/corpus_piloto_cleaning_summary.md")


FEATHER_TERMS = [
    "feather",
    "feathers",
    "featherwork",
    "pluma",
    "plumas",
]

DUPLICATE_KEY_COLUMNS = [
    "id_objeto",
    "imagen_url",
    "imagen_url_miniatura",
]

SOFT_DUPLICATE_COLUMNS = [
    "titulo_original",
    "cultura",
    "periodo",
    "material",
    "tipo_objeto",
]


def safe_text(value) -> str:
    if pd.isna(value):
        return ""
    return str(value).lower().strip()


def contains_any_text(row: pd.Series, terms: list[str]) -> bool:
    fields = [
        "titulo_original",
        "titulo_es_sugerido",
        "descripcion_oficial",
        "material",
        "material_normalizado",
        "tecnica",
        "tipo_objeto",
        "tipo_superficie",
        "corpus_analisis",
    ]

    combined = " ".join(safe_text(row.get(field, "")) for field in fields)

    return any(term in combined for term in terms)


def is_featherwork(row: pd.Series) -> bool:
    return contains_any_text(row, FEATHER_TERMS)


def detect_duplicates(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Detecta duplicados fuertes por id_objeto o URL de imagen.

    Retorna:
    - df_unique: registros únicos conservados
    - df_duplicates: registros duplicados separados
    """
    df = df.copy()

    df["_duplicate_reason"] = ""

    duplicate_masks = []

    for col in DUPLICATE_KEY_COLUMNS:
        if col in df.columns:
            mask = df[col].notna() & (df[col].astype(str).str.strip() != "") & df.duplicated(subset=[col], keep="first")
            df.loc[mask, "_duplicate_reason"] += f"duplicado_por_{col}; "
            duplicate_masks.append(mask)

    if duplicate_masks:
        final_mask = duplicate_masks[0]
        for mask in duplicate_masks[1:]:
            final_mask = final_mask | mask
    else:
        final_mask = pd.Series(False, index=df.index)

    df_duplicates = df[final_mask].copy()
    df_unique = df[~final_mask].copy()

    df_duplicates = df_duplicates.rename(columns={"_duplicate_reason": "motivo_duplicado"})
    df_unique = df_unique.drop(columns=["_duplicate_reason"], errors="ignore")

    return df_unique, df_duplicates


def detect_soft_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Marca posibles duplicados suaves por título + cultura + periodo + material + tipo.
    No los elimina automáticamente; solo los reporta en observaciones.
    """
    df = df.copy()

    available_cols = [col for col in SOFT_DUPLICATE_COLUMNS if col in df.columns]

    if not available_cols:
        df["posible_duplicado_suave"] = False
        return df

    df["posible_duplicado_suave"] = df.duplicated(subset=available_cols, keep=False)

    return df


def split_secondary(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Separa featherwork/plumas del corpus principal.

    No elimina los registros: los mueve a corpus secundario.
    """
    df = df.copy()

    feather_mask = df.apply(is_featherwork, axis=1)

    df_secondary = df[feather_mask].copy()
    df_clean = df[~feather_mask].copy()

    if not df_secondary.empty:
        df_secondary["motivo_corpus_secundario"] = "materialidad de plumas / featherwork separada del corpus principal inicial"
        df_secondary["corpus_analisis"] = "corpus_secundario_featherwork"
        df_secondary["tipo_superficie"] = "materialidad_plumas"

    return df_clean, df_secondary


def value_counts_md(series: pd.Series, col_name: str, count_name: str = "conteo") -> str:
    lines = [
        f"| {col_name} | {count_name} |",
        "|---|---:|",
    ]

    for key, value in series.items():
        key_text = str(key).replace("|", "/").replace("\n", " ")
        lines.append(f"| {key_text} | {value} |")

    return "\n".join(lines)


def write_report(
    original: pd.DataFrame,
    clean: pd.DataFrame,
    secondary: pd.DataFrame,
    duplicates: pd.DataFrame,
) -> None:
    OUTPUT_REPORT.parent.mkdir(parents=True, exist_ok=True)

    lines = []

    lines.append("# Resumen de limpieza del corpus piloto\n")

    lines.append("## Archivos generados\n")
    lines.append("- `data/metadata/corpus_piloto_clean.csv`")
    lines.append("- `data/metadata/corpus_piloto_secondary.csv`")
    lines.append("- `data/metadata/corpus_piloto_duplicates.csv`")

    lines.append("\n## Resumen general\n")
    lines.append(f"- Registros originales en `corpus_piloto.csv`: {len(original)}")
    lines.append(f"- Registros finales en corpus principal limpio: {len(clean)}")
    lines.append(f"- Registros enviados a corpus secundario: {len(secondary)}")
    lines.append(f"- Registros duplicados separados: {len(duplicates)}")

    if "tipo_objeto" in clean.columns:
        lines.append("\n## Tipo de objeto en corpus limpio\n")
        lines.append(value_counts_md(clean["tipo_objeto"].value_counts(dropna=False), "tipo_objeto"))

    if "corpus_analisis" in clean.columns:
        lines.append("\n## Corpus de análisis en corpus limpio\n")
        lines.append(value_counts_md(clean["corpus_analisis"].value_counts(dropna=False), "corpus_analisis"))

    if not secondary.empty and "tipo_objeto" in secondary.columns:
        lines.append("\n## Registros enviados a corpus secundario por tipo de objeto\n")
        lines.append(value_counts_md(secondary["tipo_objeto"].value_counts(dropna=False), "tipo_objeto"))

    if not duplicates.empty:
        lines.append("\n## Duplicados separados\n")
        preview_cols = [col for col in ["id_objeto", "titulo_original", "motivo_duplicado"] if col in duplicates.columns]
        lines.append("| id_objeto | titulo_original | motivo_duplicado |")
        lines.append("|---|---|---|")
        for _, row in duplicates[preview_cols].head(30).iterrows():
            lines.append(
                f"| {row.get('id_objeto', '')} | "
                f"{str(row.get('titulo_original', '')).replace('|', '/')} | "
                f"{str(row.get('motivo_duplicado', '')).replace('|', '/')} |"
            )

    lines.append("\n## Nota metodológica\n")
    lines.append(
        "Esta fase no elimina registros de la base amplia. Solo depura el corpus piloto principal "
        "para la primera etapa experimental. Los objetos con featherwork o plumas se conservan "
        "en un corpus secundario por presentar una materialidad visual distinta. Los duplicados "
        "se separan para evitar sesgos en los experimentos de representación multimodal."
    )

    with open(OUTPUT_REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Reporte generado: {OUTPUT_REPORT}")


def clean_corpus_piloto() -> None:
    if not INPUT_CORPUS.exists():
        raise FileNotFoundError(f"No existe el archivo: {INPUT_CORPUS}")

    OUTPUT_CLEAN.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_SECONDARY.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_DUPLICATES.parent.mkdir(parents=True, exist_ok=True)

    original = pd.read_csv(INPUT_CORPUS)

    unique_df, duplicates = detect_duplicates(original)
    unique_df = detect_soft_duplicates(unique_df)

    clean, secondary = split_secondary(unique_df)

    clean.to_csv(OUTPUT_CLEAN, index=False, encoding="utf-8-sig")
    secondary.to_csv(OUTPUT_SECONDARY, index=False, encoding="utf-8-sig")
    duplicates.to_csv(OUTPUT_DUPLICATES, index=False, encoding="utf-8-sig")

    print(f"Corpus principal limpio: {OUTPUT_CLEAN} ({len(clean)} registros)")
    print(f"Corpus secundario: {OUTPUT_SECONDARY} ({len(secondary)} registros)")
    print(f"Duplicados separados: {OUTPUT_DUPLICATES} ({len(duplicates)} registros)")

    write_report(original, clean, secondary, duplicates)


if __name__ == "__main__":
    clean_corpus_piloto()