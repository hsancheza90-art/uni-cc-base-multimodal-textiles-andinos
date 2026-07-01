# Base Multimodal de Textiles Andinos

Repositorio académico para la construcción de una base multimodal de textiles andinos orientada a investigación en ciencias computacionales, visión por computadora, recuperación imagen-texto y análisis computacional de patrimonio textil.

## Descripción

Este proyecto organiza, cura y documenta registros textiles andinos procedentes de colecciones museográficas institucionales. El objetivo no es realizar una descarga masiva de imágenes, sino construir un corpus trazable, revisable y metodológicamente defendible.

El corpus integra metadatos curatoriales, enlaces oficiales, enlaces a imágenes institucionales, decisiones de curación, criterios de inclusión y exclusión, y reportes de auditoría técnica.

## Primera Entrega

Para esta primera entrega, el corpus se concentra en dos fuentes institucionales:

1. The Metropolitan Museum of Art (MET)
2. Cleveland Museum of Art (CMA)

La decisión metodológica fue priorizar fuentes museográficas con trazabilidad institucional, metadatos curatoriales y disponibilidad de imágenes asociadas. Otras fuentes exploratorias se conservan fuera del cierre de esta entrega hasta pasar por el mismo nivel de curación, documentación y auditoría.

## Estado de MET

MET cuenta con una versión curada, normalizada y auditada en español. La versión MET v2 reorganiza el trabajo previo sin sobrescribir los archivos históricos.

### Archivos MET v2

| Archivo | Descripción |
|---|---|
| `docs/met_protocolo_fuente_v2.md` | Protocolo metodológico de fuente MET |
| `src/metadata/build_met_corpus_v2.py` | Constructor de salidas curatoriales MET v2 |
| `src/metadata/audit_met_outputs_v2.py` | Auditoría técnica de salidas MET v2 |
| `data/metadata/met_corpus_principal_v2.csv` | Corpus principal MET v2 |
| `data/metadata/met_corpus_secundario_v2.csv` | Corpus secundario MET v2 |
| `data/metadata/met_descartados_v2.csv` | Registros descartados con trazabilidad |
| `outputs/reports/met_resumen_curacion_v2.md` | Resumen de curación MET v2 |
| `outputs/reports/met_auditoria_tecnica_v2.md` | Reporte de auditoría técnica MET v2 |

### Conteos Auditados MET v2

| Conjunto | Registros |
|---|---:|
| Corpus principal MET v2 | 132 |
| Corpus secundario MET v2 | 50 |
| Descartados MET v2 | 29 |

## Estado de CMA

CMA se mantiene como segunda fuente institucional de la primera entrega. Su flujo fue planteado desde el inicio mediante scripts de recolección, normalización y auditoría, manteniendo una estructura más limpia y reproducible.

Archivos asociados:

| Archivo | Descripción |
|---|---|
| `src/collectors/cma_collector.py` | Colector de registros desde Cleveland Museum of Art |
| `src/metadata/audit_cma_outputs.py` | Auditoría de salidas CMA |
| `docs/cma_source_protocol.md` | Protocolo de fuente CMA |
| `outputs/reports/cma_collection_summary.md` | Reporte de recolección CMA |

## Estructura del Repositorio

| Carpeta | Uso |
|---|---|
| `data/raw/` | Datos crudos o respuestas originales de fuentes institucionales |
| `data/interim/` | Archivos intermedios conservados para trazabilidad |
| `data/processed/` | Salidas curatoriales previas y corpus procesado |
| `data/metadata/` | Salidas normalizadas, metadatos y corpus listos para revisión |
| `docs/` | Documentación académica, metodológica y ética |
| `outputs/reports/` | Reportes de curación, auditoría y validación |
| `outputs/review/` | Galerías o materiales auxiliares de revisión visual |
| `src/` | Scripts de recolección, normalización, curación y auditoría |

## Reproducibilidad

Construir salidas curatoriales MET v2:

```bash
python src/metadata/build_met_corpus_v2.py --root .