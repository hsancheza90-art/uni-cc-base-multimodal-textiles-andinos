"""Escritura de los workbooks del experimento (consultas T1 y juicios de relevancia).

Cada workbook tiene una hoja de guía, una hoja de trabajo con las columnas que decide el
evaluador a la izquierda (amarillas) y el contexto a la derecha (gris), una hoja de ejemplos de
referencia y una hoja de listas para las validaciones. La lectura usa src/utils/libros.py.
"""

from __future__ import annotations

from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

RELLENO_EDITABLE = PatternFill("solid", fgColor="FFF2CC")
RELLENO_CONTEXTO = PatternFill("solid", fgColor="E7E6E6")
HOJA_GUIA = "guia"
HOJA_EJEMPLOS = "ejemplos"
HOJA_LISTAS = "listas"


def hoja_tabla(libro: Workbook, nombre: str, encabezados: list[str], filas: list[dict[str, str]],
               editables: list[str], anchos: dict[str, int], enlaces: tuple[str, ...] = ()):
    hoja = libro.create_sheet(nombre)
    hoja.append(encabezados)
    for indice, columna in enumerate(encabezados, start=1):
        celda = hoja.cell(row=1, column=indice)
        celda.font = Font(bold=True)
        celda.fill = RELLENO_EDITABLE if columna in editables else RELLENO_CONTEXTO
        celda.alignment = Alignment(wrap_text=True, vertical="top")
        hoja.column_dimensions[get_column_letter(indice)].width = anchos.get(columna, 16)
    for numero, fila in enumerate(filas, start=2):
        for indice, columna in enumerate(encabezados, start=1):
            valor = fila.get(columna, "")
            celda = hoja.cell(row=numero, column=indice, value=valor if valor != "" else None)
            celda.alignment = Alignment(wrap_text=True, vertical="top")
            if valor and columna in enlaces:
                celda.hyperlink = valor
                celda.style = "Hyperlink"
    hoja.freeze_panes = hoja.cell(row=2, column=len(editables) + 1)
    hoja.auto_filter.ref = f"A1:{get_column_letter(len(encabezados))}{len(filas) + 1}"
    return hoja


def escribir_libro(ruta: Path, guia: list[str], hoja: str, encabezados: list[str], filas: list[dict[str, str]],
                   editables: list[str], anchos: dict[str, int], listas: dict[str, list[str]],
                   ejemplos: tuple[list[str], list[dict[str, str]]], enlaces: tuple[str, ...] = ()) -> None:
    """Workbook con guía, hoja de trabajo (listas desplegables en las columnas de `listas`) y ejemplos."""
    libro = Workbook()
    hoja_guia = libro.active
    hoja_guia.title = HOJA_GUIA
    for numero, linea in enumerate(guia, start=1):
        hoja_guia.cell(row=numero, column=1, value=linea)
    hoja_guia["A1"].font = Font(bold=True, size=14)
    hoja_guia.column_dimensions["A"].width = 130

    trabajo = hoja_tabla(libro, hoja, encabezados, filas, editables, anchos, enlaces)
    hoja_listas = libro.create_sheet(HOJA_LISTAS)
    for columna_lista, (nombre, valores) in enumerate(listas.items(), start=1):
        letra_lista = get_column_letter(columna_lista)
        hoja_listas.cell(row=1, column=columna_lista, value=nombre).font = Font(bold=True)
        for fila, valor in enumerate(valores, start=2):
            hoja_listas.cell(row=fila, column=columna_lista, value=valor)
        if filas and nombre in encabezados:
            letra = get_column_letter(encabezados.index(nombre) + 1)
            validacion = DataValidation(type="list", formula1=f"={HOJA_LISTAS}!${letra_lista}$2:${letra_lista}${len(valores) + 1}",
                                        allow_blank=True)
            validacion.error = f"Use un valor de la hoja '{HOJA_LISTAS}'."
            validacion.showErrorMessage = True
            validacion.add(f"{letra}2:{letra}{len(filas) + 1}")
            trabajo.add_data_validation(validacion)

    columnas_ejemplo, filas_ejemplo = ejemplos
    hoja_tabla(libro, HOJA_EJEMPLOS, columnas_ejemplo, filas_ejemplo, [], {c: 40 for c in columnas_ejemplo})
    ruta.parent.mkdir(parents=True, exist_ok=True)
    libro.save(ruta)
