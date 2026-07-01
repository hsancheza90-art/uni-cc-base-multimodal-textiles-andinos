from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


COLUMNAS_SALIDA = [
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


def normalizar_texto(valor: object) -> str:
    if pd.isna(valor):
        return ""
    return str(valor).strip()


def mapear_revision(row: pd.Series) -> dict[str, str]:
    corpus_final = normalizar_texto(row.get("corpus_final"))
    decision_revision = normalizar_texto(row.get("decision_revision"))
    motivo_revision = normalizar_texto(row.get("motivo_revision"))
    observaciones = normalizar_texto(row.get("observaciones_revision"))

    if corpus_final == "principal":
        decision_auditoria = "aceptar_principal"
        incluir = "si"
    elif corpus_final == "secundario":
        decision_auditoria = "aceptar_secundario"
        incluir = "si"
    else:
        decision_auditoria = "descartar_revision_v2"
        incluir = "no"

    return {
        "fuente": "Cleveland Museum of Art",
        "id_objeto": normalizar_texto(row.get("id_fuente")),
        "numero_acceso": "",
        "titulo_original": normalizar_texto(row.get("titulo_original")),
        "cultura": normalizar_texto(row.get("cultura")),
        "periodo": normalizar_texto(row.get("fecha_objeto")),
        "clasificacion_original": normalizar_texto(row.get("tipo_objeto")),
        "nombre_objeto_original": normalizar_texto(row.get("tipo_objeto")),
        "tecnica_original": normalizar_texto(row.get("tecnica")),
        "material_original": normalizar_texto(row.get("material")),
        "descripcion_original": "",
        "url_objeto": normalizar_texto(row.get("url_objeto")),
        "url_imagen": normalizar_texto(row.get("url_imagen")),
        "decision_auditoria": decision_auditoria,
        "motivo_auditoria": motivo_revision or decision_revision,
        "observacion_auditoria": observaciones,
        "incluir_en_corpus": incluir,
        "subconjunto_corpus": corpus_final,
        "calidad_visual": "",
        "tipo_objeto_manual": normalizar_texto(row.get("tipo_objeto")),
        "cultura_manual": normalizar_texto(row.get("cultura")),
        "periodo_manual": normalizar_texto(row.get("fecha_objeto")),
        "notas_iconograficas": "",
        "notas_tecnicas": "",
        "revisor": normalizar_texto(row.get("revisor")),
        "fecha_revision": normalizar_texto(row.get("fecha_revision")),
    }


def validar(df: pd.DataFrame) -> None:
    requeridas = ["id_fuente", "corpus_actual", "corpus_final", "decision_revision"]
    faltantes = [col for col in requeridas if col not in df.columns]
    if faltantes:
        raise ValueError(f"Faltan columnas requeridas: {faltantes}")

    permitidos = {"principal", "secundario", "descartados", "revisar"}
    invalidos = sorted(set(df["corpus_final"].dropna().astype(str).str.strip()) - permitidos)
    if invalidos:
        raise ValueError(f"Valores no permitidos en corpus_final: {invalidos}")

    pendientes = df[df["corpus_final"].astype(str).str.strip() == "revisar"]
    if len(pendientes) > 0:
        print(f"Advertencia: {len(pendientes)} registros quedan como revisar y se exportaran a pendientes.")


def exportar(df: pd.DataFrame, root: Path) -> None:
    validar(df)

    df = df.copy()
    df["corpus_final"] = df["corpus_final"].fillna("").astype(str).str.strip()

    rows = pd.DataFrame([mapear_revision(row) for _, row in df.iterrows()])
    rows = rows[COLUMNAS_SALIDA]

    output_dir = root / "data/metadata"
    report_dir = root / "outputs/reports"
    output_dir.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)

    principal = rows[rows["subconjunto_corpus"] == "principal"]
    secundario = rows[rows["subconjunto_corpus"] == "secundario"]
    descartados = rows[rows["subconjunto_corpus"] == "descartados"]
    pendientes = rows[~rows["subconjunto_corpus"].isin(["principal", "secundario", "descartados"])]

    principal.to_csv(output_dir / "cma_corpus_principal_revisado.csv", index=False, encoding="utf-8-sig")
    secundario.to_csv(output_dir / "cma_corpus_secundario_revisado.csv", index=False, encoding="utf-8-sig")
    descartados.to_csv(output_dir / "cma_descartados_revisado.csv", index=False, encoding="utf-8-sig")
    pendientes.to_csv(output_dir / "cma_pendientes_revision_v2.csv", index=False, encoding="utf-8-sig")

    movimientos = df[df["corpus_actual"] != df["corpus_final"]]

    reporte = [
        "# Resumen de revision manual CMA v2",
        "",
        f"- Total en workbook: {len(df)}",
        f"- Corpus principal revisado: {len(principal)}",
        f"- Corpus secundario revisado: {len(secundario)}",
        f"- Descartados revisados: {len(descartados)}",
        f"- Pendientes: {len(pendientes)}",
        f"- Movimientos manuales: {len(movimientos)}",
        "",
        "## Conteo por corpus_final",
        "",
    ]

    conteos = df["corpus_final"].value_counts().sort_index()
    reporte.extend(f"- {idx}: {val}" for idx, val in conteos.items())

    if len(movimientos) > 0:
        reporte.extend(["", "## Movimientos", ""])
        for _, row in movimientos.iterrows():
            reporte.append(
                f"- {normalizar_texto(row.get('id_fuente'))}: "
                f"{normalizar_texto(row.get('corpus_actual'))} -> {normalizar_texto(row.get('corpus_final'))}"
            )

    (report_dir / "cma_resumen_revision_manual_v2.md").write_text(
        "\n".join(reporte) + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Aplica workbook maestro de revision manual CMA v2.")
    parser.add_argument("--root", default=".", help="Raiz del repositorio.")
    parser.add_argument(
        "--xlsx",
        default="data/metadata/cma_revision_manual_v2.xlsx",
        help="Workbook CMA v2.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    xlsx_path = root / args.xlsx

    df = pd.read_excel(xlsx_path, sheet_name="revision_cma_v2", dtype=str)
    exportar(df, root)

    print("Revision CMA v2 aplicada.")
    print(root / "data/metadata/cma_corpus_principal_revisado.csv")
    print(root / "data/metadata/cma_corpus_secundario_revisado.csv")
    print(root / "data/metadata/cma_descartados_revisado.csv")
    print(root / "outputs/reports/cma_resumen_revision_manual_v2.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())