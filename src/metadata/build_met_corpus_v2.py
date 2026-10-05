from __future__ import annotations

import argparse
import csv
from pathlib import Path


COLUMNAS_V2 = [
    "fuente",
    "id_fuente",
    "id_registro",
    "institucion",
    "titulo_original",
    "titulo_es_sugerido",
    "cultura",
    "periodo",
    "fecha_objeto",
    "procedencia",
    "clasificacion_original",
    "tipo_objeto",
    "tipo_superficie",
    "material",
    "material_normalizado",
    "tecnica",
    "descripcion",
    "url_objeto",
    "url_imagen",
    "ruta_imagen_local",
    "licencia",
    "estado_curacion",
    "destino_curacion",
    "origen_curacion",
    "motivo_curacion",
    "decision_filtro",
    "puntaje_filtro",
    "motivo_filtrado",
    "decision_auditoria",
    "motivo_auditoria",
    "observacion_auditoria",
    "posible_duplicado_suave",
    "estado_metadata",
    "estado_anotacion",
]


def leer_csv(ruta: Path) -> list[dict[str, str]]:
    with ruta.open(newline="", encoding="utf-8-sig") as archivo:
        return list(csv.DictReader(archivo))


def escribir_csv(ruta: Path, filas: list[dict[str, str]]) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=COLUMNAS_V2)
        escritor.writeheader()
        escritor.writerows(filas)


def valor(fila: dict[str, str], campo: str) -> str:
    return (fila.get(campo) or "").strip()


def motivo_principal(fila: dict[str, str]) -> str:
    candidatos = [
        valor(fila, "motivo_curacion_final"),
        valor(fila, "motivo_revision_v2"),
        valor(fila, "motivo_superficie"),
        valor(fila, "motivo_filtrado"),
    ]
    return next((texto for texto in candidatos if texto), "")


def normalizar_fila(
    fila: dict[str, str],
    estado_curacion: str,
    destino_curacion: str,
) -> dict[str, str]:
    return {
        "fuente": valor(fila, "fuente") or "met",
        "id_fuente": valor(fila, "id_objeto"),
        "id_registro": valor(fila, "id_registro") or f"MET-{valor(fila, 'id_objeto')}",
        "institucion": valor(fila, "institucion") or "The Metropolitan Museum of Art",
        "titulo_original": valor(fila, "titulo_original"),
        "titulo_es_sugerido": valor(fila, "titulo_es_sugerido"),
        "cultura": valor(fila, "cultura"),
        "periodo": valor(fila, "periodo"),
        "fecha_objeto": valor(fila, "fecha_objeto"),
        "procedencia": valor(fila, "procedencia"),
        "clasificacion_original": valor(fila, "clasificacion_original"),
        "tipo_objeto": valor(fila, "tipo_objeto"),
        "tipo_superficie": valor(fila, "tipo_superficie"),
        "material": valor(fila, "material") or valor(fila, "material_original"),
        "material_normalizado": valor(fila, "material_normalizado"),
        "tecnica": valor(fila, "tecnica"),
        "descripcion": valor(fila, "descripcion") or valor(fila, "descripcion_oficial"),
        "url_objeto": valor(fila, "url_objeto"),
        "url_imagen": valor(fila, "url_imagen"),
        "ruta_imagen_local": valor(fila, "imagen_local"),
        "licencia": valor(fila, "licencia"),
        "estado_curacion": estado_curacion,
        "destino_curacion": destino_curacion,
        "origen_curacion": valor(fila, "origen_curacion"),
        "motivo_curacion": motivo_principal(fila),
        "decision_filtro": valor(fila, "decision_filtro"),
        "puntaje_filtro": valor(fila, "puntaje_filtro"),
        "motivo_filtrado": valor(fila, "motivo_filtrado"),
        "decision_auditoria": valor(fila, "decision_auditoria"),
        "motivo_auditoria": valor(fila, "motivo_auditoria"),
        "observacion_auditoria": valor(fila, "observacion_auditoria"),
        "posible_duplicado_suave": valor(fila, "posible_duplicado_suave"),
        "estado_metadata": valor(fila, "estado_metadata"),
        "estado_anotacion": valor(fila, "estado_anotacion"),
    }


def escribir_reporte(
    ruta: Path,
    principal: list[dict[str, str]],
    secundario: list[dict[str, str]],
    descartados: list[dict[str, str]],
) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)

    total = len(principal) + len(secundario) + len(descartados)

    lineas = [
        "# Resumen de curacion MET v2",
        "",
        "Fuente: The Metropolitan Museum of Art.",
        "",
        "La version MET v2 reorganiza las salidas curatoriales ya trabajadas en la version v1, sin sobrescribir los archivos historicos. El objetivo es presentar un flujo mas claro, reproducible y legible para la primera entrega del corpus multimodal de textiles andinos.",
        "",
        "## Conteos consolidados",
        "",
        f"- Corpus principal: {len(principal)} registros",
        f"- Corpus secundario: {len(secundario)} registros",
        f"- Registros descartados: {len(descartados)} registros",
        f"- Total revisado: {total} registros",
        "",
        "## Interpretacion curatorial",
        "",
        "El corpus principal agrupa objetos textiles andinos con valor visual suficiente para analisis computacional. El corpus secundario conserva piezas pertinentes pero menos adecuadas para el primer nucleo de analisis, por ejemplo fragmentos, materialidades mixtas o casos que requieren revision posterior. Los descartados mantienen trazabilidad de exclusion para evitar perdida de informacion metodologica.",
        "",
        "## Archivos generados",
        "",
        "- `data/metadata/met_corpus_principal_v2.csv`",
        "- `data/metadata/met_corpus_secundario_v2.csv`",
        "- `data/metadata/met_descartados_v2.csv`",
    ]

    ruta.write_text("\n".join(lineas) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Construye salidas MET v2 a partir de los archivos curatoriales MET v1."
    )
    parser.add_argument("--root", default=".", help="Raiz del repositorio.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    raiz = Path(args.root).resolve()

    ruta_principal = raiz / "data/processed/corpus_met_textiles_andinos_v1_principal.csv"
    ruta_secundario = raiz / "data/processed/corpus_met_textiles_andinos_v1_complementario.csv"
    ruta_descartados = raiz / "data/processed/corpus_met_textiles_andinos_v1_exclusiones_curatoriales.csv"

    principal_base = leer_csv(ruta_principal)
    secundario_base = leer_csv(ruta_secundario)
    descartados_base = leer_csv(ruta_descartados)

    principal = [
        normalizar_fila(fila, "corpus_principal", "principal")
        for fila in principal_base
    ]
    secundario = [
        normalizar_fila(fila, "corpus_secundario", "secundario")
        for fila in secundario_base
    ]
    descartados = [
        normalizar_fila(fila, "descartado", "exclusion_curatorial")
        for fila in descartados_base
    ]

    escribir_csv(raiz / "data/metadata/met_corpus_principal_v2.csv", principal)
    escribir_csv(raiz / "data/metadata/met_corpus_secundario_v2.csv", secundario)
    escribir_csv(raiz / "data/metadata/met_descartados_v2.csv", descartados)
    escribir_reporte(
        raiz / "outputs/reports/met_resumen_curacion_v2.md",
        principal,
        secundario,
        descartados,
    )

    print(f"Corpus principal MET v2: {len(principal)}")
    print(f"Corpus secundario MET v2: {len(secundario)}")
    print(f"Descartados MET v2: {len(descartados)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())