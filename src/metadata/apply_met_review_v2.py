"""Aplica la revisión manual de una fuente (MET, CMA o AIC): del workbook a los CSV revisados.

Uso desde la raíz del repositorio (lo ejecuta también python -m src.flujo):

    python -m src.metadata.apply_met_review_v2

Lee las decisiones del workbook de la fuente (src/utils/fuentes.py) y escribe un CSV por
subconjunto (principal, secundario, descartados), los pendientes (corpus_final = revisar)
y el resumen de movimientos. Un corpus_final vacío conserva la sugerencia automática
(corpus_actual); un valor fuera del vocabulario se envía a pendientes. Devuelve 1 si hay
hallazgos (valores inválidos o identificadores repetidos), para que el flujo se detenga.
"""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

from src.preprocessing.workbook_revision import COLUMNAS as COLUMNAS_SALIDA  # mismas columnas que el workbook
from src.utils.archivos import escribir_csv, escribir_texto
from src.utils.fuentes import DECISIONES, FUENTES, Fuente
from src.utils.libros import leer_hoja

# Estado y destino de la curación que corresponden a cada subconjunto revisado.
CURACION = {
    "principal": ("corpus_principal", "principal"),
    "secundario": ("corpus_secundario", "secundario"),
    "descartados": ("descartado", "exclusion_curatorial"),
}


def normalizar_corpus_final(fila: dict[str, str]) -> str:
    corpus_final = fila.get("corpus_final", "").lower()
    if not corpus_final:
        return fila.get("corpus_actual", "").lower()
    return corpus_final if corpus_final in DECISIONES else "revisar"


def preparar_fila_salida(fila: dict[str, str], corpus_final: str) -> dict[str, str]:
    salida = {columna: fila.get(columna, "") for columna in COLUMNAS_SALIDA}
    salida["corpus_final"] = corpus_final
    if corpus_final in CURACION:
        salida["estado_curacion"], salida["destino_curacion"] = CURACION[corpus_final]
    return salida


def escribir_reporte(raiz: Path, fuente: Fuente, filas_revision: list[dict[str, str]],
                     salidas: dict[str, list[dict[str, str]]], pendientes: list[dict[str, str]],
                     problemas: list[str]) -> None:
    movimientos = Counter()
    for fila in filas_revision:
        corpus_actual = fila.get("corpus_actual", "").lower()
        corpus_final = normalizar_corpus_final(fila)
        if corpus_final != corpus_actual:
            movimientos[(corpus_actual, corpus_final)] += 1

    lineas = [
        f"# Resumen de revision manual {fuente.codigo} v2",
        "",
        f"Este reporte resume la aplicacion de decisiones manuales registradas en `{fuente.workbook}`.",
        "",
        "## Conteos finales",
        "",
        f"- Corpus principal revisado: {len(salidas['principal'])}",
        f"- Corpus secundario revisado: {len(salidas['secundario'])}",
        f"- Descartados revisados: {len(salidas['descartados'])}",
        f"- Pendientes por revisar: {len(pendientes)}",
        "",
        "## Movimientos registrados",
        "",
    ]
    if movimientos:
        lineas += [f"- {origen} -> {destino}: {cantidad}" for (origen, destino), cantidad in sorted(movimientos.items())]
    else:
        lineas.append("- No se registraron movimientos entre corpus.")
    if pendientes:
        lineas += ["", "## Pendientes", ""]
        lineas += [f"- {fila.get('id_fuente', '')}: {fila.get('titulo_original', '')}" for fila in pendientes[:30]]
    if problemas:
        lineas += ["", "## Hallazgos", ""]
        lineas += [f"- {problema}" for problema in problemas]
    escribir_texto(raiz / fuente.reporte, lineas)


def aplicar_revision(raiz: Path, fuente: Fuente) -> int:
    filas_revision = leer_hoja(raiz / fuente.workbook, fuente.hoja, clave="id_fuente")
    salidas: dict[str, list[dict[str, str]]] = {subconjunto: [] for subconjunto in fuente.salidas}
    pendientes: list[dict[str, str]] = []
    problemas: list[str] = []

    vistos = Counter(fila["id_fuente"] for fila in filas_revision)
    for fila in filas_revision:
        corpus_final = normalizar_corpus_final(fila)
        fila_salida = preparar_fila_salida(fila, corpus_final)
        if corpus_final in salidas:
            salidas[corpus_final].append(fila_salida)
        else:
            pendientes.append(fila_salida)
            if corpus_final != "revisar":
                problemas.append(f"{fila['id_fuente']}: corpus_final invalido: {corpus_final}")
    duplicados = sorted(id_fuente for id_fuente, n in vistos.items() if n > 1)
    if duplicados:
        problemas.append(f"IDs duplicados en workbook: {', '.join(duplicados[:20])}")

    for subconjunto, ruta in fuente.salidas.items():
        escribir_csv(raiz / ruta, COLUMNAS_SALIDA, salidas[subconjunto])
    escribir_csv(raiz / fuente.pendientes, COLUMNAS_SALIDA, pendientes)
    escribir_reporte(raiz, fuente, filas_revision, salidas, pendientes, problemas)

    print(f"Principal revisado: {len(salidas['principal'])}")
    print(f"Secundario revisado: {len(salidas['secundario'])}")
    print(f"Descartados revisados: {len(salidas['descartados'])}")
    print(f"Pendientes por revisar: {len(pendientes)}")
    print(f"Reporte: {raiz / fuente.reporte}")
    return 1 if problemas else 0


def main(argv: list[str] | None = None, fuente: str = "MET") -> int:
    parser = argparse.ArgumentParser(description=f"Aplica la revision manual {fuente} v2 desde Excel.")
    parser.add_argument("--root", default=".", help="Raiz del repositorio.")
    args = parser.parse_args(argv)
    return aplicar_revision(Path(args.root).resolve(), FUENTES[fuente])


if __name__ == "__main__":
    raise SystemExit(main())
