# Trazabilidad del Corpus MET de Textiles Andinos v1.0

## Objetivo

Documentar la relacion entre los registros del corpus, la fuente oficial, los archivos generados y las decisiones de curacion aplicadas durante la construccion del Corpus MET de Textiles Andinos v1.0.

## Fuente oficial

La fuente principal de esta version es The Metropolitan Museum of Art. Cada registro conserva, cuando esta disponible, el identificador institucional del objeto, el enlace oficial al registro curatorial y el enlace a la imagen institucional.

## Identificadores de trazabilidad

| Campo | Funcion |
|---|---|
| `id_objeto` | Identificador institucional del objeto en The Met. |
| `fuente` | Codigo de la fuente museografica. En v1.0 corresponde a `met`. |
| `institucion` | Nombre de la institucion fuente. |
| `url_objeto` | Enlace oficial al registro del objeto. |
| `url_imagen` | Enlace a la imagen institucional usada como referencia visual. |
| `url_imagen_miniatura` | Enlace a imagen de menor resolucion cuando esta disponible. |
| `fecha_descarga` | Fecha asociada a la recuperacion o consolidacion del registro. |

## Flujo de archivos

| Etapa | Archivo |
|---|---|
| Inventario normalizado | `data/processed/corpus_met_textiles_andinos_v1_inventario_base.csv` |
| Seleccion principal | `data/processed/corpus_met_textiles_andinos_v1_principal.csv` |
| Seleccion complementaria | `data/processed/corpus_met_textiles_andinos_v1_complementario.csv` |
| Exclusiones curatoriales | `data/processed/corpus_met_textiles_andinos_v1_exclusiones_curatoriales.csv` |
| Duplicados | `data/processed/corpus_met_textiles_andinos_v1_duplicados.csv` |
| Fuentes y licencias | `data/metadata/corpus_met_textiles_andinos_v1_fuentes_licencias.csv` |

## Archivos intermedios

Los archivos previos de curacion y anotacion fueron movidos a:

- `data/interim/met_curacion_previa/`
- `data/interim/met_anotacion/`

Estos archivos no forman parte del entregable principal, pero se conservan para auditoria interna y reconstruccion metodologica.

## Decisiones de curacion

Las decisiones principales se documentan mediante campos como:

- `decision_curacion_final`
- `motivo_curacion_final`
- `decision_auditoria`
- `motivo_auditoria`
- `observacion_auditoria`
- `categoria_revision_v2`
- `motivo_revision_v2`

Estos campos permiten reconstruir por que un registro fue asignado al corpus principal, al corpus complementario o a exclusiones curatoriales.

## Control de duplicados

En la version v1.0 no se identificaron duplicados por `id_objeto` en el inventario base, el corpus principal ni el corpus complementario. El archivo de duplicados se conserva como evidencia del control realizado.

## Principio de trazabilidad

Ningun registro del corpus final debe depender solo de una anotacion local. Cada objeto debe poder rastrearse hacia su fuente institucional mediante `id_objeto`, `url_objeto` y, cuando corresponda, `url_imagen`.

## Nota metodologica

La trazabilidad garantiza reproducibilidad tecnica, pero no reemplaza la interpretacion experta. Las decisiones de curacion deben entenderse como una organizacion academica para investigacion computacional, no como una clasificacion definitiva de valor cultural o simbolico.
