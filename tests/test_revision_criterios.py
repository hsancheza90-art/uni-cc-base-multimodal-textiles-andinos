"""Pruebas de la revisión de criterios de la anotación v2 (decisión R18)."""

from __future__ import annotations

from src.anotacion import revision_criterios as rc
from src.utils.config import RAIZ_REPO, leer_config_anotacion
from src.utils.libros import leer_hoja
from src.utils.vocabulario import leer_vocabulario

CONFIG = leer_config_anotacion()
VOCABULARIO = leer_vocabulario()
ATRIBUTOS = CONFIG["revision_criterios"]["atributos"]


def pieza(id_global: str = "AIC:1", lote: str = "2", **campos: str) -> dict[str, str]:
    base = {"id_global": id_global, "lote": lote, "orden": "1", "composicion": "bandas", "eje_bandas": "horizontal",
            "secuencia_bandas": "lisa > geometrica > lisa", "borde": "no", "simetria": "bilateral",
            "motivos": "geometrico", "familia_iconografica": "geometrica", "observaciones_anotacion": ""}
    return base | campos


def decision(fila: dict[str, str], **campos: str) -> dict[str, str]:
    seleccionada = rc.seleccionar([fila], CONFIG, VOCABULARIO)[0]
    return seleccionada | {"decision": "", "motivo": "", "revisor": "", "fecha_revision": "", "identidad_imagen": ""} | campos


def test_los_segmentos_separan_las_etiquetas_de_la_observacion() -> None:
    texto = "OBS: dos tiras. DUDA motivo_principal: felino o ave. CRITERIO: conté las columnas como bandas. REC: nada."
    assert [e for e, _ in rc.segmentos(texto)] == ["OBS", "DUDA", "CRITERIO", "REC"]
    assert rc.segmentos(texto)[1][1] == "motivo_principal: felino o ave."


def test_una_duda_toca_a_m3_si_nombra_un_atributo_suyo_o_ninguno() -> None:
    assert rc.toca_m3("composicion: bandas o retícula")
    assert rc.toca_m3("motivo_principal y familia_iconografica: muy fragmentadas")
    assert rc.toca_m3("el rostro apenas se lee")  # sin atributo: se revisa
    assert not rc.toca_m3("motivo_principal: felino o ser mítico")
    assert not rc.toca_m3("color_dominante: el fondo es pajizo")


def test_motivos_de_revision_por_regla() -> None:
    assert rc.motivos_revision(pieza(), VOCABULARIO) == ["R12"]
    sin_bandas = pieza(eje_bandas="ausente", secuencia_bandas="ausente", simetria="traslacional")
    assert rc.motivos_revision(sin_bandas, VOCABULARIO) == ["R16"]
    con_notas = pieza(eje_bandas="ausente", secuencia_bandas="ausente",
                      observaciones_anotacion="DUDA composicion: campo o retícula. REC: verificar el id.")
    assert rc.motivos_revision(con_notas, VOCABULARIO) == ["OBS", "ID"]
    ajena = pieza(eje_bandas="ausente", secuencia_bandas="ausente", observaciones_anotacion="DUDA motivo_principal: ave. VOCAB: falta monos.")
    assert rc.motivos_revision(ajena, VOCABULARIO) == []


def test_solo_entran_los_lotes_configurados() -> None:
    filas = [pieza("AIC:1", lote="1"), pieza("AIC:2", lote="3")]
    assert [f["id_global"] for f in rc.seleccionar(filas, CONFIG, VOCABULARIO)] == ["AIC:2"]


def test_sin_workbook_no_cambia_nada_y_todo_queda_pendiente() -> None:
    filas = [pieza()]
    revision = rc.aplicar(filas, None, CONFIG, VOCABULARIO)
    assert revision.filas == filas and not revision.existe and revision.seleccionadas == 1 and not revision.errores


def test_confirmar_mantiene_y_corregir_reemplaza_solo_lo_revisado() -> None:
    a, b = pieza("AIC:1"), pieza("AIC:2")
    decisiones = [
        decision(a, decision="confirmar", revisor="hs", fecha_revision="2026-11-17"),
        decision(b, decision="corregir", revisor="hs", fecha_revision="2026-11-17", motivo="Cenefas, no bandas (R12).",
                 eje_bandas_revisado="ausente", secuencia_bandas_revisado="ausente", borde_revisado="si"),
    ]
    revision = rc.aplicar([a, b], decisiones, CONFIG, VOCABULARIO)
    assert not revision.errores and revision.pendientes == 0
    assert revision.filas[0] == a
    assert revision.filas[1] == b | {"eje_bandas": "ausente", "secuencia_bandas": "ausente", "borde": "si"}
    assert revision.decisiones == {"confirmar": 1, "corregir": 1} and len(revision.cambios) == 3
    assert a["secuencia_bandas"] == "lisa > geometrica > lisa"  # la entrada no se modifica


def test_errores_de_la_revision() -> None:
    def errores(**campos: str) -> list[str]:
        fila = pieza(observaciones_anotacion=campos.pop("observaciones", ""))
        return rc.aplicar([fila], [decision(fila, **campos)], CONFIG, VOCABULARIO).errores

    completa = {"revisor": "hs", "fecha_revision": "2026-11-17"}
    assert any("revisor vacio" in e for e in errores(decision="confirmar", fecha_revision="2026-11-17"))
    assert any("fecha_revision" in e for e in errores(decision="confirmar", revisor="hs", fecha_revision="2026-02-30"))
    assert any("no admite valores" in e for e in errores(decision="confirmar", simetria_revisado="traslacional", **completa))
    assert any("exige motivo" in e for e in errores(decision="corregir", simetria_revisado="traslacional", **completa))
    assert any("al menos un valor" in e for e in errores(decision="corregir", motivo="x", simetria_revisado="bilateral", **completa))
    assert any("fuera del vocabulario" in e for e in errores(decision="corregir", motivo="x", simetria_revisado="espejo", **completa))
    assert any("no concuerdan" in e for e in errores(decision="corregir", motivo="x", secuencia_bandas_revisado="ausente", **completa))
    assert any("sin decision" in e for e in errores(simetria_revisado="traslacional"))
    assert any("identidad_imagen" in e for e in errores(decision="confirmar", observaciones="REC: verificar el id.", **completa))
    assert not errores(decision="confirmar", observaciones="REC: verificar el id.", identidad_imagen="coincide", **completa)


def test_un_workbook_que_no_corresponde_a_la_seleccion_es_un_error() -> None:
    fila = pieza()
    viejo = decision(fila) | {"simetria": "traslacional"}  # la anotacion cambio despues de generar el workbook
    assert any("regenerelo" in e for e in rc.aplicar([fila], [viejo], CONFIG, VOCABULARIO).errores)
    assert any("no corresponde" in e for e in rc.aplicar([fila], [], CONFIG, VOCABULARIO).errores)


def test_el_workbook_versionado_tiene_las_columnas_y_la_seleccion_vigentes() -> None:
    ruta = RAIZ_REPO / CONFIG["revision_criterios"]["workbook"]
    if not ruta.exists():
        return
    filas = leer_hoja(ruta, rc.HOJA, clave="id_global")
    editables, encabezados = rc.columnas(CONFIG)
    assert list(filas[0]) == encabezados and encabezados[:len(editables)] == editables
    assert {f["lote"] for f in filas} <= {str(lote) for lote in CONFIG["revision_criterios"]["lotes"]}
    assert all(f["motivos_revision"] for f in filas)
    assert set(ATRIBUTOS) <= set(encabezados)
