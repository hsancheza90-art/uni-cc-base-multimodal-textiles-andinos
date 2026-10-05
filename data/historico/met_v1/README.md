# Auditoría manual MET v1

Decisiones humanas que explican cómo el corpus MET v1 pasó de 35 a 132 registros principales.

| Archivo | Contenido |
|---|---|
| `auditoria_aceptados_no_piloto_validada.csv` | 161 registros aceptados por el filtro que no estaban en el corpus piloto, con la decisión de auditoría manual |
| `auditoria_aceptados_no_piloto_validada.xlsx` | Workbook original en el que se registraron esas decisiones |

## Decisiones

| `decision_auditoria` | Registros | Destino en `data/processed/` |
|---|---:|---|
| `pasar_a_corpus_principal` | 97 | `corpus_met_textiles_andinos_v1_principal.csv` (`origen_curacion = auditoria_aceptados_no_piloto`) |
| `pasar_a_corpus_secundario` | 35 | `corpus_met_textiles_andinos_v1_complementario.csv` |
| `descartar` | 29 | `corpus_met_textiles_andinos_v1_exclusiones_curatoriales.csv` |

El corpus principal v1 suma esas 97 filas a los 35 registros del corpus piloto (97 + 35 = 132).

## Procedencia

Los archivos se generaron en `outputs/archive/review/` con el notebook `04_auditoria_filtros_corpus_met.ipynb` y se retiraron del repositorio en el commit `17b8e35`. Se recuperaron sin cambios desde su padre (`git show 17b8e35^:outputs/archive/review/<archivo>`); los hashes de blob coinciden con el historial.

Son registro histórico: el flujo actual (`python -m src.flujo`) parte de `data/processed/` y no los lee.
