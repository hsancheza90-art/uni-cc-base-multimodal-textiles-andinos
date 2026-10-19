# Ficha de aptitud de las imágenes (v2)

Generado por `python -m src.imagenes.informe_aptitud` a partir de `data/metadata/aptitud_imagenes_v2.csv`. Modelo calibrado con 316 decisiones manuales AIC (`config/aptitud_modelo.json`; detalle en `outputs/reports/aptitud_calibracion_aic_v2.md`).

Cada imagen recibe un nivel por atributo (fotografía, colores, formas, completitud y estructura), un puntaje ordinal de 0 a 100 y una banda sugerida. El puntaje solo sugiere; la decisión es manual.

Bandas: principal si el puntaje ≥ 54.5 (imagen de referencia sugerida si además ≥ 84.3); descartar si < 37.5; revisar entre ambos. Antes del puntaje, las puertas: pertinencia por metadatos (plumaria, muñecos, piezas posteriores a 1532), resolución insuficiente o sin imagen → descartar; fotografía en blanco y negro → secundario.

## Bandas sugeridas por fuente

| Fuente | principal | secundario | revisar | descartar | Referencias sugeridas | Total |
|---|---|---|---|---|---|---|
| AIC | 219 | 107 | 59 | 123 | 96 | 508 |
| MET | 111 | 33 | 27 | 49 | 34 | 220 |
| CMA | 118 | 0 | 8 | 20 | 47 | 146 |

Motivos de banda: `puntaje` 539, `fotografia_monocroma` 140, `zona_intermedia` 94, `resolucion_insuficiente` 37, `plumaria` 33, `posterior_inca` 26, `muneco` 4, `sin_imagen` 1.

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
| AIC | 302 | 136 | 70 |
| MET | 154 | 45 | 20 |
| CMA | 132 | 5 | 9 |

**formas**

| Fuente | no_visibles | parciales | visibles |
|---|---|---|---|
| AIC | 77 | 122 | 309 |
| MET | 24 | 40 | 155 |
| CMA | 5 | 13 | 128 |

**completitud**

| Fuente | completo | incierto | incompleto |
|---|---|---|---|
| AIC | 139 | 100 | 269 |
| MET | 59 | 64 | 96 |
| CMA | 80 | 48 | 18 |

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
| principal | 191 | 3 | 28 | 6 |
| secundario | 12 | 1 | 9 | 12 |
| descartados | 11 | 5 | 11 | 56 |

## Distribución por cultura

Control del sesgo de conservación: un filtro de imagen puede relegar a las culturas que se conservan sobre todo en fragmentos. Culturas con 8 o más candidatos AIC.

| Cultura | principal | secundario | revisar | descartar | Referencias sugeridas | Total |
|---|---|---|---|---|---|---|
| (sin cultura) | 46 | 58 | 24 | 69 | 10 | 197 |
| nazca | 38 | 17 | 16 | 12 | 16 | 83 |
| chancay | 45 | 10 | 4 | 6 | 26 | 65 |
| inca | 17 | 7 | 5 | 2 | 8 | 31 |
| chimú | 14 | 5 | 3 | 4 | 9 | 26 |
| lambayeque | 22 | 4 | 0 | 0 | 11 | 26 |
| pre-columbian | 9 | 3 | 2 | 3 | 5 | 17 |
| chuquibamba | 4 | 0 | 1 | 10 | 2 | 15 |
| huari | 11 | 0 | 0 | 1 | 3 | 12 |

