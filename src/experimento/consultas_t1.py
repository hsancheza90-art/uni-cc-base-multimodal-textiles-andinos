"""Consultas de la tarea T1 (texto a imagen): workbook del evaluador y su validación.

Uso desde la raíz del repositorio:

    python -m src.experimento.consultas_t1 --crear   # crea o actualiza el workbook (conserva lo escrito)
    python -m src.experimento.consultas_t1           # valida y exporta (paso del flujo)

El evaluador redacta en data/metadata/consultas_t1_v2.xlsx las consultas de [consultas_t1] de
config/experimento.toml: una descripción en español de lo que busca, sin copiar fichas, y una
especificación estructural opcional (composición y palabra de bandas) que usa M3. Se redactan
antes de ejecutar cualquier sistema sobre ellas (protocolo, sección 5). La hoja «ejemplos» tiene
casos hipotéticos de referencia: no son consultas ni piezas de la galería.

La validación exige autor y fecha a toda consulta con descripción y comprueba la especificación
contra config/vocabulario.toml. Con errores termina con código 1 y no actualiza
data/metadata/consultas_t1_v2.csv, que tiene siempre una fila por consulta (vacía si falta).
"""

from __future__ import annotations

import argparse
from pathlib import Path

from src.anotacion.aplicar_anotaciones import fecha_valida
from src.experimento.libro import escribir_libro
from src.utils.archivos import escribir_csv, escribir_texto
from src.utils.config import CONFIG_EXPERIMENTO, leer_config_experimento
from src.utils.libros import leer_hoja
from src.utils.vocabulario import leer_vocabulario

WORKBOOK_T1 = Path("data/metadata/consultas_t1_v2.xlsx")
HOJA_T1 = "consultas"
SALIDA_T1 = "data/metadata/consultas_t1_v2.csv"
REPORTE_T1 = "outputs/reports/experimento_v2_consultas_t1.md"
EDITABLES = ["descripcion", "composicion", "secuencia_bandas", "autor", "fecha_redaccion", "observaciones"]
COLUMNAS = ["consulta"] + EDITABLES

EJEMPLOS = (
    ["ejemplo", "descripcion", "composicion", "secuencia_bandas", "por_que_sirve"],
    [
        {"ejemplo": "E1", "descripcion": "Faja estrecha con bandas horizontales que alternan franjas lisas y franjas de "
                                         "rombos escalonados.", "composicion": "bandas",
         "secuencia_bandas": "lisa > geometrica > lisa > geometrica > lisa",
         "por_que_sirve": "Describe la organizacion (bandas y su alternancia) sin nombrar colores ni culturas."},
        {"ejemplo": "E2", "descripcion": "Pano con un campo central sin decorar rodeado por un borde de aves de perfil.",
         "composicion": "campo_central", "secuencia_bandas": "",
         "por_que_sirve": "Composicion distinta de bandas: la palabra de bandas queda vacia."},
        {"ejemplo": "E3", "descripcion": "Tejido en reticula de cuadros que alternan una figura humana frontal y un "
                                         "motivo geometrico.", "composicion": "reticula", "secuencia_bandas": "",
         "por_que_sirve": "Nombra la reticula y la alternancia de sus celdas."},
        {"ejemplo": "E4", "descripcion": "Tela de paneles verticales contiguos, cada uno con un felino estilizado.",
         "composicion": "paneles", "secuencia_bandas": "",
         "por_que_sirve": "Paneles con una figura que se repite; sin especificacion de bandas."},
    ],
)

GUIA = [
    "Consultas T1: texto a imagen (protocolo experimental v2, secciones 3 y 5)",
    "",
    "1. Redacte en 'descripcion' lo que busca, en espanol y con sus palabras: la organizacion visible (bandas, campo",
    "   central, reticula, paneles, borde), lo que se repite y los motivos. No copie titulos ni fichas de museo.",
    "2. Opcional: 'composicion' (lista) y 'secuencia_bandas' (tipos de banda en orden, separados por ' > ': lisa,",
    "   geometrica, figurativa, mixta, no_determinada). Solo si la descripcion los implica; los usa M3.",
    "3. 'autor' y 'fecha_redaccion' (AAAA-MM-DD) en cada consulta redactada.",
    "4. Redacte todas antes de ver cualquier ranking. La hoja 'ejemplos' tiene casos hipoteticos de referencia: no",
    "   son consultas ni piezas de la galeria; no los copie.",
    "",
    "Despues: python -m src.flujo valida las consultas y las exporta a data/metadata/consultas_t1_v2.csv.",
]


def codigos_consultas(config: dict) -> list[str]:
    return [f"T1-P{n:02d}" for n in range(1, int(config["consultas_t1"]["prueba"]) + 1)]


def crear(raiz: Path) -> int:
    config = leer_config_experimento(raiz)
    ruta = raiz / WORKBOOK_T1
    previas = {f["consulta"]: f for f in leer_hoja(ruta, HOJA_T1, clave="consulta")} if ruta.exists() else {}
    filas = [{"consulta": c, **{k: previas.get(c, {}).get(k, "") for k in EDITABLES}} for c in codigos_consultas(config)]
    composiciones = [c for c in leer_vocabulario(raiz)["composicion"].codigos]
    try:
        escribir_libro(ruta, GUIA, HOJA_T1, COLUMNAS, filas, EDITABLES,
                       {"descripcion": 70, "secuencia_bandas": 40, "observaciones": 40},
                       {"composicion": composiciones}, EJEMPLOS)
    except PermissionError:
        print(f"No se pudo escribir {WORKBOOK_T1}: cierre el archivo en Excel.")
        return 1
    print(f"Workbook de consultas T1: {ruta} ({len(filas)} consultas, {sum(bool(f['descripcion']) for f in filas)} redactadas)")
    return 0


def validar(raiz: Path) -> int:
    ruta = raiz / WORKBOOK_T1
    if not ruta.exists():
        print(f"No existe {WORKBOOK_T1}: las consultas T1 aun no se han creado.")
        return 0
    config = leer_config_experimento(raiz)
    vocabulario = leer_vocabulario(raiz)
    filas = {f["consulta"]: f for f in leer_hoja(ruta, HOJA_T1, clave="consulta")}
    errores, salida = [], []
    for codigo in codigos_consultas(config):
        fila = {k: filas.get(codigo, {}).get(k, "") for k in EDITABLES}
        if fila["composicion"] and fila["composicion"] not in vocabulario["composicion"].codigos:
            errores.append(f"{codigo}: composicion '{fila['composicion']}' no esta en el vocabulario")
        if fila["secuencia_bandas"]:
            fila["secuencia_bandas"] = vocabulario["secuencia_bandas"].recodificar(fila["secuencia_bandas"])
            invalidos = vocabulario["secuencia_bandas"].invalidos(fila["secuencia_bandas"])
            if invalidos:
                errores.append(f"{codigo}: secuencia_bandas fuera del vocabulario: {invalidos}")
        if fila["descripcion"]:
            if not fila["autor"]:
                errores.append(f"{codigo}: autor vacio")
            if not fecha_valida(fila["fecha_redaccion"]):
                errores.append(f"{codigo}: fecha_redaccion vacia o invalida (AAAA-MM-DD)")
        elif any(fila[k] for k in ("composicion", "secuencia_bandas")):
            errores.append(f"{codigo}: especificacion estructural sin descripcion")
        salida.append({"consulta": codigo, **fila})
    extra = sorted(set(filas) - set(codigos_consultas(config)))
    if extra:
        errores.append(f"Consultas que no estan en la configuracion: {extra}")
    redactadas = sum(bool(f["descripcion"]) for f in salida)
    escribir_texto(raiz / REPORTE_T1, [
        "# Consultas T1 (texto a imagen)",
        "",
        f"Generado por `python -m src.experimento.consultas_t1`, paso del flujo. Workbook: `{WORKBOOK_T1.as_posix()}`; "
        f"numero de consultas en `{CONFIG_EXPERIMENTO.as_posix()}` ([consultas_t1]).",
        "",
        f"- Redactadas: {redactadas} de {len(salida)}; con especificacion estructural: "
        f"{sum(bool(f['composicion'] or f['secuencia_bandas']) for f in salida)}.",
        "- Se redactan antes de ejecutar cualquier sistema sobre ellas; no se ha ejecutado ninguna.",
        "",
        "## Errores",
        "",
    ] + ([f"- {e}" for e in errores] if errores else ["Ninguno."]))
    if errores:
        print(f"Consultas T1 con {len(errores)} errores; no se actualizo {SALIDA_T1}.")
        for error in errores:
            print(f"- {error}")
        return 1
    escribir_csv(raiz / SALIDA_T1, COLUMNAS, salida)
    print(f"Consultas T1: {redactadas} de {len(salida)} redactadas -> {SALIDA_T1}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Consultas T1: workbook del evaluador y validacion.")
    parser.add_argument("--root", default=".", help="Raiz del repositorio.")
    parser.add_argument("--crear", action="store_true", help="Crea o actualiza el workbook conservando lo escrito.")
    args = parser.parse_args(argv)
    raiz = Path(args.root).resolve()
    return crear(raiz) if args.crear else validar(raiz)


if __name__ == "__main__":
    raise SystemExit(main())
