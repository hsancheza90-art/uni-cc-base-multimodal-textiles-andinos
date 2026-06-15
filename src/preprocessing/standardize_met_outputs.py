from __future__ import annotations

from pathlib import Path

import pandas as pd


INPUT_CANDIDATES = Path("data/processed/met_candidatos_normalizados.csv")
INPUT_CURATED = Path("data/processed/met_textiles_curado.csv")

OUTPUT_CLEAN = Path("data/processed/met_textiles_pilot_clean.csv")
OUTPUT_REJECTED = Path("data/processed/met_textiles_rejected.csv")
OUTPUT_REPORT = Path("outputs/reports/met_corpus_summary.md")


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

def series_to_markdown_table(series: pd.Series, column_name: str = "valor", count_name: str = "conteo") -> str:
    """
    Convierte un value_counts() en tabla Markdown sin depender de tabulate.
    """
    lines = []
    lines.append(f"| {column_name} | {count_name} |")
    lines.append(f"|---|---:|")

    for index, value in series.items():
        index_text = str(index).replace("|", "/").replace("\n", " ")
        lines.append(f"| {index_text} | {value} |")

    return "\n".join(lines)

def normalize_decision_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Unifica nombres de columnas entre la versión anterior y la versión formal.
    """
    df = df.copy()

    if "decision_filtro" not in df.columns:
        if "estado_curacion" in df.columns:
            df["decision_filtro"] = df["estado_curacion"].apply(
                lambda x: "aceptar" if str(x) in ["aceptado_textil", "revision_manual"] else "rechazar"
            )
        else:
            df["decision_filtro"] = "sin_decision"

    if "estado_filtrado" not in df.columns:
        df["estado_filtrado"] = df["decision_filtro"].apply(
            lambda x: "aceptado" if str(x) == "aceptar" else "rechazado"
        )

    if "puntaje_filtro" not in df.columns:
        if "puntaje_textil" in df.columns:
            df["puntaje_filtro"] = df["puntaje_textil"]
        else:
            df["puntaje_filtro"] = ""

    if "motivo_filtrado" not in df.columns:
        if "motivo_curacion" in df.columns:
            df["motivo_filtrado"] = df["motivo_curacion"]
        else:
            df["motivo_filtrado"] = ""

    if "fase_proceso" not in df.columns:
        df["fase_proceso"] = "fase_filtrado"

    if "corpus" not in df.columns:
        df["corpus"] = "the_met_textiles_pilot"

    return df


def build_clean_and_rejected() -> tuple[pd.DataFrame, pd.DataFrame]:
    if not INPUT_CANDIDATES.exists():
        raise FileNotFoundError(f"No existe el archivo: {INPUT_CANDIDATES}")

    df_candidates = pd.read_csv(INPUT_CANDIDATES)
    df_candidates = normalize_decision_columns(df_candidates)

    if INPUT_CURATED.exists():
        df_curated = pd.read_csv(INPUT_CURATED)
        df_curated = normalize_decision_columns(df_curated)
    else:
        df_curated = df_candidates[df_candidates["decision_filtro"] == "aceptar"].copy()

    clean_ids = set(df_curated["id_objeto"].astype(str)) if "id_objeto" in df_curated.columns else set()

    if clean_ids:
        df_clean = df_candidates[df_candidates["id_objeto"].astype(str).isin(clean_ids)].copy()
        df_rejected = df_candidates[~df_candidates["id_objeto"].astype(str).isin(clean_ids)].copy()
    else:
        df_clean = df_candidates[df_candidates["decision_filtro"] == "aceptar"].copy()
        df_rejected = df_candidates[df_candidates["decision_filtro"] != "aceptar"].copy()

    df_clean = normalize_decision_columns(df_clean)
    df_rejected = normalize_decision_columns(df_rejected)

    df_clean["decision_filtro"] = "aceptar"
    df_clean["estado_filtrado"] = "aceptado"

    df_rejected["decision_filtro"] = "rechazar"
    df_rejected["estado_filtrado"] = "rechazado"

    ensure_parent(OUTPUT_CLEAN)
    ensure_parent(OUTPUT_REJECTED)

    df_clean.to_csv(OUTPUT_CLEAN, index=False, encoding="utf-8-sig")
    df_rejected.to_csv(OUTPUT_REJECTED, index=False, encoding="utf-8-sig")

    print(f"Archivo limpio generado: {OUTPUT_CLEAN}")
    print(f"Registros aceptados: {len(df_clean)}")
    print(f"Archivo de rechazados generado: {OUTPUT_REJECTED}")
    print(f"Registros rechazados: {len(df_rejected)}")

    return df_clean, df_rejected


def write_summary(df_clean: pd.DataFrame, df_rejected: pd.DataFrame) -> None:
    ensure_parent(OUTPUT_REPORT)

    total = len(df_clean) + len(df_rejected)

    lines = []
    lines.append("# Resumen del corpus piloto The Met\n")
    lines.append("## Estado general\n")
    lines.append(f"- Total de registros evaluados: {total}")
    lines.append(f"- Registros aceptados: {len(df_clean)}")
    lines.append(f"- Registros rechazados: {len(df_rejected)}")

    if total > 0:
        lines.append(f"- Tasa de aceptación: {len(df_clean) / total:.2%}")
    else:
        lines.append("- Tasa de aceptación: 0%")

    lines.append("\n## Archivos producidos\n")
    lines.append("- `data/processed/met_textiles_pilot_clean.csv`")
    lines.append("- `data/processed/met_textiles_rejected.csv`")
    lines.append("- `data/metadata/corpus_piloto.csv`")
    lines.append("- `docs/taxonomia_atributos.md`")

    if "clasificacion_original" in df_clean.columns:
        lines.append("\n## Clasificaciones más frecuentes en aceptados\n")
        lines.append(
                series_to_markdown_table(
                    df_clean["clasificacion_original"].value_counts(dropna=False).head(10),
                    column_name="clasificacion_original",
                     count_name="conteo",
                                        )
                                            )

    if "cultura" in df_clean.columns:
        lines.append("\n## Culturas más frecuentes en aceptados\n")
        lines.append(
                    series_to_markdown_table(
                        df_clean["cultura"].value_counts(dropna=False).head(10),
                        column_name="cultura",
                        count_name="conteo",
                    )
                )

    if "motivo_filtrado" in df_rejected.columns:
        lines.append("\n## Ejemplos de motivos de rechazo\n")
        lines.append(
                series_to_markdown_table(
                    df_rejected["motivo_filtrado"].value_counts(dropna=False).head(10),
                    column_name="motivo_filtrado",
                    count_name="conteo",
                )
            )

    lines.append("\n## Nota metodológica\n")
    lines.append(
        "Este reporte resume la fase de estandarización del corpus piloto The Met. "
        "Los archivos previos `met_candidatos_normalizados.csv` y `met_textiles_curado.csv` "
        "se conservan como insumos, mientras que los archivos `met_textiles_pilot_clean.csv` "
        "y `met_textiles_rejected.csv` se utilizan como salidas formales para la fase de filtrado."
    )

    with open(OUTPUT_REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Reporte generado: {OUTPUT_REPORT}")


if __name__ == "__main__":
    clean, rejected = build_clean_and_rejected()
    write_summary(clean, rejected)