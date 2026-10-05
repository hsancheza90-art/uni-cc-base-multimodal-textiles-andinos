# Base Multimodal de Textiles Andinos

Repositorio académico para la construcción de una base multimodal de textiles andinos orientada a investigación en ciencias de la computación, visión por computadora, recuperación imagen-texto y análisis computacional de patrimonio textil.

## Descripción

Este proyecto organiza, cura y documenta registros textiles andinos procedentes de colecciones museográficas institucionales. El objetivo no es realizar una descarga masiva de imágenes, sino construir un corpus trazable, revisable y metodológicamente defendible.

El corpus integra metadatos curatoriales, enlaces oficiales, enlaces a imágenes institucionales, decisiones de curación, criterios de inclusión y exclusión, y reportes de auditoría técnica.

## Alcance del corpus

La versión consolidada del corpus se concentra en dos fuentes institucionales:

1. The Metropolitan Museum of Art (MET)
2. Cleveland Museum of Art (CMA)

La decisión metodológica fue priorizar fuentes museográficas con trazabilidad institucional, metadatos curatoriales y disponibilidad de imágenes asociadas. Otras fuentes exploratorias se conservan fuera del corpus consolidado hasta pasar por el mismo nivel de curación, documentación y auditoría.

## Estado actual

Ambas fuentes cuentan con un flujo reproducible de curación, revisión manual mediante un workbook maestro y auditoría técnica.

| Fuente | Nivel | Principal | Secundario | Descartados | Pendientes |
|---|---|---:|---:|---:|---:|
| MET v2 | Base auditada | 132 | 50 | 29 | 0 |
| MET v2 | Revisión manual | 127 | 54 | 30 | 0 |
| CMA v2 | Revisión manual (146 candidatos) | 88 | 19 | 39 | 0 |

En CMA, 138 registros se revisaron manualmente y 8 se descartaron automáticamente por estar fuera del alcance andino o corresponder a herramientas textiles.

## Salidas recomendadas para el corpus

| Conjunto | Archivo |
|---|---|
| MET principal revisado | `data/metadata/met_corpus_principal_v2_revisado.csv` |
| MET secundario revisado | `data/metadata/met_corpus_secundario_v2_revisado.csv` |
| MET descartados revisados | `data/metadata/met_descartados_v2_revisado.csv` |
| CMA principal revisado | `data/metadata/cma_corpus_principal_revisado.csv` |
| CMA secundario revisado | `data/metadata/cma_corpus_secundario_revisado.csv` |
| CMA descartados revisados | `data/metadata/cma_descartados_revisado.csv` |

Las salidas base se conservan como respaldo auditado y como punto de comparación frente a la revisión manual.

## Flujo reproducible MET v2

```bash
# 1. Construir salidas curatoriales base desde el corpus MET v1
python src/metadata/build_met_corpus_v2.py --root .

# 2. Auditar salidas base
python src/metadata/audit_met_outputs_v2.py --root .

# 3. Crear el workbook de revisión manual (data/metadata/met_revision_manual_v2.xlsx)
python src/preprocessing/create_met_review_workbook_v2.py --root .

# 4. Aplicar las decisiones registradas en el workbook
python src/metadata/apply_met_review_v2.py --root .

# 5. Generar galerías HTML revisadas
python src/review/build_met_gallery_v2.py --root . --revisado
```

## Flujo reproducible CMA v2

```bash
# 1. Crear o actualizar el workbook maestro (data/metadata/cma_revision_manual_v2.xlsx)
python src/preprocessing/create_cma_review_workbook_v2.py --root .

# 2. Aplicar la revisión manual y regenerar los CSV revisados
python src/metadata/apply_cma_review_v2.py --root .

# 3. Auditar salidas CMA
python src/metadata/audit_cma_outputs.py --root .
```

En ambos workbooks la columna de decisión final permite mover registros entre `principal`, `secundario`, `descartados` y `revisar`.

## Criterios de curación

- **Principal:** piezas textiles andinas con utilidad visual clara para el corpus.
- **Secundario:** piezas útiles, pero con menor prioridad visual, composicional o metodológica.
- **Descartados:** piezas fuera del alcance, no andinas, no textiles, duplicadas, de baja calidad visual o herramientas textiles.
- **Revisar:** casos pendientes de decisión.

Cada registro debe conservar:

1. Fuente institucional.
2. Identificador del objeto.
3. URL oficial.
4. URL de imagen o ruta local.
5. Estado de curación.
6. Motivo de inclusión, separación secundaria o descarte.

## Estructura del repositorio

| Carpeta | Uso |
|---|---|
| `data/raw/` | Respuestas originales de las fuentes; la generan los colectores y no se versiona |
| `data/processed/` | Corpus MET v1 (entrada del flujo MET v2) |
| `data/metadata/` | Salidas normalizadas, workbooks de revisión y corpus curado MET v2 y CMA v2 |
| `docs/` | Documentación académica, metodológica y ética |
| `outputs/reports/` | Reportes de curación, auditoría y validación |
| `outputs/review/` | Galerías HTML de revisión visual |
| `src/collectors/` | Recolección de datos por fuente |
| `src/metadata/` | Construcción, auditoría y aplicación de revisiones |
| `src/preprocessing/` | Workbooks de revisión, filtros y preparación de datos |
| `src/review/` | Generación de galerías visuales |
| `src/archive/` | Scripts preliminares de MET v1, conservados por trazabilidad |

## Documentación principal

| Documento | Propósito |
|---|---|
| `docs/source_registry.md` | Registro de fuentes incluidas y exploratorias |
| `docs/met_protocolo_fuente_v2.md` | Protocolo metodológico de la fuente MET v2 |
| `docs/cma/cma_source_protocol.md` | Protocolo metodológico de la fuente CMA |
| `docs/data_sources.md` | Registro general de fuentes consideradas |
| `docs/met_v1/` | Documentación histórica del corpus MET v1 (ficha, protocolo, trazabilidad, uso ético, taxonomía y guía de anotación) |
| `docs/MCC701_05-07-2026.pdf` | Primer avance de tesis |

## Instalación

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

## Uso previsto

Este corpus está destinado a investigación académica en ciencias de la computación, especialmente en:

- Visión por computadora aplicada a patrimonio textil.
- Recuperación multimodal imagen-texto.
- Clasificación exploratoria de objetos textiles.
- Organización computacional de colecciones museográficas.
- Desarrollo de descriptores visuales, composicionales e iconográficos.

## Uso no previsto

No se recomienda usar este corpus para:

- Comercialización directa de motivos patrimoniales.
- Apropiación o reproducción no contextualizada de diseños textiles.
- Clasificación cultural automática sin revisión humana.
- Interpretaciones históricas o rituales concluyentes sin validación experta.
- Sustitución de investigación etnográfica, arqueológica o curatorial especializada.

## Versiones anteriores

- `v1.0-corpus-met-textiles-andinos`: corpus MET v1 con notebooks, archivos intermedios de anotación y muestras de imágenes.
- `archivo/cma-v1`: primera curación CMA, reemplazada por el flujo reproducible CMA v2.

## Contexto académico

Este repositorio forma parte de una investigación de tesis en la Maestría en Ciencias de la Computación de la Universidad Nacional de Ingeniería, orientada al estudio computacional de textiles andinos como objetos materiales, visuales, culturales y multimodales.
