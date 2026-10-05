"""Construye el corpus consolidado MET+CMA v1.0 con el esquema armonizado.

Entradas (todas versionadas):
- MET v2 revisado (principal y secundario) + inventario base MET + corpus MET v1.
- CMA v2 revisado (principal y secundario) + candidatos CMA normalizados.
- Manifiesto de imagenes descargadas (src/imagenes/descargar_imagenes.py).

Salidas:
- data/processed/corpus_textiles_andinos_met_cma_v1_consolidado.csv
- data/processed/corpus_textiles_andinos_met_cma_v1_fuentes_licencias.csv
- data/processed/corpus_textiles_andinos_met_cma_v1_sha256.txt
- outputs/reports/corpus_textiles_andinos_met_cma_v1_resumen.md
- docs/esquema_consolidado_met_cma_v1.md
"""

from __future__ import annotations

import argparse
import csv
import hashlib
from collections import Counter, defaultdict
from pathlib import Path

from src.consolidado.esquema import (
    COLUMNAS,
    DECISIONES_VALIDAS,
    ESQUEMA,
    ESTADOS_IMAGEN_VALIDOS,
    ESTADOS_LICENCIA_VALIDOS,
    ESTADOS_METADATOS_VALIDOS,
    OBLIGATORIOS,
)
from src.preprocessing.normalizacion import normalizar_material, normalizar_tecnica
from src.preprocessing.surface_filters import normalize_object_type, nucleo_titulo
from src.utils.config import leer_config

# Valores de reglas que no aportan un tipo de objeto concreto.
TIPOS_SIN_DETERMINAR = {"tipo_no_determinado"}

MET_REVISADOS = {
    "principal": "data/metadata/met_corpus_principal_v2_revisado.csv",
    "complementario": "data/metadata/met_corpus_secundario_v2_revisado.csv",
}
MET_INVENTARIO = "data/processed/corpus_met_textiles_andinos_v1_inventario_base.csv"
MET_V1 = [
    "data/processed/corpus_met_textiles_andinos_v1_principal.csv",
    "data/processed/corpus_met_textiles_andinos_v1_complementario.csv",
]
CMA_REVISADOS = {
    "principal": "data/metadata/cma_corpus_principal_revisado.csv",
    "complementario": "data/metadata/cma_corpus_secundario_revisado.csv",
}
CMA_CANDIDATOS = "data/metadata/cma_andes_textiles_candidates.csv"

MANIFIESTO_IMAGENES = "data/metadata/imagenes_manifiesto_met_cma_v1.csv"
SALIDA_CONSOLIDADO = "data/processed/corpus_textiles_andinos_met_cma_v1_consolidado.csv"
SALIDA_FUENTES = "data/processed/corpus_textiles_andinos_met_cma_v1_fuentes_licencias.csv"
SALIDA_SHA256 = "data/processed/corpus_textiles_andinos_met_cma_v1_sha256.txt"
SALIDA_REPORTE = "outputs/reports/corpus_textiles_andinos_met_cma_v1_resumen.md"
SALIDA_ESQUEMA = "docs/esquema_consolidado_met_cma_v1.md"

ORDEN_FUENTES = {"MET": 0, "CMA": 1}

FUENTES_LICENCIAS = [
    {
        "fuente": "MET",
        "institucion": "The Metropolitan Museum of Art",
        "pais": "USA",
        "tipo_acceso": "Open Access",
        "estado_licencia": "dominio_publico",
        "campo_licencia_fuente": "isPublicDomain",
        "url_politica": "https://www.metmuseum.org/hubs/open-access",
        "api": "https://collectionapi.metmuseum.org/public/collection/v1/",
    },
    {
        "fuente": "CMA",
        "institucion": "Cleveland Museum of Art",
        "pais": "USA",
        "tipo_acceso": "Open Access",
        "estado_licencia": "cc0",
        "campo_licencia_fuente": "share_license_status",
        "url_politica": "https://www.clevelandart.org/open-access",
        "api": "https://openaccess-api.clevelandart.org/api/artworks/",
    },
]
COLUMNAS_FUENTES = list(FUENTES_LICENCIAS[0]) + [
    "registros_principal",
    "registros_complementario",
    "registros_total",
]

COLUMNAS_MANIFIESTO = [
    "id_global",
    "url_descargada",
    "ruta_imagen_local",
    "estado_descarga",
    "http_estado",
    "bytes",
    "imagen_sha256",
    "imagen_ancho",
    "imagen_alto",
    "formato",
    "imagen_dhash",
    "imagen_sha256_pixeles",
    "fecha_descarga",
    "error",
]


# --------------------------------------------------------------------------- utilidades


def leer_csv(ruta: Path) -> list[dict[str, str]]:
    with ruta.open(newline="", encoding="utf-8-sig") as archivo:
        return [
            {clave: (valor or "").strip() for clave, valor in fila.items()}
            for fila in csv.DictReader(archivo)
        ]


def indexar(filas: list[dict[str, str]], clave: str) -> dict[str, dict[str, str]]:
    indice: dict[str, dict[str, str]] = {}
    for fila in filas:
        if fila[clave] in indice:
            raise ValueError(f"Identificador repetido en insumo: {clave}={fila[clave]}")
        indice[fila[clave]] = fila
    return indice


def primero(*valores: str) -> str:
    return next((valor for valor in valores if valor), "")


def escribir_csv(ruta: Path, columnas: list[str], filas: list[dict[str, str]]) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=columnas, lineterminator="\n")
        escritor.writeheader()
        escritor.writerows(filas)


def escribir_texto(ruta: Path, lineas: list[str]) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_bytes(("\n".join(lineas) + "\n").encode("utf-8"))


def sha256_archivo(ruta: Path) -> str:
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def clave_orden(fila: dict[str, str]) -> tuple[int, int, str]:
    id_fuente = fila["id_fuente"]
    return (ORDEN_FUENTES[fila["fuente"]], int(id_fuente) if id_fuente.isdigit() else 0, id_fuente)


# --------------------------------------------------------------------------- registros base


def registros_met(raiz: Path) -> list[dict[str, str]]:
    inventario = indexar(leer_csv(raiz / MET_INVENTARIO), "id_objeto")
    v1 = indexar([fila for ruta in MET_V1 for fila in leer_csv(raiz / ruta)], "id_objeto")

    registros: list[dict[str, str]] = []
    for decision, ruta in MET_REVISADOS.items():
        for rev in leer_csv(raiz / ruta):
            id_fuente = rev["id_fuente"]
            inv = inventario[id_fuente]
            previo = v1.get(id_fuente, {})
            registros.append({
                "id_global": f"MET:{id_fuente}",
                "fuente": "MET",
                "id_fuente": id_fuente,
                "numero_acceso": "",
                "institucion": inv["institucion"],
                "url_objeto": primero(rev["url_objeto"], inv["url_objeto"]),
                "url_imagen": primero(rev["url_imagen"], inv["url_imagen"]),
                "url_imagen_miniatura": inv["url_imagen_miniatura"],
                "titulo_original": primero(rev["titulo_original"], inv["titulo_original"]),
                "titulo_es_sugerido": primero(rev["titulo_es_sugerido"], inv["titulo_es_sugerido"]),
                "descripcion": primero(previo.get("descripcion_oficial", ""), previo.get("descripcion", "")),
                "cultura": primero(rev["cultura"], inv["cultura"]),
                "periodo": inv["periodo"],
                "fecha_objeto": primero(rev["fecha_objeto"], inv["fecha_objeto"]),
                "procedencia": primero(rev["procedencia"], "; ".join(v for v in (inv["pais"], inv["region"]) if v)),
                "departamento": inv["departamento_museo"],
                "clasificacion_original": inv["clasificacion_original"],
                "nombre_objeto_original": inv["nombre_objeto_original"],
                "tipo_objeto": rev["tipo_objeto"],
                "tipo_superficie": rev["tipo_superficie"],
                "material": primero(rev["material"], inv["material_original"]),
                "material_normalizado": rev["material_normalizado"],
                # La API del MET no entrega tecnica; la de la curacion ya esta normalizada.
                "tecnica": "",
                "tecnica_normalizada": primero(rev["tecnica"], previo.get("tecnica", "")),
                "dimensiones": inv["dimensiones"],
                "decision_curacion_final": decision,
                "motivo_curacion_final": rev["motivo_curacion"],
                "decision_auditoria": rev["decision_revision"],
                "motivo_auditoria": rev["motivo_revision"],
                "observacion_auditoria": rev["observaciones_revision"],
                "categoria_revision": previo.get("categoria_revision_v2", ""),
                "origen_curacion": rev["origen_curacion"],
                "estado_licencia": "dominio_publico" if inv["es_dominio_publico"] == "True" else "",
                "licencia_fuente": f"isPublicDomain={inv['es_dominio_publico']}",
                "derechos_reproduccion": inv["derechos_reproduccion"],
                "consulta_origen": inv["termino_busqueda"],
                "archivo_origen": ruta,
                "fecha_descarga_metadatos": inv["fecha_descarga"],
            })
    return registros


def registros_cma(raiz: Path) -> list[dict[str, str]]:
    candidatos = indexar(leer_csv(raiz / CMA_CANDIDATOS), "source_id")

    registros: list[dict[str, str]] = []
    for decision, ruta in CMA_REVISADOS.items():
        for rev in leer_csv(raiz / ruta):
            id_fuente = rev["id_objeto"]
            cand = candidatos[id_fuente]
            # El workbook copia la clasificacion como tipo_objeto; solo se considera
            # tipo normalizado si el revisor escribio algo distinto.
            tipo_manual = rev["tipo_objeto_manual"]
            tipo_objeto = tipo_manual if tipo_manual not in {cand["classification"], rev["nombre_objeto_original"]} else ""
            registros.append({
                "id_global": f"CMA:{id_fuente}",
                "fuente": "CMA",
                "id_fuente": id_fuente,
                "numero_acceso": cand["accession_number"],
                "institucion": cand["source"],
                "url_objeto": primero(rev["url_objeto"], cand["url"]),
                "url_imagen": primero(rev["url_imagen"], cand["image_url"]),
                "url_imagen_miniatura": "",
                "titulo_original": primero(rev["titulo_original"], cand["title"]),
                "titulo_es_sugerido": "",
                "descripcion": cand["description"],
                "cultura": primero(rev["cultura_manual"], rev["cultura"], cand["culture"]),
                "periodo": "",
                "fecha_objeto": primero(rev["periodo_manual"], cand["creation_date"]),
                "procedencia": "",
                "departamento": cand["department"],
                "clasificacion_original": cand["classification"],
                "nombre_objeto_original": rev["nombre_objeto_original"],
                "tipo_objeto": tipo_objeto,
                "tipo_superficie": "",
                "material": cand["medium"],
                "material_normalizado": "",
                "tecnica": primero(rev["tecnica_original"], cand["technique"]),
                "tecnica_normalizada": "",
                "dimensiones": "",
                "decision_curacion_final": decision,
                "motivo_curacion_final": rev["motivo_auditoria"],
                "decision_auditoria": rev["decision_auditoria"],
                "motivo_auditoria": rev["motivo_auditoria"],
                "observacion_auditoria": rev["observacion_auditoria"],
                "categoria_revision": cand["curation_status"],
                "origen_curacion": "revision_manual_cma_v2",
                "estado_licencia": "cc0" if cand["share_license_status"] == "CC0" else "",
                "licencia_fuente": f"share_license_status={cand['share_license_status']}",
                "derechos_reproduccion": "",
                "terminos_andinos": cand["andean_terms"],
                "terminos_textiles": cand["textile_terms"],
                "consulta_origen": cand["raw_queries"],
                "archivo_origen": ruta,
                "fecha_descarga_metadatos": "",
            })
    return registros


def normalizar_campos(fila: dict[str, str]) -> None:
    """Completa por reglas los campos normalizados que la curacion dejo vacios y registra su origen."""
    contexto = {
        "titulo_original": fila["titulo_original"],
        "titulo_es_sugerido": fila["titulo_es_sugerido"],
        "nombre_objeto_original": fila["nombre_objeto_original"],
        "clasificacion_original": fila["clasificacion_original"],
        "material_original": fila["material"],
        "cultura": fila["cultura"],
    }
    reglas = {
        "tipo_objeto": lambda: normalize_object_type(contexto),
        "material_normalizado": lambda: normalizar_material(fila["material"], fila["tecnica"]),
        "tecnica_normalizada": lambda: normalizar_tecnica(
            fila["tecnica"], fila["material"], fila["clasificacion_original"], nucleo_titulo(fila["titulo_original"])
        ),
    }
    for campo, regla in reglas.items():
        if fila[campo]:
            fila[f"origen_{campo}"] = "curacion"
            continue
        valor = regla()
        if valor in TIPOS_SIN_DETERMINAR:
            valor = ""
        fila[campo] = valor
        fila[f"origen_{campo}"] = "regla" if valor else ""


def construir_registros_base(raiz: Path) -> list[dict[str, str]]:
    """Registros armonizados sin informacion de imagen, ordenados por fuente e id."""
    registros = registros_met(raiz) + registros_cma(raiz)
    for fila in registros:
        normalizar_campos(fila)
    return sorted(registros, key=clave_orden)


# --------------------------------------------------------------------------- imagen y control


def estado_metadatos(fila: dict[str, str]) -> str:
    """completo: contexto y material, tecnica y tipo normalizados; parcial: contexto y algun dato material."""
    if not (fila["titulo_original"] and fila["url_objeto"] and fila["url_imagen"]):
        return "insuficiente"
    if not (fila["cultura"] and fila["fecha_objeto"]):
        return "insuficiente"
    tipo_concreto = fila["tipo_objeto"] not in {"", "objeto_textil"}
    if fila["material_normalizado"] and fila["tecnica_normalizada"] and tipo_concreto:
        return "completo"
    if primero(fila["material"], fila["tecnica"], fila["material_normalizado"], fila["tecnica_normalizada"]):
        return "parcial"
    return "insuficiente"


def estado_imagen(imagen: dict[str, str] | None, lado_minimo: int) -> str:
    if not imagen or imagen["estado_descarga"] != "ok":
        return "no_disponible"
    if max(int(imagen["imagen_ancho"]), int(imagen["imagen_alto"])) < lado_minimo:
        return "baja_resolucion"
    return "util"


def distancia_hamming(hash_a: str, hash_b: str) -> int:
    return bin(int(hash_a, 16) ^ int(hash_b, 16)).count("1")


def agrupar_duplicados(registros: list[dict[str, str]]) -> dict[str, list[str]]:
    """Agrupa registros que comparten URL, archivo o pixeles de imagen (union-find)."""
    padre = {fila["id_global"]: fila["id_global"] for fila in registros}

    def raiz_de(nodo: str) -> str:
        while padre[nodo] != nodo:
            padre[nodo] = padre[padre[nodo]]
            nodo = padre[nodo]
        return nodo

    for campo in ("url_imagen", "imagen_sha256", "imagen_sha256_pixeles"):
        por_valor: dict[str, list[str]] = defaultdict(list)
        for fila in registros:
            if fila[campo]:
                por_valor[fila[campo]].append(fila["id_global"])
        for ids in por_valor.values():
            for otro in ids[1:]:
                padre[raiz_de(otro)] = raiz_de(ids[0])

    grupos: dict[str, list[str]] = defaultdict(list)
    for fila in registros:
        grupos[raiz_de(fila["id_global"])].append(fila["id_global"])
    return {raiz_grupo: ids for raiz_grupo, ids in grupos.items() if len(ids) > 1}


def posibles_duplicados_visuales(registros: list[dict[str, str]], umbral: int) -> list[tuple[str, str, int]]:
    con_hash = [fila for fila in registros if fila["imagen_dhash"]]
    pares = []
    for i, fila_a in enumerate(con_hash):
        for fila_b in con_hash[i + 1:]:
            if fila_a["grupo_imagen_duplicada"] and fila_a["grupo_imagen_duplicada"] == fila_b["grupo_imagen_duplicada"]:
                continue
            distancia = distancia_hamming(fila_a["imagen_dhash"], fila_b["imagen_dhash"])
            if distancia <= umbral:
                pares.append((fila_a["id_global"], fila_b["id_global"], distancia))
    return pares


def completar(registros: list[dict[str, str]], manifiesto: dict[str, dict[str, str]], lado_minimo: int) -> None:
    for fila in registros:
        imagen = manifiesto.get(fila["id_global"])
        ok = bool(imagen and imagen["estado_descarga"] == "ok")
        fila["ruta_imagen_local"] = imagen["ruta_imagen_local"] if ok else ""
        for campo in ("imagen_sha256", "imagen_dhash", "imagen_ancho", "imagen_alto", "imagen_sha256_pixeles"):
            fila[campo] = imagen.get(campo, "") if ok else ""
        fila["estado_metadatos"] = estado_metadatos(fila)
        fila["estado_anotacion"] = "sin_anotar"
        fila["estado_imagen"] = estado_imagen(imagen, lado_minimo)
        for campo in ("motivos", "familia_iconografica", "motivo_principal", "observaciones", "grupo_imagen_duplicada"):
            fila.setdefault(campo, "")
        for campo in COLUMNAS:
            fila.setdefault(campo, "")

    por_id = {fila["id_global"]: fila for fila in registros}
    grupos = sorted(agrupar_duplicados(registros).values(), key=lambda ids: clave_orden(por_id[ids[0]]))
    for numero, ids in enumerate(grupos, start=1):
        for id_global in ids:
            fila = por_id[id_global]
            fila["grupo_imagen_duplicada"] = f"DUP-{numero:03d}"
            otros = ", ".join(otro for otro in ids if otro != id_global)
            fila["observaciones"] = f"Comparte imagen con {otros}."


# --------------------------------------------------------------------------- validacion


def validar(registros: list[dict[str, str]], esperados: dict[str, int]) -> list[str]:
    problemas: list[str] = []

    ids = Counter(fila["id_global"] for fila in registros)
    repetidos = sorted(id_ for id_, n in ids.items() if n > 1)
    if repetidos:
        problemas.append(f"id_global repetidos: {repetidos[:10]}")

    pares = Counter((fila["fuente"], fila["id_fuente"]) for fila in registros)
    if any(n > 1 for n in pares.values()):
        problemas.append("Pares (fuente, id_fuente) repetidos.")

    for fila in registros:
        vacios = [campo for campo in OBLIGATORIOS if not fila[campo]]
        if vacios:
            problemas.append(f"{fila['id_global']}: campos obligatorios vacios: {', '.join(vacios)}")
        if fila["id_global"] != f"{fila['fuente']}:{fila['id_fuente']}":
            problemas.append(f"{fila['id_global']}: id_global no coincide con fuente:id_fuente")
        controles = [
            ("decision_curacion_final", DECISIONES_VALIDAS),
            ("estado_licencia", ESTADOS_LICENCIA_VALIDOS),
            ("estado_metadatos", ESTADOS_METADATOS_VALIDOS),
            ("estado_imagen", ESTADOS_IMAGEN_VALIDOS),
        ]
        for campo, validos in controles:
            if fila[campo] and fila[campo] not in validos:
                problemas.append(f"{fila['id_global']}: {campo}={fila[campo]} no permitido")

    conteos = Counter(f"{fila['fuente']}_{fila['decision_curacion_final']}" for fila in registros)
    for clave, esperado in esperados.items():
        if clave == "total":
            observado = len(registros)
        else:
            observado = conteos.get(clave, 0)
        if observado != esperado:
            problemas.append(f"Conteo {clave}: {observado}, se esperaban {esperado}")
    return problemas


# --------------------------------------------------------------------------- reportes


def filas_fuentes(registros: list[dict[str, str]]) -> list[dict[str, str]]:
    salida = []
    for fuente in FUENTES_LICENCIAS:
        propias = [fila for fila in registros if fila["fuente"] == fuente["fuente"]]
        principal = sum(fila["decision_curacion_final"] == "principal" for fila in propias)
        salida.append({
            **fuente,
            "registros_principal": str(principal),
            "registros_complementario": str(len(propias) - principal),
            "registros_total": str(len(propias)),
        })
    return salida


def lineas_reporte(
    registros: list[dict[str, str]],
    pares_visuales: list[tuple[str, str, int]],
    umbral: int,
    lado_minimo: int,
) -> list[str]:
    fuentes = list(ORDEN_FUENTES)
    lineas = [
        "# Corpus consolidado MET+CMA v1.0",
        "",
        "Resumen generado por `python -m src.flujo` (`src/consolidado/construir_consolidado.py`).",
        "",
        "## Conteos",
        "",
        "| Fuente | Principal | Complementario | Total |",
        "|---|---:|---:|---:|",
    ]
    for fuente in fuentes + ["Total"]:
        propias = [f for f in registros if fuente == "Total" or f["fuente"] == fuente]
        principal = sum(f["decision_curacion_final"] == "principal" for f in propias)
        lineas.append(f"| {fuente} | {principal} | {len(propias) - principal} | {len(propias)} |")

    lineas += ["", "## Cobertura de campos (registros con valor)", "", "| Campo | " + " | ".join(fuentes) + " |"]
    lineas.append("|---|" + "---:|" * len(fuentes))
    for campo in COLUMNAS:
        valores = []
        for fuente in fuentes:
            propias = [f for f in registros if f["fuente"] == fuente]
            valores.append(f"{sum(bool(f[campo]) for f in propias)}/{len(propias)}")
        lineas.append(f"| `{campo}` | " + " | ".join(valores) + " |")

    for campo in ("estado_metadatos", "estado_imagen", "estado_licencia"):
        lineas += ["", f"## {campo}", "", "| Valor | " + " | ".join(fuentes) + " |", "|---|" + "---:|" * len(fuentes)]
        for valor in sorted({f[campo] for f in registros}):
            conteos = [str(sum(f[campo] == valor and f["fuente"] == fuente for f in registros)) for fuente in fuentes]
            lineas.append(f"| {valor} | " + " | ".join(conteos) + " |")

    lineas += [
        "",
        "Criterios:",
        "",
        "- `estado_metadatos`: `insuficiente` si falta titulo, url_objeto, url_imagen, cultura o fecha_objeto, o si no "
        "hay ningun dato de material o tecnica; `completo` si tiene material_normalizado, tecnica_normalizada y un "
        "tipo_objeto concreto (distinto de `objeto_textil`); `parcial` en otro caso.",
        "- Los campos `origen_*` indican si el valor normalizado viene de la curacion o de una regla automatica "
        "(`src/preprocessing/normalizacion.py`, `src/preprocessing/surface_filters.py`). Los valores por regla "
        "deben validarse en la anotacion manual.",
        "- Imagen compartida: registros con la misma `url_imagen`, el mismo archivo (SHA-256) o los mismos pixeles "
        "decodificados (`imagen_sha256_pixeles` del manifiesto).",
        f"- `estado_imagen`: `no_disponible` si la descarga fallo; `baja_resolucion` si el lado mayor mide menos de "
        f"{lado_minimo} px; `util` en otro caso.",
        "",
        "## Imagenes compartidas entre registros",
        "",
    ]
    grupos: dict[str, list[dict[str, str]]] = defaultdict(list)
    for fila in registros:
        if fila["grupo_imagen_duplicada"]:
            grupos[fila["grupo_imagen_duplicada"]].append(fila)
    if grupos:
        lineas += [
            "Los registros se conservan en el corpus: son objetos distintos del museo que comparten imagen. "
            "Deben tratarse como un solo item en evaluaciones imagen-imagen.",
            "",
            "| Grupo | Registros | Titulos |",
            "|---|---|---|",
        ]
        for grupo, filas in sorted(grupos.items()):
            ids = ", ".join(f["id_global"] for f in filas)
            titulos = "; ".join(f["titulo_original"] for f in filas)
            lineas.append(f"| {grupo} | {ids} | {titulos} |")
    else:
        lineas.append("No se detectaron registros que compartan imagen.")

    lineas += ["", f"## Posibles duplicados visuales (dHash, distancia <= {umbral})", ""]
    if pares_visuales:
        lineas += [
            "Pares con imagenes perceptualmente muy parecidas que no comparten archivo. Requieren revision manual.",
            "",
            "| Registro A | Registro B | Distancia |",
            "|---|---|---:|",
        ]
        lineas += [f"| {a} | {b} | {d} |" for a, b, d in pares_visuales]
    else:
        lineas.append("No se detectaron pares por encima del umbral.")
    return lineas


def lineas_esquema() -> list[str]:
    lineas = [
        "# Esquema del corpus consolidado MET+CMA v1.0",
        "",
        "Archivo: `data/processed/corpus_textiles_andinos_met_cma_v1_consolidado.csv` "
        "(UTF-8 sin BOM, separador coma, fin de linea LF).",
        "",
        "Documento generado desde `src/consolidado/esquema.py`; no editar a mano.",
        "",
        "| # | Campo | Grupo | Descripcion |",
        "|---:|---|---|---|",
    ]
    for numero, (campo, grupo, descripcion) in enumerate(ESQUEMA, start=1):
        obligatorio = " **(obligatorio)**" if campo in OBLIGATORIOS else ""
        lineas.append(f"| {numero} | `{campo}` | {grupo} | {descripcion}{obligatorio} |")
    return lineas


# --------------------------------------------------------------------------- principal


def construir(raiz: Path) -> int:
    config = leer_config(raiz)["consolidado"]
    lado_minimo = int(config["parametros"]["lado_minimo_imagen"])
    umbral = int(config["parametros"]["umbral_dhash"])

    registros = construir_registros_base(raiz)
    ruta_manifiesto = raiz / MANIFIESTO_IMAGENES
    manifiesto = indexar(leer_csv(ruta_manifiesto), "id_global") if ruta_manifiesto.exists() else {}
    if not manifiesto:
        print(f"Advertencia: no existe {MANIFIESTO_IMAGENES}; las imagenes quedan como no_disponible.")
    completar(registros, manifiesto, lado_minimo)

    problemas = validar(registros, {clave: int(valor) for clave, valor in config["conteos"].items()})
    if problemas:
        print("Problemas en el consolidado:")
        for problema in problemas:
            print(f"- {problema}")
        return 1

    filas = [{campo: fila[campo] for campo in COLUMNAS} for fila in registros]
    escribir_csv(raiz / SALIDA_CONSOLIDADO, COLUMNAS, filas)
    escribir_csv(raiz / SALIDA_FUENTES, COLUMNAS_FUENTES, filas_fuentes(registros))

    pares_visuales = posibles_duplicados_visuales(registros, umbral)
    escribir_texto(raiz / SALIDA_REPORTE, lineas_reporte(registros, pares_visuales, umbral, lado_minimo))
    escribir_texto(raiz / SALIDA_ESQUEMA, lineas_esquema())

    verificados = [SALIDA_CONSOLIDADO, SALIDA_FUENTES, MANIFIESTO_IMAGENES]
    escribir_texto(
        raiz / SALIDA_SHA256,
        [f"{sha256_archivo(raiz / ruta)}  {ruta}" for ruta in verificados if (raiz / ruta).exists()],
    )

    grupos = {fila["grupo_imagen_duplicada"] for fila in registros if fila["grupo_imagen_duplicada"]}
    print(f"Consolidado MET+CMA v1.0: {len(registros)} registros")
    print(f"Grupos de imagen compartida: {len(grupos)}; posibles duplicados visuales: {len(pares_visuales)}")
    print(f"Salida: {raiz / SALIDA_CONSOLIDADO}")
    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Construye el corpus consolidado MET+CMA v1.0.")
    parser.add_argument("--root", default=".", help="Raiz del repositorio.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    return construir(Path(args.root).resolve())


if __name__ == "__main__":
    raise SystemExit(main())
