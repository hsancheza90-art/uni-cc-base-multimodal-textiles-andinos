"""Construye el corpus principal v2 (MET, CMA y AIC) con el esquema armonizado.

Uso desde la raiz del repositorio (lo ejecuta el flujo):

    python -m src.anotacion.corpus_v2

Une los CSV principales revisados de cada fuente (rutas de src/utils/fuentes.py) en
data/processed/corpus_textiles_andinos_v2_principal.csv, con las columnas de
src/consolidado/esquema.py y, al final, el puntaje de aptitud de cada imagen.

Cada registro se completa con su registro de origen, que guarda los datos oficiales que
el workbook de revisión no copia (institución, licencia, clasificación, fecha): la lista de
candidatos del colector en CMA y AIC y, en MET, el inventario de la descarga de la API más
las salidas base v2 (que conservan la descripción curada). Ninguno se modifica. Los campos
normalizados (tipo de objeto, material y técnica) se resuelven con las mismas reglas del
consolidado v1; un valor curado que no está en el vocabulario no se acepta como
normalizado y lo reemplaza la regla. Lo que ninguna entrada registra queda vacío.

Imagen: la copia de evaluación de 1600 px (data/metadata/imagenes_evaluacion_manifiesto_v2.csv),
que es la imagen sobre la que se anota.

No lee nada bajo data/metadata/v1_congelado/ ni escribe archivos con _v1_ en el nombre; el
único archivo _v1_ que lee es el inventario MET (autorizado el 2026-10-20 como registro de
origen, como ya lo hacía src/imagenes/aptitud.py).
"""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

from src.consolidado.construir_consolidado import (
    aplicar_anotacion,
    estado_imagen,
    estado_metadatos,
    marcar_duplicados,
    normalizar_campos,
    primero,
)
from src.consolidado.esquema import COLUMNAS, OBLIGATORIOS
from src.imagenes.aptitud import SALIDA_APTITUD
from src.imagenes.descargar_evaluacion import MANIFIESTO_EVALUACION
from src.utils.archivos import escribir_csv, escribir_texto, indexar, leer_csv
from src.utils.config import leer_config
from src.utils.fuentes import FUENTES
from src.utils.metricas import tabla
from src.utils.vocabulario import Campo, leer_vocabulario

SALIDA_PRINCIPAL_V2 = "data/processed/corpus_textiles_andinos_v2_principal.csv"
SALIDA_REPORTE = "outputs/reports/corpus_textiles_andinos_v2_principal_resumen.md"

# Columnas de la ficha de aptitud que acompañan al registro (src/imagenes/aptitud.py).
COLUMNAS_APTITUD = ["puntaje_aptitud", "banda_sugerida", "referencia_sugerida"]
COLUMNAS_V2 = COLUMNAS + COLUMNAS_APTITUD

# Campos normalizados cuyo valor curado debe estar en el vocabulario para aceptarse como tal.
NORMALIZADOS = ["tipo_objeto", "tipo_superficie", "material_normalizado", "tecnica_normalizada"]

ORDEN_FUENTES = {codigo: posicion for posicion, codigo in enumerate(FUENTES)}


def clave_orden(fila: dict[str, str]) -> tuple[int, int, str]:
    id_fuente = fila["id_fuente"]
    return (ORDEN_FUENTES[fila["fuente"]], int(id_fuente) if id_fuente.isdigit() else 0, id_fuente)


# --------------------------------------------------------------------------- registros de origen


def base_met(raiz: Path) -> dict[str, dict[str, str]]:
    """Salidas base v2 de MET (principal, secundario y descartados), por id_fuente.

    Son la reorganización del corpus MET v1 que hace build_met_corpus_v2; de ellas se toma
    la descripción curada, que el inventario de la API no trae.
    """
    filas = []
    for datos in leer_config(raiz)["met"]["base"].values():
        if isinstance(datos, dict):
            filas += leer_csv(raiz / datos["ruta"])
    return indexar(filas, "id_fuente")


def origenes(raiz: Path) -> dict[str, dict[str, dict[str, str]]]:
    """Registro de origen de cada fuente por id_fuente; en MET, con la base v2 en columnas base_*."""
    salida = {
        codigo: indexar(leer_csv(raiz / fuente.candidatos), fuente.clave_candidatos)
        for codigo, fuente in FUENTES.items()
    }
    for id_fuente, fila in base_met(raiz).items():
        if id_fuente in salida["MET"]:
            salida["MET"][id_fuente].update({f"base_{clave}": valor for clave, valor in fila.items()})
    return salida


# --------------------------------------------------------------------------- campos por fuente


def campos_met(rev: dict[str, str], org: dict[str, str]) -> dict[str, str]:
    """Mismas equivalencias que el consolidado v1 (registros_met), con el inventario como origen."""
    return {
        "institucion": org["institucion"],
        "url_objeto": primero(rev["url_objeto"], org["url_objeto"]),
        "url_imagen": primero(rev["url_imagen"], org["url_imagen"]),
        "url_imagen_miniatura": org["url_imagen_miniatura"],
        "titulo_original": primero(rev["titulo_original"], org["titulo_original"]),
        "titulo_es_sugerido": primero(rev["titulo_es_sugerido"], org["titulo_es_sugerido"]),
        "descripcion": org.get("base_descripcion", ""),
        "cultura": primero(rev["cultura"], org["cultura"]),
        "periodo": org["periodo"],
        "fecha_objeto": primero(rev["fecha_objeto"], org["fecha_objeto"]),
        "procedencia": primero(rev["procedencia"], "; ".join(v for v in (org["pais"], org["region"]) if v)),
        "departamento": org["departamento_museo"],
        "clasificacion_original": org["clasificacion_original"],
        "nombre_objeto_original": org["nombre_objeto_original"],
        "material": primero(rev["material"], org["material_original"]),
        # La API del MET no entrega tecnica; la de la curacion ya esta normalizada (igual que en v1).
        "tecnica": "",
        "tecnica_normalizada": rev["tecnica"],
        "dimensiones": org["dimensiones"],
        "estado_licencia": "dominio_publico" if org["es_dominio_publico"] == "True" else "",
        "licencia_fuente": f"isPublicDomain={org['es_dominio_publico']}",
        "derechos_reproduccion": org["derechos_reproduccion"],
        "consulta_origen": org["termino_busqueda"],
        "fecha_descarga_metadatos": org["fecha_descarga"],
    }


def campos_cma(rev: dict[str, str], org: dict[str, str]) -> dict[str, str]:
    return {
        "numero_acceso": org["accession_number"],
        "institucion": org["source"],
        "url_objeto": primero(rev["url_objeto"], org["url"]),
        "url_imagen": primero(rev["url_imagen"], org["image_url"]),
        "titulo_original": primero(rev["titulo_original"], org["title"]),
        "descripcion": org["description"],
        "cultura": primero(rev["cultura"], org["culture"]),
        "fecha_objeto": primero(rev["fecha_objeto"], org["creation_date"]),
        "departamento": org["department"],
        "clasificacion_original": org["classification"],
        "material": primero(rev["material"], org["medium"]),
        "tecnica": primero(rev["tecnica"], org["technique"]),
        "categoria_revision": org["curation_status"],
        "estado_licencia": "cc0" if org["share_license_status"] == "CC0" else "",
        "licencia_fuente": f"share_license_status={org['share_license_status']}",
        "terminos_andinos": org["andean_terms"],
        "terminos_textiles": org["textile_terms"],
        "consulta_origen": org["raw_queries"],
    }


def campos_aic(rev: dict[str, str], org: dict[str, str]) -> dict[str, str]:
    cc0 = org["es_dominio_publico"] == "True" and org["licencia_imagen"] == "CC0"
    return {
        "numero_acceso": org["numero_acceso"],
        "institucion": org["fuente"],
        "url_objeto": primero(rev["url_objeto"], org["url_objeto"]),
        "url_imagen": primero(rev["url_imagen"], org["url_imagen"]),
        "url_imagen_miniatura": org["url_imagen_miniatura"],
        "titulo_original": primero(rev["titulo_original"], org["titulo_original"]),
        "descripcion": org["descripcion"],
        "cultura": primero(rev["cultura"], org["cultura"]),
        "fecha_objeto": primero(rev["fecha_objeto"], org["fecha_objeto"]),
        "procedencia": primero(rev["procedencia"], org["procedencia"]),
        "departamento": org["departamento"],
        "clasificacion_original": org["clasificacion_original"],
        "nombre_objeto_original": org["tipo_objeto_original"],
        "material": primero(rev["material"], org["material"]),
        "tecnica": primero(rev["tecnica"], org["tecnicas"]),
        "dimensiones": org["dimensiones"],
        "categoria_revision": org["sugerencia_corpus"],
        "estado_licencia": "cc0" if cc0 else "",
        "licencia_fuente": f"is_public_domain={org['es_dominio_publico']}; licencia_imagen={org['licencia_imagen']}",
        # La descripcion de AIC no es CC0: se cita con su licencia.
        "derechos_reproduccion": f"descripcion: {org['licencia_descripcion']}" if org["licencia_descripcion"] else "",
        "terminos_andinos": org["terminos_andinos"],
        "terminos_textiles": org["terminos_textiles"],
        "consulta_origen": org["consultas_origen"],
        "fecha_descarga_metadatos": org["fecha_descarga"],
    }


CAMPOS_FUENTE = {"MET": campos_met, "CMA": campos_cma, "AIC": campos_aic}


def registro(codigo: str, rev: dict[str, str], org: dict[str, str], archivo: str) -> dict[str, str]:
    fila = {campo: "" for campo in COLUMNAS}
    fila.update({
        "id_global": f"{codigo}:{rev['id_fuente']}",
        "fuente": codigo,
        "id_fuente": rev["id_fuente"],
        "titulo_es_sugerido": rev["titulo_es_sugerido"],
        "procedencia": rev["procedencia"],
        "tipo_objeto": rev["tipo_objeto"],
        "tipo_superficie": rev["tipo_superficie"],
        "material_normalizado": rev["material_normalizado"],
        "decision_curacion_final": "principal",
        "motivo_curacion_final": primero(rev["motivo_curacion"], rev["motivo_revision"]),
        "decision_auditoria": rev["decision_revision"],
        "motivo_auditoria": rev["motivo_revision"],
        "observacion_auditoria": rev["observaciones_revision"],
        "origen_curacion": rev["origen_curacion"],
        "archivo_origen": archivo,
    })
    fila.update(CAMPOS_FUENTE[codigo](rev, org))
    return fila


# --------------------------------------------------------------------------- armonizacion


def descartar_fuera_de_vocabulario(
    fila: dict[str, str], vocabulario: dict[str, Campo]
) -> list[tuple[str, str, str]]:
    """Vacía los valores curados que no están en el vocabulario (la regla los reemplaza).

    Devuelve (fuente, campo, valor) de cada valor descartado, para el informe; el texto
    original de la fuente se conserva en clasificacion_original, material o tecnica.
    """
    descartados = []
    for campo in NORMALIZADOS:
        valor = fila[campo]
        if valor and vocabulario[campo].invalidos(vocabulario[campo].recodificar(valor)):
            descartados.append((fila["fuente"], campo, valor))
            fila[campo] = ""
    return descartados


def completar_imagen(fila: dict[str, str], imagen: dict[str, str] | None, lado_minimo: int) -> None:
    ok = bool(imagen and imagen["estado_descarga"] == "ok" and imagen["ruta_copia_evaluacion"])
    fila["ruta_imagen_local"] = imagen["ruta_copia_evaluacion"] if ok else ""
    fila["imagen_sha256"] = imagen["sha256_copia"] if ok else ""
    fila["imagen_ancho"] = imagen["ancho_copia"] if ok else ""
    fila["imagen_alto"] = imagen["alto_copia"] if ok else ""
    datos = {"estado_descarga": "ok", "imagen_ancho": fila["imagen_ancho"], "imagen_alto": fila["imagen_alto"]} if ok else None
    fila["estado_imagen"] = estado_imagen(datos, lado_minimo)
    fila["imagen_sha256_pixeles"] = ""  # agrupar_duplicados lo consulta; el manifiesto v2 no lo registra


def construir_registros(raiz: Path) -> tuple[list[dict[str, str]], list[tuple[str, str, str]], list[str]]:
    """Registros armonizados del principal v2, valores descartados por vocabulario y problemas de integridad."""
    vocabulario = leer_vocabulario(raiz)
    por_fuente = origenes(raiz)
    lado_minimo = int(leer_config(raiz)["consolidado"]["parametros"]["lado_minimo_imagen"])
    manifiesto = indexar(leer_csv(raiz / MANIFIESTO_EVALUACION), "id_global")
    aptitud = indexar(leer_csv(raiz / SALIDA_APTITUD), "id_global")

    registros: list[dict[str, str]] = []
    descartados: list[tuple[str, str, str]] = []
    problemas: list[str] = []
    for codigo, fuente in FUENTES.items():
        archivo = fuente.salidas["principal"]
        for rev in leer_csv(raiz / archivo):
            org = por_fuente[codigo].get(rev["id_fuente"])
            if org is None:
                problemas.append(f"{codigo}:{rev['id_fuente']}: no esta en el registro de origen de la fuente")
                continue
            fila = registro(codigo, rev, org, archivo)
            descartados += descartar_fuera_de_vocabulario(fila, vocabulario)
            normalizar_campos(fila, vocabulario)
            completar_imagen(fila, manifiesto.get(fila["id_global"]), lado_minimo)
            aplicar_anotacion(fila, None)  # la anotacion estructural no entra aqui: sin_anotar
            fila["estado_metadatos"] = estado_metadatos(fila)
            ficha = aptitud.get(fila["id_global"], {})
            for columna in COLUMNAS_APTITUD:
                fila[columna] = ficha.get(columna, "")
            registros.append(fila)

    registros.sort(key=clave_orden)
    marcar_duplicados(registros, clave_orden)
    return registros, descartados, problemas + validar(registros, vocabulario)


def validar(registros: list[dict[str, str]], vocabulario: dict[str, Campo]) -> list[str]:
    """Errores que detienen el flujo: identificadores repetidos o mal formados y valores fuera del vocabulario."""
    problemas: list[str] = []
    repetidos = sorted(id_ for id_, n in Counter(f["id_global"] for f in registros).items() if n > 1)
    if repetidos:
        problemas.append(f"id_global repetidos entre fuentes: {repetidos[:10]}")
    controlados = [campo for campo in vocabulario.values() if campo.nombre in COLUMNAS]
    for fila in registros:
        if fila["id_global"] != f"{fila['fuente']}:{fila['id_fuente']}":
            problemas.append(f"{fila['id_global']}: id_global no coincide con fuente:id_fuente")
        for campo in controlados:
            invalidos = campo.invalidos(fila[campo.nombre])
            if invalidos:
                problemas.append(f"{fila['id_global']}: {campo.nombre} fuera del vocabulario: {invalidos}")
    return problemas


# --------------------------------------------------------------------------- informe


def lineas_reporte(registros: list[dict[str, str]], descartados: list[tuple[str, str, str]]) -> list[str]:
    fuentes = list(FUENTES)
    de = {codigo: [f for f in registros if f["fuente"] == codigo] for codigo in fuentes}
    lineas = [
        "# Corpus principal v2 (MET, CMA y AIC)",
        "",
        "Resumen generado por `python -m src.flujo` (`src/anotacion/corpus_v2.py`). Archivo: "
        f"`{SALIDA_PRINCIPAL_V2}`, con el esquema de `docs/esquema_consolidado_met_cma_v1.md` y tres columnas "
        "de aptitud al final.",
        "",
        "## Registros",
        "",
    ]
    filas = [[codigo, str(len(de[codigo])), FUENTES[codigo].salidas["principal"]] for codigo in fuentes]
    lineas += tabla(filas + [["Total", str(len(registros)), ""]], ["Fuente", "Registros", "CSV revisado"])

    sin_aptitud = [f["id_global"] for f in registros if not f["banda_sugerida"]]
    lineas += [
        "",
        "## Aptitud",
        "",
        f"Registros sin fila en `{SALIDA_APTITUD}`: {len(sin_aptitud)}"
        + (f" ({', '.join(sin_aptitud)})." if sin_aptitud else "."),
        "Un registro sin ficha no se descarta: queda con las columnas de aptitud vacias.",
        "",
    ]
    bandas = sorted({f["banda_sugerida"] for f in registros})
    lineas += tabla(
        [[banda or "(vacia)"] + [str(sum(f["banda_sugerida"] == banda for f in de[c])) for c in fuentes] for banda in bandas],
        ["banda_sugerida"] + fuentes,
    )

    lineas += [
        "",
        "## Campos normalizados: origen del valor",
        "",
        "`curacion`: valor curado en el workbook de revision; `regla`: regla automatica sobre el texto de la fuente "
        "(`src/preprocessing/normalizacion.py`, `src/preprocessing/surface_filters.py`), que la anotacion debe validar; "
        "vacio: ninguna regla lo determina.",
        "",
    ]
    filas = []
    for campo in ("tipo_objeto", "material_normalizado", "tecnica_normalizada"):
        for origen in ("curacion", "regla", ""):
            filas.append([f"`{campo}`", origen or "(vacio)"] + [
                str(sum(f[f"origen_{campo}"] == origen for f in de[c])) for c in fuentes
            ])
    lineas += tabla(filas, ["Campo", "Origen"] + fuentes)

    lineas += [
        "",
        "## Valores curados fuera del vocabulario",
        "",
        "No se aceptan como normalizados: se vacian y, salvo en `tipo_superficie`, la regla calcula el valor. El texto "
        "de la fuente queda en `clasificacion_original`, `nombre_objeto_original`, `material` o `tecnica`.",
        "",
    ]
    if descartados:
        conteo = Counter(descartados)
        lineas += tabla(
            [[fuente, f"`{campo}`", valor, str(n)] for (fuente, campo, valor), n in sorted(conteo.items())],
            ["Fuente", "Campo", "Valor", "Registros"],
        )
    else:
        lineas.append("Ninguno.")

    lineas += ["", "## Cobertura de campos (registros con valor)", ""]
    lineas += tabla(
        [[f"`{campo}`"] + [f"{sum(bool(f[campo]) for f in de[c])}/{len(de[c])}" for c in fuentes] for campo in COLUMNAS_V2],
        ["Campo"] + fuentes,
    )

    lineas += [
        "",
        "## Campos obligatorios vacios",
        "",
        "Se informan y no detienen el flujo: un valor que ninguna entrada registra no se completa (no se imputa).",
        "",
    ]
    vacios = [(f["id_global"], c) for f in registros for c in OBLIGATORIOS if not f[c]]
    if vacios:
        lineas += tabla([[id_, f"`{c}`"] for id_, c in vacios], ["Registro", "Campo"])
    else:
        lineas.append("Ninguno.")

    for campo in ("estado_metadatos", "estado_imagen", "estado_licencia"):
        lineas += ["", f"## {campo}", ""]
        valores = sorted({f[campo] for f in registros})
        lineas += tabla(
            [[v or "(vacio)"] + [str(sum(f[campo] == v for f in de[c])) for c in fuentes] for v in valores],
            ["Valor"] + fuentes,
        )

    lineas += ["", "## Imagenes compartidas entre registros", ""]
    grupos: dict[str, list[str]] = {}
    for fila in registros:
        if fila["grupo_imagen_duplicada"]:
            grupos.setdefault(fila["grupo_imagen_duplicada"], []).append(fila["id_global"])
    if grupos:
        lineas += [
            "Misma `url_imagen` o mismo archivo de la copia de evaluacion (SHA-256). Se conservan: son objetos "
            "distintos del museo que comparten fotografia.",
            "",
        ]
        lineas += tabla([[g, ", ".join(ids)] for g, ids in sorted(grupos.items())], ["Grupo", "Registros"])
    else:
        lineas.append("No se detectaron registros que compartan imagen. Los fragmentos de una misma pieza entre "
                      "museos (dHash) se evaluan en el consolidado v2.")
    lineas += [
        "",
        "## Criterios",
        "",
        "- Registro de origen (`src/utils/fuentes.py`): candidatos de CMA y AIC; en MET, el inventario de la "
        "descarga de la API y, para la descripcion curada, las salidas base v2 (`config/corpus.toml` [met.base]). "
        "El valor del workbook tiene prioridad; el de origen lo completa si esta vacio. Ninguno se modifica.",
        "- Imagen: copia de evaluacion de 1600 px (`ruta_imagen_local`, `imagen_sha256`, `imagen_ancho`, "
        "`imagen_alto`); `estado_imagen` usa el mismo lado minimo que el consolidado v1.",
        "- `estado_anotacion` es `sin_anotar` en todos los registros: la anotacion estructural no se lee aqui.",
    ]
    return lineas


# --------------------------------------------------------------------------- principal


def construir(raiz: Path) -> int:
    registros, descartados, problemas = construir_registros(raiz)
    if problemas:
        print("Problemas en el corpus principal v2:")
        for problema in problemas:
            print(f"- {problema}")
        return 1
    escribir_csv(raiz / SALIDA_PRINCIPAL_V2, COLUMNAS_V2, [{c: f[c] for c in COLUMNAS_V2} for f in registros])
    escribir_texto(raiz / SALIDA_REPORTE, lineas_reporte(registros, descartados))
    conteo = Counter(f["fuente"] for f in registros)
    print(f"Corpus principal v2: {len(registros)} registros ({', '.join(f'{c} {conteo[c]}' for c in FUENTES)})")
    print(f"Salida: {raiz / SALIDA_PRINCIPAL_V2}")
    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Construye el corpus principal v2 (MET, CMA y AIC).")
    parser.add_argument("--root", default=".", help="Raiz del repositorio.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    return construir(Path(parse_args(argv).root).resolve())


if __name__ == "__main__":
    raise SystemExit(main())
