"""Pruebas de reproducibilidad del flujo MET v2 + CMA v2."""

from __future__ import annotations

import csv
import shutil
from pathlib import Path

import pytest

from src import flujo
from src.preprocessing import create_cma_review_workbook_v2, create_met_review_workbook_v2
from src.utils.config import RAIZ_REPO, conjuntos_esperados, contar_filas_csv, leer_config

# Insumos versionados de los que parte el flujo; todo lo demas se regenera.
INSUMOS = [
    "config/corpus.toml",
    "data/processed/corpus_met_textiles_andinos_v1_principal.csv",
    "data/processed/corpus_met_textiles_andinos_v1_complementario.csv",
    "data/processed/corpus_met_textiles_andinos_v1_exclusiones_curatoriales.csv",
    "data/metadata/met_revision_manual_v2.xlsx",
    "data/metadata/cma_revision_manual_v2.xlsx",
    "data/metadata/cma_andes_textiles_candidates.csv",
]

REPORTES = [
    "outputs/reports/met_resumen_curacion_v2.md",
    "outputs/reports/met_auditoria_tecnica_v2.md",
    "outputs/reports/met_resumen_revision_manual_v2.md",
    "outputs/reports/cma_resumen_revision_manual_v2.md",
]


def texto_normalizado(ruta: Path) -> str:
    return ruta.read_bytes().decode("utf-8").replace("\r\n", "\n")


def leer_ids(ruta: Path, columna: str) -> list[str]:
    with ruta.open(newline="", encoding="utf-8-sig") as archivo:
        return [fila[columna] for fila in csv.DictReader(archivo)]


@pytest.fixture(scope="module")
def copia_regenerada(tmp_path_factory: pytest.TempPathFactory) -> Path:
    raiz = tmp_path_factory.mktemp("repo")
    for relativa in INSUMOS:
        destino = raiz / relativa
        destino.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(RAIZ_REPO / relativa, destino)

    assert flujo.main(["--root", str(raiz)]) == 0
    return raiz


def salidas_regeneradas() -> list[str]:
    csvs = [str(ruta) for _, _, ruta, _ in conjuntos_esperados(leer_config())]
    csvs = [ruta.replace("\\", "/") for ruta in csvs if ruta.replace("\\", "/") not in INSUMOS]
    return csvs + REPORTES


@pytest.mark.parametrize("relativa", salidas_regeneradas())
def test_flujo_regenera_salidas_versionadas(copia_regenerada: Path, relativa: str) -> None:
    generado = copia_regenerada / relativa
    assert generado.exists(), f"El flujo no genero {relativa}"
    assert b"\r\n" not in generado.read_bytes(), f"{relativa} no usa finales de linea LF"
    assert texto_normalizado(generado) == texto_normalizado(RAIZ_REPO / relativa)


@pytest.mark.parametrize(
    ("etapa", "conjunto", "ruta", "esperado"),
    conjuntos_esperados(leer_config()),
    ids=lambda valor: str(valor),
)
def test_conteos_versionados_coinciden_con_config(etapa: str, conjunto: str, ruta: Path, esperado: int) -> None:
    assert contar_filas_csv(RAIZ_REPO / ruta) == esperado


@pytest.mark.parametrize(
    ("archivos", "columna"),
    [
        (
            [
                "data/metadata/met_corpus_principal_v2_revisado.csv",
                "data/metadata/met_corpus_secundario_v2_revisado.csv",
                "data/metadata/met_descartados_v2_revisado.csv",
            ],
            "id_fuente",
        ),
        (
            [
                "data/metadata/cma_corpus_principal_revisado.csv",
                "data/metadata/cma_corpus_secundario_revisado.csv",
                "data/metadata/cma_descartados_revisado.csv",
            ],
            "id_objeto",
        ),
    ],
    ids=["met_revisado", "cma_revisado"],
)
def test_subconjuntos_revisados_no_comparten_ids(archivos: list[str], columna: str) -> None:
    ids = [id_ for archivo in archivos for id_ in leer_ids(RAIZ_REPO / archivo, columna)]
    assert all(ids), "Hay identificadores vacios"
    repetidos = sorted({id_ for id_ in ids if ids.count(id_) > 1})
    assert not repetidos, f"Identificadores en mas de un subconjunto: {repetidos[:10]}"


@pytest.mark.parametrize(
    ("modulo", "workbook"),
    [
        (create_met_review_workbook_v2, "data/metadata/met_revision_manual_v2.xlsx"),
        (create_cma_review_workbook_v2, "data/metadata/cma_revision_manual_v2.xlsx"),
    ],
    ids=["met", "cma"],
)
def test_generador_no_sobrescribe_workbook_con_decisiones(tmp_path: Path, modulo, workbook: str) -> None:
    destino = tmp_path / workbook
    destino.parent.mkdir(parents=True)
    destino.write_bytes(b"decisiones manuales")

    assert modulo.main(["--root", str(tmp_path)]) == 1
    assert destino.read_bytes() == b"decisiones manuales"
