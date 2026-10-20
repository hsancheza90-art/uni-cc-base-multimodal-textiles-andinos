"""Resumen de la ficha de aptitud y galerias por banda sugerida.

Uso desde la raiz del repositorio (sin red):

    python -m src.imagenes.informe_aptitud
    python -m src.imagenes.informe_aptitud --sin-galerias

Resume las bandas y los atributos de data/metadata/aptitud_imagenes_v2.csv por
fuente, los compara con las decisiones manuales AIC (la fuente que calibra el
modelo vigente) y genera una galeria por banda para la revision visual. La
calibracion detallada esta en outputs/reports/aptitud_calibracion_v2.md.
"""

from __future__ import annotations

import argparse
import html
import os
from collections import Counter, defaultdict
from pathlib import Path

from src.imagenes.aptitud import NIVELES, SALIDA_APTITUD, leer_modelo
from src.imagenes.aptitud_workbooks import es_decision_automatica
from src.imagenes.descargar_evaluacion import ENTRADA_AIC, MANIFIESTO_EVALUACION
from src.utils.archivos import indexar, leer_csv
from src.utils.metricas import tabla

SALIDA_INFORME = "outputs/reports/aptitud_imagenes_v2_resumen.md"
CARPETA_GALERIAS = "outputs/review"
BANDAS = ("principal", "secundario", "revisar", "descartar")
FUENTES = ("AIC", "MET", "CMA")
MOTIVOS_PERTINENCIA = {"plumaria", "muneco", "posterior_inca"}
AIC_REVISADOS = (
    "data/metadata/aic_corpus_principal_v2_revisado.csv",
    "data/metadata/aic_corpus_secundario_v2_revisado.csv",
    "data/metadata/aic_descartados_v2_revisado.csv",
    "data/metadata/aic_pendientes_revision_v2.csv",
)


def referencias_aic(raiz: Path) -> dict[str, dict[str, str]]:
    """Decision manual AIC, titulo, cultura y enlace de cada candidato."""
    culturas = {fila["id_fuente"]: fila["cultura"] for fila in leer_csv(raiz / ENTRADA_AIC)}
    salida = {}
    for entrada in AIC_REVISADOS:
        for fila in leer_csv(raiz / entrada):
            salida[f"AIC:{fila['id_fuente']}"] = {
                "decision": fila["corpus_final"],
                "automatica": es_decision_automatica(lambda campo, f=fila: f.get(campo, "")),
                "titulo": fila["titulo_original"],
                "cultura": culturas.get(fila["id_fuente"], fila["cultura"]),
                "url_objeto": fila["url_objeto"],
            }
    return salida


def construir_informe(raiz: Path) -> tuple[list[str], list[dict[str, str]]]:
    aptitud = leer_csv(raiz / SALIDA_APTITUD)
    modelo = leer_modelo(raiz)
    refs = referencias_aic(raiz)
    for fila in aptitud:
        fila.update({f"ref_{k}": v for k, v in refs.get(fila["id_global"], {}).items()})

    u = modelo["umbrales"]
    lineas = [
        "# Ficha de aptitud de las imágenes (v2)",
        "",
        f"Generado por `python -m src.imagenes.informe_aptitud` a partir de `{SALIDA_APTITUD}`. Modelo calibrado con "
        f"{modelo['registros']} decisiones manuales {modelo['fuente_calibracion']} "
        f"(`config/aptitud_modelo.json`; detalle en `outputs/reports/aptitud_calibracion_v2.md`).",
        "",
        "Cada imagen recibe un nivel por atributo (fotografía, colores, formas, completitud y estructura), un puntaje "
        "ordinal de 0 a 100 y una banda sugerida. El puntaje solo sugiere; la decisión es manual.",
        "",
        f"Bandas: principal si el puntaje ≥ {u['principal']} (imagen de referencia sugerida si además ≥ {u['referencia']}); "
        f"descartar si < {u['descartar']}; revisar entre ambos. Antes del puntaje, las puertas: pertinencia por "
        "metadatos (plumaria, muñecos, piezas posteriores a 1532), resolución insuficiente o sin imagen → descartar; "
        "fotografía en blanco y negro → secundario.",
        "",
        "## Bandas sugeridas por fuente",
        "",
    ]
    conteo = Counter((f["fuente"], f["banda_sugerida"]) for f in aptitud)
    refs_sugeridas = Counter(f["fuente"] for f in aptitud if f["referencia_sugerida"] == "si")
    lineas += tabla([[fuente] + [str(conteo[(fuente, b)]) for b in BANDAS] + [str(refs_sugeridas[fuente]),
                     str(sum(conteo[(fuente, b)] for b in BANDAS))] for fuente in FUENTES],
                    ["Fuente", *BANDAS, "Referencias sugeridas", "Total"])
    motivos = Counter(f["motivo_banda"] for f in aptitud)
    lineas += ["", "Motivos de banda: " + ", ".join(f"`{m}` {n}" for m, n in motivos.most_common()) + ".", ""]

    lineas += ["## Atributos por fuente", ""]
    for atributo in (*NIVELES, "estructura"):
        valores = sorted({f[atributo] for f in aptitud if f[atributo]})
        por_fuente = Counter((f["fuente"], f[atributo]) for f in aptitud if f[atributo])
        lineas += [f"**{atributo}**", ""]
        lineas += tabla([[fuente] + [str(por_fuente[(fuente, v)]) for v in valores] for fuente in FUENTES], ["Fuente", *valores])
        lineas.append("")

    # --------------------------------------------------------------- AIC frente a las decisiones manuales
    manuales = [f for f in aptitud if f["fuente"] == "AIC" and f.get("ref_decision") in ("principal", "secundario", "descartados")
                and not f.get("ref_automatica")]
    lineas += [
        "## AIC: banda sugerida frente a la decisión manual",
        "",
        f"Decisiones humanas (n = {len(manuales)}), sin las automáticas. Cifras sobre el modelo final: son optimistas "
        "frente a las de validación cruzada del informe de calibración.",
        "",
    ]
    cruce = Counter((f["ref_decision"], f["banda_sugerida"]) for f in manuales)
    lineas += tabla([[d] + [str(cruce[(d, b)]) for b in BANDAS] for d in ("principal", "secundario", "descartados")],
                    ["Decisión manual \\ banda", *BANDAS])
    lineas.append("")

    lineas += ["## Distribución por cultura", "",
               "Control del sesgo de conservación: un filtro de imagen puede relegar a las culturas que se conservan "
               "sobre todo en fragmentos. Culturas con 8 o más candidatos AIC.", ""]
    por_cultura: dict[str, Counter] = defaultdict(Counter)
    for f in aptitud:
        if f["fuente"] != "AIC":
            continue
        cultura = (f.get("ref_cultura") or "").split(",")[0].split(";")[0].strip().lower() or "(sin cultura)"
        por_cultura[cultura][f["banda_sugerida"]] += 1
        por_cultura[cultura]["referencia"] += f["referencia_sugerida"] == "si"
    filas_cultura = [[c] + [str(n[b]) for b in BANDAS] + [str(n["referencia"]), str(sum(n[b] for b in BANDAS))]
                     for c, n in sorted(por_cultura.items(), key=lambda par: -sum(par[1][b] for b in BANDAS))
                     if sum(n[b] for b in BANDAS) >= 8]
    lineas += tabla(filas_cultura, ["Cultura", *BANDAS, "Referencias sugeridas", "Total"])
    lineas.append("")
    return lineas, aptitud


# ------------------------------------------------------------------ galerias

def esc(valor: object) -> str:
    return html.escape(str(valor or "").strip())


def tarjeta(fila: dict[str, str], imagen: str) -> str:
    img = f'<img src="{esc(imagen)}" alt="{esc(fila["id_global"])}" loading="lazy">' if imagen else '<div class="sin">Sin imagen</div>'
    referencia = '<span class="ref">referencia</span>' if fila["referencia_sugerida"] == "si" else ""
    atributos = " ".join(f'<span class="a">{esc(fila[a])}</span>' for a in ("fotografia", "colores", "formas", "completitud", "estructura") if fila[a])
    return f"""<article>
  <a href="{esc(fila.get('ref_url_objeto'))}" target="_blank" rel="noopener">{img}</a>
  <div class="cuerpo">
    <p class="cabeza"><b>{esc(fila['id_global'])}</b> {referencia} <span class="p">{esc(fila['puntaje_aptitud'] or '—')}</span></p>
    <p class="titulo">{esc(fila.get('ref_titulo'))}</p>
    <p>{esc(fila.get('ref_cultura'))}</p>
    <p>{atributos}</p>
    <p class="motivo">Motivo: {esc(fila['motivo_banda'])} · decisión manual: {esc(fila.get('ref_decision'))}</p>
    <p class="just">{esc(fila['justificacion'])}</p>
  </div>
</article>"""


def galeria(raiz: Path, banda: str, filas: list[dict[str, str]], manifiesto: dict[str, dict[str, str]]) -> Path:
    salida = raiz / CARPETA_GALERIAS / f"aptitud_{banda}_galeria.html"
    secciones = []
    for fuente in FUENTES:
        grupo = sorted((f for f in filas if f["fuente"] == fuente), key=lambda f: -float(f["puntaje_aptitud"] or 0))
        if not grupo:
            continue
        tarjetas = []
        for f in grupo:
            registro = manifiesto.get(f["id_global"], {})
            ruta = raiz / registro["ruta_copia_evaluacion"] if registro.get("ruta_copia_evaluacion") else None
            imagen = os.path.relpath(ruta, salida.parent).replace("\\", "/") if ruta and ruta.exists() else registro.get("url_descargada", "")
            tarjetas.append(tarjeta(f, imagen))
        secciones.append(f"<h2>{fuente} ({len(grupo)})</h2>\n<main>\n" + "\n".join(tarjetas) + "\n</main>")
    contenido = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Aptitud: {esc(banda)}</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 24px; background: #f6f6f4; color: #222; }}
main {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 16px; }}
article {{ background: #fff; border: 1px solid #ddd; border-radius: 8px; overflow: hidden; }}
img, .sin {{ width: 100%; height: 300px; object-fit: contain; background: #eee; display: grid; place-items: center; color: #777; }}
.cuerpo {{ padding: 12px; font-size: 13px; line-height: 1.35; }}
.cuerpo p {{ margin: 4px 0; }}
.cabeza {{ display: flex; gap: 6px; align-items: center; }}
.p {{ margin-left: auto; background: #1f4e78; color: #fff; border-radius: 999px; padding: 2px 8px; font-weight: bold; }}
.ref {{ background: #7f6000; color: #fff; border-radius: 999px; padding: 2px 8px; font-size: 11px; }}
.a {{ display: inline-block; background: #e9eef4; color: #1f4e78; border-radius: 999px; padding: 1px 6px; margin: 1px; font-size: 11px; }}
.titulo {{ font-style: italic; color: #555; }}
.motivo, .just {{ color: #444; }}
</style>
</head>
<body>
<h1>Aptitud analítica: banda «{esc(banda)}» ({len(filas)} registros)</h1>
<p>Ordenado por puntaje dentro de cada fuente. La imagen enlaza a la ficha del museo. Generado por <code>python -m src.imagenes.informe_aptitud</code>.</p>
{''.join(secciones)}
</body>
</html>
"""
    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.write_bytes(contenido.encode("utf-8"))
    return salida


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Resumen de la ficha de aptitud y galerias por banda.")
    parser.add_argument("--root", default=".", help="Raiz del repositorio.")
    parser.add_argument("--sin-galerias", action="store_true", help="Solo escribe el informe.")
    args = parser.parse_args(argv)
    raiz = Path(args.root).resolve()

    lineas, aptitud = construir_informe(raiz)
    ruta = raiz / SALIDA_INFORME
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_bytes(("\n".join(lineas) + "\n").encode("utf-8"))
    print(f"Informe: {ruta}")

    if not args.sin_galerias:
        manifiesto = indexar(leer_csv(raiz / MANIFIESTO_EVALUACION), "id_global")
        for banda in BANDAS:
            filas = [f for f in aptitud if f["banda_sugerida"] == banda]
            print(f"Galeria {banda}: {galeria(raiz, banda, filas, manifiesto)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
