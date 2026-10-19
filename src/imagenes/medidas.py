"""Etapa 1 del puntaje de aptitud: medidas objetivas de cada imagen.

Uso desde la raiz del repositorio (requiere las copias de evaluacion locales, que
descarga src/imagenes/descargar_evaluacion.py):

    python -m src.imagenes.medidas                 # mide solo las copias nuevas o modificadas
    python -m src.imagenes.medidas --recalcular    # vuelve a medir todo (tras cambiar [segmentacion])

Sobre la copia de evaluacion de 1600 px se separa el textil del fondo y se miden
rasgos que no dependen de ningun juicio: resolucion y nitidez, exposicion, color
(colorido, tonos, colores claramente distintos), bordes de diseño, forma de la pieza
(fragmentos, lagunas, compacidad, encuadre) y estructura (periodicidad y simetrias).
Cada medida es reproducible y se versiona en data/metadata/aptitud_medidas_v2.csv;
las etapas siguientes (calibrar_aptitud.py y aptitud.py) trabajan solo con ese
archivo, sin imagenes ni red, para que el flujo se pueda regenerar en un clon limpio.

Decisiones de medicion que conviene recordar al leer los resultados:

- El fondo de estudio se estima en el borde de la fotografia; si el borde no es
  uniforme, el textil llena el encuadre (toma cerrada) y el contorno no se evalua.
- La nitidez depende de la escala: la que se compara entre museos (nitidez_comun)
  se mide con el textil llevado a un tamaño comun, porque las copias MET y CMA
  vienen de originales mucho mayores que las AIC.
- Los colores se cuentan en Lab (perceptual): «colores distintos» son grupos
  separados por Delta E >= 25, lo que un observador distingue sin esfuerzo.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image

from src.imagenes.descargar_evaluacion import (
    ENTRADA_AIC,
    ENTRADA_CMA,
    ENTRADAS_MET,
    MANIFIESTO_EVALUACION,
    candidatos_evaluacion,
)
from src.utils.archivos import escribir_csv, indexar, leer_csv
from src.utils.config import leer_config_aptitud

MEDIDAS = "data/metadata/aptitud_medidas_v2.csv"


# Lado mayor de las versiones de trabajo derivadas de la copia de evaluacion.
LADO_MASCARA = 320
LADO_ESTRUCTURA = 512
LADO_DISENO = 400
LADO_CALIDAD = 800
SEMILLA = 0
COLUMNAS_MEDIDAS = [
    "id_global",
    "fuente",
    "id_fuente",
    "estado_imagen",
    "sha256_copia",
    "ancho_original",
    "alto_original",
    "encuadre_lleno",
    "fraccion_textil",
    "n_fragmentos",
    "fraccion_mayor",
    "fraccion_lagunas",
    "compacidad",
    "lado_textil_px",
    "nitidez",
    "nitidez_comun",
    "rango_dinamico",
    "fraccion_recortada",
    "croma_p90",
    "n_colores",
    "separabilidad_cromatica",
    "contraste_cromatico",
    "densidad_diseno",
    "regularidad",
    "modulo_px",
    "repeticiones",
    "simetria_horizontal",
    "simetria_vertical",
    "colorido",
    "n_tonos",
    "colores_distintos",
    "bordes_cromaticos",
    "toca_encuadre",
    "elongacion",
    "terminos_fragmento",
]
TERMINOS_FRAGMENTO = re.compile(
    r"\b(fragments?|mounted|reconstruct\w*|re-?assembled|assembled|pieced|joined|remnants?|portions?)\b",
    re.IGNORECASE,
)


def reducir(imagen: Image.Image, lado: int) -> Image.Image:
    escala = lado / max(imagen.size)
    if escala >= 1:
        return imagen
    return imagen.resize((max(1, round(imagen.width * escala)), max(1, round(imagen.height * escala))), Image.Resampling.BOX)


def rgb_a_lab(rgb: np.ndarray) -> np.ndarray:
    """sRGB (0-255) a CIELAB con iluminante D65."""
    c = rgb.astype(np.float64) / 255.0
    c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    matriz = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]])
    xyz = c @ matriz.T / np.array([0.95047, 1.0, 1.08883])
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], axis=-1)


def filtro_ventana(mascara: np.ndarray, radio: int, maximo: bool) -> np.ndarray:
    """Dilatacion (maximo) o erosion (minimo) con ventana cuadrada."""
    relleno = np.pad(mascara, radio, mode="edge")
    ventanas = np.lib.stride_tricks.sliding_window_view(relleno, (2 * radio + 1, 2 * radio + 1))
    return ventanas.max(axis=(-1, -2)) if maximo else ventanas.min(axis=(-1, -2))


def promedio_caja(matriz: np.ndarray, radio: int) -> np.ndarray:
    """Media movil cuadrada mediante la imagen integral."""
    relleno = np.pad(matriz, radio + 1, mode="edge").cumsum(0).cumsum(1)
    lado = 2 * radio + 1
    suma = relleno[lado:, lado:] - relleno[:-lado, lado:] - relleno[lado:, :-lado] + relleno[:-lado, :-lado]
    return suma[: matriz.shape[0], : matriz.shape[1]] / (lado * lado)


def etiquetar(mascara: np.ndarray) -> tuple[np.ndarray, int]:
    """Componentes conexas (vecindad 4) por union de conjuntos en dos pasadas."""
    alto, ancho = mascara.shape
    etiquetas = np.zeros((alto, ancho), dtype=np.int32)
    padre = [0]

    def raiz(i: int) -> int:
        while padre[i] != i:
            padre[i] = padre[padre[i]]
            i = padre[i]
        return i

    filas = mascara.tolist()
    for y in range(alto):
        fila = filas[y]
        for x in range(ancho):
            if not fila[x]:
                continue
            arriba = etiquetas[y - 1, x] if y else 0
            izquierda = etiquetas[y, x - 1] if x else 0
            if arriba and izquierda:
                a, b = raiz(arriba), raiz(izquierda)
                etiquetas[y, x] = min(a, b)
                padre[max(a, b)] = min(a, b)
            elif arriba or izquierda:
                etiquetas[y, x] = arriba or izquierda
            else:
                padre.append(len(padre))
                etiquetas[y, x] = len(padre) - 1
    raices = np.array([raiz(i) for i in range(len(padre))], dtype=np.int32)
    unicas, compactas = np.unique(raices, return_inverse=True)
    return compactas[etiquetas].astype(np.int32), len(unicas) - 1


def kmeans(datos: np.ndarray, k: int, iteraciones: int = 20) -> tuple[np.ndarray, np.ndarray]:
    """k-means con inicializacion k-means++ y semilla fija; devuelve centroides y tamanos."""
    rng = np.random.default_rng(SEMILLA)
    centroides = [datos[rng.integers(len(datos))]]
    for _ in range(1, k):
        d2 = np.min(((datos[:, None, :] - np.array(centroides)[None]) ** 2).sum(-1), axis=1)
        if d2.sum() == 0:
            break
        centroides.append(datos[rng.choice(len(datos), p=d2 / d2.sum())])
    c = np.array(centroides)
    for _ in range(iteraciones):
        asignacion = ((datos[:, None, :] - c[None]) ** 2).sum(-1).argmin(1)
        nuevos = np.array([datos[asignacion == j].mean(0) if np.any(asignacion == j) else c[j] for j in range(len(c))])
        if np.allclose(nuevos, c):
            break
        c = nuevos
    asignacion = ((datos[:, None, :] - c[None]) ** 2).sum(-1).argmin(1)
    return c, np.bincount(asignacion, minlength=len(c))


def segmentar(lab: np.ndarray, parametros: dict[str, Any]) -> tuple[np.ndarray, bool]:
    """Separa el textil del fondo de estudio, que se estima en el borde de la fotografia."""
    alto, ancho, _ = lab.shape
    franja = max(2, round(0.04 * min(alto, ancho)))
    borde = np.concatenate([
        lab[:franja].reshape(-1, 3), lab[-franja:].reshape(-1, 3),
        lab[:, :franja].reshape(-1, 3), lab[:, -franja:].reshape(-1, 3),
    ])
    fondo = np.median(borde, axis=0)
    dispersion = np.median(np.linalg.norm(borde - fondo, axis=1))
    if dispersion > parametros["dispersion_fondo_maxima"]:
        # El borde no es un fondo uniforme: el textil ocupa todo el encuadre.
        return np.ones((alto, ancho), dtype=bool), True
    distancia = np.linalg.norm(lab - fondo, axis=-1)
    luminancia = lab[..., 0]
    # Ventana y cierre minimos: con radios mayores se rellenan las lagunas de las piezas dañadas.
    textura = np.sqrt(np.maximum(promedio_caja(luminancia**2, 1) - promedio_caja(luminancia, 1) ** 2, 0))
    mascara = (distancia > parametros["delta_e_fondo"]) | (textura > parametros["textura_minima"])
    mascara = filtro_ventana(filtro_ventana(mascara, 1, True), 1, False)  # cierre
    mascara = filtro_ventana(filtro_ventana(mascara, 1, False), 1, True)  # apertura
    return mascara, False


def medir_superficie(mascara: np.ndarray) -> dict[str, float]:
    total = mascara.size
    etiquetas, n = etiquetar(mascara)
    areas = np.bincount(etiquetas.ravel(), minlength=n + 1)[1:]
    significativas = [i + 1 for i, area in enumerate(areas) if area >= 0.005 * total]
    if not significativas:
        return {"fraccion_textil": 0.0, "n_fragmentos": 0, "fraccion_mayor": 0.0, "fraccion_lagunas": 0.0, "compacidad": 0.0}
    textil = np.isin(etiquetas, significativas)
    area_textil = textil.sum()
    mayor = max(significativas, key=lambda i: areas[i - 1])
    principal = etiquetas == mayor
    n_fragmentos = sum(1 for i in significativas if areas[i - 1] >= 0.02 * area_textil)

    # Lagunas: zonas sin textil encerradas por el componente mayor.
    exterior, m = etiquetar(~principal)
    tocan_borde = set(np.unique(np.concatenate([exterior[0], exterior[-1], exterior[:, 0], exterior[:, -1]]))) - {0}
    lagunas = (~principal) & ~np.isin(exterior, list(tocan_borde))
    relleno = principal.sum() + lagunas.sum()

    ys, xs = np.nonzero(principal)
    caja = (ys.max() - ys.min() + 1) * (xs.max() - xs.min() + 1)
    return {
        "fraccion_textil": area_textil / total,
        "n_fragmentos": n_fragmentos,
        "fraccion_mayor": principal.sum() / area_textil,
        "fraccion_lagunas": lagunas.sum() / relleno,
        "compacidad": relleno / caja,
    }


def medir_calidad(gris: np.ndarray, mascara_gris: np.ndarray, lab: np.ndarray, mascara: np.ndarray) -> dict[str, float]:
    """Nitidez sobre la copia de 1600 px; exposicion y color sobre una version reducida."""
    laplaciano = np.abs(4 * gris[1:-1, 1:-1] - gris[:-2, 1:-1] - gris[2:, 1:-1] - gris[1:-1, :-2] - gris[1:-1, 2:])
    interior = mascara_gris[1:-1, 1:-1]
    luminancia = lab[..., 0][mascara]
    p5, p95 = np.percentile(luminancia, [5, 95])
    croma = np.hypot(lab[..., 1], lab[..., 2])[mascara]
    return {
        "nitidez": float(np.percentile(laplaciano[interior], 90) / (p95 - p5 + 1)),
        "rango_dinamico": float(p95 - p5),
        "fraccion_recortada": float(np.mean((luminancia < 3) | (luminancia > 97))),
        "croma_p90": float(np.percentile(croma, 90)),
    }


def medir_colores(lab: np.ndarray, mascara: np.ndarray, parametros: dict[str, Any]) -> dict[str, float]:
    """Colores perceptualmente distintos (k-means en Lab) y nitidez de sus fronteras."""
    interior = filtro_ventana(mascara, 1, False) if mascara.sum() > 400 else mascara
    pixeles = lab[interior]
    rng = np.random.default_rng(SEMILLA)
    if len(pixeles) > 20000:
        pixeles = pixeles[rng.choice(len(pixeles), 20000, replace=False)]
    centroides, tamanos = kmeans(pixeles, parametros["k_inicial"])
    grupos = [[c, t] for c, t in zip(centroides, tamanos) if t > 0]
    while len(grupos) > 1:
        distancias = [(np.linalg.norm(a[0] - b[0]), i, j) for i, a in enumerate(grupos) for j, b in enumerate(grupos) if i < j]
        minima, i, j = min(distancias)
        if minima >= parametros["delta_e_colores"]:
            break
        a, b = grupos[i], grupos[j]
        grupos[i] = [(a[0] * a[1] + b[0] * b[1]) / (a[1] + b[1]), a[1] + b[1]]
        del grupos[j]
    retenidos = np.array([g[0] for g in grupos if g[1] >= parametros["cobertura_minima_color"] * len(pixeles)])
    if len(retenidos) < 2:
        return {"n_colores": len(retenidos), "separabilidad_cromatica": 0.0, "contraste_cromatico": 0.0}
    distancias = np.sort(np.linalg.norm(pixeles[:, None, :] - retenidos[None], axis=-1), axis=1)
    pares = [np.linalg.norm(a - b) for i, a in enumerate(retenidos) for b in retenidos[i + 1:]]
    return {
        "n_colores": len(retenidos),
        "separabilidad_cromatica": float(np.mean(distancias[:, 0] < 0.5 * distancias[:, 1])),
        "contraste_cromatico": float(np.median(pares)),
    }


def medir_color_identificable(rgb: np.ndarray, lab: np.ndarray, mascara: np.ndarray, parametros: dict[str, Any]) -> dict[str, float]:
    """Medidas de si los colores y las formas se pueden identificar (version de 400 px).

    - colorido: indice de Hasler y Susstrunk (2003) sobre los pixeles del textil.
    - n_tonos: sectores de matiz de 30 grados con al menos el 3 % del textil y croma >= 15.
    - colores_distintos: grupos k-means separados por Delta E >= 25 (claramente distintos a la vista).
    - bordes_cromaticos: fraccion del textil con un salto de color (Delta E > 15) respecto del vecino a 2 px.
    """
    r, g, b = (rgb[..., i].astype(np.float64)[mascara] for i in range(3))
    rg, yb = r - g, 0.5 * (r + g) - b
    colorido = float(np.hypot(rg.std(), yb.std()) + 0.3 * np.hypot(rg.mean(), yb.mean()))

    a, bb = lab[..., 1][mascara], lab[..., 2][mascara]
    cromaticos = np.hypot(a, bb) >= 15
    matiz = (np.degrees(np.arctan2(bb[cromaticos], a[cromaticos])) % 360) // 30
    cobertura = np.bincount(matiz.astype(int), minlength=12) / max(mascara.sum(), 1)
    n_tonos = int((cobertura >= 0.03).sum())

    pixeles = lab[filtro_ventana(mascara, 1, False) if mascara.sum() > 400 else mascara]
    rng = np.random.default_rng(SEMILLA)
    if len(pixeles) > 20000:
        pixeles = pixeles[rng.choice(len(pixeles), 20000, replace=False)]
    centroides, tamanos = kmeans(pixeles, parametros["k_inicial"])
    grupos = [[c, t] for c, t in zip(centroides, tamanos) if t > 0]
    while len(grupos) > 1:
        minima, i, j = min((np.linalg.norm(x[0] - y[0]), i, j) for i, x in enumerate(grupos) for j, y in enumerate(grupos) if i < j)
        if minima >= parametros["delta_e_distintos"]:
            break
        x, y = grupos[i], grupos[j]
        grupos[i] = [(x[0] * x[1] + y[0] * y[1]) / (x[1] + y[1]), x[1] + y[1]]
        del grupos[j]
    colores_distintos = sum(1 for g_ in grupos if g_[1] >= 0.03 * len(pixeles))

    salto = np.linalg.norm(lab[2:, 2:] - lab[:-2, :-2], axis=-1)
    interior = mascara[2:, 2:] & mascara[:-2, :-2]
    bordes_cromaticos = float(np.mean(salto[interior] > 15)) if interior.any() else 0.0
    return {"colorido": colorido, "n_tonos": n_tonos, "colores_distintos": colores_distintos, "bordes_cromaticos": bordes_cromaticos}


def medir_encuadre(mascara: np.ndarray) -> dict[str, float]:
    """Pieza cortada por el borde de la fotografia y alargamiento del textil."""
    borde = np.concatenate([mascara[0], mascara[-1], mascara[:, 0], mascara[:, -1]])
    ys, xs = np.nonzero(mascara)
    alto, ancho = ys.max() - ys.min() + 1, xs.max() - xs.min() + 1
    return {"toca_encuadre": float(borde.mean()), "elongacion": float(max(alto, ancho) / min(alto, ancho))}


def medir_diseno(lab: np.ndarray, mascara: np.ndarray) -> float:
    """Fraccion del textil con bordes de diseno; a 400 px el tejido de fondo ya no aporta bordes."""
    luminancia = lab[..., 0]
    gradiente = np.hypot(np.diff(luminancia, axis=1)[:-1], np.diff(luminancia, axis=0)[:, :-1])
    return float(np.mean(gradiente[mascara[:-1, :-1]] > 8))


def medir_estructura(luminancia: np.ndarray, mascara: np.ndarray) -> dict[str, float]:
    """Autocorrelacion 2D del textil: regularidad, periodo del modulo y simetrias especulares."""
    ys, xs = np.nonzero(mascara)
    recorte = luminancia[ys.min(): ys.max() + 1, xs.min(): xs.max() + 1].astype(np.float64)
    zona = mascara[ys.min(): ys.max() + 1, xs.min(): xs.max() + 1]
    alto, ancho = recorte.shape
    if min(alto, ancho) < 32:
        return {"regularidad": 0.0, "periodo": 0.0, "repeticiones": 0.0, "simetria_horizontal": 0.0, "simetria_vertical": 0.0}
    recorte = np.where(zona, recorte, recorte[zona].mean())
    # Paso alto: se elimina la iluminacion y la forma general, que no son estructura del diseno.
    detalle = recorte - promedio_caja(recorte, max(4, min(alto, ancho) // 8))
    detalle = detalle * zona

    def correlacion(a: np.ndarray, b: np.ndarray) -> float:
        a, b = a - a.mean(), b - b.mean()
        return float((a * b).sum() / (np.sqrt((a * a).sum() * (b * b).sum()) + 1e-9))

    ventana = np.outer(np.hanning(alto), np.hanning(ancho))
    espectro = np.fft.rfft2(detalle * ventana, s=(2 * alto, 2 * ancho))
    auto = np.fft.fftshift(np.fft.irfft2(np.abs(espectro) ** 2, s=(2 * alto, 2 * ancho)))
    auto /= auto.max() + 1e-12
    cy, cx = alto, ancho
    dy, dx = np.mgrid[-cy: cy, -cx: cx]
    minimo = max(4, 0.03 * min(alto, ancho))
    valido = (np.hypot(dy, dx) >= minimo) & (np.abs(dy) <= alto / 2) & (np.abs(dx) <= ancho / 2)
    maximo_local = auto == filtro_ventana(auto, 2, True)
    candidatos = np.where(valido & maximo_local, auto, -1)
    pico = np.unravel_index(np.argmax(candidatos), candidatos.shape)
    regularidad = max(0.0, float(candidatos[pico]))
    desplazamiento = np.array([pico[0] - cy, pico[1] - cx], dtype=np.float64)
    periodo = float(np.hypot(*desplazamiento))
    extension = abs(desplazamiento[0]) / periodo * alto + abs(desplazamiento[1]) / periodo * ancho if periodo else 0.0
    return {
        "regularidad": regularidad,
        "periodo": periodo,
        "repeticiones": extension / periodo if periodo else 0.0,
        "simetria_horizontal": correlacion(detalle, detalle[:, ::-1]),
        "simetria_vertical": correlacion(detalle, detalle[::-1, :]),
    }


def ajustar_mascara(mascara: np.ndarray, tamano: tuple[int, int]) -> np.ndarray:
    return np.asarray(Image.fromarray(mascara.astype(np.uint8) * 255).resize(tamano, Image.Resampling.NEAREST)) > 127


def medir_nitidez_comun(imagen: Image.Image, mascara: np.ndarray, lado: int) -> float:
    """Nitidez del textil llevado siempre a `lado` px de lado mayor.

    La nitidez medida depende de la escala: reducir una imagen a la mitad la multiplica por
    1,2-1,55. Las copias MET y CMA vienen de originales de 3400-4000 px y las AIC de 1686 px,
    asi que la nitidez de la copia de 1600 px no es comparable entre fuentes. Aqui el textil
    (su rectangulo envolvente) se reescala a un tamaño comun antes de medir: lo que se compara
    es el detalle disponible a la escala del analisis.
    """
    completa = ajustar_mascara(mascara, imagen.size)
    ys, xs = np.nonzero(completa)
    caja = (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)
    recorte = imagen.crop(caja)
    escala = lado / max(recorte.size)
    tamano = (max(1, round(recorte.width * escala)), max(1, round(recorte.height * escala)))
    gris = np.asarray(recorte.convert("L").resize(tamano, Image.Resampling.LANCZOS), dtype=np.float64)
    zona = np.asarray(Image.fromarray(completa[caja[1]:caja[3], caja[0]:caja[2]].astype(np.uint8) * 255)
                      .resize(tamano, Image.Resampling.NEAREST)) > 127
    laplaciano = np.abs(4 * gris[1:-1, 1:-1] - gris[:-2, 1:-1] - gris[2:, 1:-1] - gris[1:-1, :-2] - gris[1:-1, 2:])
    interior = zona[1:-1, 1:-1]
    if not interior.any():
        return 0.0
    p5, p95 = np.percentile(gris[zona], [5, 95]) * 100 / 255
    return float(np.percentile(laplaciano[interior], 90) / (p95 - p5 + 1))


def medir_imagen(ruta: Path, ancho_original: int, alto_original: int, parametros: dict[str, Any]) -> dict[str, Any]:
    with Image.open(ruta) as archivo:
        imagen = archivo.convert("RGB")

    pequena = reducir(imagen, LADO_MASCARA)
    mascara, lleno = segmentar(rgb_a_lab(np.asarray(pequena)), parametros)
    superficie = medir_superficie(mascara)
    if superficie["fraccion_textil"] == 0:
        mascara, superficie = np.ones_like(mascara), medir_superficie(np.ones_like(mascara))

    gris = np.asarray(imagen.convert("L"), dtype=np.float64)
    calidad = reducir(imagen, LADO_CALIDAD)
    lab_calidad = rgb_a_lab(np.asarray(calidad))

    diseno = reducir(imagen, LADO_DISENO)
    lab_diseno = rgb_a_lab(np.asarray(diseno))
    mascara_diseno = ajustar_mascara(mascara, diseno.size)
    estructura_img = reducir(imagen, LADO_ESTRUCTURA)
    estructura = medir_estructura(rgb_a_lab(np.asarray(estructura_img))[..., 0], ajustar_mascara(mascara, estructura_img.size))
    escala_original = max(ancho_original, alto_original) / max(estructura_img.size)

    return {
        "encuadre_lleno": "si" if lleno else "no",
        **superficie,
        "lado_textil_px": float(np.sqrt(superficie["fraccion_textil"] * ancho_original * alto_original)),
        **medir_calidad(gris, ajustar_mascara(mascara, imagen.size), lab_calidad, ajustar_mascara(mascara, calidad.size)),
        "nitidez_comun": medir_nitidez_comun(imagen, mascara, parametros["nitidez_lado_textil"]),
        **medir_colores(lab_diseno, mascara_diseno, parametros),
        **medir_color_identificable(np.asarray(diseno), lab_diseno, mascara_diseno, parametros),
        **medir_encuadre(mascara),
        "densidad_diseno": medir_diseno(lab_diseno, mascara_diseno),
        "regularidad": estructura["regularidad"],
        "modulo_px": estructura["periodo"] * escala_original,
        "repeticiones": estructura["repeticiones"],
        "simetria_horizontal": estructura["simetria_horizontal"],
        "simetria_vertical": estructura["simetria_vertical"],
    }


def textos_metadatos(raiz: Path) -> dict[str, str]:
    """Titulo, descripcion y tecnica de cada candidato, para detectar fragmentos y montajes."""
    textos: dict[str, str] = {}
    for entrada in ENTRADAS_MET:
        for fila in leer_csv(raiz / entrada):
            textos[f"MET:{fila['id_fuente']}"] = " ".join([fila["titulo_original"], fila["tecnica"]])
    for fila in leer_csv(raiz / ENTRADA_CMA):
        textos[f"CMA:{fila['source_id']}"] = " ".join([fila["title"], fila["description"], fila["technique"]])
    for fila in leer_csv(raiz / ENTRADA_AIC):
        textos[f"AIC:{fila['id_fuente']}"] = " ".join([fila["titulo_original"], fila["descripcion"], fila["tecnicas"]])
    return textos


def formatear(valor: Any) -> str:
    if isinstance(valor, (float, np.floating)):
        return f"{float(valor):.4f}"
    return str(valor)


def medir(raiz: Path, config: dict[str, Any], recalcular: bool) -> int:
    """Mide las copias de evaluacion; reutiliza las medidas de copias que no cambiaron."""
    manifiesto = indexar(leer_csv(raiz / MANIFIESTO_EVALUACION), "id_global")
    previas = {} if recalcular or not (raiz / MEDIDAS).exists() else indexar(leer_csv(raiz / MEDIDAS), "id_global")
    textos = textos_metadatos(raiz)
    filas: list[dict[str, str]] = []
    candidatos = candidatos_evaluacion(raiz)
    reutilizadas = 0
    for numero, candidato in enumerate(candidatos, start=1):
        registro = manifiesto.get(candidato["id_global"])
        previa = previas.get(candidato["id_global"])
        if previa and previa["estado_imagen"] == "ok" and registro and previa["sha256_copia"] == registro["sha256_copia"]:
            filas.append(previa)
            reutilizadas += 1
            continue
        fila = {campo: "" for campo in COLUMNAS_MEDIDAS}
        fila.update({campo: candidato[campo] for campo in ("id_global", "fuente", "id_fuente")})
        terminos = sorted({t.lower() for t in TERMINOS_FRAGMENTO.findall(textos.get(candidato["id_global"], ""))})
        fila["terminos_fragmento"] = " ".join(terminos)
        if not registro or registro["estado_descarga"] != "ok":
            fila["estado_imagen"] = "sin_imagen"
        else:
            ruta = raiz / registro["ruta_copia_evaluacion"]
            if not ruta.exists():
                raise FileNotFoundError(f"Falta la copia de evaluacion {ruta}; ejecute src.imagenes.descargar_evaluacion")
            fila["estado_imagen"] = "ok"
            fila["sha256_copia"] = registro["sha256_copia"]
            fila["ancho_original"], fila["alto_original"] = registro["ancho_original"], registro["alto_original"]
            medidas = medir_imagen(ruta, int(registro["ancho_original"]), int(registro["alto_original"]), config["segmentacion"])
            fila.update({clave: formatear(valor) for clave, valor in medidas.items()})
        filas.append(fila)
        if numero % 50 == 0:
            print(f"  {numero}/{len(candidatos)} medidos")
    escribir_csv(raiz / MEDIDAS, COLUMNAS_MEDIDAS, filas)
    print(f"Medidas: {raiz / MEDIDAS} ({len(filas)} registros, {reutilizadas} reutilizadas)")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Medidas objetivas de las copias de evaluacion (etapa 1 del puntaje de aptitud).")
    parser.add_argument("--root", default=".", help="Raiz del repositorio.")
    parser.add_argument("--recalcular", action="store_true", help="Vuelve a medir todas las copias (tras cambiar [segmentacion]).")
    args = parser.parse_args(argv)
    raiz = Path(args.root).resolve()
    return medir(raiz, leer_config_aptitud(raiz), args.recalcular)


if __name__ == "__main__":
    raise SystemExit(main())
