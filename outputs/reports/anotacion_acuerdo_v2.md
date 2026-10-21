# Acuerdo entre anotadores (anotacion v2)

Generado por `python -m src.anotacion.acuerdo` (`src/anotacion/acuerdo.py`); parametros en `config/anotacion.toml` ([acuerdo]). Umbral de acuerdo aceptable: kappa >= 0.6.

- Anotador A: `data/metadata/anotacion_v2.xlsx` (hojas anotacion, fuera_del_nucleo): 462 piezas, 0 anotadas.
- Anotador B: `data/metadata/anotacion_v2_evaluador2.xlsx` no existe todavia.
- Piezas anotadas por los dos (emparejadas por `id_global`): 0.

Todavia no hay piezas anotadas por los dos anotadores: ningun acuerdo es estimable. La tabla muestra los atributos que se mediran y con que medida.

## Acuerdo por atributo

| Capa | Atributo | Medida | n | Excluidas | Acuerdo observado | Acuerdo esperado | Kappa | Alcanza 0.6 |
|---|---|---|---|---|---|---|---|---|
| Cromatica | `color_dominante` | kappa de Cohen | 0 | 0 |  |  |  | no estimable: sin piezas comparables |
| Cromatica | `colores` | Jaccard medio y kappa por etiqueta | 0 | 0 |  |  |  | no estimable: sin piezas comparables |
| Cromatica | `contraste` | kappa ponderado lineal | 0 | 0 |  |  |  | no estimable: sin piezas comparables |
| Cromatica | `densidad_visual` | kappa ponderado lineal | 0 | 0 |  |  |  | no estimable: sin piezas comparables |
| Estructural | `composicion` | kappa de Cohen | 0 | 0 |  |  |  | no estimable: sin piezas comparables |
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

`n`: piezas comparadas en el atributo. `Excluidas`: piezas anotadas por los dos que no entran en el atributo (detalle abajo). En los campos multiples, `Acuerdo observado` es el indice de Jaccard medio por pieza.

## Piezas excluidas por atributo

| Atributo | Vacio en alguno | Fuera del vocabulario | No observable (no_visible) |
|---|---|---|---|
| `color_dominante` | 0 | 0 | 0 |
| `colores` | 0 | 0 | 0 |
| `contraste` | 0 | 0 | 0 |
| `densidad_visual` | 0 | 0 | 0 |
| `composicion` | 0 | 0 | 0 |
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

`Vacio en alguno`: incluye la regla de los treinta segundos. `No observable`: en `borde` y `centro`, piezas que alguno de los dos marco `no_visible`; el kappa se calcula solo sobre las que ambos marcaron `si` o `no`.

## Kappa por etiqueta (campos multiples)

Presencia o ausencia de cada codigo en las piezas comparadas: muestra que etiqueta arrastra el desacuerdo.

Sin piezas comparables.

## Valores fuera del vocabulario

Ninguno.

## Como se mide

- Kappa de Cohen: (acuerdo observado - acuerdo esperado al azar) / (1 - acuerdo esperado). En los ordinales (`contraste`, `densidad_visual`, `repeticion`) un desacuerdo entre categorias vecinas cuenta como acuerdo parcial (pesos lineales), con el orden de [acuerdo.orden].
- Las correcciones se comparan por su valor efectivo: la correccion o, si esta vacia, el valor vigente del workbook. Dos correcciones vacias son acuerdo con el valor vigente.
- Si los dos anotadores usan una sola categoria, el acuerdo esperado es 1 y kappa no esta definido: se informa como no estimable, nunca como 1 ni como 0.
- Escala de referencia (Landis y Koch, 1977): 0,41-0,60 moderado, 0,61-0,80 sustancial, mas de 0,80 casi perfecto.
