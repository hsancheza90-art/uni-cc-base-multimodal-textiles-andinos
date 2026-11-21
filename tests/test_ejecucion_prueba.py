"""Pruebas de la ejecución única del test, sin ejecutar ningún sistema sobre las consultas de prueba.

La evaluación se ensaya con la partición de desarrollo y sus juicios; la tarea T1, con consultas
hipotéticas y vectores de texto sintéticos en un directorio temporal. Ninguna prueba muestra
métricas: solo comprueba la estructura y las propiedades del cálculo.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from src.experimento import ejecucion_prueba as ep
from src.experimento import evaluacion
from src.experimento.consultas_t1 import SALIDA_T1
from src.experimento.pesos_m4 import leer_juicios
from src.experimento.rankings import SALIDA_RANKINGS
from src.experimento.snapshot import SALIDA_PARTICIONES
from src.anotacion.corpus_v2 import SALIDA_PRINCIPAL_V2
from src.modelos.embeddings import EMBEDDINGS_M2, INDICE_M2
from src.utils.archivos import escribir_csv, leer_csv
from src.utils.config import RAIZ_REPO
from tests.insumos import copiar_insumos


def test_el_repositorio_solo_espera_la_aprobacion_del_protocolo() -> None:
    problemas = ep.comprobar(RAIZ_REPO)
    assert problemas and all("no esta aprobado" in p for p in problemas), problemas
    assert not ep.aprobado(RAIZ_REPO)


def test_sin_aprobacion_no_se_ejecuta_ningun_sistema_sobre_la_prueba() -> None:
    if ep.aprobado(RAIZ_REPO):
        pytest.skip("Con el protocolo aprobado esta prueba abriria el test: no se ejecuta.")
    assert ep.main(["--root", str(RAIZ_REPO), "--rankings"]) == 1
    assert not (RAIZ_REPO / ep.RANKINGS_PRUEBA).exists() and not (RAIZ_REPO / ep.RANKINGS_T1).exists()
    assert ep.main(["--root", str(RAIZ_REPO), "--comprobar"]) == 1


@pytest.fixture(scope="module")
def ensayo_desarrollo() -> dict:
    """Cálculo completo sobre la partición de desarrollo, en memoria."""
    rk = ep.leer_rankings(RAIZ_REPO / SALIDA_RANKINGS)
    return ep.calcular(RAIZ_REPO, "desarrollo", rk, leer_juicios(RAIZ_REPO))


def test_h3_reconstruccion_e_intervencion_se_cumplen(ensayo_desarrollo: dict) -> None:
    h3 = ensayo_desarrollo["h3"]
    assert h3["resultados"] == 10 * 10 and h3["cumple"]
    assert h3["reconstruccion"] <= 1e-9 and h3["intervencion"] <= 1e-9


def test_el_ensayo_produce_todas_las_comparaciones_y_variantes(ensayo_desarrollo: dict) -> None:
    r = ensayo_desarrollo
    assert set(r["comparaciones"]) == {"H1: M4 frente a M2", "H2: M3 frente a M3-sin-orden",
                                       "H2 secundario: consultas con palabra de bandas"}
    for variante in ("M4 sin M3", "M4 sin M0", "M4 con M3-sin-orden", "Control negativo", "M3 solo bandas", "M3 sin bandas"):
        assert variante in r["nombres"]
    veredictos = {evaluacion.SE_SOSTIENE, evaluacion.FAVORABLE, evaluacion.NO_SE_SOSTIENE}
    assert all(c.decision in veredictos for c in [*r["comparaciones"].values(), *r["exploratorias"].values()])
    assert r["comparaciones"]["H2 secundario: consultas con palabra de bandas"].n <= 2  # dos consultas con bandas en desarrollo
    assert {criterio for criterio, _ in r["robustez"]} == {"museo", "completitud"}
    assert len({f["consulta"] for f in r["filas"]}) == 10


def test_m4_con_m3_sin_orden_coincide_con_m4_cuando_la_consulta_no_tiene_bandas(ensayo_desarrollo: dict) -> None:
    # Sin palabra de bandas en la consulta, M3 y su control dan los mismos scores (R27): la fusion no cambia.
    r = ensayo_desarrollo
    sin_bandas = [c for c in r["ndcg"]["M4"] if c not in r["con_bandas"]]
    assert sin_bandas and all(r["ndcg"]["M4"][c] == r["ndcg"]["M4 con M3-sin-orden"][c] for c in sin_bandas)


def test_rankings_t1_con_consultas_hipoteticas(tmp_path: Path) -> None:
    congelada = "data/metadata/v2_1_congelado/anotaciones_v2_1.csv"
    copiar_insumos(tmp_path, ["config/modelos.toml", "config/anotacion.toml", "config/vocabulario.toml", SALIDA_PARTICIONES,
                              SALIDA_PRINCIPAL_V2, str(EMBEDDINGS_M2), str(INDICE_M2), congelada])
    consultas = [
        {"consulta": "T1-E1", "descripcion": "Faja con bandas lisas y de rombos escalonados", "composicion": "bandas",
         "secuencia_bandas": "lisa > geometrica > lisa"},
        {"consulta": "T1-E2", "descripcion": "Pano con campo central y borde de aves", "composicion": "", "secuencia_bandas": ""},
    ]
    escribir_csv(tmp_path / SALIDA_T1, ["consulta", "descripcion", "composicion", "secuencia_bandas"], consultas)
    vectores = np.random.default_rng(1).normal(size=(2, 512))
    (tmp_path / ep.EMBEDDINGS_T1).parent.mkdir(parents=True, exist_ok=True)
    np.save(tmp_path / ep.EMBEDDINGS_T1, (vectores / np.linalg.norm(vectores, axis=1, keepdims=True)).astype(np.float32))
    escribir_csv(tmp_path / ep.INDICE_T1, ["fila", "consulta"], [{"fila": "0", "consulta": "T1-E1"}, {"fila": "1", "consulta": "T1-E2"}])
    filas = ep.rankings_t1(tmp_path)
    galeria = len(leer_csv(RAIZ_REPO / SALIDA_PARTICIONES))
    sistemas = {(f["consulta"], f["sistema"]) for f in filas}
    assert ("T1-E1", "M3") in sistemas and ("T1-E2", "M3") not in sistemas  # M3 solo con especificacion
    assert all(sum(1 for f in filas if (f["consulta"], f["sistema"]) == par) == galeria for par in sistemas)
