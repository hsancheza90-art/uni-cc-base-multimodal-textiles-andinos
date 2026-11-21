"""Pruebas de la selección de los pesos de M4 en desarrollo (decisión R28)."""

from __future__ import annotations

from src.experimento import pesos_m4


def test_el_ranking_de_m4_sigue_al_unico_componente_con_peso() -> None:
    scores = {
        "M0": {"a": 0.0, "b": 1.0, "c": 0.5},
        "M2": {"a": 0.9, "b": 0.1, "c": 0.5},
        "M3": {"a": None, "b": 0.2, "c": 0.8},
    }
    assert pesos_m4.ranking_m4(scores, {"M0": 0.0, "M2": 1.0, "M3": 0.0}) == ["a", "c", "b"]
    assert pesos_m4.ranking_m4(scores, {"M0": 1.0, "M2": 0.0, "M3": 0.0}) == ["b", "c", "a"]


def test_evaluar_cuenta_como_cero_los_no_juzgados_y_promedia_la_proporcion_juzgada() -> None:
    scores = {"Q1": {"M0": {"a": 1.0, "b": 0.0}, "M2": {"a": 1.0, "b": 0.0}, "M3": {"a": 1.0, "b": 0.0}}}
    juicios = {"Q1": {"a": 3}}
    ndcg, juzgada = pesos_m4.evaluar(scores, juicios, {"M0": 1 / 3, "M2": 1 / 3, "M3": 1 / 3}, k=2)
    assert abs(ndcg - 1.0) < 1e-12
    assert abs(juzgada - 0.5) < 1e-12
