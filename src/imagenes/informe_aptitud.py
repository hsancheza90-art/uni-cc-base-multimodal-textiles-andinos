"""Resumen de la ficha de aptitud y galerias por banda sugerida.

Uso desde la raiz del repositorio (sin red):

    python -m src.imagenes.informe_aptitud
    python -m src.imagenes.informe_aptitud --sin-galerias

Resume las bandas y los atributos de data/metadata/aptitud_imagenes_v2.csv por
fuente, los compara con las decisiones manuales AIC (la unica fuente decidida por
completo con el criterio vigente) y genera una galeria por banda para la revision
visual. La calibracion conjunta AIC+MET+CMA esta en outputs/reports/aptitud_calibracion_v2.md.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from pathlib import Path

from src.imagenes.aptitud import NIVELES, SALIDA_APTITUD, leer_modelo
from src.imagenes.aptitud_workbooks import es_decision_automatica
from src.imagenes.descargar_evaluacion import ENTRADA_AIC, MANIFIESTO_EVALUACION
from src.review.galerias import CARPETA as CARPETA_GALERIAS
from src.review.galerias import esc, escribir_pagina, etiqueta, imagen_evaluacion, tarjeta
from src.utils.archivos import escribir_texto, indexar, leer_csv
from src.utils.fuentes import FUENTES, SUBCONJUNTOS
from src.utils.metricas import tabla

SALIDA_INFORME = "outputs/reports/aptitud_imagenes_v2_resumen.md"
BANDAS = ("principal", "secundario", "revisar", "descartar")
ORDEN_FUENTES = ("AIC", "MET", "CMA")  # AIC primero: todas sus decisiones calibran el modelo


def referencias_aic(raiz: Path) -> dict[str, dict[str, str]]:
    """Decision manual AIC, titulo, cultura y enlace de cada candidato."""
    culturas = {fila["id_fuente"]: fila["cultura"] for fila in leer_csv(raiz / ENTRADA_AIC)}
    salida = {}
    for entrada in FUENTES["AIC"].revisados:
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
                     str(sum(conteo[(fuente, b)] for b in BANDAS))] for fuente in ORDEN_FUENTES],
                    ["Fuente", *BANDAS, "Referencias sugeridas", "Total"])
    motivos = Counter(f["motivo_banda"] for f in aptitud)
    lineas += ["", "Motivos de banda: " + ", ".join(f"`{m}` {n}" for m, n in motivos.most_common()) + ".", ""]

    lineas += ["## Atributos por fuente", ""]
    for atributo in (*NIVELES, "estructura"):
        valores = sorted({f[atributo] for f in aptitud if f[atributo]})
        por_fuente = Counter((f["fuente"], f[atributo]) for f in aptitud if f[atributo])
        lineas += [f"**{atributo}**", ""]
        lineas += tabla([[fuente] + [str(por_fuente[(fuente, v)]) for v in valores] for fuente in ORDEN_FUENTES], ["Fuente", *valores])
        lineas.append("")

    # --------------------------------------------------------------- AIC frente a las decisiones manuales
    manuales = [f for f in aptitud if f["fuente"] == "AIC" and f.get("ref_decision") in SUBCONJUNTOS
                and not f.get("ref_automatica")]
    lineas += [
        "## AIC: banda sugerida frente a la decisión manual",
        "",
        f"Decisiones humanas (n = {len(manuales)}), sin las automáticas. Cifras sobre el modelo final: son optimistas "
        "frente a las de validación cruzada del informe de calibración.",
        "",
    ]
    cruce = Counter((f["ref_decision"], f["banda_sugerida"]) for f in manuales)
    lineas += tabla([[d] + [str(cruce[(d, b)]) for b in BANDAS] for d in SUBCONJUNTOS],
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

def tarjeta_aptitud(fila: dict[str, str], imagen: str) -> str:
    referencia = etiqueta("referencia", "e ref") if fila["referencia_sugerida"] == "si" else ""
    atributos = " ".join(etiqueta(fila[a]) for a in ("fotografia", "colores", "formas", "completitud", "estructura"))
    return tarjeta(imagen, fila.get("ref_url_objeto", ""), fila["id_global"], [
        f"<b>{esc(fila['id_global'])}</b> {referencia} <span class=\"p\">{esc(fila['puntaje_aptitud'] or '—')}</span>",
        ("t", esc(fila.get("ref_titulo"))),
        esc(fila.get("ref_cultura")),
        atributos,
        ("m", f"Motivo: {esc(fila['motivo_banda'])} · decisión manual: {esc(fila.get('ref_decision'))}"),
        ("m", esc(fila["justificacion"])),
    ])


def galeria(raiz: Path, banda: str, filas: list[dict[str, str]], manifiesto: dict[str, dict[str, str]]) -> Path:
    salida = raiz / CARPETA_GALERIAS / f"aptitud_{banda}_galeria.html"
    secciones = []
    for fuente in ORDEN_FUENTES:
        grupo = sorted((f for f in filas if f["fuente"] == fuente), key=lambda f: -float(f["puntaje_aptitud"] or 0))
        if grupo:
            secciones.append((fuente, [tarjeta_aptitud(f, imagen_evaluacion(raiz, manifiesto, f["id_global"], salida)) for f in grupo]))
    nota = ("Ordenado por puntaje dentro de cada fuente. La imagen enlaza a la ficha del museo. "
            "Generado por <code>python -m src.imagenes.informe_aptitud</code>.")
    return escribir_pagina(salida, f"Aptitud analítica: banda «{banda}» ({len(filas)} registros)", nota, secciones)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Resumen de la ficha de aptitud y galerias por banda.")
    parser.add_argument("--root", default=".", help="Raiz del repositorio.")
    parser.add_argument("--sin-galerias", action="store_true", help="Solo escribe el informe.")
    args = parser.parse_args(argv)
    raiz = Path(args.root).resolve()

    lineas, aptitud = construir_informe(raiz)
    ruta = raiz / SALIDA_INFORME
    escribir_texto(ruta, lineas)
    print(f"Informe: {ruta}")

    if not args.sin_galerias:
        manifiesto = indexar(leer_csv(raiz / MANIFIESTO_EVALUACION), "id_global")
        for banda in BANDAS:
            filas = [f for f in aptitud if f["banda_sugerida"] == banda]
            print(f"Galeria {banda}: {galeria(raiz, banda, filas, manifiesto)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
