# UNI-CC Andean Textiles Multimodal Dataset

Repositorio académico para la construcción de una base multimodal trazable de textiles andinos a partir de colecciones oficiales digitalizadas.

## Objetivo general

Construir una base de datos multimodal de textiles andinos que integre imágenes, descripciones curatoriales y metadatos culturales provenientes de fuentes oficiales, con el fin de apoyar investigaciones en ciencias computacionales, inteligencia artificial generativa y aprendizaje multimodal.

## Contexto académico

Este repositorio forma parte del trabajo de investigación de tesis en la Maestría en Ciencias Computacionales de la Universidad Nacional de Ingeniería.

El proyecto busca estudiar textiles andinos como objetos materiales de información, considerando dimensiones visuales, técnicas, culturales y descriptivas.

## Fuentes iniciales consideradas

- The Metropolitan Museum of Art
- Cleveland Museum of Art
- Smithsonian Open Access
- Harvard Art Museums
- British Museum
- Otros repositorios museográficos oficiales

## Estructura del repositorio

```text
data/
  raw/              Datos crudos descargados desde APIs o fuentes oficiales
  images/           Imágenes descargadas localmente, no versionadas en Git
  processed/        Bases procesadas para análisis
  metadata/         Información de fuentes, licencias y trazabilidad

notebooks/          Notebooks exploratorios y experimentales

src/
  collectors/       Scripts para recolectar datos desde APIs o sitios oficiales
  preprocessing/    Limpieza y normalización de metadatos
  utils/            Funciones auxiliares

docs/               Documentación académica y técnica

outputs/            Figuras, reportes y muestras generadas