```markdown
# Registro de fuentes del corpus

Este documento registra las fuentes usadas o preparadas para construir el corpus multimodal de textiles andinos.

| Fuente | Estado | Acceso | Uso previsto | Salida normalizada |
|---|---|---|---|---|
| The Metropolitan Museum of Art | En curacion previa | API / metadatos abiertos | Base inicial del corpus piloto | `data/metadata/corpus_piloto_clean.csv` |
| Cleveland Museum of Art | Colector implementado | Open Access API | Segunda fuente para ampliar imagenes y metadatos curatoriales | `data/metadata/cma_andes_textiles_candidates.csv` |

## Criterios comunes

1. Mantener trazabilidad por `source` y `source_id`.
2. Preservar URL institucional de la pieza y URL de imagen.
3. Separar datos crudos, metadatos normalizados y reportes.
4. Aplicar revision visual antes de fusionar con el corpus principal.
5. Registrar exclusiones por razon metodologica.
6. Evitar borrar silenciosamente casos dudosos.

## Estado actual

La fuente MET constituye la base inicial del corpus. La fuente CMA queda incorporada como segundo flujo de recoleccion, con salida normalizada y auditoria automatica.

La integracion final entre fuentes debe realizarse despues de revisar visualmente los candidatos CMA.