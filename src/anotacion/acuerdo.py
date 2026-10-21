"""Acuerdo entre dos anotaciones del mismo conjunto de piezas (anotación v2).

Uso desde la raiz del repositorio (fuera del flujo: depende de que haya dos anotaciones):

    python -m src.anotacion.acuerdo
    python -m src.anotacion.acuerdo --a otro.xlsx --b otro2.xlsx
    python -m src.anotacion.acuerdo --a libro.xlsx --hoja-a anotador1 --b libro.xlsx --hoja-b anotador2

Por defecto compara los workbooks de [acuerdo] en config/anotacion.toml (el del primer
anotador y la copia del segundo). Las piezas se emparejan por id_global y solo se comparan
las anotadas en los dos (al menos una de las 17 columnas de anotación con valor). Dentro de
cada atributo, una pieza que alguno dejó vacía (regla de los treinta segundos) o con un valor
fuera del vocabulario queda fuera de ese atributo y se cuenta.

Medidas por tipo de atributo ([acuerdo.campos]):

- nominales: kappa de Cohen;
- ordinales: kappa ponderado lineal con el orden de [acuerdo.orden];
- multiples: índice de Jaccard medio por pieza y kappa por etiqueta (presencia de cada código);
- presencia (borde, centro): kappa sobre sí/no, solo en las piezas que los dos marcaron
  observables; las que alguno marcó no_visible se cuentan aparte.

Las correcciones se comparan por su valor efectivo: la corrección, o el valor vigente que
muestra el workbook si la corrección está vacía. Un atributo con una sola categoría observada
en los dos anotadores deja kappa indefinido y se informa como «no estimable».

Salida: outputs/reports/anotacion_acuerdo_v2.md.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from src.anotacion.workbook import CAMPO_DE_COLUMNA
from src.consolidado.esquema import ATRIBUTOS_ANOTACION, CORRECCIONES
from src.utils.archivos import escribir_texto
from src.utils.config import CONFIG_ANOTACION, leer_config_anotacion
from src.utils.libros import leer_hoja
from src.utils.metricas import Acuerdo, jaccard, kappa_detalle, tabla
from src.utils.vocabulario import Campo, leer_vocabulario

SALIDA_REPORTE = "outputs/reports/anotacion_acuerdo_v2.md"
ANOTABLES = ATRIBUTOS_ANOTACION + list(CORRECCIONES)
OBSERVABLES = ("si", "no")
MEDIDA_MULTIPLES = "Jaccard medio y kappa por etiqueta"


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
    no_observables: int = 0  # borde y centro: alguno marco no_visible
    jaccard: float | None = None
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
    sin_valor = fuera = 0
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
        valores.append((par[0], par[1]))

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
        return Resultado(columna, MEDIDA_MULTIPLES, acuerdo, sin_valor, fuera,
                         jaccard=media, por_etiqueta=por_etiqueta)

    pares = [(x[0], y[0]) for x, y in valores]
    if tipo == "ordinales":
        orden = config["acuerdo"]["orden"][columna]
        return Resultado(columna, "kappa ponderado lineal", kappa_detalle(pares, orden, ponderado=True), sin_valor, fuera)
    if tipo == "presencia":
        observables = [(x, y) for x, y in pares if x in OBSERVABLES and y in OBSERVABLES]
        resultado = Resultado(columna, "kappa si/no (observables)", kappa_detalle(observables, list(OBSERVABLES)),
                              sin_valor, fuera)
        resultado.no_observables = len(pares) - len(observables)
        return resultado
    return Resultado(columna, "kappa de Cohen", kappa_detalle(pares), sin_valor, fuera)


def tipos_de_campo(config: dict[str, Any]) -> dict[str, str]:
    """Columna -> tipo de medida; las cuatro listas deben cubrir una vez las 17 columnas."""
    tipos = {columna: tipo for tipo, columnas in config["acuerdo"]["campos"].items() for columna in columnas}
    total = sum(len(columnas) for columnas in config["acuerdo"]["campos"].values())
    if sorted(tipos) != sorted(ANOTABLES) or total != len(ANOTABLES):
        raise ValueError(f"[acuerdo.campos] de {CONFIG_ANOTACION.as_posix()} debe cubrir una vez: {ANOTABLES}")
    return tipos


def medir(a: Anotador, b: Anotador, config: dict[str, Any], vocabulario: dict[str, Campo]):
    piezas = sorted(a.anotadas & b.anotadas)
    tipos = tipos_de_campo(config)
    orden = [campo for capa in config["capas"] for campo in capa["campos"]]
    invalidos: list[tuple[str, str, str, str]] = []
    resultados = [comparar_atributo(c, tipos[c], piezas, a, b, vocabulario, config, invalidos) for c in orden]
    return piezas, resultados, invalidos


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
                   invalidos: list[tuple[str, str, str, str]], config: dict[str, Any]) -> list[str]:
    umbral = float(config["acuerdo"]["umbral_kappa"])
    capa_de = {campo: capa["titulo"] for capa in config["capas"] for campo in capa["campos"]}
    lineas = [
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
    if not piezas:
        lineas += [
            "Todavia no hay piezas anotadas por los dos anotadores: ningun acuerdo es estimable. La tabla muestra los "
            "atributos que se mediran y con que medida.",
            "",
        ]
    lineas += ["## Acuerdo por atributo", ""]
    filas = []
    for r in resultados:
        excluidas = r.sin_valor + r.fuera_vocabulario + r.no_observables
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
        "`n`: piezas comparadas en el atributo. `Excluidas`: piezas anotadas por los dos que no entran en el atributo "
        "(detalle abajo). En los campos multiples, `Acuerdo observado` es el indice de Jaccard medio por pieza.",
        "",
        "## Piezas excluidas por atributo",
        "",
    ]
    lineas += tabla(
        [[f"`{r.atributo}`", str(r.sin_valor), str(r.fuera_vocabulario), str(r.no_observables)] for r in resultados],
        ["Atributo", "Vacio en alguno", "Fuera del vocabulario", "No observable (no_visible)"],
    )
    lineas += [
        "",
        "`Vacio en alguno`: incluye la regla de los treinta segundos. `No observable`: en `borde` y `centro`, piezas que "
        "alguno de los dos marco `no_visible`; el kappa se calcula solo sobre las que ambos marcaron `si` o `no`.",
        "",
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
    piezas, resultados, invalidos = medir(a, b, config, leer_vocabulario(raiz))
    escribir_texto(raiz / SALIDA_REPORTE, lineas_reporte(a, b, piezas, resultados, invalidos, config))
    print(f"Acuerdo entre anotadores: {len(piezas)} piezas anotadas por los dos")
    print(f"Informe: {raiz / SALIDA_REPORTE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
