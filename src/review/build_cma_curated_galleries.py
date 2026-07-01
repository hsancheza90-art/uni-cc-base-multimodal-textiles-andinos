from __future__ import annotations

import argparse
import csv
from html import escape
from pathlib import Path


GALERIAS = [
    (
        "data/metadata/cma_corpus_principal.csv",
        "outputs/review/cma_corpus_principal_galeria.html",
        "CMA - Corpus principal",
    ),
    (
        "data/metadata/cma_corpus_secundario.csv",
        "outputs/review/cma_corpus_secundario_galeria.html",
        "CMA - Corpus secundario",
    ),
    (
        "data/metadata/cma_descartados.csv",
        "outputs/review/cma_descartados_galeria.html",
        "CMA - Descartados",
    ),
]


def leer_csv(ruta: Path) -> list[dict[str, str]]:
    if not ruta.exists():
        return []

    with ruta.open(newline="", encoding="utf-8-sig") as archivo:
        return list(csv.DictReader(archivo))


def valor(fila: dict[str, str], columna: str) -> str:
    return escape(str(fila.get(columna, "") or "").strip())


def tarjeta(fila: dict[str, str]) -> str:
    titulo = valor(fila, "titulo_original") or "Sin titulo"
    id_objeto = valor(fila, "id_objeto")
    cultura = valor(fila, "cultura")
    periodo = valor(fila, "periodo")
    material = valor(fila, "material_original")
    tecnica = valor(fila, "tecnica_original")
    decision = valor(fila, "decision_auditoria")
    motivo = valor(fila, "motivo_auditoria")
    observacion = valor(fila, "observacion_auditoria")
    calidad = valor(fila, "calidad_visual")
    tipo = valor(fila, "tipo_objeto_manual")
    url_objeto = valor(fila, "url_objeto")
    url_imagen = valor(fila, "url_imagen")

    imagen_html = (
        f'<a href="{url_objeto}" target="_blank" rel="noopener">'
        f'<img src="{url_imagen}" alt="{titulo}" loading="lazy"></a>'
        if url_imagen
        else '<div class="sin-imagen">Sin imagen</div>'
    )

    return f"""
    <article class="card">
      {imagen_html}
      <div class="body">
        <h2>{titulo}</h2>
        <p><strong>ID objeto:</strong> {id_objeto}</p>
        <p><strong>Cultura:</strong> {cultura}</p>
        <p><strong>Periodo:</strong> {periodo}</p>
        <p><strong>Material:</strong> {material}</p>
        <p><strong>Tecnica:</strong> {tecnica}</p>
        <p><strong>Decision auditoria:</strong> {decision}</p>
        <p><strong>Motivo:</strong> {motivo}</p>
        <p><strong>Observacion:</strong> {observacion}</p>
        <p><strong>Calidad visual:</strong> {calidad}</p>
        <p><strong>Tipo objeto:</strong> {tipo}</p>
        <p><a href="{url_objeto}" target="_blank" rel="noopener">Abrir ficha institucional</a></p>
      </div>
    </article>
    """


def construir_html(titulo: str, filas: list[dict[str, str]]) -> str:
    tarjetas = "\n".join(tarjeta(fila) for fila in filas)

    return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>{escape(titulo)}</title>
  <style>
    body {{
      margin: 0;
      font-family: Arial, sans-serif;
      background: #f5f5f5;
      color: #222;
    }}
    header {{
      padding: 24px 32px;
      background: #111;
      color: white;
    }}
    header h1 {{
      margin: 0 0 8px;
      font-size: 24px;
    }}
    main {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(330px, 1fr));
      gap: 18px;
      padding: 24px;
    }}
    .card {{
      background: white;
      border: 1px solid #ddd;
      border-radius: 8px;
      overflow: hidden;
    }}
    img {{
      width: 100%;
      height: 280px;
      object-fit: contain;
      background: #eee;
      display: block;
    }}
    .sin-imagen {{
      height: 280px;
      display: grid;
      place-items: center;
      background: #eee;
      color: #777;
    }}
    .body {{
      padding: 14px;
    }}
    h2 {{
      font-size: 16px;
      margin: 0 0 10px;
    }}
    p {{
      font-size: 13px;
      line-height: 1.35;
      margin: 6px 0;
    }}
    a {{
      color: #0645ad;
    }}
  </style>
</head>
<body>
  <header>
    <h1>{escape(titulo)}</h1>
    <p>Total de registros: {len(filas)}</p>
  </header>
  <main>
    {tarjetas}
  </main>
</body>
</html>
"""


def construir_indice(root: Path, resumen: list[tuple[str, str, int]]) -> None:
    items = "\n".join(
        f'<li><a href="{archivo}">{escape(titulo)}</a> - {total} registros</li>'
        for archivo, titulo, total in resumen
    )

    html = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Indice galerias CMA</title>
</head>
<body>
  <h1>Indice galerias CMA</h1>
  <ul>
    {items}
  </ul>
</body>
</html>
"""
    (root / "outputs/review/cma_galerias_index.html").write_text(html, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Construye galerias HTML curadas CMA.")
    parser.add_argument("--root", default=".", help="Raiz del repositorio.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    resumen = []

    for csv_rel, html_rel, titulo in GALERIAS:
        filas = leer_csv(root / csv_rel)
        salida = root / html_rel
        salida.parent.mkdir(parents=True, exist_ok=True)
        salida.write_text(construir_html(titulo, filas), encoding="utf-8")

        resumen.append((Path(html_rel).name, titulo, len(filas)))
        print(f"{titulo}: {len(filas)} registros -> {salida}")

    construir_indice(root, resumen)
    print(root / "outputs/review/cma_galerias_index.html")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())