# Revision de criterios de la anotacion v2

Generado por `python -m src.anotacion.aplicar_anotaciones_v2`, paso del flujo, con las reglas de `src/anotacion/revision_criterios.py`. Workbook: `data/metadata/anotacion_v2_revision_criterios.xlsx`; parametros en `config/anotacion.toml` ([revision_criterios]).

Los lotes 2, 3, 4, 5 se anotaron antes de escribir la definicion de banda (R12) y la frontera entre simetria traslacional y repeticion modular (R16). El anotador vuelve a mirar las piezas afectadas y confirma o corrige. La primera anotacion no se modifica en su workbook: las correcciones se aplican al exportar `data/metadata/anotaciones_v2.csv` y quedan registradas abajo.

- Piezas en revision: 108.
- Confirmadas: 0; corregidas: 0; pendientes: 108.
- Valores corregidos: 0.
- Propuestas automaticas sin verificar (`revisor = auto`): 108. No se aplican: cuentan como pendientes hasta que el revisor las verifica y firma.

## Piezas por motivo de revision

| Motivo | Piezas |
|---|---|
| R12 | 52 |
| R16 | 85 |
| OBS | 32 |
| ID | 22 |

`R12`: tiene palabra de bandas. `R16`: simetria traslacional o repeticion_modular. `OBS`: sus observaciones marcan una duda o un criterio sobre un atributo que usa M3. `ID`: sus observaciones piden verificar que la imagen corresponde al registro. Una pieza puede tener varios motivos.

## Observaciones que no entran a la revision

| Tipo | Piezas |
|---|---|
| dudas sobre atributos que M3 no usa | 46 |
| huecos de vocabulario (VOCAB) | 16 |

No tocan ningun atributo de M3 (`motivo_principal`, color, tecnica, tipo de objeto o de superficie) o son huecos del vocabulario. No se resuelven en la version 2.1 y se declaran como limitacion.

## Registro de adjudicaciones

Ninguna correccion.

## Imagenes que no corresponden al registro

Ninguna.

## Errores

Ninguno.
