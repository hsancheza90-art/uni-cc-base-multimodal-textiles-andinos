"""Traslado de decisiones del revisor desde un workbook de trabajo a los workbooks MET y CMA.

Los workbooks de revision (data/metadata/*_revision_manual_v2.xlsx) son el registro unico
de las decisiones curatoriales. Cuando el revisor decide en un workbook auxiliar (la
muestra de validacion ciega o la revision con el criterio v2), sus decisiones se trasladan
aqui con su motivo, su fecha y una observacion que cita el archivo de origen y la decision
anterior, de modo que ninguna se pierda ni se edite a mano en los CSV.
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path

from openpyxl import load_workbook

from src.imagenes.aptitud_workbooks import WORKBOOKS, decision_para
from src.imagenes.motivos import analizar_motivo

REVISOR = "Henry Sánchez"
DECISIONES = ("principal", "secundario", "descartados")


def contradice_motivo(decision: str, motivo: str) -> bool:
    """La decision contradice el criterio del 2026-10-19 segun el propio motivo del revisor.

    Principal = colores y formas identificables (completo o incompleto). Un descarte o un
    secundario cuyo motivo dice «con colores y formas visibles», o un principal cuyo motivo
    dice que no se ven, se deja en revisar para que el revisor lo resuelva: el sistema no
    elige entre dos cosas que el revisor afirmo a la vez.
    """
    a = analizar_motivo(motivo)
    legible = a["colores"] == "si" and a["formas"] == "si"
    ilegible = a["colores"] == "no" or a["formas"] == "no"
    return (decision != "principal" and legible and not a["pertinencia"]) or (decision == "principal" and ilegible)


def leer_anotaciones(ruta: Path, hoja: str) -> dict[str, dict[str, str]]:
    libro = load_workbook(ruta, read_only=True, data_only=True)
    filas = list(libro[hoja].iter_rows(values_only=True))
    libro.close()
    indice = {nombre: i for i, nombre in enumerate(filas[0])}
    return {str(f[indice["id_global"]]): {c: str(f[i] or "").strip() for c, i in indice.items()} for f in filas[1:]}


def trasladar_anotaciones(raiz: Path, archivo: str, hoja_anotaciones: str, fecha: str, origen: str, descripcion: str,
                          registrar_confirmaciones: bool) -> Counter:
    """Lleva las decisiones anotadas en `archivo` a los workbooks MET y CMA.

    - Una anotacion vacia o fuera de principal/secundario/descartados no cambia nada.
    - Si contradice su propio motivo, el registro queda en revisar con la explicacion.
    - registrar_confirmaciones: si la decision coincide con la vigente, igual se registra el
      motivo nuevo (la revision v2 confirma decisiones con el criterio vigente). La validacion
      ciega no lo hace: alli solo importan los cambios.
    - Es idempotente: una fila ya trasladada con la misma decision y el mismo motivo se omite.
    """
    anotaciones = leer_anotaciones(raiz / archivo, hoja_anotaciones)
    conteo: Counter = Counter()
    for fuente in ("MET", "CMA"):
        ruta, nombre_hoja = WORKBOOKS[fuente]
        libro = load_workbook(raiz / ruta)
        hoja = libro[nombre_hoja]
        indice = {celda.value: celda.column for celda in hoja[1]}
        cambios = 0
        for fila in range(2, hoja.max_row + 1):
            id_global = f"{fuente}:{str(hoja.cell(row=fila, column=indice['id_fuente']).value or '').strip()}"
            anotacion = anotaciones.get(id_global)
            if not anotacion or anotacion.get("corpus_final") not in DECISIONES:
                continue

            def leer(columna: str) -> str:
                return str(hoja.cell(row=fila, column=indice[columna]).value or "").strip()

            decision, motivo = anotacion["corpus_final"], anotacion.get("motivo_revision", "")
            conflicto = contradice_motivo(decision, motivo)
            destino = "revisar" if conflicto else decision
            if leer("origen_curacion") == origen and (not registrar_confirmaciones or
                                                      (leer("corpus_final") == destino and leer("motivo_revision") == motivo)):
                continue  # ya trasladada
            confirma = destino == leer("corpus_final")
            if confirma and not (registrar_confirmaciones and motivo):
                conteo["coinciden"] += 1
                continue
            anterior = "; ".join(m for m in (leer("estado_curacion"), leer("motivo_curacion"), leer("motivo_revision")) if m) or "sin motivo"
            nota = (f"{descripcion} del {fecha} ({archivo}, orden {anotacion.get('orden', '')}): {decision}. "
                    f"Decisión anterior: {leer('corpus_final')} ({anterior}).")
            if conflicto:
                nota += " Queda en revisar: la anotación contradice su propio motivo según el criterio del 2026-10-19."
            valores = {
                "corpus_final": destino,
                "decision_revision": "revisar" if conflicto else decision_para(leer("corpus_actual"), destino),
                "motivo_revision": motivo,
                "observaciones_revision": nota,
                "revisor": REVISOR,
                "fecha_revision": fecha,
                "origen_curacion": origen,
            }
            for columna, valor in valores.items():
                hoja.cell(row=fila, column=indice[columna], value=valor)
            clase = "revisar" if conflicto else ("confirmadas" if confirma else "cambiadas")
            conteo[clase] += 1
            cambios += 1
            print(f"  {id_global}: {valores['corpus_final']} ({clase})")
        if cambios:
            libro.save(raiz / ruta)  # guardar sin cambios reescribe el xlsx y ensucia el historial de git
    return conteo
