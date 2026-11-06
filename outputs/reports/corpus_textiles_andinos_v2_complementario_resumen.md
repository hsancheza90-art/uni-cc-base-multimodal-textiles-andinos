# Corpus complementario v2 (MET, CMA y AIC)

Resumen generado por `python -m src.flujo` (`src/anotacion/corpus_v2.py`). Archivo: `data/processed/corpus_textiles_andinos_v2_complementario.csv`, con el esquema de `docs/esquema_consolidado_met_cma_v1.md` y tres columnas de aptitud al final.

## Registros

| Fuente | Registros | CSV revisado |
|---|---|---|
| MET | 25 | data/metadata/met_corpus_secundario_v2_revisado.csv |
| CMA | 4 | data/metadata/cma_corpus_secundario_v2_revisado.csv |
| AIC | 124 | data/metadata/aic_corpus_secundario_v2_revisado.csv |
| Total | 153 |  |

## Aptitud

Registros sin fila en `data/metadata/aptitud_imagenes_v2.csv`: 0.
Un registro sin ficha no se descarta: queda con las columnas de aptitud vacias.

| banda_sugerida | MET | CMA | AIC |
|---|---|---|---|
| descartar | 0 | 0 | 10 |
| principal | 4 | 1 | 2 |
| revisar | 2 | 3 | 21 |
| secundario | 19 | 0 | 91 |

## Campos normalizados: origen del valor

`curacion`: valor curado en el workbook de revision; `regla`: regla automatica sobre el texto de la fuente (`src/preprocessing/normalizacion.py`, `src/preprocessing/surface_filters.py`), que la anotacion debe validar; vacio: ninguna regla lo determina.

| Campo | Origen | MET | CMA | AIC |
|---|---|---|---|---|
| `tipo_objeto` | curacion | 4 | 0 | 123 |
| `tipo_objeto` | regla | 21 | 4 | 0 |
| `tipo_objeto` | (vacio) | 0 | 0 | 1 |
| `material_normalizado` | curacion | 3 | 0 | 0 |
| `material_normalizado` | regla | 22 | 4 | 21 |
| `material_normalizado` | (vacio) | 0 | 0 | 103 |
| `tecnica_normalizada` | curacion | 3 | 0 | 0 |
| `tecnica_normalizada` | regla | 18 | 1 | 123 |
| `tecnica_normalizada` | (vacio) | 4 | 3 | 1 |

## Valores curados fuera del vocabulario

No se aceptan como normalizados: se vacian y, salvo en `tipo_superficie`, la regla calcula el valor. El texto de la fuente queda en `clasificacion_original`, `nombre_objeto_original`, `material` o `tecnica`.

| Fuente | Campo | Valor | Registros |
|---|---|---|---|
| AIC | `tipo_objeto` | tipo_no_determinado | 1 |
| CMA | `tipo_objeto` | Embroidery | 1 |
| CMA | `tipo_objeto` | Textile | 3 |

## Cobertura de campos (registros con valor)

| Campo | MET | CMA | AIC |
|---|---|---|---|
| `id_global` | 25/25 | 4/4 | 124/124 |
| `fuente` | 25/25 | 4/4 | 124/124 |
| `id_fuente` | 25/25 | 4/4 | 124/124 |
| `numero_acceso` | 0/25 | 4/4 | 124/124 |
| `institucion` | 25/25 | 4/4 | 124/124 |
| `url_objeto` | 25/25 | 4/4 | 124/124 |
| `url_imagen` | 25/25 | 4/4 | 124/124 |
| `url_imagen_miniatura` | 25/25 | 0/4 | 124/124 |
| `ruta_imagen_local` | 25/25 | 4/4 | 124/124 |
| `titulo_original` | 25/25 | 4/4 | 124/124 |
| `titulo_es_sugerido` | 25/25 | 0/4 | 0/124 |
| `descripcion` | 3/25 | 3/4 | 0/124 |
| `cultura` | 25/25 | 4/4 | 69/124 |
| `periodo` | 0/25 | 0/4 | 0/124 |
| `fecha_objeto` | 25/25 | 4/4 | 120/124 |
| `procedencia` | 25/25 | 4/4 | 124/124 |
| `departamento` | 25/25 | 4/4 | 124/124 |
| `clasificacion_original` | 25/25 | 4/4 | 124/124 |
| `nombre_objeto_original` | 25/25 | 0/4 | 124/124 |
| `tipo_objeto` | 25/25 | 4/4 | 123/124 |
| `origen_tipo_objeto` | 25/25 | 4/4 | 123/124 |
| `tipo_superficie` | 4/25 | 0/4 | 124/124 |
| `material` | 25/25 | 0/4 | 64/124 |
| `material_normalizado` | 25/25 | 4/4 | 21/124 |
| `origen_material_normalizado` | 25/25 | 4/4 | 21/124 |
| `tecnica` | 0/25 | 4/4 | 0/124 |
| `tecnica_normalizada` | 21/25 | 1/4 | 123/124 |
| `origen_tecnica_normalizada` | 21/25 | 1/4 | 123/124 |
| `dimensiones` | 25/25 | 0/4 | 110/124 |
| `color_dominante` | 0/25 | 0/4 | 0/124 |
| `colores` | 0/25 | 0/4 | 0/124 |
| `contraste` | 0/25 | 0/4 | 0/124 |
| `densidad_visual` | 0/25 | 0/4 | 0/124 |
| `composicion` | 0/25 | 0/4 | 0/124 |
| `simetria` | 0/25 | 0/4 | 0/124 |
| `repeticion` | 0/25 | 0/4 | 0/124 |
| `borde` | 0/25 | 0/4 | 0/124 |
| `centro` | 0/25 | 0/4 | 0/124 |
| `motivos` | 0/25 | 0/4 | 0/124 |
| `familia_iconografica` | 0/25 | 0/4 | 0/124 |
| `motivo_principal` | 0/25 | 0/4 | 0/124 |
| `decision_curacion_final` | 25/25 | 4/4 | 124/124 |
| `motivo_curacion_final` | 25/25 | 4/4 | 124/124 |
| `decision_auditoria` | 25/25 | 4/4 | 124/124 |
| `motivo_auditoria` | 25/25 | 4/4 | 124/124 |
| `observacion_auditoria` | 25/25 | 4/4 | 90/124 |
| `categoria_revision` | 0/25 | 4/4 | 124/124 |
| `origen_curacion` | 25/25 | 4/4 | 124/124 |
| `estado_licencia` | 25/25 | 4/4 | 124/124 |
| `licencia_fuente` | 25/25 | 4/4 | 124/124 |
| `derechos_reproduccion` | 0/25 | 0/4 | 0/124 |
| `estado_metadatos` | 25/25 | 4/4 | 124/124 |
| `estado_anotacion` | 25/25 | 4/4 | 124/124 |
| `estado_imagen` | 25/25 | 4/4 | 124/124 |
| `observaciones` | 0/25 | 0/4 | 2/124 |
| `anotador` | 0/25 | 0/4 | 0/124 |
| `fecha_anotacion` | 0/25 | 0/4 | 0/124 |
| `observaciones_anotacion` | 0/25 | 0/4 | 0/124 |
| `grupo_imagen_duplicada` | 0/25 | 0/4 | 2/124 |
| `imagen_sha256` | 25/25 | 4/4 | 124/124 |
| `imagen_dhash` | 0/25 | 0/4 | 0/124 |
| `imagen_ancho` | 25/25 | 4/4 | 124/124 |
| `imagen_alto` | 25/25 | 4/4 | 124/124 |
| `terminos_andinos` | 0/25 | 4/4 | 124/124 |
| `terminos_textiles` | 0/25 | 4/4 | 67/124 |
| `consulta_origen` | 25/25 | 4/4 | 124/124 |
| `archivo_origen` | 25/25 | 4/4 | 124/124 |
| `fecha_descarga_metadatos` | 25/25 | 0/4 | 124/124 |
| `puntaje_aptitud` | 25/25 | 4/4 | 124/124 |
| `banda_sugerida` | 25/25 | 4/4 | 124/124 |
| `referencia_sugerida` | 25/25 | 4/4 | 124/124 |

## Campos obligatorios vacios

Se informan y no detienen el flujo: un valor que ninguna entrada registra no se completa (no se imputa).

Ninguno.

## estado_metadatos

| Valor | MET | CMA | AIC |
|---|---|---|---|
| completo | 20 | 1 | 14 |
| insuficiente | 0 | 0 | 56 |
| parcial | 5 | 3 | 54 |

## estado_imagen

| Valor | MET | CMA | AIC |
|---|---|---|---|
| util | 25 | 4 | 124 |

## estado_licencia

| Valor | MET | CMA | AIC |
|---|---|---|---|
| cc0 | 0 | 4 | 124 |
| dominio_publico | 25 | 0 | 0 |

## Imagenes compartidas entre registros

Misma `url_imagen` o mismo archivo de la copia de evaluacion (SHA-256). Se conservan: son objetos distintos del museo que comparten fotografia.

| Grupo | Registros |
|---|---|
| DUPC-001 | AIC:85351, AIC:85352 |

## Criterios

- Registro de origen (`src/utils/fuentes.py`): candidatos de CMA y AIC; en MET, el inventario de la descarga de la API y, para la descripcion curada, las salidas base v2 (`config/corpus.toml` [met.base]). El valor del workbook tiene prioridad; el de origen lo completa si esta vacio. Ninguno se modifica.
- Imagen: copia de evaluacion de 1600 px (`ruta_imagen_local`, `imagen_sha256`, `imagen_ancho`, `imagen_alto`); `estado_imagen` usa el mismo lado minimo que el consolidado v1.
- `estado_anotacion` es `sin_anotar` en todos los registros: la anotacion estructural no se lee aqui.
