"""Aplica la revisión manual de CMA: del workbook a los CSV revisados por subconjunto.

Uso desde la raíz del repositorio (lo ejecuta también python -m src.flujo):

    python -m src.metadata.apply_cma_review_v2

Lee las decisiones de data/metadata/cma_revision_manual_v2.xlsx y escribe un CSV por
subconjunto, los pendientes y el resumen (rutas en src/utils/fuentes.py).

A diferencia de MET y AIC (apply_met_review_v2.py), los CSV de CMA conservan el esquema
de la curación CMA v1 (id_objeto, decision_auditoria, incluir_en_corpus...) y su
codificación con BOM, porque el consolidado v1 se construyó sobre ese esquema. Unificarlo
con MET y AIC cambia salidas versionadas y se decidirá con el consolidado v2.
"""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

from src.utils.archivos import escribir_csv, escribir_texto
from src.utils.fuentes import DECISIONES, FUENTES
from src.utils.libros import leer_hoja

CMA = FUENTES["CMA"]

COLUMNAS_SALIDA = [
    "fuente", "id_objeto", "numero_acceso", "titulo_original", "cultura", "periodo",
    "clasificacion_original", "nombre_objeto_original", "tecnica_original", "material_original",
    "descripcion_original", "url_objeto", "url_imagen", "decision_auditoria", "motivo_auditoria",
    "observacion_auditoria", "incluir_en_corpus", "subconjunto_corpus", "calidad_visual",
    "tipo_objeto_manual", "cultura_manual", "periodo_manual", "notas_iconograficas",
    "notas_tecnicas", "revisor", "fecha_revision",
]


def mapear_revision(fila: dict[str, str]) -> dict[str, str]:
    """Fila del workbook v2 en el esquema heredado de CMA v1."""
    corpus_final = fila.get("corpus_final", "")
    if corpus_final == "principal":
        decision_auditoria, incluir = "aceptar_principal", "si"
    elif corpus_final == "secundario":
        decision_auditoria, incluir = "aceptar_secundario", "si"
    else:
        # Descartados y pendientes comparten el valor heredado; el subconjunto los distingue.
        decision_auditoria, incluir = "descartar_revision_v2", "no"
    return {
        "fuente": "Cleveland Museum of Art",
        "id_objeto": fila.get("id_fuente", ""),
        "numero_acceso": "",
        "titulo_original": fila.get("titulo_original", ""),
        "cultura": fila.get("cultura", ""),
        "periodo": fila.get("fecha_objeto", ""),
        "clasificacion_original": fila.get("tipo_objeto", ""),
        "nombre_objeto_original": fila.get("tipo_objeto", ""),
        "tecnica_original": fila.get("tecnica", ""),
        "material_original": fila.get("material", ""),
        "descripcion_original": "",
        "url_objeto": fila.get("url_objeto", ""),
        "url_imagen": fila.get("url_imagen", ""),
        "decision_auditoria": decision_auditoria,
        "motivo_auditoria": fila.get("motivo_revision", "") or fila.get("decision_revision", ""),
        "observacion_auditoria": fila.get("observaciones_revision", ""),
        "incluir_en_corpus": incluir,
        "subconjunto_corpus": corpus_final,
        "calidad_visual": "",
        "tipo_objeto_manual": fila.get("tipo_objeto", ""),
        "cultura_manual": fila.get("cultura", ""),
        "periodo_manual": fila.get("fecha_objeto", ""),
        "notas_iconograficas": "",
        "notas_tecnicas": "",
        "revisor": fila.get("revisor", ""),
        "fecha_revision": fila.get("fecha_revision", ""),
    }


def validar(filas: list[dict[str, str]]) -> None:
    requeridas = ["id_fuente", "corpus_actual", "corpus_final", "decision_revision"]
    faltantes = [c for c in requeridas if filas and c not in filas[0]]
    if faltantes:
        raise ValueError(f"Faltan columnas requeridas: {faltantes}")
    invalidos = sorted({f["corpus_final"] for f in filas if f["corpus_final"]} - set(DECISIONES))
    if invalidos:
        raise ValueError(f"Valores no permitidos en corpus_final: {invalidos}")
    pendientes = sum(f["corpus_final"] == "revisar" for f in filas)
    if pendientes:
        print(f"Advertencia: {pendientes} registros quedan como revisar y se exportaran a pendientes.")


def exportar(filas: list[dict[str, str]], raiz: Path) -> None:
    validar(filas)
    salida = [mapear_revision(f) for f in filas]
    por_subconjunto = {nombre: [f for f in salida if f["subconjunto_corpus"] == nombre] for nombre in CMA.salidas}
    pendientes = [f for f in salida if f["subconjunto_corpus"] not in CMA.salidas]
    for nombre, ruta in CMA.salidas.items():
        escribir_csv(raiz / ruta, COLUMNAS_SALIDA, por_subconjunto[nombre], codificacion="utf-8-sig")
    escribir_csv(raiz / CMA.pendientes, COLUMNAS_SALIDA, pendientes, codificacion="utf-8-sig")

    movimientos = [f for f in filas if f["corpus_actual"] != f["corpus_final"]]
    reporte = [
        "# Resumen de revision manual CMA v2",
        "",
        f"- Total en workbook: {len(filas)}",
        f"- Corpus principal revisado: {len(por_subconjunto['principal'])}",
        f"- Corpus secundario revisado: {len(por_subconjunto['secundario'])}",
        f"- Descartados revisados: {len(por_subconjunto['descartados'])}",
        f"- Pendientes: {len(pendientes)}",
        f"- Movimientos manuales: {len(movimientos)}",
        "",
        "## Conteo por corpus_final",
        "",
    ]
    reporte += [f"- {decision}: {n}" for decision, n in sorted(Counter(f["corpus_final"] for f in filas).items())]
    if movimientos:
        reporte += ["", "## Movimientos", ""]
        reporte += [f"- {f['id_fuente']}: {f['corpus_actual']} -> {f['corpus_final']}" for f in movimientos]
    escribir_texto(raiz / CMA.reporte, reporte)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Aplica el workbook de revisión manual CMA v2.")
    parser.add_argument("--root", default=".", help="Raíz del repositorio.")
    args = parser.parse_args(argv)
    raiz = Path(args.root).resolve()
    exportar(leer_hoja(raiz / CMA.workbook, CMA.hoja, clave="id_fuente"), raiz)
    print("Revision CMA v2 aplicada.")
    for ruta in (*CMA.revisados, CMA.reporte):
        print(raiz / ruta)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
