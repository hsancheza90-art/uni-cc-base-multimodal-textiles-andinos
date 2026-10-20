# Archivos retirados del repositorio

En la limpieza de octubre de 2026 se retiraron de la rama principal los archivos que ya no participan en la cadena de datos: código preliminar reemplazado, exploraciones sin consumidor, documentación duplicada y galerías HTML. **No se perdió nada**: todos siguen en el historial de git y se recuperan con

```bash
git show corpus-met-cma-v1.2:<ruta>          # ver un archivo
git checkout corpus-met-cma-v1.2 -- <ruta>   # restaurarlo en el árbol de trabajo
```

Se conservaron, aunque no los ejecute el flujo, todos los eslabones que producen o explican un insumo: los colectores, los generadores de workbooks, los `cma_corpus_*.csv` que conservan las decisiones de la curación CMA v1 y sembraron el workbook v2, el corpus MET v1 congelado (`data/processed/corpus_met_textiles_andinos_v1_*`), su auditoría y sus informes (`data/historico/met_v1/`; los informes se trasladaron desde `outputs/reports/`).

| Retirado | Motivo | Dónde sigue |
|---|---|---|
| `src/archive/` (8 scripts) | Cadena preliminar de MET v1 y primera anotación; sus insumos ya no existen y la reemplazan `src/metadata/build_met_corpus_v2.py` y `src/anotacion/`. | Etiqueta `corpus-met-cma-v1.2`; el corpus MET v1 que produjeron está en `data/processed/`. La cadena original con notebooks, en `v1.0-corpus-met-textiles-andinos`. |
| `src/collectors/met_collector.py`, `src/preprocessing/spanish_schema.py` | Colector MET v1, reemplazado por `met_collector_v2.py`. | `corpus-met-cma-v1.2` |
| `src/collectors/cma_discovery_probe.py`, `outputs/reports/cma_discovery_probe.csv`, `outputs/reports/cma_strategy_summary_v2.csv` | Exploración de estrategias de consulta CMA. La decisión que produjo (búsqueda conservadora) está en `docs/fuentes.md` y en `cma_collector.py`. | `corpus-met-cma-v1.2` |
| `src/metadata/compare_cma_versions.py` | Comparaba con una consulta CMA expandida que se descartó; su entrada ya no existe. | `corpus-met-cma-v1.2` |
| `src/review/build_cma_review_gallery.py` | Galería de candidatos CMA anterior al workbook v2. | `corpus-met-cma-v1.2` |
| `data/metadata/corpus_met_textiles_andinos_v1_fuentes_licencias.csv` | Registro de fuentes de MET v1, reemplazado por `data/processed/corpus_textiles_andinos_met_cma_v1_fuentes_licencias.csv`. | `corpus-met-cma-v1.2` |
| `docs/met_v1/` (6 documentos) | Documentación de MET v1, reemplazada por `docs/corpus/*_met_cma_v1.md`. | `corpus-met-cma-v1.2` |
| `docs/data_sources.md`, `docs/source_registry.md` | Fusionados en `docs/fuentes.md`; repetían conteos que quedaban desactualizados. | `corpus-met-cma-v1.2` |
| `data/metadata/cma_revision_manual_textiles_andinos.xlsx`, `src/preprocessing/create_cma_review_workbook.py`, `src/preprocessing/export_cma_curated_splits.py` | Curación CMA v1. Sus decisiones quedaron completas en `data/metadata/cma_corpus_{principal,secundario}.csv` y `cma_descartados.csv`, que sembraron el workbook vigente `cma_revision_manual_v2.xlsx`. | `corpus-met-cma-v1.2` |
| `data/historico/met_v1/auditoria_aceptados_no_piloto_validada.xlsx` | Duplicaba celda por celda el `.csv` de la misma carpeta, que se conserva. | `corpus-met-cma-v1.2` |
| `data/processed/corpus_met_textiles_andinos_v1_duplicados.csv` | Control de duplicados de MET v1 con 0 filas; ningún paso lo usa. | `corpus-met-cma-v1.2` |
| `outputs/reports/cma_curacion_manual_summary.md` | Salida del script de curación CMA v1 ya retirado; sus conteos (88/19/39) están en `docs/cma/cma_source_protocol.md`. | `corpus-met-cma-v1.2` |
| `data/metadata/revision_criterio_v2_met_cma.xlsx` | Workbook auxiliar de la revisión v2 de MET y CMA (2026-10-20). Sus 94 decisiones están en los workbooks de cada fuente, con `origen_curacion = revision_criterio_v2` y una observación que cita la fila. | Commit `0d0ebea` |
| `outputs/review/*.html` (galerías) | Ayudas visuales que se regeneran y apuntan a imágenes locales; las decisiones viven en los workbooks. Ya no se versionan (`.gitignore`). | `corpus-met-cma-v1.2`; las de AIC, en el commit `b370aa4`. Se regeneran con `python -m src.review.galerias --fuente met` (también `cma` o `aic`) y `python -m src.imagenes.informe_aptitud` (por banda de aptitud). |
| `data/metadata/cma_corpus_{principal,secundario}_revisado.csv`, `cma_descartados_revisado.csv` (esquema heredado de CMA v1, con BOM) | Reemplazados el 2026-10-20 por `cma_*_v2_revisado.csv`, con el mismo esquema y patrón de nombres que MET y AIC; las decisiones no cambian (siguen en el workbook CMA). Las copias que usa el consolidado v1 siguen en `data/metadata/v1_congelado/`. | Commit `c38996e` |
| `src/review/build_met_gallery_v2.py`, `src/metadata/apply_met_review_v2.FuenteRevision` | Galerías MET y AIC desde los CSV revisados y registro de rutas por fuente. Los reemplazan `src/review/galerias.py` (galerías de las tres fuentes desde los workbooks) y `src/utils/fuentes.py` (registro único de rutas). | Commit `af39a24` |
