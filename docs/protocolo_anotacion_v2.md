# Protocolo de anotación estructural (corpus v2)

Procedimiento para anotar los atributos estructurales del corpus principal v2 (MET, CMA y AIC) y medir la consistencia de la anotación. La anotación es la entrada del descriptor combinatorio de la tesis (§7.3). La v1 (consolidado MET+CMA, etiqueta `corpus-met-cma-v1.2`) sigue con su guía: `docs/corpus/guia_anotacion_met_cma_v1.md`.

## Alcance

- **Corpus:** el principal v2, 462 piezas (`data/processed/corpus_textiles_andinos_v2_principal.csv`), construido por el flujo desde los tres principales revisados. Los conteos vigentes están en `config/corpus.toml`.
- **Núcleo de anotación:** una muestra estratificada de 150 piezas en cinco lotes de 30 (`data/metadata/nucleo_anotacion_v2.csv`). Es lo primero que se anota; su lote 1 se re-anota para medir el acuerdo intra-anotador.
- **Resto:** las demás piezas del principal v2 están en el mismo workbook, en la hoja `fuera_del_nucleo`, para anotarlas más adelante con el mismo procedimiento.
- **Fuera de alcance:** la anotación describe lo que se ve. No interpreta el significado cultural de los motivos ni sustituye la revisión experta.

## Imagen sobre la que se anota

Se anota sobre la **copia de evaluación** de cada pieza: la imagen del museo llevada a 1600 px de lado mayor. Es la misma imagen sobre la que se midió la aptitud (`docs/protocolo_aptitud_v2.md`). La columna `imagen_local` del workbook abre esa copia y `url_imagen` abre la imagen del museo, por si hace falta ver más detalle.

## Unidad de observación

La unidad es el registro (`id_global`): un textil tal como aparece en su fotografía. Se anota lo visible en la imagen. Si un atributo no se puede observar (fragmento, imagen parcial), se registra el estado `no_observable` (ver «Estados») y se explica en `observaciones_anotacion`.

Algunos registros comparten fotografía (`grupo_imagen_duplicada`). Se anotan de forma coherente, y en las observaciones se indica a qué parte de la imagen corresponde cada uno.

## Estado de anotación

`estado_anotacion` es obligatorio en cada pieza anotada y admite un solo valor:

| Estado | Cuándo se usa |
|---|---|
| `anotado_manual` | El anotador decidió cada valor sin asistencia. Es el estado del núcleo (primera anotación, 5 de noviembre de 2026) y de la re-anotación. |
| `revisar` | La pieza tiene una duda que pide una segunda mirada (regla de los treinta segundos). |
| `corregido` | La pieza solo corrige valores vigentes. |
| `anotado_asistido` | Reservado (extensión del vocabulario): un asistente de IA propone los valores y el anotador revisa y decide cada uno. No se usa en el núcleo. Si se usa, el informe de acuerdo lo declara y la medida deja de ser un test-retest puro. |

La guía y el vocabulario no cambian hasta cerrar la re-anotación del lote 1, para que las dos pasadas usen los mismos criterios. Decisiones del revisor, 2026-11-05.

## Observaciones

`observaciones_anotacion` es texto libre. Lo que queda por decidir se marca con una etiqueta en mayúsculas, para poder contarlo sin leer cada nota:

| Etiqueta | Uso |
|---|---|
| `DUDA <atributo>` | Duda entre valores de un atributo (por ejemplo, `DUDA motivo_principal: ave o felino`). |
| `CRITERIO` | Un caso que la guía no resuelve y que conviene unificar (esquinas de borde, varias tiras en una foto, listados...). |
| `VOCAB` | Un hueco del vocabulario: el valor observado no tiene código. |

El informe de validación cuenta por lote las piezas con cada etiqueta. Las decisiones que piden se toman después de la re-anotación del lote 1 (ver «Estado de anotación»).

## Capas

Cada pieza se anota en cinco capas y en este orden. Las capas fijan el orden de las columnas del workbook y están declaradas en `config/anotacion.toml` (`[[capas]]`).

| # | Capa | Campos |
|---:|---|---|
| 1 | Cromática | `color_dominante`, `colores`, `contraste`, `densidad_visual` |
| 2 | Estructural | `composicion`, `eje_bandas`, `secuencia_bandas`, `borde`, `centro` |
| 3 | Repetición y simetría | `repeticion`, `simetria` |
| 4 | Iconográfica | `motivos`, `familia_iconografica`, `motivo_principal` |
| 5 | Correcciones | `tipo_objeto_corregido`, `tipo_superficie_corregido`, `material_corregido`, `tecnica_corregida`, `estado_imagen_corregido` |

Los valores permitidos son los códigos de `config/vocabulario.toml`, que la hoja `vocabulario` del workbook lista con sus etiquetas (también en `docs/corpus/taxonomia_atributos_v2.md`). El criterio de cada atributo es el de la guía v1 (`docs/corpus/guia_anotacion_met_cma_v1.md`, «Criterios por atributo»).

- **Campos múltiples** (`colores`, `motivos`, `material_corregido`, `tecnica_corregida`): la lista desplegable muestra los códigos. Para registrar varios se escriben separados por `; ` (por ejemplo, `rojo; crema`).
- **Correcciones:** solo se llenan si el valor gris del workbook es incorrecto. Vacías significan «acepto el valor vigente».

## Estados

La auditoría del asesor (informe 05) pide separar el valor de un atributo de su estado, para que el descriptor no confunda «no está» con «no se ve». Si un atributo no tiene valor, se escribe su estado, **solo en la celda** (nunca junto a otros códigos):

| Estado | Cuándo se usa |
|---|---|
| `ausente` | La superficie pertinente se ve y el rasgo no está (por ejemplo, una pieza sin bandas). |
| `no_observable` | La superficie pertinente no se ve: fragmento, recorte, pliegue o foto parcial. |
| `desconocido` | Se ve, pero el anotador no puede decidir (regla de los treinta segundos). |

- Cada atributo admite solo los estados que tienen sentido para él. La lista desplegable los muestra al final y la taxonomía los detalla (`docs/corpus/taxonomia_atributos_v2.md`). Los atributos cromáticos no admiten `ausente`.
- `borde` y `centro` conservan sus valores de la tesis: `no` equivale a ausente y `no_visible` a no observable; solo suman `desconocido`.
- `no_determinada` y `no_determinado` (familia y motivo principal) son valores de la tesis: se ve un motivo, pero no corresponde a ninguna categoría del vocabulario. `desconocido` es la duda del anotador entre categorías.
- Una celda vacía significa «no anotado», nunca «ausente».

Decisión del revisor, 2026-11-03.

## Bandas

`eje_bandas` y `secuencia_bandas` forman la palabra de bandas que lee el descriptor estructural (M3 del plan de cierre). Se anotan después de `composicion`:

1. **`eje_bandas`:** `horizontal` si las bandas cruzan la foto de lado a lado (se leen de arriba abajo) o `vertical` si van de arriba abajo (se leen de izquierda a derecha). El eje es el de la fotografía del museo, no el de uso de la pieza.
2. **`secuencia_bandas`:** el tipo de cada banda en el orden del eje, separados por ` > `. Por ejemplo, `lisa > geometrica > figurativa > geometrica > lisa`. Los tipos son `lisa` (un color, sin motivos), `geometrica`, `figurativa`, `mixta` y `no_determinada`.
3. **Lagunas:** un tramo que no se ve (rotura, pliegue, recorte) se escribe `laguna` en su lugar. El descriptor lo enmascara; no cuenta como una banda que se repite.
4. **Sin bandas:** si la pieza no tiene bandas, `eje_bandas` y `secuencia_bandas` van `ausente`.

No se registra el color de cada banda ni su ancho: el color ya está en la capa cromática y el ancho a ojo da una precisión aparente (decisiones del revisor, 2026-11-03). El sentido de lectura es una convención: el descriptor que se especifica en S2.5 del plan de cierre canonizará la palabra bajo inversión, para que leerla al revés no cambie la similitud entre piezas. El acuerdo intra-anotador, en cambio, compara las palabras tal como se escribieron.

## Regla de los treinta segundos

Si un atributo toma más de treinta segundos de duda, se anota `desconocido` y la pieza se marca `revisar` en `estado_anotacion`. La duda se explica en `observaciones_anotacion`. La regla evita que el anotador fuerce un valor que no observa: un valor forzado entra al descriptor como si fuera un dato.

## Flujo de trabajo

1. Regenerar el corpus y el núcleo, y crear o actualizar el workbook:

   ```bash
   python -m src.flujo
   python -m src.anotacion.workbook --corpus v2
   ```

   El workbook `data/metadata/anotacion_v2.xlsx` conserva todo lo anotado por `id_global` al regenerarse, aunque la pieza haya pasado de una hoja a otra. Las anotaciones de piezas que ya no están en el corpus pasan a la hoja `fuera_del_corpus`.

2. Anotar en la hoja `anotacion` un lote por sesión, en el orden de las columnas `lote` y `orden`. Registrar `estado_anotacion` (`anotado_manual`, `anotado_asistido`, `revisar` o `corregido`), `anotador` (nombre o iniciales) y `fecha_anotacion` (AAAA-MM-DD). Los tres son obligatorios en cada pieza anotada.

3. `python -m src.flujo` valida los dos workbooks v2 (`src/anotacion/aplicar_anotaciones_v2.py`) y exporta la primera anotación a `data/metadata/anotaciones_v2.csv`. Si hay errores (un valor fuera del vocabulario, un estado que el atributo no admite, control vacío, una fecha que no existe, o `eje_bandas` y `secuencia_bandas` que no concuerdan), el flujo termina con código 1 y no actualiza el CSV. El informe `outputs/reports/anotacion_v2_validacion.md` da solo conteos, sin valores ni observaciones por pieza, para no romper la re-anotación ciega; los errores sí se detallan. **Antes de re-anotar no se abre el CSV exportado**, porque tiene la primera anotación.

4. Hacer commit del workbook. Es el único lugar donde vive la anotación: nunca se edita un CSV a mano.

## Diseño de la muestra

Implementado en `src/anotacion/nucleo.py`, con los parámetros de `config/anotacion.toml` (`[nucleo]` y `[cultura]`). El informe `outputs/reports/nucleo_anotacion_v2.md` muestra cada estrato y la composición de cada lote.

1. **Cuota por fuente:** proporcional al principal v2 y repartida por el método de mayores restos. Con 462 piezas da MET 42, CMA 34 y AIC 74.
2. **Estratos dentro de cada fuente:** cultura agrupada por banda de aptitud (`banda_sugerida`). La cuota de la fuente se reparte entre los estratos en proporción a sus piezas, también por mayores restos. Si un estrato tuviera menos piezas que su cuota, el faltante se redistribuye entre los estratos de la misma fuente y el informe lo registra; con un reparto proporcional esto no ocurre, y queda como salvaguarda.
3. **Cultura agrupada:** el campo `cultura` de la fuente, normalizado, se compara con los términos de cada grupo (paracas, nasca, wari, chancay, inca, chimu).
   - Las culturas que no nombran ningún grupo van a `otras`; los registros sin cultura, a `sin_cultura`.
   - Los valores que nombran dos grupos se resuelven uno por uno en `[[cultura.casos]]`, con su motivo. Si aparece uno nuevo, el flujo falla en vez de elegir.
4. **Selección:** dentro de cada estrato se eligen las piezas con menor SHA-256 de «semilla:id_global». El resultado no depende de la versión de Python ni de numpy, y otra semilla (`--semilla`) cambia las piezas sin cambiar las cuotas.
5. **Lotes:** las piezas se reparten en turno entre los cinco lotes, ordenadas por fuente, banda y cultura, de modo que cada lote replica la composición del núcleo. El orden dentro de cada lote se mezcla con la semilla. Ningún lote puede tener más del 60 % de una fuente; si el reparto no lo permite, el núcleo falla con un mensaje en vez de entregar lotes sesgados.

La banda de aptitud es una sugerencia del modelo, no una decisión: todas las piezas están en el principal por decisión del revisor. La banda solo sirve para que el núcleo cubra imágenes de calidad distinta.

## Medición del acuerdo intra-anotador (test-retest)

No hay segundo anotador (plan de cierre, D1). Para estimar la consistencia de la anotación (§6.5.7 de la tesis), el mismo anotador vuelve a anotar a ciegas el lote 1 y se compara con su primera anotación. Mide la estabilidad de la anotación, no el acuerdo con otra persona: el informe lo declara como limitación. Decisión del revisor, 2026-11-03; parámetros en `config/anotacion.toml` (`[reanotacion]` y `[acuerdo]`).

1. Anotar el lote 1 en `data/metadata/anotacion_v2.xlsx`, con `fecha_anotacion` en cada pieza.
2. Al menos **7 días después** de esa fecha, anotar el workbook de re-anotación `data/metadata/anotacion_v2_reanotacion.xlsx`, sin abrir la primera anotación, sus notas ni `data/metadata/anotaciones_v2.csv`. El informe de validación indica desde qué fecha se puede empezar. Tiene solo las 30 piezas del lote 1, sin anotar y en otro orden (semilla propia). Si hubiera que regenerarlo, conserva lo ya re-anotado:

   ```bash
   python -m src.anotacion.workbook --corpus v2 --reanotacion
   ```

3. `python -m src.flujo` (o `python -m src.anotacion.acuerdo`) escribe `outputs/reports/anotacion_acuerdo_v2.md`, con una fila por atributo: n, acuerdo observado, acuerdo esperado, kappa y si alcanza el umbral de 0,6.

- **Plazo:** solo se comparan las piezas con al menos 7 días entre las dos fechas de anotación. Las que tienen menos o no tienen fecha se listan en «Piezas fuera de plazo» y no entran en ningún atributo.
- **Emparejamiento:** las piezas se emparejan por `id_global`, y solo se comparan las anotadas en las dos (al menos una de las 19 columnas con valor). Dentro de cada atributo, una pieza que alguna dejó vacía, con un valor fuera del vocabulario o con el estado `no_observable` o `desconocido` sale de ese atributo y se cuenta. `ausente` es una observación y se compara como un valor más.
- **Medida por tipo de atributo** (`[acuerdo.campos]`):

  | Tipo | Atributos | Medida |
  |---|---|---|
  | Nominal | `color_dominante`, `composicion`, `eje_bandas`, `simetria`, `familia_iconografica`, `motivo_principal`, `tipo_objeto_corregido`, `tipo_superficie_corregido`, `estado_imagen_corregido` | Kappa de Cohen |
  | Ordinal | `contraste`, `densidad_visual`, `repeticion` | Kappa ponderado lineal, con el orden de `[acuerdo.orden]` |
  | Múltiple | `colores`, `motivos`, `material_corregido`, `tecnica_corregida` | Índice de Jaccard medio por pieza y kappa por etiqueta, que muestra qué código arrastra el desacuerdo |
  | Presencia | `borde`, `centro` | Kappa sobre sí/no, solo en las piezas que las dos marcaron observables; las marcadas `no_visible` se cuentan aparte |
  | Secuencia | `secuencia_bandas` | Coincidencia exacta y similitud de edición media: 1 − d / máx(l₁, l₂), con d la distancia de Levenshtein. No tiene acuerdo esperado al azar definido, así que no se calcula kappa |

- **Correcciones:** se comparan por su valor efectivo, es decir, la corrección o, si está vacía, el valor vigente del workbook.
- **Atributos no estimables:** si los dos anotadores usan una sola categoría, el acuerdo esperado es 1 y kappa no está definido. Se informa como «no estimable», con su motivo, nunca como 1 ni como 0.
- **Criterio:** kappa ≥ 0,6, el mismo que exige una fuente nueva en el puntaje de aptitud (acuerdo sustancial según Landis y Koch, 1977). Los kappa se calculan con numpy en `src/utils/metricas.py`.
- **Con un segundo anotador**, si lo hubiera más adelante: se cambia `modalidad` y `anotador_b` en `[acuerdo]` y el mismo cálculo compara a las dos personas.

## Pendiente

- La anotación v2 se valida y se exporta (desde el 2026-11-05), pero no se incorpora aún al corpus: se hará cuando el acuerdo del lote 1 esté medido y se hayan decidido los criterios y el vocabulario que piden las observaciones.
