# Fuentes de datos consideradas

Registro general de las fuentes museográficas evaluadas para el corpus. Las fuentes incluidas, con su estado y conteos, están en `docs/source_registry.md` y en `data/processed/corpus_textiles_andinos_met_cma_v1_fuentes_licencias.csv`.

## Fuentes incluidas

### The Metropolitan Museum of Art (MET)

Primera fuente del corpus: API pública, metadatos estructurados e imágenes de objetos en dominio público (política Open Access).

Campos que se recuperan de la API: identificador (`objectID`), título, cultura, periodo, fecha, material (`medium`), dimensiones, clasificación, departamento, URL del objeto, imagen principal y miniatura, indicador de dominio público y etiquetas.

### Cleveland Museum of Art (CMA)

Segunda fuente del corpus: API Open Access con metadatos estructurados e imágenes con licencia CC0.

Campos que se recuperan: identificador, número de acceso, título, cultura, fecha de creación, tipo, técnica, material, departamento, descripción, URL, imagen y estado de licencia.

## Fuentes evaluadas, no incluidas

| Fuente | Observación |
|---|---|
| Smithsonian Open Access | Relevante por volumen y acceso abierto; pendiente de evaluación. |
| Harvard Art Museums | API con posibles imágenes IIIF; requiere revisar condiciones de uso. |
| British Museum | Alto valor académico; licencias y reutilización deben revisarse caso por caso. |
| Art Institute of Chicago (AIC) | Se exploró en otra máquina; ese trabajo no se conserva en el repositorio. |

## Criterios de candidatura

Un registro recuperado pasa a ser **candidato** para la revisión cuando tiene imagen oficial y metadatos mínimos de trazabilidad, y además presenta al menos una de estas evidencias:

- Está clasificado como textil o su material es una fibra textil.
- Contiene términos textiles como *textile*, *woven*, *tunic*, *mantle*, *fragment*, *cloth*, *tapestry* o *embroidery*.
- Está asociado a los Andes o a culturas andinas (Perú, Inca, Paracas, Nasca, Wari, Chancay, Moche, Tiwanaku u otras).

Ser candidato no implica entrar al corpus: la inclusión exige cumplir la mayoría de los criterios del protocolo (`docs/corpus/protocolo_curacion_met_cma_v1.md`).
