"""Registro único de los archivos de revisión de cada fuente (MET, CMA y AIC).

Cada fuente tiene un workbook de revisión manual (el registro de las decisiones humanas)
y los CSV que el flujo deriva de él: uno por subconjunto (principal, secundario y
descartados), los pendientes y un resumen. Los módulos que leen o escriben esos archivos
toman las rutas de aquí, de modo que una fuente nueva se agrega en un solo lugar.

Las tres fuentes siguen el mismo patrón de nombres y el mismo esquema de columnas
(src/preprocessing/workbook_revision.py). Los CSV de CMA con el esquema heredado de la
curación v1 siguen en data/metadata/v1_congelado/, de donde los lee el consolidado v1.
"""

from __future__ import annotations

from dataclasses import dataclass

# Subconjuntos del corpus y valores admitidos en corpus_final (revisar = decision pendiente).
SUBCONJUNTOS = ("principal", "secundario", "descartados")
DECISIONES = (*SUBCONJUNTOS, "revisar")


@dataclass(frozen=True)
class Fuente:
    codigo: str
    workbook: str
    hoja: str
    salidas: dict[str, str]  # subconjunto -> CSV revisado
    pendientes: str
    reporte: str
    # Registro de origen de la fuente, con los datos oficiales que el workbook no copia
    # (institución, licencia, clasificación, fecha). En CMA y AIC es la lista de candidatos
    # del colector; en MET, el inventario de la descarga de la API (solo lectura).
    candidatos: str = ""
    clave_candidatos: str = ""

    @property
    def revisados(self) -> tuple[str, ...]:
        """CSV derivados del workbook: los tres subconjuntos y los pendientes."""
        return (*self.salidas.values(), self.pendientes)


# Nombre del CSV revisado de cada subconjunto, tras el prefijo de la fuente.
NOMBRES_SALIDA = {
    "principal": "corpus_principal_v2_revisado.csv",
    "secundario": "corpus_secundario_v2_revisado.csv",
    "descartados": "descartados_v2_revisado.csv",
}


# Registro de origen de cada fuente y su columna de identificador. MET no tiene colector v2:
# su origen es el inventario de la descarga de la API que formó el corpus MET v1. Se lee,
# nunca se escribe (no pertenece a data/metadata/v1_congelado/).
CANDIDATOS = {
    "MET": ("data/processed/corpus_met_textiles_andinos_v1_inventario_base.csv", "id_objeto"),
    "CMA": ("data/metadata/cma_andes_textiles_candidates.csv", "source_id"),
    "AIC": ("data/metadata/aic_andes_textiles_candidates.csv", "id_fuente"),
}


def _fuente(codigo: str) -> Fuente:
    prefijo = codigo.lower()
    candidatos, clave = CANDIDATOS.get(codigo, ("", ""))
    return Fuente(
        codigo=codigo,
        workbook=f"data/metadata/{prefijo}_revision_manual_v2.xlsx",
        hoja=f"revision_{prefijo}_v2",
        salidas={s: f"data/metadata/{prefijo}_{NOMBRES_SALIDA[s]}" for s in SUBCONJUNTOS},
        pendientes=f"data/metadata/{prefijo}_pendientes_revision_v2.csv",
        reporte=f"outputs/reports/{prefijo}_resumen_revision_manual_v2.md",
        candidatos=candidatos,
        clave_candidatos=clave,
    )


FUENTES = {codigo: _fuente(codigo) for codigo in ("MET", "CMA", "AIC")}
