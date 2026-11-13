"""Pruebas de las métricas y de la inferencia del experimento, con datos sintéticos."""

from __future__ import annotations

import math

import pytest

from src.experimento import evaluacion as ev

JUICIOS = {"a": 3, "b": 2, "c": 0, "d": 1, "e": None}


def test_ndcg_vale_uno_con_el_orden_ideal_y_baja_si_un_relevante_queda_fuera() -> None:
    assert ev.ndcg(["a", "b", "d", "c"], JUICIOS, 10) == pytest.approx(1.0)
    esperado = (7 / 1 + 3 / math.log2(3)) / (7 / 1 + 3 / math.log2(3) + 1 / 2)
    assert ev.ndcg(["a", "b", "c", "x"], JUICIOS, 10) == pytest.approx(esperado)
    assert ev.ndcg(["d", "a"], JUICIOS, 1) == pytest.approx(1 / 7)


def test_sin_juicio_cuenta_cero_y_no_evaluable_se_retira_del_ranking() -> None:
    assert ev.ndcg(["x", "a"], JUICIOS, 10) == pytest.approx((7 / math.log2(3)) / ev.dcg([3, 2, 1, 0]))
    assert ev.ndcg(["e", "a", "b", "d"], JUICIOS, 10) == pytest.approx(1.0)
    assert ev.evaluables(["e", "a", "x"], JUICIOS) == ["a", "x"]


def test_consulta_sin_relevantes_no_tiene_ndcg() -> None:
    assert ev.ndcg(["a", "b"], {"a": 0, "b": None}, 10) is None
    assert ev.ndcg(["a"], {}, 10) is None


def test_metricas_secundarias() -> None:
    assert ev.precision(["a", "d", "b", "e", "x"], JUICIOS, 4) == pytest.approx(2 / 4)
    assert ev.rango_reciproco(["c", "e", "d", "b"], JUICIOS) == pytest.approx(1 / 3)
    assert ev.rango_reciproco(["c", "d"], JUICIOS) == 0.0
    assert ev.proporcion_juzgada(["a", "x", "e", "y"], JUICIOS, 4) == pytest.approx(0.5)


def test_retirar_los_aportes_unicos_de_un_sistema() -> None:
    procedencia = {"a": {"M3"}, "b": {"M2", "M3"}, "c": {"azar"}, "d": {"M2"}}
    sin_m3 = ev.sin_aportes_unicos(JUICIOS, procedencia, "M3")
    assert "a" not in sin_m3 and {"b", "c", "d", "e"} <= set(sin_m3)
    assert ev.ndcg(["a", "b"], sin_m3, 10) < ev.ndcg(["a", "b"], JUICIOS, 10)


def test_diferencias_excluye_las_consultas_sin_valor_y_no_depende_del_orden() -> None:
    a, b = {"q2": 0.5, "q1": 0.8, "q3": None}, {"q1": 0.6, "q2": 0.7, "q3": 0.1, "q4": 0.2}
    d, excluidas = ev.diferencias(a, b)
    assert d == pytest.approx([0.2, -0.2]) and excluidas == ["q3", "q4"]


def test_la_permutacion_es_determinista_bilateral_y_se_acerca_al_valor_exacto() -> None:
    d = [0.1 * i for i in range(1, 11)]
    p = ev.permutacion_pareada(d, 10_000, 7)
    assert p == ev.permutacion_pareada(d, 10_000, 7)
    assert p == pytest.approx(ev.permutacion_pareada([-x for x in d], 10_000, 7))
    assert 0 < p < 0.01  # exacto: 2 / 2**10
    assert ev.permutacion_pareada([0.3, -0.3, 0.1, -0.1], 10_000, 7) == pytest.approx(1.0)


def test_t_pareada_reproduce_valores_de_tabla() -> None:
    t, p = ev.t_pareada([1, 2, 3, 4, 5])
    assert t == pytest.approx(3 / (math.sqrt(2.5) / math.sqrt(5)))
    assert p == pytest.approx(0.013236, abs=1e-5)
    # Con 29 grados de libertad, |t| = 2,045230 deja 0,05 en las dos colas.
    assert ev.beta_incompleta(29 / 2, 0.5, 29 / (29 + 2.045230**2)) == pytest.approx(0.05, abs=1e-6)
    assert all(math.isnan(v) for v in ev.t_pareada([0.2, 0.2, 0.2]))


def test_el_intervalo_bootstrap_es_determinista_y_contiene_la_media() -> None:
    d = [0.05, -0.02, 0.1, 0.0, 0.07, 0.03, -0.01, 0.04]
    inferior, superior = ev.intervalo_bootstrap(d, 10_000, 0.95, 11)
    assert (inferior, superior) == ev.intervalo_bootstrap(d, 10_000, 0.95, 11)
    assert inferior < sum(d) / len(d) < superior
    assert ev.intervalo_bootstrap([0.2] * 5, 1000, 0.95, 1) == pytest.approx((0.2, 0.2))


def test_regla_de_decision_del_protocolo() -> None:
    assert ev.decidir(0.05, 0.01, 0.03, 0.05) == ev.SE_SOSTIENE
    assert ev.decidir(0.05, 0.20, 0.03, 0.05) == ev.FAVORABLE
    assert ev.decidir(0.01, 0.20, 0.03, 0.05) == ev.FAVORABLE
    assert ev.decidir(0.01, 0.01, 0.03, 0.05) == ev.NO_SE_SOSTIENE
    assert ev.decidir(-0.05, 0.01, 0.03, 0.05) == ev.NO_SE_SOSTIENE
    assert ev.decidir(0.0, 0.90, 0.03, 0.05) == ev.NO_SE_SOSTIENE


def test_comparar_reune_contraste_comprobacion_intervalo_y_decision() -> None:
    a = {f"q{i:02d}": 0.5 + 0.01 * i for i in range(30)} | {"q99": None}
    b = {f"q{i:02d}": 0.45 for i in range(30)} | {"q99": 0.3}
    c = ev.comparar(a, b, umbral=0.03, alfa=0.05, confianza=0.95, replicas=10_000,
                    semilla_permutacion=1, semilla_bootstrap=2)
    assert c.n == 30 and c.excluidas == ["q99"] and c.decision == ev.SE_SOSTIENE
    assert c.media == pytest.approx(0.195) and c.intervalo[0] < c.media < c.intervalo[1]
    assert c.p_permutacion < 0.05 and c.p_t < 0.05


def test_efecto_minimo_detectable_y_consultas_necesarias() -> None:
    assert ev.efecto_minimo_detectable(0.1, 30) == pytest.approx(0.05115, abs=1e-5)
    assert ev.efecto_minimo_detectable(1.0, 30) == pytest.approx(0.5115, abs=1e-4)
    assert ev.consultas_necesarias(0.1, 0.03) == 88
    assert ev.consultas_necesarias(0.05, 0.03) <= 30 < ev.consultas_necesarias(0.06, 0.03)


def test_el_rango_de_la_desviacion_es_amplio_con_diez_consultas() -> None:
    inferior, superior = ev.rango_desviacion(0.1, 10)
    assert inferior == pytest.approx(0.0688, abs=1e-3) and superior == pytest.approx(0.1826, abs=2e-3)
