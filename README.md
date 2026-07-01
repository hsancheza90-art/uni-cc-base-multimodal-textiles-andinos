# Base Multimodal de Textiles Andinos

Repositorio académico para la construcción de una base multimodal de textiles andinos orientada a investigación en ciencias computacionales, visión por computadora, recuperación imagen-texto y análisis computacional de patrimonio textil.

## Descripción

Este proyecto organiza, cura y documenta registros textiles andinos procedentes de colecciones museográficas institucionales. El objetivo no es realizar una descarga masiva de imágenes, sino construir un corpus trazable, revisable y metodológicamente defendible.

El corpus integra metadatos curatoriales, enlaces oficiales, enlaces a imágenes institucionales, decisiones de curación, criterios de inclusión y exclusión, y reportes de auditoría técnica.

## Alcance del Corpus

La versión consolidada del corpus se concentra en dos fuentes institucionales:

1. The Metropolitan Museum of Art (MET)
2. Cleveland Museum of Art (CMA)

La decisión metodológica fue priorizar fuentes museográficas con trazabilidad institucional, metadatos curatoriales y disponibilidad de imágenes asociadas. Otras fuentes exploratorias se conservan fuera del corpus consolidado hasta pasar por el mismo nivel de curación, documentación y auditoría.

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
| `src/preprocessing/create_met_review_workbook_v2.py` | Generador del workbook único de revisión manual |
| `src/metadata/apply_met_review_v2.py` | Aplicador de decisiones manuales registradas en el workbook |
| `src/review/build_met_gallery_v2.py` | Generador de galerías HTML desde CSV base o revisados |
| `data/metadata/met_revision_manual_v2.xlsx` | Workbook maestro de revisión manual |
| `data/metadata/met_corpus_principal_v2_revisado.csv` | Corpus principal luego de revisión manual |
| `data/metadata/met_corpus_secundario_v2_revisado.csv` | Corpus secundario luego de revisión manual |
| `data/metadata/met_descartados_v2_revisado.csv` | Descartados luego de revisión manual |
| `outputs/reports/met_resumen_revision_manual_v2.md` | Resumen de movimientos aplicados desde el workbook |
| `outputs/review/met_corpus_principal_v2_revisado_galeria.html` | Galería HTML del corpus principal revisado |
| `outputs/review/met_corpus_secundario_v2_revisado_galeria.html` | Galería HTML del corpus secundario revisado |
| `outputs/review/met_descartados_v2_revisado_galeria.html` | Galería HTML de descartados revisados |


### Conteos MET v2

La versión MET v2 distingue entre una base auditada y una revisión manual final. La base auditada preserva la reorganización del corpus curado previo; la revisión manual permite mover registros entre principal, secundario y descartados mediante un workbook único.

| Nivel | Principal | Secundario | Descartados | Pendientes |
|---|---:|---:|---:|---:|
| Base auditada | 132 | 50 | 29 | 0 |
| Revisión manual | 127 | 54 | 30 | 0 |

## Estado de CMA

CMA se mantiene como segunda fuente institucional del corpus. Su flujo fue planteado desde el inicio mediante scripts de recolección, normalización y auditoría, manteniendo una estructura más limpia y reproducible.

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

Construir salidas curatoriales MET v2 base:

```bash
python src/metadata/build_met_corpus_v2.py --root .
```

Auditar salidas MET v2 base:

```bash
python src/metadata/audit_met_outputs_v2.py --root .
```

Crear workbook de revisión manual:

```bash
python src/preprocessing/create_met_review_workbook_v2.py --root .
```

Aplicar decisiones manuales:

```bash
python src/metadata/apply_met_review_v2.py --root .
```

Generar galerías HTML revisadas:

```bash
python src/review/build_met_gallery_v2.py --root . --revisado
```

## Salida Recomendada Para el Corpus

Para el corpus se recomienda usar las salidas revisadas de MET v2:

| Conjunto | Archivo |
|---|---|
| Corpus principal MET revisado | `data/metadata/met_corpus_principal_v2_revisado.csv` |
| Corpus secundario MET revisado | `data/metadata/met_corpus_secundario_v2_revisado.csv` |
| Descartados MET revisado | `data/metadata/met_descartados_v2_revisado.csv` |
| Galería principal revisada | `outputs/review/met_corpus_principal_v2_revisado_galeria.html` |
| Galería secundaria revisada | `outputs/review/met_corpus_secundario_v2_revisado_galeria.html` |
| Galería de descartados revisada | `outputs/review/met_descartados_v2_revisado_galeria.html` |

Las salidas base se conservan como respaldo auditado y como punto de comparación frente a la revisión manual.

## Documentación Principal

| Documento | Propósito |
|---|---|
| `docs/source_registry.md` | Registro de fuentes incluidas y exploratorias |
| `docs/met_protocolo_fuente_v2.md` | Protocolo metodológico para MET v2 |
| `docs/cma_source_protocol.md` | Protocolo metodológico para CMA |
| `docs/corpus_met_textiles_andinos_v1_ficha_dataset.md` | Ficha académica del dataset MET previo |
| `docs/corpus_met_textiles_andinos_v1_protocolo_curacion.md` | Criterios curatoriales de la versión MET v1 |
| `docs/corpus_met_textiles_andinos_v1_trazabilidad.md` | Trazabilidad de fuente, archivos y decisiones |
| `docs/corpus_met_textiles_andinos_v1_uso_etico.md` | Principios de uso responsable |

## Uso Previsto

Este corpus está destinado a investigación académica en ciencias computacionales, especialmente en:

- Visión por computadora aplicada a patrimonio textil.
- Recuperación multimodal imagen-texto.
- Clasificación exploratoria de objetos textiles.
- Organización computacional de colecciones museográficas.
- Desarrollo de descriptores visuales, composicionales e iconográficos.

## Uso No Previsto

No se recomienda usar este corpus para:

- Comercialización directa de motivos patrimoniales.
- Apropiación o reproducción no contextualizada de diseños textiles.
- Clasificación cultural automática sin revisión humana.
- Interpretaciones históricas o rituales concluyentes sin validación experta.
- Sustitución de investigación etnográfica, arqueológica o curatorial especializada.

## Criterio Metodológico

El corpus se construye bajo un principio de curación documental y visual. Cada registro debe conservar:

1. Fuente institucional.
2. Identificador del objeto.
3. URL oficial.
4. URL de imagen o ruta local.
5. Estado de curación.
6. Motivo de inclusión, separación secundaria o descarte.

Este enfoque permite sostener que el corpus no es solo una colección de imágenes, sino una base de investigación con trazabilidad, decisiones explícitas y control de calidad.

## Contexto Académico

Este repositorio forma parte de una investigación de tesis en la Maestría en Ciencias Computacionales de la Universidad Nacional de Ingeniería, orientada al estudio computacional de textiles andinos como objetos materiales, visuales, culturales y multimodales.