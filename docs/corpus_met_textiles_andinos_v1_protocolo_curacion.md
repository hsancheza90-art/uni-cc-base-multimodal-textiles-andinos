# Protocolo de Curacion del Corpus MET de Textiles Andinos v1.0

## Objetivo

Establecer los criterios tecnicos y curatoriales usados para seleccionar, organizar y documentar registros textiles andinos procedentes de The Metropolitan Museum of Art.

Este protocolo busca garantizar que el corpus final sea trazable, reproducible y adecuado para investigacion en ciencias computacionales.

## Alcance

La version v1.0 considera unicamente registros procedentes de The Metropolitan Museum of Art. Otras fuentes museograficas quedan registradas como fuentes futuras, pero no forman parte del corpus consolidado.

## Etapas de curacion

1. Recuperacion inicial de registros desde la fuente oficial.
2. Normalizacion de metadatos principales.
3. Identificacion de evidencia textil y evidencia de exclusion.
4. Revision de pertinencia andina.
5. Separacion en inventario base, corpus principal, corpus complementario y exclusiones.
6. Control de duplicados por identificador institucional.
7. Validacion de enlaces oficiales e imagenes.
8. Consolidacion de archivos finales v1.0.

## Criterios de inclusion en corpus principal

Un registro se incluye en el corpus principal cuando cumple la mayoria de estas condiciones:

| Criterio | Descripcion |
|---|---|
| Pertinencia textil | El objeto corresponde a textil, prenda, fragmento textil, manto, bolsa, tunica, banda u otra superficie textil analizable. |
| Pertinencia andina | La cultura, procedencia, periodo, titulo, clasificacion o material permite justificar relacion con los Andes. |
| Imagen disponible | El registro cuenta con enlace de imagen institucional util para analisis visual. |
| Fuente trazable | El registro conserva enlace oficial al objeto del museo. |
| Valor computacional | El objeto permite analisis visual, descriptivo, multimodal o de recuperacion imagen-texto. |

## Criterios para corpus complementario

Un registro se ubica en el corpus complementario cuando tiene valor para contraste o ampliacion, pero no constituye el nucleo principal del analisis.

Casos frecuentes:

- Fragmentos de baja superficie visual.
- Accesorios textiles.
- Objetos featherwork con relacion textil.
- Piezas con informacion incompleta pero potencialmente util.
- Registros que requieren revision experta posterior.

## Criterios de exclusion

Un registro se excluye cuando presenta una o mas de estas condiciones:

| Motivo | Descripcion |
|---|---|
| Soporte no textil | Ceramica, metal, madera, piedra u otro soporte no textil. |
| Fuera de alcance cultural | Objeto no andino o sin relacion andina sustentable. |
| Imagen no util | Registro sin imagen disponible o sin imagen apta para analisis. |
| Registro moderno no pertinente | Objeto moderno o contemporaneo sin relacion directa con textiles andinos prehispanicos, historicos o tradicionales. |
| Trazabilidad insuficiente | Falta informacion minima para justificar su inclusion. |

## Control de duplicados

El control de duplicados se realiza principalmente por `id_objeto`, que corresponde al identificador institucional del MET. En la version v1.0 no se identificaron duplicados en el corpus principal ni en el corpus complementario.

## Convencion de archivos finales

Los archivos finales del entregable usan el prefijo:

`corpus_met_textiles_andinos_v1`

Esta convencion evita nombres preliminares como `pilot`, `clean`, `review` o `final_final`, y permite identificar con claridad la version academica del corpus.

## Archivos resultantes

| Archivo | Funcion |
|---|---|
| `corpus_met_textiles_andinos_v1_inventario_base.csv` | Registros recuperados y normalizados desde la fuente oficial. |
| `corpus_met_textiles_andinos_v1_principal.csv` | Corpus principal para analisis computacional. |
| `corpus_met_textiles_andinos_v1_complementario.csv` | Registros utiles para contraste o ampliacion. |
| `corpus_met_textiles_andinos_v1_exclusiones_curatoriales.csv` | Registros excluidos con motivo documentado. |
| `corpus_met_textiles_andinos_v1_duplicados.csv` | Control de duplicados. |

## Consideraciones metodologicas

La curacion no debe interpretarse como una clasificacion cultural definitiva. Es una organizacion tecnica y academica basada en metadatos institucionales, revision visual y criterios de pertinencia para investigacion computacional.

Las decisiones de inclusion o exclusion pueden revisarse en versiones posteriores del corpus, especialmente con apoyo de especialistas en textiles andinos, historia del arte, arqueologia o comunidades portadoras de conocimiento textil.



