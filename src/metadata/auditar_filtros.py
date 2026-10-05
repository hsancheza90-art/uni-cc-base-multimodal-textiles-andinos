"""Compara el filtro textil vigente con el estado registrado en el inventario MET.

No modifica el corpus: lista los registros cuya decision automatica cambiaria
con las reglas actuales, para que la revision curatorial decida.

Salida: outputs/reports/filtros_comparacion_met_inventario.md
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path

from src.preprocessing.textile_filters import evaluate_met_record

INVENTARIO = "data/processed/corpus_met_textiles_andinos_v1_inventario_base.csv"
CONSOLIDADO = "data/processed/corpus_textiles_andinos_met_cma_v1_consolidado.csv"
REPORTE = "outputs/reports/filtros_comparacion_met_inventario.md"


def leer_csv(ruta: Path) -> list[dict[str, str]]:
    with ruta.open(newline="", encoding="utf-8-sig") as archivo:
        return list(csv.DictReader(archivo))


def como_registro_api(fila: dict[str, str]) -> dict[str, object]:
    """Reconstruye los campos de la API del MET que usa el filtro a partir del inventario."""
    etiquetas = [{"term": t.strip()} for t in (fila.get("etiquetas_originales") or "").split(",") if t.strip()]
    return {
        "title": fila.get("titulo_original"),
        "classification": fila.get("clasificacion_original"),
        "medium": fila.get("material_original"),
        "objectName": fila.get("nombre_objeto_original"),
        "culture": fila.get("cultura"),
        "country": fila.get("pais"),
        "region": fila.get("region"),
        "department": fila.get("departamento_museo"),
        "tags": etiquetas,
        "primaryImage": fila.get("url_imagen"),
    }


def auditar(raiz: Path) -> list[str]:
    inventario = leer_csv(raiz / INVENTARIO)
    en_corpus = {}
    if (raiz / CONSOLIDADO).exists():
        en_corpus = {f["id_fuente"]: f["decision_curacion_final"] for f in leer_csv(raiz / CONSOLIDADO) if f["fuente"] == "MET"}

    cambios = []
    transiciones: Counter[tuple[str, str]] = Counter()
    for fila in inventario:
        nuevo = evaluate_met_record(como_registro_api(fila))
        anterior = fila["estado_curacion"]
        transiciones[(anterior, nuevo["estado_curacion"])] += 1
        if nuevo["estado_curacion"] != anterior:
            cambios.append((fila, anterior, nuevo))

    lineas = [
        "# Comparacion del filtro textil sobre el inventario MET",
        "",
        "Aplica `src/preprocessing/textile_filters.py` (coincidencia por palabra completa y sin penalizar "
        "clasificaciones o materiales mixtos con evidencia textil) a los registros de "
        f"`{INVENTARIO}` y lo compara con el `estado_curacion` registrado. No modifica el corpus.",
        "",
        f"- Registros evaluados: {len(inventario)}",
        f"- Registros con decision distinta: {len(cambios)}",
        "",
        "## Transiciones",
        "",
        "| Estado registrado | Estado con el filtro actual | Registros |",
        "|---|---|---:|",
    ]
    lineas += [f"| {a} | {b} | {n} |" for (a, b), n in sorted(transiciones.items())]

    lineas += ["", "## Registros que cambiarian", ""]
    if cambios:
        lineas += [
            "| id_objeto | Titulo | Clasificacion | Material | Registrado | Filtro actual | Puntaje | En corpus |",
            "|---|---|---|---|---|---|---:|---|",
        ]
        for fila, anterior, nuevo in sorted(cambios, key=lambda c: int(c[0]["id_objeto"])):
            lineas.append(
                f"| {fila['id_objeto']} | {fila['titulo_original']} | {fila['clasificacion_original']} | "
                f"{fila['material_original']} | {anterior} | {nuevo['estado_curacion']} | {nuevo['puntaje_textil']} | "
                f"{en_corpus.get(fila['id_objeto'], 'no')} |"
            )
    else:
        lineas.append("Ninguno.")
    return lineas


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compara el filtro textil vigente con el inventario MET.")
    parser.add_argument("--root", default=".", help="Raiz del repositorio.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    raiz = Path(parse_args(argv).root).resolve()
    lineas = auditar(raiz)
    ruta = raiz / REPORTE
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_bytes(("\n".join(lineas) + "\n").encode("utf-8"))
    print(next(linea for linea in lineas if linea.startswith("- Registros con decision distinta")))
    print(f"Reporte: {ruta}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
