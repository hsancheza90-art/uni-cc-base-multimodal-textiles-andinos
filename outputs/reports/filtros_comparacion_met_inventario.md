# Comparacion del filtro textil sobre el inventario MET

Aplica `src/preprocessing/textile_filters.py` (coincidencia por palabra completa y sin penalizar clasificaciones o materiales mixtos con evidencia textil) a los registros de `data/processed/corpus_met_textiles_andinos_v1_inventario_base.csv` y lo compara con el `estado_curacion` registrado. No modifica el corpus.

- Registros evaluados: 295
- Registros con decision distinta: 10

## Transiciones

| Estado registrado | Estado con el filtro actual | Registros |
|---|---|---:|
| aceptado_textil | aceptado_textil | 210 |
| excluido_no_textil | aceptado_textil | 8 |
| excluido_no_textil | excluido_no_textil | 70 |
| excluido_no_textil | revision_manual | 1 |
| excluido_sin_imagen | excluido_sin_imagen | 5 |
| revision_manual | aceptado_textil | 1 |

## Registros que cambiarian

| id_objeto | Titulo | Clasificacion | Material | Registrado | Filtro actual | Puntaje | En corpus |
|---|---|---|---|---|---|---:|---|
| 308287 | Tabard | Feathers-Costumes | Cotton, feathers, plant fiber | revision_manual | aceptado_textil | 12 | complementario |
| 315691 | Border Fragment, Figure | Textiles-Sculpture | Camelid hair | excluido_no_textil | aceptado_textil | 11 | no |
| 315692 | Border Fragment, Figure | Textiles-Sculpture | Camelid hair | excluido_no_textil | aceptado_textil | 11 | no |
| 315693 | Border Fragment, Figure | Textiles-Sculpture | Camelid hair | excluido_no_textil | aceptado_textil | 11 | no |
| 315694 | Border Fragment, Figure | Textiles-Sculpture | Camelid hair | excluido_no_textil | aceptado_textil | 11 | no |
| 315695 | Border Fragment, Figure | Textiles-Sculpture | Camelid hair | excluido_no_textil | aceptado_textil | 11 | no |
| 315696 | Border Fragment, Figure | Textiles-Sculpture | Camelid hair | excluido_no_textil | aceptado_textil | 11 | no |
| 315703 | Feathered Crown | Feathers-Costumes | Feathers (Paradise Tanager, Macaw), cotton, skin, cane, copper | excluido_no_textil | revision_manual | 5 | no |
| 316914 | Feathered Ornament | Textiles-Featherwork | Cotton, feathers | excluido_no_textil | aceptado_textil | 10 | no |
| 316938 | Serpent ornament | Textiles-Woven | Cotton, camelid hair | excluido_no_textil | aceptado_textil | 10 | no |
