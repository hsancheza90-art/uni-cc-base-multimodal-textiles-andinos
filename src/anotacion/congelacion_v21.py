"""Congelación de la anotación estructural v2.1 y su comprobación en el flujo.

Uso desde la raíz del repositorio:

    python -m src.anotacion.congelacion_v21 --congelar   # una sola vez, al cerrar la anotación
    python -m src.anotacion.congelacion_v21              # paso del flujo: comprueba y escribe el informe

La versión 2.1 es la anotación del núcleo que exporta src/anotacion/aplicar_anotaciones_v2.py
después de la re-anotación del lote 1 (R14), la revisión de criterios de los lotes 2 a 5 (R18 a
R21) y el traslado de las anotaciones desplazadas (R22). `--congelar` escribe una copia fija en la
carpeta de [congelacion] de config/anotacion.toml, con las sumas SHA-256 de la copia y de sus
insumos, y se niega si la revisión tiene pendientes, imágenes que no coinciden o errores, o si la
copia ya existe.

En el flujo, este paso compara la anotación recién exportada con la copia congelada. Si difieren,
termina con código 1: después de congelar, ningún cambio en los workbooks pasa en silencio. Los
sistemas (M3 y la fusión) leen la copia congelada, no la exportación.
"""

from __future__ import annotations

import argparse
import hashlib
from collections import Counter
from pathlib import Path
from typing import Any

from src.anotacion import aplicar_anotaciones_v2 as exportacion
from src.anotacion import revision_criterios
from src.utils.archivos import escribir_csv, escribir_texto, leer_csv
from src.utils.config import CONFIG_ANOTACION, leer_config_anotacion
from src.utils.metricas import tabla
from src.utils.vocabulario import leer_vocabulario

REPORTE = "outputs/reports/anotacion_v2_1_congelada.md"
ARCHIVO = "anotaciones_v2_1.csv"
SUMAS = "sha256.txt"
# Insumos de la anotación cuya suma se registra al congelar (informativa: el flujo compara la exportación).
INSUMOS = ["data/metadata/anotacion_v2.xlsx", "data/metadata/anotacion_v2_reanotacion.xlsx",
           "data/metadata/anotacion_v2_revision_criterios.xlsx", "data/metadata/anotacion_v2_revision_criterios_seleccion.csv",
           "config/anotacion.toml", "config/vocabulario.toml"]


def sha256(ruta: Path) -> str:
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def carpeta(raiz: Path, config: dict[str, Any]) -> Path:
    return raiz / config["congelacion"]["carpeta"]


def ruta_congelada(raiz: Path, config: dict[str, Any] | None = None) -> Path:
    """Ruta de la anotación congelada, la que leen los sistemas."""
    return carpeta(raiz, config or leer_config_anotacion(raiz)) / ARCHIVO


def congelar(raiz: Path) -> int:
    config = leer_config_anotacion(raiz)
    vocabulario = leer_vocabulario(raiz)
    destino = carpeta(raiz, config)
    if (destino / ARCHIVO).exists():
        print(f"La anotacion v{config['congelacion']['version']} ya esta congelada en {destino}: no se sobrescribe.")
        return 1
    base = exportacion.base_adjudicada(raiz, config, vocabulario)
    if base is None:
        print("La anotacion v2 tiene errores: corrijalos antes de congelar.")
        return 1
    revision = revision_criterios.aplicar(base, revision_criterios.leer_decisiones(raiz, config), config, vocabulario,
                                          revision_criterios.leer_seleccion(raiz, config))
    impedimentos = ([f"{revision.pendientes} piezas pendientes en la revision de criterios"] if revision.pendientes else []) \
        + ([f"imagenes que no corresponden al registro: {revision.no_coinciden}"] if revision.no_coinciden else []) \
        + revision.errores
    if not revision.existe or impedimentos:
        print("No se congela la anotacion:")
        for problema in impedimentos or ["no existe el workbook de revision de criterios"]:
            print(f"- {problema}")
        return 1
    escribir_csv(destino / ARCHIVO, exportacion.COLUMNAS_ANOTACIONES_V2, revision.filas)
    relativa = (destino / ARCHIVO).relative_to(raiz).as_posix()
    escribir_texto(destino / SUMAS, [f"{sha256(raiz / r)}  {r}" for r in [relativa, *INSUMOS]])
    print(f"Anotacion v{config['congelacion']['version']} congelada: {len(revision.filas)} piezas -> {relativa}")
    return 0


def lineas_reporte(config: dict[str, Any], congelada: list[dict[str, str]] | None, coincide: bool,
                   sumas: list[str]) -> list[str]:
    datos = config["congelacion"]
    lineas = [
        f"# Anotacion estructural v{datos['version']} congelada",
        "",
        "Generado por `python -m src.anotacion.congelacion_v21`, paso del flujo. Parametros en "
        f"`{CONFIG_ANOTACION.as_posix()}` ([congelacion]).",
        "",
    ]
    if congelada is None:
        return lineas + ["La anotacion todavia no esta congelada: se congela con "
                         "`python -m src.anotacion.congelacion_v21 --congelar` cuando la revision de criterios no tiene "
                         "pendientes."]
    lineas += [
        f"- Copia congelada: `{datos['carpeta']}/{ARCHIVO}`, {len(congelada)} piezas; fecha de congelacion: {datos['fecha']}.",
        f"- La anotacion exportada por el flujo {'coincide' if coincide else 'NO coincide'} con la copia congelada.",
        "- Contiene la re-anotacion del lote 1 (R14), las correcciones de la revision de criterios de los lotes 2 a 5 "
        "(R18 a R21) y las anotaciones trasladadas (R22). Los sistemas leen esta copia.",
        "",
        "## Piezas por lote y estado",
        "",
    ]
    por_lote = Counter((f["lote"], f["estado_anotacion"]) for f in congelada)
    estados = sorted({e for _, e in por_lote})
    lineas += tabla([[lote] + [str(por_lote[(lote, e)]) for e in estados]
                     for lote in sorted({f["lote"] for f in congelada})], ["Lote", *estados])
    for atributo in ("composicion", "simetria", "eje_bandas"):
        lineas += ["", f"## `{atributo}`", ""]
        conteo = Counter(f[atributo] for f in congelada)
        lineas += tabla([[v, str(n)] for v, n in sorted(conteo.items())], ["Valor", "Piezas"])
    lineas += ["", "## Sumas SHA-256 registradas al congelar", "", "```", *sumas, "```"]
    return lineas


def comprobar(raiz: Path) -> int:
    config = leer_config_anotacion(raiz)
    destino = carpeta(raiz, config)
    if not (destino / ARCHIVO).exists():
        escribir_texto(raiz / REPORTE, lineas_reporte(config, None, False, []))
        print("La anotacion v2.1 no esta congelada todavia.")
        return 0
    exportada = raiz / exportacion.SALIDA_ANOTACIONES_V2
    coincide = exportada.read_bytes() == (destino / ARCHIVO).read_bytes()
    sumas = (destino / SUMAS).read_text(encoding="utf-8").splitlines() if (destino / SUMAS).exists() else []
    registrada = sumas[0].split()[0] if sumas else ""
    integra = registrada == sha256(destino / ARCHIVO)
    escribir_texto(raiz / REPORTE, lineas_reporte(config, leer_csv(destino / ARCHIVO), coincide, sumas))
    if not integra:
        print(f"La copia congelada no coincide con su suma registrada en {destino / SUMAS}.")
        return 1
    if not coincide:
        print(f"La anotacion exportada ({exportacion.SALIDA_ANOTACIONES_V2}) cambio despues de congelar la "
              f"v{config['congelacion']['version']}. Deshaga el cambio en los workbooks o registre una nueva version.")
        return 1
    print(f"Anotacion v{config['congelacion']['version']} congelada: la exportacion coincide ({destino / ARCHIVO}).")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Congela la anotacion v2.1 o comprueba que no cambio.")
    parser.add_argument("--root", default=".", help="Raiz del repositorio.")
    parser.add_argument("--congelar", action="store_true", help="Escribe la copia congelada (una sola vez).")
    args = parser.parse_args(argv)
    raiz = Path(args.root).resolve()
    return congelar(raiz) if args.congelar else comprobar(raiz)


if __name__ == "__main__":
    raise SystemExit(main())
