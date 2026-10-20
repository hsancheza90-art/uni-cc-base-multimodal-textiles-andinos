"""Recolecta candidatos textiles andinos desde la API publica del MET.

Uso desde la raiz del repositorio (requiere internet):

    python -m src.collectors.met_collector_v2          # escribe en data/raw/met/

Cada objeto descargado se guarda en data/raw/met/objetos/<id>.json (fuera de git);
una corrida interrumpida se reanuda sin volver a pedir los objetos ya guardados.

El corpus MET no se construye desde esta salida: parte del corpus MET v1 congelado
(src/metadata/build_met_corpus_v2.py). El colector sirve para auditar la cobertura de
la busqueda y para ampliar MET en una version futura, como en CMA y AIC.
"""

from __future__ import annotations

import argparse
import json
import os
import time
from collections import Counter
from pathlib import Path
from typing import Any

import requests

from src.utils.archivos import escribir_csv, escribir_jsonl, escribir_texto
from src.utils.http import crear_sesion
from src.utils.texto import buscar_terminos, texto_plano

API_BUSQUEDA = "https://collectionapi.metmuseum.org/public/collection/v1/search"
API_OBJETO = "https://collectionapi.metmuseum.org/public/collection/v1/objects/{object_id}"

CONSULTAS_DEFAULT = [
    "Andes textile",
    "Andean textile",
    "Peru textile",
    "Peruvian textile",
    "Inca textile",
    "Wari textile",
    "Huari textile",
    "Chancay textile",
    "Nasca textile",
    "Nazca textile",
    "Paracas textile",
    "Moche textile",
    "Chimu textile",
    "Tiwanaku textile",
    "Tiahuanaco textile",
    "tunic Peru",
    "mantle Peru",
    "woven Peru",
]

TERMINOS_ANDINOS = {
    "andes", "andean", "peru", "peruvian", "inca", "wari", "huari",
    "chancay", "nasca", "nazca", "paracas", "moche", "chimu",
    "chimú", "tiwanaku", "tiahuanaco", "south coast", "north coast",
    "central coast", "bolivia", "ecuador",
}

TERMINOS_TEXTILES = {
    "textile", "woven", "weaving", "cloth", "cotton", "camelid",
    "wool", "fiber", "fibre", "tapestry", "tunic", "mantle",
    "fragment", "bag", "shirt", "embroidered", "embroidery",
    "feather", "featherwork",
}

COLUMNAS = [
    "fuente",
    "id_fuente",
    "numero_inventario",
    "titulo",
    "cultura",
    "fecha_creacion",
    "clasificacion",
    "tecnica",
    "material",
    "dimensiones",
    "departamento",
    "descripcion",
    "url_objeto",
    "url_imagen",
    "ruta_imagen_local",
    "licencia",
    "tiene_imagen",
    "terminos_andinos",
    "terminos_textiles",
    "estado_curacion",
    "notas_curacion",
    "consultas_origen",
]


ERRORES_RED = (requests.RequestException, json.JSONDecodeError, ValueError)


def pedir_json(
    sesion: requests.Session,
    url: str,
    parametros: dict[str, Any] | None = None,
    timeout: int = 30,
) -> dict[str, Any]:
    respuesta = sesion.get(url, params=parametros, timeout=timeout)
    respuesta.raise_for_status()
    return respuesta.json()


def texto_busqueda(registro: dict[str, Any]) -> str:
    campos = [
        "title",
        "culture",
        "period",
        "dynasty",
        "reign",
        "objectDate",
        "classification",
        "medium",
        "dimensions",
        "department",
        "country",
        "region",
        "subregion",
        "locale",
    ]
    partes = [texto_plano(registro.get(campo)).lower() for campo in campos]

    tags = registro.get("tags") or []
    if isinstance(tags, list):
        partes.extend(texto_plano(tag.get("term", "")).lower() for tag in tags if isinstance(tag, dict))

    return " ".join(partes)


def detectar_terminos(texto_total: str, terminos: set[str]) -> list[str]:
    return sorted(set(buscar_terminos(texto_total, sorted(terminos))))


def normalizar_registro(
    registro: dict[str, Any],
    consultas_origen: list[str],
) -> dict[str, str]:
    texto_total = texto_busqueda(registro)
    terminos_andinos = detectar_terminos(texto_total, TERMINOS_ANDINOS)
    terminos_textiles = detectar_terminos(texto_total, TERMINOS_TEXTILES)

    url_imagen = texto_plano(registro.get("primaryImageSmall") or registro.get("primaryImage"))
    tiene_imagen = bool(url_imagen)

    if not tiene_imagen:
        estado = "descartado_sin_imagen"
        notas = "Registro sin imagen disponible para revision visual."
    elif not terminos_textiles:
        estado = "descartado_no_textil"
        notas = "No se encontro evidencia textil suficiente en los metadatos."
    elif not terminos_andinos:
        estado = "descartado_no_andino"
        notas = "No se encontro evidencia andina suficiente en los metadatos."
    else:
        estado = "candidato"
        notas = "Registro pendiente de clasificacion curatorial y revision visual."

    return {
        "fuente": "The Metropolitan Museum of Art",
        "id_fuente": texto_plano(registro.get("objectID")),
        "numero_inventario": texto_plano(registro.get("accessionNumber")),
        "titulo": texto_plano(registro.get("title")),
        "cultura": texto_plano(registro.get("culture")),
        "fecha_creacion": texto_plano(registro.get("objectDate")),
        "clasificacion": texto_plano(registro.get("classification")),
        "tecnica": "",
        "material": texto_plano(registro.get("medium")),
        "dimensiones": texto_plano(registro.get("dimensions")),
        "departamento": texto_plano(registro.get("department")),
        "descripcion": texto_plano(registro.get("creditLine")),
        "url_objeto": texto_plano(registro.get("objectURL")),
        "url_imagen": url_imagen,
        "ruta_imagen_local": "",  # se completa al descargar la imagen
        "licencia": "Open Access MET, revisar condiciones institucionales",
        "tiene_imagen": str(tiene_imagen),
        "terminos_andinos": "; ".join(terminos_andinos),
        "terminos_textiles": "; ".join(terminos_textiles),
        "estado_curacion": estado,
        "notas_curacion": notas,
        "consultas_origen": "; ".join(sorted(set(consultas_origen))),
    }


def buscar_ids(
    sesion: requests.Session,
    consultas: list[str],
    pausa: float,
    timeout: int,
) -> tuple[dict[int, list[str]], list[str]]:
    mapa: dict[int, list[str]] = {}
    errores: list[str] = []

    for consulta in consultas:
        try:
            datos = pedir_json(sesion, API_BUSQUEDA, {"q": consulta, "hasImages": "true"}, timeout=timeout)
            ids = datos.get("objectIDs") or []
        except ERRORES_RED as exc:
            errores.append(f"{consulta}: {exc}")
            continue

        for object_id in ids:
            mapa.setdefault(int(object_id), []).append(consulta)

        time.sleep(pausa)

    return mapa, errores


def descargar_objetos(
    sesion: requests.Session,
    ids_por_consulta: dict[int, list[str]],
    pausa: float,
    timeout: int,
    cache: Path | None = None,
) -> tuple[dict[int, dict[str, Any]], list[str]]:
    """Descarga cada objeto; si existe en la cache, lo lee del disco sin pedirlo a la API."""
    registros: dict[int, dict[str, Any]] = {}
    errores: list[str] = []

    for object_id in sorted(ids_por_consulta):
        ruta_cache = cache / f"{object_id}.json" if cache else None
        if ruta_cache and ruta_cache.exists():
            registros[object_id] = json.loads(ruta_cache.read_text(encoding="utf-8"))
            continue
        try:
            registros[object_id] = pedir_json(sesion, API_OBJETO.format(object_id=object_id), timeout=timeout)
        except ERRORES_RED as exc:
            errores.append(f"{object_id}: {exc}")
        else:
            if ruta_cache:
                ruta_cache.parent.mkdir(parents=True, exist_ok=True)
                temporal = ruta_cache.with_suffix(".part")
                temporal.write_text(json.dumps(registros[object_id], ensure_ascii=False, sort_keys=True), encoding="utf-8")
                os.replace(temporal, ruta_cache)
        time.sleep(pausa)

    return registros, errores


def escribir_reporte(ruta: Path, filas: list[dict[str, str]], errores: list[str]) -> None:
    conteos = Counter(fila["estado_curacion"] for fila in filas)

    lineas = [
        "# Resumen de recoleccion MET v2",
        "",
        "Fuente: The Metropolitan Museum of Art.",
        "",
        "## Conteos",
        "",
        f"- Registros normalizados: {len(filas)}",
    ]

    for estado, cantidad in sorted(conteos.items()):
        lineas.append(f"- {estado}: {cantidad}")

    candidatos = [fila for fila in filas if fila["estado_curacion"] == "candidato"]
    lineas.extend([
        "",
        "## Muestra de candidatos",
        "",
    ])

    for fila in candidatos[:20]:
        identificador = fila["numero_inventario"] or fila["id_fuente"]
        lineas.append(f"- {identificador}: {fila['titulo']}")

    if errores:
        lineas.extend(["", "## Errores registrados", ""])
        lineas.extend(f"- {error}" for error in errores[:100])

    escribir_texto(ruta, lineas)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Recolecta y normaliza candidatos textiles andinos desde la API publica del MET."
    )
    parser.add_argument("--root", default=".", help="Raiz del repositorio.")
    parser.add_argument("--query", action="append", dest="consultas", help="Consulta adicional o alternativa.")
    parser.add_argument("--sleep", type=float, default=0.15, help="Pausa entre solicitudes.")
    parser.add_argument("--timeout", type=int, default=30, help="Timeout HTTP en segundos.")
    parser.add_argument("--salida", default="data/raw/met/met_candidatos_v2.csv", help="CSV de salida, relativo a la raiz.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    raiz = Path(args.root).resolve()
    consultas = args.consultas or CONSULTAS_DEFAULT
    sesion = crear_sesion()

    ids_por_consulta, errores_busqueda = buscar_ids(
        sesion,
        consultas=consultas,
        pausa=args.sleep,
        timeout=args.timeout,
    )

    registros, errores_objetos = descargar_objetos(
        sesion,
        ids_por_consulta=ids_por_consulta,
        pausa=args.sleep,
        timeout=args.timeout,
        cache=raiz / "data/raw/met/objetos",
    )

    filas = [
        normalizar_registro(registro, ids_por_consulta[object_id])
        for object_id, registro in sorted(registros.items())
    ]

    ruta_jsonl = raiz / "data/raw/met/met_objetos_crudos_v2.jsonl"
    ruta_csv = raiz / args.salida
    ruta_reporte = ruta_csv.with_name(ruta_csv.stem + "_resumen.md")

    escribir_jsonl(ruta_jsonl, list(registros.values()))
    escribir_csv(ruta_csv, COLUMNAS, filas)
    escribir_reporte(ruta_reporte, filas, errores_busqueda + errores_objetos)

    print(f"Objetos MET encontrados: {len(ids_por_consulta)}")
    print(f"Objetos MET descargados: {len(registros)}")
    print(f"CSV normalizado: {ruta_csv}")
    print(f"JSONL crudo: {ruta_jsonl}")
    print(f"Reporte: {ruta_reporte}")

    errores = errores_busqueda + errores_objetos
    if errores:
        print(f"Errores registrados: {len(errores)} (ver reporte)")
    return 1 if errores else 0


if __name__ == "__main__":
    raise SystemExit(main())
