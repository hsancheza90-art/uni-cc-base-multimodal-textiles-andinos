"""Acceso al vocabulario controlado de config/vocabulario.toml."""

from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path

from src.utils.config import RAIZ_REPO

RUTA_VOCABULARIO = Path("config/vocabulario.toml")
SEPARADOR = "; "


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

    @property
    def codigos(self) -> list[str]:
        return list(self.etiquetas)

    def codigo_desde_etiqueta(self) -> dict[str, str]:
        """Etiqueta (o codigo) -> codigo, para recodificar valores escritos como en la tesis."""
        mapa = {etiqueta: codigo for codigo, etiqueta in self.etiquetas.items()}
        mapa.update({codigo: codigo for codigo in self.etiquetas})
        return mapa

    def separar(self, valor: str) -> list[str]:
        if not valor:
            return []
        partes = valor.split(";") if self.multiple else [valor]
        return [parte.strip() for parte in partes if parte.strip()]

    def invalidos(self, valor: str) -> list[str]:
        return [parte for parte in self.separar(valor) if parte not in self.etiquetas]

    def ordenar(self, codigos: list[str]) -> list[str]:
        """Orden del vocabulario, sin repetidos; los valores desconocidos quedan al final."""
        def clave(codigo: str) -> tuple[int, int, str]:
            if codigo in self.etiquetas:
                return (0, self.codigos.index(codigo), "")
            return (1, 0, codigo)

        return sorted(dict.fromkeys(codigos), key=clave)

    def recodificar(self, valor: str) -> str:
        """Convierte etiquetas a codigos y ordena los valores multiples; deja intacto lo desconocido."""
        mapa = self.codigo_desde_etiqueta()
        codigos = [mapa.get(parte, parte) for parte in self.separar(valor)]
        return SEPARADOR.join(self.ordenar(codigos) if self.multiple else codigos)


def leer_vocabulario(raiz: Path = RAIZ_REPO) -> dict[str, Campo]:
    with (raiz / RUTA_VOCABULARIO).open("rb") as archivo:
        datos = tomllib.load(archivo)
    campos: dict[str, Campo] = {}
    for nombre, definicion in datos["campos"].items():
        etiquetas = {valor[0]: valor[1] for valor in definicion["valores"]}
        if len(etiquetas) != len(definicion["valores"]):
            raise ValueError(f"Codigos repetidos en el vocabulario de {nombre}")
        campos[nombre] = Campo(
            nombre=nombre,
            familia=definicion["familia"],
            cuadro=definicion["cuadro"],
            descripcion=definicion["descripcion"],
            multiple=bool(definicion["multiple"]),
            anotable=bool(definicion["anotable"]),
            etiquetas=etiquetas,
            extensiones=frozenset(valor[0] for valor in definicion["valores"] if len(valor) > 2),
        )
    return campos
