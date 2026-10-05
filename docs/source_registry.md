# Registro de fuentes del corpus

Fuentes institucionales incorporadas al corpus consolidado MET+CMA v1, con su estado, salidas y conteos. El objetivo es mantener separadas las fuentes efectivamente incorporadas de las exploratorias.

## Fuentes incluidas

| Fuente | Institución | Licencia | Estado | Principal | Complementario |
|---|---|---|---|---:|---:|
| MET | The Metropolitan Museum of Art | Dominio público (Open Access) | Curación MET v2 con revisión manual y auditoría | 126 | 55 |
| CMA | Cleveland Museum of Art | CC0 | Curación CMA v2 con revisión manual y auditoría | 88 | 19 |

Corpus consolidado: `data/processed/corpus_textiles_andinos_met_cma_v1_consolidado.csv` (288 registros).

## Criterio de selección de fuentes

Se priorizan MET y CMA porque:

1. Son instituciones museográficas con colecciones públicas y documentadas.
2. Ofrecen metadatos curatoriales que permiten trazabilidad por objeto.
3. Tienen imágenes asociadas a registros textiles con licencias abiertas.
4. Permiten construir un corpus inicial defendible sin depender de fuentes no verificadas.

## Estado de MET

| Conjunto MET | Registros | Archivo |
|---|---:|---|
| Inventario base | 295 | `data/processed/corpus_met_textiles_andinos_v1_inventario_base.csv` |
| Principal revisado | 126 | `data/metadata/met_corpus_principal_v2_revisado.csv` |
| Secundario (complementario) revisado | 55 | `data/metadata/met_corpus_secundario_v2_revisado.csv` |
| Descartados revisados | 30 | `data/metadata/met_descartados_v2_revisado.csv` |
| Pendientes de revisión | 9 | `data/metadata/met_pendientes_revision_v2.csv` |

Protocolo: `docs/met_protocolo_fuente_v2.md`. Revisión manual: `data/metadata/met_revision_manual_v2.xlsx`.

## Estado de CMA

| Conjunto CMA | Registros | Archivo |
|---|---:|---|
| Candidatos normalizados | 146 | `data/metadata/cma_andes_textiles_candidates.csv` |
| Principal revisado | 88 | `data/metadata/cma_corpus_principal_revisado.csv` |
| Secundario (complementario) revisado | 19 | `data/metadata/cma_corpus_secundario_revisado.csv` |
| Descartados revisados | 39 | `data/metadata/cma_descartados_revisado.csv` |

Protocolo: `docs/cma/cma_source_protocol.md`. Revisión manual: `data/metadata/cma_revision_manual_v2.xlsx`.

## Fuentes exploratorias fuera del corpus

Otras fuentes (`docs/data_sources.md`) pueden explorarse, pero no forman parte del corpus mientras no pasen por el mismo nivel de documentación, curación y auditoría aplicado a MET y CMA.
