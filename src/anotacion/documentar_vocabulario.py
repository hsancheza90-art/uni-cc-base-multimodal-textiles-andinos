"""Genera la taxonomia de atributos desde config/vocabulario.toml.

Salida: docs/corpus/taxonomia_atributos_met_cma_v1.md (no se edita a mano).
"""

from __future__ import annotations

import argparse
from pathlib import Path

from src.utils.vocabulario import RUTA_VOCABULARIO, Campo, leer_vocabulario

SALIDA = "docs/corpus/taxonomia_atributos_met_cma_v1.md"

FAMILIAS = [
    ("visual", "Familia visual", "Rasgos perceptibles en la imagen digital. Dependen de iluminación, fotografía, conservación y resolución, por lo que deben interpretarse con cautela."),
    ("composicional", "Familia composicional", "Organización del diseño sobre la superficie. Conecta con el modelo combinatorio: composición, simetría, repetición, borde y centro."),
    ("tecnica", "Familia técnica", "Materialidad, técnica y morfología. Parte proviene de los metadatos oficiales y parte se normaliza durante la curación."),
    ("iconografica", "Familia iconográfica", "Motivos observables o registrados. Son descriptores preliminares, no interpretaciones definitivas."),
    ("control", "Estados de control", "Avance de curación y anotación; separan información oficial, anotación manual y revisión pendiente."),
    ("curatorial", "Campos curatoriales y de licencia", "Decisión de curación y condición de uso de cada registro."),
]


def lineas_campo(campo: Campo) -> list[str]:
    atributos = [f"Cuadro {campo.cuadro} de la tesis"]
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
    return lineas + [""]


def generar(vocabulario: dict[str, Campo]) -> list[str]:
    lineas = [
        "# Taxonomía de atributos del corpus MET+CMA v1",
        "",
        f"Documento generado desde `{RUTA_VOCABULARIO.as_posix()}` por `src/anotacion/documentar_vocabulario.py`; "
        "no editar a mano. Para cambiar un valor, editar el vocabulario y ejecutar `python -m src.flujo`.",
        "",
        "La taxonomía sigue los Cuadros 6.3 a 6.8 del avance de tesis. En los datos se guarda el **código** "
        "(minúsculas, sin tildes ni espacios); la **etiqueta** es la forma usada en la tesis, los documentos y las "
        "figuras. Los valores marcados como *extensión del corpus* no figuran en la tesis y se agregaron durante la "
        "curación porque aparecen en los registros.",
        "",
        "Los atributos contextuales (Cuadro 6.7: cultura, periodo, fecha, procedencia, fuente, institución, URL) "
        "provienen de la fuente oficial y no tienen vocabulario cerrado.",
        "",
    ]
    for familia, titulo, descripcion in FAMILIAS:
        campos = [campo for campo in vocabulario.values() if campo.familia == familia]
        if not campos:
            continue
        lineas += [f"## {titulo}", "", descripcion, ""]
        for campo in campos:
            lineas += lineas_campo(campo)
    return lineas


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Genera la taxonomia de atributos desde el vocabulario.")
    parser.add_argument("--root", default=".", help="Raiz del repositorio.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    raiz = Path(parse_args(argv).root).resolve()
    ruta = raiz / SALIDA
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_bytes(("\n".join(generar(leer_vocabulario(raiz))).rstrip() + "\n").encode("utf-8"))
    print(f"Taxonomia: {ruta}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
