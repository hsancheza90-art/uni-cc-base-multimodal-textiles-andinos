"""Condiciones de buena formación B3 a B7 de la anotación estructural (capítulo 5, sección 5.4.1).

B1 y B2 las aplica la validación de los libros (src/anotacion/aplicar_anotaciones_v2.py) y B8 es un
aviso de esa validación; B9 la impone la congelación y B10 se verificó a mano. Las cinco de este
módulo se comprueban sobre la anotación final, después de las correcciones de la revisión de
criterios: la primera anotación de los libros podía incumplirlas antes de corregirse, y por eso no
son errores de los libros sino de la versión que se congela.

- B3: si `eje_bandas` y `secuencia_bandas` son estados, son el mismo estado.
- B4: una palabra de bandas tiene al menos un tipo de banda: no está formada solo por lagunas.
- B5: una palabra no tiene dos lagunas contiguas.
- B6: si `composicion` es `bandas`, `secuencia_bandas` no es `ausente`.
- B7: `motivos` es `ausente` si y solo si `familia_iconografica` lo es.

Las celdas vacías no se evalúan: las cubre B8.
"""

from __future__ import annotations

from src.utils.vocabulario import Campo

LAGUNA = "laguna"
AUSENTE = "ausente"
CONDICIONES = {
    "B3": "si eje_bandas y secuencia_bandas son estados, son el mismo",
    "B4": "una palabra de bandas no esta formada solo por lagunas",
    "B5": "una palabra de bandas no tiene dos lagunas contiguas",
    "B6": "si composicion es bandas, secuencia_bandas no es ausente",
    "B7": "motivos es ausente si y solo si familia_iconografica lo es",
}


def incumplidas(fila: dict[str, str], vocabulario: dict[str, Campo]) -> list[str]:
    """Códigos de las condiciones B3 a B7 que incumple una fila de la anotación exportada."""
    eje, secuencia = fila.get("eje_bandas", ""), fila.get("secuencia_bandas", "")
    estados_eje, estados_secuencia = vocabulario["eje_bandas"].estados, vocabulario["secuencia_bandas"].estados
    salida: list[str] = []
    if eje in estados_eje and secuencia in estados_secuencia and eje != secuencia:
        salida.append("B3")
    if secuencia and secuencia not in estados_secuencia:
        simbolos = vocabulario["secuencia_bandas"].separar(secuencia)
        if all(s == LAGUNA for s in simbolos):
            salida.append("B4")
        if any(a == b == LAGUNA for a, b in zip(simbolos, simbolos[1:])):
            salida.append("B5")
    if fila.get("composicion", "") == "bandas" and secuencia == AUSENTE:
        salida.append("B6")
    motivos, familia = fila.get("motivos", ""), fila.get("familia_iconografica", "")
    if motivos and familia and (motivos == AUSENTE) != (familia == AUSENTE):
        salida.append("B7")
    return salida


def revisar(filas: list[dict[str, str]], vocabulario: dict[str, Campo]) -> dict[str, list[str]]:
    """Para cada condición, los id_global que la incumplen (listas vacías si se cumplen todas)."""
    resultado: dict[str, list[str]] = {codigo: [] for codigo in CONDICIONES}
    for fila in filas:
        for codigo in incumplidas(fila, vocabulario):
            resultado[codigo].append(fila["id_global"])
    return resultado
