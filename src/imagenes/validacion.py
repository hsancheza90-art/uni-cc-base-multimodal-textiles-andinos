"""Muestra de validacion ciega del puntaje de aptitud en MET y CMA.

Uso desde la raiz del repositorio (sin red):

    python -m src.imagenes.validacion --crear      # muestra y workbook ciego (no sobrescribe sin --forzar)
    python -m src.imagenes.validacion              # evalua las anotaciones del workbook
    python -m src.imagenes.validacion --trasladar  # lleva las anotaciones a los workbooks MET y CMA

El modelo se calibro con las decisiones AIC. Antes de aplicarlo a MET y CMA se
comprueba si transfiere: el revisor anota una muestra con el criterio AIC
(principal, secundario o descartados y su motivo) sin ver el puntaje ni la
decision v1, y se mide el acuerdo con la banda sugerida y con la decision v1.

La muestra excluye lo que ya deciden reglas verificables (pertinencia por
metadatos, fotografia monocroma, resolucion, sin imagen) y los descartes v1 por
pertinencia (no andino, no textil, herramienta, materia prima, duplicado): ahi el
modelo de imagen no interviene. Se estratifica por fuente y banda sugerida, con
semilla fija; el orden de la galeria y del workbook es aleatorio.
"""

from __future__ import annotations

import argparse
import html
import os
from collections import Counter
from pathlib import Path

import numpy as np
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

from src.imagenes.aptitud import SALIDA_APTITUD
from src.imagenes.aptitud_workbooks import DESCARTES_PERTINENCIA_V1, WORKBOOKS
from src.imagenes.descargar_evaluacion import MANIFIESTO_EVALUACION
from src.imagenes.motivos import analizar_motivo
from src.utils.archivos import indexar, leer_csv
from src.utils.metricas import kappa, tabla

WORKBOOK_VALIDACION = "data/metadata/validacion_met_cma_v2.xlsx"
GALERIA_VALIDACION = "outputs/review/validacion_met_cma_v2_galeria.html"
INFORME_VALIDACION = "outputs/reports/validacion_met_cma_v2.md"
HOJA = "validacion"
SEMILLA = 20261019
TAMANO_POR_FUENTE = {"MET": 20, "CMA": 20}
MINIMO_POR_BANDA = 4
BANDAS = ("principal", "revisar", "descartar")
PUERTAS = {"sin_imagen", "resolucion_insuficiente", "fotografia_monocroma", "plumaria", "muneco", "posterior_inca"}

COLUMNAS = ["orden", "id_global", "titulo_original", "cultura", "url_objeto", "url_imagen",
            "corpus_final", "motivo_revision", "revisor", "fecha_revision"]


def decisiones_v1(raiz: Path, fuente: str) -> dict[str, dict[str, str]]:
    ruta, hoja = WORKBOOKS[fuente]
    libro = load_workbook(raiz / ruta, read_only=True, data_only=True)
    filas = list(libro[hoja].iter_rows(values_only=True))
    libro.close()
    indice = {nombre: i for i, nombre in enumerate(filas[0])}
    salida = {}
    for fila in filas[1:]:
        valor = {nombre: str(fila[i] or "").strip() for nombre, i in indice.items()}
        motivos = {valor.get("estado_curacion", ""), valor.get("motivo_curacion", ""), valor.get("motivo_revision_original", "")
                   or valor.get("motivo_revision", "")}
        valor["pertinencia_v1"] = "si" if valor["corpus_final"] == "descartados" and motivos & DESCARTES_PERTINENCIA_V1 else "no"
        salida[f"{fuente}:{valor['id_fuente']}"] = valor
    return salida


def universo(raiz: Path) -> list[dict[str, str]]:
    """Registros MET y CMA donde decide el modelo de imagen (sin puertas ni pertinencia v1)."""
    aptitud = indexar(leer_csv(raiz / SALIDA_APTITUD), "id_global")
    salida = []
    for fuente in TAMANO_POR_FUENTE:
        for id_global, v1 in decisiones_v1(raiz, fuente).items():
            ficha = aptitud.get(id_global)
            if not ficha or ficha["motivo_banda"] in PUERTAS or v1["pertinencia_v1"] == "si":
                continue
            if v1["corpus_final"] not in ("principal", "secundario", "descartados"):
                continue
            salida.append({"id_global": id_global, "fuente": fuente, "banda": ficha["banda_sugerida"],
                           "decision_v1": v1["corpus_final"], "titulo_original": v1["titulo_original"],
                           "cultura": v1["cultura"], "url_objeto": v1["url_objeto"], "url_imagen": v1["url_imagen"]})
    return salida


def muestrear(candidatos: list[dict[str, str]]) -> list[dict[str, str]]:
    """Muestra estratificada por fuente y banda: minimo por banda, el resto proporcional."""
    rng = np.random.default_rng(SEMILLA)
    muestra = []
    for fuente, tamano in TAMANO_POR_FUENTE.items():
        estratos = {b: sorted((c for c in candidatos if c["fuente"] == fuente and c["banda"] == b), key=lambda c: c["id_global"])
                    for b in BANDAS}
        cupos = {b: min(len(v), MINIMO_POR_BANDA) for b, v in estratos.items()}
        restante = tamano - sum(cupos.values())
        total = sum(len(v) - cupos[b] for b, v in estratos.items())
        for b, v in estratos.items():
            if total:
                cupos[b] += min(len(v) - cupos[b], round(restante * (len(v) - cupos[b]) / total))
        # El redondeo puede dejar la fuente corta o larga: el ajuste va al estrato con mas disponibles.
        diferencia = tamano - sum(cupos.values())
        mayor = max(estratos, key=lambda b: len(estratos[b]) - cupos[b])
        cupos[mayor] = max(0, min(len(estratos[mayor]), cupos[mayor] + diferencia))
        for b, v in estratos.items():
            indices = rng.choice(len(v), cupos[b], replace=False) if cupos[b] else []
            muestra += [v[i] for i in sorted(indices)]
    orden = rng.permutation(len(muestra))
    return [dict(muestra[i], orden=str(n + 1)) for n, i in enumerate(orden)]


def crear(raiz: Path, forzar: bool) -> int:
    salida = raiz / WORKBOOK_VALIDACION
    if salida.exists() and not forzar:
        print(f"{WORKBOOK_VALIDACION} ya existe y puede tener anotaciones; no se sobrescribio (use --forzar).")
        return 1
    muestra = muestrear(universo(raiz))
    libro = Workbook()
    hoja = libro.active
    hoja.title = HOJA
    hoja.append(COLUMNAS)
    for fila in muestra:
        hoja.append([fila.get(c, "") for c in COLUMNAS])
    for celda in hoja[1]:
        celda.font = Font(color="FFFFFF", bold=True)
        celda.fill = PatternFill("solid", fgColor="1F4E78")
        celda.alignment = Alignment(horizontal="center", wrap_text=True)
    for letra, ancho in zip("ABCDEFGHIJ", (7, 13, 36, 22, 40, 40, 14, 60, 14, 12)):
        hoja.column_dimensions[letra].width = ancho
    for fila in range(2, hoja.max_row + 1):
        for letra in "EF":
            if hoja[f"{letra}{fila}"].value:
                hoja[f"{letra}{fila}"].hyperlink = hoja[f"{letra}{fila}"].value
    validacion = DataValidation(type="list", formula1='"principal,secundario,descartados"', allow_blank=True)
    hoja.add_data_validation(validacion)
    validacion.add(f"G2:G{hoja.max_row}")
    hoja.freeze_panes = "B2"
    instrucciones = libro.create_sheet("instrucciones")
    for i, texto in enumerate([
        "Validacion ciega del puntaje de aptitud en MET y CMA",
        "Anote cada imagen con el mismo criterio que uso en AIC: principal si los colores y las formas se identifican "
        "(aunque la pieza este incompleta), secundario si tiene muchos defectos, descartados si no sirve para el estudio.",
        "Escriba el motivo como en AIC (por ejemplo: Textil incompleto con colores y formas visibles).",
        "La muestra no muestra el puntaje ni la decision anterior a proposito: no los busque hasta terminar.",
        f"Galeria con las mismas imagenes y el mismo orden: {GALERIA_VALIDACION}",
    ], start=1):
        instrucciones[f"A{i}"] = texto
    instrucciones["A1"].font = Font(bold=True, size=14)
    instrucciones.column_dimensions["A"].width = 120
    salida.parent.mkdir(parents=True, exist_ok=True)
    libro.save(salida)
    galeria(raiz, muestra)
    print(f"Muestra: {len(muestra)} registros -> {salida}")
    print("Por fuente y banda (no se muestra al revisor):", dict(Counter((m["fuente"], m["banda"]) for m in muestra)))
    return 0


def galeria(raiz: Path, muestra: list[dict[str, str]]) -> None:
    salida = raiz / GALERIA_VALIDACION
    manifiesto = indexar(leer_csv(raiz / MANIFIESTO_EVALUACION), "id_global")
    tarjetas = []
    for fila in sorted(muestra, key=lambda f: int(f["orden"])):
        registro = manifiesto.get(fila["id_global"], {})
        ruta = raiz / registro["ruta_copia_evaluacion"] if registro.get("ruta_copia_evaluacion") else None
        imagen = os.path.relpath(ruta, salida.parent).replace("\\", "/") if ruta and ruta.exists() else registro.get("url_descargada", "")
        tarjetas.append(f"""<article>
  <a href="{html.escape(fila['url_objeto'])}" target="_blank" rel="noopener"><img src="{html.escape(imagen)}" alt="{html.escape(fila['id_global'])}" loading="lazy"></a>
  <p><b>{html.escape(fila['orden'])}.</b> {html.escape(fila['id_global'])}</p>
  <p class="t">{html.escape(fila['titulo_original'])}</p>
  <p>{html.escape(fila['cultura'])}</p>
</article>""")
    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.write_bytes(f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Validación MET y CMA</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 24px; background: #f6f6f4; color: #222; }}
main {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 16px; }}
article {{ background: #fff; border: 1px solid #ddd; border-radius: 8px; padding-bottom: 8px; }}
img {{ width: 100%; height: 340px; object-fit: contain; background: #eee; }}
p {{ margin: 4px 12px; font-size: 14px; }}
.t {{ font-style: italic; color: #555; }}
</style>
</head>
<body>
<h1>Validación ciega: {len(muestra)} imágenes MET y CMA</h1>
<p>Anote cada imagen en <code>{WORKBOOK_VALIDACION}</code> con el criterio AIC. No se muestran el puntaje ni la decisión anterior.</p>
<main>
{chr(10).join(tarjetas)}
</main>
</body>
</html>
""".encode("utf-8"))


# ------------------------------------------------------------------ evaluacion

def evaluar(raiz: Path) -> int:
    libro = load_workbook(raiz / WORKBOOK_VALIDACION, read_only=True, data_only=True)
    filas = list(libro[HOJA].iter_rows(values_only=True))
    libro.close()
    indice = {nombre: i for i, nombre in enumerate(filas[0])}
    anotadas = [{c: str(f[indice[c]] or "").strip() for c in COLUMNAS} for f in filas[1:]]
    anotadas = [a for a in anotadas if a["corpus_final"] in ("principal", "secundario", "descartados")]
    aptitud = indexar(leer_csv(raiz / SALIDA_APTITUD), "id_global")
    v1 = {**decisiones_v1(raiz, "MET"), **decisiones_v1(raiz, "CMA")}
    if not anotadas:
        print("La muestra aun no tiene anotaciones.")
        return 0

    def principal(valor: str) -> str:
        return "principal" if valor == "principal" else "no_principal"

    lineas = ["# Validación ciega del puntaje de aptitud en MET y CMA", "",
              f"Generado por `python -m src.imagenes.validacion` desde `{WORKBOOK_VALIDACION}` "
              f"({len(anotadas)} de {len(filas) - 1} imágenes anotadas).", "",
              "El revisor anotó sin ver el puntaje ni la decisión v1, con el criterio aplicado en AIC. "
              "La comparación principal es binaria (principal frente al resto), porque el puntaje no separa "
              "secundario de descartados y la zona «revisar» queda para la decisión manual.", ""]
    filas_tabla = []
    for nombre, filtro in (("MET + CMA", ("MET", "CMA")), ("MET", ("MET",)), ("CMA", ("CMA",))):
        grupo = [a for a in anotadas if a["id_global"].split(":")[0] in filtro]
        con_banda = [a for a in grupo if aptitud[a["id_global"]]["banda_sugerida"] != "revisar"]
        pares_modelo = [(principal(a["corpus_final"]), principal(aptitud[a["id_global"]]["banda_sugerida"])) for a in con_banda]
        pares_v1 = [(principal(a["corpus_final"]), principal(v1[a["id_global"]]["corpus_final"])) for a in grupo]
        acuerdo = sum(x == y for x, y in pares_modelo) / len(pares_modelo) if pares_modelo else float("nan")
        filas_tabla.append([nombre, str(len(grupo)), str(len(con_banda)), f"{acuerdo:.2f}", f"{kappa(pares_modelo):.2f}",
                            f"{sum(x == y for x, y in pares_v1) / len(pares_v1):.2f}" if pares_v1 else "", f"{kappa(pares_v1):.2f}"])
    lineas += tabla(filas_tabla, ["Conjunto", "Anotadas", "Con banda (sin revisar)", "Acuerdo con el modelo",
                                  "Kappa con el modelo", "Acuerdo con v1", "Kappa con v1"])
    cruce = Counter((a["corpus_final"], aptitud[a["id_global"]]["banda_sugerida"]) for a in anotadas)
    lineas += ["", "## Anotación frente a banda sugerida", ""]
    lineas += tabla([[d] + [str(cruce[(d, b)]) for b in BANDAS] for d in ("principal", "secundario", "descartados")],
                    ["Anotación \\ banda", *BANDAS])
    revisar = [a for a in anotadas if aptitud[a["id_global"]]["banda_sugerida"] == "revisar"]
    lineas += ["", f"En la banda «revisar» ({len(revisar)} imágenes) el revisor puso: "
               + ", ".join(f"{d} {n}" for d, n in Counter(a["corpus_final"] for a in revisar).most_common()) + "."]
    desacuerdos = [a for a in anotadas if aptitud[a["id_global"]]["banda_sugerida"] != "revisar"
                   and principal(a["corpus_final"]) != principal(aptitud[a["id_global"]]["banda_sugerida"])]
    lineas += ["", "## Desacuerdos con el modelo", ""]
    lineas += tabla([[a["id_global"], a["corpus_final"], aptitud[a["id_global"]]["banda_sugerida"],
                      aptitud[a["id_global"]]["puntaje_aptitud"], a["motivo_revision"][:60]] for a in desacuerdos],
                    ["Registro", "Anotación", "Banda", "Puntaje", "Motivo del revisor"]) if desacuerdos else ["Ninguno."]
    atributos = Counter()
    for a in anotadas:
        m = analizar_motivo(a["motivo_revision"])
        for clave in ("colores", "formas", "completitud"):
            if m[clave]:
                atributos[(clave, m[clave], aptitud[a["id_global"]][clave])] += 1
    lineas += ["", "## Atributos: anotación del revisor frente a nivel estimado", ""]
    lineas += tabla([[c, v, n_, str(n)] for (c, v, n_), n in sorted(atributos.items())],
                    ["Atributo", "Revisor", "Imagen", "Registros"])
    ruta = raiz / INFORME_VALIDACION
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_bytes(("\n".join(lineas) + "\n").encode("utf-8"))
    print(f"Informe: {ruta}")
    return 0


# ------------------------------------------------------------------ traslado a los workbooks

ORIGEN_VALIDACION = "validacion_ciega_v2"
REVISOR = "Henry Sánchez"


def contradice_motivo(decision: str, motivo: str) -> bool:
    """La decision contradice el criterio del 2026-10-19 segun el propio motivo del revisor.

    Principal = colores y formas identificables (completo o incompleto). Un descarte o un
    secundario cuyo motivo dice «con colores y formas visibles», o un principal cuyo motivo
    dice que no se ven, se deja en revisar para que el revisor lo resuelva.
    """
    a = analizar_motivo(motivo)
    legible = a["colores"] == "si" and a["formas"] == "si"
    ilegible = a["colores"] == "no" or a["formas"] == "no"
    return (decision != "principal" and legible and not a["pertinencia"]) or (decision == "principal" and ilegible)


def trasladar(raiz: Path, fecha: str) -> int:
    """Lleva las anotaciones de la validacion a los workbooks MET y CMA como decisiones del revisor."""
    from src.imagenes.aptitud_workbooks import decision_para

    libro_v = load_workbook(raiz / WORKBOOK_VALIDACION, read_only=True, data_only=True)
    filas = list(libro_v[HOJA].iter_rows(values_only=True))
    libro_v.close()
    indice_v = {nombre: i for i, nombre in enumerate(filas[0])}
    anotaciones = {str(f[indice_v["id_global"]]): {c: str(f[indice_v[c]] or "").strip() for c in COLUMNAS} for f in filas[1:]}
    conteo = Counter()
    for fuente in TAMANO_POR_FUENTE:
        ruta, nombre_hoja = WORKBOOKS[fuente]
        libro = load_workbook(raiz / ruta)
        hoja = libro[nombre_hoja]
        indice = {celda.value: celda.column for celda in hoja[1]}
        for fila in range(2, hoja.max_row + 1):
            id_global = f"{fuente}:{str(hoja.cell(row=fila, column=indice['id_fuente']).value or '').strip()}"
            anotacion = anotaciones.get(id_global)
            if not anotacion or anotacion["corpus_final"] not in ("principal", "secundario", "descartados"):
                continue

            def leer(columna: str) -> str:
                return str(hoja.cell(row=fila, column=indice[columna]).value or "").strip()

            if leer("origen_curacion") == ORIGEN_VALIDACION:
                continue  # ya trasladada
            decision, motivo = anotacion["corpus_final"], anotacion["motivo_revision"]
            conflicto = contradice_motivo(decision, motivo)
            destino = "revisar" if conflicto else decision
            if destino == leer("corpus_final"):
                conteo["coinciden"] += 1
                continue
            anterior = "; ".join(m for m in (leer("estado_curacion"), leer("motivo_curacion"), leer("motivo_revision")) if m) or "sin motivo"
            nota = (f"Anotación de la validación ciega del {fecha} ({WORKBOOK_VALIDACION}, orden {anotacion['orden']}): "
                    f"{decision}. Decisión anterior: {leer('corpus_final')} ({anterior}).")
            if conflicto:
                nota += " Queda en revisar: la anotación contradice su propio motivo según el criterio del 2026-10-19."
            valores = {
                "corpus_final": destino,
                "decision_revision": "revisar" if conflicto else decision_para(leer("corpus_actual"), destino),
                "motivo_revision": motivo,
                "observaciones_revision": nota,
                "revisor": REVISOR,
                "fecha_revision": fecha,
                "origen_curacion": ORIGEN_VALIDACION,
            }
            for columna, valor in valores.items():
                hoja.cell(row=fila, column=indice[columna], value=valor)
            conteo["revisar" if conflicto else "trasladadas"] += 1
            print(f"  {id_global}: {valores['corpus_final']} ({'conflicto con el motivo' if conflicto else 'anotación'})")
        libro.save(raiz / ruta)
    print(f"Trasladadas {conteo['trasladadas']} | en revisar por contradicción {conteo['revisar']} | ya coincidían {conteo['coinciden']}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Muestra de validacion ciega del puntaje de aptitud en MET y CMA.")
    parser.add_argument("--root", default=".", help="Raiz del repositorio.")
    parser.add_argument("--crear", action="store_true", help="Crea la muestra, el workbook ciego y la galeria.")
    parser.add_argument("--forzar", action="store_true", help="Con --crear, sobrescribe el workbook (pierde anotaciones).")
    parser.add_argument("--trasladar", action="store_true", help="Lleva las anotaciones a los workbooks MET y CMA.")
    parser.add_argument("--fecha", default="2026-10-19", help="Fecha de las decisiones trasladadas.")
    args = parser.parse_args(argv)
    raiz = Path(args.root).resolve()
    if args.trasladar:
        return trasladar(raiz, args.fecha)
    return crear(raiz, args.forzar) if args.crear else evaluar(raiz)


if __name__ == "__main__":
    raise SystemExit(main())
