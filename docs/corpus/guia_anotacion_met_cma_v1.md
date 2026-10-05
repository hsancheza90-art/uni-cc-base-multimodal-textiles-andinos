# Guía de anotación del corpus MET+CMA v1

## Propósito

Registrar de forma controlada atributos visuales, composicionales, técnicos e iconográficos observables en cada textil, para usarlos en los experimentos computacionales. La anotación describe lo que se ve; no interpreta el significado cultural de los motivos.

Los valores permitidos están en `docs/corpus/taxonomia_atributos_met_cma_v1.md`, generada desde `config/vocabulario.toml`.

## Flujo de trabajo

1. Regenerar el corpus y el workbook:

   ```bash
   python -m src.flujo
   python -m src.anotacion.workbook
   ```

   El workbook `data/metadata/anotacion_met_cma_v1.xlsx` tiene una fila por registro. Si ya existía, conserva todo lo anotado.

2. Anotar en la hoja `anotacion`:
   - Las columnas grises son contexto (título, cultura, tipo de objeto actual, enlaces al museo y a la imagen) y no se editan.
   - Las columnas amarillas se anotan con los **códigos** de la hoja `vocabulario`. Las de un solo valor tienen lista desplegable.
   - La columna `imagen_local` abre la copia descargada; `url_imagen`, la imagen del museo.

3. Validar e incorporar:

   ```bash
   python -m src.flujo
   ```

   El flujo valida cada valor contra el vocabulario y escribe `outputs/reports/anotacion_met_cma_v1_validacion.md`. Si hay errores, se detiene sin modificar el corpus e indica la fila y el valor a corregir.

4. Hacer commit del workbook y de los archivos regenerados.

## Reglas generales

- Anotar lo que se ve en la imagen. Si un atributo no se puede observar (imagen parcial, fragmento muy pequeño), dejarlo vacío y explicarlo en `observaciones_anotacion`.
- Los campos múltiples (`colores`, `motivos`, `material_corregido`, `tecnica_corregida`) llevan varios códigos separados por `; `, por ejemplo `rojo; crema; marron`.
- Se aceptan las etiquetas de la tesis con tildes (`marrón`): el flujo las convierte a códigos. Cualquier otro valor se rechaza.
- `fecha_anotacion` con formato `AAAA-MM-DD`; `anotador` con nombre o iniciales.
- Los registros con el mismo `grupo_imagen_duplicada` comparten fotografía: anotarlos de forma coherente y explicar en observaciones a qué parte de la imagen corresponde cada uno.

## Criterios por atributo

### Familia visual (Cuadro 6.3)

| Atributo | Criterio |
|---|---|
| `color_dominante` | Color que ocupa la mayor superficie del textil, sin contar el fondo de la fotografía. Usar `multicolor` si ningún color predomina claramente. |
| `colores` | Colores distinguibles a simple vista, hasta cinco, del más al menos extenso. |
| `contraste` | `alto` si las figuras se separan nítidamente del fondo; `bajo` si los tonos son cercanos o están desvaídos. |
| `densidad_visual` | `alta` si la superficie está casi cubierta por motivos; `baja` si predominan zonas lisas. |

Los colores dependen de la fotografía y la conservación: anotar el color percibido, no el original supuesto.

### Familia composicional (Cuadro 6.4)

| Atributo | Criterio |
|---|---|
| `composicion` | Organización general: `bandas` (franjas paralelas), `campo_central` (área central diferenciada), `borde` (decoración solo perimetral), `paneles` (compartimentos), `reticula` (cuadrícula regular), `composicion_libre`. |
| `simetria` | `bilateral` (eje espejo), `radial`, `repeticion_modular` (módulo que se repite con variaciones), `traslacional` (el mismo motivo desplazado), `no_evidente`. |
| `repeticion` | `si` si un motivo aparece repetido de forma regular; `parcial` si la repetición se interrumpe o solo se ve en parte. |
| `borde` | Borde decorado diferenciado; `no_visible` si la pieza está cortada y no se puede saber. |
| `centro` | Campo central diferenciado; `no_visible` si el fragmento no permite determinarlo. |

### Familia iconográfica (Cuadro 6.6)

| Atributo | Criterio |
|---|---|
| `motivos` | Tipos de motivo presentes: `geometrico`, `antropomorfo`, `zoomorfo`, `fitomorfo`, `abstracto`. |
| `familia_iconografica` | Representación dominante: `geometrica`, `figurativa`, `mixta` (geométrica y figurativa con peso similar), `abstracta`, `no_determinada`. |
| `motivo_principal` | Motivo más visible o recurrente. Usar `no_determinado` antes que adivinar. |

### Correcciones (Cuadro 6.5)

Las columnas `tipo_objeto_corregido`, `tipo_superficie_corregido`, `material_corregido`, `tecnica_corregida` y `estado_imagen_corregido` solo se llenan cuando el valor actual (columna gris) es incorrecto. Vacías, se conserva el valor actual. Una corrección reemplaza el valor en el corpus con `origen = anotacion`.

Revisar en especial los valores con `origen = regla` en el consolidado: provienen de reglas automáticas sobre el texto de la fuente.

## Estado de anotación (Cuadro 6.8)

| Código | Uso |
|---|---|
| `sin_anotar` | Valor por defecto. |
| `anotado_manual` | Se asigna automáticamente si hay atributos anotados y el estado está vacío. |
| `corregido` | Se asigna automáticamente si hay alguna corrección y el estado está vacío. |
| `revisar` | Dudas que requieren una segunda opinión. |
| `descartado` | El registro no se puede anotar (por ejemplo, imagen inutilizable); explicar el motivo. |

## Segunda evaluación

Para estimar la consistencia de la anotación (§6.5.7 de la tesis), una muestra del corpus debe anotarse por un segundo evaluador. Se recomienda que la muestra incluya ambas fuentes y ambos subconjuntos. Esa anotación se registra en una copia del workbook y se compara con la del primer evaluador antes de resolver discrepancias.
