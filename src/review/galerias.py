"""Galerías HTML para la revisión visual: utilidades comunes y galerías por fuente.

Uso desde la raíz del repositorio (sin red; las imágenes locales se muestran si existen):

    python -m src.review.galerias --fuente met     # también cma o aic

Escribe una galería por decisión del workbook de revisión de la fuente (principal,
secundario, descartados y revisar) en outputs/review/<fuente>_<decision>_galeria.html.
Las galerías son ayudas de lectura: no se versionan (.gitignore) y las decisiones se
registran solo en los workbooks.

Las demás galerías (bandas de aptitud, validación ciega y revisión con el criterio v2)
usan las mismas utilidades: esc, imagen_relativa, tarjeta y escribir_pagina.
"""

from __future__ import annotations

import argparse
import html
import os
from pathlib import Path

from src.utils.fuentes import DECISIONES, FUENTES
from src.utils.libros import leer_hoja

CARPETA = "outputs/review"
ORDEN_SUGERENCIA = {"principal": 0, "secundario": 1, "descartados": 2}

ESTILO = """
body { font-family: Arial, sans-serif; margin: 24px; background: #f6f6f4; color: #222; }
main { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 16px; }
article { background: #fff; border: 1px solid #ddd; border-radius: 8px; overflow: hidden; padding-bottom: 8px; }
img, .sin { width: 100%; height: 320px; object-fit: contain; background: #eee; display: grid; place-items: center; color: #777; }
article p { margin: 4px 12px; font-size: 13px; line-height: 1.35; }
.t { font-style: italic; color: #555; }
.m { color: #555; }
.p { float: right; background: #1f4e78; color: #fff; border-radius: 999px; padding: 1px 8px; font-weight: bold; }
.e { display: inline-block; background: #e9eef4; color: #1f4e78; border-radius: 999px; padding: 1px 6px; margin: 1px; font-size: 11px; }
.ref { background: #7f6000; color: #fff; }
"""


def esc(valor: object) -> str:
    return html.escape(str(valor or "").strip())


def imagen_relativa(raiz: Path, ruta: str, salida: Path, respaldo: str = "") -> str:
    """Ruta de la imagen local relativa a la galería; si no está en disco, el respaldo (URL)."""
    if ruta and (raiz / ruta).exists():
        return os.path.relpath(raiz / ruta, salida.parent).replace("\\", "/")
    return respaldo


def imagen_evaluacion(raiz: Path, manifiesto: dict[str, dict[str, str]], id_global: str, salida: Path) -> str:
    """Copia de evaluación de un registro (data/images/evaluacion) o, si falta, la URL descargada."""
    registro = manifiesto.get(id_global, {})
    return imagen_relativa(raiz, registro.get("ruta_copia_evaluacion", ""), salida, registro.get("url_descargada", ""))


def etiqueta(texto: str, clase: str = "e") -> str:
    return f'<span class="{clase}">{esc(texto)}</span>' if texto else ""


def parrafo(contenido: str | tuple[str, str]) -> str:
    """Párrafo ya escapado; una tupla (clase, texto) le asigna una clase de estilo."""
    clase, texto = contenido if isinstance(contenido, tuple) else ("", contenido)
    return f'  <p class="{clase}">{texto}</p>' if clase else f"  <p>{texto}</p>"


def tarjeta(imagen: str, enlace: str, alt: str, parrafos: list[str | tuple[str, str]]) -> str:
    """Tarjeta con la imagen enlazada a la ficha del museo."""
    img = f'<img src="{esc(imagen)}" alt="{esc(alt)}" loading="lazy">' if imagen else '<div class="sin">Sin imagen</div>'
    cuerpo = "\n".join(parrafo(p) for p in parrafos)
    return f'<article>\n  <a href="{esc(enlace)}" target="_blank" rel="noopener">{img}</a>\n{cuerpo}\n</article>'


def escribir_pagina(salida: Path, titulo: str, nota: str, secciones: list[tuple[str, list[str]]]) -> Path:
    """Página con una rejilla de tarjetas por sección (sin encabezado si la sección no tiene título)."""
    cuerpo = "\n".join((f"<h2>{esc(nombre)} ({len(tarjetas)})</h2>\n" if nombre else "") + "<main>\n" + "\n".join(tarjetas) + "\n</main>"
                       for nombre, tarjetas in secciones)
    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.write_bytes(f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(titulo)}</title>
<style>{ESTILO}</style>
</head>
<body>
<h1>{esc(titulo)}</h1>
<p>{nota}</p>
{cuerpo}
</body>
</html>
""".encode("utf-8"))
    return salida


# ------------------------------------------------------------------ galerías por fuente

def tarjeta_revision(raiz: Path, fuente: str, fila: dict[str, str], salida: Path) -> str:
    imagen = imagen_relativa(raiz, fila.get("ruta_imagen_local", ""), salida, fila.get("url_imagen", ""))
    motivo = fila.get("motivo_revision") or fila.get("motivo_curacion", "")
    observaciones = fila.get("observaciones_revision", "")
    datos = " · ".join(esc(fila[c]) for c in ("cultura", "fecha_objeto", "tipo_objeto") if fila.get(c))
    return tarjeta(imagen, fila.get("url_objeto", ""), f"{fuente}:{fila['id_fuente']}", [
        f"<b>{fuente}:{esc(fila['id_fuente'])}</b> {etiqueta(fila.get('decision_revision', ''))}",
        ("t", esc(fila.get("titulo_original"))),
        datos,
        f"<b>Sugerencia automática:</b> {esc(fila.get('corpus_actual'))}",
        *([("m", f"<b>Motivo:</b> {esc(motivo)}")] if motivo else []),
        *([("m", esc(observaciones))] if observaciones else []),
    ])


def generar(raiz: Path, fuente: str) -> list[Path]:
    registro = FUENTES[fuente]
    filas = leer_hoja(raiz / registro.workbook, registro.hoja, clave="id_fuente")
    salidas = []
    for decision in DECISIONES:
        grupo = [f for f in filas if f.get("corpus_final") == decision]
        if decision == "revisar":
            grupo.sort(key=lambda f: ORDEN_SUGERENCIA.get(f.get("corpus_actual", ""), 9))  # revisar por bloques
        salida = raiz / CARPETA / f"{fuente.lower()}_{decision}_galeria.html"
        tarjetas = [tarjeta_revision(raiz, fuente, f, salida) for f in grupo]
        nota = (f"Registros con corpus_final = {decision} en <code>{esc(registro.workbook)}</code>. "
                "La imagen enlaza a la ficha del museo. Las decisiones se registran en el workbook.")
        salidas.append(escribir_pagina(salida, f"{fuente}: {decision} ({len(grupo)} registros)", nota, [("", tarjetas)]))
        print(f"{decision}: {len(grupo)} registros -> {salida}")
    return salidas


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Galerías de revisión visual por fuente, desde el workbook.")
    parser.add_argument("--root", default=".", help="Raíz del repositorio.")
    parser.add_argument("--fuente", choices=[f.lower() for f in FUENTES], required=True, help="Fuente de las galerías.")
    args = parser.parse_args(argv)
    generar(Path(args.root).resolve(), args.fuente.upper())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
