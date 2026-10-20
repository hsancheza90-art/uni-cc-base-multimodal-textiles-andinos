"""Crea el workbook maestro de revision manual CMA v2.

Uso: python -m src.preprocessing.create_cma_review_workbook_v2 [--forzar]

Siembra el workbook con las decisiones de la curacion CMA v1 (data/metadata/cma_corpus_*.csv
y cma_descartados.csv, esquema heredado con id_objeto, decision_auditoria...), traducidas
a las columnas comunes (src/preprocessing/workbook_revision.py). Los descartes automaticos
de la curacion v1 (revisor "auto") conservan su origen descarte_automatico_cma.
"""

from __future__ import annotations

from pathlib import Path

from src.preprocessing.workbook_revision import main_fuente
from src.utils.archivos import leer_csv
from src.utils.libros import lector

ENTRADAS = [
    ("principal", "data/metadata/cma_corpus_principal.csv"),
    ("secundario", "data/metadata/cma_corpus_secundario.csv"),
    ("descartados", "data/metadata/cma_descartados.csv"),
]


def construir_filas(raiz: Path) -> list[dict[str, str]]:
    filas = []
    for corpus_actual, ruta in ENTRADAS:
        for fila in leer_csv(raiz / ruta):
            leer = lector(fila)
            filas.append({
                "id_fuente": leer("id_objeto"),
                "corpus_actual": corpus_actual,
                "corpus_final": corpus_actual,
                "decision_revision": "mantener",
                "motivo_revision": leer("motivo_auditoria"),
                "observaciones_revision": leer("observacion_auditoria"),
                "revisor": leer("revisor"),
                "fecha_revision": leer("fecha_revision"),
                "titulo_original": leer("titulo_original"),
                "cultura": leer("cultura") or leer("cultura_manual"),
                "fecha_objeto": leer("periodo") or leer("periodo_manual"),
                "procedencia": leer("cultura"),
                "tipo_objeto": leer("tipo_objeto_manual") or leer("nombre_objeto_original"),
                "material": leer("material_original"),
                "tecnica": leer("tecnica_original"),
                "estado_curacion": leer("decision_auditoria"),
                "destino_curacion": corpus_actual,
                "motivo_curacion": leer("motivo_auditoria"),
                "url_objeto": leer("url_objeto"),
                "url_imagen": leer("url_imagen"),
                "origen_curacion": "descarte_automatico_cma" if leer("revisor") == "auto" else "revision_manual_cma",
            })
    return filas


def main(argv: list[str] | None = None) -> int:
    return main_fuente(argv, "CMA", construir_filas, [])


if __name__ == "__main__":
    raise SystemExit(main())
