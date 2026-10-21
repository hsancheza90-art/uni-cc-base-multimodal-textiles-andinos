# Nucleo de anotacion v2

Generado por `python -m src.flujo` (`src/anotacion/nucleo.py`) desde `data/processed/corpus_textiles_andinos_v2_principal.csv`. Parametros en `config/anotacion.toml`: semilla 20261020, 150 piezas en lotes de 30, tope de una fuente por lote 60%.

## Cuota por fuente

Proporcional al principal v2, repartida por mayores restos.

| Fuente | Disponibles | Cuota exacta | Cuota |
|---|---|---|---|
| MET | 130 | 42.21 | 42 |
| CMA | 104 | 33.77 | 34 |
| AIC | 228 | 74.03 | 74 |
| Total | 462 | 150.00 | 150 |

## Estratos

Todas las piezas estan en el principal por decision del revisor; la banda es la sugerencia del puntaje de aptitud (`banda_sugerida`) y solo sirve para que el nucleo cubra imagenes de calidad distinta.

Cultura agrupada por banda de aptitud dentro de cada fuente. `Cuota`: reparto por mayores restos de la cuota de la fuente en proporcion a las piezas disponibles; `Asignadas`: piezas elegidas tras redistribuir los faltantes; `Faltantes`: cuota que el estrato no pudo cubrir con sus piezas.

| Fuente | Cultura agrupada | Banda | Disponibles | Cuota | Asignadas | Faltantes |
|---|---|---|---|---|---|---|
| MET | paracas | principal | 7 | 2 | 2 | 0 |
| MET | paracas | revisar | 23 | 7 | 7 | 0 |
| MET | paracas | descartar | 5 | 2 | 2 | 0 |
| MET | nasca | principal | 27 | 9 | 9 | 0 |
| MET | nasca | revisar | 9 | 3 | 3 | 0 |
| MET | wari | principal | 28 | 9 | 9 | 0 |
| MET | chancay | principal | 2 | 1 | 1 | 0 |
| MET | chancay | revisar | 1 | 0 | 0 | 0 |
| MET | inca | principal | 11 | 3 | 3 | 0 |
| MET | inca | revisar | 3 | 1 | 1 | 0 |
| MET | chimu | principal | 2 | 1 | 1 | 0 |
| MET | otras | principal | 8 | 3 | 3 | 0 |
| MET | otras | revisar | 4 | 1 | 1 | 0 |
| CMA | paracas | principal | 24 | 8 | 8 | 0 |
| CMA | paracas | revisar | 3 | 1 | 1 | 0 |
| CMA | nasca | principal | 3 | 1 | 1 | 0 |
| CMA | wari | principal | 13 | 4 | 4 | 0 |
| CMA | wari | revisar | 2 | 1 | 1 | 0 |
| CMA | chancay | principal | 19 | 6 | 6 | 0 |
| CMA | chancay | revisar | 6 | 2 | 2 | 0 |
| CMA | inca | principal | 5 | 2 | 2 | 0 |
| CMA | chimu | principal | 8 | 2 | 2 | 0 |
| CMA | chimu | revisar | 1 | 0 | 0 | 0 |
| CMA | otras | principal | 18 | 6 | 6 | 0 |
| CMA | otras | revisar | 2 | 1 | 1 | 0 |
| AIC | paracas | principal | 5 | 2 | 2 | 0 |
| AIC | paracas | revisar | 4 | 1 | 1 | 0 |
| AIC | nasca | principal | 21 | 7 | 7 | 0 |
| AIC | nasca | revisar | 19 | 6 | 6 | 0 |
| AIC | nasca | secundario | 1 | 0 | 0 | 0 |
| AIC | wari | principal | 11 | 4 | 4 | 0 |
| AIC | chancay | principal | 38 | 12 | 12 | 0 |
| AIC | chancay | revisar | 8 | 3 | 3 | 0 |
| AIC | chancay | secundario | 1 | 0 | 0 | 0 |
| AIC | inca | principal | 12 | 4 | 4 | 0 |
| AIC | inca | revisar | 6 | 2 | 2 | 0 |
| AIC | inca | secundario | 1 | 0 | 0 | 0 |
| AIC | chimu | principal | 14 | 5 | 5 | 0 |
| AIC | chimu | revisar | 3 | 1 | 1 | 0 |
| AIC | chimu | descartar | 1 | 0 | 0 | 0 |
| AIC | otras | principal | 27 | 9 | 9 | 0 |
| AIC | otras | revisar | 13 | 4 | 4 | 0 |
| AIC | otras | descartar | 4 | 1 | 1 | 0 |
| AIC | sin_cultura | principal | 21 | 7 | 7 | 0 |
| AIC | sin_cultura | revisar | 18 | 6 | 6 | 0 |

Sin faltantes: con un reparto proporcional y un nucleo menor que el corpus, ninguna cuota puede superar las piezas de su estrato. La redistribucion queda como salvaguarda si cambia el diseno.

## Lotes

Composicion por fuente:

| Lote | MET | CMA | AIC | Total |
|---|---|---|---|---|
| 1 | 9 | 7 | 14 | 30 |
| 2 | 9 | 6 | 15 | 30 |
| 3 | 8 | 7 | 15 | 30 |
| 4 | 8 | 7 | 15 | 30 |
| 5 | 8 | 7 | 15 | 30 |

Composicion por banda de aptitud:

| Lote | principal | revisar | descartar |
|---|---|---|---|
| 1 | 20 | 9 | 1 |
| 2 | 20 | 9 | 1 |
| 3 | 23 | 7 | 0 |
| 4 | 22 | 8 | 0 |
| 5 | 22 | 7 | 1 |

Composicion por cultura agrupada:

| Lote | paracas | nasca | wari | chancay | inca | chimu | otras | sin_cultura |
|---|---|---|---|---|---|---|---|---|
| 1 | 5 | 5 | 4 | 4 | 3 | 1 | 6 | 2 |
| 2 | 4 | 7 | 3 | 4 | 4 | 1 | 5 | 2 |
| 3 | 5 | 5 | 3 | 6 | 1 | 4 | 3 | 3 |
| 4 | 5 | 4 | 4 | 5 | 2 | 2 | 5 | 3 |
| 5 | 4 | 5 | 4 | 5 | 2 | 1 | 6 | 3 |

## Cultura agrupada

El campo `cultura` de la fuente se normaliza y se buscan los terminos de cada grupo como palabra completa.

| Grupo | Terminos | Principal v2 | Nucleo |
|---|---|---|---|
| paracas | paracas, ocucaje | 71 | 23 |
| nasca | nasca, nazca | 80 | 26 |
| wari | wari, huari | 54 | 18 |
| chancay | chancay | 75 | 24 |
| inca | inca, inka | 38 | 12 |
| chimu | chimu | 29 | 9 |
| otras | - | 76 | 25 |
| sin_cultura | - | 39 | 13 |

Valores que nombran mas de un grupo, resueltos uno por uno por el revisor:

| Valor de la fuente | Grupo | Registros | Motivo |
|---|---|---|---|
| Nasca-Wari | wari | 1 | Estilo hibrido: se asigna a Wari, la cultura con mayor dominancia. |
| Peru, South Coast, Nasca-Huari style | wari | 1 | Estilo hibrido: se asigna a Wari, la cultura con mayor dominancia. |
| Peru, South Coast, Paracas or Nasca? | nasca | 1 | Atribucion dudosa entre dos grupos: se asigna al mas grande del principal v2 (nasca 79, paracas 71). |
| Peru, North Coast, Chimu-Inka | inca | 1 | Estilo Chimu bajo dominio inca: se asigna a Inca, la cultura con mayor dominancia. |
| Peru, Central Andes, Chimú or Chimú-Inka, 11th-16th century | chimu | 1 | Chimu esta en las dos alternativas de la atribucion. |
| Peru, Chimú or Chimú-Inka, 12th-16th century | chimu | 1 | Chimu esta en las dos alternativas de la atribucion. |
| Peru, Central Coast, Chancay-Chimú style, 11th-15th century | chancay | 1 | Estilo Chancay con rasgos Chimu: se asigna a Chancay (decision del revisor). |
