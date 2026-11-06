"""Pruebas de los grupos v2: senales de candidatos, decisiones del workbook y grupos por transitividad."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest
from openpyxl import load_workbook

from src.anotacion.corpus_v2 import SALIDA_COMPLEMENTARIO_V2, SALIDA_PRINCIPAL_V2
from src.anotacion.nucleo import SALIDA_NUCLEO
from src.grupos import grupos, workbook
from src.imagenes.descargar_evaluacion import MANIFIESTO_EVALUACION
from src.imagenes.dhash_evaluacion import SALIDA_DHASH
from src.modelos.embeddings import EMBEDDINGS_M2, INDICE_M2, Embeddings, normalizar_l2
from src.utils.archivos import leer_csv
from src.utils.config import leer_config_grupos
from tests.insumos import copiar_insumos


def test_base_de_inventario_quita_solo_el_sufijo_de_parte() -> None:
    assert grupos.base_inventario("1922.395.a") == "1922.395"
    assert grupos.base_inventario("1955.1601a-b") == "1955.1601"
    assert grupos.base_inventario("1956.99D") == "1956.99"
    assert grupos.base_inventario("1956.74") == "1956.74"  # sin sufijo, el numero completo


def pieza(id_global: str, fuente: str, **campos: str) -> dict[str, str]:
    return {"id_global": id_global, "fuente": fuente, "imagen_sha256": "", "grupo_imagen_duplicada": "",
            "numero_acceso": "", "descripcion": "", **campos}


def test_cada_senal_propone_su_par_y_el_umbral_entre_museos_es_mas_bajo() -> None:
    texto = "Fragmento de tunica con bandas de aves y peces en tapiz de algodon y camelido."
    principal = [
        pieza("AIC:1", "AIC", numero_acceso="1955.1a", imagen_sha256="x"),
        pieza("AIC:2", "AIC", numero_acceso="1955.1b", imagen_sha256="x"),
        pieza("AIC:3", "AIC", descripcion=texto),
        pieza("CMA:4", "CMA", descripcion=texto.upper()),
        pieza("MET:5", "MET"),
        pieza("CMA:6", "CMA"),
        pieza("MET:7", "MET"),
        pieza("MET:8", "MET"),
    ]
    dhash = {"MET:7": {"sha256_copia": "a", "dhash": "ffff000000000000"},
             "MET:8": {"sha256_copia": "b", "dhash": "ffff000000000007"}}  # 3 bits de diferencia
    angulo = np.deg2rad(20)  # coseno 0,94: sobre 0,93 entre museos y bajo 0,95 dentro de un museo
    vectores = np.zeros((8, 3))
    vectores[:, 2] = 1
    vectores[4] = [1, 0, 0]
    vectores[5] = [np.cos(angulo), np.sin(angulo), 0]
    embeddings = Embeddings([p["id_global"] for p in principal], normalizar_l2(vectores).astype(np.float32))
    config = leer_config_grupos()["candidatos"]

    pares = {p["par"]: p for p in grupos.candidatos(principal, dhash, None, config)}
    assert pares["AIC:1 | AIC:2"]["senales"] == "imagen_identica; inventario"
    assert pares["AIC:1 | AIC:2"]["decision_sugerida"] == "unir" and pares["AIC:1 | AIC:2"]["inventario_base"] == "1955.1"
    assert pares["AIC:3 | CMA:4"]["senales"] == "descripcion"  # ignora mayusculas y espacios
    assert pares["MET:7 | MET:8"]["senales"] == "dhash" and pares["MET:7 | MET:8"]["distancia_dhash"] == "3"

    con_m2 = {p["par"]: p for p in grupos.candidatos(principal, dhash, embeddings, config)}
    assert con_m2["CMA:6 | MET:5"]["senales"] == "m2" and con_m2["CMA:6 | MET:5"]["coseno_m2"] == "0.9397"
    principal[5]["fuente"] = "MET"  # el mismo coseno dentro de un museo no alcanza 0,95
    assert "CMA:6 | MET:5" not in {p["par"] for p in grupos.candidatos(principal, dhash, embeddings, config)}


def test_agrupar_une_por_transitividad_y_conserva_el_orden() -> None:
    componentes = grupos.agrupar(["a", "b", "c", "d", "e"], [("c", "a"), ("e", "c")])
    assert sorted(componentes.values()) == [["a", "c", "e"], ["b"], ["d"]]


# --------------------------------------------------------------------------- flujo con el workbook


@pytest.fixture()
def repo_grupos(tmp_path: Path) -> Path:
    copiar_insumos(tmp_path, ["config/grupos.toml", SALIDA_PRINCIPAL_V2, SALIDA_COMPLEMENTARIO_V2, SALIDA_NUCLEO,
                              SALIDA_DHASH, EMBEDDINGS_M2.as_posix(), INDICE_M2.as_posix(), MANIFIESTO_EVALUACION])
    assert grupos.main(["--root", str(tmp_path)]) == 0
    return tmp_path


def decidir(ruta: Path, decisiones: dict[str, dict[str, str]]) -> None:
    libro = load_workbook(ruta)
    hoja = libro[grupos.HOJA_PARES]
    encabezados = [c.value for c in hoja[1]]
    for fila in hoja.iter_rows(min_row=2):
        for columna, valor in decisiones.get(fila[encabezados.index("par")].value, {}).items():
            fila[encabezados.index(columna)].value = valor
    libro.save(ruta)


def test_sin_workbook_todos_los_pares_quedan_pendientes_y_cada_pieza_es_su_grupo(repo_grupos: Path) -> None:
    piezas = leer_csv(repo_grupos / grupos.SALIDA_GRUPOS)
    pares = leer_csv(repo_grupos / grupos.SALIDA_CANDIDATOS)
    assert len(piezas) == len(leer_csv(repo_grupos / SALIDA_PRINCIPAL_V2)) + len(leer_csv(repo_grupos / SALIDA_COMPLEMENTARIO_V2))
    assert {p["conjunto"] for p in piezas} == {"principal", "complementario"}
    assert len({p["grupo"] for p in piezas}) == len(piezas)
    reporte = (repo_grupos / grupos.REPORTE_GRUPOS).read_text(encoding="utf-8")
    assert f"| pendiente | {len(pares)} |" in reporte
    assert not any(p["id_a"] in reporte or p["id_b"] in reporte for p in pares)  # solo conteos


def test_workbook_propone_imagen_identica_y_conserva_las_decisiones(repo_grupos: Path) -> None:
    assert workbook.main(["--root", str(repo_grupos), "--fecha", "2026-11-05"]) == 0
    ruta = repo_grupos / grupos.WORKBOOK_GRUPOS
    filas = {f["par"]: f for f in grupos.leer_hoja(ruta, grupos.HOJA_PARES, clave="par")}
    auto = [f for f in filas.values() if f["revisor"] == "auto"]
    assert auto and all(f["decision"] == "unir" and "imagen_identica" in f["senales"] for f in auto)
    assert all(f["fecha_revision"] == "2026-11-05" for f in auto)

    # El revisor corrige una fila automatica y decide otra; regenerar no pisa ninguna de las dos.
    corregida = auto[0]["par"]
    otra = next(p for p, f in filas.items() if not f["decision"])
    decidir(ruta, {corregida: {"decision": "separar", "revisor": "HS", "fecha_revision": "2026-11-06"},
                   otra: {"decision": "no_seguro", "revisor": "HS", "fecha_revision": "2026-11-06"}})
    assert workbook.main(["--root", str(repo_grupos), "--fecha", "2026-11-06"]) == 0
    filas = {f["par"]: f for f in grupos.leer_hoja(ruta, grupos.HOJA_PARES, clave="par")}
    assert (filas[corregida]["decision"], filas[corregida]["revisor"]) == ("separar", "HS")
    assert filas[otra]["decision"] == "no_seguro"

    # no_seguro cuenta como unir: las dos piezas comparten grupo.
    assert grupos.main(["--root", str(repo_grupos)]) == 0
    grupo = {f["id_global"]: f["grupo"] for f in leer_csv(repo_grupos / grupos.SALIDA_GRUPOS)}
    a, b = otra.split(" | ")
    assert grupo[a] == grupo[b]
    reporte = (repo_grupos / grupos.REPORTE_GRUPOS).read_text(encoding="utf-8")
    assert f"| unir | {len(auto) - 1} |" in reporte and "| no_seguro | 1 |" in reporte and "| separar | 1 |" in reporte


def test_una_decision_invalida_detiene_el_paso_sin_tocar_los_grupos(repo_grupos: Path) -> None:
    assert workbook.main(["--root", str(repo_grupos), "--fecha", "2026-11-05"]) == 0
    assert grupos.main(["--root", str(repo_grupos)]) == 0
    salida = repo_grupos / grupos.SALIDA_GRUPOS
    antes = salida.read_bytes()
    ruta = repo_grupos / grupos.WORKBOOK_GRUPOS
    pendientes = [f["par"] for f in grupos.leer_hoja(ruta, grupos.HOJA_PARES, clave="par") if not f["decision"]]
    decidir(ruta, {pendientes[0]: {"decision": "quizas", "revisor": "HS", "fecha_revision": "2026-11-06"},
                   pendientes[1]: {"decision": "unir"},
                   pendientes[2]: {"decision": "separar", "revisor": "HS", "fecha_revision": "2026-02-30"}})
    assert grupos.main(["--root", str(repo_grupos)]) == 1
    assert salida.read_bytes() == antes
    reporte = (repo_grupos / grupos.REPORTE_GRUPOS).read_text(encoding="utf-8")
    assert f"- {pendientes[0]}: decision 'quizas' no es un codigo de [decisiones]" in reporte
    assert f"- {pendientes[1]}: decision sin revisor" in reporte
    assert f"- {pendientes[1]}: fecha_revision vacia o invalida" in reporte
    assert f"- {pendientes[2]}: fecha_revision vacia o invalida" in reporte
