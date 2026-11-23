"""Pruebas de las métricas y de la inferencia del experimento, con datos sintéticos."""

from __future__ import annotations

import math

import numpy as np
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


def test_t3_la_regla_separa_las_tres_afirmaciones_de_h1() -> None:
    # Prueba T3 del dictamen: una mejora significativa menor que el umbral ya no se confunde con una nula.
    casos = {
        (0.05, 0.01): (ev.SE_SOSTIENE, True, True),
        (0.02, 0.01): (ev.BAJO_UMBRAL, True, False),
        (-0.05, 0.01): (ev.INFERIOR, True, False),
        (0.05, 0.20): (ev.FAVORABLE, False, True),
        (0.01, 0.20): (ev.FAVORABLE, False, False),
        (0.0, 0.90): (ev.NO_DETECTADA, False, False),
        (-0.02, 0.30): (ev.NO_DETECTADA, False, False),
    }
    for (media, p), (lectura, frente_a_cero, relevante) in casos.items():
        a = ev.decidir(media, p, 0.03, 0.05)
        assert (a.lectura, a.frente_a_cero, a.relevancia_practica) == (lectura, frente_a_cero, relevante), (media, p)
        assert a.sostiene == (lectura == ev.SE_SOSTIENE)
    assert ev.decidir(0.03, 0.049, 0.03, 0.05).sostiene and not ev.decidir(0.03, 0.05, 0.03, 0.05).sostiene


def test_t3_la_permutacion_usa_exactamente_b_replicas_y_su_error_de_monte_carlo() -> None:
    d = [0.02, -0.01, 0.03, 0.0, 0.05, -0.02, 0.01, 0.04, 0.0, 0.02]
    for replicas in (999, 25_001):  # bloques de 10 000 y un resto: sin parada anticipada
        p = ev.permutacion_pareada(d, replicas, 3)
        b = p * (replicas + 1) - 1
        assert b == pytest.approx(round(b)) and 0 <= round(b) <= replicas
    p = ev.permutacion_pareada(d, 100_000, 3)
    assert ev.error_monte_carlo(p, 100_000) == pytest.approx(math.sqrt(p * (1 - p) / 100_000))
    exacta, _ = ev.permutacion_exacta(d)
    assert abs(p - exacta) < 4 * ev.error_monte_carlo(exacta, 100_000)  # converge al valor exacto


def fuerza_bruta(d: list[float]) -> float:
    """p exacta por la definición: todos los vectores de signos, incluidas las diferencias nulas."""
    from itertools import product
    observado = abs(sum(d))
    vectores = list(product((-1, 1), repeat=len(d)))
    return sum(abs(sum(s * x for s, x in zip(v, d))) >= observado - 1e-12 for v in vectores) / len(vectores)


@pytest.mark.parametrize("m", [0, 1, 5, 6, 9])
def test_t2_la_p_exacta_de_h2_coincide_con_la_enumeracion_completa(m: int) -> None:
    # Prueba T2 del dictamen: m diferencias distintas de cero entre ceros, como en H2 (m <= 9).
    distintas = [0.013 * (i + 1) * (-1) ** (i // 2) for i in range(m)]
    d = distintas + [0.0] * (12 - m)
    p, m_obtenido = ev.permutacion_exacta(d)
    assert m_obtenido == m
    assert p == pytest.approx(fuerza_bruta(d))
    assert p >= ev.p_minima(m)
    if m == 0:
        assert p == 1.0


def test_t2_p_minima_y_tolerancia_de_empates() -> None:
    assert ev.p_minima(0) == 1.0 and ev.p_minima(1) == 1.0
    assert ev.p_minima(5) == pytest.approx(0.0625) and ev.p_minima(6) == pytest.approx(0.03125)
    assert ev.permutacion_exacta([0.1] * 5)[0] == pytest.approx(0.0625)  # con m = 5 no se alcanza p < 0,05
    assert ev.permutacion_exacta([0.1] * 6)[0] == pytest.approx(ev.p_minima(6))
    assert ev.permutacion_exacta([0.1] * 9)[0] == pytest.approx(2 / 512)
    p, m = ev.permutacion_exacta([0.1, 0.2, 1e-13, -1e-13, 0.0])
    assert m == 2 and p == pytest.approx(fuerza_bruta([0.1, 0.2]))  # |d| <= 1e-12 cuenta como cero


def opciones(**cambios) -> dict:
    base = dict(umbral=0.03, alfa=0.05, confianza=0.95, replicas_permutacion=10_000, replicas_bootstrap=10_000,
                semilla_permutacion=1, semilla_bootstrap=2)
    return base | cambios


def test_comparar_reune_contraste_comprobacion_intervalo_y_decision() -> None:
    a = {f"q{i:02d}": 0.5 + 0.01 * i for i in range(30)} | {"q99": None}
    b = {f"q{i:02d}": 0.45 for i in range(30)} | {"q99": 0.3}
    c = ev.comparar(a, b, **opciones())
    assert c.n == 30 and c.excluidas == ["q99"] and c.decision == ev.SE_SOSTIENE and c.sostiene
    assert c.media == pytest.approx(0.195) and c.intervalo[0] < c.media < c.intervalo[1]
    assert c.p_permutacion < 0.05 and c.p_t < 0.05 and c.error_mc > 0 and c.replicas == 10_000
    pocas = {f"q{i:02d}": 0.5 + (0.1 if i < 4 else 0.0) for i in range(30)}
    exacta = ev.comparar(pocas, b | {f"q{i:02d}": 0.5 for i in range(30)}, **opciones(), exacta=True)
    assert exacta.m == 4 and exacta.error_mc == 0 and exacta.replicas == 16 and exacta.p_minima == pytest.approx(0.125)
    assert math.isnan(exacta.t) and exacta.decision == ev.FAVORABLE  # con m = 4 la p no baja de 0,125


def test_t1_secuencia_fija_h2_solo_es_confirmatoria_si_h1_se_sostiene() -> None:
    # Prueba T1 del dictamen (control de la tasa de error por familia): sin H1, H2 no tiene veredicto.
    base = {f"q{i:02d}": 0.5 for i in range(30)}
    mejor = {c: v + 0.1 for c, v in base.items()}
    peor = {c: v - 0.1 for c, v in base.items()}
    h2 = ev.comparar({f"q{i:02d}": 0.6 if i < 9 else 0.5 for i in range(30)}, base, **opciones(), exacta=True)
    assert h2.decision == ev.SE_SOSTIENE
    for h1, abierta in ((ev.comparar(mejor, base, **opciones()), True), (ev.comparar(peor, base, **opciones()), False),
                        (ev.comparar({c: v + 0.01 for c, v in base.items()}, base, **opciones()), False)):
        resultado = ev.compuerta(h1, h2)
        assert resultado.sostiene == abierta
        assert resultado.decision == (ev.SE_SOSTIENE if abierta else ev.EXPLORATORIA)
        assert (resultado.media, resultado.p_permutacion, resultado.intervalo) == (h2.media, h2.p_permutacion, h2.intervalo)


def test_t1_la_compuerta_mantiene_la_tasa_de_error_por_familia_bajo_la_nula() -> None:
    # Bajo la hipótesis nula global, la familia solo yerra si H1 se rechaza: la tasa no supera alfa.
    generador = np.random.default_rng(20261123)
    errores = 0
    estudios = 300
    for estudio in range(estudios):
        d1 = generador.normal(0, 0.1, 30)
        d2 = np.concatenate([generador.normal(0, 0.1, 9), np.zeros(21)])
        h1 = ev.comparar({f"q{i}": float(x) for i, x in enumerate(d1)}, {f"q{i}": 0.0 for i in range(30)},
                         **opciones(replicas_permutacion=999, replicas_bootstrap=10, semilla_permutacion=estudio, umbral=0.0))
        h2 = ev.compuerta(h1, ev.comparar({f"q{i}": float(x) for i, x in enumerate(d2)}, {f"q{i}": 0.0 for i in range(30)},
                                          **opciones(replicas_bootstrap=10, umbral=0.0), exacta=True))
        errores += h1.afirmaciones.frente_a_cero or h2.sostiene
    assert errores / estudios <= 0.05 + 3 * math.sqrt(0.05 * 0.95 / estudios)


def test_efecto_minimo_detectable_y_consultas_necesarias() -> None:
    assert ev.efecto_minimo_detectable(0.1, 30) == pytest.approx(0.05115, abs=1e-5)
    assert ev.efecto_minimo_detectable(1.0, 30) == pytest.approx(0.5115, abs=1e-4)
    assert ev.consultas_necesarias(0.1, 0.03) == 88
    assert ev.consultas_necesarias(0.05, 0.03) <= 30 < ev.consultas_necesarias(0.06, 0.03)


def test_el_rango_de_la_desviacion_es_amplio_con_diez_consultas() -> None:
    inferior, superior = ev.rango_desviacion(0.1, 10)
    assert inferior == pytest.approx(0.0688, abs=1e-3) and superior == pytest.approx(0.1826, abs=2e-3)


def test_t1_h1_confirmada_conserva_la_lectura_de_h2_favorable_o_no() -> None:
    base = {f"q{i:02d}": 0.5 for i in range(30)}
    h1 = ev.comparar({c: v + 0.1 for c, v in base.items()}, base, **opciones())
    assert h1.sostiene
    no_favorable = ev.comparar({f"q{i:02d}": 0.4 if i < 2 else 0.5 for i in range(30)}, base, **opciones(), exacta=True)
    favorable = ev.comparar({f"q{i:02d}": 0.6 if i < 3 else 0.5 for i in range(30)}, base, **opciones(), exacta=True)
    assert ev.compuerta(h1, no_favorable).decision == ev.NO_DETECTADA
    assert ev.compuerta(h1, favorable).decision == ev.FAVORABLE  # m = 3: la p no baja de 0,25


def test_t2_exclusiones_ceros_y_b_mayor_que_m() -> None:
    # 9 consultas con bandas (b = 9): 2 dan diferencia cero (b > m) y una queda excluida por no tener relevantes.
    m3 = {f"q{i:02d}": 0.5 for i in range(30)}
    sin_orden = dict(m3)
    for i in range(6):
        m3[f"q{i:02d}"] = 0.5 + 0.05 * (i + 1)
    m3["q08"] = None  # excluida: no entra en n
    c = ev.comparar(m3, sin_orden, **opciones(), exacta=True)
    assert c.n == 29 and c.excluidas == ["q08"] and c.m == 6
    assert c.p_permutacion == pytest.approx(fuerza_bruta([0.05 * (i + 1) for i in range(6)]))
    assert c.p_minima == pytest.approx(2 / 64)