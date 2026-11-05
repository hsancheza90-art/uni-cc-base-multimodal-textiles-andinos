# Validacion de la anotacion v2

Generado por `python -m src.anotacion.aplicar_anotaciones_v2` (`src/anotacion/aplicar_anotaciones_v2.py`), paso del flujo. Workbooks de [acuerdo] en `config/anotacion.toml`; vocabulario: `config/vocabulario.toml`.

Este informe da solo conteos, sin valores ni observaciones por pieza: el lote 1 se re-anota a ciegas y el anotador no debe ver su primera anotacion. Los errores, si los hay, se detallan para poder corregirlos.

- Primera anotacion: `data/metadata/anotacion_v2.xlsx`: 462 piezas, 150 anotadas, 0 errores.
- Re-anotacion: `data/metadata/anotacion_v2_reanotacion.xlsx`: 30 piezas, 0 anotadas, 0 errores.
- Exportadas (si no hay errores): `data/metadata/anotaciones_v2.csv`, 150 piezas de la primera anotacion.

## Primera anotacion por lote

| Lote | Anotadas | Fechas | estado_anotacion | Con DUDA | Con CRITERIO | Con VOCAB |
|---|---|---|---|---|---|---|
| 1 | 30 | 2026-11-05 a 2026-11-05 | anotado_manual 30 | 19 | 10 | 6 |
| 2 | 30 | 2026-11-05 a 2026-11-05 | anotado_manual 30 | 16 | 2 | 3 |
| 3 | 30 | 2026-11-05 a 2026-11-05 | anotado_manual 30 | 13 | 2 | 4 |
| 4 | 30 | 2026-11-05 a 2026-11-05 | anotado_manual 30 | 15 | 4 | 5 |
| 5 | 30 | 2026-11-05 a 2026-11-05 | anotado_manual 30 | 14 | 6 | 4 |

Re-anotacion ciega del lote 1: puede empezar el 2026-11-12 (7 dias despues de la ultima fecha del lote, 2026-11-05).

`Con DUDA`, `Con CRITERIO`, `Con VOCAB`: piezas cuyas observaciones usan esa etiqueta para marcar lo que queda por decidir (una duda sobre un valor, un criterio de la guia o un hueco del vocabulario).

## Cobertura por columna (primera anotacion)

| Columna | Con valor | Vacias | `ausente` | `no_observable` | `desconocido` |
|---|---|---|---|---|---|
| `color_dominante` | 150 | 0 | 0 | 0 | 1 |
| `colores` | 150 | 0 | 0 | 0 | 0 |
| `contraste` | 150 | 0 | 0 | 0 | 0 |
| `densidad_visual` | 150 | 0 | 0 | 0 | 0 |
| `composicion` | 150 | 0 | 0 | 2 | 0 |
| `simetria` | 150 | 0 | 0 | 5 | 1 |
| `repeticion` | 150 | 0 | 0 | 5 | 0 |
| `borde` | 150 | 0 | 0 | 0 | 0 |
| `centro` | 150 | 0 | 0 | 0 | 0 |
| `motivos` | 150 | 0 | 1 | 0 | 0 |
| `familia_iconografica` | 150 | 0 | 1 | 0 | 0 |
| `motivo_principal` | 150 | 0 | 1 | 0 | 36 |
| `eje_bandas` | 150 | 0 | 72 | 15 | 0 |
| `secuencia_bandas` | 150 | 0 | 72 | 15 | 0 |
| `tipo_objeto_corregido` | 4 | 146 | 0 | 0 | 0 |
| `tipo_superficie_corregido` | 76 | 74 | 0 | 0 | 0 |
| `material_corregido` | 0 | 150 | 0 | 0 | 0 |
| `tecnica_corregida` | 1 | 149 | 0 | 0 | 0 |
| `estado_imagen_corregido` | 2 | 148 | 0 | 0 | 0 |

`Vacias`: sin anotar. Los estados van solos en la celda; `ausente` es una observacion y `no_observable` y `desconocido` dicen que el atributo no se pudo observar o decidir. En las correcciones, vacia significa «acepto el valor vigente».

## Avisos (primera anotacion)

| Aviso | Piezas |
|---|---|
| correccion igual al valor vigente | 3 |
| desconocido en una pieza que no esta en revisar (regla de los treinta segundos) | 38 |

## Avisos (re-anotacion)

Ninguno.

## Errores (primera anotacion)

Ninguno.

## Errores (re-anotacion)

Ninguno.
