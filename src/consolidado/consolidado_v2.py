"""Construye el corpus consolidado v2 (MET, CMA y AIC): principal y complementario (paso del flujo).

Uso desde la raíz del repositorio:

    python -m src.consolidado.consolidado_v2

Entradas (todas generadas por el flujo o versionadas):
- data/processed/corpus_textiles_andinos_v2_principal.csv y _complementario.csv
  (src/anotacion/corpus_v2.py), con el esquema armonizado y la ficha de aptitud.
- data/metadata/grupos_v2.csv: el grupo de cada pieza, decidido por el revisor (src/grupos/grupos.py).
- data/metadata/imagenes_evaluacion_manifiesto_v2.csv y data/metadata/imagenes_evaluacion_dhash_v2.csv.

Salidas, con nombres nuevos (no lee ni escribe ningún archivo _v1_):
- data/processed/corpus_textiles_andinos_met_cma_aic_v2_consolidado.csv
- data/processed/corpus_textiles_andinos_met_cma_aic_v2_fuentes_licencias.csv
- data/metadata/imagenes_manifiesto_met_cma_aic_v2.csv: la copia de evaluación de cada registro.
- data/processed/corpus_textiles_andinos_met_cma_aic_v2_sha256.txt
- outputs/reports/corpus_textiles_andinos_met_cma_aic_v2_resumen.md
- docs/esquema_consolidado_met_cma_aic_v2.md

La anotación estructural v2 no entra en esta versión (estado_anotacion = sin_anotar): se
incorpora en la v2.1, cuando el acuerdo del lote 1 esté medido y los criterios decididos.
Termina con código 1 si hay ids repetidos, campos obligatorios vacíos, valores fuera del
vocabulario, una pieza sin grupo o grupos con pares pendientes.
"""

from __future__ import annotations

import argparse
import hashlib
from collections import Counter
from pathlib import Path

from src.anotacion.corpus_v2 import SALIDA_COMPLEMENTARIO_V2, SALIDA_PRINCIPAL_V2
from src.consolidado.construir_consolidado import FUENTES_LICENCIAS
from src.consolidado.esquema import COLUMNAS, COLUMNAS_CONSOLIDADO_V2, ESQUEMA, ESQUEMA_V2_EXTRA, OBLIGATORIOS
from src.grupos.grupos import REPORTE_GRUPOS, SALIDA_CANDIDATOS, SALIDA_GRUPOS, leer_decisiones
from src.imagenes.descargar_evaluacion import COLUMNAS_MANIFIESTO_EVALUACION, MANIFIESTO_EVALUACION
from src.imagenes.dhash_evaluacion import SALIDA_DHASH
from src.utils.archivos import escribir_csv, escribir_texto, indexar, leer_csv
from src.utils.config import leer_config_grupos
from src.utils.fuentes import FUENTES
from src.utils.metricas import tabla
from src.utils.vocabulario import Campo, leer_vocabulario

SALIDA_CONSOLIDADO_V2 = "data/processed/corpus_textiles_andinos_met_cma_aic_v2_consolidado.csv"
SALIDA_FUENTES_V2 = "data/processed/corpus_textiles_andinos_met_cma_aic_v2_fuentes_licencias.csv"
SALIDA_MANIFIESTO_V2 = "data/metadata/imagenes_manifiesto_met_cma_aic_v2.csv"
SALIDA_SHA256_V2 = "data/processed/corpus_textiles_andinos_met_cma_aic_v2_sha256.txt"
SALIDA_REPORTE_V2 = "outputs/reports/corpus_textiles_andinos_met_cma_aic_v2_resumen.md"
SALIDA_ESQUEMA_V2 = "docs/esquema_consolidado_met_cma_aic_v2.md"

# Fuentes de la v2: las de la v1 y el Art Institute of Chicago. Las imagenes de las tres son CC0 o
# de dominio publico; los textos de AIC (descripcion) son CC BY 4.0 y se citan.
FUENTES_LICENCIAS_V2 = [
    {**f, "licencia_textos": "CC0"} for f in FUENTES_LICENCIAS
] + [{
    "fuente": "AIC",
    "institucion": "Art Institute of Chicago",
    "pais": "USA",
    "tipo_acceso": "Open Access",
    "estado_licencia": "cc0",
    "campo_licencia_fuente": "is_public_domain",
    "url_politica": "https://www.artic.edu/open-access/open-access-images",
    "api": "https://api.artic.edu/api/v1/",
    "licencia_textos": "CC BY 4.0 (descripcion); resto de los metadatos CC0",
}]
COLUMNAS_FUENTES_V2 = list(FUENTES_LICENCIAS_V2[0]) + ["registros_principal", "registros_complementario", "registros_total"]
COLUMNAS_MANIFIESTO_V2 = COLUMNAS_MANIFIESTO_EVALUACION + ["dhash"]


def sha256_archivo(ruta: Path) -> str:
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def registros_v2(raiz: Path) -> list[dict[str, str]]:
    """Principal y complementario v2, en ese orden, con el grupo de cada pieza."""
    grupos = indexar(leer_csv(raiz / SALIDA_GRUPOS), "id_global")
    registros = []
    for ruta in (SALIDA_PRINCIPAL_V2, SALIDA_COMPLEMENTARIO_V2):
        for fila in leer_csv(raiz / ruta):
            grupo = grupos.get(fila["id_global"], {})
            registros.append({**fila, "grupo": grupo.get("grupo", ""), "tamano_grupo": grupo.get("tamano_grupo", "")})
    return registros


def validar(registros: list[dict[str, str]], vocabulario: dict[str, Campo], pendientes: int) -> list[str]:
    problemas = []
    repetidos = sorted(i for i, n in Counter(f["id_global"] for f in registros).items() if n > 1)
    if repetidos:
        problemas.append(f"id_global repetidos entre principal y complementario: {repetidos[:10]}")
    controlados = [c for c in vocabulario.values() if c.nombre in COLUMNAS]
    for fila in registros:
        vacios = [c for c in OBLIGATORIOS if not fila[c]]
        if vacios:
            problemas.append(f"{fila['id_global']}: campos obligatorios vacios: {', '.join(vacios)}")
        if not fila["grupo"]:
            problemas.append(f"{fila['id_global']}: sin grupo en {SALIDA_GRUPOS}")
        for campo in controlados:
            invalidos = campo.invalidos(fila[campo.nombre])
            if invalidos:
                problemas.append(f"{fila['id_global']}: {campo.nombre} fuera del vocabulario: {invalidos}")
    if pendientes:
        problemas.append(f"{pendientes} pares de duplicados sin decidir ({REPORTE_GRUPOS}): los grupos no estan congelados")
    return problemas


def pares_pendientes(raiz: Path) -> int:
    """Pares candidatos sin decisión en el workbook de grupos."""
    config = leer_config_grupos(raiz)["decisiones"]
    decisiones, _ = leer_decisiones(raiz, set(config["unir"]) | set(config["separar"]))
    return sum(1 for p in leer_csv(raiz / SALIDA_CANDIDATOS) if not decisiones.get(p["par"], {}).get("decision"))


def filas_fuentes(registros: list[dict[str, str]]) -> list[dict[str, str]]:
    salida = []
    for fuente in FUENTES_LICENCIAS_V2:
        propias = [f for f in registros if f["fuente"] == fuente["fuente"]]
        principal = sum(f["decision_curacion_final"] == "principal" for f in propias)
        salida.append({**fuente, "registros_principal": str(principal),
                       "registros_complementario": str(len(propias) - principal), "registros_total": str(len(propias))})
    return salida


def lineas_reporte(registros: list[dict[str, str]]) -> list[str]:
    fuentes = list(FUENTES)
    filas = []
    for fuente in fuentes + ["Total"]:
        propias = [f for f in registros if fuente == "Total" or f["fuente"] == fuente]
        principal = sum(f["decision_curacion_final"] == "principal" for f in propias)
        filas.append([fuente, str(principal), str(len(propias) - principal), str(len(propias))])
    grupos = Counter(f["grupo"] for f in registros)
    tamanos = Counter(grupos.values())
    mixtos = sum(1 for g in grupos if len({f["decision_curacion_final"] for f in registros if f["grupo"] == g}) > 1)
    lineas = [
        "# Corpus consolidado v2 (MET, CMA y AIC)",
        "",
        "Resumen generado por `python -m src.flujo` (`src/consolidado/consolidado_v2.py`). Archivo: "
        f"`{SALIDA_CONSOLIDADO_V2}`; esquema en `{SALIDA_ESQUEMA_V2}`. La serie v1 (MET+CMA, 288 registros) sigue "
        "congelada en `corpus-met-cma-v1.2` y no cambia.",
        "",
        "## Conteos",
        "",
    ]
    lineas += tabla(filas, ["Fuente", "Principal", "Complementario", "Total"])
    lineas += ["", "## Grupos de piezas relacionadas", "",
               f"Decididos por el revisor (`{SALIDA_GRUPOS}`, informe `{REPORTE_GRUPOS}`). Un grupo reune registros del "
               "mismo objeto: misma foto, vistas, partes o fragmentos. En evaluaciones de recuperacion cuenta como un "
               "solo item.", ""]
    lineas += tabla([[str(t), str(n)] for t, n in sorted(tamanos.items())], ["Registros por grupo", "Grupos"])
    lineas += ["", f"- Grupos: {len(grupos)} para {len(registros)} registros; {mixtos} reunen piezas del principal y "
                   "del complementario.", ""]
    for campo in ("estado_metadatos", "estado_imagen", "estado_licencia", "banda_sugerida"):
        lineas += [f"## {campo}", ""]
        valores = sorted({f[campo] for f in registros})
        lineas += tabla([[v or "(vacio)"] + [str(sum(f[campo] == v and f["fuente"] == c for f in registros)) for c in fuentes]
                         for v in valores], ["Valor"] + fuentes)
        lineas.append("")
    lineas += [
        "## Cobertura de campos (registros con valor)",
        "",
    ]
    lineas += tabla([[f"`{c}`"] + [f"{sum(bool(f[c]) for f in registros if f['fuente'] == x)}/"
                                    f"{sum(f['fuente'] == x for f in registros)}" for x in fuentes]
                     for c in COLUMNAS_CONSOLIDADO_V2], ["Campo"] + fuentes)
    lineas += [
        "",
        "## Criterios",
        "",
        "- Principal y complementario: las decisiones de los workbooks de revision de cada fuente (en los workbooks, "
        "«secundario»). Los descartados no entran.",
        "- Imagen: la copia de evaluacion de 1600 px (`ruta_imagen_local`), la misma sobre la que se anota; "
        f"manifiesto en `{SALIDA_MANIFIESTO_V2}` con su dHash.",
        "- `grupo_imagen_duplicada` marca imagenes compartidas dentro de cada conjunto (`DUP-` en el principal, `DUPC-` "
        "en el complementario); las compartidas entre conjuntos quedan en el mismo `grupo`.",
        "- `estado_anotacion` es `sin_anotar`: la anotacion estructural v2 se incorpora en la v2.1.",
        "- Licencias: imagenes CC0 o de dominio publico en las tres fuentes; la descripcion de AIC es CC BY 4.0 y se "
        f"cita (`{SALIDA_FUENTES_V2}`).",
    ]
    return lineas


def lineas_esquema(vocabulario: dict[str, Campo]) -> list[str]:
    lineas = [
        "# Esquema del corpus consolidado v2 (MET, CMA y AIC)",
        "",
        f"Archivo: `{SALIDA_CONSOLIDADO_V2}` (UTF-8 sin BOM, separador coma, fin de linea LF).",
        "",
        "Documento generado desde `src/consolidado/esquema.py`; no editar a mano. Es el esquema de la v1 "
        "(`docs/esquema_consolidado_met_cma_v1.md`) con cinco columnas al final; `fuente` admite tambien AIC. Los "
        "campos con vocabulario controlado guardan codigos de `config/vocabulario.toml`; sus etiquetas estan en "
        "`docs/corpus/taxonomia_atributos_v2.md`.",
        "",
        "| # | Campo | Grupo | Descripcion | Vocabulario |",
        "|---:|---|---|---|---|",
    ]
    for numero, (campo, grupo, descripcion) in enumerate(ESQUEMA + ESQUEMA_V2_EXTRA, start=1):
        if campo == "fuente":
            descripcion = "Codigo de la fuente museografica: MET, CMA o AIC."
        obligatorio = " **(obligatorio)**" if campo in OBLIGATORIOS else ""
        control = ""
        if campo in vocabulario:
            control = f"Cuadro {vocabulario[campo].cuadro}" + (", multiple" if vocabulario[campo].multiple else "")
        lineas.append(f"| {numero} | `{campo}` | {grupo} | {descripcion}{obligatorio} | {control} |")
    return lineas


def construir(raiz: Path) -> int:
    vocabulario = leer_vocabulario(raiz)
    registros = registros_v2(raiz)
    problemas = validar(registros, vocabulario, pares_pendientes(raiz))
    if problemas:
        print("Consolidado v2 no construido:")
        for problema in problemas[:20]:
            print(f"- {problema}")
        return 1
    escribir_csv(raiz / SALIDA_CONSOLIDADO_V2, COLUMNAS_CONSOLIDADO_V2,
                 [{c: f[c] for c in COLUMNAS_CONSOLIDADO_V2} for f in registros])
    escribir_csv(raiz / SALIDA_FUENTES_V2, COLUMNAS_FUENTES_V2, filas_fuentes(registros))
    manifiesto = indexar(leer_csv(raiz / MANIFIESTO_EVALUACION), "id_global")
    dhash = indexar(leer_csv(raiz / SALIDA_DHASH), "id_global")
    escribir_csv(raiz / SALIDA_MANIFIESTO_V2, COLUMNAS_MANIFIESTO_V2, [
        {**{c: manifiesto[f["id_global"]].get(c, "") for c in COLUMNAS_MANIFIESTO_EVALUACION},
         "dhash": dhash.get(f["id_global"], {}).get("dhash", "")}
        for f in registros if f["id_global"] in manifiesto
    ])
    escribir_texto(raiz / SALIDA_REPORTE_V2, lineas_reporte(registros))
    escribir_texto(raiz / SALIDA_ESQUEMA_V2, lineas_esquema(vocabulario))
    verificados = [SALIDA_CONSOLIDADO_V2, SALIDA_FUENTES_V2, SALIDA_MANIFIESTO_V2]
    escribir_texto(raiz / SALIDA_SHA256_V2, [f"{sha256_archivo(raiz / r)}  {r}" for r in verificados])
    conteo = Counter((f["fuente"], f["decision_curacion_final"]) for f in registros)
    print(f"Consolidado v2: {len(registros)} registros ("
          + ", ".join(f"{c} {conteo[(c, 'principal')]}+{conteo[(c, 'complementario')]}" for c in FUENTES) + ")")
    print(f"Salida: {raiz / SALIDA_CONSOLIDADO_V2}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Construye el corpus consolidado v2 (MET, CMA y AIC).")
    parser.add_argument("--root", default=".", help="Raiz del repositorio.")
    return construir(Path(parser.parse_args(argv).root).resolve())


if __name__ == "__main__":
    raise SystemExit(main())
