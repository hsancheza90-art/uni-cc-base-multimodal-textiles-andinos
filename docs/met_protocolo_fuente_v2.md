# Protocolo de fuente MET v2

## Objetivo

Este documento define el procedimiento de consolidación, normalización, curación y revisión manual de registros textiles andinos procedentes de The Metropolitan Museum of Art (MET).

La finalidad no es realizar una descarga masiva de objetos, sino construir una base curada, trazable y metodológicamente defendible para el corpus multimodal de textiles andinos.

La versión MET v2 reorganiza el trabajo curatorial previo, preserva los resultados ya obtenidos y explicita los criterios usados para distinguir entre corpus principal, corpus secundario y registros descartados.

## Fuente Institucional

- Institución: The Metropolitan Museum of Art.
- Acceso: API pública del MET y fichas institucionales de colección.
- Tipo de fuente: colección museográfica con metadatosatos curatoriales, imágenes asociadas y enlaces institucionales.
- Uso dentro del proyecto: fuente principal del corpus, junto con Cleveland Museum of Art (CMA).

## Enfoque Metodológico

El trabajo con MET se entiende como una curación documental y visual. Cada registro se evalúa considerando tres niveles:

1. Evidencia documental: título, cultura, clasificación, materiales, técnica, procedencia, periodo y descripción.
2. Evidencia visual: correspondencia entre la imagen disponible y un objeto textil analizable.
3. Pertinencia computacional: utilidad del objeto para tareas futuras de clasificación, recuperación multimodal, descripción visual o análisis de patrones.

Por esta razón, la fuente no se trata como una tabla neutral de datos, sino como un conjunto museográfico que requiere interpretación, control de ruido, revisión visual y criterios consistentes.

## Estrategia De Búsqueda Y Consolidación

Las consultas exploratorias combinan términos culturales, geográficos y textiles. Entre los términos considerados se incluyen:

- Andes
- Andean
- Peru
- Peruvian
- Inca
- Wari / Huari
- Chancay
- Nasca / Nazca
- Paracas
- Moche
- Chimu
- Tiwanaku / Tiahuanaco
- textile
- woven
- cloth
- cotton
- camelid
- wool
- tapestry
- tunic
- mantle
- bag

Los resultados se deduplican por identificador institucional del MET. En MET v2, la base final no se reconstruye desde cero a partir de la API, sino que se consolida a partir de los archivos curatoriales MET v1 ya versionados y revisados.

## Criterios De Inclusión

Un registro puede ingresar como candidato si cumple las siguientes condiciones:

1. Tiene identificador institucional trazable.
2. Tiene enlace a la ficha del objeto en el MET.
3. Tiene imagen disponible o una URL de imagen asociada.
4. Presenta evidencia textil en clasificación, técnica, material, título o descripción.
5. Presenta evidencia andina, prehispánica o sudamericana pertinente en cultura, procedencia, título o descripción.

## Criterios Para El Corpus Principal

Un registro se considera parte del corpus principal cuando:

1. El objeto es claramente textil.
2. La imagen permite inspección visual suficiente.
3. La pieza es pertinente para análisis de patrones, composición, materialidad o iconografía.
4. La información curatorial respalda una adscripción andina o prehispánica relacionada.
5. No corresponde principalmente a cerámica, metal, madera, piedra u otro soporte no textil.

## Criterios Para El Corpus Secundario

Un registro puede mantenerse como corpus secundario cuando tiene valor documental, pero no cumple plenamente el criterio del corpus principal. Por ejemplo:

1. Piezas con plumas o materialidad mixta.
2. Fragmentos textiles con valor de referencia, pero menor utilidad visual.
3. Objetos relacionados con indumentaria o materialidad textil, aunque no sean ideales para el primer corpus principal.
4. Casos que requieren revisión posterior por ambigüedad curatorial o visual.

## Criterios De Descarte

Un registro se descarta cuando:

1. No tiene imagen útil.
2. No presenta evidencia textil suficiente.
3. No presenta evidencia andina suficiente.
4. Corresponde a cerámica, metal, piedra, madera u otro objeto no textil.
5. La imagen o los metadatos no permiten sostener su inclusión de manera defendible.
6. Es un duplicado de otro registro ya incorporado.

## Estados De Curación

La versión MET v2 usa estados en español para facilitar lectura y revisión:

- `corpus_principal`
- `corpus_secundario`
- `descartado`
- `revisar`

Durante etapas exploratorias también pueden aparecer estados auxiliares:

- `candidato`
- `descartado_sin_imagen`
- `descartado_no_textil`
- `descartado_no_andino`
- `descartado_objeto_no_pertinente`
- `duplicado`
- `pendiente_revision_visual`

## Salidas Base MET v2

La versión v2 no sobrescribe los archivos históricos. Las salidas base se guardan con nombres versionados:

- `data/metadata/met_corpus_principal_v2.csv`
- `data/metadata/met_corpus_secundario_v2.csv`
- `data/metadata/met_descartados_v2.csv`
- `outputs/reports/met_resumen_curacion_v2.md`
- `outputs/reports/met_auditoria_tecnica_v2.md`

## Control Contra La Curación Previa

La versión MET v2 se construye a partir de los archivos curatoriales ya versionados de MET v1. Por ello, el objetivo no es volver a inferir el corpus desde cero, sino reorganizar la curación previa en salidas más claras, auditables y consistentes con el protocolo metodológico.

Los conteos consolidados de la base auditada son:

| Conjunto base MET v2 | Registros |
|---|---:|
| Corpus principal | 132 |
| Corpus secundario | 50 |
| Descartados | 29 |

Estos conteos fueron validados comparando los identificadores institucionales de los archivos fuente v1 contra las nuevas salidas MET v2. La auditoría técnica no detectó pérdida de identificadores ni duplicados en el corpus principal.

## Revisión Manual Final

Luego de construir la base auditada MET v2, se incorpora una capa de revisión manual mediante el archivo:

- `data/metadata/met_revision_manual_v2.xlsx`

Este workbook concentra todos los registros en una sola hoja y conserva dos campos clave:

- `corpus_actual`: clasificación de partida derivada de la base auditada.
- `corpus_final`: clasificación final luego de la revisión humana.

La modificación de `corpus_final` permite mover registros entre corpus principal, corpus secundario y descartados sin alterar los archivos base. Las decisiones se aplican con:

```bash
python src/metadata/apply_met_review_v2.py --root .
```

Esta capa conserva trazabilidad entre la clasificación original y la decisión final, permitiendo documentar ajustes curatoriales como duplicados visuales, imágenes caídas, piezas ambiguas o registros mejor ubicados en corpus secundario.

## Comparación Entre Base Auditada Y Revisión Manual

La revisión manual no reemplaza la base auditada. Introduce una capa curatorial final que permite corregir duplicados visuales, imágenes caídas, registros ambiguos o piezas mejor ubicadas en otro subconjunto.

| Etapa MET v2 | Corpus principal | Corpus secundario | Descartados | Pendientes |
|---|---:|---:|---:|---:|
| Base auditada | 132 | 50 | 29 | 0 |
| Revisión manual | 127 | 54 | 30 | 0 |

Los movimientos aplicados redujeron el corpus principal en 5 registros. Cuatro registros fueron reubicados en el corpus secundario y un registro fue enviado a descartados por tratarse de una imagen repetida o no adecuada para el corpus principal final.

Esta comparación permite conservar la trazabilidad entre el corpus base y el corpus revisado, evitando que la curación manual borre la historia de decisiones del proceso.

## Salidas Revisadas MET v2

La revisión manual genera los siguientes archivos:

- `data/metadata/met_revision_manual_v2.xlsx`
- `data/metadata/met_corpus_principal_v2_revisado.csv`
- `data/metadata/met_corpus_secundario_v2_revisado.csv`
- `data/metadata/met_descartados_v2_revisado.csv`
- `data/metadata/met_pendientes_revision_v2.csv`
- `outputs/reports/met_resumen_revision_manual_v2.md`
- `outputs/review/met_corpus_principal_v2_revisado_galeria.html`
- `outputs/review/met_corpus_secundario_v2_revisado_galeria.html`
- `outputs/review/met_descartados_v2_revisado_galeria.html`

## Salida Recomendada

Para efectos de la investigación, se recomienda usar las salidas revisadas:

- `data/metadata/met_corpus_principal_v2_revisado.csv`
- `data/metadata/met_corpus_secundario_v2_revisado.csv`
- `data/metadata/met_descartados_v2_revisado.csv`

Las salidas base se conservan como respaldo auditado y punto de comparación.

## Principio De Trazabilidad

Ningún registro debe incorporarse sin conservar:

1. Fuente institucional.
2. Identificador de fuente.
3. URL del objeto.
4. URL de imagen o ruta local.
5. Estado de curación.
6. Clasificación base y clasificación final.
7. Nota breve que justifique inclusión, separación secundaria, descarte o movimiento manual.

## Comandos Reproducibles

Construcción de las salidas curatoriales base:

```bash
python src/metadata/build_met_corpus_v2.py --root .
```

Auditoría técnica de la base:

```bash
python src/metadata/audit_met_outputs_v2.py --root .
```

Creación del workbook de revisión manual:

```bash
python src/preprocessing/create_met_review_workbook_v2.py --root .
```

Aplicación de decisiones manuales:

```bash
python src/metadata/apply_met_review_v2.py --root .
```

Generación de galerías HTML revisadas:

```bash
python src/review/build_met_gallery_v2.py --root . --revisado
```

## Limitaciones

El uso de colecciones museográficas implica posibles sesgos de catalogación, disponibilidad desigual de imágenes, variación terminológica entre registros y diferencias en el nivel de descripción curatorial.

Por ello, los resultados deben interpretarse como un corpus curado para investigación computacional, no como una representación exhaustiva de la producción textil andina ni como una clasificación cultural concluyente sin revisión especializada.
