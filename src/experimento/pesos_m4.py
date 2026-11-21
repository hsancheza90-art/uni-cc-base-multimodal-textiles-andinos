"""Selección de los pesos de M4 en desarrollo (protocolo experimental, sección 4; decisión R28).

Uso desde la raíz del repositorio:

    python -m src.experimento.pesos_m4

Para cada combinación de la rejilla de `[m4]` (config/modelos.toml), fusiona los scores de M0, M2
y M3 de cada consulta de desarrollo (data/processed/experimento_v2_rankings_desarrollo.csv), mide
el nDCG@10 con los juicios de desarrollo (los candidatos sin juicio cuentan como 0) y aplica la
regla de elección fijada antes de ver resultados (`elegir` en src/modelos/m4_fusion.py).

Los pesos se eligieron una sola vez, con los juicios existentes al 21 de noviembre de 2026, y se
fijaron en `[m4] pesos`. Este paso documenta la selección y comprueba si la regla, con los juicios
vigentes, sigue eligiendo esos pesos; no los cambia. Solo usa consultas de desarrollo.

El evaluador no abre el informe: contiene el rendimiento de los sistemas en desarrollo.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path

from src.experimento import evaluacion
from src.experimento.juicios import NO_EVALUABLE, SALIDA_JUICIOS
from src.experimento.rankings import SALIDA_RANKINGS
from src.modelos import m4_fusion
from src.utils.archivos import escribir_texto, leer_csv
from src.utils.config import leer_config_experimento, leer_config_modelos
from src.utils.metricas import tabla

REPORTE = "outputs/reports/experimento_v2_pesos_m4.md"


def leer_scores(raiz: Path) -> dict[str, dict[str, dict[str, float | None]]]:
    """scores[consulta][componente][candidato] de los componentes de M4."""
    scores: dict[str, dict[str, dict[str, float | None]]] = defaultdict(lambda: defaultdict(dict))
    for fila in leer_csv(raiz / SALIDA_RANKINGS):
        if fila["sistema"] in m4_fusion.COMPONENTES:
            scores[fila["consulta"]][fila["sistema"]][fila["id_global"]] = (
                float(fila["score"]) if fila["score"] != "" else None)
    return scores


def leer_juicios(raiz: Path) -> dict[str, dict[str, int | None]]:
    juicios: dict[str, dict[str, int | None]] = defaultdict(dict)
    for fila in leer_csv(raiz / SALIDA_JUICIOS):
        if fila["relevancia"]:
            juicios[fila["consulta"]][fila["id_global"]] = None if fila["relevancia"] == NO_EVALUABLE else int(fila["relevancia"])
    return juicios


def ranking_m4(scores: dict[str, dict[str, float | None]], pesos: dict[str, float]) -> list[str]:
    fusion = m4_fusion.fusionar({c: scores[c] for c in m4_fusion.COMPONENTES}, pesos)
    return [i for i, _ in m4_fusion.ordenar({i: f.score for i, f in fusion.items()})]


def evaluar(scores, juicios, pesos: dict[str, float], k: int) -> tuple[float, float]:
    """nDCG@k medio (consultas con algún relevante) y proporción juzgada media del top k."""
    ndcgs, juzgadas = [], []
    for consulta, por_componente in sorted(scores.items()):
        ranking = ranking_m4(por_componente, pesos)
        valor = evaluacion.ndcg(ranking, juicios.get(consulta, {}), k)
        if valor is not None:
            ndcgs.append(valor)
        juzgadas.append(evaluacion.proporcion_juzgada(ranking, juicios.get(consulta, {}), k))
    return (sum(ndcgs) / len(ndcgs) if ndcgs else float("nan"), sum(juzgadas) / len(juzgadas) if juzgadas else float("nan"))


def seleccionar(raiz: Path) -> tuple[dict[str, float], list[tuple[dict[str, float], float, float]]]:
    config = leer_config_modelos(raiz)["m4"]
    k = int(leer_config_experimento(raiz)["metricas"]["k"])
    scores, juicios = leer_scores(raiz), leer_juicios(raiz)
    filas = [(pesos, *evaluar(scores, juicios, pesos, k)) for pesos in m4_fusion.rejilla(config["rejilla"])]
    elegidos = m4_fusion.elegir([(pesos, ndcg) for pesos, ndcg, _ in filas])
    return elegidos, filas


def fmt(x: float, d: int = 3) -> str:
    return "—" if x != x else f"{x:.{d}f}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Seleccion de los pesos de M4 en desarrollo.")
    parser.add_argument("--root", default=".", help="Raiz del repositorio.")
    raiz = Path(parser.parse_args(argv).root).resolve()
    config = leer_config_modelos(raiz).get("m4", {})
    if "rejilla" not in config or not (raiz / SALIDA_RANKINGS).exists() or not (raiz / SALIDA_JUICIOS).exists():
        print("Sin rejilla de M4, rankings o juicios de desarrollo: no hay pesos que seleccionar.")
        return 0
    elegidos, filas = seleccionar(raiz)
    fijados = {c: float(p) for c, p in config.get("pesos", {}).items()}
    coincide = bool(fijados) and all(abs(fijados.get(c, -1) - elegidos[c]) < 1e-9 for c in m4_fusion.COMPONENTES)
    orden = sorted(filas, key=lambda f: (-round(f[1], 9), f[0] != elegidos))
    lineas = [
        "# Seleccion de los pesos de M4 (desarrollo)",
        "",
        "Generado por `python -m src.experimento.pesos_m4`, paso del flujo. **El evaluador no abre este informe**: "
        "contiene el rendimiento de los sistemas en desarrollo. Solo consultas y juicios de desarrollo; los candidatos "
        "sin juicio cuentan como 0. Regla de eleccion fijada antes de ver resultados (`elegir`): mayor nDCG@10 medio; "
        "en empate, la combinacion mas cercana a pesos iguales y luego la primera en orden lexicografico descendente.",
        "",
        f"- Combinaciones de la rejilla {config['rejilla']}: {len(filas)} (normalizadas a suma 1, sin repetir).",
        f"- Pesos que elige la regla con los juicios vigentes: {', '.join(f'{c} = {elegidos[c]:.4f}' for c in m4_fusion.COMPONENTES)}.",
        ("- Pesos fijados en `[m4] pesos`: " + ", ".join(f"{c} = {fijados[c]:.4f}" for c in m4_fusion.COMPONENTES)
         + (". Coinciden con la eleccion vigente." if coincide else
            ". **No coinciden** con la eleccion vigente: los juicios cambiaron despues de fijarlos (R28); "
            "los pesos fijados no se modifican.")) if fijados else "- Aun no hay pesos fijados en `[m4] pesos`.",
        "",
        "## Las diez mejores combinaciones",
        "",
    ]
    lineas += tabla([[", ".join(f"{p:.2f}" for p in pesos.values()), fmt(ndcg), fmt(juzgada, 2)]
                     for pesos, ndcg, juzgada in orden[:10]],
                    ["Pesos (" + ", ".join(m4_fusion.COMPONENTES) + ")", "nDCG@10 medio", "Top 10 juzgado"])
    escribir_texto(raiz / REPORTE, lineas)
    print(f"Pesos de M4 en desarrollo: {len(filas)} combinaciones -> {REPORTE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
