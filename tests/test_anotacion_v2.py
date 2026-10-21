"""Pruebas del corpus principal v2, el nucleo de anotacion, el workbook v2 y el acuerdo entre anotadores."""

from __future__ import annotations

import csv
from pathlib import Path

import pytest

from src.anotacion import corpus_v2
from src.imagenes.aptitud import SALIDA_APTITUD
from src.imagenes.descargar_evaluacion import MANIFIESTO_EVALUACION
from src.utils.archivos import escribir_csv, leer_csv_con_columnas
from src.utils.config import RAIZ_REPO, leer_config
from src.utils.fuentes import FUENTES
from src.utils.vocabulario import leer_vocabulario
from tests.insumos import copiar_insumos


def insumos_corpus_v2() -> list[str]:
    """Archivos versionados que lee src/anotacion/corpus_v2.py."""
    base_met = [d["ruta"] for d in leer_config()["met"]["base"].values() if isinstance(d, dict)]
    return [
        "config/corpus.toml",
        "config/vocabulario.toml",
        *(fuente.salidas["principal"] for fuente in FUENTES.values()),
        *(fuente.candidatos for fuente in FUENTES.values() if fuente.candidatos),
        *base_met,
        MANIFIESTO_EVALUACION,
        SALIDA_APTITUD,
    ]


def leer(ruta: Path) -> list[dict[str, str]]:
    with ruta.open(newline="", encoding="utf-8") as archivo:
        return list(csv.DictReader(archivo))


@pytest.fixture()
def repo_v2(tmp_path: Path) -> Path:
    copiar_insumos(tmp_path, insumos_corpus_v2())
    return tmp_path


# --------------------------------------------------------------------------- corpus principal v2


def test_corpus_v2_se_regenera_identico(repo_v2: Path) -> None:
    assert corpus_v2.main(["--root", str(repo_v2)]) == 0
    for relativa in (corpus_v2.SALIDA_PRINCIPAL_V2, corpus_v2.SALIDA_REPORTE):
        assert (repo_v2 / relativa).read_bytes() == (RAIZ_REPO / relativa).read_bytes(), relativa


def test_corpus_v2_une_las_tres_fuentes_sin_colisiones() -> None:
    filas = leer(RAIZ_REPO / corpus_v2.SALIDA_PRINCIPAL_V2)
    esperados = sum(len(leer(RAIZ_REPO / f.salidas["principal"])) for f in FUENTES.values())
    ids = [fila["id_global"] for fila in filas]
    assert len(filas) == esperados
    assert len(set(ids)) == len(ids)
    assert all(fila["id_global"] == f"{fila['fuente']}:{fila['id_fuente']}" for fila in filas)
    assert {fila["decision_curacion_final"] for fila in filas} == {"principal"}


def test_corpus_v2_usa_el_esquema_armonizado_y_el_vocabulario() -> None:
    columnas, filas = leer_csv_con_columnas(RAIZ_REPO / corpus_v2.SALIDA_PRINCIPAL_V2)
    assert columnas == corpus_v2.COLUMNAS_V2
    vocabulario = leer_vocabulario()
    for campo in vocabulario.values():
        if campo.nombre in columnas:
            assert not [f["id_global"] for f in filas if campo.invalidos(f[campo.nombre])], campo.nombre
    assert {f["estado_anotacion"] for f in filas} == {"sin_anotar"}


def test_corpus_v2_falla_si_un_id_global_se_repite(repo_v2: Path) -> None:
    ruta = repo_v2 / FUENTES["CMA"].salidas["principal"]
    columnas, filas = leer_csv_con_columnas(ruta)
    escribir_csv(ruta, columnas, filas + [filas[0]])
    assert corpus_v2.main(["--root", str(repo_v2)]) == 1
    assert not (repo_v2 / corpus_v2.SALIDA_PRINCIPAL_V2).exists()


def test_corpus_v2_conserva_registros_sin_ficha_de_aptitud(repo_v2: Path) -> None:
    ruta = repo_v2 / SALIDA_APTITUD
    columnas, filas = leer_csv_con_columnas(ruta)
    quitado = "AIC:" + leer(repo_v2 / FUENTES["AIC"].salidas["principal"])[0]["id_fuente"]
    escribir_csv(ruta, columnas, [f for f in filas if f["id_global"] != quitado])

    assert corpus_v2.main(["--root", str(repo_v2)]) == 0
    salida = {f["id_global"]: f for f in leer(repo_v2 / corpus_v2.SALIDA_PRINCIPAL_V2)}
    assert quitado in salida
    assert all(salida[quitado][c] == "" for c in corpus_v2.COLUMNAS_APTITUD)
    reporte = (repo_v2 / corpus_v2.SALIDA_REPORTE).read_text(encoding="utf-8")
    assert f"sin fila en `{SALIDA_APTITUD}`: 1 ({quitado})" in reporte


def test_valor_curado_fuera_del_vocabulario_lo_reemplaza_la_regla() -> None:
    vocabulario = leer_vocabulario()
    fila = {campo: "" for campo in corpus_v2.COLUMNAS}
    fila.update({"fuente": "CMA", "tipo_objeto": "Textile", "material_normalizado": "algodón"})
    descartados = corpus_v2.descartar_fuera_de_vocabulario(fila, vocabulario)
    assert descartados == [("CMA", "tipo_objeto", "Textile")]
    assert fila["tipo_objeto"] == ""
    assert fila["material_normalizado"] == "algodón"  # etiqueta valida: se recodifica despues
