# Resumen del corpus piloto The Met

## Estado general

- Total de registros evaluados: 295
- Registros aceptados: 211
- Registros rechazados: 84
- Tasa de aceptación: 71.53%

## Archivos producidos

- `data/processed/met_textiles_pilot_clean.csv`
- `data/processed/met_textiles_rejected.csv`
- `data/metadata/corpus_piloto.csv`
- `docs/taxonomia_atributos.md`

## Clasificaciones más frecuentes en aceptados

| clasificacion_original | conteo |
|---|---:|
| Textiles-Woven | 142 |
| Textiles-Costumes | 32 |
| Textiles-Featherwork | 16 |
| Textiles | 11 |
| Textiles-Non-Woven | 5 |
| Feathers-Costumes | 2 |
| Textiles-Implements | 1 |
| Feathers-Containers | 1 |
| Textiles-Velvets | 1 |

## Culturas más frecuentes en aceptados

| cultura | conteo |
|---|---:|
| Nasca | 43 |
| Paracas | 39 |
| Wari | 37 |
| Peruvian | 29 |
| Inca | 24 |
| Chancay | 14 |
| Chimú | 6 |
| Nasca (?) | 5 |
| Tiwanaku | 2 |
| Moche | 2 |

## Ejemplos de motivos de rechazo

| motivo_filtrado | conteo |
|---|---:|
| título contiene términos textiles: ['textile'] / evidencia cultural/geográfica andina: ['peru', 'nasca'] / clasificación sugiere objeto no textil: ['metal', 'ornaments'] / material sugiere objeto no textil: ['gold'] / título sugiere objeto no textil: ['ornament'] / nombre de objeto sugiere objeto no textil: ['ornament'] | 9 |
| clasificación contiene evidencia textil: ['textile', 'textiles'] / evidencia cultural/geográfica andina: ['peru', 'peruvian'] / material sugiere objeto no textil: ['wood'] / título sugiere objeto no textil: ['pin'] / nombre de objeto sugiere objeto no textil: ['pin'] | 7 |
| clasificación contiene evidencia textil: ['textile', 'textiles'] / evidencia cultural/geográfica andina: ['peru', 'peruvian'] / material sugiere objeto no textil: ['wood'] | 6 |
| clasificación contiene evidencia textil: ['textile', 'textiles'] / evidencia cultural/geográfica andina: ['peru', 'nasca'] / material sugiere objeto no textil: ['ceramic'] / título sugiere objeto no textil: ['pin'] / nombre de objeto sugiere objeto no textil: ['pin'] | 6 |
| clasificación contiene evidencia textil: ['textile', 'textiles'] / material contiene fibras o soporte textil: ['camelid'] / título contiene términos débiles asociados a fragmentos o paneles: ['fragment', 'border'] / evidencia cultural/geográfica andina: ['peru', 'nasca'] / clasificación sugiere objeto no textil: ['sculpture'] / título sugiere objeto no textil: ['figure'] / nombre de objeto sugiere objeto no textil: ['figure'] | 6 |
| evidencia cultural/geográfica andina: ['peru', 'wari'] / clasificación sugiere objeto no textil: ['ceramics', 'ceramic'] / material sugiere objeto no textil: ['ceramic'] / título sugiere objeto no textil: ['bottle'] / nombre de objeto sugiere objeto no textil: ['bottle'] | 3 |
| evidencia cultural/geográfica andina: ['peru', 'inca'] / material sugiere objeto no textil: ['wood'] / título sugiere objeto no textil: ['beaker', 'kero'] / nombre de objeto sugiere objeto no textil: ['kero'] | 2 |
| clasificación contiene evidencia textil: ['textile', 'textiles'] / material sugiere objeto no textil: ['silver'] | 2 |
| evidencia cultural/geográfica andina: ['peru', 'inca'] / clasificación sugiere objeto no textil: ['sculpture'] / material sugiere objeto no textil: ['wood'] | 2 |
| evidencia cultural/geográfica andina: ['peru', 'inca'] / clasificación sugiere objeto no textil: ['metal', 'sculpture'] / material sugiere objeto no textil: ['gold', 'silver', 'alloy'] / nombre de objeto sugiere objeto no textil: ['figure'] | 2 |

## Nota metodológica

Este reporte resume la fase de estandarización del corpus piloto The Met. Los archivos previos `met_candidatos_normalizados.csv` y `met_textiles_curado.csv` se conservan como insumos, mientras que los archivos `met_textiles_pilot_clean.csv` y `met_textiles_rejected.csv` se utilizan como salidas formales para la fase de filtrado.