"""Genera las taxonomias de atributos desde el vocabulario controlado.

Salidas (no se editan a mano):
- docs/corpus/taxonomia_atributos_v2.md, desde el vocabulario vigente (config/vocabulario.toml).
- docs/corpus/taxonomia_atributos_met_cma_v1.md, desde la copia congelada de la v1
  (data/metadata/v1_congelado/vocabulario.toml). Conserva el texto con que se publico en
  corpus-met-cma-v1.2, cuando la copia congelada aun era config/vocabulario.toml.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from src.utils.archivos import escribir_texto
from src.utils.vocabulario import RUTA_VOCABULARIO, RUTA_VOCABULARIO_V1, Campo, leer_vocabulario

SALIDA = "docs/corpus/taxonomia_atributos_v2.md"
SALIDA_V1 = "docs/corpus/taxonomia_atributos_met_cma_v1.md"

FAMILIAS = [
    ("visual", "Familia visual", "Rasgos perceptibles en la imagen digital. Dependen de iluminación, fotografía, conservación y resolución, por lo que deben interpretarse con cautela."),
    ("composicional", "Familia composicional", "Organización del diseño sobre la superficie. Conecta con el modelo combinatorio: composición, simetría, repetición, borde y centro."),
    ("tecnica", "Familia técnica", "Materialidad, técnica y morfología. Parte proviene de los metadatos oficiales y parte se normaliza durante la curación."),
    ("iconografica", "Familia iconográfica", "Motivos observables o registrados. Son descriptores preliminares, no interpretaciones definitivas."),
    ("control", "Estados de control", "Avance de curación y anotación; separan información oficial, anotación manual y revisión pendiente."),
    ("curatorial", "Campos curatoriales y de licencia", "Decisión de curación y condición de uso de cada registro."),
]

INTRODUCCION = [
    "La taxonomía sigue los Cuadros 6.3 a 6.8 del avance de tesis. En los datos se guarda el **código** "
    "(minúsculas, sin tildes ni espacios); la **etiqueta** es la forma usada en la tesis, los documentos y las "
    "figuras. Los valores marcados como *extensión del corpus* no figuran en la tesis y se agregaron durante la "
    "curación porque aparecen en los registros.",
    "",
    "Los atributos contextuales (Cuadro 6.7: cultura, periodo, fecha, procedencia, fuente, institución, URL) "
    "provienen de la fuente oficial y no tienen vocabulario cerrado.",
    "",
]


def lineas_campo(campo: Campo) -> list[str]:
    atributos = [f"Cuadro {campo.cuadro} de la tesis" if campo.cuadro else "no figura en la tesis"]
    if campo.secuencia:
        atributos.append("secuencia ordenada de valores separados por ` > `")
    else:
        atributos.append("admite varios valores separados por `; `" if campo.multiple else "un solo valor")
    atributos.append("se registra en la anotación manual" if campo.anotable else "lo asigna el flujo")
    lineas = [
        f"### `{campo.nombre}`",
        "",
        f"{campo.descripcion.rstrip('.')} ({'; '.join(atributos)}).",
        "",
        "| Código | Etiqueta | Origen |",
        "|---|---|---|",
    ]
    for codigo, etiqueta in campo.etiquetas.items():
        origen = "extensión del corpus" if codigo in campo.extensiones else "tesis"
        lineas.append(f"| `{codigo}` | {etiqueta} | {origen} |")
    for codigo, etiqueta in campo.estados.items():
        lineas.append(f"| `{codigo}` | {etiqueta} | estado de anotación |")
    return lineas + [""]


def generar(vocabulario: dict[str, Campo], encabezado: list[str]) -> list[str]:
    lineas = list(encabezado) + INTRODUCCION
    for familia, titulo, descripcion in FAMILIAS:
        campos = [campo for campo in vocabulario.values() if campo.familia == familia]
        if not campos:
            continue
        lineas += [f"## {titulo}", "", descripcion, ""]
        for campo in campos:
            lineas += lineas_campo(campo)
    while lineas and not lineas[-1]:
        lineas.pop()  # lineas_campo deja una linea en blanco tras cada seccion
    return lineas


ENCABEZADO_V2 = [
    "# Taxonomía de atributos del corpus v2 (MET, CMA y AIC)",
    "",
    f"Documento generado desde `{RUTA_VOCABULARIO.as_posix()}` por `src/anotacion/documentar_vocabulario.py`; "
    "no editar a mano. Para cambiar un valor, editar el vocabulario y ejecutar `python -m src.flujo`.",
    "",
    "Es el vocabulario vigente, el que valida la anotación v2. La serie v1 conserva el suyo en "
    f"`taxonomia_atributos_met_cma_v1.md`, generado desde la copia congelada `{RUTA_VOCABULARIO_V1.as_posix()}`.",
    "",
    "En la anotación v2, un atributo sin valor registra su **estado de anotación**, solo en la celda: `ausente` (la "
    "superficie pertinente se ve y el rasgo no está), `no_observable` (la superficie no se ve) o `desconocido` (se ve, "
    "pero el anotador no puede decidir). Cada atributo lista los estados que admite; una celda vacía significa «no "
    "anotado». Procedimiento: `docs/protocolo_anotacion_v2.md`.",
    "",
]

# Texto publicado en corpus-met-cma-v1.2: en ese momento la copia congelada era config/vocabulario.toml.
ENCABEZADO_V1 = [
    "# Taxonomía de atributos del corpus MET+CMA v1",
    "",
    f"Documento generado desde `{RUTA_VOCABULARIO.as_posix()}` por `src/anotacion/documentar_vocabulario.py`; "
    "no editar a mano. Para cambiar un valor, editar el vocabulario y ejecutar `python -m src.flujo`.",
    "",
]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Genera las taxonomias de atributos desde el vocabulario.")
    parser.add_argument("--root", default=".", help="Raiz del repositorio.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    raiz = Path(parse_args(argv).root).resolve()
    for salida, ruta_vocabulario, encabezado in (
        (SALIDA, RUTA_VOCABULARIO, ENCABEZADO_V2),
        (SALIDA_V1, RUTA_VOCABULARIO_V1, ENCABEZADO_V1),
    ):
        ruta = raiz / salida
        escribir_texto(ruta, generar(leer_vocabulario(raiz, ruta_vocabulario), encabezado))
        print(f"Taxonomia: {ruta}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
