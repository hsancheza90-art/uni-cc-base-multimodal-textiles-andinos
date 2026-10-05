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
