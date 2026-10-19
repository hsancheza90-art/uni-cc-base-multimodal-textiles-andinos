# Protocolo de aptitud analítica (corpus v2)

Procedimiento con el que se decide si la imagen de un textil sirve para el estudio y en qué subconjunto entra. Reemplaza, para la v2, el juicio general de «imagen útil» y «valor computacional» del §6.3.2 por atributos observables y verificables. La v1 (MET+CMA, etiqueta `corpus-met-cma-v1.2`) sigue con su protocolo: `docs/corpus/protocolo_curacion_met_cma_v1.md`.

## Criterio

Fijado por el revisor en la revisión de las 508 imágenes AIC (octubre de 2026) y aplicado igual a todas las fuentes:

| Subconjunto | Criterio |
|---|---|
| **Principal** | Los colores y las figuras del textil se identifican a primera vista. |
| Principal: **imagen de referencia** | Además, el textil está completo y se puede verificar en la fotografía: es la mejor imagen para el estudio. |
| Principal: incompleto legible | El textil está incompleto por rotura, corte o desgaste, pero sus colores y formas se identifican. |
| **Secundario** | La imagen no permite identificar bien colores o formas (por ejemplo, fotografía monocroma o pieza muy deteriorada). |
| **Descarte** | No sirve para el estudio o no es pertinente: plumaria, muñecos, piezas posteriores a 1532, objetos no textiles o no andinos, herramientas, imagen inexistente. |

El criterio no exige que la pieza esté entera: el modelo combinatorio necesita contar atributos identificables (colores, módulos, figuras), y un fragmento legible los conserva. Con eso la base del estudio crece sin perder rigor.

## Etapas

| # | Etapa | Comando | Requiere | Produce | Decisión humana |
|---|---|---|---|---|---|
| 0 | Recolección | `python -m src.collectors.<fuente>_collector` | Red | `data/metadata/<fuente>_andes_textiles_candidates.csv` | — |
| 1 | Copias de evaluación | `python -m src.imagenes.descargar_evaluacion` | Red | `data/images/evaluacion/` (fuera de git) y `data/metadata/imagenes_evaluacion_manifiesto_v2.csv` | — |
| 2 | Medidas | `python -m src.imagenes.medidas` | Imágenes locales | `data/metadata/aptitud_medidas_v2.csv` | — |
| 3 | Revisión manual | Workbook `data/metadata/<fuente>_revision_manual_v2.xlsx` | — | `corpus_final`, `decision_revision`, `motivo_revision` | **Sí: es la referencia de todo lo demás** |
| 4 | Calibración | `python -m src.imagenes.calibrar_aptitud --fuente aic` (lo ejecuta el flujo) | — | `config/aptitud_modelo.json`, `outputs/reports/aptitud_calibracion_aic_v2.md` | — |
| 5 | Ficha y puntaje | `python -m src.imagenes.aptitud` (lo ejecuta el flujo) | — | `data/metadata/aptitud_imagenes_v2.csv` | — |
| 6 | Ficha en los workbooks | `python -m src.imagenes.aptitud_workbooks --fuente aic` (o `--solo-reglas` en fuentes no validadas) | Excel cerrado | Columnas informativas, motivo enriquecido y decisiones automáticas por reglas | Revisar las discrepancias (`revisar_anotacion`) |
| 7 | Validación en una fuente nueva | `python -m src.imagenes.validacion --crear`, anotar, luego `python -m src.imagenes.validacion` | — | `data/metadata/validacion_met_cma_v2.xlsx`, `outputs/reports/validacion_met_cma_v2.md` | **Sí: anotación ciega** |
| 8 | Traslado de la validación | `python -m src.imagenes.validacion --trasladar` | — | Decisiones del revisor en los workbooks | Resolver las contradicciones que quedan en `revisar` |
| 8b | Revisión de decisiones antiguas | `python -m src.imagenes.revision_v2 --crear`, decidir, luego `--trasladar` | — | `data/metadata/revision_criterio_v2_met_cma.xlsx` y las decisiones en los workbooks | **Sí: el revisor decide con la ficha como apoyo** |
| 9 | Regeneración y conteos | `python -m src.flujo` | — | CSV revisados, informes y verificación de `config/corpus.toml` | Actualizar los conteos y documentar el motivo |

Las etapas 2 a 5 están separadas a propósito: las medidas no contienen ningún juicio y se versionan; la calibración traduce los juicios del revisor en pesos; la ficha aplica esos pesos sin red ni imágenes, de modo que un clon limpio regenera todo.

## Medidas (etapa 2)

Sobre la copia de evaluación de 1600 px, el textil se separa del fondo de estudio (estimado en el borde de la fotografía) y se mide:

| Grupo | Medidas | Qué responde |
|---|---|---|
| Fotografía | `nitidez_comun`, `lado_textil_px`, `fraccion_recortada`, `croma_p90` | ¿La foto tiene detalle, resolución y color? |
| Color | `colorido`, `n_tonos`, `colores_distintos`, `separabilidad_cromatica`, `contraste_cromatico` | ¿Hay colores que un observador distingue? |
| Forma del diseño | `bordes_cromaticos`, `densidad_diseno` | ¿Las figuras están dibujadas por cambios de color legibles? |
| Pieza | `compacidad`, `fraccion_lagunas`, `fraccion_mayor`, `n_fragmentos`, `toca_encuadre`, `elongacion`, `encuadre_lleno` | ¿El textil está entero en la foto o roto, cortado, en pedazos? |
| Estructura | `regularidad`, `repeticiones`, `modulo_px`, `simetria_horizontal`, `simetria_vertical` | ¿Hay un módulo que se repite o simetría? (informativo para el modelo combinatorio) |

Dos decisiones de medición que hay que declarar:

- La nitidez depende de la escala de la copia (reducir una imagen a la mitad la multiplica por 1,2–1,55). La que se compara entre museos, `nitidez_comun`, se mide con el textil llevado a 600 px de lado mayor.
- En una toma cerrada (el textil llena el encuadre) no se ve el contorno: las medidas de contorno no cuentan para la completitud.

## Atributos, puntaje y bandas (etapas 4 y 5)

El motivo libre del revisor se traduce en atributos (`src/imagenes/motivos.py`): completitud, colores visibles, formas visibles, imagen de referencia y motivos de pertinencia. Con esos atributos como etiquetas se ajusta una regresión logística por atributo y un puntaje ordinal (referencia > principal > secundario > descarte por imagen), ambos con validación cruzada. Pesos, umbrales y parámetros quedan en `config/aptitud.toml` (comentados) y en `config/aptitud_modelo.json`.

Antes del puntaje se aplican las **puertas**, reglas verificables que deciden sin modelo:

| Puerta | Banda | Fundamento |
|---|---|---|
| Plumaria (material o título «Feathered»), muñecos, fecha de inicio posterior a 1532 | descartar | Motivos del revisor; la fecha se interpreta desde el texto de cada fuente (`src/utils/fechas.py`) |
| Sin imagen o textil de menos de 300 px | descartar | No hay atributos que identificar |
| Fotografía monocroma | secundario | El color no es identificable |

Después, el puntaje sugiere principal, revisar o descartar; la imagen de referencia se sugiere sobre el umbral de referencia. Las reglas nunca suavizan una decisión ya tomada.

## Resultados vigentes

- Calibración AIC (fuera de pliegue): `outputs/reports/aptitud_calibracion_aic_v2.md`.
- Resumen por fuente, atributos y cultura: `outputs/reports/aptitud_imagenes_v2_resumen.md`.
- Validación ciega en MET y CMA: `outputs/reports/validacion_met_cma_v2.md`. El kappa (0,56) no alcanzó el criterio de 0,6, por lo que en MET y CMA solo se aplicaron las reglas y las decisiones del revisor.

## Revisión de decisiones tomadas con criterios anteriores

En MET y CMA, parte de las decisiones son anteriores al criterio v2: el secundario por tipo de objeto (prendas tridimensionales, fajas, sombreros) y los descartes por «fragmento no legible» o «baja calidad». `src/imagenes/revision_v2.py` los reúne en un solo workbook con la ficha de cada imagen y, al terminar, traslada las decisiones a los workbooks de cada fuente. Se registran también las confirmaciones con motivo nuevo, porque son etiquetas para recalibrar el modelo en MET y CMA.

## Incorporar una fuente nueva

1. Colector propio con su lista de candidatos (`docs/fuentes.md`) y workbook de revisión (`src/preprocessing/create_*_review_workbook_v2.py`).
2. Agregar la fuente a `src/imagenes/descargar_evaluacion.py` y a `metadatos_pertinencia` en `src/imagenes/aptitud.py` (título, material y fecha).
3. Descargar, medir y puntuar (etapas 1, 2 y 5); aplicar `aptitud_workbooks --solo-reglas`.
4. Validar con una muestra ciega (etapa 7). Si kappa ≥ 0,6, llevar la ficha completa al workbook como apoyo a la revisión; si no, revisar con el criterio sin sugerencias del modelo.
5. Registrar los conteos en `config/corpus.toml` con un comentario que explique cada cambio.

## Cómo escribir el motivo

El analizador reconoce frases cortas y tolera errores de escritura. Conviene empezar por la completitud y luego colores y formas, con «con» o «sin»:

- «Textil completo con colores y formas visibles» → principal; imagen de referencia.
- «Textil incompleto con colores y formas visibles» → principal.
- «Textil incompleto con colores visibles y no formas» o «… poco visibles» → secundario.
- «Textil sin colores ni formas visibles» → descarte.
- Pertinencia: «Textil con plumas», «Son muñecos», «Posterior a la época inca», «No es textil andino».

Si la decisión contradice su propio motivo (por ejemplo, «descartado» con «colores y formas visibles»), el traslado de la validación la deja en `revisar` en vez de elegir.
