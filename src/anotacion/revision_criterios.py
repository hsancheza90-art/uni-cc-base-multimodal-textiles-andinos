"""Revisión de criterios de la anotación v2 antes de congelar la versión 2.1.

Uso desde la raíz del repositorio:

    python -m src.anotacion.revision_criterios --crear   # crea o actualiza el workbook (conserva lo escrito)

Después de la re-anotación del lote 1 se escribieron dos criterios que los lotes 2 a 5 no
tuvieron: qué cuenta como banda (R12) y la frontera entre simetría traslacional y repetición
modular (R16). Este módulo selecciona las piezas de esos lotes que hay que volver a mirar,
genera el workbook donde el anotador confirma o corrige (data/metadata/
anotacion_v2_revision_criterios.xlsx) y aplica sus decisiones al exportar la anotación
(src/anotacion/aplicar_anotaciones_v2.py). El workbook de la primera anotación no se modifica:
la corrección queda registrada aparte, con su motivo, y ese registro es el de adjudicaciones.

Una pieza entra a la revisión por una o más reglas, que se escriben en `motivos_revision`:

- R12: su palabra de bandas registra bandas.
- R16: su simetría es traslacional o repeticion_modular.
- OBS: sus observaciones marcan una DUDA o un CRITERIO sobre un atributo que usa M3, o sin
  nombrar ningún atributo.
- ID: sus observaciones piden verificar que la imagen corresponde al registro.

Las dudas que solo tocan atributos ajenos a M3 (motivo_principal, color, técnica, tipo de
objeto o de superficie) y los huecos de vocabulario (VOCAB) no entran: se cuentan en el informe
y se declaran.

Propuestas automáticas (decisión R20): si existe data/metadata/
anotacion_v2_revision_criterios_propuestas.csv, `--crear` precarga cada fila sin decidir con la
propuesta y la firma `revisor = auto`. Una fila firmada así no se aplica ni cuenta como decidida:
el revisor la verifica frente a la imagen, la corrige si hace falta y pone su nombre. Las columnas
`propuesta*` conservan lo propuesto, para que el informe compare propuesta y decisión.

Decisión por pieza: `confirmar` (la anotación se mantiene) o `corregir` (al menos un valor
revisado y su motivo). Toda decisión lleva revisor y fecha. Una pieza marcada ID exige además
`identidad_imagen`. Sin decisión, la pieza queda pendiente y la versión 2.1 no puede congelarse.
"""

from __future__ import annotations

import argparse
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from src.anotacion.aplicar_anotaciones import fecha_valida
from src.experimento.libro import escribir_libro
from src.utils.archivos import leer_csv
from src.utils.config import CONFIG_ANOTACION, leer_config_anotacion
from src.utils.libros import leer_hoja
from src.utils.metricas import tabla
from src.utils.vocabulario import Campo, leer_vocabulario

HOJA = "revision"
REPORTE = "outputs/reports/anotacion_v2_revision_criterios.md"
DECISIONES = ("confirmar", "corregir")
IDENTIDAD = ("coincide", "no_coincide")
CONTROL = ["decision", "motivo", "revisor", "fecha_revision", "identidad_imagen"]
CONTEXTO_FIJO = ["id_global", "lote", "orden", "archivo_imagen", "motivos_revision"]
# Propuesta automatica (decision R20): se muestra como contexto y no cambia al editar la decision.
PROPUESTA = ["propuesta", "propuesta_vista", "propuesta_criterios", "propuesta_confianza", "propuesta_nota"]
AUTO = "auto"

# Atributos que usa M3 (docs/especificacion_m3.md) y palabras con que las observaciones los nombran.
PATRON_M3 = re.compile(
    r"composici[oó]n|composicion_libre|campo_central|ret[ií]cula|paneles|esquina|banda|palabra|\bborde\b|\bcentro\b|"
    r"simetr|repetici|\bmotivos\b|familia_iconografica", re.IGNORECASE)
PATRON_AJENO = re.compile(
    r"motivo_principal|color_dominante|\bcolores\b|t[eé]cnica|tecnica|tipo_objeto|tipo_superficie|estado_imagen",
    re.IGNORECASE)
PATRON_SEGMENTO = re.compile(r"\b(OBS|DUDA|CRITERIO|VOCAB|REC)\b")
PATRON_ID = re.compile(r"verificar el id", re.IGNORECASE)


def revisado(atributo: str) -> str:
    return f"{atributo}_revisado"


def nombre_imagen(fila: dict[str, str], extension: str = ".jpg") -> str:
    return f"L{fila['lote']}-{int(fila['orden']):03d}_{fila['id_global'].replace(':', '-')}{extension}"


# --------------------------------------------------------------------------- seleccion


def segmentos(observaciones: str) -> list[tuple[str, str]]:
    """Pares (etiqueta, texto) de una observación: OBS, DUDA, CRITERIO, VOCAB y REC."""
    partes = PATRON_SEGMENTO.split(observaciones)
    return [(partes[i], partes[i + 1].strip(" :")) for i in range(1, len(partes) - 1, 2)]


def toca_m3(texto: str) -> bool:
    """Una duda o un criterio toca a M3 si nombra un atributo suyo o no nombra ninguno."""
    return bool(PATRON_M3.search(texto)) or not PATRON_AJENO.search(texto)


def motivos_revision(fila: dict[str, str], vocabulario: dict[str, Campo]) -> list[str]:
    motivos = []
    secuencia = fila.get("secuencia_bandas", "")
    if secuencia and secuencia not in vocabulario["secuencia_bandas"].estados:
        motivos.append("R12")
    if fila.get("simetria", "") in ("traslacional", "repeticion_modular"):
        motivos.append("R16")
    observaciones = fila.get("observaciones_anotacion", "")
    if any(etiqueta in ("DUDA", "CRITERIO") and toca_m3(texto) for etiqueta, texto in segmentos(observaciones)):
        motivos.append("OBS")
    if PATRON_ID.search(observaciones):
        motivos.append("ID")
    return motivos


def seleccionar(anotadas: list[dict[str, str]], config: dict[str, Any], vocabulario: dict[str, Campo]
                ) -> list[dict[str, str]]:
    """Piezas de los lotes de [revision_criterios] que entran a la revisión, con sus motivos."""
    lotes = {str(lote) for lote in config["revision_criterios"]["lotes"]}
    atributos = list(config["revision_criterios"]["atributos"])
    salida = []
    for fila in anotadas:
        if fila.get("lote", "") not in lotes:
            continue
        motivos = motivos_revision(fila, vocabulario)
        if not motivos:
            continue
        salida.append({"id_global": fila["id_global"], "lote": fila["lote"], "orden": fila["orden"],
                       "archivo_imagen": nombre_imagen(fila), "motivos_revision": "; ".join(motivos),
                       **{a: fila.get(a, "") for a in atributos},
                       "observaciones_anotacion": fila.get("observaciones_anotacion", "")})
    return salida


def observaciones_fuera(anotadas: list[dict[str, str]], config: dict[str, Any]) -> Counter:
    """Piezas de los lotes revisados con DUDA o VOCAB que no tocan a M3 (solo conteos, para el informe)."""
    lotes = {str(lote) for lote in config["revision_criterios"]["lotes"]}
    conteo: Counter = Counter()
    for fila in anotadas:
        if fila.get("lote", "") not in lotes:
            continue
        partes = segmentos(fila.get("observaciones_anotacion", ""))
        if any(e in ("DUDA", "CRITERIO") and not toca_m3(t) for e, t in partes):
            conteo["dudas sobre atributos que M3 no usa"] += 1
        if any(e == "VOCAB" for e, _ in partes):
            conteo["huecos de vocabulario (VOCAB)"] += 1
    return conteo


# --------------------------------------------------------------------------- workbook


def columnas(config: dict[str, Any]) -> tuple[list[str], list[str]]:
    """Columnas editables (a la izquierda) y todas las columnas de la hoja."""
    atributos = list(config["revision_criterios"]["atributos"])
    editables = ["decision", *(revisado(a) for a in atributos), "identidad_imagen", "motivo", "revisor", "fecha_revision"]
    return editables, editables + CONTEXTO_FIJO + PROPUESTA + atributos + ["observaciones_anotacion"]


def resumen_decision(decision: str, valores: dict[str, str], identidad: str) -> str:
    """Forma canónica de una decisión, para comparar la propuesta automática con la decisión verificada."""
    if not decision:
        return ""
    texto = decision + (": " + "; ".join(f"{a}={v}" for a, v in sorted(valores.items())) if valores else "")
    return texto + (f" | identidad: {identidad}" if identidad else "")


def leer_propuestas(raiz: Path, config: dict[str, Any]) -> dict[str, dict[str, str]]:
    """Propuestas automáticas por pieza (insumo versionado, calculado fuera del flujo); vacío si no existen."""
    ruta = raiz / config["revision_criterios"]["propuestas"]
    return {f["id_global"]: f for f in leer_csv(ruta)} if ruta.exists() else {}


def con_propuesta(fila: dict[str, str], propuesta: dict[str, str] | None, editables: list[str], atributos: list[str]
                  ) -> dict[str, str]:
    """Añade la propuesta como contexto y, si la fila no tiene nada escrito, la precarga firmada como auto."""
    if propuesta is None:
        return {**fila, **dict.fromkeys(PROPUESTA, "")}
    valores = {a: propuesta[revisado(a)] for a in atributos if propuesta.get(revisado(a))}
    salida = {**fila, "propuesta": resumen_decision(propuesta["decision"], valores, propuesta.get("identidad_imagen", "")),
              "propuesta_vista": propuesta.get("lo_que_se_ve", ""), "propuesta_criterios": propuesta.get("criterios", ""),
              "propuesta_confianza": propuesta.get("confianza", ""), "propuesta_nota": propuesta.get("nota", "")}
    if not any(fila.get(c) for c in editables):
        salida |= {c: propuesta.get(c, "") for c in editables}
        salida |= {"revisor": AUTO, "fecha_revision": propuesta.get("fecha_propuesta", "")}
    return salida


GUIA = [
    "Revision de criterios de la anotacion v2 (lotes 2 a 5), antes de congelar la version 2.1",
    "",
    "Cada fila es una pieza que hay que volver a mirar. 'motivos_revision' dice por que:",
    "  R12  tiene palabra de bandas. Una banda es una franja que atraviesa toda la superficie visible, perpendicular al",
    "       eje de lectura. NO son bandas las cenefas perimetrales (van en 'borde'), las filas o columnas de una reticula",
    "       ni los paneles (van en 'composicion'). Si la palabra incluye alguno, corrijala; si no queda ninguna banda,",
    "       escriba 'ausente' en eje_bandas_revisado y en secuencia_bandas_revisado.",
    "  R16  simetria traslacional o repeticion_modular. traslacional: un motivo se desplaza en una sola direccion y forma",
    "       un friso continuo. repeticion_modular: un modulo con contorno propio (celda, cuadro, panel) se repite en dos",
    "       dimensiones o como piezas separadas. Si hay las dos, la que organiza la mayor parte de la superficie.",
    "  OBS  las observaciones marcan una duda o un criterio sobre un atributo que usa M3. Resuelvala.",
    "  ID   las observaciones piden verificar que la imagen corresponde al registro. Mire el archivo de la carpeta de",
    "       imagenes y llene 'identidad_imagen': coincide o no_coincide.",
    "",
    "Como se decide cada fila:",
    "  confirmar  la anotacion se mantiene. No llene ninguna columna *_revisado.",
    "  corregir   llene solo las columnas *_revisado que cambian (codigos del vocabulario o un estado) y el 'motivo'.",
    "  Toda decision lleva 'revisor' y 'fecha_revision' (AAAA-MM-DD). Una fila sin decision queda pendiente.",
    "",
    "Propuestas automaticas: las filas con revisor = auto traen una propuesta precargada. NO cuentan como decididas.",
    "  Mire la imagen, lea 'propuesta_vista' y 'propuesta_nota', y verifique la decision y los valores *_revisado.",
    "  Si esta de acuerdo, cambie 'revisor' por su nombre y ponga la fecha. Si no, corrija lo que haga falta y firme.",
    "  Las columnas 'propuesta*' son de contexto: no las edite.",
    "",
    "Mire solo la imagen. No consulte rankings, juicios de relevancia ni resultados de ningun sistema.",
    "secuencia_bandas_revisado: tipos en orden separados por ' > ' (lisa, geometrica, figurativa, mixta, no_determinada, laguna).",
    "motivos_revisado: codigos separados por '; '.",
    "",
    "Despues: python -m src.flujo aplica las correcciones al exportar data/metadata/anotaciones_v2.csv y genera",
    "outputs/reports/anotacion_v2_revision_criterios.md con el registro de adjudicaciones.",
]

EJEMPLOS = (
    ["ejemplo", "motivos_revision", "anotacion_actual", "lo_que_se_ve", "decision", "valores_revisados", "motivo"],
    [
        {"ejemplo": "E1", "motivos_revision": "R12", "anotacion_actual": "secuencia_bandas = geometrica > lisa > geometrica",
         "lo_que_se_ve": "Campo liso con una cenefa de rombos en los dos extremos.", "decision": "corregir",
         "valores_revisados": "eje_bandas_revisado = ausente; secuencia_bandas_revisado = ausente; borde_revisado = si",
         "motivo": "Las franjas de los extremos son cenefas, no bandas (R12)."},
        {"ejemplo": "E2", "motivos_revision": "R12", "anotacion_actual": "secuencia_bandas = lisa > figurativa > lisa",
         "lo_que_se_ve": "Tres franjas que atraviesan toda la pieza.", "decision": "confirmar", "valores_revisados": "",
         "motivo": ""},
        {"ejemplo": "E3", "motivos_revision": "R16", "anotacion_actual": "simetria = repeticion_modular",
         "lo_que_se_ve": "Una sola fila de aves que se repite a lo largo de la franja.", "decision": "corregir",
         "valores_revisados": "simetria_revisado = traslacional", "motivo": "Friso en una direccion, sin modulo con contorno (R16)."},
        {"ejemplo": "E4", "motivos_revision": "R12; R16", "anotacion_actual": "composicion = reticula; secuencia de seis bandas",
         "lo_que_se_ve": "Damero de cuadros; cada fila se habia escrito como una banda.", "decision": "corregir",
         "valores_revisados": "eje_bandas_revisado = ausente; secuencia_bandas_revisado = ausente",
         "motivo": "Las filas de una reticula no son bandas (R12)."},
    ],
)


def crear(raiz: Path) -> int:
    from src.anotacion import aplicar_anotaciones_v2 as exportacion  # evita la importacion circular

    config = leer_config_anotacion(raiz)
    vocabulario = leer_vocabulario(raiz)
    base = exportacion.base_adjudicada(raiz, config, vocabulario)
    if base is None:
        print("No hay anotacion v2 valida: corrija primero los errores del workbook de anotacion.")
        return 1
    ruta = raiz / config["revision_criterios"]["workbook"]
    editables, encabezados = columnas(config)
    previas = {f["id_global"]: f for f in leer_hoja(ruta, HOJA, clave="id_global")} if ruta.exists() else {}
    propuestas = leer_propuestas(raiz, config)
    atributos = list(config["revision_criterios"]["atributos"])
    filas = [con_propuesta({**fila, **{c: previas.get(fila["id_global"], {}).get(c, "") for c in editables}},
                           propuestas.get(fila["id_global"]), editables, atributos)
             for fila in seleccionar(base, config, vocabulario)]
    perdidas = sorted(i for i, f in previas.items() if any(f.get(c) for c in editables) and i not in {x["id_global"] for x in filas})
    if perdidas:
        print(f"No se actualizo el workbook: hay decisiones de piezas que ya no entran a la revision: {perdidas}")
        return 1
    listas = {"decision": list(DECISIONES), "identidad_imagen": list(IDENTIDAD)}
    for atributo in config["revision_criterios"]["atributos"]:
        campo = vocabulario[atributo]
        if not campo.multiple and not campo.secuencia:
            listas[revisado(atributo)] = list(campo.admitidos)
    anchos = {"propuesta": 45, "propuesta_vista": 60, "propuesta_nota": 60, "secuencia_bandas": 40, revisado("secuencia_bandas"): 40, "motivo": 45, "observaciones_anotacion": 90,
              "archivo_imagen": 26, "motivos": 26, revisado("motivos"): 26}
    try:
        escribir_libro(ruta, GUIA, HOJA, encabezados, filas, editables, anchos, listas, EJEMPLOS)
    except PermissionError:
        print(f"No se pudo escribir {ruta}: cierre el archivo en Excel.")
        return 1
    print(f"Workbook de revision de criterios: {ruta} ({len(filas)} piezas, "
          f"{sum(bool(f['decision']) and f['revisor'] != AUTO for f in filas)} verificadas, "
          f"{sum(f['revisor'] == AUTO for f in filas)} propuestas sin verificar)")
    return 0


# --------------------------------------------------------------------------- aplicacion


@dataclass
class Revision:
    """Resultado de aplicar el workbook de revisión a las filas adjudicadas."""

    existe: bool = False
    filas: list[dict[str, str]] = field(default_factory=list)
    seleccionadas: int = 0
    por_motivo: Counter = field(default_factory=Counter)
    decisiones: Counter = field(default_factory=Counter)
    cambios: list[list[str]] = field(default_factory=list)  # id, atributo, antes, despues, motivo
    no_coinciden: list[str] = field(default_factory=list)
    propuestas: int = 0  # filas con la propuesta automatica sin verificar (revisor = auto): no se aplican
    frente_a_propuesta: Counter = field(default_factory=Counter)  # decisiones verificadas: igual o distinta
    errores: list[str] = field(default_factory=list)
    fuera: Counter = field(default_factory=Counter)

    @property
    def pendientes(self) -> int:
        return self.seleccionadas - sum(self.decisiones.values())


def aplicar(anotadas: list[dict[str, str]], decisiones: list[dict[str, str]] | None, config: dict[str, Any],
            vocabulario: dict[str, Campo]) -> Revision:
    """Aplica las decisiones a las filas adjudicadas; `decisiones` es None si no hay workbook."""
    seleccion = {f["id_global"]: f for f in seleccionar(anotadas, config, vocabulario)}
    resultado = Revision(existe=decisiones is not None, filas=anotadas, seleccionadas=len(seleccion),
                         fuera=observaciones_fuera(anotadas, config))
    for fila in seleccion.values():
        resultado.por_motivo.update(fila["motivos_revision"].split("; "))
    if decisiones is None:
        return resultado
    atributos = list(config["revision_criterios"]["atributos"])
    por_id = {}
    for fila in decisiones:
        id_global = fila["id_global"]
        if id_global in por_id:
            resultado.errores.append(f"{id_global}: aparece mas de una vez")
        por_id[id_global] = fila
    sobran = sorted(set(por_id) - set(seleccion))
    faltan = sorted(set(seleccion) - set(por_id))
    if sobran or faltan:
        resultado.errores.append(f"El workbook no corresponde a la seleccion vigente (sobran {len(sobran)}, faltan "
                                 f"{len(faltan)}): regenerelo con --crear. Ejemplos: {(sobran + faltan)[:5]}")
    corregidas: dict[str, dict[str, str]] = {}
    for id_global, fila in por_id.items():
        if id_global not in seleccion:
            continue
        vigente = seleccion[id_global]
        if any(fila.get(a, "") != vigente[a] for a in atributos):
            resultado.errores.append(f"{id_global}: la anotacion cambio desde que se genero el workbook; regenerelo con --crear")
            continue
        nuevos = {}
        for atributo in atributos:
            valor = fila.get(revisado(atributo), "")
            if not valor:
                continue
            valor = vocabulario[atributo].recodificar(valor)
            invalidos = vocabulario[atributo].invalidos(valor)
            if invalidos:
                resultado.errores.append(f"{id_global}: {revisado(atributo)} fuera del vocabulario: {invalidos}")
            nuevos[atributo] = valor
        decision = fila.get("decision", "")
        if not decision:
            if nuevos or any(fila.get(c) for c in ("motivo", "identidad_imagen")):
                resultado.errores.append(f"{id_global}: hay valores escritos sin decision")
            continue
        if decision not in DECISIONES:
            resultado.errores.append(f"{id_global}: decision debe ser {' o '.join(DECISIONES)}")
            continue
        if fila.get("revisor") == AUTO:
            resultado.propuestas += 1  # se valida arriba, pero no cuenta ni se aplica hasta que un revisor la verifique
            continue
        resultado.decisiones[decision] += 1
        if fila.get("propuesta"):
            igual = resumen_decision(decision, nuevos, fila.get("identidad_imagen", "")) == fila["propuesta"]
            resultado.frente_a_propuesta["igual a la propuesta" if igual else "distinta de la propuesta"] += 1
        if not fila.get("revisor"):
            resultado.errores.append(f"{id_global}: revisor vacio")
        if not fecha_valida(fila.get("fecha_revision", "")):
            resultado.errores.append(f"{id_global}: fecha_revision vacia o invalida (AAAA-MM-DD)")
        identidad = fila.get("identidad_imagen", "")
        if "ID" in vigente["motivos_revision"].split("; ") and identidad not in IDENTIDAD:
            resultado.errores.append(f"{id_global}: identidad_imagen debe ser {' o '.join(IDENTIDAD)}")
        if identidad == "no_coincide":
            resultado.no_coinciden.append(id_global)
        cambios = {a: v for a, v in nuevos.items() if v != vigente[a]}
        if decision == "confirmar" and nuevos:
            resultado.errores.append(f"{id_global}: confirmar no admite valores revisados")
        if decision == "corregir":
            if not cambios:
                resultado.errores.append(f"{id_global}: corregir exige al menos un valor revisado distinto del vigente")
            if not fila.get("motivo"):
                resultado.errores.append(f"{id_global}: corregir exige motivo")
            final = {**vigente, **cambios}
            estados_eje, estados_secuencia = vocabulario["eje_bandas"].estados, vocabulario["secuencia_bandas"].estados
            if (final["eje_bandas"] in estados_eje) != (final["secuencia_bandas"] in estados_secuencia):
                resultado.errores.append(f"{id_global}: eje_bandas y secuencia_bandas no concuerdan tras la correccion")
            corregidas[id_global] = cambios
            resultado.cambios += [[id_global, f"`{a}`", vigente[a], v, fila.get("motivo", "")] for a, v in cambios.items()]
    resultado.filas = [{**fila, **corregidas.get(fila["id_global"], {})} for fila in anotadas]
    return resultado


def leer_decisiones(raiz: Path, config: dict[str, Any]) -> list[dict[str, str]] | None:
    ruta = raiz / config["revision_criterios"]["workbook"]
    return leer_hoja(ruta, HOJA, clave="id_global") if ruta.exists() else None


def lineas_reporte(revision: Revision, config: dict[str, Any]) -> list[str]:
    datos = config["revision_criterios"]
    lotes = ", ".join(str(lote) for lote in datos["lotes"])
    lineas = [
        "# Revision de criterios de la anotacion v2",
        "",
        "Generado por `python -m src.anotacion.aplicar_anotaciones_v2`, paso del flujo, con las reglas de "
        f"`src/anotacion/revision_criterios.py`. Workbook: `{datos['workbook']}`; parametros en "
        f"`{CONFIG_ANOTACION.as_posix()}` ([revision_criterios]).",
        "",
        f"Los lotes {lotes} se anotaron antes de escribir la definicion de banda (R12) y la frontera entre simetria "
        "traslacional y repeticion modular (R16). El anotador vuelve a mirar las piezas afectadas y confirma o corrige. "
        "La primera anotacion no se modifica en su workbook: las correcciones se aplican al exportar "
        "`data/metadata/anotaciones_v2.csv` y quedan registradas abajo.",
        "",
        f"- Piezas en revision: {revision.seleccionadas}.",
        f"- Confirmadas: {revision.decisiones['confirmar']}; corregidas: {revision.decisiones['corregir']}; "
        f"pendientes: {revision.pendientes if revision.existe else revision.seleccionadas}.",
        f"- Valores corregidos: {len(revision.cambios)}.",
        f"- Propuestas automaticas sin verificar (`revisor = {AUTO}`): {revision.propuestas}. No se aplican: cuentan como "
        "pendientes hasta que el revisor las verifica y firma.",
    ]
    if revision.frente_a_propuesta:
        lineas.append("- Decisiones verificadas frente a la propuesta automatica: "
                      + "; ".join(f"{k}, {v}" for k, v in sorted(revision.frente_a_propuesta.items())) + ".")
    if not revision.existe:
        lineas.append("- El workbook no existe todavia: se crea con `python -m src.anotacion.revision_criterios --crear`.")
    lineas += ["", "## Piezas por motivo de revision", "",
               *tabla([[m, str(revision.por_motivo[m])] for m in ("R12", "R16", "OBS", "ID")], ["Motivo", "Piezas"]),
               "", "`R12`: tiene palabra de bandas. `R16`: simetria traslacional o repeticion_modular. `OBS`: sus observaciones "
               "marcan una duda o un criterio sobre un atributo que usa M3. `ID`: sus observaciones piden verificar que la "
               "imagen corresponde al registro. Una pieza puede tener varios motivos.",
               "", "## Observaciones que no entran a la revision", ""]
    lineas += (tabla([[k, str(v)] for k, v in sorted(revision.fuera.items())], ["Tipo", "Piezas"])
               if revision.fuera else ["Ninguna."])
    lineas += ["", "No tocan ningun atributo de M3 (`motivo_principal`, color, tecnica, tipo de objeto o de superficie) o "
                   "son huecos del vocabulario. No se resuelven en la version 2.1 y se declaran como limitacion.",
               "", "## Registro de adjudicaciones", ""]
    lineas += (tabla(revision.cambios, ["Pieza", "Atributo", "Antes", "Despues", "Motivo"])
               if revision.cambios else ["Ninguna correccion."])
    lineas += ["", "## Imagenes que no corresponden al registro", ""]
    lineas += [f"- {i}" for i in revision.no_coinciden] if revision.no_coinciden else ["Ninguna."]
    lineas += ["", "## Errores", ""]
    lineas += [f"- {e}" for e in revision.errores] if revision.errores else ["Ninguno."]
    return lineas


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Revision de criterios de la anotacion v2: workbook del anotador.")
    parser.add_argument("--root", default=".", help="Raiz del repositorio.")
    parser.add_argument("--crear", action="store_true", help="Crea o actualiza el workbook conservando lo escrito.")
    args = parser.parse_args(argv)
    if not args.crear:
        print("Las decisiones se aplican con el flujo (src.anotacion.aplicar_anotaciones_v2). Use --crear para el workbook.")
        return 0
    return crear(Path(args.root).resolve())


if __name__ == "__main__":
    raise SystemExit(main())
