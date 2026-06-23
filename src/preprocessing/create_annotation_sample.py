from __future__ import annotations

from pathlib import Path

import pandas as pd


INPUT_CORPUS = Path("data/processed/corpus_met_textiles_andinos_v1_principal.csv")
OUTPUT_SAMPLE = Path("data/interim/met_anotacion/corpus_met_textiles_andinos_v1_muestra_anotacion.csv")
OUTPUT_REPORT = Path("outputs/reports/annotation_sample_summary.md")


SAMPLE_SIZE = 30
RANDOM_STATE = 42


ANNOTATION_COLUMNS = {
    "color_dominante": "",
    "colores": "",
    "contraste": "",
    "densidad_visual": "",
    "motivos": "",
    "familia_iconografica": "",
    "simetria": "",
    "composicion": "",
    "estado_anotacion": "pendiente",
    "observaciones_anotacion": "",
}


PRIORITY_COLUMNS = [
    "id_registro",
    "id_objeto",
    "titulo_original",
    "cultura",
    "periodo",
    "procedencia",
    "tipo_objeto",
    "tipo_superficie",
    "corpus_analisis",
    "material",
    "material_normalizado",
    "tecnica",
    "descripcion",
    "url",
    "imagen_url",
    "imagen_url_miniatura",
]


def select_balanced_sample(df: pd.DataFrame) -> pd.DataFrame:
    """
    Selecciona una muestra pequeÃ±a y relativamente diversa.
    Primero intenta balancear por tipo_objeto.
    Si no alcanza SAMPLE_SIZE, completa con muestreo aleatorio.
    """
    df = df.copy()

    if len(df) <= SAMPLE_SIZE:
        return df

    if "tipo_objeto" not in df.columns:
        return df.sample(n=SAMPLE_SIZE, random_state=RANDOM_STATE)

    groups = []

    for _, group in df.groupby("tipo_objeto", dropna=False):
        n = min(3, len(group))
        groups.append(group.sample(n=n, random_state=RANDOM_STATE))

    sample = pd.concat(groups, ignore_index=True)

    if len(sample) > SAMPLE_SIZE:
        sample = sample.sample(n=SAMPLE_SIZE, random_state=RANDOM_STATE)

    if len(sample) < SAMPLE_SIZE:
        remaining = df[~df["id_objeto"].astype(str).isin(sample["id_objeto"].astype(str))]
        needed = SAMPLE_SIZE - len(sample)

        if len(remaining) > 0:
            extra = remaining.sample(
                n=min(needed, len(remaining)),
                random_state=RANDOM_STATE,
            )
            sample = pd.concat([sample, extra], ignore_index=True)

    return sample


def reorder_columns(df: pd.DataFrame) -> pd.DataFrame:
    available_priority = [col for col in PRIORITY_COLUMNS if col in df.columns]
    annotation_cols = [col for col in ANNOTATION_COLUMNS.keys() if col in df.columns]
    remaining = [col for col in df.columns if col not in available_priority + annotation_cols]

    return df[available_priority + annotation_cols + remaining]


def write_report(sample: pd.DataFrame, original: pd.DataFrame) -> None:
    OUTPUT_REPORT.parent.mkdir(parents=True, exist_ok=True)

    lines = []

    lines.append("# Resumen de muestra de anotaciÃ³n\n")
    lines.append("## Archivos\n")
    lines.append(f"- Corpus base: `{INPUT_CORPUS}`")
    lines.append(f"- Muestra generada: `{OUTPUT_SAMPLE}`")

    lines.append("\n## Resumen general\n")
    lines.append(f"- Registros en corpus limpio: {len(original)}")
    lines.append(f"- Registros seleccionados para anotaciÃ³n: {len(sample)}")

    if "tipo_objeto" in sample.columns:
        lines.append("\n## DistribuciÃ³n de la muestra por tipo de objeto\n")
        lines.append("| tipo_objeto | conteo |")
        lines.append("|---|---:|")
        for key, value in sample["tipo_objeto"].value_counts(dropna=False).items():
            lines.append(f"| {key} | {value} |")

    if "cultura" in sample.columns:
        lines.append("\n## DistribuciÃ³n de la muestra por cultura\n")
        lines.append("| cultura | conteo |")
        lines.append("|---|---:|")
        for key, value in sample["cultura"].value_counts(dropna=False).items():
            lines.append(f"| {key} | {value} |")

    lines.append("\n## Nota metodolÃ³gica\n")
    lines.append(
        "La muestra de anotaciÃ³n se genera a partir del Corpus MET de Textiles Andinos v1.0. "
        "Su objetivo es iniciar una revisiÃ³n manual controlada de atributos visuales "
        "e iconogrÃ¡ficos, sin modificar la metadata curatorial oficial."
    )

    with open(OUTPUT_REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Reporte generado: {OUTPUT_REPORT}")


def create_annotation_sample() -> None:
    if not INPUT_CORPUS.exists():
        raise FileNotFoundError(f"No existe el archivo: {INPUT_CORPUS}")

    OUTPUT_SAMPLE.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(INPUT_CORPUS)
    sample = select_balanced_sample(df)

    for col, default_value in ANNOTATION_COLUMNS.items():
        sample[col] = default_value

    sample = reorder_columns(sample)
    sample.to_csv(OUTPUT_SAMPLE, index=False, encoding="utf-8-sig")

    print(f"Muestra de anotaciÃ³n generada: {OUTPUT_SAMPLE}")
    print(f"Registros seleccionados: {len(sample)}")

    write_report(sample, df)


if __name__ == "__main__":
    create_annotation_sample()
