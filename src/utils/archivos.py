"""Lectura y escritura de los archivos de texto del corpus (CSV, informes y JSONL).

Todas las etapas leen y escriben con las mismas convenciones, para que los archivos
versionados se regeneren byte a byte:

- lectura en UTF-8 aceptando BOM (algunos CSV se editaron en Excel);
- escritura en UTF-8 y con finales de línea LF (ver .gitattributes);
- columnas en el orden que fija cada etapa, nunca en el orden del diccionario.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path


def leer_csv(ruta: Path, recortar: bool = True) -> list[dict[str, str]]:
    """Filas del CSV como diccionarios.

    recortar=True quita espacios en blanco y convierte vacíos en "": es lo habitual.
    recortar=False devuelve el texto tal como está en el archivo; lo usan las etapas que
    luego recortan campo por campo o que deben conservar el texto de la fuente.
    """
    with ruta.open(newline="", encoding="utf-8-sig") as archivo:
        filas = list(csv.DictReader(archivo))
    if not recortar:
        return filas
    return [{clave: (valor or "").strip() for clave, valor in fila.items()} for fila in filas]


def leer_csv_con_columnas(ruta: Path) -> tuple[list[str], list[dict[str, str]]]:
    """Encabezado y filas (sin recortar), para auditar el esquema de un archivo."""
    with ruta.open(newline="", encoding="utf-8-sig") as archivo:
        lector = csv.DictReader(archivo)
        return list(lector.fieldnames or []), list(lector)


def indexar(filas: list[dict[str, str]], clave: str) -> dict[str, dict[str, str]]:
    """Índice por clave; un identificador repetido en un insumo es un error, no se resuelve en silencio."""
    indice: dict[str, dict[str, str]] = {}
    for fila in filas:
        if fila[clave] in indice:
            raise ValueError(f"Identificador repetido en insumo: {clave}={fila[clave]}")
        indice[fila[clave]] = fila
    return indice


def escribir_csv(ruta: Path, columnas: list[str], filas: list[dict[str, str]], codificacion: str = "utf-8") -> None:
    """CSV con LF. codificacion="utf-8-sig" (con BOM) solo para los CSV heredados de CMA v1."""
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("w", newline="", encoding=codificacion) as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=columnas, lineterminator="\n")
        escritor.writeheader()
        escritor.writerows(filas)


def escribir_texto(ruta: Path, lineas: list[str]) -> None:
    """Informe de texto: líneas unidas con LF y un salto final."""
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_bytes(("\n".join(lineas) + "\n").encode("utf-8"))


def escribir_jsonl(ruta: Path, registros: list[dict], ordenar_claves: bool = True) -> None:
    """Respuestas crudas de una API, una por línea, con LF en cualquier sistema."""
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("w", newline="", encoding="utf-8") as archivo:
        for registro in registros:
            archivo.write(json.dumps(registro, ensure_ascii=False, sort_keys=ordenar_claves) + "\n")
