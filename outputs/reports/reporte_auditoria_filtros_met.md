# Reporte de auditoría de filtros - The Met

## Objetivo

Revisar visualmente los registros aceptados por el filtro textil amplio que no habían pasado al corpus piloto, con el fin de identificar falsos descartes y mejorar la trazabilidad de los motivos de curación.

## Hallazgo principal

El filtro textil amplio funcionó como primera etapa de selección, pero el filtro morfológico hacia el corpus piloto fue demasiado restrictivo.

## Resultados antes/después

| Etapa | Registros |
|---|---:|
| Corpus principal actual | 35 |
| Recuperados para corpus principal | 97 |
| Corpus principal v2 | 132 |
| Corpus secundario actual | 15 |
| Recuperados para corpus secundario | 35 |
| Corpus secundario v2 | 50 |
| Descartados por auditoría | 29 |
| Requieren revisión | 0 |

## Validación de consistencia

| Cruce evaluado | Registros cruzados |
|---|---:|
| Principal / Secundario | 0 |
| Principal / Descartados | 0 |
| Secundario / Descartados | 0 |

## Interpretación metodológica

La auditoría permitió recuperar registros textiles que habían sido excluidos por criterios morfológicos demasiado restrictivos. En particular, se recuperaron fragmentos textiles, mantos, túnicas, paneles, bolsas y piezas con iconografía legible.

El corpus principal queda reservado para piezas con superficie textil visualmente analizable. El corpus secundario conserva textiles relevantes pero con morfología, función o materialidad especial, como prendas tridimensionales, formatos longitudinales, artefactos textiles y featherwork.

## Archivos generados

- `data/metadata/corpus_piloto_clean_v2.csv`
- `data/metadata/corpus_piloto_secondary_v2.csv`
- `data/metadata/corpus_piloto_descartados_auditoria.csv`
- `outputs/review/auditoria_aceptados_no_piloto_validada.csv`
- `outputs/reports/resumen_auditoria_filtros_met.csv`

## Conclusión

La versión v2 mejora la cobertura del corpus The Met y conserva trazabilidad sobre cada decisión de curación. Esta versión debe usarse como base para la siguiente etapa de revisión visual, anotación manual y experimentos multimodales.
