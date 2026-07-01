from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


ARCHIVOS_ESPERADOS = {
    "principal": {
        "ruta": "data/metadata/met_corpus_principal_v2.csv",
        "conteo": 132,
        "estado": "corpus_principal",
    },
    "secundario": {
        "ruta": "data/metadata/met_corpus_secundario_v2.csv",
        "conteo": 50,
        "estado": "corpus_secundario",
    },
    "descartados": {
        "ruta": "data/metadata/met_descartados_v2.csv",
        "conteo": 29,
        "estado": "descartado",
    },
}

COLUMNAS_REQUERIDAS = [
    "fuente",
    "id_fuente",
    "id_registro",
    "institucion",
    "titulo_original",
    "cultura",
    "material",
    "descripcion",
    "url_objeto",
    "url_imagen",
    "estado_curacion",
    "destino_curacion",
    "origen_curacion",
    "motivo_curacion",
]


def leer_csv(ruta: Path) -> tuple[list[str], list[dict[str, str]]]:
    with ruta.open(newline="", encoding="utf-8-sig") as archivo:
        lector = csv.DictReader(archivo)
        return list(lector.fieldnames or []), list(lector)


def auditar_archivo(nombre: str, config: dict[str, object], raiz: Path) -> list[str]:
    problemas: list[str] = []

    ruta = raiz / str(config["ruta"])
    conteo_esperado = int(config["conteo"])
    estado_esperado = str(config["estado"])

    if not ruta.exists():
        return [f"{nombre}: falta archivo {ruta}"]

    texto = ruta.read_text(encoding="utf-8", errors="replace")
    if "Forbidden. Calls to this URL" in texto:
        problemas.append(f"{nombre}: contiene mensaje Forbidden en lugar de datos validos")

    columnas, filas = leer_csv(ruta)

    faltantes = [columna for columna in COLUMNAS_REQUERIDAS if columna not in columnas]
    if faltantes:
        problemas.append(f"{nombre}: faltan columnas requeridas: {', '.join(faltantes)}")
        return problemas

    if len(filas) != conteo_esperado:
        problemas.append(
            f"{nombre}: conteo esperado {conteo_esperado}, conteo observado {len(filas)}"
        )

    ids_vistos: set[str] = set()
    ids_duplicados: set[str] = set()

    for numero_fila, fila in enumerate(filas, start=2):
        id_fuente = (fila.get("id_fuente") or "").strip()
        estado = (fila.get("estado_curacion") or "").strip()
        url_objeto = (fila.get("url_objeto") or "").strip()
        url_imagen = (fila.get("url_imagen") or "").strip()
        motivo = (fila.get("motivo_curacion") or "").strip()

        if not id_fuente:
            problemas.append(f"{nombre}: fila {numero_fila} sin id_fuente")
        elif id_fuente in ids_vistos:
            ids_duplicados.add(id_fuente)
        ids_vistos.add(id_fuente)

        if estado != estado_esperado:
            problemas.append(
                f"{nombre}: fila {numero_fila} tiene estado_curacion={estado}, esperado={estado_esperado}"
            )

        if not url_objeto:
            problemas.append(f"{nombre}: fila {numero_fila} sin url_objeto")

        if nombre != "descartados" and not url_imagen:
            problemas.append(f"{nombre}: fila {numero_fila} sin url_imagen")

        if not motivo:
            problemas.append(f"{nombre}: fila {numero_fila} sin motivo_curacion")

    if ids_duplicados:
        muestra = ", ".join(sorted(ids_duplicados)[:10])
        problemas.append(f"{nombre}: id_fuente duplicados: {muestra}")

    return problemas


def escribir_reporte(ruta: Path, problemas: list[str]) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)

    lineas = [
        "# Auditoria tecnica MET v2",
        "",
        "Esta auditoria valida las salidas normalizadas de MET v2: conteos, columnas, identificadores, estados de curacion y trazabilidad minima.",
        "",
    ]

    if problemas:
        lineas.extend(["## Hallazgos", ""])
        lineas.extend(f"- {problema}" for problema in problemas)
    else:
        lineas.extend([
            "## Resultado",
            "",
            "Sin hallazgos criticos. Las salidas MET v2 cumplen los controles definidos.",
        ])

    ruta.write_text("\n".join(lineas) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audita las salidas curatoriales MET v2.")
    parser.add_argument("--root", default=".", help="Raiz del repositorio.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    raiz = Path(args.root).resolve()

    problemas: list[str] = []
    for nombre, config in ARCHIVOS_ESPERADOS.items():
        problemas.extend(auditar_archivo(nombre, config, raiz))

    escribir_reporte(raiz / "outputs/reports/met_auditoria_tecnica_v2.md", problemas)

    if problemas:
        print("Hallazgos de auditoria:")
        for problema in problemas:
            print(f"- {problema}")
        return 1

    print("Auditoria MET v2 sin hallazgos criticos.")
    return 0


if __name__ == "__main__":
    sys.exit(main())