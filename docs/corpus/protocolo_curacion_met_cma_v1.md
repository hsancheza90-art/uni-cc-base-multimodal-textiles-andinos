# Protocolo de curación del corpus MET+CMA v1

## Objetivo

Definir cómo se seleccionan, separan, normalizan y documentan los registros del corpus, de modo que cada decisión pueda rastrearse desde la fuente oficial hasta el archivo consolidado.

## Etapas

1. **Recuperación** desde las API oficiales (`src/collectors/`), con consultas por cultura, geografía y materialidad.
2. **Normalización** de los metadatos a un esquema común en español.
3. **Filtro automático** de evidencia textil, evidencia andina y evidencia de exclusión (`src/preprocessing/textile_filters.py`).
4. **Revisión visual y manual** en un workbook por fuente (`data/metadata/*_revision_manual_v2.xlsx`).
5. **Separación** en principal, complementario, exclusiones y pendientes.
6. **Control de duplicados** por identificador y por imagen.
7. **Consolidación** con esquema armonizado, vocabulario controlado y validación (`python -m src.flujo`).
8. **Anotación manual** de atributos visuales, composicionales e iconográficos.

## Filtro automático

El filtro asigna un puntaje y un estado (`aceptado_textil`, `revision_manual`, `excluido_no_textil`, `excluido_sin_imagen`) a partir de la clasificación, el material, el nombre del objeto, el título y las etiquetas de la fuente.

Reglas vigentes desde la corrección de octubre de 2026:

- Los términos se buscan como **palabra completa** (`cap` no coincide con *Capelet* ni *Capac*).
- Una clasificación o un material con evidencia textil explícita no se penaliza por contener términos no textiles (*Textiles-Sculpture*, hilo metálico).
- Los términos no textiles del título (por ejemplo *figure*) solo penalizan si ni la clasificación ni el material aportan evidencia textil.
- Los formatos estrechos, bordes y sombreros se detectan en el núcleo del título (lo que precede a *with*): *Tunic with Diamond Band* es una túnica.

El filtro solo propone: la decisión final es siempre manual. `outputs/reports/filtros_comparacion_met_inventario.md` compara el filtro vigente con lo registrado en el inventario MET.

## Criterios de inclusión en el corpus principal

Un registro entra al principal cuando cumple la mayoría de estas condiciones (§6.3.2 de la tesis):

| Criterio | Descripción |
|---|---|
| Pertinencia textil | Objeto textil o superficie textil analizable. |
| Pertinencia andina | Relación sustentable con el mundo andino por cultura, procedencia, periodo, título, clasificación, material, técnica o descripción. |
| Imagen útil | Imagen institucional disponible y apta para análisis visual. |
| Fuente trazable | Enlace oficial al registro del museo. |
| Metadatos suficientes | Información mínima para su trazabilidad. |
| Valor computacional | Pertinente para análisis visual, descripción computacional o recuperación imagen-texto. |

Un registro sin imagen disponible no puede estar en el principal. Por eso MET:312615 pasó a complementario cuando su imagen dejó de existir en el museo (octubre de 2026).

## Criterios para el corpus complementario

Registros relevantes para contraste, ampliación o revisión posterior que no constituyen el núcleo del análisis: fragmentos de baja superficie visual, accesorios textiles, *featherwork* con relación textil, piezas con información incompleta y registros que requieren validación experta. No se usan en las líneas base visuales ni en recuperación imagen-imagen, pero pueden emplearse en experimentos de contraste.

## Criterios de exclusión

| Motivo | Descripción |
|---|---|
| Soporte no textil | Cerámica, metal, madera, piedra u otro soporte. |
| Fuera de alcance cultural | Sin relación andina sustentable o de otra región cultural. |
| Sin imagen útil | Registro sin imagen o con imagen no apta. |
| Moderno no pertinente | Objeto moderno o contemporáneo fuera del alcance histórico definido. |
| Trazabilidad insuficiente | Falta la información mínima para justificar su inclusión. |

La exclusión no niega el valor cultural del objeto: indica que no cumple los criterios de esta versión. Toda exclusión conserva su motivo.

## Revisión manual

Cada fuente tiene un workbook con una fila por registro evaluado. La columna `corpus_final` admite `principal`, `secundario`, `descartados` o `revisar`; `decision_revision`, `motivo_revision`, `observaciones_revision`, `revisor` y `fecha_revision` documentan la decisión humana. En el consolidado, `secundario` se denomina `complementario`, como en la tesis.

Los workbooks son insumos con decisiones humanas: sus generadores no los sobrescriben salvo con `--forzar`. Después de editarlos, `python -m src.flujo` aplica las decisiones y avisa si los conteos ya no coinciden con `config/corpus.toml`, para que cada cambio curatorial se registre de forma explícita.

## Control de duplicados

1. **Por identificador:** `id_fuente` es único dentro de cada fuente y `id_global` (`FUENTE:id_fuente`) en todo el corpus (§6.3.5).
2. **Por imagen:** se agrupan los registros que comparten URL de imagen, archivo (SHA-256) o píxeles decodificados. Son objetos distintos del museo fotografiados juntos: se conservan y se marcan en `grupo_imagen_duplicada`.
3. **Parecido visual:** los pares con hash perceptual muy cercano se listan en el resumen del consolidado para revisión manual, sin agruparlos automáticamente.

## Normalización

`tipo_objeto`, `material_normalizado` y `tecnica_normalizada` usan el vocabulario del Cuadro 6.5. Si la curación definió el valor, se conserva (`origen = curacion`); si no, se deriva por reglas a partir de los campos de la fuente (`origen = regla`). Las correcciones de la anotación manual prevalecen (`origen = anotacion`). Los textos de la fuente se conservan siempre en sus propias columnas.

## Consideraciones metodológicas

La curación es una organización técnica y académica basada en metadatos institucionales y revisión visual, no una clasificación cultural definitiva. Las decisiones pueden revisarse en versiones posteriores, en especial con apoyo de especialistas en textiles andinos, historia del arte, arqueología o comunidades portadoras de conocimiento textil.
