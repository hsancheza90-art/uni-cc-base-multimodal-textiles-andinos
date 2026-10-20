# Calibración de la ficha de aptitud por atributos (AIC+MET+CMA)

Generado por `python -m src.imagenes.calibrar_aptitud` (también lo ejecuta `python -m src.flujo`). Modelo: `config/aptitud_modelo.json`. Parámetros: `config/aptitud.toml` ([calibracion], [modelo], [atributos] y [puntaje]).

Calibran todas las decisiones humanas de AIC y, de MET y CMA, solo las tomadas con el criterio v2 (validación ciega y revisión v2); el resto de MET y CMA se decidió con criterios anteriores.

Las etiquetas salen del motivo libre del revisor (`src/imagenes/motivos.py`). Se excluyen los descartes por pertinencia (herramientas, plumaria, muñecos, piezas posteriores a 1532, no andinos) y las fotografías monocromas: no dependen de lo que la imagen permite identificar. Todas las cifras de esta página son **fuera de pliegue** (validación cruzada estratificada de 5 pliegues): cada registro se evalúa con modelos que no lo vieron.

## Registros de calibración

| Clase | AIC | MET | CMA | Total |
|---|---|---|---|---|
| descarte_imagen | 58 | 12 | 15 | 85 |
| secundario | 33 | 6 | 4 | 43 |
| principal | 69 | 6 | 10 | 85 |
| referencia | 156 | 27 | 6 | 189 |

## Atributos estimados desde la imagen

| Atributo | Etiqueta del revisor (positiva frente a negativa) | Registros | AUC fuera de pliegue | N.º de medidas |
|---|---|---|---|---|
| colores | colores: si frente a no | 372 | 0.908 | 21 |
| formas | formas: si frente a no | 355 | 0.861 | 21 |
| completitud | completitud: completo frente a incompleto | 325 | 0.874 | 21 |
| referencia | clase: referencia frente a principal | 274 | 0.813 | 21 |

## Puntaje ordinal

Media ponderada (pesos no negativos, modelo de odds proporcionales) de la calidad fotográfica y de las probabilidades de los atributos, escalada a 0-100:

| Componente | Peso (%) |
|---|---|
| fotografia | 0.0 |
| colores | 10.4 |
| formas | 29.7 |
| completitud | 29.9 |
| referencia | 30.0 |

Separación entre clases (AUC del puntaje fuera de pliegue; 0,5 = azar):

| Comparación | AUC |
|---|---|
| referencia frente a principal | 0.813 |
| principal frente a secundario | 0.634 |
| principal frente a descarte por imagen | 0.740 |
| secundario frente a descarte por imagen | 0.615 |
| referencia o principal frente al resto | 0.850 |

Medianas del puntaje por clase: descarte_imagen 42.8, secundario 54.0, principal 64.0, referencia 84.6.

## Umbrales

- Referencia: puntaje ≥ 84.6 (recoge el 50% de las imágenes de referencia del revisor: principal y textil completo con colores y formas visibles, o marcada como la mejor imagen; las que lo superan sin esa anotación son candidatas).
- Principal: puntaje ≥ 69.7 (al menos el 90% es principal o referencia).
- Descartar: puntaje < 34.9 (como máximo el 3% de los principales y referencias cae debajo).
- Entre descartar y principal: revisar.

## Separación por fuente

AUC fuera de pliegue en cada colección (útil = principal o referencia; resto = secundario o descarte por imagen). Las muestras MET y CMA son pequeñas y reúnen los casos difíciles: sus cifras tienen margen amplio.

| Fuente | Registros | Útil frente al resto | Colores | Formas | Completitud |
|---|---|---|---|---|---|
| AIC | 316 | 0.907 | 0.930 | 0.886 | 0.881 |
| MET | 51 | 0.759 | 0.786 | 0.727 | 0.984 |
| CMA | 35 | 0.829 | 0.817 | 0.800 | 0.756 |

| Clase del revisor \ banda (fuera de pliegue) | referencia | principal | revisar | descartar |
|---|---|---|---|---|
| descarte_imagen | 3 | 9 | 48 | 25 |
| secundario | 3 | 6 | 24 | 10 |
| principal | 11 | 15 | 51 | 8 |
| referencia | 94 | 69 | 26 | 0 |

