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


def exportar(df: pd.DataFrame, root: Path) -> None:
    df = df.copy()

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
        f"- Total revisado: {len(df)}",
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
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    xlsx_path = root / args.xlsx

    df = pd.read_excel(xlsx_path, sheet_name="revision_candidatos")
    exportar(df, root)

    print("Exportacion CMA completada.")
    print(root / "data/metadata/cma_corpus_principal.csv")
    print(root / "data/metadata/cma_corpus_secundario.csv")
    print(root / "data/metadata/cma_descartados.csv")
    print(root / "outputs/reports/cma_curacion_manual_summary.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())