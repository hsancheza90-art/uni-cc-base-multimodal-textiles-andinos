"""Descarga las imagenes del corpus consolidado y escribe su manifiesto.

Uso desde la raiz del repositorio (requiere acceso a internet):

    python -m src.imagenes.descargar_imagenes
    python -m src.imagenes.descargar_imagenes --limite 5     # prueba corta

Las imagenes se guardan en data/images/<fuente>/<id_fuente>.<ext> (fuera de git).
El manifiesto data/metadata/imagenes_manifiesto_met_cma_v1.csv si se versiona:
registra la URL descargada, el SHA-256, las dimensiones y el dHash de cada imagen.
Una imagen ya descargada cuyo SHA-256 coincide con el manifiesto no se vuelve a pedir.

Para MET se descarga la version web-large (url_imagen_miniatura) en lugar del
original de alta resolucion; para CMA, la version web que entrega la API.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import os
import time
from datetime import date
from pathlib import Path

import requests
from PIL import Image
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from src.consolidado.construir_consolidado import (
    COLUMNAS_MANIFIESTO,
    MANIFIESTO_IMAGENES,
    construir_registros_base,
    escribir_csv,
    indexar,
    leer_csv,
)

USER_AGENT = (
    "uni-cc-base-multimodal-textiles-andinos/2.0 "
    "(investigacion academica; https://github.com/hsancheza90-art/uni-cc-base-multimodal-textiles-andinos)"
)
EXTENSIONES = {"JPEG": "jpg", "PNG": "png", "GIF": "gif", "WEBP": "webp", "TIFF": "tif"}
TAMANO_MAXIMO = 50 * 1024 * 1024
CAMPOS_DESCRIPTIVOS = ("formato", "imagen_ancho", "imagen_alto", "imagen_dhash", "imagen_sha256_pixeles")


def crear_sesion() -> requests.Session:
    reintentos = Retry(
        total=5,
        backoff_factor=1.0,
        status_forcelist=(408, 429, 500, 502, 503, 504),
        allowed_methods=("GET",),
        respect_retry_after_header=True,
    )
    sesion = requests.Session()
    sesion.headers["User-Agent"] = USER_AGENT
    sesion.mount("https://", HTTPAdapter(max_retries=reintentos))
    return sesion


def dhash(imagen: Image.Image) -> str:
    """Hash perceptual por diferencias horizontales (64 bits, hexadecimal)."""
    gris = imagen.convert("L").resize((9, 8), Image.Resampling.LANCZOS)
    pixeles = gris.tobytes()
    bits = 0
    for fila in range(8):
        for columna in range(8):
            izquierda = pixeles[fila * 9 + columna]
            derecha = pixeles[fila * 9 + columna + 1]
            bits = (bits << 1) | int(izquierda > derecha)
    return f"{bits:016x}"


def urls_a_descargar(registro: dict[str, str]) -> list[str]:
    """Version reducida primero; si no existe, la imagen institucional original."""
    urls = [registro["url_imagen_miniatura"], registro["url_imagen"]]
    return [url for i, url in enumerate(urls) if url and url not in urls[:i]]


def describir(contenido: bytes) -> dict[str, str]:
    with Image.open(io.BytesIO(contenido)) as imagen:
        imagen.verify()
    with Image.open(io.BytesIO(contenido)) as imagen:
        imagen.load()
        rgb = imagen.convert("RGB")
        return {
            "formato": imagen.format or "",
            "imagen_ancho": str(imagen.width),
            "imagen_alto": str(imagen.height),
            "imagen_dhash": dhash(imagen),
            # Identifica la misma fotografia servida con bytes o URL distintos.
            "imagen_sha256_pixeles": hashlib.sha256(f"{rgb.size}".encode() + rgb.tobytes()).hexdigest(),
        }


def escribir_atomico(ruta: Path, contenido: bytes) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    temporal = ruta.with_suffix(ruta.suffix + ".part")
    temporal.write_bytes(contenido)
    os.replace(temporal, ruta)


def vigente(raiz: Path, previo: dict[str, str] | None, urls: list[str]) -> bool:
    if not previo or previo["estado_descarga"] != "ok" or previo["url_descargada"] not in urls:
        return False
    ruta = raiz / previo["ruta_imagen_local"]
    return ruta.exists() and hashlib.sha256(ruta.read_bytes()).hexdigest() == previo["imagen_sha256"]


def descargar(sesion: requests.Session, raiz: Path, registro: dict[str, str], urls: list[str]) -> dict[str, str]:
    fila = {campo: "" for campo in COLUMNAS_MANIFIESTO}
    fila.update({"id_global": registro["id_global"], "fecha_descarga": date.today().isoformat()})
    errores: list[str] = []
    for url in urls:
        fila["url_descargada"] = url
        try:
            respuesta = sesion.get(url, timeout=(10, 60))
            fila["http_estado"] = str(respuesta.status_code)
            respuesta.raise_for_status()
            contenido = respuesta.content
            if len(contenido) > TAMANO_MAXIMO:
                raise ValueError(f"imagen de {len(contenido)} bytes supera el maximo")
            datos = describir(contenido)
            break
        except (requests.RequestException, OSError, ValueError) as error:
            errores.append(f"{url}: {type(error).__name__}: {error}")
    else:
        fila["estado_descarga"] = "error"
        fila["error"] = " | ".join(errores)[:500]
        return fila

    if errores:
        fila["error"] = ("Respaldo tras fallo: " + " | ".join(errores))[:500]

    extension = EXTENSIONES.get(datos["formato"], "img")
    relativa = Path("data/images") / registro["fuente"].lower() / f"{registro['id_fuente']}.{extension}"
    escribir_atomico(raiz / relativa, contenido)
    fila.update(datos)
    fila.update({
        "ruta_imagen_local": relativa.as_posix(),
        "estado_descarga": "ok",
        "bytes": str(len(contenido)),
        "imagen_sha256": hashlib.sha256(contenido).hexdigest(),
    })
    return fila


def ejecutar(raiz: Path, limite: int | None, pausa: float) -> int:
    registros = construir_registros_base(raiz)
    if limite:
        registros = registros[:limite]

    ruta_manifiesto = raiz / MANIFIESTO_IMAGENES
    previos = indexar(leer_csv(ruta_manifiesto), "id_global") if ruta_manifiesto.exists() else {}

    sesion = crear_sesion()
    filas: dict[str, dict[str, str]] = dict(previos)
    descargadas = reutilizadas = errores = 0
    for numero, registro in enumerate(registros, start=1):
        urls = urls_a_descargar(registro)
        previo = previos.get(registro["id_global"])
        if vigente(raiz, previo, urls):
            # Completa desde el archivo local los campos que el manifiesto aun no tenga.
            if any(not previo.get(campo) for campo in CAMPOS_DESCRIPTIVOS):
                filas[registro["id_global"]] = {
                    **{campo: "" for campo in COLUMNAS_MANIFIESTO},
                    **previo,
                    **describir((raiz / previo["ruta_imagen_local"]).read_bytes()),
                }
            reutilizadas += 1
            continue
        fila = descargar(sesion, raiz, registro, urls)
        filas[registro["id_global"]] = fila
        if fila["estado_descarga"] == "ok":
            descargadas += 1
        else:
            errores += 1
            print(f"  error {registro['id_global']}: {fila['error']}")
        if numero % 25 == 0:
            print(f"  {numero}/{len(registros)} procesados")
        time.sleep(pausa)

    orden = {registro["id_global"]: i for i, registro in enumerate(construir_registros_base(raiz))}
    salida = sorted(filas.values(), key=lambda fila: orden.get(fila["id_global"], len(orden)))
    escribir_csv(ruta_manifiesto, COLUMNAS_MANIFIESTO, salida)

    print(f"Descargadas: {descargadas} | reutilizadas: {reutilizadas} | errores: {errores}")
    print(f"Manifiesto: {ruta_manifiesto}")
    return 1 if errores else 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Descarga las imagenes del corpus consolidado MET+CMA v1.0.")
    parser.add_argument("--root", default=".", help="Raiz del repositorio.")
    parser.add_argument("--limite", type=int, default=None, help="Procesa solo los primeros N registros.")
    parser.add_argument("--pausa", type=float, default=0.3, help="Segundos de espera entre descargas.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    return ejecutar(Path(args.root).resolve(), args.limite, args.pausa)


if __name__ == "__main__":
    raise SystemExit(main())
