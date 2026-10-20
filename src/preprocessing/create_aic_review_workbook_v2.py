"""Crea el workbook maestro de revision manual AIC v2.

Uso: python -m src.preprocessing.create_aic_review_workbook_v2 [--forzar]

Cada candidato (data/metadata/aic_andes_textiles_candidates.csv) llega con la sugerencia
automatica en corpus_actual (principal, secundario o descartados) y corpus_final = revisar,
salvo las herramientas textiles, que se descartan automaticamente como en CMA (revisor
"auto"). La estructura del workbook es comun a las fuentes (src/preprocessing/workbook_revision.py).
"""

from __future__ import annotations

from pathlib import Path

from src.preprocessing.workbook_revision import main_fuente
from src.utils.archivos import leer_csv

CANDIDATOS = "data/metadata/aic_andes_textiles_candidates.csv"
NOTAS = ["Las herramientas textiles (revisor = auto) se descartaron automaticamente, como en CMA."]


def es_herramienta(candidato: dict[str, str]) -> bool:
    return candidato["estado_filtro"] == "excluido_no_textil" and "herramienta textil" in candidato["motivo_filtro"]


def construir_filas(raiz: Path) -> list[dict[str, str]]:
    filas = []
    for c in leer_csv(raiz / CANDIDATOS, recortar=False):
        automatico = es_herramienta(c)
        filas.append({
            "id_fuente": c["id_fuente"],
            "corpus_actual": c["sugerencia_corpus"],
            "corpus_final": "descartados" if automatico else "revisar",
            "decision_revision": "descartar" if automatico else "revisar",
            "motivo_revision": "herramienta_textil" if automatico else "",
            "observaciones_revision": "Descarte automatico: herramienta de hilado o tejido." if automatico else "",
            "revisor": "auto" if automatico else "",
            "fecha_revision": c["fecha_descarga"] if automatico else "",
            "titulo_original": c["titulo_original"],
            "cultura": c["cultura"],
            "fecha_objeto": c["fecha_objeto"],
            "procedencia": c["procedencia"],
            "tipo_objeto": c["tipo_objeto"],
            "tipo_superficie": c["tipo_superficie"],
            "material": c["material"],
            "tecnica": c["tecnicas"],
            "estado_curacion": c["estado_filtro"],
            "destino_curacion": c["sugerencia_corpus"],
            "motivo_curacion": c["motivo_sugerencia"],
            "url_objeto": c["url_objeto"],
            "url_imagen": c["url_imagen_miniatura"] or c["url_imagen"],
            "licencia": c["licencia_imagen"],
            "origen_curacion": "descarte_automatico_aic" if automatico else "revision_manual_aic",
        })
    return filas


def main(argv: list[str] | None = None) -> int:
    return main_fuente(argv, "AIC", construir_filas, NOTAS)


if __name__ == "__main__":
    raise SystemExit(main())
