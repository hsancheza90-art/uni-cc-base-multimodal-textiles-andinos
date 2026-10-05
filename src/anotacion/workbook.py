"""Crea o actualiza el workbook de anotacion manual del corpus consolidado.

Uso desde la raiz del repositorio (despues de `python -m src.flujo`):

    python -m src.anotacion.workbook

El workbook data/metadata/anotacion_met_cma_v1.xlsx tiene una fila por registro
del consolidado, con columnas de contexto (solo lectura) y columnas de anotacion
con listas desplegables del vocabulario controlado. Si el workbook ya existe, se
regenera conservando todo lo anotado por id_global; las anotaciones de registros
que ya no estan en el consolidado pasan a la hoja "fuera_del_corpus".
"""

from __future__ import annotations

import argparse
import csv
from datetime import date, datetime
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

from src.consolidado.construir_consolidado import SALIDA_CONSOLIDADO
from src.consolidado.esquema import ATRIBUTOS_ANOTACION, COLUMNAS_ANOTACIONES, CORRECCIONES
from src.utils.vocabulario import Campo, leer_vocabulario

WORKBOOK = Path("data/metadata/anotacion_met_cma_v1.xlsx")
HOJA_ANOTACION = "anotacion"
HOJA_VOCABULARIO = "vocabulario"
HOJA_GUIA = "guia"
HOJA_HUERFANAS = "fuera_del_corpus"

CONTEXTO = [
    "id_global",
    "fuente",
    "decision_curacion_final",
    "grupo_imagen_duplicada",
    "titulo_original",
    "titulo_es_sugerido",
    "cultura",
    "fecha_objeto",
    "tipo_objeto",
    "tipo_superficie",
    "material_normalizado",
    "tecnica_normalizada",
    "estado_imagen",
    "url_objeto",
    "url_imagen",
    "imagen_local",
]
COLUMNAS_EDITABLES = COLUMNAS_ANOTACIONES[1:]

# Columna de anotacion -> campo del vocabulario que define sus valores.
CAMPO_DE_COLUMNA: dict[str, str] = {
    **{campo: campo for campo in ATRIBUTOS_ANOTACION},
    **CORRECCIONES,
    "estado_anotacion": "estado_anotacion",
}

RELLENO_CONTEXTO = PatternFill("solid", fgColor="E7E6E6")
RELLENO_ANOTACION = PatternFill("solid", fgColor="FFF2CC")

GUIA = [
    "Anotacion manual del corpus consolidado MET+CMA",
    "",
    "1. Las columnas grises son contexto: no se editan; se regeneran desde el consolidado.",
    "2. Las columnas amarillas se anotan con los codigos de la hoja 'vocabulario' (listas desplegables).",
    "3. Campos multiples (colores, motivos, material_corregido, tecnica_corregida): varios codigos separados por '; '.",
    "4. Las columnas *_corregido solo se llenan para corregir el valor actual; vacias, se conserva el actual.",
    "5. estado_anotacion: si queda vacio y hay anotaciones, se registra 'anotado_manual' (o 'corregido' si hay correcciones).",
    "6. fecha_anotacion con formato AAAA-MM-DD.",
    "7. Despues de anotar: python -m src.flujo valida el workbook y actualiza el consolidado.",
    "",
    "Guia completa: docs/corpus/guia_anotacion_met_cma_v1.md",
]


def leer_consolidado(raiz: Path) -> list[dict[str, str]]:
    with (raiz / SALIDA_CONSOLIDADO).open(newline="", encoding="utf-8-sig") as archivo:
        return list(csv.DictReader(archivo))


def texto_celda(valor: object) -> str:
    """Valor de celda como texto; las fechas de Excel se escriben AAAA-MM-DD."""
    if valor is None:
        return ""
    if isinstance(valor, datetime):
        return valor.date().isoformat()
    if isinstance(valor, date):
        return valor.isoformat()
    return str(valor).strip()


def leer_anotaciones_existentes(ruta: Path) -> dict[str, dict[str, str]]:
    """Anotaciones del workbook actual (hoja principal y fuera_del_corpus) por id_global."""
    if not ruta.exists():
        return {}
    libro = load_workbook(ruta, data_only=True)
    anotaciones: dict[str, dict[str, str]] = {}
    for nombre in (HOJA_ANOTACION, HOJA_HUERFANAS):
        if nombre not in libro.sheetnames:
            continue
        hoja = libro[nombre]
        encabezados = [texto_celda(celda.value) for celda in hoja[1]]
        for fila in hoja.iter_rows(min_row=2, values_only=True):
            datos = {encabezados[i]: texto_celda(v) for i, v in enumerate(fila) if i < len(encabezados)}
            if datos.get("id_global") and any(datos.get(c) for c in COLUMNAS_EDITABLES):
                anotaciones[datos["id_global"]] = {c: datos.get(c, "") for c in COLUMNAS_EDITABLES}
    return anotaciones


def escribir_hoja_vocabulario(libro: Workbook, vocabulario: dict[str, Campo]) -> dict[str, str]:
    """Una pareja de columnas (codigo, etiqueta) por campo; devuelve el rango de codigos de cada campo."""
    hoja = libro.create_sheet(HOJA_VOCABULARIO)
    rangos: dict[str, str] = {}
    columna = 1
    for campo in vocabulario.values():
        if not campo.anotable:
            continue
        letra_codigo, letra_etiqueta = get_column_letter(columna), get_column_letter(columna + 1)
        hoja[f"{letra_codigo}1"] = campo.nombre
        hoja[f"{letra_etiqueta}1"] = "etiqueta"
        hoja[f"{letra_codigo}1"].font = hoja[f"{letra_etiqueta}1"].font = Font(bold=True)
        for fila, (codigo, etiqueta) in enumerate(campo.etiquetas.items(), start=2):
            hoja[f"{letra_codigo}{fila}"] = codigo
            hoja[f"{letra_etiqueta}{fila}"] = etiqueta
        rangos[campo.nombre] = f"{HOJA_VOCABULARIO}!${letra_codigo}$2:${letra_codigo}${len(campo.etiquetas) + 1}"
        hoja.column_dimensions[letra_codigo].width = 28
        hoja.column_dimensions[letra_etiqueta].width = 28
        columna += 3
    return rangos


def agregar_validaciones(hoja, vocabulario: dict[str, Campo], rangos: dict[str, str], filas: int) -> None:
    encabezados = [celda.value for celda in hoja[1]]
    for columna, nombre_campo in CAMPO_DE_COLUMNA.items():
        campo = vocabulario[nombre_campo]
        letra = get_column_letter(encabezados.index(columna) + 1)
        rango_celdas = f"{letra}2:{letra}{filas + 1}"
        if campo.multiple:
            validacion = DataValidation(allow_blank=True)
            validacion.promptTitle = columna[:32]
            validacion.prompt = ("Codigos separados por '; ': " + ", ".join(campo.codigos))[:255]
            validacion.showInputMessage = True
        else:
            validacion = DataValidation(type="list", formula1=f"={rangos[nombre_campo]}", allow_blank=True)
            validacion.error = f"Use un codigo de la hoja '{HOJA_VOCABULARIO}'."
            validacion.showErrorMessage = True
        validacion.add(rango_celdas)
        hoja.add_data_validation(validacion)


def escribir_enlace(celda, url: str) -> None:
    if url:
        celda.value = url
        celda.hyperlink = url
        celda.style = "Hyperlink"


def construir_libro(
    registros: list[dict[str, str]],
    anotaciones: dict[str, dict[str, str]],
    vocabulario: dict[str, Campo],
) -> Workbook:
    libro = Workbook()
    hoja = libro.active
    hoja.title = HOJA_ANOTACION
    encabezados = CONTEXTO + COLUMNAS_EDITABLES
    hoja.append(encabezados)
    for indice, nombre in enumerate(encabezados, start=1):
        celda = hoja.cell(row=1, column=indice)
        celda.font = Font(bold=True)
        celda.fill = RELLENO_CONTEXTO if nombre in CONTEXTO else RELLENO_ANOTACION
        celda.alignment = Alignment(wrap_text=True, vertical="top")

    columna_de = {nombre: indice for indice, nombre in enumerate(encabezados, start=1)}
    for numero, registro in enumerate(registros, start=2):
        for nombre in CONTEXTO[:-3]:
            hoja.cell(row=numero, column=columna_de[nombre], value=registro.get(nombre, ""))
        escribir_enlace(hoja.cell(row=numero, column=columna_de["url_objeto"]), registro["url_objeto"])
        escribir_enlace(hoja.cell(row=numero, column=columna_de["url_imagen"]), registro["url_imagen"])
        if registro.get("ruta_imagen_local"):
            # El workbook vive en data/metadata; la imagen local, en data/images.
            relativa = "../" + registro["ruta_imagen_local"].removeprefix("data/")
            escribir_enlace(hoja.cell(row=numero, column=columna_de["imagen_local"]), relativa)
        previo = anotaciones.get(registro["id_global"], {})
        for nombre in COLUMNAS_EDITABLES:
            if previo.get(nombre):
                hoja.cell(row=numero, column=columna_de[nombre], value=previo[nombre])

    anchos = {"titulo_original": 34, "titulo_es_sugerido": 22, "cultura": 24, "url_objeto": 22, "url_imagen": 22}
    for nombre, indice in columna_de.items():
        hoja.column_dimensions[get_column_letter(indice)].width = anchos.get(nombre, 18)
    hoja.freeze_panes = "C2"
    hoja.auto_filter.ref = f"A1:{get_column_letter(len(encabezados))}{len(registros) + 1}"

    rangos = escribir_hoja_vocabulario(libro, vocabulario)
    agregar_validaciones(hoja, vocabulario, rangos, len(registros))

    guia = libro.create_sheet(HOJA_GUIA, 0)
    for numero, linea in enumerate(GUIA, start=1):
        guia.cell(row=numero, column=1, value=linea)
    guia["A1"].font = Font(bold=True, size=14)
    guia.column_dimensions["A"].width = 120

    ids_actuales = {registro["id_global"] for registro in registros}
    huerfanas = {id_: datos for id_, datos in anotaciones.items() if id_ not in ids_actuales}
    if huerfanas:
        hoja_h = libro.create_sheet(HOJA_HUERFANAS)
        hoja_h.append(["id_global"] + COLUMNAS_EDITABLES)
        for id_global, datos in sorted(huerfanas.items()):
            hoja_h.append([id_global] + [datos.get(c, "") for c in COLUMNAS_EDITABLES])
    return libro


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Crea o actualiza el workbook de anotacion manual.")
    parser.add_argument("--root", default=".", help="Raiz del repositorio.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    raiz = Path(parse_args(argv).root).resolve()
    ruta = raiz / WORKBOOK
    anotaciones = leer_anotaciones_existentes(ruta)
    registros = leer_consolidado(raiz)
    libro = construir_libro(registros, anotaciones, leer_vocabulario(raiz))
    ruta.parent.mkdir(parents=True, exist_ok=True)
    try:
        libro.save(ruta)
    except PermissionError:
        print(f"No se pudo escribir {ruta}: cierre el archivo en Excel y vuelva a intentarlo.")
        return 1
    conservadas = sum(1 for id_ in anotaciones if id_ in {r["id_global"] for r in registros})
    print(f"Workbook de anotacion: {ruta}")
    print(f"Registros: {len(registros)} | anotaciones conservadas: {conservadas} | fuera del corpus: {len(anotaciones) - conservadas}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
