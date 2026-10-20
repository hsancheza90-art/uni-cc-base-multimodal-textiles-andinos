# Informe final del Corpus MET de Textiles Andinos v1.0

## Resumen

Este informe resume la consolidacion del Corpus MET de Textiles Andinos v1.0, construido a partir de registros oficiales de The Metropolitan Museum of Art.

## Archivos consolidados

| Archivo | Registros | Funcion |
|---|---:|---|
| `data/processed/corpus_met_textiles_andinos_v1_inventario_base.csv` | 295 | Inventario base normalizado |
| `data/processed/corpus_met_textiles_andinos_v1_principal.csv` | 132 | Corpus principal para analisis multimodal |
| `data/processed/corpus_met_textiles_andinos_v1_complementario.csv` | 50 | Corpus complementario para contraste o ampliacion |
| `data/processed/corpus_met_textiles_andinos_v1_exclusiones_curatoriales.csv` | 29 | Registros excluidos con motivo documentado |
| `data/processed/corpus_met_textiles_andinos_v1_duplicados.csv` | 0 | Control de duplicados |

## Validaciones principales

- No se identificaron duplicados por `id_objeto` en el inventario base, corpus principal ni corpus complementario.
- El corpus principal conserva enlaces oficiales de objeto e imagen.
- La version v1.0 separa inventario base, corpus principal, corpus complementario y exclusiones curatoriales.
- Los archivos intermedios se conservaron en `data/interim/` y `outputs/archive/` para auditoria interna.

## Alcance

La version v1.0 considera exclusivamente registros de The Metropolitan Museum of Art. Otras fuentes museograficas quedan documentadas como fuentes futuras.

## Nota metodologica

El corpus fue organizado para investigacion en ciencias computacionales. Las decisiones de curacion deben entenderse como criterios academicos de seleccion y trazabilidad, no como clasificaciones culturales definitivas.
