from __future__ import annotations

import argparse
import html
import os
from pathlib import Path

from src.utils.archivos import leer_csv

ENTRADAS_BASE = [
    ("principal", "data/metadata/met_corpus_principal_v2.csv", "outputs/review/met_corpus_principal_v2_galeria.html"),
    ("secundario", "data/metadata/met_corpus_secundario_v2.csv", "outputs/review/met_corpus_secundario_v2_galeria.html"),
    ("descartados", "data/metadata/met_descartados_v2.csv", "outputs/review/met_descartados_v2_galeria.html"),
]

ENTRADAS_REVISADAS = [
    ("principal", "data/metadata/met_corpus_principal_v2_revisado.csv", "outputs/review/met_corpus_principal_v2_revisado_galeria.html"),
    ("secundario", "data/metadata/met_corpus_secundario_v2_revisado.csv", "outputs/review/met_corpus_secundario_v2_revisado_galeria.html"),
    ("descartados", "data/metadata/met_descartados_v2_revisado.csv", "outputs/review/met_descartados_v2_revisado_galeria.html"),
    ("pendientes", "data/metadata/met_pendientes_revision_v2.csv", "outputs/review/met_pendientes_revision_v2_galeria.html"),
]

ENTRADAS_AIC = [
    ("pendientes", "data/metadata/aic_pendientes_revision_v2.csv", "outputs/review/aic_pendientes_revision_v2_galeria.html"),
    ("principal", "data/metadata/aic_corpus_principal_v2_revisado.csv", "outputs/review/aic_corpus_principal_v2_revisado_galeria.html"),
    ("secundario", "data/metadata/aic_corpus_secundario_v2_revisado.csv", "outputs/review/aic_corpus_secundario_v2_revisado_galeria.html"),
    ("descartados", "data/metadata/aic_descartados_v2_revisado.csv", "outputs/review/aic_descartados_v2_revisado_galeria.html"),
]

ORDEN_SUGERENCIA = {"principal": 0, "secundario": 1, "descartados": 2}


def esc(valor: object) -> str:
    return html.escape(str(valor or "").strip())


def obtener_imagen(fila: dict[str, str], raiz: Path, salida_html: Path) -> str:
    ruta_local = (fila.get("ruta_imagen_local") or "").strip()
    url_imagen = (fila.get("url_imagen") or "").strip()

    if ruta_local:
        ruta_absoluta = raiz / ruta_local
        if ruta_absoluta.exists():
            relativa = os.path.relpath(ruta_absoluta, salida_html.parent)
            return relativa.replace("\\", "/")

    return url_imagen


def construir_tarjeta(fila: dict[str, str], raiz: Path, salida_html: Path, institucion: str = "MET") -> str:
    id_fuente = esc(fila.get("id_fuente"))
    corpus_actual = esc(fila.get("corpus_actual"))
    corpus_final = esc(fila.get("corpus_final"))
    decision = esc(fila.get("decision_revision"))
    titulo = esc(fila.get("titulo_es_sugerido") or fila.get("titulo_original") or "Sin titulo")
    titulo_original = esc(fila.get("titulo_original"))
    cultura = esc(fila.get("cultura"))
    fecha = esc(fila.get("fecha_objeto"))
    procedencia = esc(fila.get("procedencia"))
    tipo = esc(fila.get("tipo_objeto"))
    superficie = esc(fila.get("tipo_superficie"))
    material = esc(fila.get("material"))
    motivo = esc(fila.get("motivo_revision") or fila.get("motivo_curacion"))
    observaciones = esc(fila.get("observaciones_revision"))
    url_objeto = esc(fila.get("url_objeto"))

    imagen_src = esc(obtener_imagen(fila, raiz, salida_html))
    imagen = (
        f'<img src="{imagen_src}" alt="{titulo}" loading="lazy">'
        if imagen_src
        else '<div class="sin-imagen">Sin imagen</div>'
    )

    return f"""
    <article class="card">
      <a class="imagen" href="{url_objeto}" target="_blank" rel="noopener noreferrer">
        {imagen}
      </a>
      <div class="body">
        <div class="badges">
          <span>{corpus_final}</span>
          <span>{decision}</span>
        </div>
        <h2>{titulo}</h2>
        <p class="subtitulo">{titulo_original}</p>
        <p><strong>ID {institucion}:</strong> {id_fuente}</p>
        <p><strong>Cultura:</strong> {cultura}</p>
        <p><strong>Fecha:</strong> {fecha}</p>
        <p><strong>Procedencia:</strong> {procedencia}</p>
        <p><strong>Tipo:</strong> {tipo}</p>
        <p><strong>Superficie:</strong> {superficie}</p>
        <p><strong>Material:</strong> {material}</p>
        <p><strong>Corpus actual:</strong> {corpus_actual}</p>
        <p class="motivo"><strong>Motivo:</strong> {motivo}</p>
        <p class="observaciones"><strong>Observaciones:</strong> {observaciones}</p>
        <a class="link" href="{url_objeto}" target="_blank" rel="noopener noreferrer">Ver ficha institucional {institucion}</a>
      </div>
    </article>
    """


def construir_html(
    nombre: str,
    filas: list[dict[str, str]],
    raiz: Path,
    salida_html: Path,
    revisado: bool,
    institucion: str = "MET",
) -> str:
    tarjetas = "\n".join(construir_tarjeta(fila, raiz, salida_html, institucion) for fila in filas)
    titulo = f"Galeria {institucion} v2 revisada - {nombre}" if revisado else f"Galeria {institucion} v2 base - {nombre}"

    return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>{esc(titulo)}</title>
  <style>
    body {{
      font-family: Arial, sans-serif;
      margin: 24px;
      background: #f6f6f4;
      color: #222;
    }}
    header {{
      margin-bottom: 20px;
      max-width: 1100px;
    }}
    h1 {{
      margin: 0 0 8px;
      font-size: 28px;
    }}
    .nota {{
      color: #555;
      line-height: 1.45;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 18px;
    }}
    .card {{
      background: white;
      border: 1px solid #ddd;
      border-radius: 8px;
      overflow: hidden;
    }}
    .imagen {{
      display: block;
      background: #eee;
      height: 280px;
    }}
    img {{
      width: 100%;
      height: 280px;
      object-fit: contain;
      background: #eee;
    }}
    .sin-imagen {{
      height: 280px;
      display: grid;
      place-items: center;
      color: #777;
      background: #eee;
    }}
    .body {{
      padding: 14px;
    }}
    .badges {{
      display: flex;
      gap: 6px;
      flex-wrap: wrap;
      margin-bottom: 10px;
    }}
    .badges span {{
      background: #e9eef4;
      color: #1f4e78;
      border-radius: 999px;
      padding: 4px 8px;
      font-size: 12px;
      font-weight: bold;
    }}
    h2 {{
      font-size: 17px;
      margin: 0 0 6px;
    }}
    .subtitulo {{
      color: #666;
      font-style: italic;
    }}
    p {{
      margin: 6px 0;
      font-size: 14px;
      line-height: 1.35;
    }}
    .motivo,
    .observaciones {{
      color: #444;
    }}
    .link {{
      display: inline-block;
      margin-top: 10px;
      color: #0645ad;
    }}
  </style>
</head>
<body>
  <header>
    <h1>{esc(titulo)}</h1>
    <p class="nota">Total de registros: {len(filas)}. Esta galeria se genera desde los CSV {'revisados' if revisado else 'base'} de {institucion} v2.</p>
  </header>
  <main class="grid">
    {tarjetas}
  </main>
</body>
</html>
"""


def generar_galerias(raiz: Path, revisado: bool, fuente: str = "met") -> None:
    if fuente == "aic":
        entradas, institucion, revisado = ENTRADAS_AIC, "AIC", True
    else:
        entradas, institucion = (ENTRADAS_REVISADAS if revisado else ENTRADAS_BASE), "MET"

    for nombre, entrada, salida in entradas:
        ruta_entrada = raiz / entrada
        ruta_salida = raiz / salida

        if not ruta_entrada.exists():
            raise FileNotFoundError(f"No existe el CSV requerido: {ruta_entrada}")

        filas = leer_csv(ruta_entrada, recortar=False)
        if nombre == "pendientes":
            # Agrupa los pendientes por sugerencia automatica para revisarlos por bloques.
            filas.sort(key=lambda f: ORDEN_SUGERENCIA.get(f.get("corpus_actual", ""), 9))
        ruta_salida.parent.mkdir(parents=True, exist_ok=True)
        ruta_salida.write_bytes(
            construir_html(nombre, filas, raiz, ruta_salida, revisado, institucion).encode("utf-8")
        )

        print(f"{nombre}: {len(filas)} registros -> {ruta_salida}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Genera galerias HTML para revision visual (MET v2 o AIC v2).")
    parser.add_argument("--root", default=".", help="Raiz del repositorio.")
    parser.add_argument("--revisado", action="store_true", help="Usa los CSV revisados desde el workbook manual.")
    parser.add_argument("--fuente", choices=["met", "aic"], default="met", help="Fuente de las galerias.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    generar_galerias(Path(args.root).resolve(), revisado=args.revisado, fuente=args.fuente)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())