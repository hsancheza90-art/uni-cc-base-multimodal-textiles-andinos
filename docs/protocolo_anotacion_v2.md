# Protocolo de anotación estructural (corpus v2)

Procedimiento para anotar los atributos estructurales del corpus principal v2 (MET, CMA y AIC) y medir el acuerdo entre anotadores. La anotación es la entrada del descriptor combinatorio de la tesis (§7.3). La v1 (consolidado MET+CMA, etiqueta `corpus-met-cma-v1.2`) sigue con su guía: `docs/corpus/guia_anotacion_met_cma_v1.md`.

## Alcance

- **Corpus:** el principal v2, 462 piezas (`data/processed/corpus_textiles_andinos_v2_principal.csv`), construido por el flujo desde los tres principales revisados. Los conteos vigentes están en `config/corpus.toml`.
- **Núcleo de anotación:** una muestra estratificada de 150 piezas en cinco lotes de 30 (`data/metadata/nucleo_anotacion_v2.csv`). Es lo primero que se anota y la base para medir el acuerdo entre anotadores.
- **Resto:** las demás piezas del principal v2 están en el mismo workbook, en la hoja `fuera_del_nucleo`, para anotarlas más adelante con el mismo procedimiento.
- **Fuera de alcance:** la anotación describe lo que se ve. No interpreta el significado cultural de los motivos ni sustituye la revisión experta.

## Imagen sobre la que se anota

Se anota sobre la **copia de evaluación** de cada pieza: la imagen del museo llevada a 1600 px de lado mayor. Es la misma imagen sobre la que se midió la aptitud (`docs/protocolo_aptitud_v2.md`). La columna `imagen_local` del workbook abre esa copia y `url_imagen` abre la imagen del museo, por si hace falta ver más detalle.

## Unidad de observación

La unidad es el registro (`id_global`): un textil tal como aparece en su fotografía. Se anota lo visible en la imagen. Si un atributo no se puede observar (fragmento, imagen parcial), se deja vacío y se explica en `observaciones_anotacion`.

Algunos registros comparten fotografía (`grupo_imagen_duplicada`). Se anotan de forma coherente, y en las observaciones se indica a qué parte de la imagen corresponde cada uno.

## Capas

Cada pieza se anota en cinco capas y en este orden. Las capas fijan el orden de las columnas del workbook y están declaradas en `config/anotacion.toml` (`[[capas]]`).

| # | Capa | Campos |
|---:|---|---|
| 1 | Cromática | `color_dominante`, `colores`, `contraste`, `densidad_visual` |
| 2 | Estructural | `composicion`, `borde`, `centro` |
| 3 | Repetición y simetría | `repeticion`, `simetria` |
| 4 | Iconográfica | `motivos`, `familia_iconografica`, `motivo_principal` |
| 5 | Correcciones | `tipo_objeto_corregido`, `tipo_superficie_corregido`, `material_corregido`, `tecnica_corregida`, `estado_imagen_corregido` |

Los valores permitidos son los códigos de `config/vocabulario.toml`, que la hoja `vocabulario` del workbook lista con sus etiquetas. El criterio de cada atributo es el de la guía v1 (`docs/corpus/guia_anotacion_met_cma_v1.md`, «Criterios por atributo»).

- **Campos múltiples** (`colores`, `motivos`, `material_corregido`, `tecnica_corregida`): la lista desplegable muestra los códigos. Para registrar varios se escriben separados por `; ` (por ejemplo, `rojo; crema`).
- **Correcciones:** solo se llenan si el valor gris del workbook es incorrecto. Vacías significan «acepto el valor vigente».

## Regla de los treinta segundos

Si un atributo toma más de treinta segundos de duda, se deja vacío y la pieza se marca `revisar` en `estado_anotacion`. La duda se explica en `observaciones_anotacion`. La regla evita que el anotador fuerce un valor que no observa: un valor forzado entra al descriptor como si fuera un dato.

## Flujo de trabajo

1. Regenerar el corpus y el núcleo, y crear o actualizar el workbook:

   ```bash
   python -m src.flujo
   python -m src.anotacion.workbook --corpus v2
   ```

   El workbook `data/metadata/anotacion_v2.xlsx` conserva todo lo anotado por `id_global` al regenerarse, aunque la pieza haya pasado de una hoja a otra. Las anotaciones de piezas que ya no están en el corpus pasan a la hoja `fuera_del_corpus`.

2. Anotar en la hoja `anotacion` un lote por sesión, en el orden de las columnas `lote` y `orden`. Registrar `anotador` (nombre o iniciales) y `fecha_anotacion` (AAAA-MM-DD).

3. Hacer commit del workbook. Es el único lugar donde vive la anotación: nunca se edita un CSV a mano.

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

## Medición del acuerdo entre anotadores

Para estimar la consistencia de la anotación (§6.5.7 de la tesis), un segundo anotador anota el núcleo en una copia sin anotar del workbook v2: `data/metadata/anotacion_v2_evaluador2.xlsx`. Las dos rutas están declaradas en `config/anotacion.toml` (`[acuerdo]`). Después:

```bash
python -m src.anotacion.acuerdo
```

escribe `outputs/reports/anotacion_acuerdo_v2.md`, con una fila por atributo: n, acuerdo observado, acuerdo esperado, kappa y si alcanza el umbral de 0,6.

- **Emparejamiento:** las piezas se emparejan por `id_global`, y solo se comparan las anotadas por los dos (al menos una de las 17 columnas con valor). Dentro de cada atributo, una pieza que alguno dejó vacía o con un valor fuera del vocabulario sale de ese atributo y se cuenta.
- **Medida por tipo de atributo** (`[acuerdo.campos]`):

  | Tipo | Atributos | Medida |
  |---|---|---|
  | Nominal | `color_dominante`, `composicion`, `simetria`, `familia_iconografica`, `motivo_principal`, `tipo_objeto_corregido`, `tipo_superficie_corregido`, `estado_imagen_corregido` | Kappa de Cohen |
  | Ordinal | `contraste`, `densidad_visual`, `repeticion` | Kappa ponderado lineal, con el orden de `[acuerdo.orden]` |
  | Múltiple | `colores`, `motivos`, `material_corregido`, `tecnica_corregida` | Índice de Jaccard medio por pieza y kappa por etiqueta, que muestra qué código arrastra el desacuerdo |
  | Presencia | `borde`, `centro` | Kappa sobre sí/no, solo en las piezas que los dos marcaron observables; las marcadas `no_visible` se cuentan aparte |

- **Correcciones:** se comparan por su valor efectivo, es decir, la corrección o, si está vacía, el valor vigente del workbook.
- **Atributos no estimables:** si los dos anotadores usan una sola categoría, el acuerdo esperado es 1 y kappa no está definido. Se informa como «no estimable», con su motivo, nunca como 1 ni como 0.
- **Criterio:** kappa ≥ 0,6, el mismo que exige una fuente nueva en el puntaje de aptitud (acuerdo sustancial según Landis y Koch, 1977). Los kappa se calculan con numpy en `src/utils/metricas.py`.

## Pendiente

- El flujo valida contra el vocabulario el workbook v1, pero todavía no el v2; por ahora, el informe de acuerdo lista los valores fuera del vocabulario.
- La anotación v2 no se incorpora aún al corpus: se hará cuando el núcleo esté anotado y su acuerdo medido.
