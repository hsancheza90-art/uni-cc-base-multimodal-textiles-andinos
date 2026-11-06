"""Pruebas del consolidado v2 (MET, CMA y AIC) que no dependen de los datos versionados."""

from __future__ import annotations

from src.consolidado import consolidado_v2
from src.consolidado.esquema import COLUMNAS, OBLIGATORIOS
from src.utils.vocabulario import leer_vocabulario


def registro(id_global: str, **campos: str) -> dict[str, str]:
    fila = {c: "x" for c in OBLIGATORIOS} | {c: "" for c in COLUMNAS if c not in OBLIGATORIOS}
    fila |= {"id_global": id_global, "fuente": id_global.split(":")[0], "id_fuente": id_global.split(":")[1],
             "decision_curacion_final": "principal", "estado_licencia": "cc0", "estado_metadatos": "parcial",
             "estado_anotacion": "sin_anotar", "estado_imagen": "util", "grupo": "G-001", "tamano_grupo": "1"}
    return fila | campos


def test_validar_detiene_por_ids_repetidos_piezas_sin_grupo_y_pares_pendientes() -> None:
    vocabulario = leer_vocabulario()
    assert consolidado_v2.validar([registro("AIC:1"), registro("CMA:2")], vocabulario, 0) == []
    problemas = consolidado_v2.validar([registro("AIC:1"), registro("AIC:1"), registro("MET:3", grupo="")],
                                       vocabulario, 4)
    assert any("repetidos" in p for p in problemas)
    assert any(p.startswith("MET:3: sin grupo") for p in problemas)
    assert any(p.startswith("4 pares de duplicados sin decidir") for p in problemas)


def test_fuentes_y_licencias_incluyen_aic_y_la_licencia_de_sus_textos() -> None:
    filas = consolidado_v2.filas_fuentes([registro("AIC:1"), registro("AIC:2", decision_curacion_final="complementario")])
    aic = next(f for f in filas if f["fuente"] == "AIC")
    assert (aic["registros_principal"], aic["registros_complementario"], aic["registros_total"]) == ("1", "1", "2")
    assert "CC BY 4.0" in aic["licencia_textos"]
    assert [f["fuente"] for f in filas] == ["MET", "CMA", "AIC"]
