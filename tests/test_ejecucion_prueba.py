"""Pruebas de la ejecución única del test, sin ejecutar ningún sistema sobre las consultas de prueba.

La evaluación se ensaya con la partición de desarrollo y sus juicios; la tarea T1, con consultas
hipotéticas y vectores de texto sintéticos en un directorio temporal. Ninguna prueba muestra
métricas: solo comprueba la estructura y las propiedades del cálculo.
"""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

import numpy as np
import pytest

from src.experimento import ejecucion_prueba as ep
from src.experimento import evaluacion, juicios
from src.experimento.consultas_t1 import SALIDA_T1
from src.experimento.pesos_m4 import leer_juicios
from src.experimento.rankings import SALIDA_RANKINGS
from src.experimento.snapshot import SALIDA_CONSULTAS, SALIDA_PARTICIONES
from src.anotacion.corpus_v2 import SALIDA_PRINCIPAL_V2
from src.imagenes.descargar_evaluacion import MANIFIESTO_EVALUACION
from src.modelos.embeddings import EMBEDDINGS_M2, INDICE_M2
from src.utils.archivos import escribir_csv, leer_csv
from src.utils.config import CONFIG_EXPERIMENTO, RAIZ_REPO, leer_config_experimento
from tests.insumos import copiar_insumos


def test_la_comprobacion_previa_del_repositorio_solo_depende_de_la_autorizacion_y_de_la_corrida() -> None:
    # Antes de la autorización, el único problema es su falta; después (R40), solo puede objetar que la corrida
    # ya avanzó más allá del sellado de insumos, porque el test se ejecuta una sola vez.
    problemas = ep.comprobar(RAIZ_REPO)
    if not ep.aprobado(RAIZ_REPO):
        assert problemas and all("no esta aprobado" in p for p in problemas), problemas
    else:
        assert problemas == ep.reejecucion(RAIZ_REPO), problemas


def test_sin_aprobacion_no_se_ejecuta_ningun_sistema_sobre_la_prueba() -> None:
    if ep.aprobado(RAIZ_REPO):
        pytest.skip("Con el protocolo aprobado esta prueba abriria el test: no se ejecuta.")
    assert ep.main(["--root", str(RAIZ_REPO), "--rankings"]) == 1
    assert not (RAIZ_REPO / ep.RANKINGS_PRUEBA).exists() and not (RAIZ_REPO / ep.RANKINGS_T1).exists()
    assert ep.main(["--root", str(RAIZ_REPO), "--comprobar"]) == 1


@pytest.fixture(scope="module")
def ensayo_desarrollo() -> dict:
    """Cálculo completo sobre la partición de desarrollo, en memoria."""
    rk = ep.leer_rankings(RAIZ_REPO / SALIDA_RANKINGS)
    pool = juicios.construir_pool(RAIZ_REPO, leer_config_experimento())
    return ep.calcular(RAIZ_REPO, "desarrollo", rk, leer_juicios(RAIZ_REPO), pool)


def test_h3_reconstruccion_e_intervencion_se_cumplen(ensayo_desarrollo: dict) -> None:
    h3 = ensayo_desarrollo["h3"]
    assert h3["resultados"] == 10 * 10 and h3["cumple"]
    assert h3["reconstruccion"] <= 1e-9 and h3["intervencion"] <= 1e-9


def test_el_ensayo_produce_todas_las_comparaciones_y_variantes(ensayo_desarrollo: dict) -> None:
    r = ensayo_desarrollo
    assert set(r["comparaciones"]) == {"H1: M4 frente a M2", "H2: M3 frente a M3-sin-orden",
                                       "H2, subgrupo: consultas con palabra de bandas"}
    for variante in ("M4 sin M3", "M4 sin M0", "M4 con M3-sin-orden", "Control negativo", "M3 solo bandas", "M3 sin bandas"):
        assert variante in r["nombres"]
    veredictos = {*evaluacion.LECTURAS, evaluacion.EXPLORATORIA, ep.DESCRIPTIVA}
    assert all(c.decision in veredictos for c in [*r["comparaciones"].values(), *r["exploratorias"].values()])
    h1, h2 = r["comparaciones"]["H1: M4 frente a M2"], r["comparaciones"]["H2: M3 frente a M3-sin-orden"]
    assert not h1.exacta and h1.replicas == 100_000 and h1.error_mc > 0  # R34
    assert h2.exacta and h2.m <= r["b"] <= 2 and h2.p_permutacion >= h2.p_minima  # R35: dos consultas con bandas en desarrollo
    assert h2.sostiene <= h1.sostiene  # R33: H2 no se sostiene si H1 no se sostiene
    assert r["comparaciones"]["H2, subgrupo: consultas con palabra de bandas"].decision == ep.DESCRIPTIVA
    assert {criterio for criterio, _ in r["robustez"]} == {"museo", "completitud"}
    assert set(r["no_evaluables"]) == set(ep.SISTEMAS_POOL)
    assert len({f["consulta"] for f in r["filas"]}) == 10


def test_m4_con_m3_sin_orden_coincide_con_m4_cuando_la_consulta_no_tiene_bandas(ensayo_desarrollo: dict) -> None:
    # Sin palabra de bandas en la consulta, M3 y su control dan los mismos scores (R27): la fusion no cambia.
    r = ensayo_desarrollo
    sin_bandas = [c for c in r["ndcg"]["M4"] if c not in r["con_bandas"]]
    assert sin_bandas and all(r["ndcg"]["M4"][c] == r["ndcg"]["M4 con M3-sin-orden"][c] for c in sin_bandas)


def test_rankings_t1_con_consultas_hipoteticas(tmp_path: Path) -> None:
    congelada = "data/metadata/v2_1_congelado/anotaciones_v2_1.csv"
    copiar_insumos(tmp_path, ["config/modelos.toml", "config/anotacion.toml", "config/vocabulario.toml", SALIDA_PARTICIONES,
                              SALIDA_PRINCIPAL_V2, str(EMBEDDINGS_M2), str(INDICE_M2), congelada])
    consultas = [
        {"consulta": "T1-E1", "descripcion": "Faja con bandas lisas y de rombos escalonados", "composicion": "bandas",
         "secuencia_bandas": "lisa > geometrica > lisa"},
        {"consulta": "T1-E2", "descripcion": "Pano con campo central y borde de aves", "composicion": "", "secuencia_bandas": ""},
    ]
    escribir_csv(tmp_path / SALIDA_T1, ["consulta", "descripcion", "composicion", "secuencia_bandas"], consultas)
    vectores = np.random.default_rng(1).normal(size=(2, 512))
    (tmp_path / ep.EMBEDDINGS_T1).parent.mkdir(parents=True, exist_ok=True)
    np.save(tmp_path / ep.EMBEDDINGS_T1, (vectores / np.linalg.norm(vectores, axis=1, keepdims=True)).astype(np.float32))
    escribir_csv(tmp_path / ep.INDICE_T1, ["fila", "consulta"], [{"fila": "0", "consulta": "T1-E1"}, {"fila": "1", "consulta": "T1-E2"}])
    filas = ep.rankings_t1(tmp_path)
    galeria = len(leer_csv(RAIZ_REPO / SALIDA_PARTICIONES))
    sistemas = {(f["consulta"], f["sistema"]) for f in filas}
    assert ("T1-E1", "M3") in sistemas and ("T1-E2", "M3") not in sistemas  # M3 solo con especificacion
    assert all(sum(1 for f in filas if (f["consulta"], f["sistema"]) == par) == galeria for par in sistemas)


# --------------------------------------------------------------------------- custodia, fallos, H3 y cegamiento


def repo_autorizado(tmp_path: Path) -> Path:
    """Repositorio temporal con una autorizacion hipotetica: nunca toca la configuracion real."""
    texto = (RAIZ_REPO / CONFIG_EXPERIMENTO).read_text(encoding="utf-8")
    texto = re.sub(r'(?m)^aprobacion_protocolo = ".*"$', 'aprobacion_protocolo = "2099-01-01 hipotetica"', texto)
    (tmp_path / CONFIG_EXPERIMENTO).parent.mkdir(parents=True, exist_ok=True)
    (tmp_path / CONFIG_EXPERIMENTO).write_text(texto, encoding="utf-8")
    for nombre, contenido in (("a.csv", "x\n1\n"), ("b.csv", "y\n2\n")):
        (tmp_path / nombre).write_text(contenido, encoding="utf-8")
    return tmp_path


def sellar(raiz: Path) -> None:
    config = leer_config_experimento(raiz)
    man = {"corrida": ep.identificador_corrida(config), "estados": [
        {"estado": "autorizada", "sha256": {}},
        {"estado": "insumos_sellados", "sha256": {"a.csv": ep.sha256(raiz / "a.csv")}},
    ]}
    ep.publicar(raiz, [], lambda _: man)
    ep.publicar(raiz, [("c.csv", lambda ruta: ruta.write_text("z\n3\n", encoding="utf-8"))],
                lambda sumas: ep.con_estado(man, "rankings_sellados", sumas))


def test_t4_alterar_un_byte_de_un_archivo_sellado_suspende_la_corrida(tmp_path: Path) -> None:
    raiz = repo_autorizado(tmp_path)
    assert ep.verificar(raiz, "rankings_sellados")[1] == ["Falta el manifiesto de ejecucion "
                                                          f"({ep.MANIFIESTO_EJECUCION}): la corrida no se puede continuar."]
    sellar(raiz)
    man, problemas = ep.verificar(raiz, "rankings_sellados")
    assert problemas == [] and ep.estado_actual(man) == "rankings_sellados"
    assert ep.verificar(raiz, "juicios_cerrados")[1]  # un estado que todavia no se alcanzo
    contenido = bytearray((raiz / "a.csv").read_bytes())
    contenido[0] ^= 1
    (raiz / "a.csv").write_bytes(bytes(contenido))
    man, problemas = ep.verificar(raiz, "rankings_sellados")
    assert any("huella de a.csv" in p for p in problemas)
    assert ep.crear_juicios(raiz) == 1  # aborta y suspende
    assert ep.estado_actual(ep.leer_manifiesto(raiz)) == ep.SUSPENDIDA
    assert ep.verificar(raiz, "rankings_sellados")[1][0].startswith("La corrida esta suspendida")
    assert ep.evaluar(raiz) == 1 and ep.cerrar_juicios(raiz) == 1


def test_t4_un_manifiesto_de_otra_corrida_no_se_acepta(tmp_path: Path) -> None:
    raiz = repo_autorizado(tmp_path)
    sellar(raiz)
    texto = (raiz / CONFIG_EXPERIMENTO).read_text(encoding="utf-8").replace("2099-01-01 hipotetica", "2099-02-02 otra")
    (raiz / CONFIG_EXPERIMENTO).write_text(texto, encoding="utf-8")
    assert any("otra corrida" in p for p in ep.verificar(raiz, "rankings_sellados")[1])


def test_t5_una_caida_parcial_no_deja_salidas_ni_avanza_el_estado(tmp_path: Path) -> None:
    raiz = repo_autorizado(tmp_path)
    sellar(raiz)
    antes = (raiz / ep.MANIFIESTO_EJECUCION).read_bytes()

    def falla(ruta: Path) -> None:
        raise RuntimeError("corte simulado")

    man = ep.leer_manifiesto(raiz)
    with pytest.raises(RuntimeError):
        ep.publicar(raiz, [("d.csv", lambda ruta: ruta.write_text("d\n", encoding="utf-8")), ("e.csv", falla)],
                    lambda sumas: ep.con_estado(man, "juicios_cerrados", sumas))
    assert not (raiz / "d.csv").exists() and not (raiz / "e.csv").exists()
    assert not list(raiz.glob("*.tmp.*"))  # sin temporales
    assert (raiz / ep.MANIFIESTO_EJECUCION).read_bytes() == antes  # el estado no avanzo
    ep.publicar(raiz, [("d.csv", lambda ruta: ruta.write_text("d\n", encoding="utf-8"))],
                lambda sumas: ep.con_estado(man, "juicios_cerrados", sumas))  # el paso se repite
    man, problemas = ep.verificar(raiz, "juicios_cerrados")
    assert problemas == [] and ep.sellados(man)["d.csv"] == ep.sha256(raiz / "d.csv")


def test_t5_el_paso_de_rankings_exige_todos_los_insumos(tmp_path: Path) -> None:
    raiz = repo_autorizado(tmp_path)
    with pytest.raises(FileNotFoundError):
        ep.huellas(raiz, ["a.csv", "no_existe.csv"])
    assert str(ep.EMBEDDINGS_T1.as_posix()) in ep.insumos_obligatorios(RAIZ_REPO)


def rk_sintetico(grados: list[int | None]) -> tuple[dict, dict]:
    candidatos = [f"AIC:{i}" for i in range(len(grados))]
    puntos = [(c, 1 - i / 100) for i, c in enumerate(candidatos)]
    rk = {"Q1": {s: list(puntos) for s in ("M0", "M2", "M3", "M4")}}
    return rk, {"Q1": dict(zip(candidatos, grados))}


@pytest.mark.parametrize("grados, aciertos, errores", [
    ([3] * 10, 5, 0),                                  # sin errores: la clase vacia se informa
    ([2, 3, 0, 1, None, 3, 2, 3, 3, 3], 5, 2),         # dos errores: se usan todos; no_evaluable fuera
    ([0] * 3 + [None] * 7, 0, 3),                      # sin aciertos
])
def test_t6_la_muestra_de_h3_usa_todos_los_casos_si_una_clase_es_corta(grados, aciertos: int, errores: int) -> None:
    rk, juicios_t3 = rk_sintetico(grados)
    config = leer_config_experimento()
    muestra, disponibles = ep.muestra_revision_h3(rk, juicios_t3, config)
    clases = Counter(f["clase"] for f in muestra)
    assert (clases["acierto"], clases["error"]) == (aciertos, errores)
    assert disponibles["error"] == sum(1 for g in grados if g is not None and g < 2)
    assert [f["ficha"] for f in muestra] == [f"F{n:02d}" for n in range(1, len(muestra) + 1)]
    assert muestra == ep.muestra_revision_h3(rk, juicios_t3, config)[0]  # semilla fija
    assert all(juicios_t3["Q1"][f["id_global"]] is not None for f in muestra)


def test_t6_la_ficha_de_h3_es_ciega_y_se_valida() -> None:
    assert not [c for c in ep.EDITABLES_H3 + ep.CONTEXTO_H3 if any(p in c for p in ep.PROHIBIDAS)]
    rk, _ = rk_sintetico([3] * 10)
    texto = ep.explicacion(rk["Q1"], "AIC:0", {"M0": 1 / 7, "M2": 4 / 7, "M3": 2 / 7})
    assert "M0 (" in texto and "Total:" in texto
    errores, pendientes = ep.validar_revision_h3([
        {"ficha": "F01", "valoracion": "correcta", "componente_en_desacuerdo": "ninguno", "evaluador": "HS", "fecha_revision": "2026-11-30"},
        {"ficha": "F02", "valoracion": "quizas", "componente_en_desacuerdo": "ninguno", "evaluador": "", "fecha_revision": "30-11"},
        {"ficha": "F03", "valoracion": "", "evaluador": "", "fecha_revision": ""},
        {"ficha": "F04", "valoracion": "especulativa", "componente_en_desacuerdo": "ninguno", "evaluador": "HS",
         "fecha_revision": "2026-11-30"},
        {"ficha": "F05", "valoracion": "incorrecta", "componente_en_desacuerdo": "M3", "justificacion": "El M3 alto no se ve",
         "evaluador": "HS", "fecha_revision": "2026-11-30"},
        {"ficha": "F06", "valoracion": "correcta", "componente_en_desacuerdo": "M9", "evaluador": "HS", "fecha_revision": "2026-11-30"},
    ])
    assert pendientes == 1 and len(errores) == 5  # F02: tres; F04: sin componente ni justificacion; F06: codigo


def test_t7_el_libro_de_juicios_es_ciego_de_extremo_a_extremo(tmp_path: Path) -> None:
    # Con el pool de DESARROLLO, en un directorio temporal: el libro escrito no lleva sistema, puntuacion
    # ni posicion y conserva el orden sorteado. No se ejecuta ningun sistema sobre la prueba.
    copiar_insumos(tmp_path, [MANIFIESTO_EVALUACION, SALIDA_CONSULTAS])
    config = leer_config_experimento()
    tarea = ep.Tarea("T3", SALIDA_RANKINGS, "data/processed/pool_ensayo.csv", Path("data/metadata/juicios_ensayo.xlsx"),
                     "data/metadata/juicios_ensayo.csv", Path("outputs/review/ensayo.html"), ep.GUIA_T3)
    pares = juicios.construir_pool(RAIZ_REPO, config, SALIDA_RANKINGS)
    escribir_csv(tmp_path / tarea.pool, ep.COLUMNAS_POOL, pares)
    filas = ep.filas_libro(tmp_path, tarea, leer_csv(tmp_path / tarea.pool))
    ep.escribir_libro_juicios(tmp_path, tarea, filas, config, tmp_path / tarea.workbook)
    assert ep.cegamiento_del_libro(tmp_path, tarea) == []
    encabezados = ep.encabezados_libro(tmp_path / tarea.workbook, juicios.HOJA_JUICIOS)
    assert not any(p in c.lower() for c in encabezados for p in ep.PROHIBIDAS)
    # Un libro con el sistema o con otro orden no pasa la validacion.
    assert ep.validar_cegamiento(encabezados + ["sistema"], filas, pares)
    invertidas = [dict(f) for f in reversed(filas)]
    assert ep.validar_cegamiento(encabezados, invertidas, pares)

def test_el_informe_sigue_la_plantilla_de_diez_tablas(ensayo_desarrollo: dict) -> None:
    # Solo la estructura: la prueba no muestra ninguna cifra del ensayo.
    config = leer_config_experimento()
    integridad = {"corrida": "corrida-ensayo", "estados": list(ep.ESTADOS), "huellas": 0, "commit": "",
                  "cegamiento": {"T3": "sin problemas", "T1": "sin problemas"}}
    lineas = ep.informe(ensayo_desarrollo, config, integridad, (None, "no realizada"), None, None)
    titulos = [l for l in lineas if l.startswith("## ")]
    assert [t.split(".")[0] for t in titulos] == [f"## {n}" for n in range(1, 11)]
    texto = "\n".join(lineas)
    assert "p minima alcanzable" in texto and "Error de Monte Carlo" in texto and "Compuerta de H1" in texto

def sellar_hasta_juicios(raiz: Path) -> dict:
    sellar(raiz)
    man = ep.leer_manifiesto(raiz)
    ep.publicar(raiz, [("j.csv", lambda ruta: ruta.write_text("juicio\n2\n", encoding="utf-8"))],
                lambda sumas: ep.con_estado(man, "juicios_cerrados", sumas))
    return ep.leer_manifiesto(raiz)


@pytest.mark.parametrize("archivo", ["a.csv", "c.csv", "j.csv"])  # insumo, ranking y juicios
def test_t4_evaluar_se_detiene_antes_de_producir_metricas_si_cambia_un_byte(tmp_path: Path, archivo: str) -> None:
    raiz = repo_autorizado(tmp_path)
    sellar_hasta_juicios(raiz)
    assert ep.verificar(raiz, "juicios_cerrados")[1] == []
    contenido = bytearray((raiz / archivo).read_bytes())
    contenido[-1] ^= 1
    (raiz / archivo).write_bytes(bytes(contenido))
    assert ep.evaluar(raiz) == 1
    assert not (raiz / ep.METRICAS).exists() and not (raiz / ep.REPORTE).exists()
    assert ep.estado_actual(ep.leer_manifiesto(raiz)) == ep.SUSPENDIDA


def test_t4_un_archivo_sellado_faltante_suspende(tmp_path: Path) -> None:
    raiz = repo_autorizado(tmp_path)
    sellar_hasta_juicios(raiz)
    (raiz / "c.csv").unlink()
    assert ep.evaluar(raiz) == 1 and not (raiz / ep.METRICAS).exists()
    assert "Falta un archivo sellado: c.csv" in ep.leer_manifiesto(raiz)["estados"][-1]["motivo"]


def test_t5_se_rechaza_la_reejecucion_accidental(tmp_path: Path) -> None:
    raiz = repo_autorizado(tmp_path)
    assert ep.reejecucion(raiz) == []
    config = leer_config_experimento(raiz)
    man = {"corrida": ep.identificador_corrida(config), "estados": [{"estado": "autorizada", "sha256": {}},
                                                                    {"estado": "insumos_sellados", "sha256": {}}]}
    ep.publicar(raiz, [], lambda _: man)
    assert ep.reejecucion(raiz) == []  # una corrida en insumos_sellados puede reanudarse tras un fallo documentado
    ep.publicar(raiz, [("c.csv", lambda ruta: ruta.write_text("z\n", encoding="utf-8"))],
                lambda sumas: ep.con_estado(man, "rankings_sellados", sumas))
    assert any("una sola vez" in p for p in ep.reejecucion(raiz))  # despues del sellado, no
    (raiz / ep.RANKINGS_PRUEBA).parent.mkdir(parents=True, exist_ok=True)
    (raiz / ep.RANKINGS_PRUEBA).write_text("x\n", encoding="utf-8")
    assert len(ep.reejecucion(raiz)) == 2


def test_t7_las_reglas_de_juicio_se_sellan_y_su_cambio_se_detecta(tmp_path: Path, monkeypatch) -> None:
    raiz = repo_autorizado(tmp_path)
    config = leer_config_experimento(raiz)
    huella = ep.huella_reglas(config)
    man = {"corrida": ep.identificador_corrida(config), "estados": [
        {"estado": "autorizada", "sha256": {}}, {"estado": "insumos_sellados", "reglas_juicio": huella, "sha256": {}}]}
    ep.publicar(raiz, [], lambda _: man)
    assert ep.verificar(raiz, "insumos_sellados")[1] == []
    monkeypatch.setattr(ep, "GUIA_T3", ep.GUIA_T3 + ["Instruccion agregada despues del sellado"])
    assert any("reglas de juicio" in p for p in ep.verificar(raiz, "insumos_sellados")[1])