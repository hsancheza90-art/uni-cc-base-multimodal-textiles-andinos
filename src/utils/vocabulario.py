"""Acceso al vocabulario controlado de config/vocabulario.toml.

La serie v1 (consolidado y taxonomia v1) lee la copia congelada RUTA_VOCABULARIO_V1, para
regenerarse identica aunque el vocabulario vigente gane valores nuevos.

Anotacion v2: un atributo puede admitir estados ([estados]: ausente, no_observable,
desconocido) en lugar de un valor; el estado va solo en la celda. Un campo de secuencia
(secuencia_bandas) guarda codigos en orden, separados por " > ".
"""

from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path

from src.utils.config import RAIZ_REPO

RUTA_VOCABULARIO = Path("config/vocabulario.toml")
RUTA_VOCABULARIO_V1 = Path("data/metadata/v1_congelado/vocabulario.toml")
SEPARADOR = "; "
SEPARADOR_SECUENCIA = " > "
# Estados que dicen que el atributo no se pudo observar: el acuerdo los cuenta aparte.
# ausente si es una observacion (el rasgo no esta) y se compara como un valor mas.
SIN_OBSERVACION = frozenset({"no_observable", "desconocido"})


@dataclass(frozen=True)
class Campo:
    nombre: str
    familia: str
    cuadro: str
    descripcion: str
    multiple: bool
    anotable: bool
    etiquetas: dict[str, str]
    extensiones: frozenset[str] = field(default_factory=frozenset)
    estados: dict[str, str] = field(default_factory=dict)  # codigo de estado -> etiqueta
    secuencia: bool = False

    @property
    def codigos(self) -> list[str]:
        return list(self.etiquetas)

    @property
    def admitidos(self) -> dict[str, str]:
        """Valores y estados que acepta una celda, con su etiqueta (lista del workbook)."""
        return {**self.etiquetas, **self.estados}

    def codigo_desde_etiqueta(self) -> dict[str, str]:
        """Etiqueta (o codigo) -> codigo, para recodificar valores escritos como en la tesis."""
        mapa = {etiqueta: codigo for codigo, etiqueta in self.admitidos.items()}
        mapa.update({codigo: codigo for codigo in self.admitidos})
        return mapa

    def separar(self, valor: str) -> list[str]:
        if not valor:
            return []
        if self.secuencia:
            partes = valor.split(">")
        else:
            partes = valor.split(";") if self.multiple else [valor]
        return [parte.strip() for parte in partes if parte.strip()]

    def invalidos(self, valor: str) -> list[str]:
        """Partes que no son del vocabulario; un estado solo vale si ocupa la celda completa."""
        partes = self.separar(valor)
        if len(partes) == 1 and partes[0] in self.estados:
            return []
        return [parte for parte in partes if parte not in self.etiquetas]

    def ordenar(self, codigos: list[str]) -> list[str]:
        """Orden del vocabulario, sin repetidos; los valores desconocidos quedan al final."""
        def clave(codigo: str) -> tuple[int, int, str]:
            if codigo in self.etiquetas:
                return (0, self.codigos.index(codigo), "")
            return (1, 0, codigo)

        return sorted(dict.fromkeys(codigos), key=clave)

    def recodificar(self, valor: str) -> str:
        """Convierte etiquetas a codigos y ordena los valores multiples (no las secuencias); deja intacto lo desconocido."""
        mapa = self.codigo_desde_etiqueta()
        codigos = [mapa.get(parte, parte) for parte in self.separar(valor)]
        if self.secuencia:
            return SEPARADOR_SECUENCIA.join(codigos)
        return SEPARADOR.join(self.ordenar(codigos) if self.multiple else codigos)


def leer_vocabulario(raiz: Path = RAIZ_REPO, ruta: Path = RUTA_VOCABULARIO) -> dict[str, Campo]:
    with (raiz / ruta).open("rb") as archivo:
        datos = tomllib.load(archivo)
    estados_declarados: dict[str, str] = datos.get("estados", {})
    campos: dict[str, Campo] = {}
    for nombre, definicion in datos["campos"].items():
        etiquetas = {valor[0]: valor[1] for valor in definicion["valores"]}
        if len(etiquetas) != len(definicion["valores"]):
            raise ValueError(f"Codigos repetidos en el vocabulario de {nombre}")
        estados = definicion.get("estados", [])
        if [e for e in estados if e not in estados_declarados or e in etiquetas]:
            raise ValueError(f"Estados de {nombre} no declarados en [estados] o repetidos como valor: {estados}")
        campos[nombre] = Campo(
            nombre=nombre,
            familia=definicion["familia"],
            cuadro=definicion["cuadro"],
            descripcion=definicion["descripcion"],
            multiple=bool(definicion["multiple"]),
            anotable=bool(definicion["anotable"]),
            etiquetas=etiquetas,
            extensiones=frozenset(valor[0] for valor in definicion["valores"] if len(valor) > 2),
            estados={estado: estados_declarados[estado] for estado in estados},
            secuencia=bool(definicion.get("secuencia", False)),
        )
    return campos
