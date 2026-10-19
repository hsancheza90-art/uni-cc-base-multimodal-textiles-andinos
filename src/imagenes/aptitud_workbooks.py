"""Lleva la ficha de aptitud a los workbooks de revision manual (MET, CMA y AIC).

Uso desde la raiz del repositorio (sin red; cerrar Excel antes):

    python -m src.imagenes.aptitud_workbooks
    python -m src.imagenes.aptitud_workbooks --fuente aic

Agrega al final de la hoja de revision columnas informativas: puntaje, banda
sugerida, imagen de referencia sugerida, nivel de cada atributo (fotografia,
colores, formas, completitud, estructura), justificacion y las discrepancias
entre la anotacion del revisor y lo que muestra la imagen (revisar_anotacion).

Enriquece motivo_revision: «Revisor: <motivo normalizado>. Analisis de imagen:
<conclusiones con sus medidas>». El texto del revisor se conserva intacto en
motivo_revision_original; si el revisor edita despues motivo_revision, la edicion
se toma como su nuevo original (motivo_generado, oculta, guarda el ultimo texto
generado para detectarlo).

No cambia ninguna decision humana. Solo decide, con revisor "auto", en las filas
que siguen en corpus_final = revisar y caen en una puerta:

- fotografia_monocroma -> secundario (el color no es identificable);
- resolucion_insuficiente o sin_imagen -> descartados;
- plumaria, muneco o posterior_inca (reglas de pertinencia por metadatos) -> descartados.

Una fila decidida antes por este script y no corregida se vuelve a evaluar.
"""

from __future__ import annotations

import argparse
import tomllib
from datetime import date
from pathlib import Path

from openpyxl import load_workbook
from openpyxl.styles import Alignment, Font, PatternFill

from src.imagenes.aptitud import SALIDA_APTITUD
from src.imagenes.motivos import analizar_motivo, describir_motivo
from src.utils.archivos import indexar, leer_csv
from src.utils.config import CONFIG_APTITUD

WORKBOOKS = {
    "MET": ("data/metadata/met_revision_manual_v2.xlsx", "revision_met_v2"),
    "CMA": ("data/metadata/cma_revision_manual_v2.xlsx", "revision_cma_v2"),
    "AIC": ("data/metadata/aic_revision_manual_v2.xlsx", "revision_aic_v2"),
}

# Columna del workbook -> columna de data/metadata/aptitud_imagenes_v2.csv (ancho en Excel).
COLUMNAS_APTITUD = {
    "puntaje_aptitud": ("puntaje_aptitud", 12),
    "banda_sugerida": ("banda_sugerida", 14),
    "referencia_sugerida": ("referencia_sugerida", 14),
    "motivo_banda": ("motivo_banda", 20),
    "fotografia": ("fotografia", 14),
    "colores": ("colores", 18),
    "formas": ("formas", 16),
    "completitud": ("completitud", 14),
    "estructura": ("estructura", 20),
    "justificacion_aptitud": ("justificacion", 70),
}
COLUMNAS_REVISION = {"revisar_anotacion": 50, "motivo_revision_original": 50, "motivo_generado": 10}

PUERTAS = {
    "plumaria": ("descartados", "Textil con plumaria: fuera del estudio."),
    "muneco": ("descartados", "Muñeco: no es una superficie textil del estudio."),
    "posterior_inca": ("descartados", "Pieza posterior a 1532: el estudio abarca textiles incas y anteriores."),
    "fotografia_monocroma": ("secundario", "Fotografia en blanco y negro: el color no es identificable."),
    "resolucion_insuficiente": ("descartados", "Resolucion insuficiente del textil en la imagen institucional."),
    "sin_imagen": ("descartados", "Sin imagen institucional disponible."),
}
ORIGEN_AUTOMATICO = "aptitud_automatica"
# Orden de severidad: una regla solo puede llevar una decision hacia un corpus mas estricto.
SEVERIDAD = {"principal": 0, "secundario": 1, "descartados": 2}
# Descartes v1 por pertinencia (no dependen de la imagen): las reglas no los tocan.
DESCARTES_PERTINENCIA_V1 = {
    "material_sin_superficie", "implemento_textil_no_analizable", "descartar_no_andino", "descartar_no_textil",
    "descartar_duplicado", "herramienta_textil", "fuera_alcance",
}
PREFIJO_OBSERVACION = "Asignacion automatica (puntaje de aptitud)."


def puerta_registrada(leer) -> str:
    """Puerta que este script dejo escrita en la observacion de la fila (vacio si no hay)."""
    observacion = leer("observaciones_revision")
    if not observacion.startswith(PREFIJO_OBSERVACION):
        return ""
    for codigo, (_, texto) in PUERTAS.items():
        if observacion[len(PREFIJO_OBSERVACION):].strip().startswith(texto):
            return codigo
    return ""


def intacta(leer) -> bool:
    """Fila que este script decidio y cuya decision nadie cambio despues.

    Si el revisor cambio corpus_final o decision_revision (aunque dejara revisor = auto),
    la fila cuenta como decision humana y no se vuelve a tocar.
    """
    puerta = puerta_registrada(leer)
    return (
        bool(puerta)
        and leer("origen_curacion") == ORIGEN_AUTOMATICO
        and leer("revisor") == "auto"
        and leer("corpus_final") == PUERTAS[puerta][0]
        and leer("decision_revision") == decision_para(leer("corpus_actual"), PUERTAS[puerta][0])
    )


def editada(leer) -> bool:
    return leer("origen_curacion") == ORIGEN_AUTOMATICO and leer("revisor") == "auto" and not intacta(leer)


def es_decision_automatica(leer) -> bool:
    """Decision automatica (filtro o puntaje) que el revisor no corrigio despues."""
    return leer("revisor") == "auto" and not editada(leer)


def es_descarte_pertinencia_v1(leer) -> bool:
    motivos = {leer("estado_curacion"), leer("motivo_curacion"), leer("motivo_revision")}
    return leer("corpus_final") == "descartados" and bool(motivos & DESCARTES_PERTINENCIA_V1)


def regla_endurece(leer, motivo: str) -> bool:
    """La puerta lleva la decision vigente a un corpus mas estricto (nunca la suaviza)."""
    actual = leer("corpus_final")
    return (motivo in PUERTAS and actual in SEVERIDAD and not es_descarte_pertinencia_v1(leer)
            and SEVERIDAD[PUERTAS[motivo][0]] > SEVERIDAD[actual])


def decision_para(corpus_actual: str, corpus_final: str) -> str:
    if corpus_final == "descartados":
        return "descartar"
    return "mantener" if corpus_actual == corpus_final else "mover"


def motivo_del_revisor(leer) -> str:
    """Motivo escrito por el revisor, sin el analisis de imagen añadido por este script."""
    generado = leer("motivo_generado")
    if generado and leer("motivo_revision") == generado:
        return leer("motivo_revision_original")
    return leer("motivo_revision")  # primera vez, o el revisor edito el motivo enriquecido


def motivo_enriquecido(original: str, justificacion: str, automatica: bool) -> str:
    partes = []
    autor = "Decisión automática" if automatica else "Revisor"
    normalizado = describir_motivo(analizar_motivo(original))
    if normalizado:
        partes.append(f"{autor}: {normalizado}.")
    elif original:
        partes.append(f"{autor}: {original.strip()}.")
    if justificacion:
        partes.append(f"Análisis de imagen: {justificacion}")
    return " ".join(partes)


def discrepancias(original: str, decision: str, registro: dict[str, str], umbral: float) -> str:
    """Desacuerdos fuertes entre la anotacion del revisor y lo que muestra la imagen."""
    if not registro.get("prob_colores"):
        return ""
    a = analizar_motivo(original)
    p = {clave: float(registro[f"prob_{clave}"]) for clave in ("colores", "formas", "completitud", "referencia")}
    # Las notas se separan con «; »: dentro de cada nota solo se usan comas.
    notas = []
    if a["completitud"] != "completo" and p["completitud"] >= umbral:
        notas.append(f"posible textil completo no anotado (probabilidad {p['completitud']:.2f})")
    if a["completitud"] == "completo" and p["completitud"] <= 1 - umbral:
        notas.append(f"anotado completo, pero la imagen sugiere incompleto ({p['completitud']:.2f})")
    for atributo, nombre in (("colores", "colores"), ("formas", "formas")):
        if a[atributo] == "si" and p[atributo] <= 1 - umbral:
            notas.append(f"anotado con {nombre} visibles, pero la imagen sugiere lo contrario ({p[atributo]:.2f})")
        if a[atributo] == "no" and p[atributo] >= umbral:
            notas.append(f"anotado sin {nombre} visibles, pero la imagen sugiere que sí ({p[atributo]:.2f})")
    if decision == "principal" and not a["referencia"] and registro["referencia_sugerida"] == "si":
        notas.append(f"posible imagen de referencia (puntaje {float(registro['puntaje_aptitud']):.0f})")
    if decision == "principal" and registro["banda_sugerida"] == "descartar":
        notas.append("en principal, pero la imagen sugiere descartar")
    if decision == "descartados" and not a["pertinencia"] and registro["banda_sugerida"] == "principal":
        notas.append("descartado, pero la imagen sugiere principal")
    return "; ".join(notas)


def agregar_columna(hoja, encabezado: list, nombre: str, ancho: int, oculta: bool = False) -> None:
    if nombre in encabezado:
        return
    celda = hoja.cell(row=1, column=len(encabezado) + 1, value=nombre)
    celda.font = Font(color="FFFFFF", bold=True)
    celda.fill = PatternFill("solid", fgColor="7F6000")  # distinto del encabezado de decisiones
    celda.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    hoja.column_dimensions[celda.column_letter].width = ancho
    hoja.column_dimensions[celda.column_letter].hidden = oculta
    encabezado.append(nombre)


def actualizar_workbook(raiz: Path, fuente: str, aptitud: dict[str, dict[str, str]], hoy: str, umbral: float,
                        solo_reglas: bool = False) -> dict[str, int]:
    """Lleva la ficha al workbook.

    solo_reglas (MET y CMA tras la validacion del 2026-10-19, kappa 0,56 < 0,6): aplica las
    puertas tambien a las filas ya decididas, solo si endurecen la decision, y no agrega la
    ficha completa ni enriquece motivos; solo refresca las columnas informativas existentes.
    """
    ruta, nombre_hoja = WORKBOOKS[fuente]
    libro = load_workbook(raiz / ruta)
    hoja = libro[nombre_hoja]
    encabezado = [celda.value for celda in hoja[1]]
    if not solo_reglas:
        for columna, (_, ancho) in COLUMNAS_APTITUD.items():
            agregar_columna(hoja, encabezado, columna, ancho)
        for columna, ancho in COLUMNAS_REVISION.items():
            agregar_columna(hoja, encabezado, columna, ancho, oculta=columna == "motivo_generado")
    indice = {nombre: posicion + 1 for posicion, nombre in enumerate(encabezado)}

    conteo = {"filas": 0, "automaticas": 0, "editadas": 0, "sin_puntaje": 0, "discrepancias": 0}
    for fila in range(2, hoja.max_row + 1):
        id_fuente = str(hoja.cell(row=fila, column=indice["id_fuente"]).value or "").strip()
        if not id_fuente:
            continue
        conteo["filas"] += 1

        def leer(columna: str) -> str:
            return str(hoja.cell(row=fila, column=indice[columna]).value or "").strip() if columna in indice else ""

        def escribir(**valores: object) -> None:
            for columna, valor in valores.items():
                celda = hoja.cell(row=fila, column=indice[columna], value=valor)
                celda.alignment = Alignment(vertical="top", wrap_text=True)

        registro = aptitud.get(f"{fuente}:{id_fuente}")
        if registro is None:
            conteo["sin_puntaje"] += 1
            continue
        escribir(**{columna: (float(registro[origen]) if columna == "puntaje_aptitud" and registro[origen] else registro[origen])
                    for columna, (origen, _) in COLUMNAS_APTITUD.items() if columna in indice})

        original = motivo_del_revisor(leer)
        motivo = registro["motivo_banda"]
        if intacta(leer) and puerta_registrada(leer) != motivo:
            # Decidida antes por este script, sin cambios, y la puerta cambio: se vuelve a evaluar.
            escribir(corpus_final="revisar", decision_revision="revisar", observaciones_revision="",
                     revisor="", fecha_revision="", origen_curacion=f"revision_manual_{fuente.lower()}")
            original = ""
        pendiente = leer("corpus_final") == "revisar" and not leer("revisor")
        if editada(leer):
            conteo["editadas"] += 1
        elif motivo in PUERTAS and (pendiente or (solo_reglas and not intacta(leer) and regla_endurece(leer, motivo))):
            corpus_final, texto = PUERTAS[motivo]
            anterior = "" if pendiente else (
                f" Decisión anterior: {leer('corpus_final')}"
                f" ({'; '.join(m for m in (leer('estado_curacion'), leer('motivo_curacion'), leer('motivo_revision')) if m) or 'sin motivo'}).")
            escribir(
                corpus_final=corpus_final,
                decision_revision=decision_para(leer("corpus_actual"), corpus_final),
                observaciones_revision=f"{PREFIJO_OBSERVACION} {texto} {registro['justificacion']}{anterior}",
                revisor="auto",
                fecha_revision=hoy,
                origen_curacion=ORIGEN_AUTOMATICO,
            )
            original = motivo
            conteo["automaticas"] += 1

        if solo_reglas:
            if es_decision_automatica(leer) and leer("origen_curacion") == ORIGEN_AUTOMATICO:
                escribir(motivo_revision=puerta_registrada(leer))
            continue
        enriquecido = motivo_enriquecido(original, registro["justificacion"], es_decision_automatica(leer))
        nota = discrepancias(original, leer("corpus_final"), registro, umbral)
        conteo["discrepancias"] += bool(nota)
        escribir(motivo_revision_original=original, motivo_revision=enriquecido, motivo_generado=enriquecido, revisar_anotacion=nota)

    hoja.auto_filter.ref = hoja.dimensions
    libro.save(raiz / ruta)
    return conteo


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Lleva la ficha de aptitud a los workbooks de revision.")
    parser.add_argument("--root", default=".", help="Raiz del repositorio.")
    parser.add_argument("--fuente", choices=["met", "cma", "aic"], action="append", help="Workbook(s) a actualizar; por defecto, todos.")
    parser.add_argument("--fecha", default=date.today().isoformat(), help="Fecha de las decisiones automaticas.")
    parser.add_argument("--solo-reglas", action="store_true",
                        help="Solo aplica las puertas (tambien a filas decididas, si endurecen) y refresca las columnas existentes.")
    args = parser.parse_args(argv)
    raiz = Path(args.root).resolve()
    with (raiz / CONFIG_APTITUD).open("rb") as archivo:
        umbral = tomllib.load(archivo)["revision"]["umbral_discrepancia"]
    aptitud = indexar(leer_csv(raiz / SALIDA_APTITUD), "id_global")
    for fuente in [f.upper() for f in args.fuente] if args.fuente else list(WORKBOOKS):
        conteo = actualizar_workbook(raiz, fuente, aptitud, args.fecha, umbral, args.solo_reglas)
        print(f"{fuente}: {conteo['filas']} filas | decisiones automaticas {conteo['automaticas']} | "
              f"automaticas editadas a mano (se respetan) {conteo['editadas']} | "
              f"discrepancias para revisar {conteo['discrepancias']} | sin puntaje {conteo['sin_puntaje']} -> {WORKBOOKS[fuente][0]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
