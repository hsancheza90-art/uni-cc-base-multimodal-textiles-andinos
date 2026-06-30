# Protocolo de fuente: Cleveland Museum of Art

## Objetivo

Incorporar una segunda fuente abierta para ampliar el corpus multimodal de textiles andinos con imagenes y metadatos curatoriales trazables.

## Fuente

- Institucion: Cleveland Museum of Art.
- Acceso: Open Access API.
- Endpoint principal: `https://openaccess-api.clevelandart.org/api/artworks/`.
- Tipo de salida: metadatos curatoriales e imagenes cuando estan disponibles.
- Uso en el corpus: generacion de candidatos para revision visual y curacion manual.

## Estrategia de consulta

El colector ejecuta consultas textuales que combinan area cultural andina y materialidad textil:

- `Andes textile`
- `Andean textile`
- `Peru textile`
- `Peruvian textile`
- `Inca textile`
- `Wari textile`
- `Huari textile`
- `Chancay textile`
- `Nazca textile`
- `Nasca textile`
- `Paracas textile`
- `Moche textile`
- `Chimu textile`
- `Tiwanaku textile`
- `South Coast textile`
- `North Coast textile`

Los resultados se deduplican por `source_id`, correspondiente al identificador del registro en la API.

## Criterio automatico inicial

Un registro queda como `candidate` si cumple las tres condiciones:

1. Tiene URL de imagen.
2. Presenta evidencia andina en campos curatoriales.
3. Presenta evidencia textil en campos curatoriales.

Los registros que no cumplen quedan marcados con una razon explicita:

- `excluded_no_image`
- `excluded_no_andean_evidence`
- `excluded_no_textile_evidence`

## Salidas generadas

- `data/raw/cma/cma_andes_textiles_raw.jsonl`: registros crudos deduplicados.
- `data/metadata/cma_andes_textiles_candidates.csv`: tabla normalizada para revision.
- `outputs/reports/cma_collection_summary.md`: conteos de recoleccion y estados de curacion.

## Control de calidad

Antes de fusionar esta fuente con el corpus principal:

1. Revisar visualmente cada registro con `curation_status = candidate`.
2. Confirmar que la pieza sea textil y no solo una representacion de textil.
3. Confirmar evidencia andina o precolombina andina en los metadatos.
4. Separar piezas dudosas, fragmentos no informativos o piezas que no aporten al objetivo visual del corpus.
5. Mantener `source`, `source_id`, `url`, `image_url` y `share_license_status` para trazabilidad.

## Comandos de ejecucion

Prueba controlada:

```bash
python src/collectors/cma_collector.py --root . --query "Andes textile" --limit-per-query 5
python src/metadata/audit_cma_outputs.py --root .