# Base Multimodal de Textiles Andinos

Repositorio académico para la construcción de una base multimodal de textiles andinos orientada a investigación en ciencias de la computación, visión por computadora, recuperación imagen-texto y análisis computacional de patrimonio textil.

## Descripción

Este proyecto organiza, cura y documenta registros textiles andinos procedentes de colecciones museográficas institucionales. El objetivo no es una descarga masiva de imágenes, sino un corpus trazable, revisable y metodológicamente defendible: cada registro conserva su enlace oficial, su licencia y la decisión humana que lo ubicó en su subconjunto, y todo lo que hay entre ambos extremos se regenera desde el código.

## Fuentes y estado

Tres museos con imágenes en dominio público o CC0 y API pública (detalle y fuentes descartadas en `docs/fuentes.md`):

| Fuente | Principal | Secundario | Descartados | Pendientes |
|---|---:|---:|---:|---:|
| The Metropolitan Museum of Art (MET) | 130 | 25 | 65 | 0 |
| Cleveland Museum of Art (CMA) | 104 | 4 | 38 | 0 |
| Art Institute of Chicago (AIC) | 228 | 124 | 156 | 0 |

Conteos del corpus v2 en curso al 2026-10-20. La fuente de verdad es `config/corpus.toml`: el flujo falla si un archivo no coincide, y cada cambio curatorial queda comentado allí con su fecha y motivo.

### Criterio de selección (v2)

Van al corpus principal los textiles cuyos colores y figuras se identifican a primera vista, estén completos o no; si además el textil está completo y se verifica en la fotografía, es una imagen de referencia para el estudio. Secundario: la imagen no permite identificar bien colores o formas. Descarte: no sirve o no es pertinente (plumaria, muñecos, piezas posteriores a 1532, objetos no textiles o no andinos). El procedimiento, las medidas de imagen que lo apoyan y su validación están en `docs/protocolo_aptitud_v2.md`.

### Corpus consolidado MET+CMA v1 (congelado)

El respaldo del primer avance de tesis es el consolidado MET+CMA v1 (etiqueta `corpus-met-cma-v1.2`): 288 registros, 214 en el principal y 74 en el complementario, con el esquema armonizado de los Cuadros 6.1 y 6.8. Se regenera idéntico desde copias congeladas de sus entradas (`data/metadata/v1_congelado/`), de modo que los cambios de la v2 no lo alteran.

| Archivo | Contenido |
|---|---|
| `data/processed/corpus_textiles_andinos_met_cma_v1_consolidado.csv` | Consolidado v1 |
| `data/processed/corpus_textiles_andinos_met_cma_v1_fuentes_licencias.csv` | Fuentes y licencias |
| `data/processed/corpus_textiles_andinos_met_cma_v1_sha256.txt` | Sumas SHA-256 |
| `data/metadata/imagenes_manifiesto_met_cma_v1.csv` | Manifiesto de imágenes |
| `docs/esquema_consolidado_met_cma_v1.md` | Esquema campo por campo |

## Instalación

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows (en Linux/macOS: source .venv/bin/activate)
pip install -r requirements-dev.txt
```

`requirements.txt` fija las versiones exactas con las que se verificó el flujo (Python 3.14); `pyproject.toml` declara los rangos compatibles (Python 3.11 o superior).

## Regenerar y verificar

Desde la raíz del repositorio, sin acceso a red:

```bash
python -m src.flujo     # regenera todas las salidas y verifica los conteos de config/corpus.toml
pytest                  # comprueba que la regeneración coincide byte a byte con lo versionado
```

El flujo aplica la revisión manual de cada fuente (workbooks `data/metadata/*_revision_manual_v2.xlsx`), calibra el puntaje de aptitud con las decisiones AIC, puntúa todas las imágenes, valida la anotación manual y construye el consolidado v1. Termina con código distinto de cero si algún paso o conteo falla; tras un cambio curatorial eso es lo esperado: se actualiza `config/corpus.toml` y se documenta el motivo.

## Pasos que requieren red o trabajo manual

Fuera del flujo, porque dependen de la red, de imágenes locales o de una decisión humana. Todos escriben insumos versionados y ninguno sobrescribe decisiones manuales sin `--forzar`.

```bash
# Recolección desde las API (por defecto escriben en data/raw/, fuera de git)
python -m src.collectors.met_collector_v2
python -m src.collectors.cma_collector
python -m src.collectors.aic_collector

# Imágenes del consolidado v1 (manifiesto versionado; las imágenes no se versionan)
python -m src.imagenes.descargar_imagenes

# Puntaje de aptitud: copias de evaluación y medidas (ver docs/protocolo_aptitud_v2.md)
python -m src.imagenes.descargar_evaluacion
python -m src.imagenes.medidas
python -m src.imagenes.aptitud_workbooks --fuente aic          # ficha en el workbook AIC
python -m src.imagenes.aptitud_workbooks --fuente met --fuente cma --solo-reglas
python -m src.imagenes.validacion --crear | (sin opciones: evaluar) | --trasladar
python -m src.imagenes.revision_v2 --crear | --trasladar     # revisión de MET y CMA con el criterio v2

# Anotación manual
python -m src.anotacion.workbook        # crea o actualiza data/metadata/anotacion_met_cma_v1.xlsx

# Galerías HTML de revisión (locales, no se versionan)
python -m src.review.build_met_gallery_v2 --root . --revisado
python -m src.review.build_met_gallery_v2 --root . --fuente aic
python -m src.imagenes.informe_aptitud
```

## Estructura del repositorio

| Carpeta | Uso |
|---|---|
| `config/corpus.toml` | Conteos esperados por fuente y etapa, con el motivo de cada cambio |
| `config/vocabulario.toml` | Vocabulario controlado (Cuadros 6.3 a 6.8 de la tesis) |
| `config/aptitud.toml`, `config/aptitud_modelo.json` | Parámetros comentados del puntaje de aptitud y modelo calibrado |
| `data/raw/` | Respuestas originales de las API; no se versiona |
| `data/images/` | Imágenes locales (consolidado y copias de evaluación); no se versiona |
| `data/processed/` | Corpus MET v1 congelado (entrada de MET v2) y consolidado MET+CMA v1 |
| `data/metadata/` | Candidatos, workbooks de revisión (decisiones humanas), subconjuntos revisados, medidas y puntajes de aptitud |
| `data/metadata/v1_congelado/` | Entradas del consolidado v1, idénticas a la etiqueta `corpus-met-cma-v1.2` |
| `data/historico/met_v1/` | Auditoría manual que formó el corpus MET v1 |
| `docs/` | Documentación metodológica, ética y de fuentes |
| `outputs/reports/` | Informes de curación, auditoría, calibración y validación |
| `outputs/review/` | Galerías HTML locales (no se versionan) |
| `src/collectors/` | Recolección por fuente |
| `src/preprocessing/` | Filtros, normalización y generadores de workbooks |
| `src/metadata/` | Construcción, auditoría y aplicación de la revisión manual |
| `src/imagenes/` | Descargas, medidas, calibración, ficha de aptitud y validación |
| `src/consolidado/` | Esquema armonizado y constructor del consolidado |
| `src/anotacion/` | Workbook de anotación, validación y taxonomía |
| `src/review/` | Galerías de revisión |
| `src/utils/` | Lectura y escritura de archivos, métricas, fechas, texto, HTTP y configuración |
| `src/flujo.py` | Punto de entrada único del flujo reproducible |
| `tests/` | Pruebas de reproducibilidad y de cada etapa |

## Documentación

| Documento | Propósito |
|---|---|
| `docs/fuentes.md` | Fuentes incluidas, extracción y fuentes descartadas |
| `docs/protocolo_aptitud_v2.md` | Criterio de selección v2, etapas, medidas, puntaje y validación |
| `docs/met_protocolo_fuente_v2.md`, `docs/cma/cma_source_protocol.md` | Protocolo y cadena de curación por fuente |
| `docs/corpus/` | Ficha, protocolo, taxonomía, guía de anotación, trazabilidad y uso ético del consolidado v1 |
| `docs/esquema_consolidado_met_cma_v1.md` | Esquema del consolidado (generado por el flujo) |
| `docs/notas_para_tesis.md` | Diferencias con el capítulo 6 del primer avance y material para la segunda parte |
| `docs/historico.md` | Archivos retirados del repositorio y dónde recuperarlos |
| `docs/MCC701_05-07-2026.pdf` | Primer avance de tesis |

## Uso previsto

Investigación académica en ciencias de la computación: visión por computadora aplicada a patrimonio textil, recuperación multimodal imagen-texto, clasificación exploratoria de objetos textiles, organización computacional de colecciones y desarrollo de descriptores visuales, composicionales e iconográficos.

## Uso no previsto

No se recomienda usar este corpus para comercializar motivos patrimoniales, reproducir diseños textiles sin contexto, clasificar culturas de forma automática sin revisión humana, sostener interpretaciones históricas o rituales concluyentes sin validación experta, ni sustituir la investigación etnográfica, arqueológica o curatorial especializada (`docs/corpus/uso_etico_met_cma_v1.md`).

## Versiones

- `corpus-met-cma-v1.0`: primer consolidado MET+CMA (288 registros).
- `corpus-met-cma-v1.1`: MET:312615 a complementario; tipo de objeto, material y técnica normalizados con origen.
- `corpus-met-cma-v1.2`: vocabulario controlado, flujo de anotación, documentación del corpus y 9 registros MET pendientes. **Respaldo del primer avance.**
- En curso: corpus v2 MET+CMA+AIC con el criterio de aptitud analítica; se congelará como `corpus-met-cma-aic-v2.0`.

Versiones anteriores: `v1.0-corpus-met-textiles-andinos` (corpus MET v1 con notebooks) y `archivo/cma-v1` (primera curación CMA).

## Contexto académico

Este repositorio forma parte de la tesis «Estructuras combinatorias y representación multimodal en textiles andinos», de la Maestría en Ciencias de la Computación de la Universidad Nacional de Ingeniería, orientada al estudio computacional de textiles andinos como objetos materiales, visuales, culturales y multimodales.
