"""Pruebas de los colectores con una sesion HTTP simulada (sin red)."""

from __future__ import annotations

from pathlib import Path

import requests

from src.collectors import cma_collector


class Respuesta:
    def __init__(self, datos: dict, estado: int = 200) -> None:
        self.datos = datos
        self.status_code = estado

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise requests.HTTPError(f"{self.status_code} Error")

    def json(self) -> dict:
        return self.datos


class SesionFalsa:
    def __init__(self, responder) -> None:
        self.responder = responder
        self.llamadas: list[tuple[str, dict | None]] = []

    def get(self, url: str, params: dict | None = None, timeout: object = None) -> Respuesta:
        self.llamadas.append((url, dict(params) if params else None))
        return self.responder(url, params or {})


def pagina_cma(total: int):
    def responder(url: str, params: dict) -> Respuesta:
        inicio, limite = params["skip"], params["limit"]
        ids = range(inicio, min(inicio + limite, total))
        return Respuesta({"info": {"total": total}, "data": [{"id": i} for i in ids]})

    return responder


def test_cma_pagina_hasta_el_total() -> None:
    sesion = SesionFalsa(pagina_cma(total=25))
    registros, _, avisos = cma_collector.fetch_cma_records(["q"], limit_per_query=10, sleep_seconds=0, session=sesion)

    assert len(registros) == 25
    assert [params["skip"] for _, params in sesion.llamadas] == [0, 10, 20]
    assert avisos == []


def test_cma_avisa_si_trunca() -> None:
    sesion = SesionFalsa(pagina_cma(total=50))
    registros, _, avisos = cma_collector.fetch_cma_records(
        ["q"], limit_per_query=10, sleep_seconds=0, session=sesion, max_per_query=20
    )

    assert len(registros) == 20
    assert avisos and "truncada en 20 de 50" in avisos[0]


def test_cma_no_sobrescribe_el_insumo_curado(tmp_path: Path) -> None:
    insumo = tmp_path / cma_collector.INSUMO_CURADO
    insumo.parent.mkdir(parents=True)
    insumo.write_text("lista curada", encoding="utf-8")

    codigo = cma_collector.main(["--root", str(tmp_path), "--salida", cma_collector.INSUMO_CURADO.as_posix()])

    assert codigo == 1
    assert insumo.read_text(encoding="utf-8") == "lista curada"
