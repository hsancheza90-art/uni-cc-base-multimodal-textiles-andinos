# Validación ciega del puntaje de aptitud en MET y CMA

Generado por `python -m src.imagenes.validacion` desde `data/metadata/validacion_met_cma_v2.xlsx` (40 de 40 imágenes anotadas).

El revisor anotó sin ver el puntaje ni la decisión v1, con el criterio aplicado en AIC. La comparación principal es binaria (principal frente al resto), porque el puntaje no separa secundario de descartados y la zona «revisar» queda para la decisión manual.

| Conjunto | Anotadas | Con banda (sin revisar) | Acuerdo con el modelo | Kappa con el modelo | Acuerdo con v1 | Kappa con v1 |
|---|---|---|---|---|---|---|
| MET + CMA | 40 | 30 | 0.83 | 0.56 | 0.85 | 0.60 |
| MET | 20 | 15 | 0.80 | 0.44 | 0.85 | 0.48 |
| CMA | 20 | 15 | 0.87 | 0.66 | 0.85 | 0.67 |

## Anotación frente a banda sugerida

| Anotación \ banda | principal | revisar | descartar |
|---|---|---|---|
| principal | 20 | 8 | 3 |
| secundario | 2 | 1 | 0 |
| descartados | 0 | 1 | 5 |

En la banda «revisar» (10 imágenes) el revisor puso: principal 8, secundario 1, descartados 1.

## Desacuerdos con el modelo

| Registro | Anotación | Banda | Puntaje | Motivo del revisor |
|---|---|---|---|---|
| MET:307970 | secundario | principal | 74.2 | Textil con colores visibles |
| CMA:104236 | principal | descartar | 45.4 | textil con colores y formas visibles |
| CMA:126269 | secundario | principal | 70.4 | textil con colores visibles |
| MET:308106 | principal | descartar | 20.7 | textil incompleto con colores y formas visibles |
| MET:308098 | principal | descartar | 45.7 | fragmento textil con colores y formas visibles |

## Atributos: anotación del revisor frente a nivel estimado

| Atributo | Revisor | Imagen | Registros |
|---|---|---|---|
| colores | no | identificables | 1 |
| colores | no | no_identificables | 1 |
| colores | si | identificables | 26 |
| colores | si | no_identificables | 1 |
| colores | si | parciales | 7 |
| completitud | completo | completo | 6 |
| completitud | completo | incierto | 7 |
| completitud | incompleto | completo | 5 |
| completitud | incompleto | incierto | 1 |
| completitud | incompleto | incompleto | 11 |
| formas | no | no_visibles | 2 |
| formas | no | parciales | 1 |
| formas | no | visibles | 1 |
| formas | si | no_visibles | 1 |
| formas | si | parciales | 6 |
| formas | si | visibles | 25 |
