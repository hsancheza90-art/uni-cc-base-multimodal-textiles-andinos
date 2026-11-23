"""Planificación de la potencia de H1 y H2, antes del test (protocolo, sección 7; R04, R29, R34 y R35).

Uso desde la raíz del repositorio:

    python -m src.experimento.potencia

Para H1 (M4 frente a M2), con los rankings y los juicios de desarrollo, calcula la desviación
estándar de las diferencias pareadas de nDCG@10 y, con el número de consultas de prueba, el efecto
mínimo detectable con potencia del 80 % y nivel 0,05, con el rango que resulta de estimar la
desviación con pocas consultas. Para H2 (M3 frente a M3-sin-orden), cuya p es exacta y discreta,
informa la p mínima alcanzable y el umbral equivalente en las consultas con palabra de bandas, en
lugar de un efecto mínimo detectable por aproximación normal. No calcula potencia a posteriori ni
usa consultas de prueba (solo cuenta cuántas tienen palabra de bandas).

El informe no muestra el nDCG medio de ningún sistema ni la dirección de las diferencias: el
evaluador juzga después la prueba y no debe conocerlas.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path

import numpy as np

from src.anotacion import congelacion_v21
from src.experimento import evaluacion
from src.experimento.pesos_m4 import leer_juicios
from src.experimento.rankings import SALIDA_RANKINGS
from src.experimento.snapshot import SALIDA_CONSULTAS
from src.modelos import m3_estructura
from src.utils.archivos import escribir_texto, indexar, leer_csv
from src.utils.config import leer_config_experimento
from src.utils.metricas import tabla

REPORTE = "outputs/reports/experimento_v2_potencia.md"
ALFA = 0.05
POTENCIA = 0.8


def ndcg_por_consulta(raiz: Path, k: int) -> dict[str, dict[str, float | None]]:
    """ndcg[sistema][consulta] en desarrollo."""
    rankings: dict[tuple[str, str], list[tuple[int, str]]] = defaultdict(list)
    for fila in leer_csv(raiz / SALIDA_RANKINGS):
        rankings[(fila["sistema"], fila["consulta"])].append((int(fila["rango"]), fila["id_global"]))
    juicios = leer_juicios(raiz)
    resultado: dict[str, dict[str, float | None]] = defaultdict(dict)
    for (sistema, consulta), lista in rankings.items():
        ranking = [i for _, i in sorted(lista)]
        resultado[sistema][consulta] = evaluacion.ndcg(ranking, juicios.get(consulta, {}), k)
    return resultado


def consultas_con_palabra(raiz: Path, particion: str) -> set[str]:
    anotacion = indexar(leer_csv(congelacion_v21.ruta_congelada(raiz)), "id_global")
    return {c["consulta"] for c in leer_csv(raiz / SALIDA_CONSULTAS)
            if c["particion"] == particion and m3_estructura.palabra_de_bandas(anotacion[c["id_global"]]["secuencia_bandas"])}


def fila_potencia(nombre: str, d: list[float], n_prueba: int, umbral: float, confianza: float) -> list[str]:
    if len(d) < 3:
        # Con menos de tres diferencias la DE y su rango (aproximacion de Wilson y Hilferty) no son estimables.
        return [nombre, str(len(d)), "no estimable", "—", "—", str(n_prueba), "—"]
    de = float(np.std(d, ddof=1))
    if de == 0:
        return [nombre, str(len(d)), "0", "0", "—", str(n_prueba), "no estimable (sin variacion)"]
    bajo, alto = evaluacion.rango_desviacion(de, len(d), confianza)
    emd = evaluacion.efecto_minimo_detectable(de, n_prueba, ALFA, POTENCIA)
    rango = (f"{evaluacion.efecto_minimo_detectable(bajo, n_prueba, ALFA, POTENCIA):.3f} a "
             f"{evaluacion.efecto_minimo_detectable(alto, n_prueba, ALFA, POTENCIA):.3f}")
    necesarias = evaluacion.consultas_necesarias(de, umbral, ALFA, POTENCIA)
    return [nombre, str(len(d)), f"{de:.3f}", f"{emd:.3f}", rango, str(n_prueba), str(necesarias)]


def m_minimo(alfa: float = ALFA) -> int:
    """Menor número de diferencias distintas de cero con el que la prueba exacta puede dar p < alfa."""
    m = 1
    while evaluacion.p_minima(m) >= alfa:
        m += 1
    return m


def fila_exacta(nombre: str, d: list[float], b_prueba: int, n_prueba: int, umbral: float, tolerancia: float) -> list[str]:
    """Planificación de H2 con la prueba exacta (R35): sin aproximación normal ni efecto mínimo detectable.

    Informa cuántas diferencias de desarrollo son distintas de cero (no su signo), el número de
    consultas de prueba con palabra de bandas (cota de m), la p mínima alcanzable si todas ellas
    dieran diferencia distinta de cero y el umbral práctico equivalente en ese subgrupo."""
    no_nulas = int((evaluacion.sin_empates(d, tolerancia) != 0).sum())
    equivalente = f"{umbral * n_prueba / b_prueba:.3f}" if b_prueba else "no estimable"
    return [nombre, str(len(d)), str(no_nulas), str(b_prueba), f"{evaluacion.p_minima(b_prueba):.4f}",
            str(m_minimo()), equivalente]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Efecto minimo detectable de H1 y H2 antes del test.")
    parser.add_argument("--root", default=".", help="Raiz del repositorio.")
    raiz = Path(parser.parse_args(argv).root).resolve()
    if not (raiz / SALIDA_RANKINGS).exists():
        print(f"No existe {SALIDA_RANKINGS}: no hay potencia que estimar.")
        return 0
    config = leer_config_experimento(raiz)
    k, umbral, confianza = int(config["metricas"]["k"]), float(config["metricas"]["umbral_practico"]), float(config["metricas"]["confianza"])
    n_prueba = int(config["consultas_t3"]["prueba"])
    ndcg = ndcg_por_consulta(raiz, k)
    if "M4" not in ndcg:
        print("M4 no esta en los rankings de desarrollo: no hay potencia que estimar para H1.")
        return 0
    d_h1, excl_h1 = evaluacion.diferencias(ndcg["M4"], ndcg["M2"])
    d_h2, excl_h2 = evaluacion.diferencias(ndcg["M3"], ndcg["M3-sin-orden"])
    con_palabra_dev = consultas_con_palabra(raiz, "desarrollo")
    n_secundario = len(consultas_con_palabra(raiz, "prueba"))
    tolerancia = float(config["metricas"]["tolerancia_empates"])
    lineas = [
        "# Planificacion de la potencia antes del test (desarrollo)",
        "",
        "Generado por `python -m src.experimento.potencia`, paso del flujo (protocolo, seccion 7; decisiones R04, R27, "
        "R29, R34 y R35). **No se informa el nDCG medio de ningun sistema ni el signo de las diferencias**: el evaluador "
        "juzga despues la prueba.",
        "",
        "## H1: efecto minimo detectable",
        "",
        "Con las diferencias pareadas de nDCG@10 en las consultas de desarrollo y el numero de consultas de prueba, con "
        f"nivel {ALFA} y potencia {POTENCIA:.0%}: EMD = (z_0,975 + z_0,8) · DE / raiz(n). El rango usa el intervalo del "
        f"{confianza:.0%} de la DE estimada con pocas consultas. Es una estimacion aproximada de planificacion, no una "
        "frontera: no garantiza que un efecto mayor se detecte ni que uno menor no se detecte (R34).",
        "",
    ]
    lineas += tabla([fila_potencia("H1: M4 frente a M2", d_h1, n_prueba, umbral, confianza)],
                    ["Comparacion", "Consultas de desarrollo", "DE de las diferencias", "EMD con n de prueba",
                     "Rango del EMD", "n de prueba", f"Consultas para detectar {umbral}"])
    lineas += [
        "",
        "## H2: prueba exacta",
        "",
        "H2 se contrasta con la enumeracion exacta de los 2^m cambios de signo, con m el numero de diferencias distintas "
        "de cero (R35). Solo pueden ser distintas de cero las de las consultas con palabra de bandas (R27), de modo que "
        "m <= b. La distribucion es discreta y la aproximacion normal no vale: en lugar de un efecto minimo detectable se "
        "informa la p minima alcanzable, 2^(1 - m), y el umbral practico equivalente en el subgrupo, 0,03 · n / b. La "
        "version anterior de este informe (R29) daba para H2 un EMD de 0,026 con la aproximacion normal; esa cifra se retira.",
        "",
    ]
    lineas += tabla([fila_exacta("H2: M3 frente a M3-sin-orden", d_h2, n_secundario, n_prueba, umbral, tolerancia)],
                    ["Comparacion", "Consultas de desarrollo", "Diferencias distintas de cero en desarrollo",
                     "b: consultas de prueba con bandas", "p minima con m = b", f"m minimo para p < {ALFA}",
                     f"Umbral equivalente en el subgrupo (n = {n_prueba})"])
    lineas += [
        "",
        f"- Consultas de desarrollo excluidas por no tener relevantes: H1 {len(excl_h1)}, H2 {len(excl_h2)}.",
        f"- Con m de {m_minimo() - 1} o menos, la prueba exacta no puede dar p < {ALFA} cualquiera sea el resultado.",
        f"- El analisis del subgrupo tiene {len(con_palabra_dev)} consultas de desarrollo con palabra de bandas y "
        f"{n_secundario} de prueba; es descriptivo y no puede confirmar H2 (R33).",
        "- H2 solo recibe una conclusion confirmatoria si H1 se sostiene (secuencia fija, R33): con esta potencia, una "
        "conclusion confirmatoria sobre H2 es improbable.",
        "",
        "Lectura: un resultado no significativo se informara como «no se detecto una mejora», no como ausencia de efecto. "
        "El numero de consultas de prueba no se modifica despues de abrir el test.",
    ]
    escribir_texto(raiz / REPORTE, lineas)
    print(f"Efecto minimo detectable: H1 y H2 -> {REPORTE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
