"""Efecto mínimo detectable de H1 y H2, calculado antes del test (protocolo, sección 7; decisión R04).

Uso desde la raíz del repositorio:

    python -m src.experimento.potencia

Con los rankings y los juicios de desarrollo calcula, por consulta, el nDCG@10 de los sistemas que
comparan H1 (M4 frente a M2) y H2 (M3 frente a M3-sin-orden), la desviación estándar de las
diferencias pareadas y, con el número de consultas de prueba, el efecto mínimo detectable con
potencia del 80 % y nivel 0,05, con el rango que resulta de estimar la desviación con pocas
consultas. Para el análisis secundario de H2 (R27) usa las consultas cuya pieza tiene palabra de
bandas. No calcula potencia a posteriori ni usa consultas de prueba.

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
    d_h2s, _ = evaluacion.diferencias({c: v for c, v in ndcg["M3"].items() if c in con_palabra_dev},
                                       {c: v for c, v in ndcg["M3-sin-orden"].items() if c in con_palabra_dev})
    nulas_h2 = sum(1 for x in d_h2 if x == 0)
    lineas = [
        "# Efecto minimo detectable antes del test (desarrollo)",
        "",
        "Generado por `python -m src.experimento.potencia`, paso del flujo (protocolo, seccion 7; decisiones R04 y R27). "
        "Se calcula con las diferencias pareadas de nDCG@10 en las consultas de desarrollo y el numero de consultas de "
        f"prueba, con nivel {ALFA} y potencia {POTENCIA:.0%}: EMD = (z_0,975 + z_0,8) · DE / raiz(n). El rango usa el "
        f"intervalo del {confianza:.0%} de la DE estimada con pocas consultas. **No se informa el nDCG medio de ningun "
        "sistema ni el signo de las diferencias**: el evaluador juzga despues la prueba.",
        "",
    ]
    lineas += tabla([
        fila_potencia("H1: M4 frente a M2", d_h1, n_prueba, umbral, confianza),
        fila_potencia("H2: M3 frente a M3-sin-orden (30 consultas)", d_h2, n_prueba, umbral, confianza),
        fila_potencia("H2 secundario: consultas con palabra de bandas", d_h2s, n_secundario, umbral, confianza),
    ], ["Comparacion", "Consultas de desarrollo", "DE de las diferencias", "EMD con n de prueba",
        "Rango del EMD", "n de prueba", f"Consultas para detectar {umbral}"])
    lineas += [
        "",
        f"- Consultas de desarrollo excluidas por no tener relevantes: H1 {len(excl_h1)}, H2 {len(excl_h2)}.",
        f"- En H2, {nulas_h2} de {len(d_h2)} diferencias de desarrollo son exactamente cero: las consultas sin palabra de "
        "bandas dan el mismo score en M3 y en su control (R27). Por eso su DE es pequena, pero el efecto medio se diluye "
        f"en la misma proporcion: si solo actua en las {n_secundario} consultas de prueba con bandas, en ellas tendria que ser "
        f"unas {n_prueba}/{n_secundario} veces el EMD de la tabla para detectarse en la media de las {n_prueba}.",
        f"- El analisis secundario de H2 tiene {len(con_palabra_dev)} consultas de desarrollo con palabra de bandas y "
        f"{n_secundario} de prueba; con tan pocas consultas de desarrollo su desviacion no es estimable con fiabilidad.",
        "",
        "Lectura: si el EMD supera el umbral practico, el estudio no tiene potencia para detectar un efecto de esa "
        "magnitud. Un resultado no significativo se informara entonces como «no se detecto una mejora de la magnitud "
        "detectable», no como ausencia de efecto. El numero de consultas de prueba no se modifica despues de abrir el test.",
    ]
    escribir_texto(raiz / REPORTE, lineas)
    print(f"Efecto minimo detectable: H1 y H2 -> {REPORTE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
