from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


ACEPTAR_PRINCIPAL = {"aceptar_principal"}
ACEPTAR_SECUNDARIO = {"aceptar_secundario"}


def clasificar_subconjunto(decision: str) -> str:
    decision = str(decision).strip()
    if decision in ACEPTAR_PRINCIPAL:
        return "principal"
    if decision in ACEPTAR_SECUNDARIO:
        return "secundario"
    return "descartado"


def incluir_en_corpus(decision: str) -> str:
    decision = str(decision).strip()
    return "si" if decision in ACEPTAR_PRINCIPAL | ACEPTAR_SECUNDARIO else "no"


def mapear_candidato_a_revision(row: pd.Series) -> dict[str, str]:
    title = str(row.get("title", ""))
    culture = str(row.get("culture", ""))
    source_id = str(row.get("source_id", "")).strip()

    if "spindle" in title.lower():
        decision = "descartar_no_textil"
        motivo = "herramienta_textil"
        observacion = "Huso/spindle: herramienta asociada al tejido, no pieza textil analizable como superficie visual."
        tipo = "no_textil"
    else:
        decision = "descartar_no_andino"
        motivo = "fuera_alcance"
        observacion = f"Falso positivo fuera del ambito andino: {culture}"
        tipo = "no_textil"

    return {
        "fuente": row.get("source", "Cleveland Museum of Art"),
        "id_objeto": source_id,
        "numero_acceso": row.get("accession_number", ""),
        "titulo_original": title,
        "cultura": culture,
        "periodo": row.get("creation_date", ""),
        "clasificacion_original": row.get("classification", ""),
        "nombre_objeto_original": row.get("classification", ""),
        "tecnica_original": row.get("technique", ""),
        "material_original": row.get("medium", ""),
        "descripcion_original": row.get("description", ""),
        "url_objeto": row.get("url", ""),
        "url_imagen": row.get("image_url", ""),
        "terminos_andinos_auto": row.get("andean_terms", ""),
        "terminos_textiles_auto": row.get("textile_terms", ""),
        "decision_sugerida": row.get("curation_status", ""),
        "decision_auditoria": decision,
        "motivo_auditoria": motivo,
        "observacion_auditoria": observacion,
        "incluir_en_corpus": "no",
        "subconjunto_corpus": "descartado",
        "calidad_visual": "no_aplica",
        "tipo_objeto_manual": tipo,
        "cultura_manual": "",
        "periodo_manual": "",
        "notas_iconograficas": "",
        "notas_tecnicas": "",
        "revisor": "auto",
        "fecha_revision": "",
    }


def agregar_descartes_automaticos(df: pd.DataFrame, root: Path, candidates_csv: str) -> tuple[pd.DataFrame, int]:
    candidates_path = root / candidates_csv
    if not candidates_path.exists():
        return df, 0

    candidatos = pd.read_csv(candidates_path, dtype=str).fillna("")
    ids_revisados = set(df["id_objeto"].fillna("").astype(str).str.strip())
    faltantes = candidatos[
        ~candidatos["source_id"].fillna("").astype(str).str.strip().isin(ids_revisados)
    ]

    if faltantes.empty:
        return df, 0

    extras = pd.DataFrame([mapear_candidato_a_revision(row) for _, row in faltantes.iterrows()])
    return pd.concat([df, extras], ignore_index=True), len(extras)


def exportar(df: pd.DataFrame, root: Path, candidates_csv: str) -> None:
    df = df.copy()
    registros_manual = len(df)

    df, descartes_auto = agregar_descartes_automaticos(df, root, candidates_csv)

    df["decision_auditoria"] = df["decision_auditoria"].fillna("").astype(str).str.strip()
    pendientes = df[df["decision_auditoria"] == ""]

    if len(pendientes) > 0:
        raise ValueError(f"Hay {len(pendientes)} registros sin decision_auditoria.")

    df["incluir_en_corpus"] = df["decision_auditoria"].apply(incluir_en_corpus)
    df["subconjunto_corpus"] = df["decision_auditoria"].apply(clasificar_subconjunto)

    columnas_salida = [
        "fuente",
        "id_objeto",
        "numero_acceso",
        "titulo_original",
        "cultura",
        "periodo",
        "clasificacion_original",
        "nombre_objeto_original",
        "tecnica_original",
        "material_original",
        "descripcion_original",
        "url_objeto",
        "url_imagen",
        "terminos_andinos_auto",
        "terminos_textiles_auto",
        "decision_sugerida",
        "decision_auditoria",
        "motivo_auditoria",
        "observacion_auditoria",
        "incluir_en_corpus",
        "subconjunto_corpus",
        "calidad_visual",
        "tipo_objeto_manual",
        "cultura_manual",
        "periodo_manual",
        "notas_iconograficas",
        "notas_tecnicas",
        "revisor",
        "fecha_revision",
    ]

    columnas_existentes = [col for col in columnas_salida if col in df.columns]
    df_salida = df[columnas_existentes]

    output_dir = root / "data/metadata"
    report_dir = root / "outputs/reports"
    output_dir.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)

    principal = df_salida[df_salida["subconjunto_corpus"] == "principal"]
    secundario = df_salida[df_salida["subconjunto_corpus"] == "secundario"]
    descartados = df_salida[df_salida["subconjunto_corpus"] == "descartado"]

    principal.to_csv(output_dir / "cma_corpus_principal.csv", index=False, encoding="utf-8-sig")
    secundario.to_csv(output_dir / "cma_corpus_secundario.csv", index=False, encoding="utf-8-sig")
    descartados.to_csv(output_dir / "cma_descartados.csv", index=False, encoding="utf-8-sig")

    conteos_decision = df["decision_auditoria"].value_counts().sort_index()
    reporte = [
        "# Resumen de curacion manual CMA",
        "",
        f"- Registros en workbook manual: {registros_manual}",
        f"- Descartes automaticos agregados: {descartes_auto}",
        f"- Total exportado: {len(df)}",
        f"- Corpus principal: {len(principal)}",
        f"- Corpus secundario: {len(secundario)}",
        f"- Descartados: {len(descartados)}",
        "",
        "## Conteo por decision_auditoria",
        "",
    ]
    reporte.extend(f"- {idx}: {val}" for idx, val in conteos_decision.items())

    (report_dir / "cma_curacion_manual_summary.md").write_text(
        "\n".join(reporte) + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Exporta corpus CMA curado desde Excel.")
    parser.add_argument("--root", default=".", help="Raiz del repositorio.")
    parser.add_argument(
        "--xlsx",
        default="data/metadata/cma_revision_manual_textiles_andinos.xlsx",
        help="Workbook de curacion manual CMA.",
    )
    parser.add_argument(
        "--candidates-csv",
        default="data/metadata/cma_andes_textiles_candidates.csv",
        help="CSV normalizado CMA usado para registrar descartes automaticos no incluidos en el workbook.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    xlsx_path = root / args.xlsx

    df = pd.read_excel(xlsx_path, sheet_name="revision_candidatos", dtype=str)
    exportar(df, root, args.candidates_csv)

    print("Exportacion CMA completada.")
    print(root / "data/metadata/cma_corpus_principal.csv")
    print(root / "data/metadata/cma_corpus_secundario.csv")
    print(root / "data/metadata/cma_descartados.csv")
    print(root / "outputs/reports/cma_curacion_manual_summary.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())