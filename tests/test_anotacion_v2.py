"""Pruebas del corpus principal v2, el nucleo de anotacion, el workbook v2 y el acuerdo entre anotadores."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

import pytest

from src.anotacion import corpus_v2, nucleo
from src.imagenes.aptitud import SALIDA_APTITUD
from src.imagenes.descargar_evaluacion import MANIFIESTO_EVALUACION
from src.utils.archivos import escribir_csv, leer_csv_con_columnas
from src.utils.config import RAIZ_REPO, leer_config, leer_config_anotacion
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


# --------------------------------------------------------------------------- nucleo de anotacion


@pytest.fixture()
def repo_nucleo(tmp_path: Path) -> Path:
    copiar_insumos(tmp_path, ["config/anotacion.toml", corpus_v2.SALIDA_PRINCIPAL_V2])
    return tmp_path


def correr_nucleo(raiz: Path, semilla: int | None = None) -> nucleo.Nucleo:
    config = leer_config_anotacion(raiz)
    registros = leer(raiz / corpus_v2.SALIDA_PRINCIPAL_V2)
    return nucleo.construir_nucleo(registros, config, int(config["nucleo"]["semilla"]) if semilla is None else semilla)


def test_nucleo_se_regenera_byte_a_byte(repo_nucleo: Path) -> None:
    for _ in range(2):
        assert nucleo.main(["--root", str(repo_nucleo)]) == 0
        for relativa in (nucleo.SALIDA_NUCLEO, nucleo.SALIDA_REPORTE):
            assert (repo_nucleo / relativa).read_bytes() == (RAIZ_REPO / relativa).read_bytes(), relativa


def test_cuotas_por_fuente_suman_el_tamano_y_respetan_la_proporcion() -> None:
    resultado = correr_nucleo(RAIZ_REPO)
    tamano = int(leer_config_anotacion()["nucleo"]["tamano"])
    total = sum(resultado.disponibles_fuente.values())
    assert sum(resultado.cuotas_fuente.values()) == len(resultado.filas) == tamano
    for fuente, cuota in resultado.cuotas_fuente.items():
        assert abs(cuota - tamano * resultado.disponibles_fuente[fuente] / total) < 1
        assert sum(f["fuente"] == fuente for f in resultado.filas) == cuota


def test_otra_semilla_cambia_las_piezas_pero_no_las_cuotas() -> None:
    a, b = correr_nucleo(RAIZ_REPO), correr_nucleo(RAIZ_REPO, semilla=7)
    assert {f["id_global"] for f in a.filas} != {f["id_global"] for f in b.filas}
    cuotas = lambda r: [(e.fuente, e.cultura, e.banda, e.cuota, e.asignadas) for e in r.estratos]  # noqa: E731
    assert cuotas(a) == cuotas(b)


def test_mayores_restos_da_la_unidad_sobrante_al_mayor_resto() -> None:
    # Cuotas exactas 1,6 / 1,2 / 0,2: las partes enteras suman 2 y la unidad restante va al mayor resto (a).
    assert nucleo.mayores_restos(3, {"a": 8, "b": 6, "c": 1}) == {"a": 2, "b": 1, "c": 0}
    # Un estrato pequeño entra si su resto lo justifica: exactas 1,54 / 1,54 / 0,92; c tiene el mayor
    # resto y entra con 1; la segunda unidad desempata a favor de a (mismo peso, primera clave).
    assert nucleo.mayores_restos(4, {"a": 15, "b": 15, "c": 9}) == {"a": 2, "b": 1, "c": 1}


def test_estrato_con_menos_piezas_que_su_cuota_redistribuye_el_faltante() -> None:
    # a pide 5 y tiene 3: los 2 que faltan van a b (3 libres) y c (1 libre) en proporcion a lo libre,
    # exactas 1,5 / 0,5; el empate de restos se resuelve por mayor peso (b).
    asignadas, faltantes = nucleo.ajustar_a_disponibles({"a": 5, "b": 2, "c": 3}, {"a": 3, "b": 5, "c": 4})
    assert asignadas == {"a": 3, "b": 4, "c": 3}
    assert faltantes == {"a": 2, "b": 0, "c": 0}


def test_el_informe_registra_los_faltantes() -> None:
    resultado = correr_nucleo(RAIZ_REPO)
    resultado.estratos[0].faltantes = 2
    lineas = nucleo.lineas_reporte(resultado, leer_config_anotacion())
    assert "Faltantes redistribuidos dentro de su fuente: 2 pieza(s)." in lineas


def test_ningun_lote_supera_el_tope_de_una_fuente() -> None:
    config = leer_config_anotacion()
    tope, tamano_lote = float(config["nucleo"]["tope_fuente_lote"]), int(config["nucleo"]["tamano_lote"])
    filas = leer(RAIZ_REPO / nucleo.SALIDA_NUCLEO)
    for lote in {f["lote"] for f in filas}:
        propias = [f for f in filas if f["lote"] == lote]
        assert len(propias) == tamano_lote
        assert sorted(int(f["orden"]) for f in propias) == list(range(1, tamano_lote + 1))
        assert max(Counter(f["fuente"] for f in propias).values()) <= tope * tamano_lote


def test_un_tope_imposible_falla_con_mensaje_claro(repo_nucleo: Path, capsys: pytest.CaptureFixture[str]) -> None:
    ruta = repo_nucleo / "config/anotacion.toml"
    ruta.write_text(ruta.read_text(encoding="utf-8").replace("tope_fuente_lote = 0.6", "tope_fuente_lote = 0.4"), encoding="utf-8")
    assert nucleo.main(["--root", str(repo_nucleo)]) == 1
    assert "tope 40%" in capsys.readouterr().out
    assert not (repo_nucleo / nucleo.SALIDA_NUCLEO).exists()


def test_cultura_agrupada_usa_terminos_casos_y_sin_cultura() -> None:
    config = leer_config_anotacion()
    casos = nucleo.leer_casos(config)
    assert nucleo.agrupar_cultura("Peru, South Coast, Wari Culture", config, casos) == "wari"
    assert nucleo.agrupar_cultura("huari", config, casos) == "wari"
    assert nucleo.agrupar_cultura("Nasca-Wari", config, casos) == "wari"
    assert nucleo.agrupar_cultura("Lambayeque", config, casos) == "otras"
    assert nucleo.agrupar_cultura("", config, casos) == "sin_cultura"
    with pytest.raises(nucleo.ErrorNucleo, match="nombra varios grupos"):
        nucleo.agrupar_cultura("Paracas-Wari", config, casos)
