# Registro de fuentes del corpus

Este documento registra las fuentes institucionales usadas para el corpus multimodal de textiles andinos. El objetivo es mantener trazabilidad, claridad metodologica y separacion entre fuentes efectivamente incorporadas y fuentes exploratorias.

## Fuentes incluidas en el Corpus

| Fuente | Institucion | Estado | Uso en el corpus | Salida principal |
|---|---|---|---|---|
| MET | The Metropolitan Museum of Art | Curacion MET v2 construida y auditada | Fuente principal del corpus curado de textiles andinos | `data/metadata/met_corpus_principal_v2.csv` |
| CMA | Cleveland Museum of Art | Recoleccion y revision manual en curso | Segunda fuente institucional para ampliar el corpus con registros abiertos y trazables | `data/metadata/cma_andes_textiles_candidates.csv` |

## Criterio de seleccion de fuentes

Para la versión consolidada del corpus se priorizan MET y CMA por cuatro razones:

1. Son instituciones museograficas con colecciones publicas y documentadas.
2. Ofrecen metadatos curatoriales que permiten trazabilidad por objeto.
3. Presentan imagenes asociadas a registros textiles o potencialmente textiles.
4. Permiten construir un corpus inicial defendible sin depender de fuentes no verificadas.

## Enfoque de trabajo

El corpus no se construye como una descarga automatica de imagenes. Cada fuente requiere:

1. Recoleccion o consolidacion de registros.
2. Normalizacion de campos.
3. Revision de evidencia textil.
4. Revision de evidencia andina.
5. Separacion entre corpus principal, corpus secundario y descartes.
6. Auditoria tecnica de conteos, identificadores y trazabilidad.

## Estado de MET

MET cuenta con una version curada y reorganizada como MET v2.

Salidas principales:

- `data/metadata/met_corpus_principal_v2.csv`
- `data/metadata/met_corpus_secundario_v2.csv`
- `data/metadata/met_descartados_v2.csv`
- `outputs/reports/met_resumen_curacion_v2.md`
- `outputs/reports/met_auditoria_tecnica_v2.md`

Conteos auditados:

| Conjunto MET v2 | Registros |
|---|---:|
| Corpus principal | 132 |
| Corpus secundario | 50 |
| Descartados | 29 |

## Estado de CMA

CMA se mantiene como segunda fuente del corpus. Su flujo es mas limpio desde el inicio porque fue planteado mediante scripts y revision manual, sin depender de notebooks exploratorios.

Salidas asociadas:

- `src/collectors/cma_collector.py`
- `src/metadata/audit_cma_outputs.py`
- `docs/cma_source_protocol.md`
- `outputs/reports/cma_collection_summary.md`

## Fuentes exploratorias fuera del Corpus

Otras fuentes pueden conservarse como trabajo exploratorio, pero no forman parte del corpus mientras no pasen por el mismo nivel de documentacion, curacion y auditoria aplicado a MET y CMA.
