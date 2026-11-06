"""Workbook y galería de los pares candidatos a duplicado (fuera del flujo: escribe un insumo curado).

Uso desde la raíz del repositorio (después de python -m src.flujo):

    python -m src.grupos.workbook
    python -m src.grupos.workbook --fecha 2026-11-06

Crea o actualiza data/metadata/grupos_revision_v2.xlsx con un par por fila, desde
data/metadata/grupos_candidatos_v2.csv: a la izquierda las columnas que decide el revisor
(decision, relacion, motivo, revisor, fecha_revision) y a la derecha el contexto de las dos
piezas. Si el workbook existe, conserva todas las decisiones por par, incluidas las de pares que
ya no son candidatos (con candidato = no). Un par nuevo con imagen idéntica entra como unir con
revisor = auto y la fecha de --fecha, según [decisiones] de config/grupos.toml; el revisor
puede corregirlo. Nunca cambia una decisión ya escrita.

También escribe la galería local outputs/review/grupos_v2_galeria.html (no se versiona), con las
dos imágenes de cada par lado a lado.
"""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

from src.grupos.grupos import HOJA_PARES, SALIDA_CANDIDATOS, WORKBOOK_GRUPOS, piezas_v2
from src.imagenes.descargar_evaluacion import MANIFIESTO_EVALUACION
from src.review.galerias import CARPETA, esc, escribir_pagina, etiqueta, imagen_evaluacion, tarjeta
from src.utils.archivos import indexar, leer_csv
from src.utils.config import CONFIG_GRUPOS, leer_config_grupos
from src.utils.libros import leer_hoja

GALERIA = Path(CARPETA) / "grupos_v2_galeria.html"
HOJA_GUIA = "guia"
HOJA_LISTAS = "listas"
DECISION = ["decision", "relacion", "motivo", "revisor", "fecha_revision"]
PIEZA = ["titulo_original", "numero_acceso", "cultura", "fecha_objeto"]
CONTEXTO = (["par", "candidato", "senales", "grupo_imagen_duplicada", "distancia_dhash", "coseno_m2", "inventario_base"]
            + [f"{c}_{lado}" for lado in ("a", "b") for c in ["id", "fuente", *PIEZA, "imagen", "url_objeto"]])
ANCHOS = {"par": 26, "senales": 22, "motivo": 40, "titulo_original_a": 30, "titulo_original_b": 30,
          "imagen_a": 14, "imagen_b": 14, "url_objeto_a": 14, "url_objeto_b": 14}
RELLENO_DECISION = PatternFill("solid", fgColor="FFF2CC")
RELLENO_CONTEXTO = PatternFill("solid", fgColor="E7E6E6")

GUIA = [
    "Revision de pares candidatos a duplicado (principal v2)",
    "",
    "Cada fila es un par de piezas que alguna senal propone como el mismo objeto. Se decide si se unen en un grupo:",
    "el grupo es la unidad de particion del protocolo experimental (dos piezas del mismo grupo nunca quedan una en",
    "desarrollo y otra en prueba).",
    "",
    "decision: unir (mismo objeto: misma foto, vistas, partes o fragmentos), separar (objetos distintos) o",
    "  no_seguro (no se puede decidir; cuenta como unir).",
    "relacion (opcional al unir): misma_imagen, vistas_mismo_objeto, partes_mismo_objeto, fragmentos_misma_pieza u otra.",
    "motivo: lo que se ve o lo que dice la ficha. revisor: nombre o iniciales. fecha_revision: AAAA-MM-DD.",
    "",
    "Los pares con imagen identica entran como unir con revisor = auto; se pueden corregir.",
    "Senales: imagen_identica, inventario (mismo numero base con sufijo de parte), descripcion (ficha identica),",
    "  dhash (foto casi identica) y m2 (OpenCLIP casi identico). Las imagenes se ven en",
    f"  {GALERIA.as_posix()} (python -m src.grupos.workbook la regenera).",
    "",
    f"Parametros: {CONFIG_GRUPOS.as_posix()}. Despues de decidir: python -m src.flujo aplica las decisiones.",
]


def filas_workbook(raiz: Path, fecha: str) -> list[dict[str, str]]:
    """Filas del workbook: candidatos actuales con las decisiones previas, y pares decididos que ya no son candidatos."""
    config = leer_config_grupos(raiz)["decisiones"]
    candidatos = leer_csv(raiz / SALIDA_CANDIDATOS)
    principal = indexar(piezas_v2(raiz), "id_global")
    manifiesto = indexar(leer_csv(raiz / MANIFIESTO_EVALUACION), "id_global")
    ruta = raiz / WORKBOOK_GRUPOS
    previas = {f["par"]: f for f in leer_hoja(ruta, HOJA_PARES, clave="par")} if ruta.exists() else {}

    def contexto(id_global: str, lado: str) -> dict[str, str]:
        pieza = principal.get(id_global, {})
        copia = manifiesto.get(id_global, {}).get("ruta_copia_evaluacion", "")
        return {f"id_{lado}": id_global, f"fuente_{lado}": pieza.get("fuente", ""),
                **{f"{c}_{lado}": pieza.get(c, "") for c in PIEZA},
                f"imagen_{lado}": "../" + copia.removeprefix("data/") if copia else "",
                f"url_objeto_{lado}": pieza.get("url_objeto", "")}

    filas = []
    for par in candidatos:
        fila = {c: par.get(c, "") for c in ("par", "senales", "grupo_imagen_duplicada", "distancia_dhash", "coseno_m2",
                                              "inventario_base")}
        fila["candidato"] = "si"
        fila |= contexto(par["id_a"], "a") | contexto(par["id_b"], "b")
        previa = previas.get(par["par"])
        if previa and any(previa.get(c) for c in DECISION):
            fila |= {c: previa.get(c, "") for c in DECISION}
        elif par["decision_sugerida"] == "unir" and config.get("auto_unir_imagen_identica"):
            fila |= {"decision": "unir", "relacion": "misma_imagen", "revisor": "auto", "fecha_revision": fecha,
                     "motivo": "Imagen identica (misma copia, misma imagen original o mismo grupo_imagen_duplicada)."}
        filas.append(fila)
    vigentes = {f["par"] for f in filas}
    for clave, previa in previas.items():
        if clave not in vigentes and any(previa.get(c) for c in DECISION):
            a, _, b = clave.partition(" | ")
            filas.append({"par": clave, "candidato": "no", **contexto(a, "a"), **contexto(b, "b"),
                          **{c: previa.get(c, "") for c in DECISION}})
    return filas


def escribir_workbook(ruta: Path, filas: list[dict[str, str]], codigos: list[str], relaciones: list[str]) -> None:
    libro = Workbook()
    guia = libro.active
    guia.title = HOJA_GUIA
    for numero, linea in enumerate(GUIA, start=1):
        guia.cell(row=numero, column=1, value=linea)
    guia["A1"].font = Font(bold=True, size=14)
    guia.column_dimensions["A"].width = 120

    hoja = libro.create_sheet(HOJA_PARES)
    encabezados = DECISION + CONTEXTO
    hoja.append(encabezados)
    for indice, nombre in enumerate(encabezados, start=1):
        celda = hoja.cell(row=1, column=indice)
        celda.font = Font(bold=True)
        celda.fill = RELLENO_DECISION if nombre in DECISION else RELLENO_CONTEXTO
        celda.alignment = Alignment(wrap_text=True, vertical="top")
        hoja.column_dimensions[get_column_letter(indice)].width = ANCHOS.get(nombre, 16)
    for numero, fila in enumerate(filas, start=2):
        for indice, nombre in enumerate(encabezados, start=1):
            valor = fila.get(nombre, "")
            celda = hoja.cell(row=numero, column=indice, value=valor or None)
            if valor and (nombre.startswith("imagen_") or nombre.startswith("url_objeto_")):
                celda.hyperlink = valor
                celda.style = "Hyperlink"

    listas = libro.create_sheet(HOJA_LISTAS)
    for numero, codigo in enumerate(codigos, start=1):
        listas.cell(row=numero, column=1, value=codigo)
    for numero, relacion in enumerate(relaciones, start=1):
        listas.cell(row=numero, column=2, value=relacion)
    if filas:
        for nombre, columna, cantidad in (("decision", "A", len(codigos)), ("relacion", "B", len(relaciones))):
            letra = get_column_letter(encabezados.index(nombre) + 1)
            validacion = DataValidation(type="list", formula1=f"={HOJA_LISTAS}!${columna}$1:${columna}${cantidad}",
                                        allow_blank=True)
            validacion.error = f"Use un codigo de la hoja '{HOJA_LISTAS}'."
            validacion.showErrorMessage = True
            validacion.add(f"{letra}2:{letra}{len(filas) + 1}")
            hoja.add_data_validation(validacion)
    hoja.freeze_panes = hoja.cell(row=2, column=len(DECISION) + 2)
    hoja.auto_filter.ref = f"A1:{get_column_letter(len(encabezados))}{len(filas) + 1}"
    ruta.parent.mkdir(parents=True, exist_ok=True)
    libro.save(ruta)


def escribir_galeria(raiz: Path, filas: list[dict[str, str]]) -> Path:
    salida = raiz / GALERIA
    manifiesto = indexar(leer_csv(raiz / MANIFIESTO_EVALUACION), "id_global")
    secciones = []
    for fila in filas:
        tarjetas = []
        for lado in ("a", "b"):
            id_global = fila[f"id_{lado}"]
            parrafos = [f"<b>{esc(id_global)}</b> {esc(fila.get(f'numero_acceso_{lado}', ''))}",
                        ("t", esc(fila.get(f"titulo_original_{lado}", ""))),
                        ("m", esc(fila.get(f"cultura_{lado}", "")))]
            tarjetas.append(tarjeta(imagen_evaluacion(raiz, manifiesto, id_global, salida),
                                    fila.get(f"url_objeto_{lado}", ""), id_global, parrafos))
        senales = " ".join(etiqueta(s) for s in fila.get("senales", "").split("; ") if s)
        decision = f" [{fila['decision']}]" if fila.get("decision") else ""
        secciones.append((f"{fila['par']}{decision}", tarjetas + [f"<article><p>{senales}</p></article>"]))
    return escribir_pagina(salida, "Pares candidatos a duplicado (principal v2)",
                           f"Decisiones en <code>{esc(WORKBOOK_GRUPOS.as_posix())}</code>. Galeria local, no se versiona.",
                           secciones)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Workbook y galeria de los pares candidatos a duplicado (grupos v2).")
    parser.add_argument("--root", default=".", help="Raiz del repositorio.")
    parser.add_argument("--fecha", default=date.today().isoformat(), help="Fecha de las decisiones automaticas.")
    args = parser.parse_args(argv)
    raiz = Path(args.root).resolve()
    if not (raiz / SALIDA_CANDIDATOS).exists():
        print(f"No existe {SALIDA_CANDIDATOS}: ejecute antes python -m src.flujo.")
        return 1
    config = leer_config_grupos(raiz)["decisiones"]
    filas = filas_workbook(raiz, args.fecha)
    try:
        escribir_workbook(raiz / WORKBOOK_GRUPOS, filas, config["unir"] + config["separar"], config["relaciones"])
    except PermissionError:
        print(f"No se pudo escribir {WORKBOOK_GRUPOS}: cierre el archivo en Excel y vuelva a intentarlo.")
        return 1
    galeria = escribir_galeria(raiz, filas)
    decididos = sum(1 for f in filas if f.get("decision"))
    print(f"Workbook de grupos: {raiz / WORKBOOK_GRUPOS} | pares: {len(filas)}, con decision: {decididos}")
    print(f"Galeria: {galeria}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
