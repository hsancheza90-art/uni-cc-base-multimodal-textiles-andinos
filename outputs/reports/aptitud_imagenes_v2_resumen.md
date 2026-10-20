# Ficha de aptitud de las imágenes (v2)

Generado por `python -m src.imagenes.informe_aptitud` a partir de `data/metadata/aptitud_imagenes_v2.csv`. Modelo calibrado con 402 decisiones manuales AIC+MET+CMA (`config/aptitud_modelo.json`; detalle en `outputs/reports/aptitud_calibracion_v2.md`).

Cada imagen recibe un nivel por atributo (fotografía, colores, formas, completitud y estructura), un puntaje ordinal de 0 a 100 y una banda sugerida. El puntaje solo sugiere; la decisión es manual.

Bandas: principal si el puntaje ≥ 69.7 (imagen de referencia sugerida si además ≥ 84.6); descartar si < 34.9; revisar entre ambos. Antes del puntaje, las puertas: pertinencia por metadatos (plumaria, muñecos, piezas posteriores a 1532), resolución insuficiente o sin imagen → descartar; fotografía en blanco y negro → secundario.

## Bandas sugeridas por fuente

| Fuente | principal | secundario | revisar | descartar | Referencias sugeridas | Total |
|---|---|---|---|---|---|---|
| AIC | 154 | 107 | 138 | 109 | 81 | 508 |
| MET | 93 | 33 | 53 | 41 | 66 | 220 |
| CMA | 99 | 0 | 29 | 18 | 57 | 146 |

Motivos de banda: `puntaje` 413, `zona_intermedia` 213, `fotografia_monocroma` 140, `resolucion_insuficiente` 37, `plumaria` 33, `posterior_inca` 26, `posible_figurilla` 7, `muneco` 4, `sin_imagen` 1.

## Atributos por fuente

**fotografia**

| Fuente | buena | deficiente | regular |
|---|---|---|---|
| AIC | 138 | 191 | 179 |
| MET | 72 | 93 | 54 |
| CMA | 78 | 15 | 53 |

**colores**

| Fuente | identificables | no_identificables | parciales |
|---|---|---|---|
| AIC | 301 | 146 | 61 |
| MET | 163 | 38 | 18 |
| CMA | 132 | 3 | 11 |

**formas**

| Fuente | no_visibles | parciales | visibles |
|---|---|---|---|
| AIC | 81 | 125 | 302 |
| MET | 8 | 40 | 171 |
| CMA | 4 | 8 | 134 |

**completitud**

| Fuente | completo | incierto | incompleto |
|---|---|---|---|
| AIC | 121 | 109 | 278 |
| MET | 100 | 36 | 83 |
| CMA | 96 | 33 | 17 |

**estructura**

| Fuente | no_evidente | repetitiva | repetitiva_y_simetrica | simetrica |
|---|---|---|---|---|
| AIC | 298 | 145 | 25 | 40 |
| MET | 150 | 27 | 16 | 26 |
| CMA | 93 | 25 | 17 | 11 |

## AIC: banda sugerida frente a la decisión manual

Decisiones humanas (n = 345), sin las automáticas. Cifras sobre el modelo final: son optimistas frente a las de validación cruzada del informe de calibración.

| Decisión manual \ banda | principal | secundario | revisar | descartar |
|---|---|---|---|---|
| principal | 149 | 3 | 71 | 5 |
| secundario | 2 | 1 | 21 | 10 |
| descartados | 3 | 5 | 33 | 42 |

## Distribución por cultura

Control del sesgo de conservación: un filtro de imagen puede relegar a las culturas que se conservan sobre todo en fragmentos. Culturas con 8 o más candidatos AIC.

| Cultura | principal | secundario | revisar | descartar | Referencias sugeridas | Total |
|---|---|---|---|---|---|---|
| (sin cultura) | 23 | 58 | 55 | 61 | 8 | 197 |
| nazca | 21 | 17 | 37 | 8 | 15 | 83 |
| chancay | 38 | 10 | 11 | 6 | 22 | 65 |
| inca | 12 | 7 | 10 | 2 | 5 | 31 |
| chimú | 13 | 5 | 4 | 4 | 8 | 26 |
| lambayeque | 19 | 4 | 3 | 0 | 10 | 26 |
| pre-columbian | 6 | 3 | 6 | 2 | 3 | 17 |
| chuquibamba | 3 | 0 | 3 | 9 | 1 | 15 |
| huari | 11 | 0 | 0 | 1 | 4 | 12 |

