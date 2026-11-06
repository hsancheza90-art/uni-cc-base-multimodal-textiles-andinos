"""Pruebas de los sistemas de recuperacion que no necesitan torch (M2: insumos versionados y candidatos)."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest
from PIL import Image

from src.anotacion.corpus_v2 import SALIDA_PRINCIPAL_V2
from src.imagenes.descargar_evaluacion import MANIFIESTO_EVALUACION
from src.modelos.embeddings import (
    EMBEDDINGS_M2,
    INDICE_M2,
    MANIFIESTO_M2,
    Embeddings,
    leer_embeddings,
    normalizar_l2,
    pares_sobre_umbral,
    vecino_mas_cercano,
)
from src.imagenes.descargar_evaluacion import sha256_archivo
from src.modelos.m2_openclip import relleno_cuadrado
from src.utils.archivos import escribir_csv, leer_csv
from src.utils.config import RAIZ_REPO, leer_config_modelos


def test_relleno_cuadrado_centra_la_imagen_sobre_el_color_mediano_del_borde() -> None:
    imagen = Image.new("RGB", (4, 2), (10, 20, 30))
    imagen.putpixel((1, 0), (200, 200, 200))  # un pixel distinto no cambia la mediana del borde
    cuadrado = relleno_cuadrado(imagen)
    assert cuadrado.size == (4, 4)
    assert cuadrado.getpixel((0, 0)) == (10, 20, 30)  # relleno
    assert cuadrado.getpixel((1, 1)) == (200, 200, 200)  # la imagen original, desplazada una fila
    assert relleno_cuadrado(Image.new("RGB", (3, 3))).size == (3, 3)


def test_pares_sobre_umbral_y_vecino_mas_cercano() -> None:
    matriz = normalizar_l2(np.array([[1.0, 0.0], [0.99, 0.141], [0.0, 1.0], [0.0, 1.0]]))
    embeddings = Embeddings(["C:2", "A:1", "B:3", "B:4"], matriz.astype(np.float32))
    pares = pares_sobre_umbral(embeddings, 0.95)
    assert [(a, b) for a, b, _ in pares] == [("B:3", "B:4"), ("A:1", "C:2")]  # de mayor a menor coseno
    assert pares[0][2] == pytest.approx(1.0) and pares[1][2] == pytest.approx(0.99, abs=1e-3)
    vecinos = vecino_mas_cercano(embeddings)
    assert vecinos == {"C:2": "A:1", "A:1": "C:2", "B:3": "B:4", "B:4": "B:3"}


def test_un_embedding_nulo_no_se_normaliza() -> None:
    with pytest.raises(ValueError, match="nulos"):
        normalizar_l2(np.zeros((2, 3)))


def test_indice_y_matriz_deben_coincidir(tmp_path: Path) -> None:
    (tmp_path / EMBEDDINGS_M2).parent.mkdir(parents=True)
    np.save(tmp_path / EMBEDDINGS_M2, np.eye(3, dtype=np.float32))
    escribir_csv(tmp_path / INDICE_M2, ["fila", "id_global", "fuente", "sha256_copia"],
                 [{"fila": "0", "id_global": "A:1", "fuente": "AIC", "sha256_copia": "x"}])
    with pytest.raises(ValueError, match="forma"):
        leer_embeddings(tmp_path)


def test_config_de_m2_es_coherente() -> None:
    m2 = leer_config_modelos()["m2"]
    assert m2["encuadre"] in {"relleno_cuadrado", "centro"} and m2["precision"] == "fp32"
    assert m2["licencia_pesos"] and m2["repositorio_pesos"].startswith("laion/")


# --------------------------------------------------------------------------- insumos versionados


requiere_m2 = pytest.mark.skipif(not (RAIZ_REPO / EMBEDDINGS_M2).exists(), reason="sin embeddings M2 versionados")


@requiere_m2
def test_embeddings_m2_versionados_cubren_las_copias_verificadas() -> None:
    embeddings = leer_embeddings(RAIZ_REPO)
    manifiesto_imagenes = [f for f in leer_csv(RAIZ_REPO / MANIFIESTO_EVALUACION) if f["estado_descarga"] == "ok"]
    assert embeddings.ids == [f["id_global"] for f in manifiesto_imagenes]
    indice = leer_csv(RAIZ_REPO / INDICE_M2)
    assert [f["sha256_copia"] for f in indice] == [f["sha256_copia"] for f in manifiesto_imagenes]
    assert np.allclose(np.linalg.norm(embeddings.matriz.astype(np.float64), axis=1), 1, atol=1e-5)
    assert {f["id_global"] for f in leer_csv(RAIZ_REPO / SALIDA_PRINCIPAL_V2)} <= set(embeddings.ids)


@requiere_m2
def test_manifiesto_m2_registra_el_checkpoint_y_los_hashes_de_sus_salidas() -> None:
    manifiesto = json.loads((RAIZ_REPO / MANIFIESTO_M2).read_text(encoding="utf-8"))
    m2 = leer_config_modelos()["m2"]
    assert (manifiesto["arquitectura"], manifiesto["pesos"], manifiesto["encuadre"]) == (
        m2["arquitectura"], m2["pesos"], m2["encuadre"])
    assert len(manifiesto["sha256_pesos"]) == 64
    assert manifiesto["sha256_embeddings"] == sha256_archivo(RAIZ_REPO / EMBEDDINGS_M2)
    assert manifiesto["sha256_indice"] == sha256_archivo(RAIZ_REPO / INDICE_M2)


