"""Acuerdo entre dos anotaciones del mismo conjunto de piezas (anotación v2).

Uso desde la raiz del repositorio (también lo corre el flujo, para que el informe siga al workbook):

    python -m src.anotacion.acuerdo
    python -m src.anotacion.acuerdo --a otro.xlsx --b otro2.xlsx
    python -m src.anotacion.acuerdo --a libro.xlsx --hoja-a anotador1 --b libro.xlsx --hoja-b anotador2

Por defecto compara los workbooks de [acuerdo] en config/anotacion.toml. Con modalidad
«intraanotador» (sin segundo anotador, desde el 2026-11-03) A es la primera anotación y B la
re-anotación ciega del mismo anotador ([reanotacion]); solo se comparan las piezas con al menos
intervalo_minimo_dias entre las dos fechas de anotación, y las demás se listan.

Las piezas se emparejan por id_global y solo se comparan las anotadas en los dos (al menos una
de las 19 columnas de anotación con valor). Dentro de cada atributo, una pieza que alguno dejó
vacía, con un valor fuera del vocabulario o con el estado no_observable o desconocido queda fuera
de ese atributo y se cuenta. El estado ausente es una observación y se compara como un valor.

Medidas por tipo de atributo ([acuerdo.campos]):

- nominales: kappa de Cohen;
- ordinales: kappa ponderado lineal con el orden de [acuerdo.orden];
- multiples: índice de Jaccard medio por pieza y kappa por etiqueta (presencia de cada código);
- presencia (borde, centro): kappa sobre sí/no, solo en las piezas que los dos marcaron
  observables; las que alguno marcó no_visible se cuentan aparte;
- secuencias (secuencia_bandas): coincidencia exacta y similitud de edición media
  (1 - distancia de Levenshtein / longitud de la palabra más larga).

Las correcciones se comparan por su valor efectivo: la corrección, o el valor vigente que
muestra el workbook si la corrección está vacía. Un atributo con una sola categoría observada
en los dos anotadores deja kappa indefinido y se informa como «no estimable».

Salida: outputs/reports/anotacion_acuerdo_v2.md.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

from src.anotacion.workbook import CAMPO_DE_COLUMNA
from src.consolidado.esquema import ATRIBUTOS_ANOTACION_V2, CORRECCIONES
from src.utils.archivos import escribir_texto
from src.utils.config import CONFIG_ANOTACION, leer_config_anotacion
from src.utils.libros import leer_hoja
from src.utils.metricas import Acuerdo, jaccard, kappa_detalle, similitud_edicion, tabla
from src.utils.vocabulario import SIN_OBSERVACION, Campo, leer_vocabulario

SALIDA_REPORTE = "outputs/reports/anotacion_acuerdo_v2.md"
ANOTABLES = ATRIBUTOS_ANOTACION_V2 + list(CORRECCIONES)
OBSERVABLES = ("si", "no")
MEDIDA_MULTIPLES = "Jaccard medio y kappa por etiqueta"
MEDIDA_SECUENCIAS = "similitud de edicion media"
INTRAANOTADOR = "intraanotador"


@dataclass
class Anotador:
    ruta: str
    hojas: list[str]
    existe: bool
    filas: dict[str, dict[str, str]] = field(default_factory=dict)

    @property
    def anotadas(self) -> set[str]:
        return {id_ for id_, fila in self.filas.items() if any(fila.get(c) for c in ANOTABLES)}


@dataclass
class Resultado:
    atributo: str
    medida: str
    acuerdo: Acuerdo
    sin_valor: int = 0  # alguno de los dos lo dejo vacio
    fuera_vocabulario: int = 0
    no_observables: int = 0  # alguno marco no_observable o desconocido (o no_visible en borde y centro)
    jaccard: float | None = None
    exactas: int = 0  # secuencias identicas
    por_etiqueta: list[tuple[str, Acuerdo]] = field(default_factory=list)


# --------------------------------------------------------------------------- lectura


def leer_anotador(raiz: Path, ruta: str, hojas: list[str]) -> Anotador:
    """Filas de las hojas indicadas por id_global; un id repetido entre hojas es un error."""
    absoluta = raiz / ruta
    anotador = Anotador(ruta, hojas, absoluta.exists())
    if not anotador.existe:
        return anotador
    for hoja in hojas:
        try:
            filas = leer_hoja(absoluta, hoja, clave="id_global")
        except ValueError:
            continue  # una hoja ausente no tiene piezas
        for fila in filas:
            if fila["id_global"] in anotador.filas:
                raise ValueError(f"{ruta}: {fila['id_global']} aparece en mas de una hoja")
            anotador.filas[fila["id_global"]] = fila
    return anotador


def valor_efectivo(fila: dict[str, str], columna: str) -> str:
    """La corrección, o el valor vigente del workbook si la corrección está vacía."""
    if columna in CORRECCIONES:
        return fila.get(columna, "") or fila.get(CORRECCIONES[columna], "")
    return fila.get(columna, "")


def codigos(valor: str, campo: Campo) -> list[str] | None:
    """Códigos del valor (las etiquetas de la tesis se recodifican); None si alguno no es del vocabulario."""
    recodificado = campo.recodificar(valor)
    if campo.invalidos(recodificado):
        return None
    return campo.separar(recodificado)


# --------------------------------------------------------------------------- medidas


def comparar_atributo(
    columna: str,
    tipo: str,
    piezas: list[str],
    a: Anotador,
    b: Anotador,
    vocabulario: dict[str, Campo],
    config: dict[str, Any],
    invalidos: list[tuple[str, str, str, str]],
) -> Resultado:
    campo = vocabulario[CAMPO_DE_COLUMNA[columna]]
    sin_valor = fuera = sin_observacion = 0
    valores: list[tuple[list[str], list[str]]] = []
    for id_global in piezas:
        crudos = valor_efectivo(a.filas[id_global], columna), valor_efectivo(b.filas[id_global], columna)
        if not all(crudos):
            sin_valor += 1
            continue
        par = [codigos(crudo, campo) for crudo in crudos]
        if None in par:
            fuera += 1
            for nombre, crudo, cod in zip(("A", "B"), crudos, par):
                if cod is None:
                    invalidos.append((id_global, columna, nombre, crudo))
            continue
        if any(cod == [estado] for cod in par for estado in SIN_OBSERVACION):
            sin_observacion += 1
            continue
        valores.append((par[0], par[1]))

    if tipo == "secuencias":
        similitudes = [similitud_edicion(x, y) for x, y in valores]
        media = sum(similitudes) / len(similitudes) if similitudes else None
        acuerdo = Acuerdo(len(valores), media, None, None, "" if valores else "sin piezas comparables")
        return Resultado(columna, MEDIDA_SECUENCIAS, acuerdo, sin_valor, fuera, sin_observacion,
                         exactas=sum(x == y for x, y in valores))

    if tipo == "multiples":
        conjuntos = [(set(x), set(y)) for x, y in valores]
        etiquetas = [c for c in campo.codigos if any(c in x | y for x, y in conjuntos)]
        por_etiqueta = [
            (etiqueta, kappa_detalle([("si" if etiqueta in x else "no", "si" if etiqueta in y else "no") for x, y in conjuntos],
                                     ["no", "si"]))
            for etiqueta in etiquetas
        ]
        media = sum(jaccard(x, y) for x, y in conjuntos) / len(conjuntos) if conjuntos else None
        acuerdo = Acuerdo(len(conjuntos), media, None, None, "" if conjuntos else "sin piezas comparables")
        return Resultado(columna, MEDIDA_MULTIPLES, acuerdo, sin_valor, fuera, sin_observacion,
                         jaccard=media, por_etiqueta=por_etiqueta)

    pares = [(x[0], y[0]) for x, y in valores]
    if tipo == "ordinales":
        orden = config["acuerdo"]["orden"][columna]
        return Resultado(columna, "kappa ponderado lineal", kappa_detalle(pares, orden, ponderado=True), sin_valor, fuera,
                         sin_observacion)
    if tipo == "presencia":
        observables = [(x, y) for x, y in pares if x in OBSERVABLES and y in OBSERVABLES]
        resultado = Resultado(columna, "kappa si/no (observables)", kappa_detalle(observables, list(OBSERVABLES)),
                              sin_valor, fuera, sin_observacion)
        resultado.no_observables += len(pares) - len(observables)
        return resultado
    return Resultado(columna, "kappa de Cohen", kappa_detalle(pares), sin_valor, fuera, sin_observacion)


def tipos_de_campo(config: dict[str, Any]) -> dict[str, str]:
    """Columna -> tipo de medida; las listas deben cubrir una vez las 19 columnas."""
    tipos = {columna: tipo for tipo, columnas in config["acuerdo"]["campos"].items() for columna in columnas}
    total = sum(len(columnas) for columnas in config["acuerdo"]["campos"].values())
    if sorted(tipos) != sorted(ANOTABLES) or total != len(ANOTABLES):
        raise ValueError(f"[acuerdo.campos] de {CONFIG_ANOTACION.as_posix()} debe cubrir una vez: {ANOTABLES}")
    return tipos


def fecha(texto: str) -> date | None:
    try:
        return date.fromisoformat(texto)
    except ValueError:
        return None


def separar_por_intervalo(
    piezas: list[str], a: Anotador, b: Anotador, config: dict[str, Any]
) -> tuple[list[str], list[tuple[str, str]]]:
    """Intra-anotador: piezas con al menos intervalo_minimo_dias entre las dos fechas; las demas, con su motivo."""
    if config["acuerdo"].get("modalidad") != INTRAANOTADOR:
        return piezas, []
    minimo = int(config["reanotacion"]["intervalo_minimo_dias"])
    validas, excluidas = [], []
    for id_global in piezas:
        primera, segunda = fecha(a.filas[id_global].get("fecha_anotacion", "")), fecha(b.filas[id_global].get("fecha_anotacion", ""))
        if primera is None or segunda is None:
            excluidas.append((id_global, "fecha_anotacion vacia o invalida"))
        elif (segunda - primera).days < minimo:
            excluidas.append((id_global, f"{(segunda - primera).days} dias entre anotaciones (minimo {minimo})"))
        else:
            validas.append(id_global)
    return validas, excluidas


def medir(a: Anotador, b: Anotador, config: dict[str, Any], vocabulario: dict[str, Campo]):
    piezas, fuera_de_plazo = separar_por_intervalo(sorted(a.anotadas & b.anotadas), a, b, config)
    tipos = tipos_de_campo(config)
    orden = [campo for capa in config["capas"] for campo in capa["campos"]]
    invalidos: list[tuple[str, str, str, str]] = []
    resultados = [comparar_atributo(c, tipos[c], piezas, a, b, vocabulario, config, invalidos) for c in orden]
    return piezas, resultados, invalidos, fuera_de_plazo


# --------------------------------------------------------------------------- informe


def numero(valor: float | None) -> str:
    return "" if valor is None else f"{valor:.3f}"


def alcanza(acuerdo: Acuerdo, umbral: float) -> str:
    if acuerdo.kappa is None:
        return f"no estimable: {acuerdo.motivo}"
    return "si" if acuerdo.kappa >= umbral else "no"


def describir(anotador: Anotador, nombre: str) -> str:
    if not anotador.existe:
        return f"- Anotador {nombre}: `{anotador.ruta}` no existe todavia."
    return (f"- Anotador {nombre}: `{anotador.ruta}` (hojas {', '.join(anotador.hojas)}): {len(anotador.filas)} piezas, "
            f"{len(anotador.anotadas)} anotadas.")


def lineas_reporte(a: Anotador, b: Anotador, piezas: list[str], resultados: list[Resultado],
                   invalidos: list[tuple[str, str, str, str]], config: dict[str, Any],
                   fuera_de_plazo: list[tuple[str, str]] | None = None) -> list[str]:
    fuera_de_plazo = fuera_de_plazo or []
    umbral = float(config["acuerdo"]["umbral_kappa"])
    capa_de = {campo: capa["titulo"] for capa in config["capas"] for campo in capa["campos"]}
    intra = config["acuerdo"].get("modalidad") == INTRAANOTADOR
    if intra:
        reanotacion = config["reanotacion"]
        encabezado = [
            "# Acuerdo intra-anotador (anotacion v2, test-retest)",
            "",
            f"Generado por `python -m src.anotacion.acuerdo` (`src/anotacion/acuerdo.py`); parametros en "
            f"`{CONFIG_ANOTACION.as_posix()}` ([acuerdo] y [reanotacion]). Umbral de acuerdo aceptable: kappa >= {umbral}.",
            "",
            "Sin segundo anotador (plan de cierre, D1), el mismo anotador re-anota a ciegas el lote "
            f"{reanotacion['lote']}, en otro orden y al menos {reanotacion['intervalo_minimo_dias']} dias despues. "
            "Mide la estabilidad de la anotacion, no su acuerdo con otra persona: es una limitacion del estudio.",
            "",
            describir(a, "A (primera anotacion)"),
            describir(b, "B (re-anotacion)"),
            f"- Piezas anotadas en las dos (emparejadas por `id_global`) con el intervalo minimo: {len(piezas)}; "
            f"fuera de plazo: {len(fuera_de_plazo)}.",
            "",
        ]
    else:
        encabezado = [
            "# Acuerdo entre anotadores (anotacion v2)",
            "",
            f"Generado por `python -m src.anotacion.acuerdo` (`src/anotacion/acuerdo.py`); parametros en "
            f"`{CONFIG_ANOTACION.as_posix()}` ([acuerdo]). Umbral de acuerdo aceptable: kappa >= {umbral}.",
            "",
            describir(a, "A"),
            describir(b, "B"),
            f"- Piezas anotadas por los dos (emparejadas por `id_global`): {len(piezas)}.",
            "",
        ]
    lineas = encabezado
    if not piezas:
        lineas += [
            "Todavia no hay piezas anotadas en las dos anotaciones: ningun acuerdo es estimable. La tabla muestra los "
            "atributos que se mediran y con que medida.",
            "",
        ]
    lineas += ["## Acuerdo por atributo", ""]
    filas = []
    for r in resultados:
        excluidas = r.sin_valor + r.fuera_vocabulario + r.no_observables
        if r.medida == MEDIDA_SECUENCIAS:
            filas.append([capa_de[r.atributo], f"`{r.atributo}`", r.medida, str(r.acuerdo.n), str(excluidas),
                          numero(r.acuerdo.observado), "", "", f"coincidencia exacta: {r.exactas} de {r.acuerdo.n}"
                          if r.acuerdo.n else f"no estimable: {r.acuerdo.motivo}"])
            continue
        if r.medida == MEDIDA_MULTIPLES:
            filas.append([capa_de[r.atributo], f"`{r.atributo}`", r.medida, str(r.acuerdo.n), str(excluidas),
                          numero(r.jaccard), "", "", "ver kappa por etiqueta" if r.jaccard is not None else
                          f"no estimable: {r.acuerdo.motivo}"])
            continue
        filas.append([capa_de[r.atributo], f"`{r.atributo}`", r.medida, str(r.acuerdo.n), str(excluidas),
                      numero(r.acuerdo.observado), numero(r.acuerdo.esperado), numero(r.acuerdo.kappa),
                      alcanza(r.acuerdo, umbral)])
    lineas += tabla(filas, ["Capa", "Atributo", "Medida", "n", "Excluidas", "Acuerdo observado", "Acuerdo esperado",
                            "Kappa", f"Alcanza {umbral}"])
    lineas += [
        "",
        "`n`: piezas comparadas en el atributo. `Excluidas`: piezas anotadas en las dos que no entran en el atributo "
        "(detalle abajo). En los campos multiples, `Acuerdo observado` es el indice de Jaccard medio por pieza; en las "
        "secuencias, la similitud de edicion media (1 - distancia de Levenshtein / longitud de la palabra mas larga).",
        "",
        "## Piezas excluidas por atributo",
        "",
    ]
    lineas += tabla(
        [[f"`{r.atributo}`", str(r.sin_valor), str(r.fuera_vocabulario), str(r.no_observables)] for r in resultados],
        ["Atributo", "Vacio en alguno", "Fuera del vocabulario", "No observable o desconocido"],
    )
    lineas += [
        "",
        "`Vacio en alguno`: celda sin anotar en alguna de las dos. `No observable o desconocido`: alguna de las dos "
        "registro el estado `no_observable` o `desconocido` (regla de los treinta segundos) o, en `borde` y `centro`, "
        "`no_visible`; el estado `ausente` es una observacion y se compara como un valor mas.",
        "",
    ]
    if intra:
        lineas += ["## Piezas fuera de plazo", "",
                   "Anotadas en las dos, pero sin el intervalo minimo entre fechas: no entran en ningun atributo.", ""]
        if fuera_de_plazo:
            lineas += tabla([[id_, motivo] for id_, motivo in fuera_de_plazo], ["Pieza", "Motivo"])
        else:
            lineas.append("Ninguna.")
        lineas.append("")
    lineas += [
        "## Kappa por etiqueta (campos multiples)",
        "",
        "Presencia o ausencia de cada codigo en las piezas comparadas: muestra que etiqueta arrastra el desacuerdo.",
        "",
    ]
    filas = [
        [f"`{r.atributo}`", etiqueta, str(ac.n), numero(ac.observado), numero(ac.esperado), numero(ac.kappa), alcanza(ac, umbral)]
        for r in resultados for etiqueta, ac in r.por_etiqueta
    ]
    if filas:
        lineas += tabla(filas, ["Atributo", "Etiqueta", "n", "Acuerdo observado", "Acuerdo esperado", "Kappa", f"Alcanza {umbral}"])
    else:
        lineas.append("Sin piezas comparables.")
    lineas += ["", "## Valores fuera del vocabulario", ""]
    if invalidos:
        lineas += tabla([[id_, f"`{col}`", quien, valor] for id_, col, quien, valor in invalidos],
                        ["Pieza", "Columna", "Anotador", "Valor"])
    else:
        lineas.append("Ninguno.")
    lineas += [
        "",
        "## Como se mide",
        "",
        "- Kappa de Cohen: (acuerdo observado - acuerdo esperado al azar) / (1 - acuerdo esperado). En los ordinales "
        "(`contraste`, `densidad_visual`, `repeticion`) un desacuerdo entre categorias vecinas cuenta como acuerdo "
        "parcial (pesos lineales), con el orden de [acuerdo.orden].",
        "- Secuencias (`secuencia_bandas`): las dos palabras de bandas se comparan en el orden del eje de lectura. Se "
        "informa cuantas coinciden exactamente y la similitud media 1 - d / max(l1, l2), con d la distancia de "
        "Levenshtein: una banda de mas, de menos o distinta resta lo mismo. No hay acuerdo esperado al azar definido, "
        "asi que no se calcula kappa.",
        "- Las correcciones se comparan por su valor efectivo: la correccion o, si esta vacia, el valor vigente del "
        "workbook. Dos correcciones vacias son acuerdo con el valor vigente.",
        "- Si los dos anotadores usan una sola categoria, el acuerdo esperado es 1 y kappa no esta definido: se informa "
        "como no estimable, nunca como 1 ni como 0.",
        "- Escala de referencia (Landis y Koch, 1977): 0,41-0,60 moderado, 0,61-0,80 sustancial, mas de 0,80 casi perfecto.",
    ]
    return lineas


# --------------------------------------------------------------------------- principal


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Mide el acuerdo entre dos anotaciones (anotacion v2).")
    parser.add_argument("--root", default=".", help="Raiz del repositorio.")
    parser.add_argument("--a", default=None, help="Workbook del anotador A (por defecto, [acuerdo] anotador_a).")
    parser.add_argument("--b", default=None, help="Workbook del anotador B (por defecto, [acuerdo] anotador_b).")
    parser.add_argument("--hoja-a", default=None, help="Hoja unica del anotador A (por defecto, [acuerdo] hojas).")
    parser.add_argument("--hoja-b", default=None, help="Hoja unica del anotador B (por defecto, [acuerdo] hojas).")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    raiz = Path(args.root).resolve()
    config = leer_config_anotacion(raiz)
    datos = config["acuerdo"]
    a = leer_anotador(raiz, args.a or datos["anotador_a"], [args.hoja_a] if args.hoja_a else list(datos["hojas"]))
    b = leer_anotador(raiz, args.b or datos["anotador_b"], [args.hoja_b] if args.hoja_b else list(datos["hojas"]))
    piezas, resultados, invalidos, fuera_de_plazo = medir(a, b, config, leer_vocabulario(raiz))
    escribir_texto(raiz / SALIDA_REPORTE, lineas_reporte(a, b, piezas, resultados, invalidos, config, fuera_de_plazo))
    print(f"Acuerdo: {len(piezas)} piezas comparadas, {len(fuera_de_plazo)} fuera de plazo")
    print(f"Informe: {raiz / SALIDA_REPORTE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
