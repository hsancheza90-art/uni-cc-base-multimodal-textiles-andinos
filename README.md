# Corpus MET de Textiles Andinos v1.0

Base multimodal trazable de textiles andinos construida a partir de registros oficiales de The Metropolitan Museum of Art para investigacion en ciencias computacionales.

## Descripcion

Este repositorio contiene el Corpus MET de Textiles Andinos v1.0, un entregable academico orientado a la organizacion, curacion y documentacion de registros textiles andinos procedentes de la coleccion digital de The Metropolitan Museum of Art.

El corpus integra metadatos curatoriales, enlaces oficiales, enlaces a imagenes institucionales, decisiones de curacion y documentacion metodologica. Su finalidad es servir como base para tareas de vision por computadora, aprendizaje multimodal, recuperacion imagen-texto y analisis computacional de patrimonio textil andino.

## Alcance de la version v1.0

La version v1.0 considera exclusivamente registros procedentes de The Metropolitan Museum of Art. Otras fuentes museograficas quedan documentadas como fuentes futuras, pero no forman parte del corpus consolidado en esta version.

## Archivos principales

| Archivo | Descripcion | Filas |
|---|---:|---:|
| `data/processed/corpus_met_textiles_andinos_v1_inventario_base.csv` | Inventario base normalizado desde la fuente oficial | 295 |
| `data/processed/corpus_met_textiles_andinos_v1_principal.csv` | Corpus principal para analisis multimodal | 132 |
| `data/processed/corpus_met_textiles_andinos_v1_complementario.csv` | Corpus complementario para contraste o ampliacion | 50 |
| `data/processed/corpus_met_textiles_andinos_v1_exclusiones_curatoriales.csv` | Registros excluidos con motivo documentado | 29 |
| `data/processed/corpus_met_textiles_andinos_v1_duplicados.csv` | Control de duplicados | 0 |
| `data/metadata/corpus_met_textiles_andinos_v1_fuentes_licencias.csv` | Fuentes, licencias y estado de inclusion | 5 |

## Estructura del repositorio

- `data/processed/`: archivos finales del Corpus MET de Textiles Andinos v1.0.
- `data/metadata/`: fuentes, licencias y metadatos de trazabilidad.
- `data/interim/`: archivos intermedios conservados para auditoria interna.
- `data/raw/`: datos crudos descargados desde fuentes oficiales.
- `docs/`: documentacion academica y metodologica.
- `notebooks/`: cuadernos de exploracion, revision y validacion.
- `outputs/`: reportes, galerias y archivos derivados de revision.
- `src/`: scripts de recoleccion, preprocesamiento y revision.

## Documentacion

| Documento | Proposito |
|---|---|
| `docs/corpus_met_textiles_andinos_v1_ficha_dataset.md` | Ficha academica del dataset |
| `docs/corpus_met_textiles_andinos_v1_protocolo_curacion.md` | Criterios de inclusion, exclusion y organizacion |
| `docs/corpus_met_textiles_andinos_v1_trazabilidad.md` | Relacion entre fuente oficial, archivos y decisiones de curacion |
| `docs/corpus_met_textiles_andinos_v1_uso_etico.md` | Principios de uso responsable del corpus |

## Uso previsto

Este corpus esta destinado a investigacion academica en ciencias computacionales, especialmente en tareas de analisis multimodal, vision por computadora, recuperacion imagen-texto y organizacion computacional de patrimonio textil andino.

## Uso no previsto

No se recomienda usar este corpus para comercializacion directa de motivos patrimoniales, apropiacion de disenos, interpretaciones culturales concluyentes sin validacion experta ni clasificacion cultural automatica sin revision humana.

## Estado del entregable

La version v1.0 consolida el primer corpus institucional del proyecto, basado en registros del MET, con archivos finales, documentacion metodologica, control de duplicados y trazabilidad hacia la fuente oficial.

## Contexto academico

Este repositorio forma parte de una investigacion de tesis en la Maestria en Ciencias Computacionales de la Universidad Nacional de Ingenieria, orientada al estudio computacional de textiles andinos como objetos materiales, visuales, culturales y multimodales.


