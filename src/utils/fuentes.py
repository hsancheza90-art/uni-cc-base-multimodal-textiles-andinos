"""Registro único de los archivos de revisión de cada fuente (MET, CMA y AIC).

Cada fuente tiene un workbook de revisión manual (el registro de las decisiones humanas)
y los CSV que el flujo deriva de él: uno por subconjunto (principal, secundario y
descartados), los pendientes y un resumen. Los módulos que leen o escriben esos archivos
toman las rutas de aquí, de modo que una fuente nueva se agrega en un solo lugar.

Los nombres de CMA no siguen el patrón de MET y AIC (sin «_v2» en los CSV revisados)
porque son anteriores a la revisión v2; se conservan para no romper la trazabilidad
con la serie v1.
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

    @property
    def revisados(self) -> tuple[str, ...]:
        """CSV derivados del workbook: los tres subconjuntos y los pendientes."""
        return (*self.salidas.values(), self.pendientes)


def _fuente(codigo: str, salidas: tuple[str, str, str], pendientes: str) -> Fuente:
    prefijo = codigo.lower()
    return Fuente(
        codigo=codigo,
        workbook=f"data/metadata/{prefijo}_revision_manual_v2.xlsx",
        hoja=f"revision_{prefijo}_v2",
        salidas={s: f"data/metadata/{ruta}" for s, ruta in zip(SUBCONJUNTOS, salidas)},
        pendientes=f"data/metadata/{pendientes}",
        reporte=f"outputs/reports/{prefijo}_resumen_revision_manual_v2.md",
    )


FUENTES = {
    "MET": _fuente("MET", ("met_corpus_principal_v2_revisado.csv", "met_corpus_secundario_v2_revisado.csv",
                           "met_descartados_v2_revisado.csv"), "met_pendientes_revision_v2.csv"),
    "CMA": _fuente("CMA", ("cma_corpus_principal_revisado.csv", "cma_corpus_secundario_revisado.csv",
                           "cma_descartados_revisado.csv"), "cma_pendientes_revision_v2.csv"),
    "AIC": _fuente("AIC", ("aic_corpus_principal_v2_revisado.csv", "aic_corpus_secundario_v2_revisado.csv",
                           "aic_descartados_v2_revisado.csv"), "aic_pendientes_revision_v2.csv"),
}
