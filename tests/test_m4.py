"""Pruebas de propiedades de M4 (fusión de scores) y de su variante por posiciones, con datos sintéticos."""

from __future__ import annotations

from fractions import Fraction
from itertools import product

import numpy as np
import pytest

from src.modelos import m4_fusion as m4

PESOS = {"M0": 0.25, "M2": 0.5, "M3": 0.25}


def consulta(semilla: int, n: int = 40, sin_evidencia: float = 0.2) -> dict[str, dict[str, float | None]]:
    """Scores sintéticos de una consulta: BM25 con ceros, cosenos y similitudes M3 con huecos."""
    rng = np.random.default_rng(semilla)
    ids = [f"X:{i:03d}" for i in range(n)]
    m3 = [None if rng.random() < sin_evidencia else float(rng.random()) for _ in ids]
    return {"M0": dict(zip(ids, np.maximum(rng.normal(2, 3, n), 0).tolist())),
            "M2": dict(zip(ids, rng.uniform(-0.2, 0.9, n).tolist())),
            "M3": dict(zip(ids, m3))}


def test_la_normalizacion_lleva_a_cero_uno_y_conserva_los_huecos() -> None:
    n = m4.normalizar({"a": 2.0, "b": 5.0, "c": None, "d": 3.5})
    assert n == {"a": 0.0, "b": 1.0, "c": None, "d": pytest.approx(0.5)}
    assert m4.normalizar({"a": 0.7, "b": 0.7, "c": None}) == {"a": 0.0, "b": 0.0, "c": None}
    assert m4.normalizar({"a": None}) == {"a": None}


@pytest.mark.parametrize("semilla", range(20))
def test_las_contribuciones_reconstruyen_el_score_y_los_pesos_efectivos_suman_uno(semilla: int) -> None:
    for i, f in m4.fusionar(consulta(semilla), PESOS).items():
        assert abs(sum(f.contribuciones.values()) - f.score) <= 1e-9
        assert sum(f.pesos.values()) == pytest.approx(1.0)
        assert 0.0 <= f.score <= 1.0 + 1e-12


def test_sin_evidencia_estructural_el_peso_se_reparte_en_proporcion() -> None:
    scores = {"M0": {"a": 1.0, "b": 0.0, "c": 0.5}, "M2": {"a": 0.0, "b": 1.0, "c": 0.5}, "M3": {"a": 1.0, "b": 0.0, "c": None}}
    f = m4.fusionar(scores, PESOS)
    assert f["c"].pesos == {"M0": pytest.approx(1 / 3), "M2": pytest.approx(2 / 3)} and "M3" not in f["c"].contribuciones
    assert f["a"].pesos == PESOS and f["a"].score == pytest.approx(0.25 + 0.25)
    assert f["c"].score == pytest.approx(0.5)


def test_un_par_sin_evidencia_no_recibe_la_similitud_maxima() -> None:
    scores = {"M0": {"a": 0.0, "b": 0.0, "c": 1.0}, "M2": {"a": 0.2, "b": 0.2, "c": 0.9}, "M3": {"a": 1.0, "b": None, "c": 0.0}}
    f = m4.fusionar(scores, PESOS)
    assert f["b"].score < f["a"].score
    solo_m3 = m4.fusionar(scores, {"M0": 0.0, "M2": 0.0, "M3": 1.0})
    assert solo_m3["b"].score == 0.0 and solo_m3["b"].contribuciones == {"M0": 0.0, "M2": 0.0}


@pytest.mark.parametrize("semilla", range(10))
@pytest.mark.parametrize("componente", m4.COMPONENTES)
def test_retirar_un_componente_cambia_el_score_como_predice_la_formula(semilla: int, componente: str) -> None:
    scores = consulta(semilla)
    completa, sin = m4.fusionar(scores, PESOS), m4.fusionar(scores, PESOS, excluir=frozenset({componente}))
    for i, f in completa.items():
        peso = f.pesos.get(componente, 0.0)
        previsto = (f.score - f.contribuciones.get(componente, 0.0)) / (1 - peso)
        assert abs(sin[i].score - previsto) <= 1e-9
        assert componente not in sin[i].contribuciones


def test_la_fusion_no_cambia_con_una_transformacion_afin_positiva_de_un_componente() -> None:
    scores = consulta(3)
    otra = dict(scores) | {"M2": {i: 7.0 * v + 3.0 for i, v in scores["M2"].items()}}
    a, b = m4.fusionar(scores, PESOS), m4.fusionar(otra, PESOS)
    assert all(a[i].score == pytest.approx(b[i].score) for i in a)


def test_con_todo_el_peso_en_un_componente_se_reproduce_su_ranking() -> None:
    scores = consulta(5, sin_evidencia=0.0)
    for componente in m4.COMPONENTES:
        pesos = {c: float(c == componente) for c in m4.COMPONENTES}
        fusion = m4.ordenar({i: f.score for i, f in m4.fusionar(scores, pesos).items()})
        assert [i for i, _ in fusion] == [i for i, _ in m4.ordenar(scores[componente])]


def test_la_fusion_es_determinista_y_los_empates_van_por_id() -> None:
    scores = consulta(8)
    assert m4.fusionar(scores, PESOS) == m4.fusionar({c: dict(reversed(list(s.items()))) for c, s in scores.items()}, PESOS)
    assert m4.ordenar({"b": 0.5, "a": 0.5, "c": 0.9}) == [("c", 0.9), ("a", 0.5), ("b", 0.5)]


def test_errores_de_entrada() -> None:
    with pytest.raises(ValueError):
        m4.fusionar({"M0": {"a": 1.0}, "M2": {"b": 1.0}, "M3": {"a": 1.0}}, PESOS)
    with pytest.raises(ValueError):
        m4.fusionar(consulta(1), {"M0": -0.5, "M2": 1.0, "M3": 0.5})


def test_la_rejilla_normaliza_no_repite_y_tiene_orden_fijo() -> None:
    valores = [0, 0.25, 0.5, 0.75, 1]
    combinaciones = m4.rejilla(valores)
    esperadas = {tuple(Fraction(p) / sum(map(Fraction, c)) for p in map(Fraction, c))
                 for c in product(map(str, valores), repeat=3) if sum(map(Fraction, c)) > 0}
    assert len(combinaciones) == len(esperadas) == len({tuple(c.values()) for c in combinaciones})
    assert all(sum(c.values()) == pytest.approx(1.0) for c in combinaciones)
    assert combinaciones[0] == {"M0": 1.0, "M2": 0.0, "M3": 0.0} and combinaciones[-1] == {"M0": 0.0, "M2": 0.0, "M3": 1.0}
    assert {"M0": pytest.approx(1 / 3), "M2": pytest.approx(1 / 3), "M3": pytest.approx(1 / 3)} in combinaciones
    assert combinaciones == m4.rejilla(list(reversed(valores)))


def test_elegir_toma_el_maximo_y_desempata_hacia_pesos_iguales() -> None:
    a, b, c = {"M0": 1.0, "M2": 0.0, "M3": 0.0}, {"M0": 0.5, "M2": 0.5, "M3": 0.0}, {"M0": 0.0, "M2": 0.5, "M3": 0.5}
    assert m4.elegir([(a, 0.40), (b, 0.45), (c, 0.41)]) == b
    assert m4.elegir([(a, 0.45), (b, 0.45)]) == b
    assert m4.elegir([(c, 0.45), (b, 0.45)]) == b == m4.elegir([(b, 0.45), (c, 0.45)])
    with pytest.raises(ValueError):
        m4.elegir([])


def test_posiciones_reciprocas() -> None:
    rankings = {"M0": ["a", "b", "c"], "M2": ["b", "a", "c"], "M3": ["c", "a", "b"]}
    puntajes = m4.posiciones_reciprocas(rankings)
    assert puntajes["a"] == pytest.approx(1 / 61 + 1 / 62 + 1 / 62)
    assert puntajes["b"] == pytest.approx(1 / 62 + 1 / 61 + 1 / 63)
    assert [i for i, _ in m4.ordenar(puntajes)] == ["a", "b", "c"]
    assert m4.posiciones_reciprocas({"M0": ["a", "b"], "M2": ["b", "a"]}, k=1) == {"a": pytest.approx(5 / 6), "b": pytest.approx(5 / 6)}
    with pytest.raises(ValueError):
        m4.posiciones_reciprocas({"M0": ["a", "b"], "M2": ["a", "c"]})
    with pytest.raises(ValueError):
        m4.posiciones_reciprocas({"M0": ["a", "a"], "M2": ["a", "a"]})
