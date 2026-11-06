"""Pruebas del snapshot experimental v2 y de la coherencia entre config/experimento.toml y el protocolo."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

import pytest

from src.anotacion.aplicar_anotaciones_v2 import SALIDA_ANOTACIONES_V2
from src.anotacion.nucleo import SALIDA_NUCLEO
from src.experimento import snapshot
from src.grupos.grupos import SALIDA_GRUPOS
from src.utils.archivos import escribir_csv, leer_csv
from src.utils.config import CONFIG_EXPERIMENTO, RAIZ_REPO, leer_config_experimento

PROTOCOLO = RAIZ_REPO / "docs/protocolo_experimental_v2.md"


def test_la_configuracion_coincide_con_el_protocolo() -> None:
    config = leer_config_experimento()
    texto = PROTOCOLO.read_text(encoding="utf-8")
    c3, juicios, metricas = config["consultas_t3"], config["juicios"], config["metricas"]
    assert f"**desarrollo ({round(config['particiones']['proporcion_desarrollo'] * 100)} %)**" in texto
    assert f"{c3['desarrollo']} de desarrollo, tomadas de grupos de desarrollo, y {c3['prueba']} de prueba" in texto
    assert f"**Consultas T1:** {config['consultas_t1']['prueba']}, solo de prueba" in texto
    assert f"los {juicios['profundidad_pool']} primeros de M0" in texto and f"más {juicios['aleatorios_pool']} candidatos al azar" in texto
    assert f"los pools de {juicios['consultas_doble_juicio']} consultas de prueba" in texto
    assert f"nDCG@{metricas['k']}" in texto and juicios["escala"] == [0, 1, 2, 3]
    assert f"Umbral práctico: Δ = {str(metricas['umbral_practico']).replace('.', ',')}" in texto
    assert f"{metricas['replicas_bootstrap']:,} réplicas".replace(",", " ") in texto
    assert f"IC {round(metricas['confianza'] * 100)} %" in texto


CONFIG_PEQUENA = """
[particiones]
semilla = 1
proporcion_desarrollo = 0.3
[consultas_t3]
semilla = 2
desarrollo = 2
prueba = 4
excluir_composicion = ["no_observable", "desconocido"]
"""


@pytest.fixture()
def repo(tmp_path: Path) -> Path:
    """Veinte piezas: G-001 une tres (AIC), G-002 dos (MET); una sin composicion observable."""
    (tmp_path / CONFIG_EXPERIMENTO).parent.mkdir(parents=True)
    (tmp_path / CONFIG_EXPERIMENTO).write_text(CONFIG_PEQUENA, encoding="utf-8")
    ids = [f"AIC:{i}" for i in range(1, 11)] + [f"MET:{i}" for i in range(11, 21)]
    grupo = {"AIC:1": "G-001", "AIC:2": "G-001", "AIC:3": "G-001", "MET:11": "G-002", "MET:12": "G-002"}
    escribir_csv(tmp_path / SALIDA_NUCLEO, ["id_global"], [{"id_global": i} for i in ids])
    escribir_csv(tmp_path / SALIDA_GRUPOS, ["id_global", "fuente", "grupo"],
                 [{"id_global": i, "fuente": i.split(":")[0], "grupo": grupo.get(i, f"G-{i}")} for i in ids])
    composicion = {i: ("bandas" if n % 2 else "paneles") for n, i in enumerate(ids)} | {"MET:20": "no_observable"}
    escribir_csv(tmp_path / SALIDA_ANOTACIONES_V2, ["id_global", "composicion"],
                 [{"id_global": i, "composicion": c} for i, c in composicion.items()])
    return tmp_path


def test_crear_reparte_por_grupo_sin_fugas_y_no_sobrescribe(repo: Path) -> None:
    assert snapshot.main(["--root", str(repo), "--crear"]) == 0
    particiones = {f["id_global"]: f for f in leer_csv(repo / snapshot.SALIDA_PARTICIONES)}
    assert len({particiones[i]["particion"] for i in ("AIC:1", "AIC:2", "AIC:3")}) == 1  # el grupo no se parte
    assert particiones["AIC:2"]["grupo"] == "AIC:1"  # clave estable: el menor id del grupo
    consultas = leer_csv(repo / snapshot.SALIDA_CONSULTAS)
    assert Counter(c["particion"] for c in consultas) == {"desarrollo": 2, "prueba": 4}
    assert len({c["grupo"] for c in consultas}) == len(consultas)  # una por grupo
    assert all(c["id_global"] != "MET:20" for c in consultas)  # composicion no observable
    assert all(c["particion"] == particiones[c["id_global"]]["particion"] for c in consultas)
    reporte = (repo / snapshot.REPORTE_SNAPSHOT).read_text(encoding="utf-8")
    assert "Sin fugas" in reporte and not any(c["id_global"] in reporte for c in consultas)
    antes = (repo / snapshot.SALIDA_CONSULTAS).read_bytes()
    assert snapshot.main(["--root", str(repo), "--crear"]) == 1  # congelado
    assert (repo / snapshot.SALIDA_CONSULTAS).read_bytes() == antes


def test_reemplazo_cambia_solo_la_consulta_que_dejo_de_ser_elegible(repo: Path) -> None:
    assert snapshot.main(["--root", str(repo), "--crear"]) == 0
    consultas = leer_csv(repo / snapshot.SALIDA_CONSULTAS)
    anotaciones = leer_csv(repo / SALIDA_ANOTACIONES_V2)
    caida = consultas[0]
    for fila in anotaciones:
        if fila["id_global"] == caida["id_global"]:
            fila["composicion"] = "no_observable"
    escribir_csv(repo / SALIDA_ANOTACIONES_V2, ["id_global", "composicion"], anotaciones)
    assert snapshot.main(["--root", str(repo)]) == 1  # la validacion lo detecta
    assert snapshot.main(["--root", str(repo), "--reemplazar"]) == 0
    nuevas = leer_csv(repo / snapshot.SALIDA_CONSULTAS)
    assert [c["consulta"] for c in nuevas] == [c["consulta"] for c in consultas]
    assert nuevas[1:] == consultas[1:]  # las demas no cambian
    assert nuevas[0]["id_global"] != caida["id_global"] and nuevas[0]["estrato"] == caida["estrato"]


def test_sin_otra_pieza_elegible_en_el_estrato_el_reemplazo_lo_deja_al_revisor(repo: Path) -> None:
    assert snapshot.main(["--root", str(repo), "--crear"]) == 0
    caida = leer_csv(repo / snapshot.SALIDA_CONSULTAS)[0]
    museo, _, comp = caida["estrato"].partition(" | ")
    anotaciones = leer_csv(repo / SALIDA_ANOTACIONES_V2)
    for fila in anotaciones:  # el estrato se queda sin piezas elegibles
        if fila["id_global"].startswith(museo) and fila["composicion"] == comp:
            fila["composicion"] = "no_observable"
    escribir_csv(repo / SALIDA_ANOTACIONES_V2, ["id_global", "composicion"], anotaciones)
    antes = (repo / snapshot.SALIDA_CONSULTAS).read_bytes()
    assert snapshot.main(["--root", str(repo), "--reemplazar"]) == 1
    assert (repo / snapshot.SALIDA_CONSULTAS).read_bytes() == antes


def test_un_grupo_partido_entre_particiones_detiene_el_flujo(repo: Path) -> None:
    assert snapshot.main(["--root", str(repo), "--crear"]) == 0
    filas = leer_csv(repo / snapshot.SALIDA_PARTICIONES)
    for fila in filas:
        if fila["id_global"] == "AIC:3":
            fila["particion"] = "prueba" if fila["particion"] == "desarrollo" else "desarrollo"
    escribir_csv(repo / snapshot.SALIDA_PARTICIONES, snapshot.COLUMNAS_PARTICIONES, filas)
    assert snapshot.main(["--root", str(repo)]) == 1
    assert "grupos repartidos entre desarrollo y prueba (fuga)" in (repo / snapshot.REPORTE_SNAPSHOT).read_text(encoding="utf-8")


def test_sin_snapshot_la_validacion_no_hace_nada(tmp_path: Path) -> None:
    assert snapshot.main(["--root", str(tmp_path)]) == 0
