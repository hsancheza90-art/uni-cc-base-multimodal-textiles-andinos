"""Lectura y escritura de los archivos tabulares del corpus.

Todas las etapas leen y escriben CSV con las mismas convenciones, para que los
archivos versionados se regeneren byte a byte:

- lectura en UTF-8 aceptando BOM (algunos CSV se editaron en Excel);
- escritura en UTF-8 sin BOM y con finales de linea LF (ver .gitattributes);
- columnas en el orden que fija cada etapa, nunca en el orden del diccionario.
"""

from __future__ import annotations

import csv
from pathlib import Path


def leer_csv(ruta: Path, recortar: bool = True) -> list[dict[str, str]]:
    """Filas del CSV como diccionarios.

    recortar=True quita espacios en blanco y convierte vacios en "": es lo que usan el
    consolidado y el puntaje de aptitud. Las etapas MET v2 y los generadores de workbooks
    leen el texto tal cual (recortar=False) para no alterar lo que escribio la fuente.
    """
    with ruta.open(newline="", encoding="utf-8-sig") as archivo:
        filas = list(csv.DictReader(archivo))
    if not recortar:
        return filas
    return [{clave: (valor or "").strip() for clave, valor in fila.items()} for fila in filas]


def indexar(filas: list[dict[str, str]], clave: str) -> dict[str, dict[str, str]]:
    """Indice por clave; un identificador repetido en un insumo es un error, no se resuelve en silencio."""
    indice: dict[str, dict[str, str]] = {}
    for fila in filas:
        if fila[clave] in indice:
            raise ValueError(f"Identificador repetido en insumo: {clave}={fila[clave]}")
        indice[fila[clave]] = fila
    return indice


def escribir_csv(ruta: Path, columnas: list[str], filas: list[dict[str, str]]) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=columnas, lineterminator="\n")
        escritor.writeheader()
        escritor.writerows(filas)


def escribir_texto(ruta: Path, lineas: list[str]) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_bytes(("\n".join(lineas) + "\n").encode("utf-8"))
