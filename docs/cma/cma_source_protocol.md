# Protocolo de fuente: Cleveland Museum of Art (CMA)

## Objetivo

Incorporar una segunda fuente abierta para ampliar el corpus multimodal de textiles andinos con imágenes y metadatos curatoriales trazables.

## Fuente

- Institución: Cleveland Museum of Art.
- Acceso: Open Access API, `https://openaccess-api.clevelandart.org/api/artworks/`.
- Licencia de imagen: CC0 (campo `share_license_status`).
- Imagen: el colector registra la versión web; para medir la aptitud se usa la versión de impresión (`_print.jpg`, unos 3400 px).

## Estrategia de consulta

El colector (`src/collectors/cma_collector.py`) combina área cultural andina y materialidad textil: `Andes textile`, `Andean textile`, `Peru textile`, `Peruvian textile`, `Inca textile`, `Wari textile`, `Huari textile`, `Chancay textile`, `Nazca textile`, `Nasca textile`, `Paracas textile`, `Moche textile`, `Chimu textile`, `Tiwanaku textile`, `South Coast textile` y `North Coast textile`. Cada consulta se pagina por completo y el colector avisa si una queda truncada. Los resultados se deduplican por `source_id`.

Se probó una estrategia amplia (`type=Textile`): recuperó 2045 registros, casi todos no andinos, y los dos candidatos nuevos que aportaba eran textiles de Indonesia e Italia. Por eso el corpus usa la búsqueda conservadora.

## Criterio automático inicial

Un registro queda como `candidate` si tiene URL de imagen y evidencia andina y textil en sus campos curatoriales. Los demás quedan marcados con su razón (`excluded_no_image`, `excluded_no_andean_evidence`, `excluded_no_textile_evidence`). De los 146 registros normalizados, 138 llegaron a la revisión manual; los 8 restantes se descartaron automáticamente por estar fuera del ámbito andino o ser herramientas textiles.

## Cadena de curación

```text
cma_collector.py
  -> data/metadata/cma_andes_textiles_candidates.csv               146 registros normalizados
  -> curación manual v1 (workbook y scripts en la etiqueta corpus-met-cma-v1.2)
  -> data/metadata/cma_corpus_{principal,secundario}.csv, cma_descartados.csv   88 / 19 / 39, con las decisiones v1
  -> create_cma_review_workbook_v2.py + revisión manual
  -> data/metadata/cma_revision_manual_v2.xlsx                      insumo vigente
  -> apply_cma_review_v2.py (en el flujo)
  -> data/metadata/cma_*_revisado.csv
```

La curación v1 es histórica: sus decisiones (decisión, motivo, observación, calidad visual y notas) quedaron en los tres CSV que sembraron el workbook vigente, por lo que el workbook v1 y sus dos scripts se retiraron (`docs/historico.md`). Los generadores de workbooks no sobrescriben un workbook existente sin `--forzar`.

Desde octubre de 2026, el workbook vigente también recibe las decisiones de las reglas de aptitud (plumaria, periodo, fotografía monocroma) y de la validación ciega, con el criterio de `docs/protocolo_aptitud_v2.md`. Los conteos vigentes y el motivo de cada cambio están en `config/corpus.toml`.

## Control de calidad

1. Confirmar que la pieza sea textil y no una representación de un textil.
2. Confirmar evidencia andina o precolombina andina en los metadatos.
3. Aplicar el criterio de aptitud: colores y figuras identificables a primera vista.
4. Mantener `source`, `source_id`, `url`, `image_url` y `share_license_status` para la trazabilidad.

## Comandos

```bash
# Recolección (requiere red). Escribe en data/raw/cma/; la lista versionada solo se reemplaza a propósito:
python -m src.collectors.cma_collector
python -m src.collectors.cma_collector --salida data/metadata/cma_andes_textiles_candidates.csv --forzar

# Prueba controlada
python -m src.collectors.cma_collector --query "Andes textile" --limit-per-query 5

# Aplicación de la revisión y auditoría (las ejecuta también python -m src.flujo)
python -m src.metadata.apply_cma_review_v2
python -m src.metadata.audit_cma_outputs
```
