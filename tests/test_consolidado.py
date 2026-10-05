"""Pruebas del corpus consolidado MET+CMA v1.0 y del descargador de imagenes."""

from __future__ import annotations

import csv
import hashlib
import io
from pathlib import Path

import pytest
import requests
from PIL import Image

from src.consolidado import construir_consolidado as cc
from src.consolidado.esquema import COLUMNAS, OBLIGATORIOS
from src.imagenes import descargar_imagenes as di
from src.utils.config import RAIZ_REPO, leer_config
from src.utils.vocabulario import leer_vocabulario


def leer(relativa: str) -> list[dict[str, str]]:
    with (RAIZ_REPO / relativa).open(newline="", encoding="utf-8-sig") as archivo:
        return list(csv.DictReader(archivo))


@pytest.fixture(scope="module")
def consolidado() -> list[dict[str, str]]:
    return leer(cc.SALIDA_CONSOLIDADO)


def test_columnas_siguen_el_esquema(consolidado: list[dict[str, str]]) -> None:
    assert list(consolidado[0]) == COLUMNAS


def test_id_global_unico_y_armonizado(consolidado: list[dict[str, str]]) -> None:
    ids = [fila["id_global"] for fila in consolidado]
    assert len(ids) == len(set(ids))
    assert all(fila["id_global"] == f"{fila['fuente']}:{fila['id_fuente']}" for fila in consolidado)


def test_conteos_por_fuente_y_decision(consolidado: list[dict[str, str]]) -> None:
    esperados = leer_config()["consolidado"]["conteos"]
    for clave, esperado in esperados.items():
        if clave == "total":
            assert len(consolidado) == esperado
        else:
            fuente, decision = clave.split("_")
            observado = sum(f["fuente"] == fuente and f["decision_curacion_final"] == decision for f in consolidado)
            assert observado == esperado, clave


def test_obligatorios_sin_vacios(consolidado: list[dict[str, str]]) -> None:
    vacios = [(f["id_global"], c) for f in consolidado for c in OBLIGATORIOS if not f[c]]
    assert not vacios, vacios[:10]


@pytest.mark.parametrize(
    ("revisados", "clave", "fuente"),
    [(cc.MET_REVISADOS, "id_fuente", "MET"), (cc.CMA_REVISADOS, "id_objeto", "CMA")],
    ids=["met", "cma"],
)
def test_no_se_pierden_registros_ni_titulos(consolidado, revisados, clave, fuente) -> None:
    por_id = {f["id_global"]: f for f in consolidado}
    for decision, ruta in revisados.items():
        for fila in leer(ruta):
            registro = por_id[f"{fuente}:{fila[clave]}"]
            assert registro["decision_curacion_final"] == decision
            assert registro["titulo_original"] == fila["titulo_original"]


@pytest.mark.parametrize("campo", ["tipo_objeto", "material_normalizado", "tecnica_normalizada"])
def test_origen_de_campos_normalizados(consolidado: list[dict[str, str]], campo: str) -> None:
    for fila in consolidado:
        origen = fila[f"origen_{campo}"]
        assert origen == ("" if not fila[campo] else origen)
        assert origen in ({"curacion", "regla"} if fila[campo] else {""}), (fila["id_global"], campo)


def test_valores_curados_se_conservan_recodificados(consolidado: list[dict[str, str]]) -> None:
    vocabulario = leer_vocabulario()
    por_id = {f["id_global"]: f for f in consolidado}
    pares = [("tipo_objeto", "tipo_objeto"), ("material_normalizado", "material_normalizado"), ("tecnica", "tecnica_normalizada")]
    for ruta in cc.MET_REVISADOS.values():
        for fila in leer(ruta):
            registro = por_id[f"MET:{fila['id_fuente']}"]
            for campo_rev, campo_cons in pares:
                if fila[campo_rev]:
                    assert registro[campo_cons] == vocabulario[campo_cons].recodificar(fila[campo_rev])
                    assert registro[f"origen_{campo_cons}"] == "curacion"


def test_campos_controlados_usan_el_vocabulario(consolidado: list[dict[str, str]]) -> None:
    vocabulario = leer_vocabulario()
    for fila in consolidado:
        for campo in vocabulario.values():
            if campo.nombre in fila:
                assert not campo.invalidos(fila[campo.nombre]), (fila["id_global"], campo.nombre)


def test_titulo_sugerido_se_conserva(consolidado: list[dict[str, str]]) -> None:
    por_id = {f["id_global"]: f for f in consolidado}
    for ruta in cc.MET_REVISADOS.values():
        for fila in leer(ruta):
            if fila["titulo_es_sugerido"]:
                assert por_id[f"MET:{fila['id_fuente']}"]["titulo_es_sugerido"] == fila["titulo_es_sugerido"]


def test_grupos_de_imagen_compartida(consolidado: list[dict[str, str]]) -> None:
    grupos: dict[str, set[str]] = {}
    for fila in consolidado:
        if fila["grupo_imagen_duplicada"]:
            grupos.setdefault(fila["grupo_imagen_duplicada"], set()).add(fila["id_global"])
    assert sorted(map(sorted, grupos.values())) == [
        ["CMA:165266", "CMA:165267"],
        ["MET:307964", "MET:307965"],
        ["MET:307966", "MET:307967"],
        ["MET:308036", "MET:308106"],
    ]


def test_sumas_sha256_corresponden_a_los_archivos() -> None:
    lineas = (RAIZ_REPO / cc.SALIDA_SHA256).read_text(encoding="utf-8").splitlines()
    assert len(lineas) == 3
    for linea in lineas:
        suma, ruta = linea.split("  ", 1)
        assert hashlib.sha256((RAIZ_REPO / ruta).read_bytes()).hexdigest() == suma, ruta


def test_agrupa_por_url_archivo_o_pixeles() -> None:
    base = {"url_imagen": "", "imagen_sha256": "", "imagen_sha256_pixeles": ""}
    registros = [
        {**base, "id_global": "A", "url_imagen": "u1"},
        {**base, "id_global": "B", "url_imagen": "u1", "imagen_sha256": "s1"},
        {**base, "id_global": "C", "imagen_sha256": "s1"},
        {**base, "id_global": "D", "imagen_sha256_pixeles": "p1"},
        {**base, "id_global": "E", "imagen_sha256_pixeles": "p1"},
        {**base, "id_global": "F", "url_imagen": "u9"},
    ]
    grupos = sorted(sorted(ids) for ids in cc.agrupar_duplicados(registros).values())
    assert grupos == [["A", "B", "C"], ["D", "E"]]


# --------------------------------------------------------------------------- descargador


def jpeg(color: tuple[int, int, int], tamano: tuple[int, int] = (40, 30)) -> bytes:
    salida = io.BytesIO()
    Image.new("RGB", tamano, color).save(salida, format="JPEG")
    return salida.getvalue()


class RespuestaFalsa:
    def __init__(self, estado: int, contenido: bytes = b"") -> None:
        self.status_code = estado
        self.content = contenido

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise requests.HTTPError(f"{self.status_code} Error")


class SesionFalsa:
    def __init__(self, respuestas: dict[str, RespuestaFalsa]) -> None:
        self.respuestas = respuestas
        self.pedidas: list[str] = []

    def get(self, url: str, timeout: object = None) -> RespuestaFalsa:
        self.pedidas.append(url)
        return self.respuestas[url]


REGISTRO = {
    "id_global": "MET:1",
    "fuente": "MET",
    "id_fuente": "1",
    "url_imagen": "https://x/original.jpg",
    "url_imagen_miniatura": "https://x/web-large.jpg",
}


def test_descarga_usa_respaldo_si_la_miniatura_no_existe(tmp_path: Path) -> None:
    contenido = jpeg((200, 10, 10))
    sesion = SesionFalsa({
        "https://x/web-large.jpg": RespuestaFalsa(404),
        "https://x/original.jpg": RespuestaFalsa(200, contenido),
    })
    fila = di.descargar(sesion, tmp_path, REGISTRO, di.urls_a_descargar(REGISTRO))

    assert sesion.pedidas == ["https://x/web-large.jpg", "https://x/original.jpg"]
    assert fila["estado_descarga"] == "ok"
    assert fila["url_descargada"] == "https://x/original.jpg"
    assert (fila["imagen_ancho"], fila["imagen_alto"]) == ("40", "30")
    assert (tmp_path / fila["ruta_imagen_local"]).read_bytes() == contenido
    assert fila["imagen_sha256"] == hashlib.sha256(contenido).hexdigest()


def test_descarga_registra_error_si_ninguna_url_responde(tmp_path: Path) -> None:
    sesion = SesionFalsa({url: RespuestaFalsa(404) for url in di.urls_a_descargar(REGISTRO)})
    fila = di.descargar(sesion, tmp_path, REGISTRO, di.urls_a_descargar(REGISTRO))

    assert fila["estado_descarga"] == "error"
    assert "404" in fila["error"]
    assert not (tmp_path / "data/images").exists()


def test_misma_fotografia_tiene_mismo_hash_de_pixeles() -> None:
    imagen = Image.new("RGB", (40, 30), (120, 60, 30))
    png, bmp = io.BytesIO(), io.BytesIO()
    imagen.save(png, format="PNG")
    imagen.save(bmp, format="BMP")

    a, b = di.describir(png.getvalue()), di.describir(bmp.getvalue())
    assert a["imagen_sha256_pixeles"] == b["imagen_sha256_pixeles"]
    assert a["imagen_dhash"] == b["imagen_dhash"]
