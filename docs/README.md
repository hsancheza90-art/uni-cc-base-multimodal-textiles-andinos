# Documentación del proyecto

Documentación metodológica del corpus multimodal de textiles andinos. Según la §6.6.5 de la tesis, forma parte del corpus: define sus condiciones de uso, interpretación, revisión y reproducibilidad.

## Corpus v2 (en curso)

| Documento | Contenido |
|---|---|
| `protocolo_aptitud_v2.md` | Criterio de selección v2, etapas con sus comandos, medidas de imagen, puntaje, validación y cómo incorporar una fuente nueva. |
| `fuentes.md` | Fuentes incluidas (MET, CMA, AIC), particularidades de cada API y fuentes descartadas. |
| `met_protocolo_fuente_v2.md` | Protocolo y cadena de curación MET. |
| `cma/cma_source_protocol.md` | Protocolo y cadena de curación CMA. |

Los conteos vigentes y el motivo de cada cambio están en `config/corpus.toml`.

## Corpus consolidado MET+CMA v1 (`corpus/`, congelado)

| Documento | Contenido |
|---|---|
| `corpus/ficha_dataset_met_cma_v1.md` | Ficha del dataset: contenido, conteos, archivos, licencias y limitaciones. |
| `corpus/protocolo_curacion_met_cma_v1.md` | Criterios de inclusión, complementario y exclusión de la v1. |
| `corpus/taxonomia_atributos_met_cma_v1.md` | Vocabulario controlado (códigos y etiquetas), generado desde `config/vocabulario.toml`. |
| `corpus/guia_anotacion_met_cma_v1.md` | Flujo y criterios de la anotación manual. |
| `corpus/trazabilidad_met_cma_v1.md` | Cadena de cada registro, versiones, sumas de verificación y cambios curatoriales. |
| `corpus/uso_etico_met_cma_v1.md` | Principios de uso responsable. |
| `esquema_consolidado_met_cma_v1.md` | Esquema campo por campo (generado por el flujo). |

## Tesis e historia del repositorio

| Documento | Contenido |
|---|---|
| `MCC701_05-07-2026.pdf` | Primer avance de tesis. |
| `notas_para_tesis.md` | Diferencias con el capítulo 6 y material para la segunda parte. |
| `historico.md` | Archivos retirados del repositorio y dónde recuperarlos. |
