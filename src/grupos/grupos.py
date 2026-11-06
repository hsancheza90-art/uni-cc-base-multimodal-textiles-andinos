"""Grupos de piezas relacionadas del principal y el complementario v2 (paso del flujo, sin red y sin torch).

Uso desde la raíz del repositorio:

    python -m src.grupos.grupos

Un grupo reúne los registros que muestran el mismo objeto o partes de él; es la unidad de
partición del protocolo experimental (docs/protocolo_experimental_v2.md, sección 2). El paso:

1. Propone pares candidatos con cinco señales ([candidatos] de config/grupos.toml): imagen
   idéntica (misma copia de evaluación, misma imagen original o mismo grupo_imagen_duplicada),
   dHash de la copia (data/metadata/imagenes_evaluacion_dhash_v2.csv), coseno de M2 (embeddings
   versionados), número de inventario con sufijo de parte (1922.395.a, 1922.395.b) y descripción
   curatorial idéntica. Escribe data/metadata/grupos_candidatos_v2.csv.
2. Lee las decisiones del revisor en data/metadata/grupos_revision_v2.xlsx (lo crea y actualiza
   python -m src.grupos.workbook) y une las piezas de cada par unir o no_seguro, por
   transitividad. Escribe data/metadata/grupos_v2.csv, una fila por pieza con su grupo.
3. Informa en outputs/reports/grupos_v2.md, solo con conteos: los pares también incluyen piezas
   de la galería del protocolo, que se juzga a ciegas.

Una decisión con un código que no está en [decisiones], sin revisor o sin una fecha_revision
válida (AAAA-MM-DD) detiene el paso sin escribir los grupos.
Los pares sin decisión quedan pendientes; mientras haya pendientes, los grupos no se congelan.
"""

from __future__ import annotations

import argparse
import re
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
from typing import Any

import numpy as np

from src.anotacion.aplicar_anotaciones import fecha_valida
from src.anotacion.corpus_v2 import SALIDA_COMPLEMENTARIO_V2, SALIDA_PRINCIPAL_V2
from src.anotacion.nucleo import SALIDA_NUCLEO
from src.consolidado.construir_consolidado import distancia_hamming
from src.imagenes.dhash_evaluacion import SALIDA_DHASH
from src.modelos.embeddings import EMBEDDINGS_M2, leer_embeddings, subconjunto, vecino_mas_cercano
from src.utils.archivos import escribir_csv, escribir_texto, indexar, leer_csv
from src.utils.config import CONFIG_GRUPOS, leer_config_grupos
from src.utils.libros import leer_hoja
from src.utils.metricas import tabla

SALIDA_CANDIDATOS = "data/metadata/grupos_candidatos_v2.csv"
SALIDA_GRUPOS = "data/metadata/grupos_v2.csv"
REPORTE_GRUPOS = "outputs/reports/grupos_v2.md"
WORKBOOK_GRUPOS = Path("data/metadata/grupos_revision_v2.xlsx")
HOJA_PARES = "pares"
SENALES = ["imagen_identica", "inventario", "descripcion", "dhash", "m2"]
COLUMNAS_CANDIDATOS = [
    "par", "id_a", "id_b", "fuente_a", "fuente_b", "senales", "grupo_imagen_duplicada", "distancia_dhash",
    "coseno_m2", "inventario_base", "decision_sugerida",
]
COLUMNAS_GRUPOS = ["id_global", "fuente", "conjunto", "grupo", "tamano_grupo", "en_nucleo"]
# Sufijo de parte al final del numero de inventario: .a, -b, a, a-b (sin distinguir mayusculas).
SUFIJO_PARTE = re.compile(r"^(?P<base>.*\d)[.\-]?[a-z](?:-[a-z])?$", re.IGNORECASE)


def clave_par(a: str, b: str) -> str:
    return " | ".join(sorted((a, b)))


def base_inventario(numero: str) -> str:
    """Número de inventario sin su sufijo de parte (o el número completo si no lo tiene)."""
    coincidencia = SUFIJO_PARTE.match(numero.strip())
    return coincidencia.group("base") if coincidencia else numero.strip()


def normalizar_descripcion(texto: str) -> str:
    return " ".join(texto.split()).lower()


# --------------------------------------------------------------------------- candidatos


def piezas_v2(raiz: Path) -> list[dict[str, str]]:
    """Principal y complementario v2 en ese orden, con la columna conjunto (decisión del revisor, 2026-11-06)."""
    return ([{**f, "conjunto": "principal"} for f in leer_csv(raiz / SALIDA_PRINCIPAL_V2)]
            + [{**f, "conjunto": "complementario"} for f in leer_csv(raiz / SALIDA_COMPLEMENTARIO_V2)])


def candidatos(principal: list[dict[str, str]], dhash: dict[str, dict[str, str]], embeddings, config: dict[str, Any]
               ) -> list[dict[str, str]]:
    """Pares propuestos por alguna señal, con todas las señales que los proponen."""
    par = {"umbral_dhash": int(config["umbral_dhash"]), "coseno": float(config["umbral_coseno"]),
           "coseno_entre": float(config["umbral_coseno_entre_museos"]),
           "descripcion": int(config["longitud_minima_descripcion"])}
    datos = {f["id_global"]: f for f in principal}
    ids = [f["id_global"] for f in principal]
    senales: dict[str, set[str]] = defaultdict(set)
    inventario: dict[str, str] = {}

    for a, b in combinations(ids, 2):
        fa, fb = datos[a], datos[b]
        copia_a, copia_b = dhash.get(a, {}), dhash.get(b, {})
        if ((copia_a and copia_a["sha256_copia"] == copia_b.get("sha256_copia"))
                or (fa["imagen_sha256"] and fa["imagen_sha256"] == fb["imagen_sha256"])
                or (fa["grupo_imagen_duplicada"] and fa["grupo_imagen_duplicada"] == fb["grupo_imagen_duplicada"])):
            senales[clave_par(a, b)].add("imagen_identica")
        if copia_a and copia_b and distancia_hamming(copia_a["dhash"], copia_b["dhash"]) <= par["umbral_dhash"]:
            senales[clave_par(a, b)].add("dhash")

    por_inventario: dict[tuple[str, str], list[str]] = defaultdict(list)
    por_descripcion: dict[str, list[str]] = defaultdict(list)
    for fila in principal:
        if fila["numero_acceso"]:
            por_inventario[(fila["fuente"], base_inventario(fila["numero_acceso"]))].append(fila["id_global"])
        texto = normalizar_descripcion(fila["descripcion"])
        if len(texto) >= par["descripcion"]:
            por_descripcion[texto].append(fila["id_global"])
    for (_, base), miembros in por_inventario.items():
        for a, b in combinations(miembros, 2):
            senales[clave_par(a, b)].add("inventario")
            inventario[clave_par(a, b)] = base
    for miembros in por_descripcion.values():
        for a, b in combinations(miembros, 2):
            senales[clave_par(a, b)].add("descripcion")

    similitud = None
    if embeddings is not None:
        con_imagen = [id_ for id_ in ids if id_ in set(embeddings.ids)]  # sin imagen no hay embedding
        sub = subconjunto(embeddings, con_imagen)
        similitud = sub.matriz.astype(np.float64) @ sub.matriz.astype(np.float64).T
        posicion = {id_: i for i, id_ in enumerate(con_imagen)}
        filas, columnas = np.nonzero(np.triu(similitud >= min(par["coseno"], par["coseno_entre"]), k=1))
        for i, j in zip(filas.tolist(), columnas.tolist()):
            a, b = con_imagen[i], con_imagen[j]
            umbral = par["coseno"] if datos[a]["fuente"] == datos[b]["fuente"] else min(par["coseno"], par["coseno_entre"])
            if similitud[i, j] >= umbral:
                senales[clave_par(a, b)].add("m2")

    salida = []
    for clave, conjunto in senales.items():
        a, b = clave.split(" | ")
        copia_a, copia_b = dhash.get(a), dhash.get(b)
        grupo = datos[a]["grupo_imagen_duplicada"]
        coseno = ""
        if similitud is not None and a in posicion and b in posicion:
            coseno = f"{similitud[posicion[a], posicion[b]]:.4f}"
        salida.append({
            "par": clave, "id_a": a, "id_b": b, "fuente_a": datos[a]["fuente"], "fuente_b": datos[b]["fuente"],
            "senales": "; ".join(s for s in SENALES if s in conjunto),
            "grupo_imagen_duplicada": grupo if grupo and grupo == datos[b]["grupo_imagen_duplicada"] else "",
            "distancia_dhash": str(distancia_hamming(copia_a["dhash"], copia_b["dhash"])) if copia_a and copia_b else "",
            "coseno_m2": coseno, "inventario_base": inventario.get(clave, ""),
            "decision_sugerida": "unir" if "imagen_identica" in conjunto else "",
        })
    # Primero la señal más fuerte; dentro de cada una, por par.
    return sorted(salida, key=lambda f: (min(SENALES.index(s) for s in f["senales"].split("; ")), f["par"]))


# --------------------------------------------------------------------------- decisiones y grupos


def leer_decisiones(raiz: Path, codigos: set[str]) -> tuple[dict[str, dict[str, str]], list[str]]:
    """Decisiones del workbook por par, y los errores (códigos que no existen, pares repetidos)."""
    ruta = raiz / WORKBOOK_GRUPOS
    if not ruta.exists():
        return {}, []
    decisiones, errores = {}, []
    for fila in leer_hoja(ruta, HOJA_PARES, clave="par"):
        if fila["par"] in decisiones:
            errores.append(f"{fila['par']}: par repetido en el workbook")
            continue
        if fila.get("decision"):
            if fila["decision"] not in codigos:
                errores.append(f"{fila['par']}: decision '{fila['decision']}' no es un codigo de [decisiones]")
            if not fila.get("revisor"):
                errores.append(f"{fila['par']}: decision sin revisor")
            if not fecha_valida(fila.get("fecha_revision", "")):
                errores.append(f"{fila['par']}: fecha_revision vacia o invalida (AAAA-MM-DD)")
        decisiones[fila["par"]] = fila
    return decisiones, errores


def agrupar(ids: list[str], pares_unidos: list[tuple[str, str]]) -> dict[str, list[str]]:
    """Componentes conexas (unión-búsqueda); cada grupo lista sus ids en el orden de ids."""
    padre = {id_: id_ for id_ in ids}

    def raiz_de(x: str) -> str:
        while padre[x] != x:
            padre[x] = padre[padre[x]]
            x = padre[x]
        return x

    for a, b in pares_unidos:
        ra, rb = raiz_de(a), raiz_de(b)
        if ra != rb:
            padre[rb] = ra
    grupos: dict[str, list[str]] = defaultdict(list)
    for id_ in ids:
        grupos[raiz_de(id_)].append(id_)
    return grupos


def lineas_reporte(pares: list[dict[str, str]], estado: Counter, grupos: list[list[str]], nucleo: set[str],
                   verificacion: tuple[int, int] | None, config: dict[str, Any], errores: list[str],
                   avisos: list[str]) -> list[str]:
    c = config["candidatos"]
    por_senal = Counter(s for p in pares for s in p["senales"].split("; "))
    tamanos = Counter(len(g) for g in grupos)
    en_nucleo = [g for g in grupos if any(i in nucleo for i in g)]
    mixtos = sum(1 for g in en_nucleo if any(i not in nucleo for i in g))
    pendientes = estado["pendiente"]
    lineas = [
        "# Grupos de piezas relacionadas (principal y complementario v2)",
        "",
        "Generado por `python -m src.grupos.grupos` (`src/grupos/grupos.py`), paso del flujo. Parametros en "
        f"`{CONFIG_GRUPOS.as_posix()}`; decisiones del revisor en `{WORKBOOK_GRUPOS.as_posix()}` (lo crea "
        "`python -m src.grupos.workbook`).",
        "",
        "Un grupo reune los registros que muestran el mismo objeto o partes de el; es la unidad de particion del "
        "protocolo experimental. El informe da solo conteos: los pares incluyen piezas de la galeria, que se juzga a "
        f"ciegas. Los pares estan en `{SALIDA_CANDIDATOS}`.",
        "",
        "## Pares candidatos por senal",
        "",
        f"Un par puede tener varias senales. Umbrales: dHash <= {c['umbral_dhash']}; coseno M2 >= {c['umbral_coseno']} "
        f"(>= {c['umbral_coseno_entre_museos']} entre museos); descripcion identica de {c['longitud_minima_descripcion']} "
        "caracteres o mas; inventario con la misma base y sufijo de parte.",
        "",
    ]
    lineas += tabla([[f"`{s}`", str(por_senal[s])] for s in SENALES] + [["Pares distintos", str(len(pares))]],
                    ["Senal", "Pares"])
    entre = sum(p["fuente_a"] != p["fuente_b"] for p in pares)
    con_nucleo = sum(p["id_a"] in nucleo or p["id_b"] in nucleo for p in pares)
    lineas += ["", f"- Entre museos: {entre}. Con alguna pieza del nucleo: {con_nucleo}.", ""]
    if verificacion:
        lineas += [f"- Comprobacion de M2: de {verificacion[1]} piezas con imagen compartida conocida "
                   f"(`grupo_imagen_duplicada`), {verificacion[0]} tienen a una pieza de su grupo como vecina mas "
                   "cercana.", ""]
    lineas += ["## Decisiones", ""]
    lineas += tabla([[clase, str(estado[clase])] for clase in ("unir", "no_seguro", "separar", "pendiente")],
                    ["Decision", "Pares"])
    lineas += ["", f"`unir` incluye {estado['auto']} pares de imagen identica propuestos con `revisor = auto`. "
                   "`no_seguro` cuenta como unir (regla de [decisiones]).", ""]
    lineas += ["## Grupos", ""]
    lineas += tabla([[str(t), str(n)] for t, n in sorted(tamanos.items())], ["Piezas por grupo", "Grupos"])
    lineas += [
        "",
        f"- Grupos: {len(grupos)} para {sum(len(g) for g in grupos)} piezas del principal y del complementario.",
        f"- Nucleo de anotacion: {len(nucleo)} piezas en {len(en_nucleo)} grupos; {mixtos} grupos del nucleo incluyen "
        "piezas de fuera del nucleo.",
        "",
    ]
    if pendientes:
        lineas += [f"**Quedan {pendientes} pares pendientes.** Los grupos no se congelan ni se construyen las "
                   "particiones (S2.3) mientras haya pares sin decidir.", ""]
    else:
        lineas += ["Todos los pares tienen decision: los grupos pueden congelarse.", ""]
    lineas += ["## Avisos", ""] + ([f"- {a}" for a in avisos] if avisos else ["Ninguno."])
    lineas += ["", "## Errores", ""] + ([f"- {e}" for e in errores] if errores else ["Ninguno."])
    return lineas


def construir(raiz: Path) -> int:
    config = leer_config_grupos(raiz)
    principal = piezas_v2(raiz)
    ids = [f["id_global"] for f in principal]
    nucleo = {f["id_global"] for f in leer_csv(raiz / SALIDA_NUCLEO)}
    dhash = indexar(leer_csv(raiz / SALIDA_DHASH), "id_global") if (raiz / SALIDA_DHASH).exists() else {}
    embeddings = leer_embeddings(raiz) if (raiz / EMBEDDINGS_M2).exists() else None
    pares = candidatos(principal, dhash, embeddings, config["candidatos"])

    decisiones_cfg = config["decisiones"]
    codigos = set(decisiones_cfg["unir"]) | set(decisiones_cfg["separar"])
    decisiones, errores = leer_decisiones(raiz, codigos)
    validos = set(ids)
    estado: Counter = Counter()
    unidos = []
    claves = {p["par"] for p in pares}
    for p in pares:
        decision = decisiones.get(p["par"], {})
        codigo = decision.get("decision", "")
        if not codigo:
            estado["pendiente"] += 1
        else:
            estado[codigo] += 1
            estado["auto"] += codigo == "unir" and decision.get("revisor", "") == "auto"
    avisos = []
    for clave, decision in decisiones.items():
        a, _, b = clave.partition(" | ")
        if decision.get("decision") in decisiones_cfg["unir"]:
            if a in validos and b in validos:
                unidos.append((a, b))
            if clave not in claves:
                avisos.append(f"{clave}: decidido como unir, pero ya no es candidato (se aplica si las dos piezas siguen)")
    if errores:
        escribir_texto(raiz / REPORTE_GRUPOS, lineas_reporte(pares, estado, [], nucleo, None, config, errores, avisos))
        print(f"Workbook de grupos con errores; no se actualizo {SALIDA_GRUPOS}. Ver {REPORTE_GRUPOS}.")
        for error in errores[:20]:
            print(f"- {error}")
        return 1

    componentes = agrupar(ids, unidos)
    orden = {id_: i for i, id_ in enumerate(ids)}
    grupos = sorted(componentes.values(), key=lambda g: orden[g[0]])
    datos = {f["id_global"]: f for f in principal}
    filas = []
    for numero, grupo in enumerate(grupos, start=1):
        for id_ in grupo:
            filas.append({"id_global": id_, "fuente": datos[id_]["fuente"], "conjunto": datos[id_]["conjunto"],
                          "grupo": f"G-{numero:03d}", "tamano_grupo": str(len(grupo)),
                          "en_nucleo": "si" if id_ in nucleo else "no"})
    filas.sort(key=lambda f: orden[f["id_global"]])

    verificacion = None
    if embeddings is not None:
        vecinos = vecino_mas_cercano(subconjunto(embeddings, [i for i in ids if i in set(embeddings.ids)]))
        miembros = [f for f in principal if f["grupo_imagen_duplicada"] and f["id_global"] in vecinos]
        aciertos = sum(datos[vecinos[f["id_global"]]]["grupo_imagen_duplicada"] == f["grupo_imagen_duplicada"]
                       for f in miembros)
        verificacion = (aciertos, len(miembros))

    escribir_csv(raiz / SALIDA_CANDIDATOS, COLUMNAS_CANDIDATOS, pares)
    escribir_csv(raiz / SALIDA_GRUPOS, COLUMNAS_GRUPOS, filas)
    escribir_texto(raiz / REPORTE_GRUPOS, lineas_reporte(pares, estado, grupos, nucleo, verificacion, config, errores,
                                                         avisos))
    print(f"Grupos v2: {len(pares)} pares candidatos, {estado['pendiente']} pendientes; {len(grupos)} grupos "
          f"para {len(ids)} piezas -> {SALIDA_GRUPOS}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Candidatos a duplicado y grupos de piezas del principal y complementario v2.")
    parser.add_argument("--root", default=".", help="Raiz del repositorio.")
    return construir(Path(parser.parse_args(argv).root).resolve())


if __name__ == "__main__":
    raise SystemExit(main())
