"""Recolecta candidatos textiles andinos desde la API publica del Art Institute of Chicago (AIC).

Uso desde la raiz del repositorio (requiere internet; la API no pide clave):

    python -m src.collectors.aic_collector                      # escribe en data/raw/aic/
    python -m src.collectors.aic_collector --salida data/metadata/aic_andes_textiles_candidates.csv

Alcance: obras de dominio publico, con imagen, del departamento de Textiles o de
tipo textil, cuyo lugar de origen o estilo cultural es andino. Cada registro se
evalua con el filtro textil del proyecto y recibe una sugerencia de subconjunto
para la revision manual. La lista curada data/metadata/aic_andes_textiles_candidates.csv
es insumo del corpus: si ya existe, solo se reemplaza con --forzar.

Licencias (https://www.artic.edu/image-licensing, https://api.artic.edu/docs/):
imagenes de dominio publico CC0, metadatos CC0, campo description CC BY 4.0.
"""

from __future__ import annotations

import argparse
import html
import re
import time
from datetime import date
from pathlib import Path
from typing import Any

import requests

from src.preprocessing.surface_filters import classify_surface_type, normalize_object_type
from src.preprocessing.textile_filters import ANDEAN_CULTURAL_TERMS, TEXTILE_STRONG_TERMS, evaluate_met_record
from src.utils.archivos import escribir_csv, escribir_jsonl, escribir_texto
from src.utils.http import crear_sesion
from src.utils.texto import buscar_terminos, texto_plano

API_BUSQUEDA = "https://api.artic.edu/api/v1/artworks/search"
IIIF = "https://www.artic.edu/iiif/2/{image_id}/full/{ancho},/0/default.jpg"
URL_OBRA = "https://www.artic.edu/artworks/{id}"
INSUMO_CURADO = Path("data/metadata/aic_andes_textiles_candidates.csv")
REPORTE_INSUMO = Path("outputs/reports/aic_collection_summary.md")
SALIDA_DEFECTO = Path("data/raw/aic/aic_andes_textiles_candidates.csv")

LUGARES_ANDINOS = ["Peru", "Bolivia", "Chile", "Ecuador", "Andes", "South America"]
CULTURAS_ANDINAS = [
    "nazca", "chancay", "inca", "chimú", "chimu", "lambayeque", "huari", "wari", "moche", "paracas",
    "chuquibamba", "tiwanaku", "ica", "recuay", "sihuas", "andean",
]
CAMPOS = [
    "id", "title", "main_reference_number", "date_display", "date_start", "date_end", "place_of_origin",
    "style_title", "artwork_type_title", "department_title", "classification_title", "classification_titles",
    "medium_display", "material_titles", "technique_titles", "term_titles", "dimensions", "description",
    "credit_line", "is_public_domain", "image_id",
]

# Sugerencia inicial de subconjunto segun la utilidad morfologica (classify_surface_type).
SUGERENCIA_POR_SUPERFICIE = {
    "superficie_amplia": "principal",
    "objeto_tridimensional_iconografico": "principal",
    "formato_estrecho": "secundario",
    "borde_o_fragmento_lineal": "secundario",
    "objeto_tridimensional_no_prioritario": "secundario",
    "fragmento_para_revision": "secundario",
    "revision_morfologica": "secundario",
}

COLUMNAS = [
    "fuente",
    "id_fuente",
    "numero_acceso",
    "titulo_original",
    "cultura",
    "fecha_objeto",
    "fecha_inicio",
    "fecha_fin",
    "procedencia",
    "departamento",
    "clasificacion_original",
    "tipo_objeto_original",
    "material",
    "materiales",
    "tecnicas",
    "terminos_fuente",
    "dimensiones",
    "descripcion",
    "linea_credito",
    "url_objeto",
    "url_imagen",
    "url_imagen_miniatura",
    "es_dominio_publico",
    "licencia_imagen",
    "licencia_descripcion",
    "terminos_andinos",
    "terminos_textiles",
    "puntaje_textil",
    "estado_filtro",
    "motivo_filtro",
    "tipo_objeto",
    "tipo_superficie",
    "sugerencia_corpus",
    "motivo_sugerencia",
    "consultas_origen",
    "fecha_descarga",
]


def consulta_alcance() -> dict[str, Any]:
    lugar = [{"match_phrase": {"place_of_origin": lugar}} for lugar in LUGARES_ANDINOS]
    cultura = [{"match": {"style_title": c}} for c in CULTURAS_ANDINAS]
    textil = [
        {"match": {"department_title": "Textiles"}},
        {"match": {"classification_titles": "textile"}},
        {"match": {"artwork_type_title": "Textile"}},
    ]
    return {
        "bool": {
            "must": [
                {"term": {"is_public_domain": True}},
                {"exists": {"field": "image_id"}},
                {"bool": {"should": textil, "minimum_should_match": 1}},
                {"bool": {"should": lugar + cultura, "minimum_should_match": 1}},
            ]
        }
    }


def limpiar_html(valor: Any) -> str:
    return texto_plano(html.unescape(re.sub(r"<[^>]+>", " ", texto_plano(valor))))


def buscar(
    sesion: requests.Session,
    por_pagina: int = 100,
    pausa: float = 1.1,
    maximo: int = 10000,
) -> tuple[list[dict[str, Any]], list[str]]:
    """Pagina la consulta de alcance; avisa si la API anuncia mas resultados que los entregados."""
    registros: list[dict[str, Any]] = []
    avisos: list[str] = []
    pagina, total = 1, None
    while True:
        cuerpo = {"query": consulta_alcance(), "fields": CAMPOS, "limit": por_pagina, "page": pagina}
        respuesta = sesion.post(API_BUSQUEDA, json=cuerpo, timeout=60)
        respuesta.raise_for_status()
        datos = respuesta.json()
        total = datos.get("pagination", {}).get("total", total)
        lote = datos.get("data", [])
        registros.extend(lote)
        time.sleep(pausa)
        if not lote or len(lote) < por_pagina or (total is not None and len(registros) >= total):
            break
        if len(registros) >= maximo:
            avisos.append(f"truncada en {len(registros)} de {total} resultados (maximo={maximo})")
            break
        pagina += 1
    if total is not None and len(registros) < total and not avisos:
        avisos.append(f"la API anuncio {total} resultados y entrego {len(registros)}")
    return registros, avisos


def como_registro_met(obra: dict[str, Any], url_imagen: str) -> dict[str, Any]:
    """Campos de la API del MET que usa el filtro textil del proyecto."""
    return {
        "title": obra.get("title"),
        "classification": texto_plano(obra.get("classification_titles")) or obra.get("classification_title"),
        "medium": obra.get("medium_display"),
        "objectName": obra.get("artwork_type_title"),
        "culture": obra.get("style_title"),
        "country": obra.get("place_of_origin"),
        "department": obra.get("department_title"),
        "tags": [{"term": t} for t in obra.get("term_titles") or []],
        "primaryImage": url_imagen,
    }


def sugerir(estado_filtro: str, tipo_superficie: str) -> tuple[str, str]:
    if estado_filtro.startswith("excluido"):
        return "descartados", f"filtro textil: {estado_filtro}"
    if estado_filtro == "revision_manual":
        return "secundario", "filtro textil: evidencia textil debil, revisar"
    sugerencia = SUGERENCIA_POR_SUPERFICIE.get(tipo_superficie, "secundario")
    return sugerencia, f"tipo de superficie: {tipo_superficie}"


def normalizar(obra: dict[str, Any], fecha_descarga: str) -> dict[str, str]:
    image_id = texto_plano(obra.get("image_id"))
    url_imagen = IIIF.format(image_id=image_id, ancho=1686) if image_id else ""
    descripcion = limpiar_html(obra.get("description"))
    filtro = evaluate_met_record(como_registro_met(obra, url_imagen))

    fila_superficie = {
        "titulo_original": obra.get("title"),
        "nombre_objeto_original": obra.get("artwork_type_title"),
        "material_original": obra.get("medium_display"),
        "clasificacion_original": texto_plano(obra.get("classification_titles")),
        "cultura": obra.get("style_title"),
        "pais": obra.get("place_of_origin"),
    }
    superficie = classify_surface_type(fila_superficie)
    sugerencia, motivo = sugerir(filtro["estado_curacion"], superficie["tipo_superficie"])

    contexto = " ".join(texto_plano(obra.get(c)) for c in ("title", "style_title", "place_of_origin", "medium_display", "description"))
    return {
        "fuente": "Art Institute of Chicago",
        "id_fuente": texto_plano(obra.get("id")),
        "numero_acceso": texto_plano(obra.get("main_reference_number")),
        "titulo_original": texto_plano(obra.get("title")),
        "cultura": texto_plano(obra.get("style_title")),
        "fecha_objeto": texto_plano(obra.get("date_display")),
        "fecha_inicio": texto_plano(obra.get("date_start")),
        "fecha_fin": texto_plano(obra.get("date_end")),
        "procedencia": texto_plano(obra.get("place_of_origin")),
        "departamento": texto_plano(obra.get("department_title")),
        "clasificacion_original": texto_plano(obra.get("classification_titles")) or texto_plano(obra.get("classification_title")),
        "tipo_objeto_original": texto_plano(obra.get("artwork_type_title")),
        "material": texto_plano(obra.get("medium_display")),
        "materiales": texto_plano(obra.get("material_titles")),
        "tecnicas": texto_plano(obra.get("technique_titles")),
        "terminos_fuente": texto_plano(obra.get("term_titles")),
        "dimensiones": texto_plano(obra.get("dimensions")),
        "descripcion": descripcion,
        "linea_credito": texto_plano(obra.get("credit_line")),
        "url_objeto": URL_OBRA.format(id=texto_plano(obra.get("id"))),
        "url_imagen": url_imagen,
        "url_imagen_miniatura": IIIF.format(image_id=image_id, ancho=843) if image_id else "",
        "es_dominio_publico": str(bool(obra.get("is_public_domain"))),
        "licencia_imagen": "CC0" if obra.get("is_public_domain") else "",
        "licencia_descripcion": "CC BY 4.0" if descripcion else "",
        "terminos_andinos": "; ".join(sorted(set(buscar_terminos(contexto, ANDEAN_CULTURAL_TERMS + CULTURAS_ANDINAS)))),
        "terminos_textiles": "; ".join(sorted(set(buscar_terminos(contexto, TEXTILE_STRONG_TERMS)))),
        "puntaje_textil": str(filtro["puntaje_textil"]),
        "estado_filtro": filtro["estado_curacion"],
        "motivo_filtro": filtro["motivo_curacion"],
        "tipo_objeto": normalize_object_type(fila_superficie),
        "tipo_superficie": superficie["tipo_superficie"],
        "sugerencia_corpus": sugerencia,
        "motivo_sugerencia": motivo,
        "consultas_origen": "alcance: lugar o cultura andina + textil + dominio publico + imagen",
        "fecha_descarga": fecha_descarga,
    }


def escribir_reporte(ruta: Path, filas: list[dict[str, str]], avisos: list[str]) -> None:
    def conteo(campo: str) -> list[str]:
        valores: dict[str, int] = {}
        for fila in filas:
            valores[fila[campo] or "(vacio)"] = valores.get(fila[campo] or "(vacio)", 0) + 1
        return [f"| {valor} | {n} |" for valor, n in sorted(valores.items(), key=lambda x: (-x[1], x[0]))]

    lineas = [
        "# Recoleccion Art Institute of Chicago (AIC)",
        "",
        "Generado por `src/collectors/aic_collector.py`. Alcance: obras de dominio publico, con imagen, textiles "
        "y de lugar o cultura andina.",
        "",
        f"- Registros recolectados: {len(filas)}",
        f"- Con descripcion (CC BY 4.0): {sum(bool(f['descripcion']) for f in filas)}",
        "",
    ]
    for campo, titulo in [("estado_filtro", "Filtro textil"), ("sugerencia_corpus", "Sugerencia de subconjunto"),
                          ("cultura", "Cultura (style_title)"), ("tipo_objeto_original", "Tipo de obra AIC")]:
        lineas += [f"## {titulo}", "", "| Valor | Registros |", "|---|---:|"] + conteo(campo) + [""]
    if avisos:
        lineas += ["## Avisos de paginacion", ""] + [f"- {aviso}" for aviso in avisos]
    while lineas and not lineas[-1]:
        lineas.pop()  # cada tabla deja una linea en blanco al final
    escribir_texto(ruta, lineas)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Recolecta candidatos textiles andinos desde el AIC.")
    parser.add_argument("--root", default=".", help="Raiz del repositorio.")
    parser.add_argument("--salida", default=str(SALIDA_DEFECTO), help="CSV de salida, relativo a la raiz.")
    parser.add_argument("--forzar", action="store_true", help=f"Permite reemplazar {INSUMO_CURADO.as_posix()}.")
    parser.add_argument("--pausa", type=float, default=1.1, help="Segundos entre paginas (limite AIC: 60/min).")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    raiz = Path(args.root).resolve()
    salida = Path(args.salida)
    es_insumo = salida.as_posix() == INSUMO_CURADO.as_posix()
    if es_insumo and (raiz / salida).exists() and not args.forzar:
        print(f"{salida.as_posix()} es insumo curado del corpus y no se sobrescribio. Use --forzar si es intencional.")
        return 1

    sesion = crear_sesion()
    obras, avisos = buscar(sesion, pausa=args.pausa)

    fecha = date.today().isoformat()
    filas = sorted((normalizar(obra, fecha) for obra in obras), key=lambda f: int(f["id_fuente"]))

    escribir_jsonl(raiz / "data/raw/aic/aic_andes_textiles_raw.jsonl", obras)
    escribir_csv(raiz / salida, COLUMNAS, filas)
    reporte = raiz / (REPORTE_INSUMO if es_insumo else salida.with_name(salida.stem + "_resumen.md"))
    escribir_reporte(reporte, filas, avisos)

    print(f"Registros AIC: {len(filas)}")
    for aviso in avisos:
        print(f"Aviso: {aviso}")
    print(f"CSV: {raiz / salida}")
    print(f"Reporte: {reporte}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
