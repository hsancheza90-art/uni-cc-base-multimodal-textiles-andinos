"""Pruebas de las condiciones de buena formación B3 a B7 (capítulo 5, sección 5.4.1)."""

from __future__ import annotations

import pytest

from src.anotacion import buena_formacion as bf
from src.anotacion import congelacion_v21
from src.utils.archivos import leer_csv
from src.utils.config import RAIZ_REPO
from src.utils.vocabulario import leer_vocabulario

VOCABULARIO = leer_vocabulario()


def fila(**campos: str) -> dict[str, str]:
    base = {"id_global": "X:1", "composicion": "bandas", "eje_bandas": "horizontal",
            "secuencia_bandas": "lisa > geometrica > lisa", "motivos": "geometrico", "familia_iconografica": "geometrica"}
    return base | campos


def test_una_fila_bien_formada_no_incumple_nada() -> None:
    assert bf.incumplidas(fila(), VOCABULARIO) == []
    # Casos admitidos por el capitulo 5: una sola banda, bandas contiguas iguales y una laguna aislada.
    assert bf.incumplidas(fila(secuencia_bandas="lisa"), VOCABULARIO) == []
    assert bf.incumplidas(fila(secuencia_bandas="lisa > lisa > laguna > figurativa"), VOCABULARIO) == []
    # Sin bandas en una pieza de paneles, con eje y secuencia en el mismo estado.
    assert bf.incumplidas(fila(composicion="paneles", eje_bandas="ausente", secuencia_bandas="ausente"), VOCABULARIO) == []


@pytest.mark.parametrize(("campos", "condicion"), [
    ({"eje_bandas": "ausente", "secuencia_bandas": "no_observable", "composicion": "paneles"}, "B3"),
    ({"secuencia_bandas": "laguna"}, "B4"),
    ({"secuencia_bandas": "lisa > laguna > laguna > geometrica"}, "B5"),
    ({"eje_bandas": "ausente", "secuencia_bandas": "ausente"}, "B6"),
    ({"motivos": "ausente"}, "B7"),
    ({"familia_iconografica": "ausente"}, "B7"),
])
def test_cada_condicion_detecta_su_incumplimiento(campos: dict[str, str], condicion: str) -> None:
    assert condicion in bf.incumplidas(fila(**campos), VOCABULARIO)


def test_las_celdas_vacias_no_se_evaluan() -> None:
    assert bf.incumplidas(fila(secuencia_bandas="", eje_bandas="", motivos="", familia_iconografica=""), VOCABULARIO) == []


def test_la_anotacion_congelada_cumple_b3_a_b7() -> None:
    ruta = congelacion_v21.ruta_congelada(RAIZ_REPO)
    if not ruta.exists():
        return
    assert all(not ids for ids in bf.revisar(leer_csv(ruta), VOCABULARIO).values())
