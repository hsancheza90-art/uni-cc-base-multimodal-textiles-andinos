# Taxonomía de atributos del corpus v2 (MET, CMA y AIC)

Documento generado desde `config/vocabulario.toml` por `src/anotacion/documentar_vocabulario.py`; no editar a mano. Para cambiar un valor, editar el vocabulario y ejecutar `python -m src.flujo`.

Es el vocabulario vigente, el que valida la anotación v2. La serie v1 conserva el suyo en `taxonomia_atributos_met_cma_v1.md`, generado desde la copia congelada `data/metadata/v1_congelado/vocabulario.toml`.

En la anotación v2, un atributo sin valor registra su **estado de anotación**, solo en la celda: `ausente` (la superficie pertinente se ve y el rasgo no está), `no_observable` (la superficie no se ve) o `desconocido` (se ve, pero el anotador no puede decidir). Cada atributo lista los estados que admite; una celda vacía significa «no anotado». Procedimiento: `docs/protocolo_anotacion_v2.md`.

La taxonomía sigue los Cuadros 6.3 a 6.8 del avance de tesis. En los datos se guarda el **código** (minúsculas, sin tildes ni espacios); la **etiqueta** es la forma usada en la tesis, los documentos y las figuras. Los valores marcados como *extensión del corpus* no figuran en la tesis y se agregaron durante la curación porque aparecen en los registros.

Los atributos contextuales (Cuadro 6.7: cultura, periodo, fecha, procedencia, fuente, institución, URL) provienen de la fuente oficial y no tienen vocabulario cerrado.

## Familia visual

Rasgos perceptibles en la imagen digital. Dependen de iluminación, fotografía, conservación y resolución, por lo que deben interpretarse con cautela.

### `color_dominante`

Color visualmente predominante (Cuadro 6.3 de la tesis; un solo valor; se registra en la anotación manual).

| Código | Etiqueta | Origen |
|---|---|---|
| `rojo` | rojo | tesis |
| `marron` | marrón | tesis |
| `crema` | crema | tesis |
| `negro` | negro | tesis |
| `azul` | azul | tesis |
| `amarillo` | amarillo | tesis |
| `verde` | verde | tesis |
| `multicolor` | multicolor | tesis |
| `no_observable` | no observable | estado de anotación |
| `desconocido` | desconocido | estado de anotación |

### `colores`

Lista breve de colores visibles (Cuadro 6.3 de la tesis; admite varios valores separados por `; `; se registra en la anotación manual).

| Código | Etiqueta | Origen |
|---|---|---|
| `rojo` | rojo | tesis |
| `marron` | marrón | tesis |
| `crema` | crema | tesis |
| `negro` | negro | tesis |
| `azul` | azul | tesis |
| `amarillo` | amarillo | tesis |
| `verde` | verde | tesis |
| `blanco` | blanco | extensión del corpus |
| `naranja` | naranja | extensión del corpus |
| `rosado` | rosado | extensión del corpus |
| `morado` | morado | extensión del corpus |
| `gris` | gris | extensión del corpus |
| `ocre` | ocre | extensión del corpus |
| `no_observable` | no observable | estado de anotación |
| `desconocido` | desconocido | estado de anotación |

### `contraste`

Diferencia visual entre zonas cromáticas (Cuadro 6.3 de la tesis; un solo valor; se registra en la anotación manual).

| Código | Etiqueta | Origen |
|---|---|---|
| `bajo` | bajo | tesis |
| `medio` | medio | tesis |
| `alto` | alto | tesis |
| `no_observable` | no observable | estado de anotación |
| `desconocido` | desconocido | estado de anotación |

### `densidad_visual`

Saturación de elementos visuales en la superficie (Cuadro 6.3 de la tesis; un solo valor; se registra en la anotación manual).

| Código | Etiqueta | Origen |
|---|---|---|
| `baja` | baja | tesis |
| `media` | media | tesis |
| `alta` | alta | tesis |
| `no_observable` | no observable | estado de anotación |
| `desconocido` | desconocido | estado de anotación |

## Familia composicional

Organización del diseño sobre la superficie. Conecta con el modelo combinatorio: composición, simetría, repetición, borde y centro.

### `composicion`

Organización general del diseño (Cuadro 6.4 de la tesis; un solo valor; se registra en la anotación manual).

| Código | Etiqueta | Origen |
|---|---|---|
| `bandas` | bandas | tesis |
| `campo_central` | campo central | tesis |
| `borde` | borde | tesis |
| `paneles` | paneles | tesis |
| `reticula` | retícula | tesis |
| `composicion_libre` | composición libre | tesis |
| `no_observable` | no observable | estado de anotación |
| `desconocido` | desconocido | estado de anotación |

### `simetria`

Organización simétrica o repetitiva (Cuadro 6.4 de la tesis; un solo valor; se registra en la anotación manual).

| Código | Etiqueta | Origen |
|---|---|---|
| `bilateral` | bilateral | tesis |
| `radial` | radial | tesis |
| `repeticion_modular` | repetición modular | tesis |
| `traslacional` | traslacional | tesis |
| `no_evidente` | no evidente | tesis |
| `no_observable` | no observable | estado de anotación |
| `desconocido` | desconocido | estado de anotación |

### `repeticion`

Presencia de patrones repetidos (Cuadro 6.4 de la tesis; un solo valor; se registra en la anotación manual).

| Código | Etiqueta | Origen |
|---|---|---|
| `si` | sí | tesis |
| `no` | no | tesis |
| `parcial` | parcial | tesis |
| `no_observable` | no observable | estado de anotación |
| `desconocido` | desconocido | estado de anotación |

### `borde`

Presencia de borde decorado (Cuadro 6.4 de la tesis; un solo valor; se registra en la anotación manual).

| Código | Etiqueta | Origen |
|---|---|---|
| `si` | sí | tesis |
| `no` | no | tesis |
| `no_visible` | no visible | tesis |
| `desconocido` | desconocido | estado de anotación |

### `centro`

Presencia de campo central diferenciado (Cuadro 6.4 de la tesis; un solo valor; se registra en la anotación manual).

| Código | Etiqueta | Origen |
|---|---|---|
| `si` | sí | tesis |
| `no` | no | tesis |
| `no_visible` | no visible | tesis |
| `desconocido` | desconocido | estado de anotación |

### `eje_bandas`

Orientación de las bandas en la fotografía; fija el eje de lectura de secuencia_bandas (no figura en la tesis; un solo valor; se registra en la anotación manual).

| Código | Etiqueta | Origen |
|---|---|---|
| `horizontal` | horizontal (se lee de arriba abajo) | extensión del corpus |
| `vertical` | vertical (se lee de izquierda a derecha) | extensión del corpus |
| `ausente` | ausente | estado de anotación |
| `no_observable` | no observable | estado de anotación |
| `desconocido` | desconocido | estado de anotación |

### `secuencia_bandas`

Palabra de bandas: el tipo de cada banda, en el orden del eje de lectura (no figura en la tesis; secuencia ordenada de valores separados por ` > `; se registra en la anotación manual).

| Código | Etiqueta | Origen |
|---|---|---|
| `lisa` | lisa | extensión del corpus |
| `geometrica` | geométrica | extensión del corpus |
| `figurativa` | figurativa | extensión del corpus |
| `mixta` | mixta | extensión del corpus |
| `no_determinada` | no determinada | extensión del corpus |
| `laguna` | laguna (tramo no observable) | extensión del corpus |
| `ausente` | ausente | estado de anotación |
| `no_observable` | no observable | estado de anotación |
| `desconocido` | desconocido | estado de anotación |

## Familia técnica

Materialidad, técnica y morfología. Parte proviene de los metadatos oficiales y parte se normaliza durante la curación.

### `material_normalizado`

Material normalizado desde los metadatos oficiales (Cuadro 6.5 de la tesis; admite varios valores separados por `; `; se registra en la anotación manual).

| Código | Etiqueta | Origen |
|---|---|---|
| `algodon` | algodón | tesis |
| `fibra_de_camelido` | fibra de camélido | tesis |
| `lana` | lana | tesis |
| `plumas` | plumas | tesis |
| `seda` | seda | extensión del corpus |
| `metal` | metal | extensión del corpus |
| `pelo_humano` | pelo humano | extensión del corpus |
| `fibra_vegetal` | fibra vegetal | extensión del corpus |
| `pigmento` | pigmento | extensión del corpus |
| `fibra_textil` | fibra textil | extensión del corpus |

### `tecnica_normalizada`

Técnica identificada desde los metadatos oficiales (Cuadro 6.5 de la tesis; admite varios valores separados por `; `; se registra en la anotación manual).

| Código | Etiqueta | Origen |
|---|---|---|
| `tejido` | tejido | tesis |
| `tapiz` | tapiz | tesis |
| `bordado` | bordado | tesis |
| `trabajo_con_plumas` | trabajo con plumas | tesis |
| `brocado` | brocado | extensión del corpus |
| `tela_doble` | tela doble | extensión del corpus |
| `pintado` | pintado | extensión del corpus |

### `tipo_objeto`

Tipo de textil u objeto textil (Cuadro 6.5 de la tesis; un solo valor; se registra en la anotación manual).

| Código | Etiqueta | Origen |
|---|---|---|
| `manto` | manto | tesis |
| `tunica` | túnica | tesis |
| `bolso_textil` | bolso textil | tesis |
| `panel_textil` | panel | tesis |
| `fragmento_textil` | fragmento | tesis |
| `tapiz_textil` | tapiz | tesis |
| `banda` | banda | extensión del corpus |
| `borde_textil` | borde | extensión del corpus |
| `borla_textil` | borla | extensión del corpus |
| `faja` | faja | extensión del corpus |
| `honda_textil` | honda | extensión del corpus |
| `mascara_textil` | máscara textil | extensión del corpus |
| `objeto_textil` | objeto textil | extensión del corpus |
| `sombrero_o_gorro` | sombrero o gorro | extensión del corpus |
| `sombrero_wari_iconografico` | sombrero wari iconográfico | extensión del corpus |
| `tela` | tela | extensión del corpus |
| `tocado` | tocado | extensión del corpus |
| `vestimenta_textil` | vestimenta | extensión del corpus |
| `vincha_textil` | vincha | extensión del corpus |

### `tipo_superficie`

Utilidad morfológica para análisis visual (Cuadro 6.5 de la tesis; un solo valor; se registra en la anotación manual).

| Código | Etiqueta | Origen |
|---|---|---|
| `superficie_amplia` | superficie amplia | tesis |
| `objeto_tridimensional` | objeto tridimensional | tesis |
| `formato_estrecho` | formato estrecho | tesis |
| `borde_o_fragmento_lineal` | borde o fragmento lineal | tesis |
| `revision_morfologica` | revisión morfológica | tesis |
| `objeto_tridimensional_iconografico` | objeto tridimensional iconográfico | extensión del corpus |
| `objeto_tridimensional_no_prioritario` | objeto tridimensional no prioritario | extensión del corpus |
| `materialidad_plumas` | materialidad de plumas | extensión del corpus |
| `fragmento_para_revision` | fragmento para revisión | extensión del corpus |

## Familia iconográfica

Motivos observables o registrados. Son descriptores preliminares, no interpretaciones definitivas.

### `motivos`

Motivos observables (Cuadro 6.6 de la tesis; admite varios valores separados por `; `; se registra en la anotación manual).

| Código | Etiqueta | Origen |
|---|---|---|
| `geometrico` | geométrico | tesis |
| `antropomorfo` | antropomorfo | tesis |
| `zoomorfo` | zoomorfo | tesis |
| `fitomorfo` | fitomorfo | tesis |
| `abstracto` | abstracto | tesis |
| `ausente` | ausente | estado de anotación |
| `no_observable` | no observable | estado de anotación |
| `desconocido` | desconocido | estado de anotación |

### `familia_iconografica`

Familia dominante de representación (Cuadro 6.6 de la tesis; un solo valor; se registra en la anotación manual).

| Código | Etiqueta | Origen |
|---|---|---|
| `geometrica` | geométrica | tesis |
| `figurativa` | figurativa | tesis |
| `mixta` | mixta | tesis |
| `abstracta` | abstracta | tesis |
| `no_determinada` | no determinada | tesis |
| `ausente` | ausente | estado de anotación |
| `no_observable` | no observable | estado de anotación |
| `desconocido` | desconocido | estado de anotación |

### `motivo_principal`

Motivo más visible o relevante (Cuadro 6.6 de la tesis; un solo valor; se registra en la anotación manual).

| Código | Etiqueta | Origen |
|---|---|---|
| `rombos` | rombos | tesis |
| `aves` | aves | tesis |
| `felinos` | felinos | tesis |
| `figuras_humanas` | figuras humanas | tesis |
| `serpientes` | serpientes | tesis |
| `escalonados` | escalonados | tesis |
| `no_determinado` | no determinado | tesis |
| `peces` | peces | extensión del corpus |
| `camelidos` | camélidos | extensión del corpus |
| `cruces` | cruces | extensión del corpus |
| `volutas` | volutas | extensión del corpus |
| `ausente` | ausente | estado de anotación |
| `no_observable` | no observable | estado de anotación |
| `desconocido` | desconocido | estado de anotación |

## Estados de control

Avance de curación y anotación; separan información oficial, anotación manual y revisión pendiente.

### `estado_metadatos`

Nivel de suficiencia de metadatos (Cuadro 6.8 de la tesis; un solo valor; lo asigna el flujo).

| Código | Etiqueta | Origen |
|---|---|---|
| `completo` | completo | tesis |
| `parcial` | parcial | tesis |
| `insuficiente` | insuficiente | tesis |

### `estado_anotacion`

Estado de revisión manual (Cuadro 6.8 de la tesis; un solo valor; se registra en la anotación manual).

| Código | Etiqueta | Origen |
|---|---|---|
| `sin_anotar` | sin anotar | tesis |
| `anotado_manual` | anotado manual | tesis |
| `revisar` | revisar | tesis |
| `corregido` | corregido | tesis |
| `descartado` | descartado | tesis |
| `anotado_asistido` | anotado asistido | extensión del corpus |

### `estado_imagen`

Estado de disponibilidad y utilidad visual (Cuadro 6.8 de la tesis; un solo valor; se registra en la anotación manual).

| Código | Etiqueta | Origen |
|---|---|---|
| `util` | útil | tesis |
| `baja_resolucion` | baja resolución | tesis |
| `no_disponible` | no disponible | tesis |
| `requiere_revision` | requiere revisión | tesis |

## Campos curatoriales y de licencia

Decisión de curación y condición de uso de cada registro.

### `decision_curacion_final`

Decisión final de curación (Cuadro 6.1 de la tesis; un solo valor; lo asigna el flujo).

| Código | Etiqueta | Origen |
|---|---|---|
| `principal` | principal | tesis |
| `complementario` | complementario | tesis |

### `estado_licencia`

Condición de uso, dominio público o licencia abierta (Cuadro 6.7 de la tesis; un solo valor; lo asigna el flujo).

| Código | Etiqueta | Origen |
|---|---|---|
| `dominio_publico` | dominio público | tesis |
| `cc0` | CC0 | tesis |
