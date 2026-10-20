"""Descarga las imagenes de evaluacion de todos los candidatos MET, CMA y AIC.

Uso desde la raiz del repositorio (requiere acceso a internet):

    python -m src.imagenes.descargar_evaluacion
    python -m src.imagenes.descargar_evaluacion --fuente aic --limite 5    # prueba corta

A diferencia de descargar_imagenes (copias web del consolidado v1), aqui se pide
la mejor imagen institucional disponible de cada candidato, incluidos los
descartados, para medir su aptitud analitica (src/imagenes/aptitud.py):

- MET: el original de alta resolucion (url_imagen).
- CMA: la version de impresion (_print.jpg); si falla, la version web.
- AIC: la imagen IIIF de 1686 px de ancho que recomienda el museo; si el original
  es mas angosto, la de 843 px o la del ancho original que informa la API.

Del original solo se registran sus dimensiones y su SHA-256. Se guarda una copia
de evaluacion reducida a 1600 px de lado mayor en data/images/evaluacion/<fuente>/
(fuera de git). El manifiesto data/metadata/imagenes_evaluacion_manifiesto_v2.csv
si se versiona. Una copia ya descargada cuyo SHA-256 coincide no se vuelve a pedir.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import threading
import time
from collections.abc import Iterator
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

import requests
from PIL import Image

from src.imagenes.descargar_imagenes import TAMANO_MAXIMO, escribir_atomico
from src.utils.archivos import escribir_csv, indexar, leer_csv
from src.utils.fuentes import FUENTES
from src.utils.http import crear_sesion

MANIFIESTO_EVALUACION = "data/metadata/imagenes_evaluacion_manifiesto_v2.csv"
CARPETA_EVALUACION = Path("data/images/evaluacion")
LADO_EVALUACION = 1600
CALIDAD_JPEG = 95

ENTRADAS_MET = FUENTES["MET"].revisados
ENTRADA_CMA = "data/metadata/cma_andes_textiles_candidates.csv"
ENTRADA_AIC = "data/metadata/aic_andes_textiles_candidates.csv"

# Hilos y pausa por fuente: la API del AIC admite 60 peticiones por minuto.
POLITICA = {"MET": (4, 0.0), "CMA": (4, 0.0), "AIC": (1, 1.05)}
ORDEN_FUENTES = {"MET": 0, "CMA": 1, "AIC": 2}
API_AIC = "https://api.artic.edu/api/v1/artworks/{id_fuente}?fields=id,thumbnail"

COLUMNAS_MANIFIESTO_EVALUACION = [
    "id_global",
    "fuente",
    "id_fuente",
    "url_descargada",
    "estado_descarga",
    "http_estado",
    "bytes_original",
    "sha256_original",
    "ancho_original",
    "alto_original",
    "ruta_copia_evaluacion",
    "ancho_copia",
    "alto_copia",
    "sha256_copia",
    "fecha_descarga",
    "error",
]

# Los originales del MET superan el limite de Pillow contra imagenes maliciosas;
# las fuentes son APIs institucionales, asi que se amplia el limite.
Image.MAX_IMAGE_PIXELS = 400_000_000


def candidatos_evaluacion(raiz: Path) -> list[dict]:
    """Todos los candidatos evaluados de las tres fuentes, con sus URL en orden de preferencia."""
    candidatos: list[dict] = []
    for entrada in ENTRADAS_MET:
        for fila in leer_csv(raiz / entrada):
            candidatos.append({"fuente": "MET", "id_fuente": fila["id_fuente"], "urls": [fila["url_imagen"]]})
    for fila in leer_csv(raiz / ENTRADA_CMA):
        web = fila["image_url"]
        impresion = web.replace("_web.jpg", "_print.jpg") if web.endswith("_web.jpg") else ""
        candidatos.append({"fuente": "CMA", "id_fuente": fila["source_id"], "urls": [impresion, web]})
    for fila in leer_csv(raiz / ENTRADA_AIC):
        # Algunas imagenes solo se sirven a 843 px: a 1686 px el IIIF responde 403.
        candidatos.append({"fuente": "AIC", "id_fuente": fila["id_fuente"], "urls": [fila["url_imagen"], fila["url_imagen_miniatura"]]})
    for candidato in candidatos:
        candidato["id_global"] = f"{candidato['fuente']}:{candidato['id_fuente']}"
        # Algunas URL del MET contienen espacios: por eso se guardan en lista, sin separadores.
        candidato["urls"] = [url for url in candidato["urls"] if url]
    indexar(candidatos, "id_global")
    return candidatos


def copia_evaluacion(contenido: bytes) -> tuple[dict[str, str], bytes]:
    """Mide el original y devuelve una copia JPEG de LADO_EVALUACION px de lado mayor."""
    with Image.open(io.BytesIO(contenido)) as imagen:
        imagen.verify()
    with Image.open(io.BytesIO(contenido)) as imagen:
        ancho, alto = imagen.size
        # En JPEG, draft decodifica a una escala reducida y evita cargar el original completo.
        imagen.draft("RGB", (LADO_EVALUACION, LADO_EVALUACION))
        rgb = imagen.convert("RGB")
    escala = LADO_EVALUACION / max(rgb.size)
    if escala < 1:
        rgb = rgb.resize((round(rgb.width * escala), round(rgb.height * escala)), Image.Resampling.LANCZOS)
    salida = io.BytesIO()
    rgb.save(salida, format="JPEG", quality=CALIDAD_JPEG)
    copia = salida.getvalue()
    datos = {
        "ancho_original": str(ancho),
        "alto_original": str(alto),
        "ancho_copia": str(rgb.width),
        "alto_copia": str(rgb.height),
        "sha256_copia": hashlib.sha256(copia).hexdigest(),
    }
    return datos, copia


def vigente(raiz: Path, previo: dict[str, str] | None, urls: list[str]) -> bool:
    if not previo or previo["estado_descarga"] != "ok" or not misma_imagen(previo["url_descargada"], urls):
        return False
    ruta = raiz / previo["ruta_copia_evaluacion"]
    return ruta.exists() and hashlib.sha256(ruta.read_bytes()).hexdigest() == previo["sha256_copia"]


def urls_intento(sesion: requests.Session, candidato: dict) -> Iterator[str]:
    """URL del candidato y, para AIC, la del ancho original, que solo se consulta si las demas fallan.

    El IIIF del AIC responde 403 si se pide un ancho mayor que el de la imagen original
    (por ejemplo, 843 px de una imagen de 810 px); la API informa ese ancho en thumbnail.width.
    """
    yield from candidato["urls"]
    if candidato["fuente"] != "AIC" or not candidato["urls"]:
        return
    try:
        respuesta = sesion.get(API_AIC.format(id_fuente=candidato["id_fuente"]), timeout=(10, 60))
        respuesta.raise_for_status()
        ancho = ((respuesta.json().get("data") or {}).get("thumbnail") or {}).get("width")
    except (requests.RequestException, ValueError):
        return  # el error de las URL anteriores queda registrado en el manifiesto
    if ancho:
        yield f"{candidato['urls'][0].split('/full/')[0]}/full/{int(ancho)},/0/default.jpg"


def misma_imagen(url: str, urls: list[str]) -> bool:
    """Compara sin el tamano pedido al IIIF: la misma imagen puede descargarse a otro ancho."""
    return any(url.split("/full/")[0] == otra.split("/full/")[0] for otra in urls)


def descargar(sesion: requests.Session, raiz: Path, candidato: dict) -> dict[str, str]:
    fila = {campo: "" for campo in COLUMNAS_MANIFIESTO_EVALUACION}
    fila.update({campo: candidato[campo] for campo in ("id_global", "fuente", "id_fuente")})
    fila["fecha_descarga"] = date.today().isoformat()
    errores: list[str] = []
    for url in urls_intento(sesion, candidato):
        fila["url_descargada"] = url
        try:
            respuesta = sesion.get(url, timeout=(10, 120))
            fila["http_estado"] = str(respuesta.status_code)
            respuesta.raise_for_status()
            contenido = respuesta.content
            if len(contenido) > TAMANO_MAXIMO:
                raise ValueError(f"imagen de {len(contenido)} bytes supera el maximo")
            datos, copia = copia_evaluacion(contenido)
            break
        except (requests.RequestException, OSError, ValueError, Image.DecompressionBombError) as error:
            errores.append(f"{url}: {type(error).__name__}: {error}")
    else:
        fila["estado_descarga"] = "error" if candidato["urls"] else "sin_url"
        fila["error"] = " | ".join(errores)[:500]
        return fila

    if errores:
        fila["error"] = ("Respaldo tras fallo: " + " | ".join(errores))[:500]
    relativa = CARPETA_EVALUACION / candidato["fuente"].lower() / f"{candidato['id_fuente']}.jpg"
    escribir_atomico(raiz / relativa, copia)
    fila.update(datos)
    fila.update({
        "ruta_copia_evaluacion": relativa.as_posix(),
        "estado_descarga": "ok",
        "bytes_original": str(len(contenido)),
        "sha256_original": hashlib.sha256(contenido).hexdigest(),
    })
    return fila


def ejecutar(raiz: Path, fuentes: list[str], limite: int | None) -> int:
    ruta_manifiesto = raiz / MANIFIESTO_EVALUACION
    previos = indexar(leer_csv(ruta_manifiesto), "id_global") if ruta_manifiesto.exists() else {}
    filas: dict[str, dict[str, str]] = dict(previos)
    candidatos = candidatos_evaluacion(raiz)
    orden = {c["id_global"]: i for i, c in enumerate(candidatos)}
    errores = 0

    def guardar() -> int:
        salida = sorted(filas.values(), key=lambda f: (ORDEN_FUENTES[f["fuente"]], orden.get(f["id_global"], len(orden))))
        escribir_csv(ruta_manifiesto, COLUMNAS_MANIFIESTO_EVALUACION, salida)
        return len(salida)

    for fuente in fuentes:
        pendientes = [c for c in candidatos if c["fuente"] == fuente]
        if limite:
            pendientes = pendientes[:limite]
        pendientes = [c for c in pendientes if not vigente(raiz, previos.get(c["id_global"]), c["urls"])]
        hilos, pausa = POLITICA[fuente]
        print(f"{fuente}: {len(pendientes)} por descargar ({hilos} hilos, pausa {pausa} s)")

        local = threading.local()
        cerrojo = threading.Lock()
        hechos = 0

        def tarea(candidato: dict) -> dict[str, str]:
            nonlocal hechos
            if not hasattr(local, "sesion"):
                local.sesion = crear_sesion()
            fila = descargar(local.sesion, raiz, candidato)
            time.sleep(pausa)
            with cerrojo:
                hechos += 1
                if hechos % 25 == 0:
                    print(f"  {fuente}: {hechos}/{len(pendientes)}")
            return fila

        with ThreadPoolExecutor(max_workers=hilos) as ejecutor:
            for numero, fila in enumerate(ejecutor.map(tarea, pendientes), start=1):
                filas[fila["id_global"]] = fila
                if fila["estado_descarga"] != "ok":
                    errores += 1
                    print(f"  error {fila['id_global']}: {fila['error']}")
                if numero % 25 == 0:
                    guardar()  # una interrupcion no obliga a repetir lo ya descargado

    total = guardar()
    print(f"Registros en el manifiesto: {total} | errores en esta ejecucion: {errores}")
    print(f"Manifiesto: {ruta_manifiesto}")
    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Descarga las imagenes de evaluacion de los candidatos MET, CMA y AIC.")
    parser.add_argument("--root", default=".", help="Raiz del repositorio.")
    parser.add_argument("--fuente", choices=["met", "cma", "aic"], action="append", help="Fuente(s) a descargar; por defecto, todas.")
    parser.add_argument("--limite", type=int, default=None, help="Procesa solo los primeros N candidatos de cada fuente.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    fuentes = [f.upper() for f in args.fuente] if args.fuente else list(ORDEN_FUENTES)
    return ejecutar(Path(args.root).resolve(), fuentes, args.limite)


if __name__ == "__main__":
    raise SystemExit(main())
