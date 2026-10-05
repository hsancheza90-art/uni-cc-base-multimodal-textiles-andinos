"""Sesion HTTP comun para las APIs de museos: reintentos, espera progresiva y User-Agent."""

from __future__ import annotations

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

USER_AGENT = (
    "uni-cc-base-multimodal-textiles-andinos/2.0 "
    "(investigacion academica; https://github.com/hsancheza90-art/uni-cc-base-multimodal-textiles-andinos)"
)


def crear_sesion(reintentos: int = 5, espera: float = 1.0) -> requests.Session:
    """Reintenta 408, 429 y 5xx con espera exponencial y respeta Retry-After."""
    politica = Retry(
        total=reintentos,
        backoff_factor=espera,
        status_forcelist=(408, 429, 500, 502, 503, 504),
        allowed_methods=("GET",),
        respect_retry_after_header=True,
    )
    sesion = requests.Session()
    sesion.headers.update({"User-Agent": USER_AGENT, "Accept": "application/json, image/*;q=0.9, */*;q=0.8"})
    adaptador = HTTPAdapter(max_retries=politica)
    sesion.mount("https://", adaptador)
    sesion.mount("http://", adaptador)
    return sesion
