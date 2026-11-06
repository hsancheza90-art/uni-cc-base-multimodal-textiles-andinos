"""M1: color y textura del textil (fuera del flujo para calcular; la comparación es solo numpy).

Uso desde la raíz del repositorio:

    python -m src.modelos.m1_vision

Para cada copia de evaluación verificada (SHA-256 del manifiesto) reduce la imagen a [m1] lado,
separa el textil del fondo con la segmentación del puntaje de aptitud ([segmentacion] de
config/aptitud.toml) y calcula dos histogramas normalizados sobre los píxeles del textil:

- color: histograma conjunto de CIELAB con cubetas_l × cubetas_ab × cubetas_ab cubetas
  (L de 0 a 100; a y b de -64 a 64, recortados);
- textura: LBP de 8 vecinos y radio 1, invariante a la rotación y uniforme (riu2, 10 valores),
  sobre la luminancia L.

Escribe, como insumos versionados, data/metadata/m1_caracteristicas_v2.npy (una fila por imagen:
color y luego textura), su índice data/metadata/m1_indice_v2.csv y el informe
outputs/reports/m1_caracteristicas_v2.md. La disimilitud entre dos piezas es la media ponderada
([m1] peso_color y peso_textura) de la mitad de la distancia L1 entre sus histogramas, en [0, 1].
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image

from src.imagenes.descargar_evaluacion import imagenes_verificadas, sha256_archivo
from src.imagenes.medidas import medir_superficie, reducir, rgb_a_lab, segmentar
from src.utils.archivos import escribir_csv, escribir_texto, leer_csv
from src.utils.config import CONFIG_MODELOS, leer_config_aptitud, leer_config_modelos

CARACTERISTICAS_M1 = Path("data/metadata/m1_caracteristicas_v2.npy")
INDICE_M1 = Path("data/metadata/m1_indice_v2.csv")
REPORTE_M1 = "outputs/reports/m1_caracteristicas_v2.md"
COLUMNAS_INDICE = ["fila", "id_global", "fuente", "sha256_copia", "fraccion_textil"]
VALORES_LBP = 10  # riu2 con 8 vecinos: 0..8 transiciones uniformes y una clase para las no uniformes
DECIMALES = 6


def dimension_color(config: dict[str, Any]) -> int:
    return int(config["cubetas_l"]) * int(config["cubetas_ab"]) ** 2


def histograma_color(lab: np.ndarray, mascara: np.ndarray, config: dict[str, Any]) -> np.ndarray:
    pixeles = lab[mascara]
    nl, nab = int(config["cubetas_l"]), int(config["cubetas_ab"])
    il = np.clip((pixeles[:, 0] / 100 * nl).astype(int), 0, nl - 1)
    ia = np.clip(((np.clip(pixeles[:, 1], -64, 64) + 64) / 128 * nab).astype(int), 0, nab - 1)
    ib = np.clip(((np.clip(pixeles[:, 2], -64, 64) + 64) / 128 * nab).astype(int), 0, nab - 1)
    conteo = np.bincount((il * nab + ia) * nab + ib, minlength=nl * nab * nab).astype(np.float64)
    return conteo / conteo.sum() if conteo.sum() else conteo


def lbp_riu2(luminancia: np.ndarray) -> np.ndarray:
    """Código LBP riu2 (0..9) de cada píxel interior; el borde de un píxel queda fuera (-1)."""
    centro = luminancia[1:-1, 1:-1]
    desplazamientos = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]  # en círculo
    alto, ancho = luminancia.shape
    bits = np.stack([luminancia[1 + dy:alto - 1 + dy, 1 + dx:ancho - 1 + dx] >= centro for dy, dx in desplazamientos])
    transiciones = np.sum(bits != np.roll(bits, 1, axis=0), axis=0)
    codigo = np.where(transiciones <= 2, bits.sum(axis=0), VALORES_LBP - 1)
    salida = np.full(luminancia.shape, -1, dtype=np.int64)
    salida[1:-1, 1:-1] = codigo
    return salida


def histograma_textura(lab: np.ndarray, mascara: np.ndarray) -> np.ndarray:
    codigos = lbp_riu2(lab[..., 0])
    validos = codigos[mascara & (codigos >= 0)]
    conteo = np.bincount(validos, minlength=VALORES_LBP).astype(np.float64)
    return conteo / conteo.sum() if conteo.sum() else conteo


def caracteristicas(imagen: Image.Image, config: dict[str, Any], segmentacion: dict[str, Any]) -> tuple[np.ndarray, float]:
    """Vector [color | textura] del textil y la fracción de la imagen que ocupa."""
    rgb = np.asarray(reducir(imagen.convert("RGB"), int(config["lado"])))
    lab = rgb_a_lab(rgb)
    mascara, _ = segmentar(lab, segmentacion)
    superficie = medir_superficie(mascara)
    if superficie["fraccion_textil"] == 0:
        # Sin textil separable: toda la imagen, con la misma regla que las medidas de aptitud.
        mascara = np.ones(mascara.shape, dtype=bool)
        superficie = medir_superficie(mascara)
    vector = np.concatenate([histograma_color(lab, mascara, config), histograma_textura(lab, mascara)])
    return vector, float(superficie["fraccion_textil"])


def disimilitud(a: np.ndarray, b: np.ndarray, config: dict[str, Any]) -> float:
    """Media ponderada de la mitad de la distancia L1 entre los histogramas de color y de textura."""
    corte = dimension_color(config)
    d_color = 0.5 * float(np.abs(a[:corte] - b[:corte]).sum())
    d_textura = 0.5 * float(np.abs(a[corte:] - b[corte:]).sum())
    pc, pt = float(config["peso_color"]), float(config["peso_textura"])
    return (pc * d_color + pt * d_textura) / (pc + pt)


def calcular(raiz: Path) -> int:
    config = leer_config_modelos(raiz)["m1"]
    segmentacion = leer_config_aptitud(raiz)["segmentacion"]
    filas, errores = imagenes_verificadas(raiz)
    if errores:
        print(f"{len(errores)} copias sin verificar; no se calculan las caracteristicas M1:")
        for error in errores[:20]:
            print(f"- {error}")
        return 1
    vectores, indice = [], []
    for numero, fila in enumerate(filas):
        with Image.open(raiz / fila["ruta_copia_evaluacion"]) as imagen:
            vector, fraccion = caracteristicas(imagen, config, segmentacion)
        vectores.append(vector)
        indice.append({"fila": str(numero), "id_global": fila["id_global"], "fuente": fila["fuente"],
                       "sha256_copia": fila["sha256_copia"], "fraccion_textil": f"{fraccion:.4f}"})
    matriz = np.round(np.array(vectores), DECIMALES).astype(np.float32)
    (raiz / CARACTERISTICAS_M1).parent.mkdir(parents=True, exist_ok=True)
    np.save(raiz / CARACTERISTICAS_M1, matriz, allow_pickle=False)
    escribir_csv(raiz / INDICE_M1, COLUMNAS_INDICE, indice)
    fracciones = [float(f["fraccion_textil"]) for f in indice]
    escribir_texto(raiz / REPORTE_M1, [
        "# M1: caracteristicas de color y textura (v2)",
        "",
        "Generado por `python -m src.modelos.m1_vision` (`src/modelos/m1_vision.py`), fuera del flujo: lee las copias "
        f"de evaluacion locales. Parametros en `{CONFIG_MODELOS.as_posix()}` ([m1]); segmentacion del textil en "
        "`config/aptitud.toml` ([segmentacion]).",
        "",
        f"- `{CARACTERISTICAS_M1.as_posix()}`: {matriz.shape[0]} imagenes x {matriz.shape[1]} valores "
        f"({dimension_color(config)} de color Lab y {VALORES_LBP} de textura LBP riu2), float32 redondeado a {DECIMALES} "
        f"decimales. SHA-256 `{sha256_archivo(raiz / CARACTERISTICAS_M1)}`.",
        f"- `{INDICE_M1.as_posix()}`: id_global, fuente, SHA-256 de la copia y fraccion de la imagen que ocupa el textil.",
        f"- Fraccion del textil: mediana {np.median(fracciones):.3f}, minima {min(fracciones):.3f}.",
        "",
        "Sin rankings ni vecinos: la galeria del protocolo se juzga a ciegas.",
    ])
    print(f"M1: {matriz.shape[0]} vectores de {matriz.shape[1]} valores -> {CARACTERISTICAS_M1.as_posix()}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="M1: caracteristicas de color y textura de las copias de evaluacion.")
    parser.add_argument("--root", default=".", help="Raiz del repositorio.")
    return calcular(Path(parser.parse_args(argv).root).resolve())


if __name__ == "__main__":
    raise SystemExit(main())
