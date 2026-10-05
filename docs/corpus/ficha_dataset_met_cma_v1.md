# Ficha del Corpus Multimodal de Textiles Andinos MET+CMA v1

## Identificación

| Campo | Valor |
|---|---|
| Nombre | Corpus Multimodal de Textiles Andinos MET+CMA |
| Serie | v1 (archivos con prefijo `corpus_textiles_andinos_met_cma_v1_`) |
| Entrega documentada | etiqueta git `corpus-met-cma-v1.2` |
| Autor | Henry Sánchez Alvarado |
| Asesor | César Lara Ávila |
| Institución | Universidad Nacional de Ingeniería, Maestría en Ciencias de la Computación |
| Repositorio | https://github.com/hsancheza90-art/uni-cc-base-multimodal-textiles-andinos |
| Fuentes | The Metropolitan Museum of Art (MET) y Cleveland Museum of Art (CMA) |

Cada entrega se congela con una etiqueta `corpus-met-cma-v1.N`. Las cifras de esta ficha corresponden a la entrega indicada; la verificación de integridad está en `data/processed/corpus_textiles_andinos_met_cma_v1_sha256.txt`.

## Descripción

El corpus reúne registros curatoriales, enlaces oficiales e imágenes de textiles andinos de dos colecciones museográficas con acceso abierto. Cada registro combina metadatos de la fuente, decisiones de curación documentadas, campos normalizados con vocabulario controlado y la información técnica de su imagen.

Está pensado como base de investigación para visión por computadora, recuperación imagen-texto y análisis computacional de patrones textiles. No es una descarga masiva: cada registro pasó por filtros automáticos y revisión manual.

## Contenido

| Fuente | Principal | Complementario | Total |
|---|---:|---:|---:|
| MET | 126 | 55 | 181 |
| CMA | 88 | 19 | 107 |
| **Total** | **214** | **74** | **288** |

- **Principal:** núcleo para los experimentos computacionales (textil andino con imagen útil y metadatos suficientes).
- **Complementario:** registros útiles para contraste, ampliación o revisión posterior (fragmentos, accesorios, *featherwork*, piezas con información incompleta).

### Cascada de curación

| Etapa | MET | CMA |
|---|---:|---:|
| Inventario base normalizado | 295 | 146 |
| Descartes iniciales automáticos | 84 | 8 |
| Conjunto evaluado | 211 | 138 |
| Principal tras revisión manual | 126 | 88 |
| Complementario tras revisión manual | 55 | 19 |
| Exclusiones curatoriales | 30 | 31 |
| Pendientes de revisión | 9 (de los 84 descartes iniciales) | 0 |

En MET, 126 + 55 + 30 = 211 evaluados. En CMA, 88 + 19 + 31 = 138 evaluados; los 39 registros de `cma_descartados_revisado.csv` suman las 31 exclusiones curatoriales y los 8 descartes automáticos.

Los 9 pendientes MET son registros que el filtro automático de la versión 1 excluyó por error y que el filtro corregido recupera; no forman parte del consolidado hasta su revisión visual (`outputs/review/met_pendientes_revision_v2_galeria.html`).

## Archivos

| Archivo | Contenido |
|---|---|
| `data/processed/corpus_textiles_andinos_met_cma_v1_consolidado.csv` | Corpus consolidado: 288 registros, 68 columnas |
| `data/processed/corpus_textiles_andinos_met_cma_v1_fuentes_licencias.csv` | Fuentes, políticas de acceso y conteos por fuente |
| `data/processed/corpus_textiles_andinos_met_cma_v1_sha256.txt` | Sumas SHA-256 de los archivos principales |
| `data/metadata/imagenes_manifiesto_met_cma_v1.csv` | URL descargada, SHA-256, dimensiones y hashes perceptuales de cada imagen |
| `data/metadata/anotaciones_met_cma_v1.csv` | Anotaciones manuales validadas |
| `docs/esquema_consolidado_met_cma_v1.md` | Esquema campo por campo |
| `docs/corpus/taxonomia_atributos_met_cma_v1.md` | Vocabulario controlado (códigos y etiquetas) |

Formato: CSV en UTF-8 sin BOM, separador coma, fin de línea LF. Los campos con varios valores usan `; ` como separador.

## Campos

El esquema sigue los Cuadros 6.1 y 6.8 del avance de tesis y se organiza en grupos:

- **Identificación:** `id_global` (`FUENTE:id_fuente`, único), `fuente`, `id_fuente`, `numero_acceso`, `institucion`.
- **Visual:** `url_objeto`, `url_imagen`, `url_imagen_miniatura`, `ruta_imagen_local`, `estado_imagen` y la información técnica de la imagen (`imagen_sha256`, `imagen_dhash`, dimensiones, `grupo_imagen_duplicada`).
- **Textual:** `titulo_original`, `titulo_es_sugerido`, `descripcion`.
- **Contextual:** `cultura`, `periodo`, `fecha_objeto`, `procedencia`, `departamento`, `estado_licencia`.
- **Estructural:** campos de la fuente (`clasificacion_original`, `nombre_objeto_original`, `material`, `tecnica`, `dimensiones`) y normalizados (`tipo_objeto`, `tipo_superficie`, `material_normalizado`, `tecnica_normalizada`).
- **Anotación (Cuadros 6.3, 6.4 y 6.6):** color, contraste, densidad visual, composición, simetría, repetición, borde, centro, motivos, familia iconográfica y motivo principal.
- **Curatorial y de control:** decisión y motivo de curación, decisión de auditoría, `estado_metadatos`, `estado_anotacion`, observaciones y trazabilidad (`archivo_origen`, `origen_curacion`).

Los valores de los campos categóricos son códigos del vocabulario controlado (`config/vocabulario.toml`). Los campos normalizados indican su procedencia en `origen_*`: `curacion` (decisión de la revisión manual), `regla` (normalización automática que debe validarse en la anotación) o `anotacion` (corrección manual).

## Estado actual

| Indicador | Valor |
|---|---|
| Imágenes descargadas y verificadas | 287 de 288 (MET:312615 no tiene imagen disponible en el museo) |
| Registros que comparten fotografía | 4 grupos de 2 registros (`grupo_imagen_duplicada`) |
| `estado_metadatos` | 234 completo, 54 parcial |
| `estado_anotacion` | 288 sin anotar (inicio de la anotación manual) |
| `tipo_objeto` normalizado | 49 por curación, 237 por regla, 2 sin determinar |

## Licencias y atribución

| Fuente | Condición | Campo de la fuente |
|---|---|---|
| MET | Dominio público, política Open Access de The Met | `isPublicDomain = True` en los 181 registros |
| CMA | CC0 | `share_license_status = CC0` en los 107 registros |

Las imágenes no se redistribuyen en el repositorio: se descargan desde las URL oficiales con `python -m src.imagenes.descargar_imagenes`. Toda publicación derivada debe citar la institución de origen de cada registro y este corpus.

## Uso previsto y no previsto

Uso previsto: investigación académica en visión por computadora, aprendizaje multimodal, recuperación imagen-texto, clasificación exploratoria y análisis de patrones textiles.

No se recomienda para comercializar motivos patrimoniales, clasificar culturas automáticamente sin revisión experta, ni presentar interpretaciones simbólicas como definitivas. Ver `docs/corpus/uso_etico_met_cma_v1.md`.

## Limitaciones

1. Depende de la información curatorial de dos instituciones; no representa la diversidad completa de los textiles andinos.
2. La atribución cultural de la fuente puede contener vacíos, generalizaciones o cambios de catalogación.
3. Las copias locales de MET son la versión web-large del museo (lado mayor de unos 600 px).
4. Los valores normalizados por regla (`origen_* = regla`) son aproximaciones que la anotación manual debe validar.
5. Cuatro grupos de registros comparten fotografía: en evaluaciones imagen-imagen deben tratarse como un solo ítem.
6. La disponibilidad de las imágenes depende de las políticas de cada museo y puede cambiar.

## Cómo reproducir

```bash
pip install -r requirements-dev.txt
python -m src.flujo     # regenera y valida el corpus sin acceso a red
pytest                  # verifica que la regeneración coincide con lo versionado
```
