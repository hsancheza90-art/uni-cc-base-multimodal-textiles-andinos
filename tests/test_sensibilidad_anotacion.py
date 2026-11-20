"""Pruebas del análisis de sensibilidad de M3 a la revisión de la anotación."""

from __future__ import annotations

from src.experimento import sensibilidad_anotacion as s


def fila(id_global: str, composicion: str) -> dict[str, str]:
    base = {a: "ausente" for a in s.ATRIBUTOS_M3 + ["eje_bandas"]}
    return {"id_global": id_global, **base, "composicion": composicion, "observaciones_anotacion": id_global}


def test_trasladar_mueve_cada_anotacion_a_la_imagen_que_describe() -> None:
    ids = list(s.DESPLAZADAS) + ["AIC:1"]
    filas = [fila(i, f"comp_de_{i}") for i in ids]
    salida = {f["id_global"]: f for f in s.trasladar(filas)}
    for origen, destino in s.DESPLAZADAS.items():
        assert salida[destino]["composicion"] == f"comp_de_{origen}"
        assert salida[destino]["observaciones_anotacion"] == destino  # solo se mueven los atributos
    assert salida["AIC:1"]["composicion"] == "comp_de_AIC:1"


def test_las_desplazadas_forman_una_permutacion() -> None:
    assert sorted(s.DESPLAZADAS) == sorted(s.DESPLAZADAS.values())


def test_spearman_de_rankings_iguales_e_invertidos() -> None:
    a = ["x", "y", "z", "w"]
    assert abs(s.spearman(a, a) - 1) < 1e-12
    assert abs(s.spearman(a, a[::-1]) + 1) < 1e-12
