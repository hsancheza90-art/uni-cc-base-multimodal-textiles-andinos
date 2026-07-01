# UNI-CC Base Multimodal de Textiles Andinos

Repositorio para construir, curar y documentar una base multimodal de textiles andinos a partir de fuentes museales abiertas.

## Estado actual

El repositorio incluye flujos reproducibles para curación de registros textiles andinos desde fuentes abiertas.

### Cleveland Museum of Art (CMA)

La fuente CMA cuenta con un flujo reproducible de curación y revisión manual.

**Resultados actuales CMA:**

| Conjunto | Registros |
|---|---:|
| Candidatos normalizados | 146 |
| Corpus principal revisado | 88 |
| Corpus secundario revisado | 19 |
| Descartados revisados | 39 |
| Pendientes de revisión | 0 |

El flujo conserva trazabilidad completa:

- 138 registros revisados manualmente.
- 8 descartes automáticos documentados por estar fuera del alcance andino o corresponder a herramientas textiles.
- Auditoría ejecutada sin hallazgos críticos.

## Archivos principales CMA

### Datos

| Archivo | Descripción |
|---|---|
| `data/metadata/cma_andes_textiles_candidates.csv` | Candidatos CMA normalizados. |
| `data/metadata/cma_revision_manual_v2.xlsx` | Workbook maestro para revisión manual y movimiento entre subconjuntos. |
| `data/metadata/cma_corpus_principal_revisado.csv` | Corpus principal CMA revisado. |
| `data/metadata/cma_corpus_secundario_revisado.csv` | Corpus secundario CMA revisado. |
| `data/metadata/cma_descartados_revisado.csv` | Registros descartados CMA revisados. |
| `data/metadata/cma_pendientes_revision_v2.csv` | Registros pendientes de revisión. Actualmente vacío. |

### Scripts

| Script | Uso |
|---|---|
| `src/collectors/cma_collector.py` | Recolección de candidatos desde CMA. |
| `src/preprocessing/create_cma_review_workbook_v2.py` | Genera el workbook maestro de revisión CMA v2. |
| `src/metadata/apply_cma_review_v2.py` | Aplica cambios del workbook y regenera los CSV revisados. |
| `src/metadata/audit_cma_outputs.py` | Audita salidas normalizadas CMA. |
| `src/review/build_cma_review_gallery.py` | Genera galerías HTML de revisión visual. |

### Reportes y galerías

| Archivo | Descripción |
|---|---|
| `outputs/reports/cma_resumen_revision_manual_v2.md` | Resumen de revisión manual CMA v2. |
| `outputs/reports/cma_curacion_manual_summary.md` | Resumen de curación manual y descartes automáticos. |
| `outputs/review/cma_corpus_principal_revisado_galeria.html` | Galería del corpus principal revisado. |
| `outputs/review/cma_corpus_secundario_revisado_galeria.html` | Galería del corpus secundario revisado. |
| `outputs/review/cma_descartados_revisado_galeria.html` | Galería de descartados revisados. |


## Flujo reproducible CMA

### 1. Crear o actualizar workbook maestro

```bash
python src/preprocessing/create_cma_review_workbook_v2.py --root .
```

Este comando genera:

```text
data/metadata/cma_revision_manual_v2.xlsx
```

En este Excel se puede modificar la columna `corpus_final` para mover registros entre:

```text
principal
secundario
descartados
revisar
```

### 2. Aplicar revisión manual

```bash
python src/metadata/apply_cma_review_v2.py --root .
```

Este comando regenera:

```text
data/metadata/cma_corpus_principal_revisado.csv
data/metadata/cma_corpus_secundario_revisado.csv
data/metadata/cma_descartados_revisado.csv
data/metadata/cma_pendientes_revision_v2.csv
outputs/reports/cma_resumen_revision_manual_v2.md
```

### 3. Auditar salidas CMA

```bash
python src/metadata/audit_cma_outputs.py --root .
```

Resultado esperado actual:

```text
Registros auditados: 146
Sin hallazgos criticos.
```

## Criterios de curación

Los registros se separan en:

- **Principal:** piezas textiles andinas con utilidad visual clara para el corpus.
- **Secundario:** piezas útiles, pero con menor prioridad visual, composicional o metodológica.
- **Descartados:** piezas fuera del alcance, no andinas, no textiles, duplicadas, de baja calidad visual o herramientas textiles.
- **Revisar:** casos pendientes de decisión.

## Estructura del repositorio

```text
data/
  metadata/        Metadatos normalizados, workbook y corpus curado.
  raw/             Datos crudos por fuente.

docs/              Protocolos y documentación metodológica.

outputs/
  reports/         Reportes de curación y auditoría.
  review/          Galerías HTML para revisión visual.

src/
  collectors/      Recolección de datos por fuente.
  metadata/        Auditoría, comparación y aplicación de revisiones.
  preprocessing/   Construcción de workbooks y preparación de datos.
  review/          Generación de galerías visuales.
```

## Nota metodológica

El objetivo del repositorio es mantener un flujo trazable y reproducible: cada decisión de curación debe poder rastrearse desde los candidatos normalizados hasta los subconjuntos finales revisados.
