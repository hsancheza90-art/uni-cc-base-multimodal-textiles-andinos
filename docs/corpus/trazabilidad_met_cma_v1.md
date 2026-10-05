# Trazabilidad del corpus MET+CMA v1

## Principio

Cada registro del consolidado puede rastrearse hasta su registro oficial en el museo y hasta la decisión humana que lo ubicó en su subconjunto. Toda transformación entre ambos extremos está en el código del repositorio y se puede regenerar sin acceso a red.

## Cadena de un registro

```text
API del museo
  -> colector (src/collectors/)                    respuestas crudas en data/raw/ (fuera de git)
  -> inventario o candidatos normalizados           MET: data/processed/corpus_met_textiles_andinos_v1_inventario_base.csv
                                                    CMA: data/metadata/cma_andes_textiles_candidates.csv
  -> filtro automático y revisión manual            MET v1: data/historico/met_v1/ (auditoría de 161 registros)
                                                    v2: data/metadata/*_revision_manual_v2.xlsx
  -> subconjuntos revisados                         data/metadata/*_revisado.csv
  -> consolidado armonizado                         data/processed/corpus_textiles_andinos_met_cma_v1_consolidado.csv
  -> anotación manual                               data/metadata/anotacion_met_cma_v1.xlsx -> anotaciones_met_cma_v1.csv
```

## Campos de trazabilidad por registro

| Campo | Indica |
|---|---|
| `id_global`, `fuente`, `id_fuente` | Identidad del objeto en el corpus y en el museo |
| `url_objeto`, `url_imagen` | Registro e imagen oficiales |
| `archivo_origen` | CSV revisado del que proviene el registro |
| `origen_curacion` | Etapa en la que el registro entró al corpus |
| `decision_auditoria`, `motivo_curacion_final` | Decisión humana y su justificación |
| `origen_tipo_objeto`, `origen_material_normalizado`, `origen_tecnica_normalizada` | Si el valor normalizado viene de la curación, de una regla o de la anotación |
| `licencia_fuente` | Campo de licencia tal como lo entrega el museo |
| `fecha_descarga_metadatos` | Fecha de descarga de los metadatos (MET) |
| `imagen_sha256` | Huella del archivo de imagen descargado |

## Versiones y verificación

- Cada entrega se congela con una etiqueta git: `v1.0-corpus-met-textiles-andinos` (MET v1), `corpus-met-cma-v1.0`, `corpus-met-cma-v1.1` y siguientes.
- `data/processed/corpus_textiles_andinos_met_cma_v1_sha256.txt` registra el SHA-256 del consolidado, del registro de fuentes y del manifiesto de imágenes. Para verificar una copia: `sha256sum -c data/processed/corpus_textiles_andinos_met_cma_v1_sha256.txt` (o `Get-FileHash` en Windows).
- `python -m src.flujo` regenera todas las salidas desde los insumos versionados; `pytest` comprueba que la regeneración coincide byte a byte con lo versionado.
- Los archivos de texto usan fin de línea LF en cualquier sistema (`.gitattributes`), de modo que las sumas no dependen del sistema operativo.

## Cambios curatoriales registrados

| Fecha | Cambio | Dónde consta |
|---|---|---|
| 2026-06 | Auditoría manual MET v1: 97 al principal, 35 al complementario, 29 excluidos | `data/historico/met_v1/` |
| 2026-07 | Revisión manual MET v2 y CMA v2 | `data/metadata/*_revision_manual_v2.xlsx` |
| 2026-10-05 | MET:312615 pasa a complementario: imagen no disponible en el museo | `met_revision_manual_v2.xlsx`, fila del registro |
| 2026-10-05 | 9 registros MET recuperados por el filtro corregido, pendientes de revisión | `met_revision_manual_v2.xlsx`, `met_pendientes_revision_v2.csv` |

## Lo que no se versiona

- Respuestas crudas de las API (`data/raw/`): se regeneran con los colectores.
- Imágenes (`data/images/`): se descargan con `python -m src.imagenes.descargar_imagenes`; el manifiesto versionado permite verificar que son las mismas.
