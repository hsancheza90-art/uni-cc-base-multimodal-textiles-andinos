"""dHash de las copias de evaluación (fuera del flujo: lee las imágenes locales).

Uso desde la raíz del repositorio:

    python -m src.imagenes.dhash_evaluacion

Calcula el hash perceptual por diferencias (64 bits, el mismo de src/imagenes/descargar_imagenes.py
que usa el consolidado v1) de cada copia de evaluación descargada (manifiesto
data/metadata/imagenes_evaluacion_manifiesto_v2.csv, estado ok), después de verificar su SHA-256.
Escribe el insumo versionado data/metadata/imagenes_evaluacion_dhash_v2.csv, que el flujo usa
para proponer candidatos a duplicado (src/grupos/grupos.py).
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image

from src.imagenes.descargar_evaluacion import MANIFIESTO_EVALUACION, imagenes_verificadas
from src.imagenes.descargar_imagenes import dhash
from src.utils.archivos import escribir_csv

SALIDA_DHASH = "data/metadata/imagenes_evaluacion_dhash_v2.csv"
COLUMNAS = ["id_global", "fuente", "sha256_copia", "dhash"]


def calcular(raiz: Path) -> int:
    filas, errores = imagenes_verificadas(raiz)
    if errores:
        print(f"{len(errores)} copias sin verificar; no se calcula el dHash:")
        for error in errores[:20]:
            print(f"- {error}")
        return 1
    salida = []
    for fila in filas:
        with Image.open(raiz / fila["ruta_copia_evaluacion"]) as imagen:
            salida.append({"id_global": fila["id_global"], "fuente": fila["fuente"],
                           "sha256_copia": fila["sha256_copia"], "dhash": dhash(imagen)})
    escribir_csv(raiz / SALIDA_DHASH, COLUMNAS, salida)
    print(f"dHash de {len(salida)} copias de evaluacion ({MANIFIESTO_EVALUACION}) -> {SALIDA_DHASH}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="dHash de las copias de evaluacion (insumo de los grupos v2).")
    parser.add_argument("--root", default=".", help="Raiz del repositorio.")
    return calcular(Path(parser.parse_args(argv).root).resolve())


if __name__ == "__main__":
    raise SystemExit(main())
