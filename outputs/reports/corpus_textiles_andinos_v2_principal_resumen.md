# Corpus principal v2 (MET, CMA y AIC)

Resumen generado por `python -m src.flujo` (`src/anotacion/corpus_v2.py`). Archivo: `data/processed/corpus_textiles_andinos_v2_principal.csv`, con el esquema de `docs/esquema_consolidado_met_cma_v1.md` y tres columnas de aptitud al final.

## Registros

| Fuente | Registros | CSV revisado |
|---|---|---|
| MET | 130 | data/metadata/met_corpus_principal_v2_revisado.csv |
| CMA | 104 | data/metadata/cma_corpus_principal_v2_revisado.csv |
| AIC | 228 | data/metadata/aic_corpus_principal_v2_revisado.csv |
| Total | 462 |  |

## Aptitud

Registros sin fila en `data/metadata/aptitud_imagenes_v2.csv`: 0.
Un registro sin ficha no se descarta: queda con las columnas de aptitud vacias.

| banda_sugerida | MET | CMA | AIC |
|---|---|---|---|
| descartar | 5 | 0 | 5 |
| principal | 85 | 90 | 149 |
| revisar | 40 | 14 | 71 |
| secundario | 0 | 0 | 3 |

## Campos normalizados: origen del valor

`curacion`: valor curado en el workbook de revision; `regla`: regla automatica sobre el texto de la fuente (`src/preprocessing/normalizacion.py`, `src/preprocessing/surface_filters.py`), que la anotacion debe validar; vacio: ninguna regla lo determina.

| Campo | Origen | MET | CMA | AIC |
|---|---|---|---|---|
| `tipo_objeto` | curacion | 26 | 0 | 226 |
| `tipo_objeto` | regla | 104 | 100 | 0 |
| `tipo_objeto` | (vacio) | 0 | 4 | 2 |
| `material_normalizado` | curacion | 26 | 0 | 0 |
| `material_normalizado` | regla | 104 | 103 | 166 |
| `material_normalizado` | (vacio) | 0 | 1 | 62 |
| `tecnica_normalizada` | curacion | 21 | 0 | 0 |
| `tecnica_normalizada` | regla | 81 | 86 | 224 |
| `tecnica_normalizada` | (vacio) | 28 | 18 | 4 |

## Valores curados fuera del vocabulario

No se aceptan como normalizados: se vacian y, salvo en `tipo_superficie`, la regla calcula el valor. El texto de la fuente queda en `clasificacion_original`, `nombre_objeto_original`, `material` o `tecnica`.

| Fuente | Campo | Valor | Registros |
|---|---|---|---|
| AIC | `tipo_objeto` | tipo_no_determinado | 2 |
| CMA | `tipo_objeto` | Embroidery | 2 |
| CMA | `tipo_objeto` | Garment | 1 |
| CMA | `tipo_objeto` | Tapestry | 4 |
| CMA | `tipo_objeto` | Textile | 97 |

## Cobertura de campos (registros con valor)

| Campo | MET | CMA | AIC |
|---|---|---|---|
| `id_global` | 130/130 | 104/104 | 228/228 |
| `fuente` | 130/130 | 104/104 | 228/228 |
| `id_fuente` | 130/130 | 104/104 | 228/228 |
| `numero_acceso` | 0/130 | 104/104 | 228/228 |
| `institucion` | 130/130 | 104/104 | 228/228 |
| `url_objeto` | 130/130 | 104/104 | 228/228 |
| `url_imagen` | 130/130 | 104/104 | 228/228 |
| `url_imagen_miniatura` | 130/130 | 0/104 | 228/228 |
| `ruta_imagen_local` | 130/130 | 104/104 | 228/228 |
| `titulo_original` | 130/130 | 104/104 | 228/228 |
| `titulo_es_sugerido` | 130/130 | 0/104 | 0/228 |
| `descripcion` | 26/130 | 50/104 | 43/228 |
| `cultura` | 130/130 | 104/104 | 189/228 |
| `periodo` | 0/130 | 0/104 | 0/228 |
| `fecha_objeto` | 130/130 | 104/104 | 227/228 |
| `procedencia` | 130/130 | 104/104 | 228/228 |
| `departamento` | 130/130 | 104/104 | 228/228 |
| `clasificacion_original` | 130/130 | 104/104 | 228/228 |
| `nombre_objeto_original` | 130/130 | 0/104 | 228/228 |
| `tipo_objeto` | 130/130 | 100/104 | 226/228 |
| `origen_tipo_objeto` | 130/130 | 100/104 | 226/228 |
| `tipo_superficie` | 26/130 | 0/104 | 228/228 |
| `material` | 130/130 | 0/104 | 195/228 |
| `material_normalizado` | 130/130 | 103/104 | 166/228 |
| `origen_material_normalizado` | 130/130 | 103/104 | 166/228 |
| `tecnica` | 0/130 | 104/104 | 40/228 |
| `tecnica_normalizada` | 102/130 | 86/104 | 224/228 |
| `origen_tecnica_normalizada` | 102/130 | 86/104 | 224/228 |
| `dimensiones` | 130/130 | 0/104 | 220/228 |
| `color_dominante` | 0/130 | 0/104 | 0/228 |
| `colores` | 0/130 | 0/104 | 0/228 |
| `contraste` | 0/130 | 0/104 | 0/228 |
| `densidad_visual` | 0/130 | 0/104 | 0/228 |
| `composicion` | 0/130 | 0/104 | 0/228 |
| `simetria` | 0/130 | 0/104 | 0/228 |
| `repeticion` | 0/130 | 0/104 | 0/228 |
| `borde` | 0/130 | 0/104 | 0/228 |
| `centro` | 0/130 | 0/104 | 0/228 |
| `motivos` | 0/130 | 0/104 | 0/228 |
| `familia_iconografica` | 0/130 | 0/104 | 0/228 |
| `motivo_principal` | 0/130 | 0/104 | 0/228 |
| `decision_curacion_final` | 130/130 | 104/104 | 228/228 |
| `motivo_curacion_final` | 130/130 | 16/104 | 228/228 |
| `decision_auditoria` | 130/130 | 104/104 | 228/228 |
| `motivo_auditoria` | 33/130 | 16/104 | 228/228 |
| `observacion_auditoria` | 33/130 | 16/104 | 1/228 |
| `categoria_revision` | 0/130 | 104/104 | 228/228 |
| `origen_curacion` | 130/130 | 104/104 | 228/228 |
| `estado_licencia` | 130/130 | 104/104 | 228/228 |
| `licencia_fuente` | 130/130 | 104/104 | 228/228 |
| `derechos_reproduccion` | 0/130 | 0/104 | 43/228 |
| `estado_metadatos` | 130/130 | 104/104 | 228/228 |
| `estado_anotacion` | 130/130 | 104/104 | 228/228 |
| `estado_imagen` | 130/130 | 104/104 | 228/228 |
| `observaciones` | 6/130 | 2/104 | 8/228 |
| `anotador` | 0/130 | 0/104 | 0/228 |
| `fecha_anotacion` | 0/130 | 0/104 | 0/228 |
| `observaciones_anotacion` | 0/130 | 0/104 | 0/228 |
| `grupo_imagen_duplicada` | 6/130 | 2/104 | 8/228 |
| `imagen_sha256` | 130/130 | 104/104 | 228/228 |
| `imagen_dhash` | 0/130 | 0/104 | 0/228 |
| `imagen_ancho` | 130/130 | 104/104 | 228/228 |
| `imagen_alto` | 130/130 | 104/104 | 228/228 |
| `terminos_andinos` | 0/130 | 104/104 | 228/228 |
| `terminos_textiles` | 0/130 | 104/104 | 205/228 |
| `consulta_origen` | 130/130 | 104/104 | 228/228 |
| `archivo_origen` | 130/130 | 104/104 | 228/228 |
| `fecha_descarga_metadatos` | 130/130 | 0/104 | 228/228 |
| `puntaje_aptitud` | 130/130 | 104/104 | 228/228 |
| `banda_sugerida` | 130/130 | 104/104 | 228/228 |
| `referencia_sugerida` | 130/130 | 104/104 | 228/228 |

## Campos obligatorios vacios

Se informan y no detienen el flujo: un valor que ninguna entrada registra no se completa (no se imputa).

Ninguno.

## estado_metadatos

| Valor | MET | CMA | AIC |
|---|---|---|---|
| completo | 102 | 81 | 137 |
| insuficiente | 0 | 0 | 42 |
| parcial | 28 | 23 | 49 |

## estado_imagen

| Valor | MET | CMA | AIC |
|---|---|---|---|
| util | 130 | 104 | 228 |

## estado_licencia

| Valor | MET | CMA | AIC |
|---|---|---|---|
| cc0 | 0 | 104 | 228 |
| dominio_publico | 130 | 0 | 0 |

## Imagenes compartidas entre registros

Misma `url_imagen` o mismo archivo de la copia de evaluacion (SHA-256). Se conservan: son objetos distintos del museo que comparten fotografia.

| Grupo | Registros |
|---|---|
| DUP-001 | MET:307964, MET:307965 |
| DUP-002 | MET:307966, MET:307967 |
| DUP-003 | MET:308036, MET:308106 |
| DUP-004 | CMA:165266, CMA:165267 |
| DUP-005 | AIC:2097, AIC:223218, AIC:223219, AIC:223220 |
| DUP-006 | AIC:85028, AIC:195555 |
| DUP-007 | AIC:85397, AIC:90831 |

## Criterios

- Registro de origen (`src/utils/fuentes.py`): candidatos de CMA y AIC; en MET, el inventario de la descarga de la API y, para la descripcion curada, las salidas base v2 (`config/corpus.toml` [met.base]). El valor del workbook tiene prioridad; el de origen lo completa si esta vacio. Ninguno se modifica.
- Imagen: copia de evaluacion de 1600 px (`ruta_imagen_local`, `imagen_sha256`, `imagen_ancho`, `imagen_alto`); `estado_imagen` usa el mismo lado minimo que el consolidado v1.
- `estado_anotacion` es `sin_anotar` en todos los registros: la anotacion estructural no se lee aqui.
