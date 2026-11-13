# Acuerdo intra-anotador (anotacion v2, test-retest)

Generado por `python -m src.anotacion.acuerdo` (`src/anotacion/acuerdo.py`); parametros en `config/anotacion.toml` ([acuerdo] y [reanotacion]). Un kappa menor que 0.6 es una senal para revisar el atributo en la guia antes de congelar la anotacion; no es un criterio de aprobacion (decision R02, `docs/registro_decisiones.md`).

Sin segundo anotador (plan de cierre, D1), el mismo anotador re-anota a ciegas el lote 1, en otro orden y al menos 7 dias despues. Mide la estabilidad de la anotacion, no su acuerdo con otra persona: es una limitacion del estudio.

- Anotador A (primera anotacion): `data/metadata/anotacion_v2.xlsx` (hojas anotacion, fuera_del_nucleo): 462 piezas, 150 anotadas.
- Anotador B (re-anotacion): `data/metadata/anotacion_v2_reanotacion.xlsx` (hojas anotacion, fuera_del_nucleo): 30 piezas, 30 anotadas.
- Piezas anotadas en las dos (emparejadas por `id_global`) con el intervalo minimo: 30; fuera de plazo: 0.

## Acuerdo por atributo

| Capa | Atributo | Medida | n | Excluidas | Acuerdo observado | Acuerdo esperado | Kappa | Kappa >= 0.6 |
|---|---|---|---|---|---|---|---|---|
| Cromatica | `color_dominante` | kappa de Cohen | 29 | 1 | 0.966 | 0.317 | 0.949 | si |
| Cromatica | `colores` | Jaccard medio y kappa por etiqueta | 30 | 0 | 0.770 |  |  | ver kappa por etiqueta |
| Cromatica | `contraste` | kappa ponderado lineal | 30 | 0 | 0.917 | 0.684 | 0.736 | si |
| Cromatica | `densidad_visual` | kappa ponderado lineal | 30 | 0 | 0.933 | 0.702 | 0.776 | si |
| Estructural | `composicion` | kappa de Cohen | 24 | 6 | 0.875 | 0.234 | 0.837 | si |
| Estructural | `eje_bandas` | kappa de Cohen | 24 | 6 | 0.833 | 0.365 | 0.738 | si |
| Estructural | `secuencia_bandas` | similitud de edicion media | 24 | 6 | 0.797 |  |  | coincidencia exacta: 17 de 24 |
| Estructural | `borde` | kappa si/no (observables) | 24 | 6 | 0.875 | 0.500 | 0.750 | si |
| Estructural | `centro` | kappa si/no (observables) | 25 | 5 | 0.800 | 0.608 | 0.490 | no |
| Repeticion y simetria | `repeticion` | kappa ponderado lineal | 27 | 3 | 0.944 | 0.724 | 0.799 | si |
| Repeticion y simetria | `simetria` | kappa de Cohen | 23 | 7 | 0.826 | 0.259 | 0.765 | si |
| Iconografica | `motivos` | Jaccard medio y kappa por etiqueta | 30 | 0 | 0.844 |  |  | ver kappa por etiqueta |
| Iconografica | `familia_iconografica` | kappa de Cohen | 29 | 1 | 0.828 | 0.307 | 0.751 | si |
| Iconografica | `motivo_principal` | kappa de Cohen | 21 | 9 | 0.810 | 0.163 | 0.772 | si |
| Correcciones | `tipo_objeto_corregido` | kappa de Cohen | 30 | 0 | 0.933 | 0.097 | 0.926 | si |
| Correcciones | `tipo_superficie_corregido` | kappa de Cohen | 27 | 3 | 0.889 | 0.396 | 0.816 | si |
| Correcciones | `material_corregido` | Jaccard medio y kappa por etiqueta | 28 | 2 | 1.000 |  |  | ver kappa por etiqueta |
| Correcciones | `tecnica_corregida` | Jaccard medio y kappa por etiqueta | 25 | 5 | 0.960 |  |  | ver kappa por etiqueta |
| Correcciones | `estado_imagen_corregido` | kappa de Cohen | 30 | 0 | 1.000 | 1.000 |  | no estimable: una sola categoria observada (util) |

`n`: piezas comparadas en el atributo. `Excluidas`: piezas anotadas en las dos que no entran en el atributo (detalle abajo). En los campos multiples, `Acuerdo observado` es el indice de Jaccard medio por pieza; en las secuencias, la similitud de edicion media (1 - distancia de Levenshtein / longitud de la palabra mas larga).

## Piezas excluidas por atributo

| Atributo | Vacio en alguno | Fuera del vocabulario | No observable o desconocido |
|---|---|---|---|
| `color_dominante` | 0 | 0 | 1 |
| `colores` | 0 | 0 | 0 |
| `contraste` | 0 | 0 | 0 |
| `densidad_visual` | 0 | 0 | 0 |
| `composicion` | 0 | 0 | 6 |
| `eje_bandas` | 0 | 0 | 6 |
| `secuencia_bandas` | 0 | 0 | 6 |
| `borde` | 0 | 0 | 6 |
| `centro` | 0 | 0 | 5 |
| `repeticion` | 0 | 0 | 3 |
| `simetria` | 0 | 0 | 7 |
| `motivos` | 0 | 0 | 0 |
| `familia_iconografica` | 0 | 0 | 1 |
| `motivo_principal` | 0 | 0 | 9 |
| `tipo_objeto_corregido` | 0 | 0 | 0 |
| `tipo_superficie_corregido` | 3 | 0 | 0 |
| `material_corregido` | 2 | 0 | 0 |
| `tecnica_corregida` | 5 | 0 | 0 |
| `estado_imagen_corregido` | 0 | 0 | 0 |

`Vacio en alguno`: celda sin anotar en alguna de las dos. `No observable o desconocido`: alguna de las dos registro el estado `no_observable` o `desconocido` (regla de los treinta segundos) o, en `borde` y `centro`, `no_visible`; el estado `ausente` es una observacion y se compara como un valor mas.

## Observabilidad por atributo

Si el atributo se pudo observar en cada pasada: un valor (incluido `ausente`) frente a un estado de no observacion (`no_observable`, `desconocido` o `no_visible`). El kappa de arriba solo usa los pares observados en las dos; esta tabla muestra si la frontera entre «se ve» y «no se ve» es estable, que es lo que decide que bloques compara M3.

| Atributo | Observable en las dos | Solo en A | Solo en B | En ninguna | Acuerdo observado | Kappa |
|---|---|---|---|---|---|---|
| `color_dominante` | 29 | 0 | 1 | 0 | 0.967 | 0.000 |
| `colores` | 30 | 0 | 0 | 0 | 1.000 | no estimable: una sola categoria observada (si) |
| `contraste` | 30 | 0 | 0 | 0 | 1.000 | no estimable: una sola categoria observada (si) |
| `densidad_visual` | 30 | 0 | 0 | 0 | 1.000 | no estimable: una sola categoria observada (si) |
| `composicion` | 24 | 4 | 2 | 0 | 0.800 | -0.098 |
| `eje_bandas` | 24 | 2 | 2 | 2 | 0.867 | 0.423 |
| `secuencia_bandas` | 24 | 2 | 2 | 2 | 0.867 | 0.423 |
| `borde` | 24 | 2 | 1 | 3 | 0.900 | 0.609 |
| `centro` | 25 | 2 | 2 | 1 | 0.867 | 0.259 |
| `repeticion` | 27 | 1 | 1 | 1 | 0.933 | 0.464 |
| `simetria` | 23 | 4 | 2 | 1 | 0.800 | 0.143 |
| `motivos` | 30 | 0 | 0 | 0 | 1.000 | no estimable: una sola categoria observada (si) |
| `familia_iconografica` | 29 | 1 | 0 | 0 | 0.967 | 0.000 |
| `motivo_principal` | 21 | 3 | 3 | 3 | 0.800 | 0.375 |

## Piezas fuera de plazo

Anotadas en las dos, pero sin el intervalo minimo entre fechas: no entran en ningun atributo.

Ninguna.

## Kappa por etiqueta (campos multiples)

Presencia o ausencia de cada codigo en las piezas comparadas: muestra que etiqueta arrastra el desacuerdo.

| Atributo | Etiqueta | n | Acuerdo observado | Acuerdo esperado | Kappa | Kappa >= 0.6 |
|---|---|---|---|---|---|---|
| `colores` | rojo | 30 | 0.867 | 0.607 | 0.661 | si |
| `colores` | marron | 30 | 0.833 | 0.540 | 0.638 | si |
| `colores` | crema | 30 | 0.900 | 0.567 | 0.769 | si |
| `colores` | negro | 30 | 0.833 | 0.500 | 0.667 | si |
| `colores` | azul | 30 | 0.967 | 0.567 | 0.923 | si |
| `colores` | amarillo | 30 | 0.733 | 0.489 | 0.478 | no |
| `colores` | verde | 30 | 0.967 | 0.504 | 0.933 | si |
| `colores` | naranja | 30 | 0.867 | 0.642 | 0.627 | si |
| `colores` | rosado | 30 | 0.967 | 0.700 | 0.889 | si |
| `colores` | morado | 30 | 0.900 | 0.700 | 0.667 | si |
| `colores` | gris | 30 | 1.000 | 0.936 | 1.000 | si |
| `colores` | ocre | 30 | 0.800 | 0.722 | 0.280 | no |
| `motivos` | geometrico | 30 | 0.933 | 0.820 | 0.630 | si |
| `motivos` | antropomorfo | 30 | 0.933 | 0.536 | 0.856 | si |
| `motivos` | zoomorfo | 30 | 0.833 | 0.513 | 0.658 | si |
| `motivos` | fitomorfo | 30 | 0.967 | 0.847 | 0.783 | si |
| `motivos` | abstracto | 30 | 0.933 | 0.873 | 0.474 | no |
| `material_corregido` | algodon | 28 | 1.000 | 0.503 | 1.000 | si |
| `material_corregido` | fibra_de_camelido | 28 | 1.000 | 0.663 | 1.000 | si |
| `material_corregido` | lana | 28 | 1.000 | 0.541 | 1.000 | si |
| `material_corregido` | pigmento | 28 | 1.000 | 0.755 | 1.000 | si |
| `material_corregido` | fibra_textil | 28 | 1.000 | 0.931 | 1.000 | si |
| `tecnica_corregida` | tejido | 25 | 1.000 | 1.000 |  | no estimable: una sola categoria observada (si) |
| `tecnica_corregida` | tapiz | 25 | 1.000 | 0.539 | 1.000 | si |
| `tecnica_corregida` | bordado | 25 | 0.960 | 0.656 | 0.884 | si |
| `tecnica_corregida` | tela_doble | 25 | 1.000 | 0.853 | 1.000 | si |
| `tecnica_corregida` | pintado | 25 | 0.960 | 0.886 | 0.648 | si |

## Valores fuera del vocabulario

Ninguno.

## Como se mide

- Kappa de Cohen: (acuerdo observado - acuerdo esperado al azar) / (1 - acuerdo esperado). En los ordinales (`contraste`, `densidad_visual`, `repeticion`) un desacuerdo entre categorias vecinas cuenta como acuerdo parcial (pesos lineales), con el orden de [acuerdo.orden].
- Secuencias (`secuencia_bandas`): las dos palabras de bandas se comparan en el orden del eje de lectura. Se informa cuantas coinciden exactamente y la similitud media 1 - d / max(l1, l2), con d la distancia de Levenshtein: una banda de mas, de menos o distinta resta lo mismo. No hay acuerdo esperado al azar definido, asi que no se calcula kappa.
- Las correcciones se comparan por su valor efectivo: la correccion o, si esta vacia, el valor vigente del workbook. Dos correcciones vacias son acuerdo con el valor vigente.
- Si los dos anotadores usan una sola categoria, el acuerdo esperado es 1 y kappa no esta definido: se informa como no estimable, nunca como 1 ni como 0.
- Escala de referencia (Landis y Koch, 1977): 0,41-0,60 moderado, 0,61-0,80 sustancial, mas de 0,80 casi perfecto.
