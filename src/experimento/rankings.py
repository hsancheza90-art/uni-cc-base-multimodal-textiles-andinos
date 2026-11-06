"""Rankings de desarrollo de la tarea T3 para M0, M1 y M2 (paso del flujo, sin red y sin torch).

Uso desde la raíz del repositorio:

    python -m src.experimento.rankings

Para cada consulta T3 de desarrollo (data/metadata/consultas_t3_v2.csv) ordena las piezas de la
galería (data/metadata/particiones_v2.csv) que no son del grupo de la consulta:

- M0: BM25 del texto de la ficha de la consulta contra el de cada candidato (src/modelos/m0_texto.py);
  es una condición de metadatos de la consulta.
- M1: 1 - disimilitud de color y textura del textil (src/modelos/m1_vision.py).
- M2: coseno de los embeddings OpenCLIP congelados (src/modelos/m2_openclip.py).

Los empates se resuelven por id_global ascendente. Escribe
data/processed/experimento_v2_rankings_desarrollo.csv (ranking completo de cada consulta) y un
informe con conteos. Las consultas de prueba no se ejecutan aquí: se corren una sola vez con los
sistemas congelados (protocolo, sección 9). El evaluador no abre los rankings: los juicios se
hacen sobre un pool barajado, sin sistema ni posición (protocolo, sección 6).
"""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

import numpy as np

from src.anotacion.corpus_v2 import SALIDA_PRINCIPAL_V2
from src.experimento.snapshot import SALIDA_CONSULTAS, SALIDA_PARTICIONES
from src.modelos import m0_texto, m1_vision
from src.modelos.embeddings import leer_embeddings
from src.utils.archivos import escribir_csv, escribir_texto, indexar, leer_csv
from src.utils.config import CONFIG_MODELOS, leer_config_modelos
from src.utils.metricas import tabla

SALIDA_RANKINGS = "data/processed/experimento_v2_rankings_desarrollo.csv"
REPORTE_RANKINGS = "outputs/reports/experimento_v2_rankings_desarrollo.md"
COLUMNAS = ["sistema", "consulta", "rango", "id_global", "score"]
SISTEMAS = ("M0", "M1", "M2")


def ordenar(puntajes: dict[str, float]) -> list[tuple[str, float]]:
    return sorted(puntajes.items(), key=lambda par: (-round(par[1], 9), par[0]))


def puntuadores(raiz: Path, galeria: list[str]):
    """Funciones score(consulta, candidato) de cada sistema sobre la galería."""
    config = leer_config_modelos(raiz)
    fichas = [f for f in leer_csv(raiz / SALIDA_PRINCIPAL_V2) if f["id_global"] in set(galeria)]
    bm25, terminos = m0_texto.indice(fichas, config["m0"])

    matriz = np.load(raiz / m1_vision.CARACTERISTICAS_M1)
    fila_m1 = {f["id_global"]: int(f["fila"]) for f in leer_csv(raiz / m1_vision.INDICE_M1)}
    embeddings = leer_embeddings(raiz)
    posicion = embeddings.posicion()
    m2 = embeddings.matriz.astype(np.float64)

    return {
        "M0": lambda q, c: bm25.puntuar(terminos[q], c),
        "M1": lambda q, c: 1 - m1_vision.disimilitud(matriz[fila_m1[q]].astype(np.float64),
                                                       matriz[fila_m1[c]].astype(np.float64), config["m1"]),
        "M2": lambda q, c: float(m2[posicion[q]] @ m2[posicion[c]]),
    }, terminos


def construir(raiz: Path) -> int:
    if not (raiz / SALIDA_CONSULTAS).exists():
        print(f"No existe {SALIDA_CONSULTAS}: no hay consultas que ejecutar.")
        return 0
    particiones = leer_csv(raiz / SALIDA_PARTICIONES)
    galeria = [f["id_global"] for f in particiones]
    grupo = {f["id_global"]: f["grupo"] for f in particiones}
    consultas = [c for c in leer_csv(raiz / SALIDA_CONSULTAS) if c["particion"] == "desarrollo"]
    funciones, terminos = puntuadores(raiz, galeria)

    filas, sin_texto, puntaje_cero = [], 0, Counter()
    for consulta in consultas:
        q = consulta["id_global"]
        candidatos = [c for c in galeria if grupo[c] != grupo[q]]
        sin_texto += not terminos[q]
        for sistema in SISTEMAS:
            puntajes = {c: funciones[sistema](q, c) for c in candidatos}
            puntaje_cero[sistema] += sum(1 for p in puntajes.values() if p == 0)
            for rango, (id_global, score) in enumerate(ordenar(puntajes), start=1):
                filas.append({"sistema": sistema, "consulta": consulta["consulta"], "rango": str(rango),
                              "id_global": id_global, "score": f"{score:.6f}"})

    escribir_csv(raiz / SALIDA_RANKINGS, COLUMNAS, filas)
    candidatos_por_consulta = Counter((f["sistema"], f["consulta"]) for f in filas)
    pares = len(consultas) * len(SISTEMAS)
    escribir_texto(raiz / REPORTE_RANKINGS, [
        "# Rankings de desarrollo T3 (M0, M1 y M2)",
        "",
        "Generado por `python -m src.experimento.rankings` (`src/experimento/rankings.py`), paso del flujo. Parametros "
        f"en `{CONFIG_MODELOS.as_posix()}`. Solo consultas de desarrollo: las de prueba se ejecutan una vez, con los "
        "sistemas congelados. El evaluador no abre los rankings; este informe da solo conteos.",
        "",
        f"- Consultas de desarrollo: {len(consultas)}; galeria: {len(galeria)} piezas; candidatos por consulta: de "
        f"{min(candidatos_por_consulta.values()) if filas else 0} a {max(candidatos_por_consulta.values()) if filas else 0} "
        "(sin el grupo de la consulta).",
        f"- Consultas sin texto de ficha para M0: {sin_texto}.",
        "",
    ] + tabla([[s, str(len(consultas)), str(puntaje_cero[s])] for s in SISTEMAS],
              ["Sistema", "Consultas", "Pares consulta-candidato con score 0"]) + [
        "",
        f"Total: {len(filas)} filas ({pares} rankings completos). En M0, un score 0 indica que el candidato no comparte "
        "ningun termino con la consulta: esos candidatos quedan al final, por id.",
    ])
    print(f"Rankings de desarrollo: {len(consultas)} consultas x {len(SISTEMAS)} sistemas -> {SALIDA_RANKINGS}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Rankings de desarrollo T3 de M0, M1 y M2.")
    parser.add_argument("--root", default=".", help="Raiz del repositorio.")
    return construir(Path(parser.parse_args(argv).root).resolve())


if __name__ == "__main__":
    raise SystemExit(main())
