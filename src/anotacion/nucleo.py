"""Muestra estratificada y reproducible del principal v2 para la anotación estructural.

Uso desde la raiz del repositorio (lo ejecuta el flujo):

    python -m src.anotacion.nucleo
    python -m src.anotacion.nucleo --semilla 123

Diseño (parámetros en config/anotacion.toml):

1. Cuota por fuente proporcional a su peso en el principal v2, repartida por mayores restos.
2. Dentro de cada fuente, estratos cruzados de cultura agrupada y banda de aptitud; la cuota
   de la fuente se reparte entre ellos, también por mayores restos y en proporción a las
   piezas disponibles. Si un estrato recibiera más piezas de las que tiene, el faltante se
   redistribuye entre los estratos de la misma fuente con piezas libres y el informe lo dice.
3. Dentro de cada estrato se eligen las piezas con menor SHA-256 de «semilla:id_global»: el
   resultado no depende de la versión de Python ni de numpy y cambia con la semilla.
4. Las piezas elegidas se reparten en turno entre los lotes, ordenadas por fuente, banda y
   cultura, de modo que cada lote replica la composición del núcleo; el orden dentro de cada
   lote se mezcla con la semilla. Si un lote supera el tope de concentración de una fuente,
   el núcleo falla en vez de entregarlo.

Salidas: data/metadata/nucleo_anotacion_v2.csv y outputs/reports/nucleo_anotacion_v2.md.
"""

from __future__ import annotations

import argparse
import hashlib
from collections import Counter
from collections.abc import Hashable
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from src.anotacion.corpus_v2 import SALIDA_PRINCIPAL_V2
from src.utils.archivos import escribir_csv, escribir_texto, leer_csv
from src.utils.config import CONFIG_ANOTACION, leer_config_anotacion
from src.utils.fuentes import FUENTES
from src.utils.metricas import tabla
from src.utils.texto import buscar_terminos, normalizar_texto

SALIDA_NUCLEO = "data/metadata/nucleo_anotacion_v2.csv"
SALIDA_REPORTE = "outputs/reports/nucleo_anotacion_v2.md"
COLUMNAS_NUCLEO = ["id_global", "fuente", "cultura_agrupada", "banda_sugerida", "referencia_sugerida", "lote", "orden"]

# Banda de los registros sin ficha de aptitud (corpus_v2 los conserva con la banda vacía).
SIN_BANDA = "sin_banda"
ORDEN_BANDAS = ["principal", "revisar", "secundario", "descartar", SIN_BANDA]


class ErrorNucleo(ValueError):
    """El diseño no se puede cumplir con el corpus y la configuración actuales."""


# --------------------------------------------------------------------------- cultura agrupada


@dataclass(frozen=True)
class Caso:
    valor: str
    grupo: str
    motivo: str


def leer_casos(config: dict[str, Any]) -> dict[str, Caso]:
    casos = [Caso(c["valor"], c["grupo"], c["motivo"]) for c in config["cultura"].get("casos", [])]
    return {normalizar_texto(caso.valor): caso for caso in casos}


def agrupar_cultura(cultura: str, config: dict[str, Any], casos: dict[str, Caso]) -> str:
    """Grupo de cultura de un registro; falla si el valor nombra varios grupos y no tiene caso declarado."""
    datos = config["cultura"]
    if not cultura.strip():
        return datos["sin_cultura"]
    caso = casos.get(normalizar_texto(cultura))
    if caso:
        return caso.grupo
    grupos = [g for g in datos["grupos"] if buscar_terminos(cultura, datos["terminos"][g])]
    if len(grupos) > 1:
        raise ErrorNucleo(
            f"La cultura {cultura!r} nombra varios grupos ({', '.join(grupos)}): declare su grupo en "
            f"[[cultura.casos]] de {CONFIG_ANOTACION.as_posix()}."
        )
    return grupos[0] if grupos else datos["otras"]


# --------------------------------------------------------------------------- cuotas


def mayores_restos(total: int, pesos: dict[Hashable, int]) -> dict[Hashable, int]:
    """Reparto de `total` en proporción a `pesos` por el método de mayores restos (Hamilton).

    Cada clave recibe la parte entera de su cuota exacta; las unidades que faltan van a los
    mayores restos. Los empates se resuelven por mayor peso y luego por el orden de las claves,
    de modo que el reparto no depende de la semilla.
    """
    suma = sum(pesos.values())
    if suma == 0:
        return {clave: 0 for clave in pesos}
    exactas = {clave: Fraction(total * peso, suma) for clave, peso in pesos.items()}
    cuotas = {clave: int(exacta) for clave, exacta in exactas.items()}
    orden = sorted(pesos, key=lambda c: (-(exactas[c] - cuotas[c]), -pesos[c], c))
    for clave in orden[: total - sum(cuotas.values())]:
        cuotas[clave] += 1
    return cuotas


def ajustar_a_disponibles(
    cuotas: dict[Hashable, int], disponibles: dict[Hashable, int]
) -> tuple[dict[Hashable, int], dict[Hashable, int]]:
    """Limita cada cuota a las piezas disponibles y redistribuye el faltante.

    El faltante va a los estratos con piezas libres, en proporción a esas piezas libres y por
    mayores restos, hasta agotarlo. Devuelve (asignadas, faltantes por estrato). Falla si el
    total pedido supera las piezas disponibles.
    """
    if sum(cuotas.values()) > sum(disponibles.values()):
        raise ErrorNucleo("La cuota pedida supera las piezas disponibles.")
    asignadas = {c: min(cuotas[c], disponibles[c]) for c in cuotas}
    faltantes = {c: cuotas[c] - asignadas[c] for c in cuotas}
    pendiente = sum(faltantes.values())
    while pendiente:
        libres = {c: disponibles[c] - asignadas[c] for c in cuotas if disponibles[c] > asignadas[c]}
        extra = mayores_restos(pendiente, libres)
        for clave, n in extra.items():
            asignadas[clave] += min(n, libres[clave])
        pendiente = sum(cuotas.values()) - sum(asignadas.values())
    return asignadas, faltantes


# --------------------------------------------------------------------------- muestra y lotes


def huella(semilla: int, etiqueta: str, id_global: str) -> str:
    return hashlib.sha256(f"{semilla}:{etiqueta}:{id_global}".encode("utf-8")).hexdigest()


@dataclass
class Estrato:
    fuente: str
    cultura: str
    banda: str
    disponibles: int
    cuota: int = 0
    asignadas: int = 0
    faltantes: int = 0


@dataclass
class Nucleo:
    filas: list[dict[str, str]]
    estratos: list[Estrato]
    cuotas_fuente: dict[str, int]
    disponibles_fuente: dict[str, int]
    casos_aplicados: list[tuple[Caso, int]]
    grupos_principal: Counter[str]
    semilla: int


def construir_nucleo(registros: list[dict[str, str]], config: dict[str, Any], semilla: int) -> Nucleo:
    parametros = config["nucleo"]
    tamano, tamano_lote = int(parametros["tamano"]), int(parametros["tamano_lote"])
    tope = float(parametros["tope_fuente_lote"])
    if tamano % tamano_lote:
        raise ErrorNucleo(f"tamano ({tamano}) debe ser multiplo de tamano_lote ({tamano_lote}).")
    if tamano > len(registros):
        raise ErrorNucleo(f"tamano ({tamano}) supera el principal v2 ({len(registros)}).")

    casos = leer_casos(config)
    uso_casos: Counter[str] = Counter()
    for fila in registros:
        fila["cultura_agrupada"] = agrupar_cultura(fila["cultura"], config, casos)
        fila["banda"] = fila["banda_sugerida"] or SIN_BANDA
        if normalizar_texto(fila["cultura"]) in casos:
            uso_casos[normalizar_texto(fila["cultura"])] += 1

    orden_cultura = {g: i for i, g in enumerate([*config["cultura"]["grupos"], config["cultura"]["otras"], config["cultura"]["sin_cultura"]])}
    orden_fuente = {c: i for i, c in enumerate(FUENTES)}

    def clave_estrato(fila: dict[str, str]) -> tuple[int, int, int]:
        return (orden_fuente[fila["fuente"]], orden_cultura[fila["cultura_agrupada"]], ORDEN_BANDAS.index(fila["banda"]))

    disponibles_fuente = {c: sum(f["fuente"] == c for f in registros) for c in FUENTES}
    cuotas_fuente = mayores_restos(tamano, disponibles_fuente)

    por_estrato: dict[tuple[int, int, int], list[dict[str, str]]] = {}
    for fila in registros:
        por_estrato.setdefault(clave_estrato(fila), []).append(fila)

    elegidas: list[dict[str, str]] = []
    estratos: list[Estrato] = []
    for fuente in FUENTES:
        propios = {clave: filas for clave, filas in por_estrato.items() if clave[0] == orden_fuente[fuente]}
        disponibles = {clave: len(filas) for clave, filas in propios.items()}
        cuotas = mayores_restos(cuotas_fuente[fuente], disponibles)
        asignadas, faltantes = ajustar_a_disponibles(cuotas, disponibles)
        for clave in sorted(propios):
            filas = sorted(propios[clave], key=lambda f: huella(semilla, "muestra", f["id_global"]))
            elegidas += filas[: asignadas[clave]]
            muestra = propios[clave][0]
            estratos.append(Estrato(fuente, muestra["cultura_agrupada"], muestra["banda"], disponibles[clave],
                                    cuotas[clave], asignadas[clave], faltantes[clave]))

    # Reparto en turno: cada lote recibe piezas de todas las fuentes, bandas y culturas.
    elegidas.sort(key=lambda f: (*clave_estrato(f), huella(semilla, "muestra", f["id_global"])))
    lotes = tamano // tamano_lote
    por_lote: dict[int, list[dict[str, str]]] = {lote: [] for lote in range(1, lotes + 1)}
    for posicion, fila in enumerate(elegidas):
        por_lote[posicion % lotes + 1].append(fila)

    salida: list[dict[str, str]] = []
    for lote, filas in por_lote.items():
        conteo = Counter(f["fuente"] for f in filas)
        fuente, n = conteo.most_common(1)[0]
        if n > tope * len(filas):
            raise ErrorNucleo(
                f"El lote {lote} tendria {n} de {len(filas)} piezas de {fuente} (tope {tope:.0%}). "
                f"Revise tope_fuente_lote o tamano_lote en {CONFIG_ANOTACION.as_posix()}."
            )
        filas.sort(key=lambda f: huella(semilla, "orden", f["id_global"]))
        for orden, fila in enumerate(filas, start=1):
            salida.append({
                "id_global": fila["id_global"],
                "fuente": fila["fuente"],
                "cultura_agrupada": fila["cultura_agrupada"],
                "banda_sugerida": fila["banda_sugerida"],
                "referencia_sugerida": fila["referencia_sugerida"],
                "lote": str(lote),
                "orden": str(orden),
            })

    aplicados = [(caso, uso_casos[clave]) for clave, caso in casos.items()]
    grupos = Counter(fila["cultura_agrupada"] for fila in registros)
    return Nucleo(salida, estratos, cuotas_fuente, disponibles_fuente, aplicados, grupos, semilla)


# --------------------------------------------------------------------------- informe


def lineas_reporte(nucleo: Nucleo, config: dict[str, Any]) -> list[str]:
    parametros = config["nucleo"]
    total = sum(nucleo.disponibles_fuente.values())
    lineas = [
        "# Nucleo de anotacion v2",
        "",
        f"Generado por `python -m src.flujo` (`src/anotacion/nucleo.py`) desde `{SALIDA_PRINCIPAL_V2}`. "
        f"Parametros en `{CONFIG_ANOTACION.as_posix()}`: semilla {nucleo.semilla}, {parametros['tamano']} piezas en lotes de "
        f"{parametros['tamano_lote']}, tope de una fuente por lote {float(parametros['tope_fuente_lote']):.0%}.",
        "",
        "## Cuota por fuente",
        "",
        "Proporcional al principal v2, repartida por mayores restos.",
        "",
    ]
    filas = []
    for fuente in FUENTES:
        exacta = Fraction(int(parametros["tamano"]) * nucleo.disponibles_fuente[fuente], total)
        filas.append([fuente, str(nucleo.disponibles_fuente[fuente]), f"{float(exacta):.2f}", str(nucleo.cuotas_fuente[fuente])])
    filas.append(["Total", str(total), f"{float(parametros['tamano']):.2f}", str(sum(nucleo.cuotas_fuente.values()))])
    lineas += tabla(filas, ["Fuente", "Disponibles", "Cuota exacta", "Cuota"])

    faltantes = sum(e.faltantes for e in nucleo.estratos)
    lineas += [
        "",
        "## Estratos",
        "",
        "Todas las piezas estan en el principal por decision del revisor; la banda es la sugerencia del puntaje de "
        "aptitud (`banda_sugerida`) y solo sirve para que el nucleo cubra imagenes de calidad distinta.",
        "",
        "Cultura agrupada por banda de aptitud dentro de cada fuente. `Cuota`: reparto por mayores restos de la cuota "
        "de la fuente en proporcion a las piezas disponibles; `Asignadas`: piezas elegidas tras redistribuir los "
        "faltantes; `Faltantes`: cuota que el estrato no pudo cubrir con sus piezas.",
        "",
    ]
    lineas += tabla(
        [[e.fuente, e.cultura, e.banda, str(e.disponibles), str(e.cuota), str(e.asignadas), str(e.faltantes)] for e in nucleo.estratos],
        ["Fuente", "Cultura agrupada", "Banda", "Disponibles", "Cuota", "Asignadas", "Faltantes"],
    )
    lineas.append("")
    if faltantes:
        lineas.append(f"Faltantes redistribuidos dentro de su fuente: {faltantes} pieza(s).")
    else:
        lineas.append(
            "Sin faltantes: con un reparto proporcional y un nucleo menor que el corpus, ninguna cuota puede superar "
            "las piezas de su estrato. La redistribucion queda como salvaguarda si cambia el diseno."
        )

    lineas += ["", "## Lotes", "", "Composicion por fuente:", ""]
    lotes = sorted({int(f["lote"]) for f in nucleo.filas})
    def conteo(campo: str, valor: str, lote: int) -> str:
        return str(sum(f[campo] == valor and int(f["lote"]) == lote for f in nucleo.filas))
    lineas += tabla(
        [[str(l)] + [conteo("fuente", c, l) for c in FUENTES] + [str(sum(int(f["lote"]) == l for f in nucleo.filas))] for l in lotes],
        ["Lote", *FUENTES, "Total"],
    )
    bandas = [b for b in ORDEN_BANDAS if any(f["banda_sugerida"] == b or (b == SIN_BANDA and not f["banda_sugerida"]) for f in nucleo.filas)]
    lineas += ["", "Composicion por banda de aptitud:", ""]
    lineas += tabla(
        [[str(l)] + [conteo("banda_sugerida", "" if b == SIN_BANDA else b, l) for b in bandas] for l in lotes],
        ["Lote", *bandas],
    )
    grupos = [*config["cultura"]["grupos"], config["cultura"]["otras"], config["cultura"]["sin_cultura"]]
    lineas += ["", "Composicion por cultura agrupada:", ""]
    lineas += tabla([[str(l)] + [conteo("cultura_agrupada", g, l) for g in grupos] for l in lotes], ["Lote", *grupos])

    lineas += [
        "",
        "## Cultura agrupada",
        "",
        "El campo `cultura` de la fuente se normaliza y se buscan los terminos de cada grupo como palabra completa.",
        "",
    ]
    terminos = config["cultura"]["terminos"]
    lineas += tabla(
        [[g, ", ".join(terminos.get(g, [])) or "-", str(nucleo.grupos_principal[g]),
          str(sum(f["cultura_agrupada"] == g for f in nucleo.filas))] for g in grupos],
        ["Grupo", "Terminos", "Principal v2", "Nucleo"],
    )
    lineas += ["", "Valores que nombran mas de un grupo, resueltos uno por uno por el revisor:", ""]
    lineas += tabla(
        [[caso.valor, caso.grupo, str(n), caso.motivo] for caso, n in nucleo.casos_aplicados],
        ["Valor de la fuente", "Grupo", "Registros", "Motivo"],
    )
    return lineas


# --------------------------------------------------------------------------- principal


def generar(raiz: Path, semilla: int | None = None) -> int:
    config = leer_config_anotacion(raiz)
    semilla = int(config["nucleo"]["semilla"]) if semilla is None else semilla
    registros = leer_csv(raiz / SALIDA_PRINCIPAL_V2)
    try:
        nucleo = construir_nucleo(registros, config, semilla)
    except ErrorNucleo as error:
        print(f"No se pudo construir el nucleo de anotacion: {error}")
        return 1
    escribir_csv(raiz / SALIDA_NUCLEO, COLUMNAS_NUCLEO, nucleo.filas)
    escribir_texto(raiz / SALIDA_REPORTE, lineas_reporte(nucleo, config))
    print(f"Nucleo de anotacion: {len(nucleo.filas)} piezas ({', '.join(f'{c} {n}' for c, n in nucleo.cuotas_fuente.items())}), semilla {semilla}")
    print(f"Salida: {raiz / SALIDA_NUCLEO}")
    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Genera el nucleo de anotacion v2 (muestra estratificada).")
    parser.add_argument("--root", default=".", help="Raiz del repositorio.")
    parser.add_argument("--semilla", type=int, default=None, help=f"Sobrescribe la semilla de {CONFIG_ANOTACION.as_posix()}.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    return generar(Path(args.root).resolve(), args.semilla)


if __name__ == "__main__":
    raise SystemExit(main())
