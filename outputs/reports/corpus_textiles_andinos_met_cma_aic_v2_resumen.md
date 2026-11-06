# Corpus consolidado v2 (MET, CMA y AIC)

Resumen generado por `python -m src.flujo` (`src/consolidado/consolidado_v2.py`). Archivo: `data/processed/corpus_textiles_andinos_met_cma_aic_v2_consolidado.csv`; esquema en `docs/esquema_consolidado_met_cma_aic_v2.md`. La serie v1 (MET+CMA, 288 registros) sigue congelada en `corpus-met-cma-v1.2` y no cambia.

## Conteos

| Fuente | Principal | Complementario | Total |
|---|---|---|---|
| MET | 130 | 25 | 155 |
| CMA | 104 | 4 | 108 |
| AIC | 228 | 124 | 352 |
| Total | 462 | 153 | 615 |

## Grupos de piezas relacionadas

Decididos por el revisor (`data/metadata/grupos_v2.csv`, informe `outputs/reports/grupos_v2.md`). Un grupo reune registros del mismo objeto: misma foto, vistas, partes o fragmentos. En evaluaciones de recuperacion cuenta como un solo item.

| Registros por grupo | Grupos |
|---|---|
| 1 | 555 |
| 2 | 15 |
| 3 | 2 |
| 4 | 3 |
| 5 | 1 |
| 7 | 1 |

- Grupos: 577 para 615 registros; 1 reunen piezas del principal y del complementario.

## estado_metadatos

| Valor | MET | CMA | AIC |
|---|---|---|---|
| completo | 122 | 82 | 151 |
| insuficiente | 0 | 0 | 98 |
| parcial | 33 | 26 | 103 |

## estado_imagen

| Valor | MET | CMA | AIC |
|---|---|---|---|
| util | 155 | 108 | 352 |

## estado_licencia

| Valor | MET | CMA | AIC |
|---|---|---|---|
| cc0 | 0 | 108 | 352 |
| dominio_publico | 155 | 0 | 0 |

## banda_sugerida

| Valor | MET | CMA | AIC |
|---|---|---|---|
| descartar | 5 | 0 | 15 |
| principal | 89 | 91 | 151 |
| revisar | 42 | 17 | 92 |
| secundario | 19 | 0 | 94 |

## Cobertura de campos (registros con valor)

| Campo | MET | CMA | AIC |
|---|---|---|---|
| `id_global` | 155/155 | 108/108 | 352/352 |
| `fuente` | 155/155 | 108/108 | 352/352 |
| `id_fuente` | 155/155 | 108/108 | 352/352 |
| `numero_acceso` | 0/155 | 108/108 | 352/352 |
| `institucion` | 155/155 | 108/108 | 352/352 |
| `url_objeto` | 155/155 | 108/108 | 352/352 |
| `url_imagen` | 155/155 | 108/108 | 352/352 |
| `url_imagen_miniatura` | 155/155 | 0/108 | 352/352 |
| `ruta_imagen_local` | 155/155 | 108/108 | 352/352 |
| `titulo_original` | 155/155 | 108/108 | 352/352 |
| `titulo_es_sugerido` | 155/155 | 0/108 | 0/352 |
| `descripcion` | 29/155 | 53/108 | 43/352 |
| `cultura` | 155/155 | 108/108 | 258/352 |
| `periodo` | 0/155 | 0/108 | 0/352 |
| `fecha_objeto` | 155/155 | 108/108 | 347/352 |
| `procedencia` | 155/155 | 108/108 | 352/352 |
| `departamento` | 155/155 | 108/108 | 352/352 |
| `clasificacion_original` | 155/155 | 108/108 | 352/352 |
| `nombre_objeto_original` | 155/155 | 0/108 | 352/352 |
| `tipo_objeto` | 155/155 | 104/108 | 349/352 |
| `origen_tipo_objeto` | 155/155 | 104/108 | 349/352 |
| `tipo_superficie` | 30/155 | 0/108 | 352/352 |
| `material` | 155/155 | 0/108 | 259/352 |
| `material_normalizado` | 155/155 | 107/108 | 187/352 |
| `origen_material_normalizado` | 155/155 | 107/108 | 187/352 |
| `tecnica` | 0/155 | 108/108 | 40/352 |
| `tecnica_normalizada` | 123/155 | 87/108 | 347/352 |
| `origen_tecnica_normalizada` | 123/155 | 87/108 | 347/352 |
| `dimensiones` | 155/155 | 0/108 | 330/352 |
| `color_dominante` | 0/155 | 0/108 | 0/352 |
| `colores` | 0/155 | 0/108 | 0/352 |
| `contraste` | 0/155 | 0/108 | 0/352 |
| `densidad_visual` | 0/155 | 0/108 | 0/352 |
| `composicion` | 0/155 | 0/108 | 0/352 |
| `simetria` | 0/155 | 0/108 | 0/352 |
| `repeticion` | 0/155 | 0/108 | 0/352 |
| `borde` | 0/155 | 0/108 | 0/352 |
| `centro` | 0/155 | 0/108 | 0/352 |
| `motivos` | 0/155 | 0/108 | 0/352 |
| `familia_iconografica` | 0/155 | 0/108 | 0/352 |
| `motivo_principal` | 0/155 | 0/108 | 0/352 |
| `decision_curacion_final` | 155/155 | 108/108 | 352/352 |
| `motivo_curacion_final` | 155/155 | 20/108 | 352/352 |
| `decision_auditoria` | 155/155 | 108/108 | 352/352 |
| `motivo_auditoria` | 58/155 | 20/108 | 352/352 |
| `observacion_auditoria` | 58/155 | 20/108 | 91/352 |
| `categoria_revision` | 0/155 | 108/108 | 352/352 |
| `origen_curacion` | 155/155 | 108/108 | 352/352 |
| `estado_licencia` | 155/155 | 108/108 | 352/352 |
| `licencia_fuente` | 155/155 | 108/108 | 352/352 |
| `derechos_reproduccion` | 0/155 | 0/108 | 43/352 |
| `estado_metadatos` | 155/155 | 108/108 | 352/352 |
| `estado_anotacion` | 155/155 | 108/108 | 352/352 |
| `estado_imagen` | 155/155 | 108/108 | 352/352 |
| `observaciones` | 6/155 | 2/108 | 10/352 |
| `anotador` | 0/155 | 0/108 | 0/352 |
| `fecha_anotacion` | 0/155 | 0/108 | 0/352 |
| `observaciones_anotacion` | 0/155 | 0/108 | 0/352 |
| `grupo_imagen_duplicada` | 6/155 | 2/108 | 10/352 |
| `imagen_sha256` | 155/155 | 108/108 | 352/352 |
| `imagen_dhash` | 0/155 | 0/108 | 0/352 |
| `imagen_ancho` | 155/155 | 108/108 | 352/352 |
| `imagen_alto` | 155/155 | 108/108 | 352/352 |
| `terminos_andinos` | 0/155 | 108/108 | 352/352 |
| `terminos_textiles` | 0/155 | 108/108 | 272/352 |
| `consulta_origen` | 155/155 | 108/108 | 352/352 |
| `archivo_origen` | 155/155 | 108/108 | 352/352 |
| `fecha_descarga_metadatos` | 155/155 | 0/108 | 352/352 |
| `puntaje_aptitud` | 155/155 | 108/108 | 352/352 |
| `banda_sugerida` | 155/155 | 108/108 | 352/352 |
| `referencia_sugerida` | 155/155 | 108/108 | 352/352 |
| `grupo` | 155/155 | 108/108 | 352/352 |
| `tamano_grupo` | 155/155 | 108/108 | 352/352 |

## Criterios

- Principal y complementario: las decisiones de los workbooks de revision de cada fuente (en los workbooks, «secundario»). Los descartados no entran.
- Imagen: la copia de evaluacion de 1600 px (`ruta_imagen_local`), la misma sobre la que se anota; manifiesto en `data/metadata/imagenes_manifiesto_met_cma_aic_v2.csv` con su dHash.
- `grupo_imagen_duplicada` marca imagenes compartidas dentro de cada conjunto (`DUP-` en el principal, `DUPC-` en el complementario); las compartidas entre conjuntos quedan en el mismo `grupo`.
- `estado_anotacion` es `sin_anotar`: la anotacion estructural v2 se incorpora en la v2.1.
- Licencias: imagenes CC0 o de dominio publico en las tres fuentes; la descripcion de AIC es CC BY 4.0 y se cita (`data/processed/corpus_textiles_andinos_met_cma_aic_v2_fuentes_licencias.csv`).
