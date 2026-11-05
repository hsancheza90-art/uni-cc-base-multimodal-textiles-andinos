"""Pruebas de reproducibilidad del flujo MET v2 + CMA v2."""

from __future__ import annotations

import csv
from pathlib import Path

import pytest
from openpyxl import load_workbook

from src import flujo
from src.metadata import apply_aic_review_v2, apply_cma_review_v2, apply_met_review_v2
from src.preprocessing import (
    create_aic_review_workbook_v2,
    create_cma_review_workbook_v2,
    create_met_review_workbook_v2,
)
from src.utils.config import RAIZ_REPO, conjuntos_esperados, contar_filas_csv, leer_config
from src.utils.fuentes import FUENTES
from src.utils.libros import indice_columnas, leer_hoja
from tests.insumos import copiar_insumos

# Insumos versionados de los que parte el flujo; todo lo demas se regenera.
INSUMOS = [
    "config/corpus.toml",
    "data/processed/corpus_met_textiles_andinos_v1_principal.csv",
    "data/processed/corpus_met_textiles_andinos_v1_complementario.csv",
    "data/processed/corpus_met_textiles_andinos_v1_exclusiones_curatoriales.csv",
    "data/processed/corpus_met_textiles_andinos_v1_inventario_base.csv",
    "data/metadata/met_revision_manual_v2.xlsx",
    "data/metadata/cma_revision_manual_v2.xlsx",
    "data/metadata/cma_andes_textiles_candidates.csv",
    "data/metadata/imagenes_manifiesto_met_cma_v1.csv",
    "data/metadata/anotacion_met_cma_v1.xlsx",
    "data/metadata/aic_andes_textiles_candidates.csv",
    "data/metadata/aic_revision_manual_v2.xlsx",
    "config/vocabulario.toml",
    "data/metadata/v1_congelado/vocabulario.toml",
    "config/aptitud.toml",
    "data/metadata/aptitud_medidas_v2.csv",
    "data/metadata/imagenes_evaluacion_manifiesto_v2.csv",
    "config/anotacion.toml",
    "data/metadata/anotacion_v2.xlsx",
    "data/metadata/anotacion_v2_reanotacion.xlsx",
    "data/metadata/v1_congelado/met_corpus_principal_v2_revisado.csv",
    "data/metadata/v1_congelado/met_corpus_secundario_v2_revisado.csv",
    "data/metadata/v1_congelado/cma_corpus_principal_revisado.csv",
    "data/metadata/v1_congelado/cma_corpus_secundario_revisado.csv",
]

REPORTES = [
    "outputs/reports/met_resumen_curacion_v2.md",
    "outputs/reports/met_auditoria_tecnica_v2.md",
    "outputs/reports/met_resumen_revision_manual_v2.md",
    "outputs/reports/cma_resumen_revision_manual_v2.md",
    "outputs/reports/aic_resumen_revision_manual_v2.md",
    "outputs/reports/corpus_textiles_andinos_met_cma_v1_resumen.md",
    "outputs/reports/filtros_comparacion_met_inventario.md",
    "outputs/reports/anotacion_met_cma_v1_validacion.md",
    "docs/corpus/taxonomia_atributos_met_cma_v1.md",
    "docs/corpus/taxonomia_atributos_v2.md",
    "data/metadata/anotaciones_met_cma_v1.csv",
    "docs/esquema_consolidado_met_cma_v1.md",
    "data/processed/corpus_textiles_andinos_met_cma_v1_sha256.txt",
    "config/aptitud_modelo.json",
    "data/metadata/aptitud_imagenes_v2.csv",
    "outputs/reports/aptitud_calibracion_v2.md",
    "outputs/reports/aptitud_imagenes_v2_resumen.md",
    "outputs/reports/corpus_textiles_andinos_v2_principal_resumen.md",
    "outputs/reports/nucleo_anotacion_v2.md",
    "outputs/reports/anotacion_v2_validacion.md",
    "outputs/reports/anotacion_acuerdo_v2.md",
]


def texto_normalizado(ruta: Path) -> str:
    return ruta.read_bytes().decode("utf-8").replace("\r\n", "\n")


def leer_ids(ruta: Path, columna: str) -> list[str]:
    with ruta.open(newline="", encoding="utf-8-sig") as archivo:
        return [fila[columna] for fila in csv.DictReader(archivo)]


@pytest.fixture(scope="module")
def copia_regenerada(tmp_path_factory: pytest.TempPathFactory) -> Path:
    raiz = tmp_path_factory.mktemp("repo")
    copiar_insumos(raiz, INSUMOS)
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
        (list(FUENTES[codigo].salidas.values()), "id_fuente") for codigo in FUENTES
    ],
    ids=[f"{codigo.lower()}_revisado" for codigo in FUENTES],
)
def test_subconjuntos_revisados_no_comparten_ids(archivos: list[str], columna: str) -> None:
    ids = [id_ for archivo in archivos for id_ in leer_ids(RAIZ_REPO / archivo, columna)]
    assert all(ids), "Hay identificadores vacios"
    repetidos = sorted({id_ for id_ in ids if ids.count(id_) > 1})
    assert not repetidos, f"Identificadores en mas de un subconjunto: {repetidos[:10]}"


APLICAR_REVISION = {"MET": apply_met_review_v2.main, "CMA": apply_cma_review_v2.main, "AIC": apply_aic_review_v2.main}


def editar_revision(raiz: Path, codigo: str, cambios: dict[tuple[int, str], object]) -> None:
    """Escribe valores en el workbook de revision copiado: {(fila de Excel, columna): valor}."""
    fuente = FUENTES[codigo]
    libro = load_workbook(raiz / fuente.workbook)
    hoja = libro[fuente.hoja]
    columnas = indice_columnas(hoja)
    for (fila, columna), valor in cambios.items():
        hoja.cell(row=fila, column=columnas[columna]).value = valor  # cell(value=None) no borra
    libro.save(raiz / fuente.workbook)


@pytest.mark.parametrize("caso", ["decision_invalida", "fila_sin_id", "id_repetido"])
@pytest.mark.parametrize("codigo", list(FUENTES))
def test_revision_con_hallazgos_termina_en_1_sin_reemplazar_salidas(tmp_path: Path, codigo: str, caso: str) -> None:
    fuente = FUENTES[codigo]
    copiar_insumos(tmp_path, [fuente.workbook])
    assert APLICAR_REVISION[codigo](["--root", str(tmp_path)]) == 0
    salidas = [*fuente.salidas.values(), fuente.pendientes, fuente.reporte]
    antes = {relativa: (tmp_path / relativa).read_bytes() for relativa in salidas}

    segunda_id = leer_hoja(tmp_path / fuente.workbook, fuente.hoja)[1]["id_fuente"]
    cambios = {
        "decision_invalida": {(2, "corpus_final"): "principall"},
        "fila_sin_id": {(2, "id_fuente"): None},
        "id_repetido": {(2, "id_fuente"): segunda_id},
    }[caso]
    editar_revision(tmp_path, codigo, cambios)

    assert APLICAR_REVISION[codigo](["--root", str(tmp_path)]) == 1
    assert {relativa: (tmp_path / relativa).read_bytes() for relativa in salidas} == antes


def test_revisar_es_un_pendiente_legitimo(tmp_path: Path) -> None:
    fuente = FUENTES["AIC"]
    copiar_insumos(tmp_path, [fuente.workbook])
    primera_id = leer_hoja(tmp_path / fuente.workbook, fuente.hoja)[0]["id_fuente"]
    editar_revision(tmp_path, "AIC", {(2, "corpus_final"): "revisar"})

    assert APLICAR_REVISION["AIC"](["--root", str(tmp_path)]) == 0
    assert leer_ids(tmp_path / fuente.pendientes, "id_fuente") == [primera_id]


@pytest.mark.parametrize(
    ("modulo", "workbook"),
    [
        (create_met_review_workbook_v2, "data/metadata/met_revision_manual_v2.xlsx"),
        (create_cma_review_workbook_v2, "data/metadata/cma_revision_manual_v2.xlsx"),
        (create_aic_review_workbook_v2, "data/metadata/aic_revision_manual_v2.xlsx"),
    ],
    ids=["met", "cma", "aic"],
)
def test_generador_no_sobrescribe_workbook_con_decisiones(tmp_path: Path, modulo, workbook: str) -> None:
    destino = tmp_path / workbook
    destino.parent.mkdir(parents=True)
    destino.write_bytes(b"decisiones manuales")

    assert modulo.main(["--root", str(tmp_path)]) == 1
    assert destino.read_bytes() == b"decisiones manuales"
