# Documentación del proyecto

Documentación metodológica del corpus multimodal de textiles andinos. Según la §6.6.5 de la tesis, forma parte del corpus: define sus condiciones de uso, interpretación, revisión y reproducibilidad.

## Revisión del asesor (noviembre de 2026)

| Documento | Contenido |
|---|---|
| `revision_asesor_2026-11/` | Carta de envío, informe de avance y matriz de respuesta a la auditoría. Es el punto de entrada de la revisión. |
| `auditoria_2026-10-20/` | Auditoría del asesor del 20 de octubre de 2026, versionada sin cambios, con una nota sobre la verificación de sus sumas. |

## Corpus v2 y experimento (etiqueta `corpus-met-cma-aic-v2.0`)

| Documento | Contenido |
|---|---|
| `protocolo_experimental_v2.md` | Protocolo del experimento de recuperación estructural, propuesto para la aprobación del asesor. |
| `especificacion_m3.md` | Descriptor estructural M3: definiciones, propiedades y pruebas. |
| `protocolo_anotacion_v2.md` | Anotación estructural v2: capas, bandas, estados, núcleo y acuerdo intra-anotador. |
| `esquema_consolidado_met_cma_aic_v2.md` | Esquema del consolidado v2, campo por campo (generado por el flujo). |
| `protocolo_aptitud_v2.md` | Criterio de selección v2, etapas con sus comandos, medidas de imagen, puntaje, validación y cómo incorporar una fuente nueva. |
| `fuentes.md` | Fuentes incluidas (MET, CMA, AIC), particularidades de cada API y fuentes descartadas. |
| `met_protocolo_fuente_v2.md` | Protocolo y cadena de curación MET. |
| `cma/cma_source_protocol.md` | Protocolo y cadena de curación CMA. |
| `corpus/taxonomia_atributos_v2.md` | Vocabulario controlado vigente (códigos, etiquetas y extensiones), generado desde `config/vocabulario.toml`. |

Los conteos vigentes y el motivo de cada cambio están en `config/corpus.toml`.

## Corpus consolidado MET+CMA v1 (`corpus/`, congelado)

| Documento | Contenido |
|---|---|
| `corpus/ficha_dataset_met_cma_v1.md` | Ficha del dataset: contenido, conteos, archivos, licencias y limitaciones. |
| `corpus/protocolo_curacion_met_cma_v1.md` | Criterios de inclusión, complementario y exclusión de la v1. |
| `corpus/taxonomia_atributos_met_cma_v1.md` | Vocabulario controlado de la v1, generado desde su copia congelada `data/metadata/v1_congelado/vocabulario.toml`. |
| `corpus/guia_anotacion_met_cma_v1.md` | Flujo y criterios de la anotación manual. |
| `corpus/trazabilidad_met_cma_v1.md` | Cadena de cada registro, versiones, sumas de verificación y cambios curatoriales. |
| `corpus/uso_etico_met_cma_v1.md` | Principios de uso responsable. |
| `esquema_consolidado_met_cma_v1.md` | Esquema campo por campo (generado por el flujo). |

## Tesis e historia del repositorio

| Documento | Contenido |
|---|---|
| `MCC701_05-07-2026.pdf` | Primer avance de tesis. |
| `notas_para_tesis.md` | Diferencias con el capítulo 6 y material para la segunda parte. |
| `plan_cierre_tesis.md` | Plan de cuatro semanas (26-10 al 22-11-2026) alineado con la auditoría del asesor. |
| `historico.md` | Archivos retirados del repositorio y dónde recuperarlos. |
