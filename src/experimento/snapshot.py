"""Snapshot experimental v2: particiones por grupo y sorteo de consultas T3 (protocolo, sección 5).

Uso desde la raíz del repositorio:

    python -m src.experimento.snapshot --crear        # una vez: fija particiones y consultas
    python -m src.experimento.snapshot --reemplazar   # regla de reemplazo de consultas
    python -m src.experimento.snapshot                # validación (paso del flujo)

--crear reparte en desarrollo y prueba los grupos (data/metadata/grupos_v2.csv) que tienen alguna
pieza de la galería (el núcleo de anotación), estratificados por museo, y sortea las consultas T3:
a lo sumo una por grupo, entre las piezas con composición observable, con cuotas por museo y
composición. Escribe dos insumos congelados, que no sobrescribe sin --forzar:

- data/metadata/particiones_v2.csv: cada pieza de la galería con su grupo y su partición.
- data/metadata/consultas_t3_v2.csv: cada consulta con su pieza, su partición y su estrato.

--reemplazar cambia solo las consultas que dejaron de ser elegibles (composición no observable
tras corregir la anotación) por la siguiente pieza elegible de su estrato original, en el orden de
la semilla, y deja las demás como están.

Sin opciones, comprueba que no haya fugas (ningún grupo en dos particiones, cada consulta en la
partición de su pieza, una consulta por grupo, consultas elegibles y en el número de
config/experimento.toml) y escribe outputs/reports/experimento_v2_snapshot.md, solo con conteos.
Cualquier fuga detiene el flujo. Sin snapshot creado, no hace nada.

consultas_t3_v2.csv registra el estrato (museo y composición) de cada consulta: hasta cerrar la
re-anotación del lote 1 no se abre, igual que data/metadata/anotaciones_v2.csv.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Any

from src.anotacion.aplicar_anotaciones_v2 import SALIDA_ANOTACIONES_V2
from src.anotacion.nucleo import SALIDA_NUCLEO, huella, mayores_restos
from src.grupos.grupos import SALIDA_GRUPOS
from src.utils.archivos import escribir_csv, escribir_texto, indexar, leer_csv
from src.utils.config import CONFIG_EXPERIMENTO, leer_config_experimento
from src.utils.metricas import tabla

SALIDA_PARTICIONES = "data/metadata/particiones_v2.csv"
SALIDA_CONSULTAS = "data/metadata/consultas_t3_v2.csv"
REPORTE_SNAPSHOT = "outputs/reports/experimento_v2_snapshot.md"
COLUMNAS_PARTICIONES = ["id_global", "fuente", "grupo", "particion"]
COLUMNAS_CONSULTAS = ["consulta", "id_global", "grupo", "particion", "estrato"]
PARTICIONES = ("desarrollo", "prueba")
PREFIJO = {"desarrollo": "T3-D", "prueba": "T3-P"}


# --------------------------------------------------------------------------- datos


def galeria(raiz: Path) -> tuple[list[str], dict[str, str], dict[str, str]]:
    """Piezas del núcleo, su grupo (clave estable: el menor id_global del grupo) y su museo."""
    nucleo = [f["id_global"] for f in leer_csv(raiz / SALIDA_NUCLEO)]
    filas = leer_csv(raiz / SALIDA_GRUPOS)
    miembros: dict[str, list[str]] = defaultdict(list)
    for fila in filas:
        miembros[fila["grupo"]].append(fila["id_global"])
    clave = {id_: min(ids) for ids in miembros.values() for id_ in ids}
    fuente = {f["id_global"]: f["fuente"] for f in filas}
    return nucleo, clave, fuente


def composiciones(raiz: Path) -> dict[str, str]:
    return {f["id_global"]: f["composicion"] for f in leer_csv(raiz / SALIDA_ANOTACIONES_V2)}


def elegible(composicion: str, config: dict[str, Any]) -> bool:
    return bool(composicion) and composicion not in config["consultas_t3"]["excluir_composicion"]


# --------------------------------------------------------------------------- creacion


def repartir(nucleo: list[str], clave: dict[str, str], fuente: dict[str, str], config: dict[str, Any]) -> dict[str, str]:
    """Partición de cada grupo de la galería: cuota de desarrollo por museo y orden por la semilla."""
    semilla = int(config["particiones"]["semilla"])
    grupos = sorted({clave[id_] for id_ in nucleo})
    por_museo: dict[str, list[str]] = defaultdict(list)
    for grupo in grupos:
        por_museo[fuente[grupo]].append(grupo)
    total = round(Fraction(str(config["particiones"]["proporcion_desarrollo"])) * len(grupos))
    cuotas = mayores_restos(int(total), {museo: len(g) for museo, g in por_museo.items()})
    particion = {}
    for museo, lista in por_museo.items():
        orden = sorted(lista, key=lambda g: huella(semilla, "particion", g))
        for posicion, grupo in enumerate(orden):
            particion[grupo] = "desarrollo" if posicion < cuotas[museo] else "prueba"
    return particion


def orden_estrato(candidatas: list[str], semilla: int) -> list[str]:
    return sorted(candidatas, key=lambda id_: huella(semilla, "consulta", id_))


def candidatas_por_estrato(nucleo: list[str], clave: dict[str, str], fuente: dict[str, str], composicion: dict[str, str],
                           particion: dict[str, str], config: dict[str, Any]) -> dict[tuple[str, str, str], list[str]]:
    """(partición, museo, composición) -> piezas elegibles, una por grupo (la primera según la semilla)."""
    semilla = int(config["consultas_t3"]["semilla"])
    por_grupo: dict[str, list[str]] = defaultdict(list)
    for id_ in nucleo:
        if elegible(composicion.get(id_, ""), config):
            por_grupo[clave[id_]].append(id_)
    estratos: dict[tuple[str, str, str], list[str]] = defaultdict(list)
    for grupo, ids in por_grupo.items():
        elegida = orden_estrato(ids, semilla)[0]
        estratos[(particion[grupo], fuente[elegida], composicion[elegida])].append(elegida)
    return {e: orden_estrato(ids, semilla) for e, ids in estratos.items()}


def sortear(estratos: dict[tuple[str, str, str], list[str]], clave: dict[str, str], config: dict[str, Any]) -> list[dict[str, str]]:
    consultas = []
    for nombre in PARTICIONES:
        propios = {(m, c): ids for (p, m, c), ids in estratos.items() if p == nombre}
        cuotas = mayores_restos(int(config["consultas_t3"][nombre]), {e: len(ids) for e, ids in propios.items()})
        elegidas = [(e, id_) for e in sorted(propios) for id_ in propios[e][:cuotas[e]]]
        for numero, ((museo, comp), id_) in enumerate(sorted(elegidas, key=lambda x: x[1]), start=1):
            consultas.append({"consulta": f"{PREFIJO[nombre]}{numero:02d}", "id_global": id_, "grupo": clave[id_],
                              "particion": nombre, "estrato": f"{museo} | {comp}"})
    return consultas


def crear(raiz: Path, forzar: bool) -> int:
    existentes = [r for r in (SALIDA_PARTICIONES, SALIDA_CONSULTAS) if (raiz / r).exists()]
    if existentes and not forzar:
        print(f"Ya existen {', '.join(existentes)}: el snapshot esta congelado. Use --forzar solo con permiso del revisor.")
        return 1
    config = leer_config_experimento(raiz)
    nucleo, clave, fuente = galeria(raiz)
    particion = repartir(nucleo, clave, fuente, config)
    escribir_csv(raiz / SALIDA_PARTICIONES, COLUMNAS_PARTICIONES, [
        {"id_global": id_, "fuente": fuente[id_], "grupo": clave[id_], "particion": particion[clave[id_]]} for id_ in nucleo
    ])
    estratos = candidatas_por_estrato(nucleo, clave, fuente, composiciones(raiz), particion, config)
    escribir_csv(raiz / SALIDA_CONSULTAS, COLUMNAS_CONSULTAS, sortear(estratos, clave, config))
    print(f"Snapshot creado: {SALIDA_PARTICIONES} y {SALIDA_CONSULTAS}")
    return validar(raiz)


def reemplazar(raiz: Path) -> int:
    """Cambia las consultas no elegibles por la siguiente elegible de su estrato original."""
    config = leer_config_experimento(raiz)
    semilla = int(config["consultas_t3"]["semilla"])
    nucleo, clave, fuente = galeria(raiz)
    particion = {f["grupo"]: f["particion"] for f in leer_csv(raiz / SALIDA_PARTICIONES)}
    composicion = composiciones(raiz)
    consultas = leer_csv(raiz / SALIDA_CONSULTAS)
    usados = {c["grupo"] for c in consultas}
    cambios = 0
    for consulta in consultas:
        if elegible(composicion.get(consulta["id_global"], ""), config):
            continue
        museo, _, comp = consulta["estrato"].partition(" | ")
        candidatas = [id_ for id_ in nucleo if fuente[id_] == museo and composicion.get(id_) == comp
                      and particion[clave[id_]] == consulta["particion"] and clave[id_] not in usados]
        if not candidatas:
            print(f"{consulta['consulta']}: su estrato no tiene otra pieza elegible; decide el revisor.")
            return 1
        nueva = orden_estrato(candidatas, semilla)[0]
        usados.discard(consulta["grupo"])
        usados.add(clave[nueva])
        consulta.update({"id_global": nueva, "grupo": clave[nueva]})
        cambios += 1
    escribir_csv(raiz / SALIDA_CONSULTAS, COLUMNAS_CONSULTAS, consultas)
    print(f"Consultas reemplazadas: {cambios}")
    return validar(raiz)


# --------------------------------------------------------------------------- validacion


def comprobar(raiz: Path, config: dict[str, Any]) -> tuple[list[str], dict[str, Any]]:
    nucleo, clave, fuente = galeria(raiz)
    particiones = leer_csv(raiz / SALIDA_PARTICIONES)
    consultas = leer_csv(raiz / SALIDA_CONSULTAS)
    composicion = composiciones(raiz)
    errores = []
    asignada = {f["id_global"]: f["particion"] for f in particiones}
    if sorted(asignada) != sorted(nucleo) or len(asignada) != len(particiones):
        errores.append("particiones_v2.csv no tiene exactamente una fila por pieza del nucleo")
    if any(p not in PARTICIONES for p in asignada.values()):
        errores.append("particiones_v2.csv tiene particiones que no son desarrollo ni prueba")
    por_grupo: dict[str, set[str]] = defaultdict(set)
    for id_, p in asignada.items():
        if id_ in clave:
            por_grupo[clave[id_]].add(p)
    divididos = [g for g, ps in por_grupo.items() if len(ps) > 1]
    if divididos:
        errores.append(f"{len(divididos)} grupos repartidos entre desarrollo y prueba (fuga): {sorted(divididos)[:10]}")
    for nombre in PARTICIONES:
        n = sum(c["particion"] == nombre for c in consultas)
        if n != int(config["consultas_t3"][nombre]):
            errores.append(f"{n} consultas de {nombre}; config/experimento.toml pide {config['consultas_t3'][nombre]}")
    for c in consultas:
        if c["id_global"] not in asignada:
            errores.append(f"{c['consulta']}: la pieza no esta en la galeria")
        elif asignada[c["id_global"]] != c["particion"]:
            errores.append(f"{c['consulta']}: su pieza esta en {asignada[c['id_global']]}, no en {c['particion']}")
        if not elegible(composicion.get(c["id_global"], ""), config):
            errores.append(f"{c['consulta']}: la pieza ya no tiene composicion observable (use --reemplazar)")
    repetidos = [g for g, n in Counter(clave.get(c["id_global"], "") for c in consultas).items() if n > 1]
    if repetidos:
        errores.append(f"{len(repetidos)} grupos con mas de una consulta")
    resumen = {"particiones": particiones, "consultas": consultas, "clave": clave, "fuente": fuente,
               "composicion": composicion}
    return errores, resumen


def lineas_reporte(errores: list[str], r: dict[str, Any], config: dict[str, Any]) -> list[str]:
    grupos = {(f["grupo"], f["particion"]) for f in r["particiones"]}
    filas = []
    for museo in sorted({f["fuente"] for f in r["particiones"]}):
        fila = [museo]
        for nombre in PARTICIONES:
            piezas = sum(f["fuente"] == museo and f["particion"] == nombre for f in r["particiones"])
            n_grupos = len({g for g, p in grupos if p == nombre and r["fuente"][g] == museo})
            consultas = sum(c["particion"] == nombre and r["fuente"][c["id_global"]] == museo for c in r["consultas"])
            fila += [str(piezas), str(n_grupos), str(consultas)]
        filas.append(fila)
    composicion = Counter(r["composicion"].get(c["id_global"], "") for c in r["consultas"])
    lineas = [
        "# Snapshot experimental v2: particiones y consultas T3",
        "",
        "Generado por `python -m src.experimento.snapshot` (`src/experimento/snapshot.py`), paso del flujo. Parametros "
        f"en `{CONFIG_EXPERIMENTO.as_posix()}`; protocolo en `docs/protocolo_experimental_v2.md` (seccion 5). Los "
        f"insumos congelados son `{SALIDA_PARTICIONES}` y `{SALIDA_CONSULTAS}`.",
        "",
        "Solo conteos: la galeria se juzga a ciegas y el lote 1 se re-anota a ciegas.",
        "",
        f"- Galeria: {len(r['particiones'])} piezas del nucleo en {len({g for g, _ in grupos})} grupos.",
        f"- Proporcion de desarrollo: {config['particiones']['proporcion_desarrollo']} de los grupos, por museo.",
        "",
        "## Piezas, grupos y consultas por museo y particion",
        "",
    ]
    lineas += tabla(filas, ["Museo", "Piezas desarrollo", "Grupos desarrollo", "Consultas desarrollo",
                            "Piezas prueba", "Grupos prueba", "Consultas prueba"])
    lineas += ["", "## Consultas por tipo de composicion (todas)", ""]
    lineas += tabla([[f"`{c}`", str(n)] for c, n in sorted(composicion.items())], ["Composicion", "Consultas"])
    lineas += ["", "## Comprobacion de fugas", ""]
    lineas += [f"- {e}" for e in errores] if errores else [
        "Sin fugas: ningun grupo esta en las dos particiones, cada consulta esta en la particion de su pieza, hay a lo "
        "sumo una consulta por grupo, todas tienen composicion observable y su numero es el de la configuracion."]
    return lineas


def validar(raiz: Path) -> int:
    if not (raiz / SALIDA_PARTICIONES).exists():
        print(f"No existe {SALIDA_PARTICIONES}: el snapshot experimental aun no se ha creado.")
        return 0
    config = leer_config_experimento(raiz)
    errores, resumen = comprobar(raiz, config)
    escribir_texto(raiz / REPORTE_SNAPSHOT, lineas_reporte(errores, resumen, config))
    if errores:
        print(f"Snapshot experimental con {len(errores)} problemas; ver {REPORTE_SNAPSHOT}.")
        for error in errores[:20]:
            print(f"- {error}")
        return 1
    print(f"Snapshot experimental sin fugas: {len(resumen['particiones'])} piezas, {len(resumen['consultas'])} consultas T3")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Snapshot experimental v2: particiones y consultas T3.")
    parser.add_argument("--root", default=".", help="Raiz del repositorio.")
    accion = parser.add_mutually_exclusive_group()
    accion.add_argument("--crear", action="store_true", help="Fija las particiones y sortea las consultas (una vez).")
    accion.add_argument("--reemplazar", action="store_true", help="Reemplaza las consultas que dejaron de ser elegibles.")
    parser.add_argument("--forzar", action="store_true", help="Con --crear, sobrescribe un snapshot existente.")
    args = parser.parse_args(argv)
    raiz = Path(args.root).resolve()
    if args.crear:
        return crear(raiz, args.forzar)
    if args.reemplazar:
        return reemplazar(raiz)
    return validar(raiz)


if __name__ == "__main__":
    raise SystemExit(main())
