"""Pruebas de M0 (BM25), M1 (color y textura), M3 (descriptor estructural) y los rankings de desarrollo."""

from __future__ import annotations

from collections import Counter
from itertools import product

import numpy as np
import pytest

from src.experimento import rankings
from src.experimento.snapshot import SALIDA_CONSULTAS, SALIDA_PARTICIONES
from src.modelos import m0_texto, m1_vision
from src.modelos import m3_estructura as m3
from src.utils.archivos import leer_csv
from src.utils.config import RAIZ_REPO, leer_config_anotacion, leer_config_modelos
from src.utils.vocabulario import leer_vocabulario

CONFIG = leer_config_modelos()


# --------------------------------------------------------------------------- M0


def test_m0_excluye_la_descripcion_plantilla_de_met_y_normaliza() -> None:
    met = {"fuente": "MET", "titulo_original": "Tunic Fragment", "descripcion": "Título oficial: Tunic"}
    cma = {"fuente": "CMA", "titulo_original": "Túnica", "descripcion": "Bands of birds"}
    assert "oficial" not in m0_texto.documento(met, CONFIG["m0"])
    assert m0_texto.documento(cma, CONFIG["m0"]) == "tunica bands of birds"
    assert m0_texto.tokenizar("Bands of birds, 1-2", 3) == ["bands", "birds"]


def test_bm25_premia_los_terminos_raros_y_compartidos() -> None:
    documentos = {"a": ["tunic", "birds", "birds"], "b": ["tunic", "fish"], "c": ["tunic", "mantle"]}
    indice = m0_texto.Bm25(documentos, 1.2, 0.75)
    assert indice.puntuar(["birds"], "a") > 0 and indice.puntuar(["birds"], "b") == 0
    assert indice.idf["birds"] > indice.idf["tunic"]  # tunic esta en todos
    assert indice.puntuar(["birds", "tunic"], "a") > indice.puntuar(["tunic"], "a")


# --------------------------------------------------------------------------- M1


def test_lbp_de_una_imagen_plana_es_uniforme_con_ocho_unos() -> None:
    codigos = m1_vision.lbp_riu2(np.full((5, 5), 40.0))
    assert set(codigos[1:-1, 1:-1].ravel()) == {8} and set(codigos[0]) == {-1}


def test_disimilitud_m1_es_cero_consigo_misma_y_esta_en_cero_uno() -> None:
    config = CONFIG["m1"]
    lab = np.zeros((20, 20, 3))
    lab[..., 0] = 50
    otra = lab.copy()
    otra[..., 1] = 60  # mas rojo
    mascara = np.ones((20, 20), dtype=bool)
    a = np.concatenate([m1_vision.histograma_color(lab, mascara, config), m1_vision.histograma_textura(lab, mascara)])
    b = np.concatenate([m1_vision.histograma_color(otra, mascara, config), m1_vision.histograma_textura(otra, mascara)])
    assert a[:m1_vision.dimension_color(config)].sum() == pytest.approx(1.0)
    assert m1_vision.disimilitud(a, a, config) == 0
    assert 0 < m1_vision.disimilitud(a, b, config) <= 1


# --------------------------------------------------------------------------- M3


ALFABETO = ["lisa", "geometrica", "figurativa", "mixta", "no_determinada"]


def test_la_forma_canonica_es_invariante_a_la_reversion() -> None:
    w = ("lisa", "geometrica", "figurativa")
    assert m3.canonizar(w, ALFABETO) == m3.canonizar(m3.reverso(w), ALFABETO) == w


def test_burnside_cuatro_posiciones_dos_simbolos_dan_diez_orbitas() -> None:
    # (2^4 + 2^2) / 2 = 10: ejemplo verificable del informe 05 de la auditoria.
    palabras = set(product(["a", "b"], repeat=4))
    assert len({m3.canonizar(w, ["a", "b"]) for w in palabras}) == 10


def test_el_control_sin_orden_no_distingue_lo_que_las_adyacencias_si() -> None:
    aabb, abab = tuple("aabb"), tuple("abab")
    assert m3.histograma_tipos(aabb) == m3.histograma_tipos(abab)
    assert m3.histograma_adyacencias(aabb) != m3.histograma_adyacencias(abab)
    assert m3.histograma_adyacencias(aabb) == m3.histograma_adyacencias(m3.reverso(aabb))


def test_distancia_de_palabras_simetrica_invariante_y_con_lagunas_enmascaradas() -> None:
    a, b = ("lisa", "geometrica", "lisa"), ("geometrica", "figurativa")
    assert m3.distancia_palabras(a, b) == m3.distancia_palabras(b, a)
    assert m3.distancia_palabras(a, m3.reverso(b)) == m3.distancia_palabras(a, b)
    assert m3.distancia_palabras(("lisa", "laguna", "geometrica"), ("lisa", "geometrica")) == 0
    assert m3.distancia_palabras((), ()) == 0 and m3.distancia_palabras((), a) == 1
    assert m3.histograma_adyacencias(("lisa", "laguna", "geometrica")) == {}  # la laguna corta el par


def test_orden_de_repeticion_y_alfabeto_coinciden_con_la_configuracion() -> None:
    assert m3.ORDEN_REPETICION == leer_config_anotacion()["acuerdo"]["orden"]["repeticion"]
    assert ALFABETO == [c for c in leer_vocabulario()["secuencia_bandas"].codigos if c != m3.LAGUNA]


def test_periodo_exacto() -> None:
    assert m3.periodo(tuple("ababab")) == 2
    assert m3.periodo(tuple("abc")) == 3  # p* = l: no hay repeticion


def fila(**campos: str) -> dict[str, str]:
    base = {"composicion": "bandas", "secuencia_bandas": "lisa > geometrica > lisa", "borde": "si", "centro": "no",
            "simetria": "bilateral", "repeticion": "si", "motivos": "geometrico; ave", "familia_iconografica": "zoomorfa"}
    return base | campos


def test_disimilitud_mixta_simetrica_acotada_y_sin_evidencia() -> None:
    pesos = CONFIG["m3"]["pesos"]
    i, j = m3.descriptor(fila()), m3.descriptor(fila(composicion="paneles", repeticion="parcial", motivos="ave"))
    ij, ji = m3.comparar(i, j, pesos), m3.comparar(j, i, pesos)
    assert ij.disimilitud == pytest.approx(ji.disimilitud) and 0 < ij.disimilitud <= 1
    assert m3.comparar(i, i, pesos).disimilitud == 0
    nada = {c: "no_observable" for c in fila()}
    vacio = m3.comparar(m3.descriptor(nada), i, pesos)
    assert vacio.disimilitud is None and vacio.cobertura == 0  # sin evidencia estructural, no similitud maxima


def test_la_suma_de_contribuciones_reconstruye_la_disimilitud_y_la_intervencion_es_exacta() -> None:
    pesos = dict(CONFIG["m3"]["pesos"])
    i, j = m3.descriptor(fila()), m3.descriptor(fila(composicion="paneles", secuencia_bandas="lisa > figurativa"))
    comparacion = m3.comparar(i, j, pesos)
    assert sum(comparacion.contribuciones.values()) == pytest.approx(comparacion.disimilitud, abs=1e-12)
    # Retirar un bloque recalcula D con la formula: los demas bloques, renormalizados.
    d = m3.distancias_por_bloque(i, j)
    sin_composicion = m3.comparar(i, j, pesos | {"composicion": 0.0})
    esperado = sum(pesos[b] * d[b] for b in d if b != "composicion") / sum(pesos[b] for b in d if b != "composicion")
    assert sin_composicion.disimilitud == pytest.approx(esperado, abs=1e-12)


def test_m3_sin_orden_ignora_el_orden_de_las_bandas() -> None:
    pesos = CONFIG["m3"]["pesos"]
    i = m3.descriptor(fila(secuencia_bandas="lisa > lisa > geometrica > geometrica"))
    j = m3.descriptor(fila(secuencia_bandas="lisa > geometrica > lisa > geometrica"))
    assert m3.comparar(i, j, pesos, sin_orden=True).disimilitud == 0
    assert m3.comparar(i, j, pesos).disimilitud > 0


# --------------------------------------------------------------------------- rankings de desarrollo


requiere_snapshot = pytest.mark.skipif(not (RAIZ_REPO / rankings.SALIDA_RANKINGS).exists(), reason="sin rankings")


@requiere_snapshot
def test_rankings_solo_de_desarrollo_sin_el_grupo_de_la_consulta_y_ordenados() -> None:
    filas = leer_csv(RAIZ_REPO / rankings.SALIDA_RANKINGS)
    consultas = {c["consulta"]: c for c in leer_csv(RAIZ_REPO / SALIDA_CONSULTAS)}
    grupo = {f["id_global"]: f["grupo"] for f in leer_csv(RAIZ_REPO / SALIDA_PARTICIONES)}
    assert {consultas[f["consulta"]]["particion"] for f in filas} == {"desarrollo"}
    assert all(grupo[f["id_global"]] != consultas[f["consulta"]]["grupo"] for f in filas)
    por_ranking: dict[tuple[str, str], list[dict[str, str]]] = {}
    for f in filas:
        por_ranking.setdefault((f["sistema"], f["consulta"]), []).append(f)
    assert Counter(s for s, _ in por_ranking) == {s: 10 for s in rankings.SISTEMAS}
    for lista in por_ranking.values():
        assert [int(f["rango"]) for f in lista] == list(range(1, len(lista) + 1))
        puntajes = [float(f["score"]) for f in lista]
        assert puntajes == sorted(puntajes, reverse=True)
