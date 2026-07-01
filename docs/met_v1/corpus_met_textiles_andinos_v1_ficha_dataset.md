# Corpus MET de Textiles Andinos v1.0

## Nombre del dataset

Corpus MET de Textiles Andinos v1.0: Base Multimodal Trazable para Investigacion en Ciencias Computacionales.

## Descripcion general

Este dataset reune registros curatoriales, enlaces oficiales e imagenes publicas de textiles andinos procedentes de The Metropolitan Museum of Art. La version v1.0 organiza los registros en inventario base, corpus principal, corpus complementario, exclusiones curatoriales y control de duplicados.

El dataset ha sido preparado como insumo para una tesis de Maestria en Ciencias Computacionales orientada al analisis multimodal de textiles andinos, con enfasis en trazabilidad, curacion de metadatos y uso responsable de fuentes museograficas oficiales.

## Fuente principal

- Institucion: The Metropolitan Museum of Art
- Fuente: coleccion digital oficial y API publica de The Met
- Alcance de esta version: objetos recuperados, normalizados y curados desde registros del MET
- Version del corpus: v1.0
- Fecha de consolidacion: 2026-06-23

## Archivos principales

| Archivo | Descripcion | Filas |
|---|---:|---:|
| `data/processed/corpus_met_textiles_andinos_v1_inventario_base.csv` | Inventario base normalizado desde la fuente oficial | 295 |
| `data/processed/corpus_met_textiles_andinos_v1_principal.csv` | Corpus principal para analisis multimodal | 132 |
| `data/processed/corpus_met_textiles_andinos_v1_complementario.csv` | Corpus complementario para revision, contraste o ampliacion | 50 |
| `data/processed/corpus_met_textiles_andinos_v1_exclusiones_curatoriales.csv` | Registros excluidos por criterios curatoriales o tecnicos | 29 |
| `data/processed/corpus_met_textiles_andinos_v1_duplicados.csv` | Control de duplicados identificados | 0 |

## Criterios de inclusion

Un registro puede formar parte del corpus principal cuando cumple con los siguientes criterios:

1. Corresponde a un objeto textil o superficie textil andina.
2. Presenta enlace oficial al objeto en la coleccion del museo.
3. Presenta enlace disponible a imagen institucional.
4. Tiene metadatos suficientes para su trazabilidad.
5. Su cultura, procedencia, clasificacion, material o descripcion permiten justificar su relacion con textiles andinos.
6. Es pertinente para tareas de analisis visual, recuperacion multimodal, clasificacion o descripcion computacional.

## Criterios de corpus complementario

Un registro puede ubicarse en el corpus complementario cuando es relevante para el estudio, pero no constituye el nucleo principal del analisis. Esto incluye fragmentos, accesorios, piezas de menor superficie visual, objetos con valor comparativo o registros que requieren validacion posterior.

## Criterios de exclusion

Un registro se excluye cuando presenta una o mas de las siguientes condiciones:

1. No corresponde a un textil o artefacto textil.
2. Corresponde a ceramica, metal, madera u otro soporte no textil.
3. No presenta relacion andina suficientemente sustentada.
4. Pertenece a una region cultural fuera del alcance del corpus.
5. No cuenta con imagen util para analisis visual.
6. Presenta limitaciones curatoriales, tecnicas o de trazabilidad que impiden su uso como registro principal.

## Campos relevantes

El corpus principal y complementario incluyen campos de identificacion, fuente, enlaces, imagenes, cultura, periodo, procedencia, tipo de objeto, material, tecnica, descripcion, licencia, estado de anotacion, decisiones de filtro y observaciones curatoriales.

Campos clave:

- `id_objeto`
- `fuente`
- `institucion`
- `url_objeto`
- `url_imagen`
- `titulo_original`
- `titulo_es_sugerido`
- `cultura`
- `periodo`
- `fecha_objeto`
- `tipo_objeto`
- `material`
- `material_normalizado`
- `tecnica`
- `motivos`
- `familia_iconografica`
- `decision_curacion_final`
- `motivo_curacion_final`

## Trazabilidad

Cada registro conserva identificador institucional, enlace oficial al objeto y enlace a imagen cuando se encuentra disponible. La version v1.0 prioriza la trazabilidad hacia la fuente oficial sobre la descarga local de imagenes.

## Uso previsto

Este dataset esta destinado a investigacion academica en ciencias computacionales, aprendizaje multimodal, vision por computadora, recuperacion imagen-texto y analisis computacional de patrimonio textil andino.

## Uso no previsto

No se recomienda usar este dataset para comercializacion directa de motivos patrimoniales, afirmaciones concluyentes sobre significados culturales sin validacion experta, apropiacion de disenos, ni clasificacion cultural automatica sin revision humana.

## Limitaciones

1. Los metadatos dependen de la informacion curatorial disponible en la fuente oficial.
2. La clasificacion cultural puede contener vacios, generalizaciones o cambios historicos de catalogacion.
3. La disponibilidad de imagenes puede variar segun la politica institucional.
4. Algunas decisiones de curacion requieren revision experta adicional.
5. El corpus v1.0 cubre solo la fuente MET y no representa la totalidad de textiles andinos existentes en museos o comunidades.

## Nota etica

Los textiles andinos no deben tratarse solo como patrones visuales. Son objetos materiales, historicos, culturales y, en algunos casos, vinculados a memorias comunitarias o dimensiones rituales. Por ello, las inferencias computacionales deben presentarse como aproximaciones analiticas y no como interpretaciones culturales definitivas.

