# Corpus consolidado MET+CMA v1.0

Resumen generado por `python -m src.flujo` (`src/consolidado/construir_consolidado.py`).

## Conteos

| Fuente | Principal | Complementario | Total |
|---|---:|---:|---:|
| MET | 126 | 55 | 181 |
| CMA | 88 | 19 | 107 |
| Total | 214 | 74 | 288 |

## Cobertura de campos (registros con valor)

| Campo | MET | CMA |
|---|---:|---:|
| `id_global` | 181/181 | 107/107 |
| `fuente` | 181/181 | 107/107 |
| `id_fuente` | 181/181 | 107/107 |
| `numero_acceso` | 0/181 | 107/107 |
| `institucion` | 181/181 | 107/107 |
| `url_objeto` | 181/181 | 107/107 |
| `url_imagen` | 181/181 | 107/107 |
| `url_imagen_miniatura` | 181/181 | 0/107 |
| `ruta_imagen_local` | 180/181 | 107/107 |
| `titulo_original` | 181/181 | 107/107 |
| `titulo_es_sugerido` | 180/181 | 0/107 |
| `descripcion` | 49/181 | 50/107 |
| `cultura` | 181/181 | 107/107 |
| `periodo` | 0/181 | 0/107 |
| `fecha_objeto` | 181/181 | 107/107 |
| `procedencia` | 181/181 | 0/107 |
| `departamento` | 181/181 | 107/107 |
| `clasificacion_original` | 181/181 | 107/107 |
| `nombre_objeto_original` | 181/181 | 107/107 |
| `tipo_objeto` | 49/181 | 0/107 |
| `tipo_superficie` | 49/181 | 0/107 |
| `material` | 181/181 | 0/107 |
| `material_normalizado` | 49/181 | 0/107 |
| `tecnica` | 45/181 | 107/107 |
| `dimensiones` | 181/181 | 0/107 |
| `motivos` | 0/181 | 0/107 |
| `familia_iconografica` | 0/181 | 0/107 |
| `motivo_principal` | 0/181 | 0/107 |
| `decision_curacion_final` | 181/181 | 107/107 |
| `motivo_curacion_final` | 181/181 | 107/107 |
| `decision_auditoria` | 181/181 | 107/107 |
| `motivo_auditoria` | 1/181 | 107/107 |
| `observacion_auditoria` | 1/181 | 0/107 |
| `categoria_revision` | 132/181 | 107/107 |
| `origen_curacion` | 181/181 | 107/107 |
| `estado_licencia` | 181/181 | 107/107 |
| `licencia_fuente` | 181/181 | 107/107 |
| `derechos_reproduccion` | 0/181 | 0/107 |
| `estado_metadatos` | 181/181 | 107/107 |
| `estado_anotacion` | 181/181 | 107/107 |
| `estado_imagen` | 181/181 | 107/107 |
| `observaciones` | 6/181 | 2/107 |
| `grupo_imagen_duplicada` | 6/181 | 2/107 |
| `imagen_sha256` | 180/181 | 107/107 |
| `imagen_dhash` | 180/181 | 107/107 |
| `imagen_ancho` | 180/181 | 107/107 |
| `imagen_alto` | 180/181 | 107/107 |
| `terminos_andinos` | 0/181 | 107/107 |
| `terminos_textiles` | 0/181 | 107/107 |
| `consulta_origen` | 181/181 | 107/107 |
| `archivo_origen` | 181/181 | 107/107 |
| `fecha_descarga_metadatos` | 181/181 | 0/107 |

## estado_metadatos

| Valor | MET | CMA |
|---|---:|---:|
| completo | 45 | 0 |
| parcial | 136 | 107 |

## estado_imagen

| Valor | MET | CMA |
|---|---:|---:|
| no_disponible | 1 | 0 |
| util | 180 | 107 |

## estado_licencia

| Valor | MET | CMA |
|---|---:|---:|
| cc0 | 0 | 107 |
| dominio_publico | 181 | 0 |

Criterios:

- `estado_metadatos`: `insuficiente` si falta titulo, url_objeto, url_imagen, cultura, fecha_objeto o (material o tecnica); `completo` si ademas tiene material, tecnica y tipo_objeto normalizado; `parcial` en otro caso.
- Imagen compartida: registros con la misma `url_imagen`, el mismo archivo (SHA-256) o los mismos pixeles decodificados (`imagen_sha256_pixeles` del manifiesto).
- `estado_imagen`: `no_disponible` si la descarga fallo; `baja_resolucion` si el lado mayor mide menos de 500 px; `util` en otro caso.

## Imagenes compartidas entre registros

Los registros se conservan en el corpus: son objetos distintos del museo que comparten imagen. Deben tratarse como un solo item en evaluaciones imagen-imagen.

| Grupo | Registros | Titulos |
|---|---|---|
| DUP-001 | MET:307964, MET:307965 | Band Fragment; Band Fragment |
| DUP-002 | MET:307966, MET:307967 | Band Fragment; Band Fragment |
| DUP-003 | MET:308036, MET:308106 | Embroidered Mantle Fragment; Embroidered Fragment |
| DUP-004 | CMA:165266, CMA:165267 | Textile Fragments; Textile Fragment |

## Posibles duplicados visuales (dHash, distancia <= 4)

Pares con imagenes perceptualmente muy parecidas que no comparten archivo. Requieren revision manual.

| Registro A | Registro B | Distancia |
|---|---|---:|
| MET:312674 | MET:312676 | 3 |
| MET:312674 | MET:312678 | 4 |
| MET:312676 | MET:312677 | 4 |
| MET:312676 | MET:312681 | 3 |
| MET:312676 | MET:312683 | 4 |
| MET:312677 | MET:312680 | 3 |
| MET:312677 | MET:312683 | 2 |
| MET:312680 | MET:312681 | 4 |
| MET:312680 | MET:312683 | 1 |
| MET:312681 | MET:312683 | 3 |
| CMA:157111 | CMA:157112 | 0 |
