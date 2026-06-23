# Validacion tecnica del Corpus MET de Textiles Andinos v1.0

Fecha de validacion: 2026-06-23

Este reporte resume controles tecnicos aplicados a los archivos finales del corpus: conteo de filas y columnas, duplicados por identificador institucional, campos criticos vacios y consistencia de cabeceras.

## Resumen por archivo

| Archivo | Filas | Columnas | ID vacios | ID duplicados | URL objeto vacias | URL imagen vacias | Licencia vacia | Columnas antiguas |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| data/processed/corpus_met_textiles_andinos_v1_inventario_base.csv | 295 | 33 | 0 | 0 | 0 | 5 |  | [] |
| data/processed/corpus_met_textiles_andinos_v1_principal.csv | 132 | 53 | 0 | 0 | 0 | 0 | 0 | [] |
| data/processed/corpus_met_textiles_andinos_v1_complementario.csv | 50 | 54 | 0 | 0 | 0 | 0 | 0 | [] |
| data/processed/corpus_met_textiles_andinos_v1_exclusiones_curatoriales.csv | 29 | 19 | 0 | 0 | 0 | 0 |  | [] |
| data/processed/corpus_met_textiles_andinos_v1_duplicados.csv | 0 | 41 | 0 | 0 | 0 | 0 | 0 | [] |

## Observaciones

- No se identifican duplicados por id_objeto en los archivos finales con registros.
- El corpus principal y el corpus complementario tienen enlaces oficiales, enlaces de imagen y licencia completos.
- El inventario base conserva 5 registros sin url_imagen; se mantienen como parte del inventario normalizado porque pueden corresponder a objetos sin imagen institucional disponible en la metadata consultada.
- El archivo de duplicados conserva solo cabeceras porque no se identificaron duplicados por identificador institucional en esta version.

## Resultado

La version v1.0 queda tecnicamente consistente para entrega academica, con trazabilidad por identificador institucional y enlaces oficiales del MET.
