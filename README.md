# UNI-CC Base Multimodal de Textiles Andinos

Repositorio académico para la construcción de una base multimodal trazable de textiles andinos a partir de colecciones oficiales digitalizadas.

## Objetivo

Construir una base de datos multimodal de textiles andinos que integre imágenes, descripciones curatoriales y metadatos culturales provenientes de fuentes oficiales, con el fin de apoyar investigaciones en ciencias computacionales, aprendizaje multimodal y análisis computacional del patrimonio textil andino.

## Alcance actual

En la etapa inicial del proyecto se ha implementado un primer pipeline de recolección y curaduría sobre la colección digital de The Metropolitan Museum of Art (The Met). Este pipeline:

- recupera objetos candidatos mediante la API oficial,
- normaliza los registros en un esquema académico en español,
- aplica reglas de inclusión y exclusión para identificar textiles,
- separa candidatos generales de un subconjunto curado,
- descarga únicamente imágenes de registros aceptados como textiles.

## Estructura general

- `data/raw/`: datos crudos descargados desde fuentes oficiales.
- `data/processed/`: conjuntos normalizados y curados.
- `outputs/samples/`: muestras visuales descargadas para validación.
- `src/collectors/`: recolectores desde APIs o fuentes oficiales.
- `src/preprocessing/`: reglas de filtrado, normalización y curaduría.
- `notebooks/`: cuadernos de revisión y validación.
- `docs/`: documentación metodológica y académica.

## Estado del proyecto

Fase actual: implementación del pipeline curado en español para The Met y validación inicial del subconjunto textil.