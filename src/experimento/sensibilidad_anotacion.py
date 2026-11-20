"""Sensibilidad de M3 a la revisión asistida de la anotación (desarrollo, exploratorio).

Uso desde la raíz del repositorio:

    python -m src.experimento.sensibilidad_anotacion --crear   # escribe la anotación previa (lee git, fuera del flujo)
    python -m src.experimento.sensibilidad_anotacion           # compara y escribe el informe (paso del flujo)

La anotación v2.1 incluye las correcciones de la revisión de criterios de los lotes 2 a 5, que
partió de propuestas automáticas verificadas y firmadas por el anotador (decisiones R18 a R22). Este
análisis mide cuánto cambian los rankings de M3 y de M3-sin-orden en las consultas de desarrollo si
se usa la anotación anterior a esa revisión en lugar de la v2.1.

Anotación previa: la exportación de data/metadata/anotaciones_v2.csv en el commit d0bce67 (12 de
noviembre), que ya incluye la re-anotación del lote 1 (R14) y todavía no la revisión. Ocho de sus
filas describían la imagen de otro registro (R20); para que la comparación mida solo la revisión y
no ese error, `--crear` traslada cada una a la fila de la imagen que describe, sin corregirla. El
resultado se versiona como insumo en data/metadata/anotacion_v2_previa_revision.csv.

Solo usa consultas y juicios de desarrollo; no ejecuta ninguna consulta de prueba. Los pesos son los
de [m3.pesos] en config/modelos.toml. El informe da cifras por consulta sin identificadores de
candidatos.
"""

from __future__ import annotations

import argparse
import csv
import io
import subprocess
from collections import Counter
from pathlib import Path

import numpy as np

from src.anotacion import congelacion_v21
from src.experimento import evaluacion
from src.experimento.juicios import NO_EVALUABLE, SALIDA_JUICIOS
from src.experimento.rankings import ordenar, similitud_m3
from src.experimento.snapshot import SALIDA_CONSULTAS, SALIDA_PARTICIONES
from src.modelos import m3_estructura
from src.utils.archivos import escribir_csv, escribir_texto, indexar, leer_csv
from src.utils.config import leer_config_experimento, leer_config_modelos
from src.utils.metricas import tabla

PREVIA = "data/metadata/anotacion_v2_previa_revision.csv"
REPORTE = "outputs/reports/experimento_v2_sensibilidad_anotacion.md"
COMMIT_PREVIA = "d0bce67"
ORIGEN_PREVIA = "data/metadata/anotaciones_v2.csv"
SISTEMAS = ("M3", "M3-sin-orden")
ATRIBUTOS_M3 = ["composicion", "secuencia_bandas", "borde", "centro", "simetria", "repeticion", "motivos",
                "familia_iconografica"]
# Fila cuya anotación describía la imagen de otro registro -> registro de esa imagen (decisiones R20 y R22).
DESPLAZADAS = {
    "AIC:85282": "MET:307933",
    "AIC:85310": "AIC:85282",
    "CMA:155505": "AIC:85310",
    "AIC:223218": "CMA:155505",
    "AIC:85388": "AIC:223218",
    "MET:307933": "AIC:85388",
    "MET:316978": "MET:316341",
    "MET:316341": "MET:316978",
}


# --------------------------------------------------------------------------- insumo


def trasladar(filas: list[dict[str, str]]) -> list[dict[str, str]]:
    """Mueve los atributos de cada anotación desplazada a la fila de la imagen que describe."""
    por_id = {f["id_global"]: f for f in filas}
    salida = []
    for fila in filas:
        origen = next((x for x, destino in DESPLAZADAS.items() if destino == fila["id_global"]), None)
        if origen is None:
            salida.append(dict(fila))
            continue
        nueva = dict(fila)
        for atributo in ATRIBUTOS_M3 + ["eje_bandas"]:
            nueva[atributo] = por_id[origen][atributo]
        salida.append(nueva)
    return salida


def crear(raiz: Path, git: str) -> int:
    texto = subprocess.run([git, "show", f"{COMMIT_PREVIA}:{ORIGEN_PREVIA}"], cwd=raiz, capture_output=True,
                           check=True).stdout.decode("utf-8")
    filas = list(csv.DictReader(io.StringIO(texto)))
    escribir_csv(raiz / PREVIA, list(filas[0]), trasladar(filas))
    print(f"Anotacion previa a la revision ({COMMIT_PREVIA}, {len(filas)} piezas, 8 trasladadas) -> {PREVIA}")
    return 0


# --------------------------------------------------------------------------- comparacion


def spearman(a: list[str], b: list[str]) -> float:
    """Correlación de Spearman entre las posiciones de los mismos candidatos en dos rankings."""
    pos_b = {i: r for r, i in enumerate(b)}
    x = np.arange(len(a), dtype=float)
    y = np.array([pos_b[i] for i in a], dtype=float)
    return float(np.corrcoef(x, y)[0, 1]) if len(a) > 1 else float("nan")


def leer_juicios(raiz: Path) -> dict[str, dict[str, int | None]]:
    juicios: dict[str, dict[str, int | None]] = {}
    for fila in leer_csv(raiz / SALIDA_JUICIOS):
        if fila["relevancia"]:
            valor = None if fila["relevancia"] == NO_EVALUABLE else int(fila["relevancia"])
            juicios.setdefault(fila["consulta"], {})[fila["id_global"]] = valor
    return juicios


def cambios_por_atributo(previa: dict[str, dict[str, str]], v21: dict[str, dict[str, str]]) -> Counter:
    return Counter(a for i in v21 for a in ATRIBUTOS_M3 if previa[i][a] != v21[i][a])


def fmt(x: float | None, d: int = 3) -> str:
    return "—" if x is None or x != x else f"{x:.{d}f}"


def comparar(raiz: Path) -> int:
    if not (raiz / PREVIA).exists():
        print(f"No existe {PREVIA}: no hay anotacion previa que comparar.")
        return 0
    particiones = leer_csv(raiz / SALIDA_PARTICIONES)
    galeria = [f["id_global"] for f in particiones]
    grupo = {f["id_global"]: f["grupo"] for f in particiones}
    consultas = [c for c in leer_csv(raiz / SALIDA_CONSULTAS) if c["particion"] == "desarrollo"]
    pesos = {b: float(p) for b, p in leer_config_modelos(raiz)["m3"]["pesos"].items()}
    k = int(leer_config_experimento(raiz)["metricas"]["k"])
    juicios = leer_juicios(raiz)

    previa = indexar(leer_csv(raiz / PREVIA), "id_global")
    v21 = indexar(leer_csv(congelacion_v21.ruta_congelada(raiz)), "id_global")
    versiones = {"previa": previa, "v2.1": v21}
    funciones = {}
    for nombre, anotacion in versiones.items():
        descriptores = {i: m3_estructura.descriptor(anotacion[i]) for i in galeria}
        for sistema in SISTEMAS:
            funciones[(nombre, sistema)] = similitud_m3(descriptores, pesos, sin_orden=sistema == "M3-sin-orden")

    filas, ndcg = [], {}
    for consulta in consultas:
        q, nombre_c = consulta["id_global"], consulta["consulta"]
        candidatos = [c for c in galeria if grupo[c] != grupo[q]]
        rankings = {}
        for clave, funcion in funciones.items():
            rankings[clave] = [i for i, _ in ordenar({c: funcion(q, c) for c in candidatos})]
            ndcg[(clave, nombre_c)] = evaluacion.ndcg(rankings[clave], juicios.get(nombre_c, {}), k)
        for sistema in SISTEMAS:
            a, b = rankings[("previa", sistema)], rankings[("v2.1", sistema)]
            filas.append([
                nombre_c, sistema, "si" if previa[q] != v21[q] and any(previa[q][x] != v21[q][x] for x in ATRIBUTOS_M3)
                else "no", str(len(set(a[:k]) & set(b[:k]))), fmt(spearman(a, b)),
                fmt(ndcg[(("previa", sistema), nombre_c)]), fmt(ndcg[(("v2.1", sistema), nombre_c)]),
                fmt(evaluacion.proporcion_juzgada(a, juicios.get(nombre_c, {}), k), 2)])

    def media(nombre: str, sistema: str) -> float:
        valores = [ndcg[((nombre, sistema), c["consulta"])] for c in consultas]
        valores = [v for v in valores if v is not None]
        return sum(valores) / len(valores) if valores else float("nan")

    def delta_h2(nombre: str) -> list[float]:
        return [ndcg[((nombre, "M3"), c["consulta"])] - ndcg[((nombre, "M3-sin-orden"), c["consulta"])]
                for c in consultas if ndcg[((nombre, "M3"), c["consulta"])] is not None
                and ndcg[((nombre, "M3-sin-orden"), c["consulta"])] is not None]

    cambios = cambios_por_atributo(previa, v21)
    piezas_cambiadas = sum(1 for i in v21 if any(previa[i][a] != v21[i][a] for a in ATRIBUTOS_M3))
    con_bandas = {n: sum(1 for f in a.values() if m3_estructura.palabra_de_bandas(f["secuencia_bandas"]))
                  for n, a in versiones.items()}
    lineas = [
        "# Sensibilidad de M3 a la revision asistida de la anotacion (desarrollo)",
        "",
        "Generado por `python -m src.experimento.sensibilidad_anotacion` (`src/experimento/sensibilidad_anotacion.py`), "
        f"paso del flujo. Compara la anotacion previa a la revision de criterios (`{PREVIA}`: exportacion del commit "
        f"`{COMMIT_PREVIA}` con las ocho anotaciones desplazadas trasladadas a su fila, sin corregir) con la anotacion "
        "v2.1 congelada. Solo consultas y juicios de desarrollo; pesos de `[m3.pesos]`. Analisis exploratorio: no "
        "decide ninguna hipotesis.",
        "",
        "## Cambios en la anotacion",
        "",
        f"- Piezas del nucleo con algun atributo de M3 distinto: {piezas_cambiadas} de {len(v21)}.",
        f"- Piezas con palabra de bandas: previa {con_bandas['previa']}, v2.1 {con_bandas['v2.1']}.",
        "",
    ]
    lineas += tabla([[a, str(cambios[a])] for a in ATRIBUTOS_M3], ["Atributo", "Piezas con valor distinto"])
    lineas += ["", "## Rankings por consulta de desarrollo", "",
               f"`Top {k} comun`: candidatos compartidos por los {k} primeros de las dos versiones. `Spearman`: "
               "correlacion entre las posiciones de todos los candidatos. `Juzgada`: parte del top de la version previa "
               "con juicio (el pool se construyo con la v2.1; un candidato sin juicio cuenta como 0).", ""]
    lineas += tabla(filas, ["Consulta", "Sistema", "Consulta cambiada", f"Top {k} comun", "Spearman",
                            f"nDCG@{k} previa", f"nDCG@{k} v2.1", "Juzgada (previa)"])
    d_prev, d_v21 = delta_h2("previa"), delta_h2("v2.1")
    lineas += ["", "## Resumen", ""]
    lineas += tabla([[s, fmt(media("previa", s)), fmt(media("v2.1", s))] for s in SISTEMAS],
                    ["Sistema", f"nDCG@{k} medio, previa", f"nDCG@{k} medio, v2.1"])
    lineas += ["",
               f"- Diferencia M3 - M3-sin-orden (control de H2), media por consulta: previa {fmt(sum(d_prev) / len(d_prev) if d_prev else None)}"
               f" ({sum(1 for d in d_prev if d != 0)} de {len(d_prev)} consultas distintas de cero); v2.1 "
               f"{fmt(sum(d_v21) / len(d_v21) if d_v21 else None)} ({sum(1 for d in d_v21 if d != 0)} de {len(d_v21)}).",
               "",
               "Lectura. La comparacion de rankings (top comun y Spearman) no depende de los juicios y es la medida principal "
               "de la sensibilidad. El nDCG debe leerse con dos reservas. Primera: el pool se construyo con la v2.1, de modo "
               "que el nDCG de la version previa se subestima cuando su top incluye candidatos sin juicio. Segunda: las "
               "propuestas de la revision de criterios (R20) y la segunda opinion de los juicios de desarrollo (R25) "
               "provienen de la misma familia de modelos; una mejora del nDCG con la v2.1 puede reflejar ese criterio "
               "compartido y no una anotacion mas fiel a la imagen."]
    escribir_texto(raiz / REPORTE, lineas)
    print(f"Sensibilidad de M3 a la revision de la anotacion: {len(consultas)} consultas -> {REPORTE}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Sensibilidad de M3 a la revision asistida de la anotacion.")
    parser.add_argument("--root", default=".", help="Raiz del repositorio.")
    parser.add_argument("--crear", action="store_true", help="Escribe la anotacion previa desde el historial de git.")
    parser.add_argument("--git", default="git", help="Ejecutable de git (solo con --crear).")
    args = parser.parse_args(argv)
    raiz = Path(args.root).resolve()
    return crear(raiz, args.git) if args.crear else comparar(raiz)


if __name__ == "__main__":
    raise SystemExit(main())
