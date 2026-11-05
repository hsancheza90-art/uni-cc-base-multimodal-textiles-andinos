"""Valida los workbooks de anotación v2 y exporta la primera anotación a CSV.

Paso del flujo (sin red). Lee los dos workbooks de [acuerdo] en config/anotacion.toml: la
primera anotación (anotador_a, data/metadata/anotacion_v2.xlsx) y la re-anotación ciega
(anotador_b). Recodifica etiquetas a códigos, valida cada pieza anotada contra el
vocabulario vigente (config/vocabulario.toml) y escribe:

- data/metadata/anotaciones_v2.csv: las piezas anotadas de la primera anotación, en el
  orden del workbook (núcleo por lote y orden, luego el resto del principal v2).
- outputs/reports/anotacion_v2_validacion.md: avance, cobertura, avisos y errores.

Una pieza está anotada si alguna de sus 19 columnas de anotación tiene valor. En cada una:

- errores (el paso termina con código 1 y no actualiza el CSV): un valor fuera del
  vocabulario o un estado que el atributo no admite; estado_anotacion vacío o sin_anotar;
  anotador vacío; fecha_anotacion vacía o que no existe en el calendario; eje_bandas y
  secuencia_bandas que no concuerdan (una dice que hay bandas y la otra no); un id_global
  repetido entre hojas.
- avisos (no detienen el flujo): atributos sin anotar en una pieza anotada; un desconocido
  en una pieza que no está en revisar (regla de los treinta segundos); una corrección igual
  al valor vigente; piezas anotadas que ya no están en el corpus.

El informe y la consola dan solo conteos, sin valores ni observaciones por pieza: el lote
de [reanotacion] se re-anota a ciegas y el anotador no debe ver su primera anotación. Los
errores sí se detallan, porque hay que corregirlos. Sin workbook de primera anotación, no
hace nada.
"""

from __future__ import annotations

import argparse
import re
from collections import Counter
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path
from typing import Any

from src.anotacion.aplicar_anotaciones import fecha_valida
from src.anotacion.workbook import CAMPO_DE_COLUMNA, HOJA_HUERFANAS
from src.consolidado.esquema import ATRIBUTOS_ANOTACION_V2, COLUMNAS_ANOTACIONES_V2, CORRECCIONES
from src.utils.archivos import escribir_csv, escribir_texto
from src.utils.config import CONFIG_ANOTACION, leer_config_anotacion
from src.utils.libros import leer_hoja
from src.utils.metricas import tabla
from src.utils.vocabulario import Campo, leer_vocabulario

SALIDA_ANOTACIONES_V2 = "data/metadata/anotaciones_v2.csv"
REPORTE_V2 = "outputs/reports/anotacion_v2_validacion.md"
ANOTABLES = ATRIBUTOS_ANOTACION_V2 + list(CORRECCIONES)
ESTADOS_ANOTADA = ("anotado_manual", "anotado_asistido", "revisar", "corregido", "descartado")
# Etiquetas con que el anotador marca en observaciones_anotacion lo que queda por decidir.
ETIQUETAS = ("DUDA", "CRITERIO", "VOCAB")
PATRON_ETIQUETA = re.compile(r"\b(DUDA|CRITERIO|VOCAB)\b")
ESTADOS_RESUMEN = ("ausente", "no_observable", "desconocido")


@dataclass
class Validacion:
    """Resultado de validar un workbook (primera anotación o re-anotación)."""

    ruta: str
    existe: bool
    piezas: int = 0
    anotadas: list[dict[str, str]] = field(default_factory=list)
    huerfanas: list[str] = field(default_factory=list)
    errores: list[str] = field(default_factory=list)
    avisos: Counter = field(default_factory=Counter)


# --------------------------------------------------------------------------- validacion


def esta_anotada(fila: dict[str, str]) -> bool:
    return any(fila.get(columna) for columna in ANOTABLES)


def tiene_bandas(valor: str, campo: Campo) -> bool:
    """True si el valor registra bandas (un eje o una secuencia), False si es un estado."""
    return valor not in campo.estados


def validar_fila(fila: dict[str, str], vocabulario: dict[str, Campo]) -> tuple[dict[str, str], list[str], list[str]]:
    """Pieza recodificada, sus errores y sus avisos (como claves de conteo)."""
    id_global = fila["id_global"]
    salida = {columna: fila.get(columna, "") for columna in COLUMNAS_ANOTACIONES_V2}
    errores: list[str] = []
    avisos: list[str] = []
    for columna in ANOTABLES + ["estado_anotacion"]:
        valor = salida[columna]
        if not valor:
            continue
        campo = vocabulario[CAMPO_DE_COLUMNA[columna]]
        salida[columna] = campo.recodificar(valor)
        invalidos = campo.invalidos(salida[columna])
        if invalidos:
            errores.append(f"{id_global}: {columna} fuera del vocabulario: {invalidos}")

    if salida["estado_anotacion"] not in ESTADOS_ANOTADA:
        errores.append(f"{id_global}: estado_anotacion debe ser uno de {', '.join(ESTADOS_ANOTADA)}")
    if not salida["anotador"]:
        errores.append(f"{id_global}: anotador vacio")
    if not fecha_valida(salida["fecha_anotacion"]):
        errores.append(f"{id_global}: fecha_anotacion vacia o invalida (AAAA-MM-DD)")

    eje, secuencia = salida["eje_bandas"], salida["secuencia_bandas"]
    if eje and secuencia:
        if tiene_bandas(eje, vocabulario["eje_bandas"]) != tiene_bandas(secuencia, vocabulario["secuencia_bandas"]):
            errores.append(f"{id_global}: eje_bandas y secuencia_bandas no concuerdan (una registra bandas y la otra un estado)")

    if any(not salida[columna] for columna in ATRIBUTOS_ANOTACION_V2):
        avisos.append("atributos sin anotar en una pieza anotada")
    if salida["estado_anotacion"] != "revisar" and any(salida[c] == "desconocido" for c in ATRIBUTOS_ANOTACION_V2):
        avisos.append("desconocido en una pieza que no esta en revisar (regla de los treinta segundos)")
    if any(salida[correccion] and salida[correccion] == fila.get(base, "") for correccion, base in CORRECCIONES.items()):
        avisos.append("correccion igual al valor vigente")
    return salida, errores, avisos


def validar_workbook(raiz: Path, ruta: str, hojas: list[str], vocabulario: dict[str, Campo]) -> Validacion:
    absoluta = raiz / ruta
    resultado = Validacion(ruta, absoluta.exists())
    if not resultado.existe:
        return resultado
    vistos: set[str] = set()
    for hoja in [*hojas, HOJA_HUERFANAS]:
        try:
            filas = leer_hoja(absoluta, hoja, clave="id_global")
        except ValueError:
            continue  # una hoja ausente no tiene piezas
        for fila in filas:
            id_global = fila["id_global"]
            if id_global in vistos:
                resultado.errores.append(f"{id_global}: aparece en mas de una hoja")
                continue
            vistos.add(id_global)
            if hoja != HOJA_HUERFANAS:
                resultado.piezas += 1
            if not esta_anotada(fila):
                if any(fila.get(c) for c in ("estado_anotacion", "anotador", "fecha_anotacion", "observaciones_anotacion")):
                    resultado.avisos["control lleno en una pieza sin atributos anotados"] += 1
                continue
            if hoja == HOJA_HUERFANAS:
                resultado.huerfanas.append(id_global)
                resultado.avisos["pieza anotada que ya no esta en el corpus (hoja fuera_del_corpus)"] += 1
                continue
            salida, errores, avisos = validar_fila(fila, vocabulario)
            resultado.errores += errores
            resultado.avisos.update(avisos)
            resultado.anotadas.append(salida)
    return resultado


# --------------------------------------------------------------------------- informe


def etiquetas_por_lote(anotadas: list[dict[str, str]]) -> dict[str, Counter]:
    """Piezas que usan cada etiqueta de observaciones, por lote (solo conteos)."""
    conteos: dict[str, Counter] = {}
    for fila in anotadas:
        usadas = set(PATRON_ETIQUETA.findall(fila.get("observaciones_anotacion", "")))
        conteos.setdefault(fila.get("lote", "") or "fuera del nucleo", Counter()).update(usadas)
    return conteos


def lineas_lotes(anotadas: list[dict[str, str]], config: dict[str, Any], con_inicio: bool = True) -> list[str]:
    """Tabla por lote; con_inicio agrega la fecha desde la que se puede re-anotar (primera anotacion)."""
    lote_reanotacion = str(config["reanotacion"]["lote"])
    dias = int(config["reanotacion"]["intervalo_minimo_dias"])
    por_lote: dict[str, list[dict[str, str]]] = {}
    for fila in anotadas:
        por_lote.setdefault(fila.get("lote", "") or "fuera del nucleo", []).append(fila)
    etiquetas = etiquetas_por_lote(anotadas)
    filas = []
    for lote, piezas in por_lote.items():
        fechas = sorted(date.fromisoformat(f["fecha_anotacion"]) for f in piezas if fecha_valida(f["fecha_anotacion"]))
        rango = f"{fechas[0]} a {fechas[-1]}" if fechas else ""
        estados = Counter(f["estado_anotacion"] for f in piezas)
        filas.append([lote, str(len(piezas)), rango, ", ".join(f"{e} {n}" for e, n in sorted(estados.items())),
                      *(str(etiquetas[lote][e]) for e in ETIQUETAS)])
    lineas = tabla(filas, ["Lote", "Anotadas", "Fechas", "estado_anotacion", *(f"Con {e}" for e in ETIQUETAS)])
    lote_a = [f for f in anotadas if f.get("lote", "") == lote_reanotacion and fecha_valida(f["fecha_anotacion"])]
    if lote_a and con_inicio:
        ultima = max(date.fromisoformat(f["fecha_anotacion"]) for f in lote_a)
        lineas += ["", f"Re-anotacion ciega del lote {lote_reanotacion}: puede empezar el {ultima + timedelta(days=dias)} "
                       f"({dias} dias despues de la ultima fecha del lote, {ultima})."]
    lineas += ["", "`Con DUDA`, `Con CRITERIO`, `Con VOCAB`: piezas cuyas observaciones usan esa etiqueta para marcar "
                   "lo que queda por decidir (una duda sobre un valor, un criterio de la guia o un hueco del vocabulario)."]
    return lineas


def lineas_cobertura(anotadas: list[dict[str, str]]) -> list[str]:
    filas = []
    for columna in ANOTABLES:
        estados = Counter(f[columna] for f in anotadas if f[columna] in ESTADOS_RESUMEN)
        con_valor = sum(bool(f[columna]) for f in anotadas)
        filas.append([f"`{columna}`", str(con_valor), str(len(anotadas) - con_valor),
                      *(str(estados[e]) for e in ESTADOS_RESUMEN)])
    return tabla(filas, ["Columna", "Con valor", "Vacias", *(f"`{e}`" for e in ESTADOS_RESUMEN)])


def lineas_workbook(validacion: Validacion, nombre: str) -> str:
    if not validacion.existe:
        return f"- {nombre}: `{validacion.ruta}` no existe todavia."
    return (f"- {nombre}: `{validacion.ruta}`: {validacion.piezas} piezas, {len(validacion.anotadas)} anotadas, "
            f"{len(validacion.errores)} errores.")


def lineas_reporte(a: Validacion, b: Validacion, config: dict[str, Any]) -> list[str]:
    lote = config["reanotacion"]["lote"]
    lineas = [
        "# Validacion de la anotacion v2",
        "",
        "Generado por `python -m src.anotacion.aplicar_anotaciones_v2` (`src/anotacion/aplicar_anotaciones_v2.py`), "
        f"paso del flujo. Workbooks de [acuerdo] en `{CONFIG_ANOTACION.as_posix()}`; vocabulario: `config/vocabulario.toml`.",
        "",
        f"Este informe da solo conteos, sin valores ni observaciones por pieza: el lote {lote} se re-anota a ciegas y el "
        "anotador no debe ver su primera anotacion. Los errores, si los hay, se detallan para poder corregirlos.",
        "",
        lineas_workbook(a, "Primera anotacion"),
        lineas_workbook(b, "Re-anotacion"),
        f"- Exportadas (si no hay errores): `{SALIDA_ANOTACIONES_V2}`, {len(a.anotadas)} piezas de la primera anotacion.",
        "",
    ]
    if a.anotadas:
        lineas += ["## Primera anotacion por lote", ""] + lineas_lotes(a.anotadas, config)
        lineas += ["", "## Cobertura por columna (primera anotacion)", ""] + lineas_cobertura(a.anotadas)
        lineas += ["", "`Vacias`: sin anotar. Los estados van solos en la celda; `ausente` es una observacion y "
                       "`no_observable` y `desconocido` dicen que el atributo no se pudo observar o decidir. En las "
                       "correcciones, vacia significa «acepto el valor vigente»."]
    if b.anotadas:
        lineas += ["", "## Re-anotacion", ""] + lineas_lotes(b.anotadas, config, con_inicio=False)
    for validacion, nombre in ((a, "primera anotacion"), (b, "re-anotacion")):
        lineas += ["", f"## Avisos ({nombre})", ""]
        if validacion.avisos:
            lineas += tabla([[aviso, str(n)] for aviso, n in sorted(validacion.avisos.items())], ["Aviso", "Piezas"])
        else:
            lineas.append("Ninguno.")
    for validacion, nombre in ((a, "primera anotacion"), (b, "re-anotacion")):
        lineas += ["", f"## Errores ({nombre})", ""]
        lineas += [f"- {error}" for error in validacion.errores] if validacion.errores else ["Ninguno."]
    return lineas


# --------------------------------------------------------------------------- principal


def aplicar(raiz: Path) -> int:
    config = leer_config_anotacion(raiz)
    datos = config["acuerdo"]
    hojas = list(datos["hojas"])
    vocabulario = leer_vocabulario(raiz)
    a = validar_workbook(raiz, datos["anotador_a"], hojas, vocabulario)
    if not a.existe:
        print(f"No existe {datos['anotador_a']}; no hay anotaciones v2 que validar.")
        return 0
    b = validar_workbook(raiz, datos["anotador_b"], hojas, vocabulario)

    escribir_texto(raiz / REPORTE_V2, lineas_reporte(a, b, config))
    errores = a.errores + [f"(re-anotacion) {error}" for error in b.errores]
    if errores:
        print(f"Anotacion v2 con {len(errores)} errores; no se actualizo {SALIDA_ANOTACIONES_V2}. Ver {REPORTE_V2}.")
        for error in errores[:20]:
            print(f"- {error}")
        return 1
    escribir_csv(raiz / SALIDA_ANOTACIONES_V2, COLUMNAS_ANOTACIONES_V2, a.anotadas)
    print(f"Anotaciones v2 validas: {len(a.anotadas)} de {a.piezas} piezas -> {SALIDA_ANOTACIONES_V2}")
    print(f"Re-anotacion: {len(b.anotadas)} anotadas | avisos: {sum(a.avisos.values())} y {sum(b.avisos.values())}")
    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Valida los workbooks de anotacion v2 y exporta la primera anotacion.")
    parser.add_argument("--root", default=".", help="Raiz del repositorio.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    return aplicar(Path(parse_args(argv).root).resolve())


if __name__ == "__main__":
    raise SystemExit(main())
