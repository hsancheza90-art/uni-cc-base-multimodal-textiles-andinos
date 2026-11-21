"""Pruebas del cálculo del efecto mínimo detectable antes del test."""

from __future__ import annotations

import numpy as np

from src.experimento import evaluacion, potencia


def test_con_menos_de_tres_diferencias_no_se_estima() -> None:
    fila = potencia.fila_potencia("H2", [0.1, -0.2], 9, 0.03, 0.95)
    assert fila[2] == "no estimable"


def test_el_emd_de_la_fila_sigue_la_formula_del_protocolo() -> None:
    d = [0.1, -0.05, 0.2, 0.0, 0.15]
    fila = potencia.fila_potencia("H1", d, 30, 0.03, 0.95)
    esperado = evaluacion.efecto_minimo_detectable(float(np.std(d, ddof=1)), 30)
    assert fila[3] == f"{esperado:.3f}"


def test_sin_variacion_no_hay_emd() -> None:
    fila = potencia.fila_potencia("H2", [0.0, 0.0, 0.0], 30, 0.03, 0.95)
    assert fila[6].startswith("no estimable")
