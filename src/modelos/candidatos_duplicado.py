"""Candidatos a duplicado o vista de una misma pieza según M2 (paso del flujo, sin red y sin torch).

Lee los embeddings versionados de M2 (src/modelos/m2_openclip.py) de las piezas del principal
v2 y lista los pares con coseno >= [m2.duplicados] umbral_coseno de config/modelos.toml. Son
candidatos para la decisión humana del workbook de grupos (S1.7 del plan de cierre), nunca
uniones automáticas: dos fotos casi iguales pueden ser la misma pieza, dos vistas o dos piezas
distintas de un mismo taller. Escribe:

- data/metadata/m2_candidatos_duplicado_v2.csv: un par por fila, con el coseno, las fuentes,
  si las dos copias son el mismo archivo y el grupo_imagen_duplicada que ya comparten, si lo hay.
- outputs/reports/m2_candidatos_duplicado_v2.md: solo conteos, y la comprobación de que las
  piezas con imagen compartida conocida tienen a su par como vecino más cercano.

El informe no lista pares ni vecinos: la galería del protocolo experimental se juzga a ciegas.
Sin embeddings versionados no hace nada.
"""

from __future__ import annotations

import argparse
from collections import Counter
from itertools import combinations
from pathlib import Path

from src.anotacion.corpus_v2 import SALIDA_PRINCIPAL_V2
from src.modelos.embeddings import EMBEDDINGS_M2, INDICE_M2, leer_embeddings, pares_sobre_umbral, subconjunto, vecino_mas_cercano
from src.utils.archivos import escribir_csv, escribir_texto, indexar, leer_csv
from src.utils.config import CONFIG_MODELOS, leer_config_modelos
from src.utils.metricas import tabla

SALIDA_CANDIDATOS = "data/metadata/m2_candidatos_duplicado_v2.csv"
REPORTE_CANDIDATOS = "outputs/reports/m2_candidatos_duplicado_v2.md"
COLUMNAS = ["id_a", "id_b", "coseno", "fuente_a", "fuente_b", "misma_copia", "grupo_imagen_duplicada"]
TRAMOS = [(0.99, "0,99 o mas"), (0.97, "0,97 a 0,99"), (0.0, "umbral a 0,97")]


def tramo(coseno: float) -> str:
    return next(nombre for limite, nombre in TRAMOS if coseno >= limite)


def lineas_reporte(pares: list[dict[str, str]], umbral: float, piezas: int, aciertos: int, en_grupos: int,
                   pares_conocidos: int, conocidos_sobre_umbral: int) -> list[str]:
    por_tramo = Counter(tramo(float(p["coseno"])) for p in pares)
    por_fuentes = Counter("mismo museo" if p["fuente_a"] == p["fuente_b"] else "entre museos" for p in pares)
    lineas = [
        "# M2: candidatos a duplicado (principal v2)",
        "",
        "Generado por `python -m src.modelos.candidatos_duplicado` (`src/modelos/candidatos_duplicado.py`), paso del "
        f"flujo, desde los embeddings versionados de M2 (`{EMBEDDINGS_M2.as_posix()}`). Umbral en "
        f"`{CONFIG_MODELOS.as_posix()}` ([m2.duplicados]): coseno >= {umbral}.",
        "",
        "Son candidatos para la decision humana del workbook de grupos (S1.7), nunca uniones automaticas. El informe "
        "da solo conteos, sin pares ni vecinos, porque la galeria del protocolo experimental se juzga a ciegas; los "
        f"pares estan en `{SALIDA_CANDIDATOS}`.",
        "",
        f"- Piezas del principal v2 con embedding: {piezas}.",
        f"- Pares candidatos: {len(pares)}; con la misma copia de evaluacion (mismo archivo): "
        f"{sum(p['misma_copia'] == 'si' for p in pares)}.",
        "",
        "## Pares por tramo de coseno y por museo",
        "",
    ]
    lineas += tabla([[nombre, str(por_tramo[nombre])] for _, nombre in TRAMOS], ["Coseno", "Pares"])
    lineas += [""]
    lineas += tabla([[clase, str(por_fuentes[clase])] for clase in ("mismo museo", "entre museos")], ["Museos", "Pares"])
    lineas += [
        "",
        "## Comprobacion con las imagenes compartidas conocidas",
        "",
        "`grupo_imagen_duplicada` marca piezas del principal v2 que comparten imagen (misma URL, archivo o pixeles). "
        "Si M2 es coherente, cada una tiene a una pieza de su grupo como vecina mas cercana.",
        "",
        f"- Piezas en grupos conocidos: {en_grupos}; con una pieza de su grupo como vecina mas cercana: {aciertos}.",
        f"- Pares dentro de grupos conocidos: {pares_conocidos}; con coseno sobre el umbral: {conocidos_sobre_umbral}.",
    ]
    return lineas


def construir(raiz: Path) -> int:
    if not (raiz / EMBEDDINGS_M2).exists():
        print(f"No existe {EMBEDDINGS_M2.as_posix()}; no hay candidatos M2 que calcular.")
        return 0
    umbral = float(leer_config_modelos(raiz)["m2"]["duplicados"]["umbral_coseno"])
    principal = leer_csv(raiz / SALIDA_PRINCIPAL_V2)
    indice = indexar(leer_csv(raiz / INDICE_M2), "id_global")
    faltan = [f["id_global"] for f in principal if f["id_global"] not in indice]
    if faltan:
        print(f"{len(faltan)} piezas del principal v2 sin embedding M2: {faltan[:10]}. Recalcular M2.")
        return 1
    embeddings = subconjunto(leer_embeddings(raiz), [f["id_global"] for f in principal])
    datos = {f["id_global"]: f for f in principal}

    pares = []
    for a, b, coseno in pares_sobre_umbral(embeddings, umbral):
        grupo_a, grupo_b = datos[a]["grupo_imagen_duplicada"], datos[b]["grupo_imagen_duplicada"]
        pares.append({
            "id_a": a, "id_b": b, "coseno": f"{coseno:.4f}",
            "fuente_a": datos[a]["fuente"], "fuente_b": datos[b]["fuente"],
            "misma_copia": "si" if indice[a]["sha256_copia"] == indice[b]["sha256_copia"] else "no",
            "grupo_imagen_duplicada": grupo_a if grupo_a and grupo_a == grupo_b else "",
        })

    grupos: dict[str, list[str]] = {}
    for fila in principal:
        if fila["grupo_imagen_duplicada"]:
            grupos.setdefault(fila["grupo_imagen_duplicada"], []).append(fila["id_global"])
    vecinos = vecino_mas_cercano(embeddings)
    miembros = [(id_, grupo) for grupo, ids in grupos.items() for id_ in ids]
    aciertos = sum(datos[vecinos[id_]]["grupo_imagen_duplicada"] == grupo for id_, grupo in miembros)
    conocidos = {tuple(sorted(par)) for ids in grupos.values() for par in combinations(ids, 2)}
    sobre_umbral = sum((p["id_a"], p["id_b"]) in conocidos for p in pares)

    escribir_csv(raiz / SALIDA_CANDIDATOS, COLUMNAS, pares)
    escribir_texto(raiz / REPORTE_CANDIDATOS, lineas_reporte(
        pares, umbral, len(principal), aciertos, len(miembros), len(conocidos), sobre_umbral))
    print(f"M2: {len(pares)} pares candidatos a duplicado (coseno >= {umbral}) -> {SALIDA_CANDIDATOS}")
    print(f"Imagenes compartidas conocidas con su par como vecino mas cercano: {aciertos} de {len(miembros)}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Candidatos a duplicado del principal v2 segun los embeddings M2.")
    parser.add_argument("--root", default=".", help="Raiz del repositorio.")
    return construir(Path(parser.parse_args(argv).root).resolve())


if __name__ == "__main__":
    raise SystemExit(main())
