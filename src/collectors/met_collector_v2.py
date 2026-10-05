from __future__ import annotations

import argparse
import csv
import json
import time
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


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


def pedir_json(url: str, timeout: int = 30) -> dict[str, Any]:
    solicitud = Request(url, headers={"User-Agent": "uni-cc-textiles-andinos/0.2"})
    with urlopen(solicitud, timeout=timeout) as respuesta:
        return json.loads(respuesta.read().decode("utf-8"))


def construir_url(base: str, parametros: dict[str, Any]) -> str:
    return f"{base}?{urlencode(parametros)}"


def texto(valor: Any) -> str:
    if valor is None:
        return ""
    if isinstance(valor, str):
        return " ".join(valor.split())
    if isinstance(valor, list):
        return "; ".join(texto(x) for x in valor if texto(x))
    return str(valor)


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
    partes = [texto(registro.get(campo)).lower() for campo in campos]

    tags = registro.get("tags") or []
    if isinstance(tags, list):
        partes.extend(texto(tag.get("term", "")).lower() for tag in tags if isinstance(tag, dict))

    return " ".join(partes)


def detectar_terminos(texto_total: str, terminos: set[str]) -> list[str]:
    return sorted(termino for termino in terminos if termino in texto_total)


def normalizar_registro(
    registro: dict[str, Any],
    consultas_origen: list[str],
    ruta_imagen_local: str = "",
) -> dict[str, str]:
    texto_total = texto_busqueda(registro)
    terminos_andinos = detectar_terminos(texto_total, TERMINOS_ANDINOS)
    terminos_textiles = detectar_terminos(texto_total, TERMINOS_TEXTILES)

    url_imagen = texto(registro.get("primaryImageSmall") or registro.get("primaryImage"))
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
        "id_fuente": texto(registro.get("objectID")),
        "numero_inventario": texto(registro.get("accessionNumber")),
        "titulo": texto(registro.get("title")),
        "cultura": texto(registro.get("culture")),
        "fecha_creacion": texto(registro.get("objectDate")),
        "clasificacion": texto(registro.get("classification")),
        "tecnica": "",
        "material": texto(registro.get("medium")),
        "dimensiones": texto(registro.get("dimensions")),
        "departamento": texto(registro.get("department")),
        "descripcion": texto(registro.get("creditLine")),
        "url_objeto": texto(registro.get("objectURL")),
        "url_imagen": url_imagen,
        "ruta_imagen_local": ruta_imagen_local,
        "licencia": "Open Access MET, revisar condiciones institucionales",
        "tiene_imagen": str(tiene_imagen),
        "terminos_andinos": "; ".join(terminos_andinos),
        "terminos_textiles": "; ".join(terminos_textiles),
        "estado_curacion": estado,
        "notas_curacion": notas,
        "consultas_origen": "; ".join(sorted(set(consultas_origen))),
    }


def buscar_ids(consultas: list[str], pausa: float, timeout: int) -> tuple[dict[int, list[str]], list[str]]:
    mapa: dict[int, list[str]] = {}
    errores: list[str] = []

    for consulta in consultas:
        url = construir_url(API_BUSQUEDA, {"q": consulta, "hasImages": "true"})
        try:
            datos = pedir_json(url, timeout=timeout)
            ids = datos.get("objectIDs") or []
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
            errores.append(f"{consulta}: {exc}")
            continue

        for object_id in ids:
            mapa.setdefault(int(object_id), []).append(consulta)

        time.sleep(pausa)

    return mapa, errores


def descargar_objetos(
    ids_por_consulta: dict[int, list[str]],
    pausa: float,
    timeout: int,
) -> tuple[dict[int, dict[str, Any]], list[str]]:
    registros: dict[int, dict[str, Any]] = {}
    errores: list[str] = []

    for object_id in sorted(ids_por_consulta):
        url = API_OBJETO.format(object_id=object_id)
        try:
            registros[object_id] = pedir_json(url, timeout=timeout)
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
            errores.append(f"{object_id}: {exc}")
        time.sleep(pausa)

    return registros, errores


def escribir_jsonl(ruta: Path, registros: dict[int, dict[str, Any]]) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("w", encoding="utf-8") as archivo:
        for registro in registros.values():
            archivo.write(json.dumps(registro, ensure_ascii=False, sort_keys=True) + "\n")


def escribir_csv(ruta: Path, filas: list[dict[str, str]]) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=COLUMNAS)
        escritor.writeheader()
        escritor.writerows(filas)


def escribir_reporte(ruta: Path, filas: list[dict[str, str]], errores: list[str]) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)

    conteos: dict[str, int] = {}
    for fila in filas:
        estado = fila["estado_curacion"]
        conteos[estado] = conteos.get(estado, 0) + 1

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

    ruta.write_text("\n".join(lineas) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Recolecta y normaliza candidatos textiles andinos desde la API publica del MET."
    )
    parser.add_argument("--root", default=".", help="Raiz del repositorio.")
    parser.add_argument("--query", action="append", dest="consultas", help="Consulta adicional o alternativa.")
    parser.add_argument("--sleep", type=float, default=0.15, help="Pausa entre solicitudes.")
    parser.add_argument("--timeout", type=int, default=30, help="Timeout HTTP en segundos.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    raiz = Path(args.root).resolve()
    consultas = args.consultas or CONSULTAS_DEFAULT

    ids_por_consulta, errores_busqueda = buscar_ids(
        consultas=consultas,
        pausa=args.sleep,
        timeout=args.timeout,
    )

    registros, errores_objetos = descargar_objetos(
        ids_por_consulta=ids_por_consulta,
        pausa=args.sleep,
        timeout=args.timeout,
    )

    filas = [
        normalizar_registro(registro, ids_por_consulta[object_id])
        for object_id, registro in sorted(registros.items())
    ]

    ruta_jsonl = raiz / "data/raw/met/met_objetos_crudos_v2.jsonl"
    ruta_csv = raiz / "data/metadata/met_candidatos_v2.csv"
    ruta_reporte = raiz / "outputs/reports/met_resumen_recoleccion_v2.md"

    escribir_jsonl(ruta_jsonl, registros)
    escribir_csv(ruta_csv, filas)
    escribir_reporte(ruta_reporte, filas, errores_busqueda + errores_objetos)

    print(f"Objetos MET encontrados: {len(ids_por_consulta)}")
    print(f"Objetos MET descargados: {len(registros)}")
    print(f"CSV normalizado: {ruta_csv}")
    print(f"JSONL crudo: {ruta_jsonl}")
    print(f"Reporte: {ruta_reporte}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())