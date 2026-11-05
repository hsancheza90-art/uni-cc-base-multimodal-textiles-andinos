"""Embeddings versionados de los sistemas de recuperación y operaciones de similitud (solo numpy).

Los embeddings los calcula un paso fuera del flujo (por ejemplo, src/modelos/m2_openclip.py,
que necesita torch) y se guardan como insumo versionado: una matriz .npy de float32, una fila
por imagen, y un índice .csv con el id_global de cada fila. Este módulo los lee y compara sin
torch, para que el flujo y las pruebas no dependan del modelo.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np

from src.utils.archivos import leer_csv

# M2 (OpenCLIP congelado): rutas de sus insumos versionados.
EMBEDDINGS_M2 = Path("data/metadata/m2_openclip_embeddings_v2.npy")
INDICE_M2 = Path("data/metadata/m2_openclip_indice_v2.csv")
MANIFIESTO_M2 = Path("data/metadata/m2_openclip_manifiesto_v2.json")
COLUMNAS_INDICE = ["fila", "id_global", "fuente", "sha256_copia"]
# Decimales con que se guardan los embeddings: absorben las diferencias de redondeo entre
# ejecuciones o dispositivos (del orden de 1e-7), de modo que recalcular no cambie el archivo versionado.
DECIMALES = 6


@dataclass(frozen=True)
class Embeddings:
    ids: list[str]
    matriz: np.ndarray  # (n, d) float32, filas de norma 1

    def posicion(self) -> dict[str, int]:
        return {id_global: fila for fila, id_global in enumerate(self.ids)}


def normalizar_l2(matriz: np.ndarray) -> np.ndarray:
    """Filas de norma 1; una fila nula es un error (no tiene dirección)."""
    normas = np.linalg.norm(matriz, axis=1, keepdims=True)
    if np.any(normas == 0):
        raise ValueError("Hay embeddings nulos: no se pueden normalizar")
    return matriz / normas


def redondear(matriz: np.ndarray) -> np.ndarray:
    return np.round(matriz.astype(np.float64), DECIMALES).astype(np.float32)


def leer_embeddings(raiz: Path, matriz: Path = EMBEDDINGS_M2, indice: Path = INDICE_M2) -> Embeddings:
    """Matriz e índice versionados; comprueba que coincidan fila a fila."""
    datos = np.load(raiz / matriz)
    filas = leer_csv(raiz / indice)
    if datos.ndim != 2 or datos.shape[0] != len(filas):
        raise ValueError(f"{matriz} tiene forma {datos.shape} y {indice} {len(filas)} filas")
    if [int(f["fila"]) for f in filas] != list(range(len(filas))):
        raise ValueError(f"{indice}: la columna fila debe ir de 0 a {len(filas) - 1} sin saltos")
    ids = [f["id_global"] for f in filas]
    if len(set(ids)) != len(ids):
        raise ValueError(f"{indice}: id_global repetido")
    return Embeddings(ids, datos.astype(np.float32))


def subconjunto(embeddings: Embeddings, ids: list[str]) -> Embeddings:
    posicion = embeddings.posicion()
    faltan = [id_ for id_ in ids if id_ not in posicion]
    if faltan:
        raise ValueError(f"Sin embedding: {faltan[:10]}")
    return Embeddings(list(ids), embeddings.matriz[[posicion[id_] for id_ in ids]])


def pares_sobre_umbral(embeddings: Embeddings, umbral: float) -> list[tuple[str, str, float]]:
    """Pares (a, b, coseno) con a < b y coseno >= umbral, de mayor a menor coseno y luego por id."""
    similitud = embeddings.matriz.astype(np.float64) @ embeddings.matriz.astype(np.float64).T
    filas, columnas = np.nonzero(np.triu(similitud >= umbral, k=1))
    pares = []
    for i, j in zip(filas.tolist(), columnas.tolist()):
        a, b = sorted((embeddings.ids[i], embeddings.ids[j]))
        pares.append((a, b, float(similitud[i, j])))
    return sorted(pares, key=lambda par: (-round(par[2], DECIMALES), par[0], par[1]))


def vecino_mas_cercano(embeddings: Embeddings) -> dict[str, str]:
    """Para cada id, el otro id con mayor coseno (empates por id ascendente)."""
    similitud = embeddings.matriz.astype(np.float64) @ embeddings.matriz.astype(np.float64).T
    np.fill_diagonal(similitud, -np.inf)
    orden = np.argsort(np.array(embeddings.ids))  # empates: el id menor primero
    vecinos = {}
    for i, id_global in enumerate(embeddings.ids):
        fila = similitud[i, orden]
        vecinos[id_global] = embeddings.ids[orden[int(np.argmax(fila))]]
    return vecinos
