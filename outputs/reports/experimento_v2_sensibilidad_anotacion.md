# Sensibilidad de M3 a la revision asistida de la anotacion (desarrollo)

Generado por `python -m src.experimento.sensibilidad_anotacion` (`src/experimento/sensibilidad_anotacion.py`), paso del flujo. Compara la anotacion previa a la revision de criterios (`data/metadata/anotacion_v2_previa_revision.csv`: exportacion del commit `d0bce67` con las ocho anotaciones desplazadas trasladadas a su fila, sin corregir) con la anotacion v2.1 congelada. Solo consultas y juicios de desarrollo; pesos de `[m3.pesos]`. Analisis exploratorio: no decide ninguna hipotesis.

## Cambios en la anotacion

- Piezas del nucleo con algun atributo de M3 distinto: 46 de 150.
- Piezas con palabra de bandas: previa 66, v2.1 53.

| Atributo | Piezas con valor distinto |
|---|---|
| composicion | 28 |
| secuencia_bandas | 34 |
| borde | 24 |
| centro | 0 |
| simetria | 34 |
| repeticion | 0 |
| motivos | 23 |
| familia_iconografica | 23 |

## Rankings por consulta de desarrollo

`Top 10 comun`: candidatos compartidos por los 10 primeros de las dos versiones. `Spearman`: correlacion entre las posiciones de todos los candidatos. `Juzgada`: parte del top de la version previa con juicio (el pool se construyo con la v2.1; un candidato sin juicio cuenta como 0).

| Consulta | Sistema | Consulta cambiada | Top 10 comun | Spearman | nDCG@10 previa | nDCG@10 v2.1 | Juzgada (previa) |
|---|---|---|---|---|---|---|---|
| T3-D01 | M3 | no | 4 | 0.766 | 0.424 | 0.470 | 0.50 |
| T3-D01 | M3-sin-orden | no | 4 | 0.766 | 0.424 | 0.470 | 0.50 |
| T3-D02 | M3 | no | 6 | 0.833 | 0.118 | 0.149 | 0.70 |
| T3-D02 | M3-sin-orden | no | 6 | 0.833 | 0.118 | 0.149 | 0.70 |
| T3-D03 | M3 | no | 9 | 0.864 | 0.535 | 0.555 | 0.90 |
| T3-D03 | M3-sin-orden | no | 9 | 0.864 | 0.535 | 0.555 | 0.90 |
| T3-D04 | M3 | si | 4 | 0.562 | 0.536 | 0.555 | 0.70 |
| T3-D04 | M3-sin-orden | si | 3 | 0.550 | 0.583 | 0.555 | 0.70 |
| T3-D05 | M3 | no | 5 | 0.716 | 0.394 | 0.610 | 0.70 |
| T3-D05 | M3-sin-orden | no | 5 | 0.716 | 0.394 | 0.610 | 0.70 |
| T3-D06 | M3 | si | 5 | 0.735 | 0.231 | 0.655 | 0.50 |
| T3-D06 | M3-sin-orden | si | 4 | 0.748 | 0.193 | 0.805 | 0.50 |
| T3-D07 | M3 | no | 5 | 0.799 | 0.066 | 0.044 | 0.70 |
| T3-D07 | M3-sin-orden | no | 5 | 0.799 | 0.066 | 0.044 | 0.70 |
| T3-D08 | M3 | no | 8 | 0.837 | 0.195 | 0.146 | 0.90 |
| T3-D08 | M3-sin-orden | no | 8 | 0.837 | 0.195 | 0.146 | 0.90 |
| T3-D09 | M3 | no | 6 | 0.848 | 0.413 | 0.346 | 0.90 |
| T3-D09 | M3-sin-orden | no | 7 | 0.853 | 0.273 | 0.297 | 0.90 |
| T3-D10 | M3 | no | 7 | 0.907 | 0.757 | 0.785 | 0.70 |
| T3-D10 | M3-sin-orden | no | 7 | 0.907 | 0.757 | 0.785 | 0.70 |

## Resumen

| Sistema | nDCG@10 medio, previa | nDCG@10 medio, v2.1 |
|---|---|---|
| M3 | 0.367 | 0.431 |
| M3-sin-orden | 0.354 | 0.441 |

- Diferencia M3 - M3-sin-orden (control de H2), media por consulta: previa 0.013 (3 de 10 consultas distintas de cero); v2.1 -0.010 (2 de 10).

Lectura. La comparacion de rankings (top comun y Spearman) no depende de los juicios y es la medida principal de la sensibilidad. El nDCG debe leerse con dos reservas. Primera: el pool se construyo con la v2.1, de modo que el nDCG de la version previa se subestima cuando su top incluye candidatos sin juicio. Segunda: las propuestas de la revision de criterios (R20) y la segunda opinion de los juicios de desarrollo (R25) provienen de la misma familia de modelos; una mejora del nDCG con la v2.1 puede reflejar ese criterio compartido y no una anotacion mas fiel a la imagen.
