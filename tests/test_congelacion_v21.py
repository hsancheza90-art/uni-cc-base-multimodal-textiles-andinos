"""Pruebas de la congelación de la anotación v2.1 (decisión R23)."""

from __future__ import annotations

from pathlib import Path

from src.anotacion import congelacion_v21 as cv
from src.utils.archivos import leer_csv
from src.utils.config import RAIZ_REPO, leer_config_anotacion
from tests.insumos import copiar_insumos

CONFIG = leer_config_anotacion()
CONGELADA = f"{CONFIG['congelacion']['carpeta']}/{cv.ARCHIVO}"
SUMAS = f"{CONFIG['congelacion']['carpeta']}/{cv.SUMAS}"
EXPORTADA = "data/metadata/anotaciones_v2.csv"
BASE = ["config/anotacion.toml", "config/vocabulario.toml", EXPORTADA, CONGELADA, SUMAS]


def test_la_copia_congelada_coincide_con_su_suma_y_con_la_exportacion() -> None:
    if not (RAIZ_REPO / CONGELADA).exists():
        return
    sumas = (RAIZ_REPO / SUMAS).read_text(encoding="utf-8").splitlines()
    assert sumas[0] == f"{cv.sha256(RAIZ_REPO / CONGELADA)}  {CONGELADA}"
    assert {s.split("  ")[1] for s in sumas[1:]} == set(cv.INSUMOS)
    assert (RAIZ_REPO / CONGELADA).read_bytes() == (RAIZ_REPO / EXPORTADA).read_bytes()
    assert len(leer_csv(RAIZ_REPO / CONGELADA)) == 150


def test_un_cambio_despues_de_congelar_detiene_el_flujo(tmp_path: Path) -> None:
    copiar_insumos(tmp_path, BASE)
    assert cv.main(["--root", str(tmp_path)]) == 0
    exportada = tmp_path / EXPORTADA
    exportada.write_bytes(exportada.read_bytes().replace(b"bandas", b"paneles", 1))
    assert cv.main(["--root", str(tmp_path)]) == 1
    assert "NO coincide" in (tmp_path / cv.REPORTE).read_text(encoding="utf-8")


def test_una_copia_alterada_no_pasa_la_suma(tmp_path: Path) -> None:
    copiar_insumos(tmp_path, BASE)
    for relativa in (CONGELADA, EXPORTADA):
        ruta = tmp_path / relativa
        ruta.write_bytes(ruta.read_bytes() + b"\n")
    assert cv.main(["--root", str(tmp_path)]) == 1


def test_no_se_congela_dos_veces(tmp_path: Path) -> None:
    copiar_insumos(tmp_path, BASE)
    antes = (tmp_path / CONGELADA).read_bytes()
    assert cv.main(["--root", str(tmp_path), "--congelar"]) == 1
    assert (tmp_path / CONGELADA).read_bytes() == antes


def test_sin_copia_el_paso_no_falla_y_lo_informa(tmp_path: Path) -> None:
    copiar_insumos(tmp_path, ["config/anotacion.toml", "config/vocabulario.toml", EXPORTADA])
    assert cv.main(["--root", str(tmp_path)]) == 0
    assert "todavia no esta congelada" in (tmp_path / cv.REPORTE).read_text(encoding="utf-8")
