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

### Corpus consolidado MET+CMA v1.0

Une los subconjuntos principal y complementario revisados de ambas fuentes con el esquema armonizado del capítulo 6 de la tesis (Cuadros 6.1 y 6.8): identificador global `FUENTE:id_fuente`, cabeceras comunes en español, estado de licencia por objeto, estados de control e información de imagen.

| Fuente | Principal | Complementario | Total |
|---|---:|---:|---:|
| MET | 127 | 54 | 181 |
| CMA | 88 | 19 | 107 |
| **Total** | **215** | **73** | **288** |

El consolidado usa MET v2 revisado. El avance de tesis reporta 289 porque sumaba MET base (132 + 50); con la revisión manual MET el total es 288.

- 287 imágenes descargadas y verificadas; MET:312615 no tiene imagen disponible en el museo (404).
- 4 grupos de registros que comparten la misma fotografía (`grupo_imagen_duplicada`); se conservan y deben tratarse como un solo ítem en evaluaciones imagen-imagen.
- Detalle de cobertura, estados y posibles duplicados visuales: `outputs/reports/corpus_textiles_andinos_met_cma_v1_resumen.md`.
- Esquema campo por campo: `docs/esquema_consolidado_met_cma_v1.md`.

## Salidas recomendadas para el corpus

| Conjunto | Archivo |
|---|---|
| **Consolidado MET+CMA v1.0** | `data/processed/corpus_textiles_andinos_met_cma_v1_consolidado.csv` |
| Fuentes y licencias | `data/processed/corpus_textiles_andinos_met_cma_v1_fuentes_licencias.csv` |
| Sumas SHA-256 | `data/processed/corpus_textiles_andinos_met_cma_v1_sha256.txt` |
| Manifiesto de imágenes | `data/metadata/imagenes_manifiesto_met_cma_v1.csv` |
| MET principal revisado | `data/metadata/met_corpus_principal_v2_revisado.csv` |
| MET secundario revisado | `data/metadata/met_corpus_secundario_v2_revisado.csv` |
| MET descartados revisados | `data/metadata/met_descartados_v2_revisado.csv` |
| CMA principal revisado | `data/metadata/cma_corpus_principal_revisado.csv` |
| CMA secundario revisado | `data/metadata/cma_corpus_secundario_revisado.csv` |
| CMA descartados revisados | `data/metadata/cma_descartados_revisado.csv` |

Las salidas base se conservan como respaldo auditado y como punto de comparación frente a la revisión manual.

## Instalación

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows (en Linux/macOS: source .venv/bin/activate)
pip install -r requirements-dev.txt
```

`requirements.txt` fija las versiones exactas con las que se verificó el flujo; `pyproject.toml` declara los rangos compatibles (Python 3.11 o superior).

## Regenerar y verificar el corpus

Desde la raíz del repositorio:

```bash
python -m src.flujo
```

El comando ejecuta sin acceso a red los pasos de MET v2 y CMA v2 (construcción, revisión manual y auditoría), construye y valida el consolidado MET+CMA v1.0, y comprueba los conteos esperados de `config/corpus.toml`. Termina con código distinto de cero si algún paso o conteo falla.

### Imágenes

Las imágenes no se versionan. Para descargarlas a `data/images/<fuente>/` (requiere internet, unos 64 MB):

```bash
python -m src.imagenes.descargar_imagenes
```

Para MET se descarga la versión web-large del museo (lado mayor de unos 600 px) y, si no existe, la original; para CMA, la versión web. Las imágenes ya descargadas y verificadas no se vuelven a pedir. El script actualiza `data/metadata/imagenes_manifiesto_met_cma_v1.csv` (URL, SHA-256, dimensiones, dHash y hash de píxeles), que sí se versiona y es insumo del consolidado.

Para verificar que el flujo reproduce exactamente los archivos versionados:

```bash
pytest
```

Las pruebas regeneran el corpus en una carpeta temporal que solo contiene los insumos y comparan cada salida con la versión del repositorio.

Los workbooks de revisión manual (`data/metadata/*_revision_manual_v2.xlsx`) son insumos: contienen decisiones humanas. Sus generadores no los sobrescriben salvo con `--forzar`.

## Flujo reproducible MET v2 (pasos individuales)

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

## Flujo reproducible CMA v2 (pasos individuales)

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
| `config/corpus.toml` | Conteos esperados por fuente y etapa |
| `data/raw/` | Respuestas originales de las fuentes; la generan los colectores y no se versiona |
| `data/processed/` | Corpus MET v1 (entrada del flujo MET v2) y corpus consolidado MET+CMA v1.0 |
| `data/images/` | Copias locales de las imágenes; las genera el descargador y no se versionan |
| `data/metadata/` | Salidas normalizadas, workbooks de revisión y corpus curado MET v2 y CMA v2 |
| `data/historico/met_v1/` | Decisiones de la auditoría manual que formaron el corpus MET v1 (97 + 35 + 29) |
| `docs/` | Documentación académica, metodológica y ética |
| `outputs/reports/` | Reportes de curación, auditoría y validación |
| `outputs/review/` | Galerías HTML de revisión visual |
| `src/collectors/` | Recolección de datos por fuente |
| `src/metadata/` | Construcción, auditoría y aplicación de revisiones |
| `src/preprocessing/` | Workbooks de revisión, filtros y preparación de datos |
| `src/review/` | Generación de galerías visuales |
| `src/consolidado/` | Esquema armonizado y constructor del consolidado MET+CMA |
| `src/imagenes/` | Descarga y verificación de imágenes |
| `src/flujo.py` | Punto de entrada único del flujo reproducible |
| `src/archive/` | Scripts preliminares y de anotación de MET v1, conservados por trazabilidad |
| `tests/` | Pruebas de reproducibilidad |

## Documentación principal

| Documento | Propósito |
|---|---|
| `docs/esquema_consolidado_met_cma_v1.md` | Esquema del corpus consolidado (generado desde el código) |
| `docs/source_registry.md` | Registro de fuentes incluidas y exploratorias |
| `docs/met_protocolo_fuente_v2.md` | Protocolo metodológico de la fuente MET v2 |
| `docs/cma/cma_source_protocol.md` | Protocolo metodológico de la fuente CMA |
| `docs/data_sources.md` | Registro general de fuentes consideradas |
| `docs/met_v1/` | Documentación histórica del corpus MET v1 (ficha, protocolo, trazabilidad, uso ético, taxonomía y guía de anotación) |
| `docs/MCC701_05-07-2026.pdf` | Primer avance de tesis |

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
