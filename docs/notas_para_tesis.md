# Correcciones pendientes en el capítulo 6 de la tesis

Diferencias entre el avance de tesis (`docs/MCC701_05-07-2026.pdf`, capítulo 6) y el corpus de la entrega `corpus-met-cma-v1.2`. Cada punto indica la sección, lo que dice el avance y el valor actual con su evidencia en el repositorio.

## Conteos (Cuadro 6.9)

| Fila | Avance | Corpus actual | Motivo |
|---|---:|---:|---|
| Corpus principal MET | 132 | 126 | Revisión manual MET v2 y paso de MET:312615 a complementario por imagen no disponible |
| Corpus complementario MET | 50 | 55 | Revisión manual MET v2 |
| Exclusiones finales MET | 29 | 30 | Revisión manual MET v2 |
| Pendientes MET | — | 9 | Registros recuperados por el filtro corregido, en revisión |
| Descartes iniciales CMA | 0 | 8 | El colector CMA excluye automáticamente 5 sin evidencia andina y 3 sin evidencia textil |
| Conjunto evaluado CMA | 146 | 138 | 146 candidatos menos los 8 descartes automáticos |
| Exclusiones finales CMA | 39 | 31 curatoriales + 8 automáticas | Los 39 de `cma_descartados_revisado.csv` incluyen ambas |
| Corpus consolidado | 289 | 288 | El avance sumaba MET base (132 + 50); el consolidado usa MET revisado (126 + 55) |
| Principal consolidado | 220 (implícito: 132 + 88) | 214 | 126 + 88 |
| Complementario consolidado | 69 (implícito: 50 + 19) | 74 | 55 + 19 |

Evidencia: `config/corpus.toml`, `outputs/reports/corpus_textiles_andinos_met_cma_v1_resumen.md`, `outputs/reports/met_resumen_revision_manual_v2.md`.

## Duplicados (§6.3.5 y Cuadro 6.9)

El avance reporta 0 duplicados en ambas fuentes y deja la comparación visual para versiones posteriores. Ya está implementada:

- Por identificador: 0 duplicados, como en el avance.
- Por imagen: 4 grupos de registros que comparten fotografía (3 pares MET y 1 par CMA), detectados por URL, archivo o píxeles idénticos. Se conservan y se marcan en `grupo_imagen_duplicada`.
- Por parecido visual (hash perceptual): 11 pares listados para revisión manual.

Sugerencia: reemplazar «Duplicados MET: 0» por «Duplicados por identificador: 0; registros que comparten imagen: 3 pares» (y 1 par en CMA).

## Archivos (§6.6.1)

Existen con el nombre propuesto: `corpus_textiles_andinos_met_cma_v1_consolidado.csv` y `corpus_textiles_andinos_met_cma_v1_fuentes_licencias.csv` (en `data/processed/`). Los archivos por fuente de CMA (`corpus_cma_textiles_andinos_v1_*.csv`) no se generan: su contenido está en el consolidado (columna `fuente`) y en `data/metadata/cma_*_revisado.csv`. Conviene ajustar la lista del avance o indicar estas rutas.

## Campos (Cuadros 6.1 a 6.8)

- Los nombres de los Cuadros 6.1 y 6.8 se usan tal cual, con dos precisiones: `estado_metadatos` se llama así en la tesis y en el corpus; `observaciones` se divide en `observaciones` (generadas por el flujo) y `observaciones_anotacion` (del anotador).
- Los valores se guardan como códigos sin tildes (`campo_central`, `fibra_de_camelido`); las etiquetas de la tesis están en `config/vocabulario.toml`. Conviene indicarlo al presentar los cuadros.
- El vocabulario agrega valores que aparecen en los registros y no figuran en los cuadros (por ejemplo `seda`, `metal`, `brocado`, `tela_doble`, `borde_textil`, `mascara_textil`). Están marcados como extensión en `docs/corpus/taxonomia_atributos_met_cma_v1.md`.
- Campos agregados para trazabilidad e imagen: `origen_tipo_objeto`, `origen_material_normalizado`, `origen_tecnica_normalizada`, `tecnica_normalizada`, `grupo_imagen_duplicada`, `imagen_sha256`, `imagen_dhash` y otros. Ver `docs/esquema_consolidado_met_cma_v1.md`.

## Versionamiento (§6.6.2)

El avance recomienda asociar cada entrega a una etiqueta y registrar sumas de verificación. Ya se hace: etiquetas `corpus-met-cma-v1.N` y `data/processed/corpus_textiles_andinos_met_cma_v1_sha256.txt`. Se puede citar la etiqueta de la entrega usada en los experimentos.

## Datos del programa

El README del repositorio decía «Maestría en Ciencias Computacionales»; se unificó con el avance: «Maestría en Ciencias de la Computación».

## Criterio de aptitud analítica (segunda parte, §6.3.2)

Para la segunda parte se reemplaza el juicio general de «imagen útil» y «valor computacional» por una ficha de aptitud con atributos observables. Material para redactarla:

- **Criterio (2026-10-19).** Van al corpus principal los textiles cuyos colores y figuras se identifican a primera vista. Si además el textil está completo y se puede verificar en la fotografía, es una **imagen de referencia** (la mejor imagen para el estudio). Un textil incompleto por rotura, corte o desgaste también va al principal si sus colores y formas se identifican. Secundario: la imagen no permite identificar bien colores o formas (por ejemplo, fotografía monocroma o pieza muy deteriorada). Descarte: no sirve para el estudio o no es pertinente. El criterio amplía la base del estudio porque rescata los atributos que necesita el modelo combinatorio aunque la pieza no esté entera. Se fijó en la revisión manual de las 508 imágenes AIC y se aplica igual a MET, CMA y las fuentes futuras.
- **Ficha por imagen.** Calidad fotográfica (nitidez a escala común del textil, resolución, píxeles recortados), colores identificables, formas visibles, completitud e imagen de referencia («la mejor imagen para el estudio»), estimados con regresiones logísticas calibradas con los motivos del revisor; estructura repetitiva o simétrica como dato informativo. Detalle y cifras en `outputs/reports/aptitud_calibracion_v2.md`.
- **Validez en AIC (validación cruzada de 5 pliegues).** AUC de 0,94 (colores), 0,90 (formas), 0,89 (completitud) y 0,91 (principal frente a descarte por imagen). Con la imagen de referencia definida por la completitud (y no solo por la marca «la mejor imagen»), su AUC frente al resto del principal sube de 0,72 a 0,82.
- **Reglas verificables.** Pertinencia por metadatos (plumaria, muñecos, piezas con fecha de inicio posterior a 1532), resolución insuficiente, imagen inexistente y fotografía monocroma (a secundario). Se aplican de forma automática y documentada; nunca suavizan una decisión.
- **Transferencia a MET y CMA (validación ciega, `outputs/reports/validacion_met_cma_v2.md`).** El revisor anotó 40 imágenes sin ver el puntaje ni la decisión v1. Kappa con el modelo: 0,56 (MET 0,44; CMA 0,66), por debajo del criterio acordado de 0,6, y similar al kappa con la v1 (0,60). La banda principal transfiere bien (20 de 22), pero el modelo es más estricto que el revisor en el extremo bajo. Por eso en MET y CMA solo se aplicaron las reglas: 49 cambios (44 MET y 5 CMA), detallados en `config/corpus.toml`.
- **Revisión de MET y CMA con el criterio v2 (2026-10-20).** El revisor decidió los 94 registros que se habían decidido con criterios anteriores (secundario por tipo de objeto, descartes por «fragmento no legible» o «baja calidad»): 54 cambios y 40 confirmaciones. MET pasa a 130/25/65 y CMA a 104/4/38; el corpus v2 queda en 462 principal, 153 secundario y 259 descartados (874 imágenes). Por cultura, el criterio no relega a las que se conservan en fragmentos (principal: Paracas 92 %, Wari 78 %, Chancay 70 %, Nasca 54 %).
- **Calibración conjunta (2026-10-20).** Con esas etiquetas se comprobó que el modelo calibrado solo con AIC no generalizaba a MET (separación útil/resto 0,49, azar) y apenas a CMA (0,73). Calibrado con AIC más las 86 decisiones MET y CMA tomadas con el criterio v2, la separación fuera de pliegue es 0,91 en AIC, 0,76 en MET y 0,83 en CMA. Conviene presentarlo como hallazgo metodológico: la fotografía y los tipos de pieza de cada museo cambian la relación entre medidas y legibilidad, y la calibración debe incluir ejemplos de cada colección. Límite: la muestra de validación ya forma parte del entrenamiento, así que la transferencia a una fuente nueva exige otra muestra ciega.
- **Sesgo de escala corregido.** La nitidez medida sobre la copia de 1600 px dependía de cuánto se había reducido el original (las copias MET y CMA venían de 3400-4000 px, las AIC de 1686 px). Se mide sobre el textil llevado a 600 px de lado; vale la pena mencionarlo como decisión metodológica.
- **Versionamiento.** El consolidado v1 lee copias congeladas de sus entradas (`data/metadata/v1_congelado/`, idénticas a la etiqueta `corpus-met-cma-v1.2`), de modo que los cambios de la v2 no alteran los archivos `_v1_`.
- **Limitaciones para declarar.** Etiquetas de un solo revisor (se medirá el acuerdo entre anotadores en F2-H2), diferencias de fotografía entre museos y sesgo de conservación (se reporta la distribución por cultura).
