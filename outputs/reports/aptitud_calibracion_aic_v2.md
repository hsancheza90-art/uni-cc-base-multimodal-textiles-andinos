# Calibración de la ficha de aptitud por atributos (AIC)

Generado por `python -m src.imagenes.calibrar_aptitud --fuente aic` (también lo ejecuta `python -m src.flujo`). Modelo: `config/aptitud_modelo.json`. Parámetros: `config/aptitud.toml` ([modelo], [atributos] y [puntaje]).

Las etiquetas salen del motivo libre del revisor (`src/imagenes/motivos.py`). Se excluyen los descartes por pertinencia (herramientas, plumaria, muñecos, piezas posteriores a 1532, no andinos) y las fotografías monocromas: no dependen de lo que la imagen permite identificar. Todas las cifras de esta página son **fuera de pliegue** (validación cruzada estratificada de 5 pliegues): cada registro se evalúa con modelos que no lo vieron.

## Registros de calibración

| Clase | Registros |
|---|---|
| descarte_imagen | 58 |
| secundario | 33 |
| principal | 69 |
| referencia | 156 |

## Atributos estimados desde la imagen

| Atributo | Etiqueta del revisor (positiva frente a negativa) | Registros | AUC fuera de pliegue | N.º de medidas |
|---|---|---|---|---|
| colores | colores: si frente a no | 298 | 0.940 | 21 |
| formas | formas: si frente a no | 294 | 0.894 | 21 |
| completitud | completitud: completo frente a incompleto | 267 | 0.889 | 21 |
| referencia | clase: referencia frente a principal | 225 | 0.819 | 21 |

## Puntaje ordinal

Media ponderada (pesos no negativos, modelo de odds proporcionales) de la calidad fotográfica y de las probabilidades de los atributos, escalada a 0-100:

| Componente | Peso (%) |
|---|---|
| fotografia | 0.0 |
| colores | 12.1 |
| formas | 26.3 |
| completitud | 31.6 |
| referencia | 30.0 |

Separación entre clases (AUC del puntaje fuera de pliegue; 0,5 = azar):

| Comparación | AUC |
|---|---|
| referencia frente a principal | 0.828 |
| principal frente a secundario | 0.672 |
| principal frente a descarte por imagen | 0.829 |
| secundario frente a descarte por imagen | 0.633 |
| referencia o principal frente al resto | 0.894 |

Medianas del puntaje por clase: descarte_imagen 35.2, secundario 48.9, principal 61.9, referencia 84.3.

## Umbrales

- Referencia: puntaje ≥ 84.3 (recoge el 50% de las imágenes de referencia del revisor: principal y textil completo con colores y formas visibles, o marcada como la mejor imagen; las que lo superan sin esa anotación son candidatas).
- Principal: puntaje ≥ 54.5 (al menos el 90% es principal o referencia).
- Descartar: puntaje < 37.5 (como máximo el 3% de los principales y referencias cae debajo).
- Entre descartar y principal: revisar.

| Clase del revisor \ banda (fuera de pliegue) | referencia | principal | revisar | descartar |
|---|---|---|---|---|
| descarte_imagen | 1 | 8 | 17 | 32 |
| secundario | 1 | 11 | 10 | 11 |
| principal | 8 | 35 | 20 | 6 |
| referencia | 78 | 72 | 6 | 0 |

