"""Etapa 3 del puntaje de aptitud: ficha de cada imagen, puntaje y banda sugerida.

Uso desde la raiz del repositorio (sin red ni imagenes; lo ejecuta src/flujo.py):

    python -m src.imagenes.aptitud

Pregunta que responde: ¿permite la imagen identificar los atributos del textil que
el modelo combinatorio cuenta despues? Criterio del revisor (2026-10-19): van al
principal los textiles cuyos colores y figuras se identifican a primera vista, esten
completos o no; si ademas estan completos y se verifica en la fotografia, son
imagenes de referencia (la mejor imagen para el estudio).

Para cada imagen, a partir de sus medidas (etapa 1, medidas.py) y del modelo
calibrado con las decisiones del revisor (etapa 2, calibrar_aptitud.py):

1. Puertas verificables, antes de cualquier puntaje: pertinencia por metadatos
   (plumaria, muñecos, fecha de inicio posterior a 1532), sin imagen o textil de
   menos de lado_textil_minimo px -> descartar; fotografia monocroma -> secundario.
2. Atributos: calidad fotografica (por reglas) y probabilidad de que los colores
   sean identificables, las formas visibles, el textil este completo y sea una
   imagen de referencia; cada uno con un nivel legible.
3. Puntaje ordinal 0-100 y banda sugerida (principal, revisar o descartar).
4. Justificacion en una frase por atributo, con las medidas que la sostienen.

El puntaje sugiere; la decision es del revisor y se registra en los workbooks.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np

from src.imagenes.descargar_evaluacion import ENTRADA_AIC, ENTRADA_CMA, ENTRADAS_MET
from src.imagenes.medidas import COLUMNAS_MEDIDAS, MEDIDAS
from src.utils.archivos import escribir_csv, leer_csv
from src.utils.config import leer_config_aptitud
from src.utils.fechas import anio_inicio
from src.utils.fuentes import FUENTES

INVENTARIO_MET = FUENTES["MET"].candidatos
SALIDA_APTITUD = "data/metadata/aptitud_imagenes_v2.csv"
COLUMNAS_APTITUD = [
    "id_global",
    "fuente",
    "id_fuente",
    "puntaje_aptitud",
    "banda_sugerida",
    "referencia_sugerida",
    "motivo_banda",
    "fotografia",
    "colores",
    "formas",
    "completitud",
    "estructura",
    "calidad_fotografica",
    "prob_colores",
    "prob_formas",
    "prob_completitud",
    "prob_referencia",
    "justificacion",
]
MODELO_APTITUD = Path("config/aptitud_modelo.json")


# Nivel legible de cada atributo segun su valor (0-1): [umbral alto, umbral medio] y etiquetas.
NIVELES = {
    "fotografia": ("buena", "regular", "deficiente"),
    "colores": ("identificables", "parciales", "no_identificables"),
    "formas": ("visibles", "parciales", "no_visibles"),
    "completitud": ("completo", "incierto", "incompleto"),
}


def metadatos_pertinencia(raiz: Path) -> dict[str, dict[str, str]]:
    """Titulo, material y año de inicio de cada candidato, para las reglas de pertinencia.

    No se usa la descripcion: describe la iconografia («three-feathered wing»), no el soporte.
    MET no trae la fecha en los CSV revisados: se toma del inventario v1 (texto libre).
    """
    salida: dict[str, dict[str, str]] = {}
    fechas_met = {fila["id_objeto"]: fila["fecha_objeto"] for fila in leer_csv(raiz / INVENTARIO_MET)}
    for entrada in ENTRADAS_MET:
        for fila in leer_csv(raiz / entrada):
            fecha = fechas_met.get(fila["id_fuente"]) or fila["fecha_objeto"]
            salida[f"MET:{fila['id_fuente']}"] = {"titulo": fila["titulo_original"], "material": fila["material"],
                                                  "fecha_inicio": anio_inicio(fecha)}
    for fila in leer_csv(raiz / ENTRADA_CMA):
        salida[f"CMA:{fila['source_id']}"] = {"titulo": fila["title"], "material": fila["medium"],
                                              "fecha_inicio": anio_inicio(fila["creation_date"])}
    for fila in leer_csv(raiz / ENTRADA_AIC):
        salida[f"AIC:{fila['id_fuente']}"] = {
            "titulo": fila["titulo_original"], "material": " ".join([fila["material"], fila["materiales"]]),
            "fecha_inicio": int(float(fila["fecha_inicio"])) if fila["fecha_inicio"] else None,
        }
    return salida


def palabras(texto: str) -> set[str]:
    return set(re.findall(r"[a-z]+", texto.lower()))


# Motivos de pertinencia que descartan; posible_figurilla solo pide revision.
PERTINENCIA_DESCARTE = {"plumaria", "muneco", "posterior_inca"}


def posible_figurilla(titulo: str, reglas: dict[str, Any]) -> bool:
    """El titulo nombra el objeto como «Figure» (figurilla), no una figura representada en el textil.

    «Border Fragment, Figure» o «Male Figure with Modern Additions» son figurillas;
    «Fragment with Figure» o «Tunic with Frontal Figures» son textiles con figuras. Por
    prudencia solo cuenta la forma singular y no si la precede «with», «of», «depicting»...
    """
    texto = titulo.lower()
    figura = rf"\b{re.escape(reglas['figurilla_titulo'])}\b"
    if not re.search(figura, texto):
        return False
    representada = "|".join(re.escape(p) for p in reglas["figurilla_excluir_si_precede"])
    return not re.search(rf"\b({representada})\b[^,;]*{figura}", texto)


def motivo_pertinencia(metadatos: dict | None, reglas: dict[str, Any]) -> str:
    """Motivo de pertinencia segun los metadatos; vacio si no aplica ninguna regla."""
    if not metadatos:
        return ""
    plumaria = (palabras(metadatos["material"]) & set(reglas["plumaria_material"])
                or palabras(metadatos["titulo"]) & set(reglas["plumaria_titulo"]))
    if plumaria:
        return "plumaria"
    if palabras(metadatos["titulo"]) & set(reglas["muneco_titulo"]):
        return "muneco"
    if metadatos["fecha_inicio"] is not None and metadatos["fecha_inicio"] > reglas["fecha_inicio_maxima"]:
        return "posterior_inca"
    if posible_figurilla(metadatos["titulo"], reglas):
        return "posible_figurilla"
    return ""


TEXTOS_PERTINENCIA = {
    "plumaria": "Los metadatos registran plumas: los textiles con plumaria quedan fuera del estudio.",
    "muneco": "Los metadatos lo describen como muñeco: no es una superficie textil del estudio.",
    "posterior_inca": "Fecha de inicio posterior a 1532: el estudio abarca textiles incas y anteriores.",
    "posible_figurilla": "El título sugiere una figurilla («Figure»): confirmar si es un textil o un objeto tridimensional.",
}


def normalizar(valor: float, ancla: dict[str, float]) -> float:
    """Lineal entre el ancla baja (0) y la alta (1); admite anclas invertidas."""
    bajo, alto = ancla["bajo"], ancla["alto"]
    if ancla.get("escala") == "log":
        valor, bajo, alto = np.log10(max(valor, 1e-9)), np.log10(bajo), np.log10(alto)
    return float(np.clip((valor - bajo) / (alto - bajo), 0.0, 1.0))


# Medidas muy sesgadas: el modelo por atributos las usa en escala logaritmica.
MEDIDAS_LOG = {"lado_textil_px", "nitidez", "nitidez_comun", "modulo_px", "repeticiones", "elongacion", "colorido", "contraste_cromatico"}


def transformar(nombre: str, valor: float) -> float:
    return float(np.log1p(max(valor, 0.0))) if nombre in MEDIDAS_LOG else valor


def valor_medida(medidas: dict[str, str], nombre: str) -> float:
    """Valor de una medida, incluidas las derivadas de los metadatos."""
    if nombre == "titulo_fragmento":
        # El titulo o la tecnica de la fuente dicen «fragment(s)»: la pieza no esta entera.
        return 1.0 if {"fragment", "fragments"} & set(medidas["terminos_fragmento"].split()) else 0.0
    return float(medidas[nombre])


# En una toma cerrada (el textil llena el encuadre) no se ve el contorno de la pieza: estas
# medidas no dicen nada sobre su completitud y entran al modelo con el valor medio (z = 0).
MEDIDAS_CONTORNO = {"toca_encuadre", "compacidad", "fraccion_textil", "elongacion", "fraccion_lagunas", "fraccion_mayor", "n_fragmentos"}


def vector(medidas: dict[str, str], nombres: list[str], estandar: dict[str, list[float]]) -> np.ndarray:
    """Medidas transformadas y estandarizadas (media y desviacion de la fuente de calibracion)."""
    salida = []
    cerrada = medidas.get("encuadre_lleno") == "si"
    for nombre in nombres:
        if cerrada and nombre in MEDIDAS_CONTORNO:
            salida.append(0.0)
            continue
        valor = transformar(nombre, valor_medida(medidas, nombre))
        media, desviacion = estandar.get(nombre, [0.0, 1.0])
        salida.append((valor - media) / desviacion)
    return np.array(salida)


def capa_calidad(medidas: dict[str, str], config: dict[str, Any]) -> float:
    """Calidad fotografica (0-1): media ponderada de las medidas de [pesos.calidad] normalizadas."""
    componentes = config["pesos"]["calidad"]
    total = sum(componentes.values())
    return sum(peso * normalizar(float(medidas[m]), config["anclas"][m]) for m, peso in componentes.items()) / total


def leer_modelo(raiz: Path) -> dict[str, Any]:
    with (raiz / MODELO_APTITUD).open(encoding="utf-8") as archivo:
        return json.load(archivo)


def nivel(atributo: str, valor: float, config: dict[str, Any]) -> str:
    alto, medio = config["niveles"][atributo]
    etiquetas = NIVELES[atributo]
    return etiquetas[0] if valor >= alto else etiquetas[1] if valor >= medio else etiquetas[2]


def estructura(valores: dict[str, float], config: dict[str, Any]) -> str:
    """Descripcion de la estructura para el modelo combinatorio (informativa, no calibrada)."""
    criterio = config["estructura"]
    rasgos = []
    if valores["regularidad"] >= criterio["regularidad_minima"] and valores["repeticiones"] >= criterio["repeticiones_minimas"]:
        rasgos.append("repetitiva")
    if max(valores["simetria_horizontal"], valores["simetria_vertical"]) >= criterio["simetria_minima"]:
        rasgos.append("simetrica")
    return "_y_".join(rasgos) or "no_evidente"


def sigmoide(z):
    return 1 / (1 + np.exp(-np.clip(z, -30, 30)))


def predecir(x: np.ndarray, w: np.ndarray) -> np.ndarray:
    """Probabilidad del modelo logistico de un atributo (w[0] es el intercepto)."""
    return sigmoide(w[0] + x @ w[1:])


def probabilidad(medidas: dict[str, str], modelo: dict[str, Any], atributo: str) -> float:
    parametros = modelo["atributos"][atributo]
    x = vector(medidas, parametros["medidas"], modelo["estandarizacion"])
    return float(predecir(x, np.array(parametros["pesos"])))


def puntuar_registro(medidas: dict[str, str], config: dict[str, Any], modelo: dict[str, Any], pertinencia: str = "") -> dict[str, str]:
    """Ficha de aptitud de una imagen: atributos, puntaje, banda sugerida y justificacion."""
    salida = {campo: "" for campo in COLUMNAS_APTITUD}
    salida.update({campo: medidas[campo] for campo in ("id_global", "fuente", "id_fuente")})
    puertas = config["puertas"]

    if medidas["estado_imagen"] != "ok":
        salida.update({"banda_sugerida": "descartar", "referencia_sugerida": "no", "motivo_banda": "sin_imagen",
                       "justificacion": "No se pudo obtener la imagen institucional."})
        return salida

    valores = {campo: valor_medida(medidas, campo) for campo in COLUMNAS_MEDIDAS
               if campo not in {"id_global", "fuente", "id_fuente", "estado_imagen", "sha256_copia", "encuadre_lleno", "terminos_fragmento"}}
    valores["titulo_fragmento"] = valor_medida(medidas, "titulo_fragmento")
    componentes = {"fotografia": capa_calidad(medidas, config)}
    for atributo in modelo["puntaje"]["componentes"][1:]:
        componentes[atributo] = probabilidad(medidas, modelo, atributo)
    pesos = np.array(modelo["puntaje"]["pesos"])
    z = np.array([componentes[c] for c in modelo["puntaje"]["componentes"]])
    puntaje = float(100 * z @ pesos / pesos.sum())

    monocroma = valores["croma_p90"] < puertas["croma_monocromo"]
    niveles = {atributo: nivel(atributo, componentes[atributo], config) for atributo in NIVELES}
    if monocroma:
        niveles["colores"] = "no_identificables"  # sin color en la fotografia no hay colores que contar

    umbrales = modelo["umbrales"]
    if pertinencia in PERTINENCIA_DESCARTE:
        banda, motivo = "descartar", pertinencia
    elif pertinencia == "posible_figurilla":
        # Prudencia: un textil con figuras no debe salir por una regla; lo decide el revisor.
        banda, motivo = "revisar", pertinencia
    elif valores["lado_textil_px"] < puertas["lado_textil_minimo"]:
        banda, motivo = "descartar", "resolucion_insuficiente"
    elif monocroma:
        # Sin color no se pueden contar colores: nunca al principal, pero se conserva en el secundario.
        banda, motivo = "secundario", "fotografia_monocroma"
    elif puntaje >= umbrales["principal"]:
        banda, motivo = "principal", "puntaje"
    elif puntaje >= umbrales["descartar"]:
        banda, motivo = "revisar", "zona_intermedia"
    else:
        banda, motivo = "descartar", "puntaje"
    referencia = banda == "principal" and puntaje >= umbrales["referencia"]
    forma = estructura(valores, config)

    salida.update({
        "puntaje_aptitud": f"{puntaje:.1f}",
        "banda_sugerida": banda,
        "referencia_sugerida": "si" if referencia else "no",
        "motivo_banda": motivo,
        **niveles,
        "estructura": forma,
        "calidad_fotografica": f"{componentes['fotografia']:.3f}",
        **{f"prob_{a}": f"{componentes[a]:.3f}" for a in ("colores", "formas", "completitud", "referencia")},
        "justificacion": justificar(valores, niveles, forma, puntaje, motivo, referencia, puertas, componentes, medidas["encuadre_lleno"] == "si"),
    })
    return salida


ETIQUETAS_NIVEL = {
    "fotografia": {"buena": "fotografía buena", "regular": "fotografía regular", "deficiente": "fotografía deficiente"},
    "colores": {"identificables": "colores identificables", "parciales": "colores parcialmente identificables",
                "no_identificables": "colores no identificables"},
    "formas": {"visibles": "formas visibles", "parciales": "formas parcialmente visibles", "no_visibles": "formas no visibles"},
    "completitud": {"completo": "textil completo", "incierto": "completitud incierta", "incompleto": "textil incompleto"},
}


def decimal(valor: float, decimales: int) -> str:
    """Numero con coma decimal, como en el texto de la tesis."""
    return f"{valor:.{decimales}f}".replace(".", ",")


ETIQUETAS_ESTRUCTURA = {
    "repetitiva_y_simetrica": "repetitiva y simétrica", "repetitiva": "repetitiva",
    "simetrica": "simétrica", "no_evidente": "no evidente",
}


def cantidad(n: float, singular: str, plural: str) -> str:
    return f"{int(n)} {singular if int(n) == 1 else plural}"


def justificar(valores: dict[str, float], niveles: dict[str, str], forma: str, puntaje: float, motivo: str,
               referencia: bool, puertas: dict[str, Any], probabilidades: dict[str, float], cerrada: bool = False) -> str:
    """Conclusiones del analisis de la imagen: nivel de cada atributo, su probabilidad y medidas descriptivas."""
    p = {clave: decimal(valor, 2) for clave, valor in probabilidades.items()}
    partes = [
        f"{ETIQUETAS_NIVEL['fotografia'][niveles['fotografia']]} (nitidez {decimal(valores['nitidez_comun'], 2)}; "
        f"textil de {valores['lado_textil_px']:.0f} px de lado)",
        f"{ETIQUETAS_NIVEL['colores'][niveles['colores']]} (probabilidad {p['colores']}; "
        f"{cantidad(valores['colores_distintos'], 'color claramente distinto', 'colores claramente distintos')}, "
        f"{cantidad(valores['n_tonos'], 'tono', 'tonos')}, colorido {valores['colorido']:.0f})",
        f"{ETIQUETAS_NIVEL['formas'][niveles['formas']]} (probabilidad {p['formas']}; "
        f"bordes cromáticos en el {decimal(100 * valores['bordes_cromaticos'], 0)} % del textil)",
        f"{ETIQUETAS_NIVEL['completitud'][niveles['completitud']]} (probabilidad {p['completitud']}; "
        + ("toma cerrada, el contorno de la pieza no se ve" if cerrada else
           f"compacidad {decimal(valores['compacidad'], 2)}, lagunas {decimal(100 * valores['fraccion_lagunas'], 1)} %")
        + f"{', el título dice «fragment»' if valores['titulo_fragmento'] else ''})",
        f"estructura {ETIQUETAS_ESTRUCTURA[forma]}",
    ]
    texto = "; ".join(partes)
    texto = texto[:1].upper() + texto[1:] + f". Puntaje {puntaje:.0f}"
    texto += " (imagen de referencia sugerida)." if referencia else "."
    if motivo in TEXTOS_PERTINENCIA:
        texto = TEXTOS_PERTINENCIA[motivo] + " " + texto
    elif motivo == "fotografia_monocroma":
        texto = f"Fotografía en blanco y negro (croma {decimal(valores['croma_p90'], 1)}): el color no es identificable. " + texto
    elif motivo == "resolucion_insuficiente":
        texto = (f"El textil mide {valores['lado_textil_px']:.0f} px de lado en la imagen institucional "
                 f"(mínimo {puertas['lado_textil_minimo']}). ") + texto
    return texto


def puntuar(raiz: Path, config: dict[str, Any]) -> list[dict[str, str]]:
    metadatos = metadatos_pertinencia(raiz)
    modelo = leer_modelo(raiz)
    filas = [
        puntuar_registro(medidas, config, modelo, motivo_pertinencia(metadatos.get(medidas["id_global"]), config["pertinencia"]))
        for medidas in leer_csv(raiz / MEDIDAS)
    ]
    escribir_csv(raiz / SALIDA_APTITUD, COLUMNAS_APTITUD, filas)
    return filas


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Ficha de aptitud, puntaje y banda sugerida (etapa 3 del puntaje de aptitud).")
    parser.add_argument("--root", default=".", help="Raiz del repositorio.")
    args = parser.parse_args(argv)
    raiz = Path(args.root).resolve()
    if not (raiz / MODELO_APTITUD).exists():
        print(f"Falta {MODELO_APTITUD}: ejecute python -m src.imagenes.calibrar_aptitud antes de puntuar.")
        return 1
    filas = puntuar(raiz, leer_config_aptitud(raiz))
    conteo = Counter(fila["banda_sugerida"] for fila in filas)
    referencias = sum(fila["referencia_sugerida"] == "si" for fila in filas)
    print(f"Aptitud: {raiz / SALIDA_APTITUD} | " + ", ".join(f"{banda} {n}" for banda, n in sorted(conteo.items()))
          + f" | referencias sugeridas {referencias}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
