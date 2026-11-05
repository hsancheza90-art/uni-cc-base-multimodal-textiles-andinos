# Acuerdo intra-anotador (anotacion v2, test-retest)

Generado por `python -m src.anotacion.acuerdo` (`src/anotacion/acuerdo.py`); parametros en `config/anotacion.toml` ([acuerdo] y [reanotacion]). Umbral de acuerdo aceptable: kappa >= 0.6.

Sin segundo anotador (plan de cierre, D1), el mismo anotador re-anota a ciegas el lote 1, en otro orden y al menos 7 dias despues. Mide la estabilidad de la anotacion, no su acuerdo con otra persona: es una limitacion del estudio.

- Anotador A (primera anotacion): `data/metadata/anotacion_v2.xlsx` (hojas anotacion, fuera_del_nucleo): 462 piezas, 150 anotadas.
- Anotador B (re-anotacion): `data/metadata/anotacion_v2_reanotacion.xlsx` (hojas anotacion, fuera_del_nucleo): 30 piezas, 0 anotadas.
- Piezas anotadas en las dos (emparejadas por `id_global`) con el intervalo minimo: 0; fuera de plazo: 0.

Todavia no hay piezas anotadas en las dos anotaciones: ningun acuerdo es estimable. La tabla muestra los atributos que se mediran y con que medida.

## Acuerdo por atributo

| Capa | Atributo | Medida | n | Excluidas | Acuerdo observado | Acuerdo esperado | Kappa | Alcanza 0.6 |
|---|---|---|---|---|---|---|---|---|
| Cromatica | `color_dominante` | kappa de Cohen | 0 | 0 |  |  |  | no estimable: sin piezas comparables |
| Cromatica | `colores` | Jaccard medio y kappa por etiqueta | 0 | 0 |  |  |  | no estimable: sin piezas comparables |
| Cromatica | `contraste` | kappa ponderado lineal | 0 | 0 |  |  |  | no estimable: sin piezas comparables |
| Cromatica | `densidad_visual` | kappa ponderado lineal | 0 | 0 |  |  |  | no estimable: sin piezas comparables |
| Estructural | `composicion` | kappa de Cohen | 0 | 0 |  |  |  | no estimable: sin piezas comparables |
| Estructural | `eje_bandas` | kappa de Cohen | 0 | 0 |  |  |  | no estimable: sin piezas comparables |
| Estructural | `secuencia_bandas` | similitud de edicion media | 0 | 0 |  |  |  | no estimable: sin piezas comparables |
| Estructural | `borde` | kappa si/no (observables) | 0 | 0 |  |  |  | no estimable: sin piezas comparables |
| Estructural | `centro` | kappa si/no (observables) | 0 | 0 |  |  |  | no estimable: sin piezas comparables |
| Repeticion y simetria | `repeticion` | kappa ponderado lineal | 0 | 0 |  |  |  | no estimable: sin piezas comparables |
| Repeticion y simetria | `simetria` | kappa de Cohen | 0 | 0 |  |  |  | no estimable: sin piezas comparables |
| Iconografica | `motivos` | Jaccard medio y kappa por etiqueta | 0 | 0 |  |  |  | no estimable: sin piezas comparables |
| Iconografica | `familia_iconografica` | kappa de Cohen | 0 | 0 |  |  |  | no estimable: sin piezas comparables |
| Iconografica | `motivo_principal` | kappa de Cohen | 0 | 0 |  |  |  | no estimable: sin piezas comparables |
| Correcciones | `tipo_objeto_corregido` | kappa de Cohen | 0 | 0 |  |  |  | no estimable: sin piezas comparables |
| Correcciones | `tipo_superficie_corregido` | kappa de Cohen | 0 | 0 |  |  |  | no estimable: sin piezas comparables |
| Correcciones | `material_corregido` | Jaccard medio y kappa por etiqueta | 0 | 0 |  |  |  | no estimable: sin piezas comparables |
| Correcciones | `tecnica_corregida` | Jaccard medio y kappa por etiqueta | 0 | 0 |  |  |  | no estimable: sin piezas comparables |
| Correcciones | `estado_imagen_corregido` | kappa de Cohen | 0 | 0 |  |  |  | no estimable: sin piezas comparables |

`n`: piezas comparadas en el atributo. `Excluidas`: piezas anotadas en las dos que no entran en el atributo (detalle abajo). En los campos multiples, `Acuerdo observado` es el indice de Jaccard medio por pieza; en las secuencias, la similitud de edicion media (1 - distancia de Levenshtein / longitud de la palabra mas larga).

## Piezas excluidas por atributo

| Atributo | Vacio en alguno | Fuera del vocabulario | No observable o desconocido |
|---|---|---|---|
| `color_dominante` | 0 | 0 | 0 |
| `colores` | 0 | 0 | 0 |
| `contraste` | 0 | 0 | 0 |
| `densidad_visual` | 0 | 0 | 0 |
| `composicion` | 0 | 0 | 0 |
| `eje_bandas` | 0 | 0 | 0 |
| `secuencia_bandas` | 0 | 0 | 0 |
| `borde` | 0 | 0 | 0 |
| `centro` | 0 | 0 | 0 |
| `repeticion` | 0 | 0 | 0 |
| `simetria` | 0 | 0 | 0 |
| `motivos` | 0 | 0 | 0 |
| `familia_iconografica` | 0 | 0 | 0 |
| `motivo_principal` | 0 | 0 | 0 |
| `tipo_objeto_corregido` | 0 | 0 | 0 |
| `tipo_superficie_corregido` | 0 | 0 | 0 |
| `material_corregido` | 0 | 0 | 0 |
| `tecnica_corregida` | 0 | 0 | 0 |
| `estado_imagen_corregido` | 0 | 0 | 0 |

`Vacio en alguno`: celda sin anotar en alguna de las dos. `No observable o desconocido`: alguna de las dos registro el estado `no_observable` o `desconocido` (regla de los treinta segundos) o, en `borde` y `centro`, `no_visible`; el estado `ausente` es una observacion y se compara como un valor mas.

## Piezas fuera de plazo

Anotadas en las dos, pero sin el intervalo minimo entre fechas: no entran en ningun atributo.

Ninguna.

## Kappa por etiqueta (campos multiples)

Presencia o ausencia de cada codigo en las piezas comparadas: muestra que etiqueta arrastra el desacuerdo.

Sin piezas comparables.

## Valores fuera del vocabulario

Ninguno.

## Como se mide

- Kappa de Cohen: (acuerdo observado - acuerdo esperado al azar) / (1 - acuerdo esperado). En los ordinales (`contraste`, `densidad_visual`, `repeticion`) un desacuerdo entre categorias vecinas cuenta como acuerdo parcial (pesos lineales), con el orden de [acuerdo.orden].
- Secuencias (`secuencia_bandas`): las dos palabras de bandas se comparan en el orden del eje de lectura. Se informa cuantas coinciden exactamente y la similitud media 1 - d / max(l1, l2), con d la distancia de Levenshtein: una banda de mas, de menos o distinta resta lo mismo. No hay acuerdo esperado al azar definido, asi que no se calcula kappa.
- Las correcciones se comparan por su valor efectivo: la correccion o, si esta vacia, el valor vigente del workbook. Dos correcciones vacias son acuerdo con el valor vigente.
- Si los dos anotadores usan una sola categoria, el acuerdo esperado es 1 y kappa no esta definido: se informa como no estimable, nunca como 1 ni como 0.
- Escala de referencia (Landis y Koch, 1977): 0,41-0,60 moderado, 0,61-0,80 sustancial, mas de 0,80 casi perfecto.
