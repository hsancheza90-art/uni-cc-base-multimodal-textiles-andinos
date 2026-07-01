# Protocolo de fuente MET v2

## Objetivo

Este documento define el procedimiento de recoleccion, normalizacion y curacion de registros textiles andinos procedentes de The Metropolitan Museum of Art. La finalidad no es realizar una descarga masiva de objetos, sino construir una base curada, trazable y metodologicamente defendible para el corpus multimodal de textiles andinos.

La version v2 busca ordenar el flujo previo de trabajo, preservar los resultados ya obtenidos y expresar de manera explicita los criterios curatoriales usados para distinguir entre corpus principal, corpus secundario y registros descartados.

## Fuente institucional

- Institucion: The Metropolitan Museum of Art.
- Acceso: API publica del MET.
- Tipo de fuente: coleccion museografica con metadatos curatoriales, imagenes asociadas y enlaces institucionales.
- Uso dentro del proyecto: fuente principal para la primera entrega del corpus junto con Cleveland Museum of Art.

## Enfoque metodologico

El trabajo con MET se entiende como una curacion documental y visual. Cada registro debe ser evaluado considerando tres niveles:

1. Evidencia documental: titulo, cultura, clasificacion, materiales, tecnica, departamento y descripcion.
2. Evidencia visual: correspondencia entre la imagen y un objeto textil analizable.
3. Pertinencia para el corpus: utilidad del objeto para tareas futuras de clasificacion, recuperacion multimodal o descripcion visual.

Por esta razon, la fuente no se trata como una tabla neutral de datos, sino como un conjunto museografico que requiere interpretacion, control de ruido y criterios consistentes.

## Estrategia de busqueda

Las consultas deben combinar terminos culturales, geograficos y textiles. Entre los terminos considerados se incluyen:

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

Los resultados se deduplican por identificador institucional del MET.

## Criterios de inclusion

Un registro puede ingresar como candidato si cumple las siguientes condiciones:

1. Tiene identificador institucional trazable.
2. Tiene enlace a la ficha del objeto en el MET.
3. Tiene imagen disponible o una URL de imagen asociada.
4. Presenta evidencia textil en clasificacion, tecnica, material, titulo o descripcion.
5. Presenta evidencia andina, prehispanica o sudamericana pertinente en cultura, procedencia, titulo o descripcion.

## Criterios para el corpus principal

Un registro se considera parte del corpus principal cuando:

1. El objeto es claramente textil.
2. La imagen permite inspeccion visual suficiente.
3. La pieza es pertinente para analisis de patrones, composicion, materialidad o iconografia.
4. La informacion curatorial respalda una adscripcion andina o prehispanica relacionada.
5. No corresponde principalmente a ceramica, metal, madera, piedra u otro soporte no textil.

## Criterios para el corpus secundario

Un registro puede mantenerse como corpus secundario cuando tiene valor documental, pero no cumple plenamente el criterio del corpus principal. Por ejemplo:

1. Piezas con plumas o materialidad mixta.
2. Fragmentos textiles con valor de referencia, pero menor utilidad visual.
3. Objetos relacionados con indumentaria o materialidad textil, aunque no sean ideales para el primer corpus principal.
4. Casos que requieren revision posterior por ambiguedad curatorial o visual.

## Criterios de descarte

Un registro se descarta cuando:

1. No tiene imagen util.
2. No presenta evidencia textil suficiente.
3. No presenta evidencia andina suficiente.
4. Corresponde a ceramica, metal, piedra, madera u otro objeto no textil.
5. La imagen o los metadatos no permiten sostener su inclusion de manera defendible.
6. Es un duplicado de otro registro ya incorporado.

## Estados de curacion

La version v2 usara estados en espanol para facilitar lectura y revision:

- candidato
- corpus_principal
- corpus_secundario
- descartado_sin_imagen
- descartado_no_textil
- descartado_no_andino
- descartado_objeto_no_pertinente
- duplicado
- pendiente_revision_visual

## Columnas normalizadas

Las salidas normalizadas de MET v2 deben usar nombres en espanol:

- fuente
- id_fuente
- numero_inventario
- titulo
- cultura
- fecha_creacion
- clasificacion
- tecnica
- material
- dimensiones
- departamento
- descripcion
- url_objeto
- url_imagen
- ruta_imagen_local
- licencia
- tiene_imagen
- terminos_andinos
- terminos_textiles
- estado_curacion
- notas_curacion
- consultas_origen

## Salidas esperadas

La version v2 no debe sobrescribir los archivos historicos. Las nuevas salidas se guardaran con nombres versionados:

- `data/metadata/met_candidatos_v2.csv`
- `data/metadata/met_corpus_principal_v2.csv`
- `data/metadata/met_corpus_secundario_v2.csv`
- `data/metadata/met_descartados_v2.csv`
- `outputs/reports/met_resumen_curacion_v2.md`


## Control contra la curacion previa

La version MET v2 se construye a partir de los archivos curatoriales ya versionados de MET v1. Por ello, el objetivo no es volver a inferir el corpus desde cero, sino reorganizar la curacion previa en salidas mas claras, auditables y consistentes con el protocolo metodologico.

Los conteos consolidados de referencia son:

| Conjunto | Conteo esperado |
|---|---:|
| corpus principal v2 | 132 |
| corpus secundario v2 | 50 |
| descartados | 29 |

Estos conteos fueron validados comparando los identificadores institucionales de los archivos fuente v1 contra las nuevas salidas MET v2. La auditoria tecnica no detecto perdida de identificadores ni duplicados en el corpus principal.

Si en una etapa posterior se requiere una submuestra para entrega, presentacion o anotacion manual, esta debera registrarse como seleccion derivada del corpus curado, no como reemplazo del corpus MET v2.


## Principio de trazabilidad

Ningun registro debe incorporarse sin conservar:

1. Fuente institucional.
2. Identificador de fuente.
3. URL del objeto.
4. URL de imagen o ruta local.
5. Estado de curacion.
6. Nota breve que justifique inclusion, separacion secundaria o descarte.

## Limitaciones

El uso de colecciones museograficas implica posibles sesgos de catalogacion, disponibilidad desigual de imagenes, variacion terminologica entre registros y diferencias en el nivel de descripcion curatorial. Por ello, los resultados deben interpretarse como un corpus curado para investigacion computacional, no como una representacion exhaustiva de la produccion textil andina.

## Comandos reproducibles

Construccion de las salidas curatoriales:

```bash
python src/metadata/build_met_corpus_v2.py --root .