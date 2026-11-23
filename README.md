# Base multimodal de textiles andinos

Repositorio de la tesis «Estructuras combinatorias y representación multimodal en textiles andinos» (Maestría en Ciencias de la Computación, Universidad Nacional de Ingeniería). Reúne el corpus de textiles andinos prehispánicos de tres museos, la anotación de su organización visible, los sistemas de recuperación que se comparan y el experimento que los evalúa.

## Descripción

El corpus reúne fichas e imágenes de textiles andinos procedentes de colecciones de museo con licencia abierta. Cada registro conserva su enlace oficial, su licencia y la decisión humana que lo ubicó en su subconjunto. Todo lo que media entre la ficha original y el resultado de un experimento se regenera desde el código, sin acceso a la red.

## Fuentes

Tres museos con imágenes en dominio público o CC0 y una interfaz de programación pública: The Metropolitan Museum of Art (MET), Cleveland Museum of Art (CMA) y Art Institute of Chicago (AIC). El detalle de cada fuente y las fuentes descartadas están en `docs/fuentes.md`.

Los conteos por fuente y subconjunto (principal, complementario y descartados) están en un solo lugar, `config/corpus.toml`, que el flujo verifica en cada ejecución; cada cambio curatorial queda comentado allí con su fecha y su motivo. En los libros de revisión el subconjunto complementario se llama «secundario».

### Criterio de selección (v2)

Van al corpus principal los textiles cuyos colores y figuras se identifican a primera vista, estén completos o no; si además el textil está completo y se verifica en la fotografía, es una imagen de referencia. Complementario: la imagen no permite identificar bien colores o formas. Descarte: la pieza no es pertinente o la imagen no sirve (plumaria, muñecos, piezas posteriores a 1532, objetos no textiles o no andinos). El procedimiento, las medidas de imagen que lo apoyan y su validación están en `docs/protocolo_aptitud_v2.md`.

### Corpus consolidado v2 (MET, CMA y AIC)

El consolidado v2 (`data/processed/corpus_textiles_andinos_met_cma_aic_v2_consolidado.csv`, etiqueta `corpus-met-cma-aic-v2.0`) une el principal y el complementario de las tres fuentes con el esquema de la v1, la ficha de aptitud y el grupo de piezas relacionadas de cada registro. Resumen en `outputs/reports/corpus_textiles_andinos_met_cma_aic_v2_resumen.md`; esquema en `docs/esquema_consolidado_met_cma_aic_v2.md`.

### Anotación estructural v2.1

Un núcleo de 150 piezas del principal v2 tiene anotada su organización visible (composición, secuencia de bandas, borde, centro, simetría, repetición y motivos) con estados de observación. La versión 2.1 está congelada en `data/metadata/v2_1_congelado/` (etiqueta `anotacion-v2.1`) y es la base del descriptor estructural. Protocolo en `docs/protocolo_anotacion_v2.md`.

### Corpus consolidado MET+CMA v1 (congelado)

El respaldo del primer avance de tesis es el consolidado MET+CMA v1 (etiqueta `corpus-met-cma-v1.2`): 288 registros, con el esquema armonizado de los Cuadros 6.1 y 6.8 del primer avance. Se regenera idéntico desde copias congeladas de sus entradas (`data/metadata/v1_congelado/`), de modo que los cambios de la v2 no lo alteran.

| Archivo | Contenido |
|---|---|
| `data/processed/corpus_textiles_andinos_met_cma_v1_consolidado.csv` | Consolidado v1 |
| `data/processed/corpus_textiles_andinos_met_cma_v1_fuentes_licencias.csv` | Fuentes y licencias |
| `data/processed/corpus_textiles_andinos_met_cma_v1_sha256.txt` | Sumas SHA-256 |
| `data/metadata/imagenes_manifiesto_met_cma_v1.csv` | Manifiesto de imágenes |
| `docs/esquema_consolidado_met_cma_v1.md` | Esquema campo por campo |

## Experimento

El experimento compara, en una tarea de recuperación por ejemplar sobre el núcleo anotado, una búsqueda léxica sobre la ficha (M0), una medida de color y textura (M1), OpenCLIP congelado (M2), el descriptor estructural (M3) con su control sin orden (M3-sin-orden) y la fusión tardía de M0, M2 y M3 (M4), con su variante por posiciones recíprocas (M4-RRF). Las hipótesis, las particiones, los juicios de relevancia y la regla de decisión están en `docs/protocolo_experimental_v2.md`; el descriptor M3, en `docs/especificacion_m3.md`; las decisiones posteriores al protocolo, en `docs/registro_decisiones.md`. A la fecha solo se han ejecutado las consultas de desarrollo: el test espera la aprobación del protocolo.

## Instalación

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows (en Linux/macOS: source .venv/bin/activate)
pip install -r requirements-dev.txt
```

`requirements.txt` fija las versiones exactas con las que se verificó el flujo (Python 3.15.2); `pyproject.toml` declara los rangos compatibles (Python 3.11 o superior). Las dependencias del codificador visual (M2) están aparte, en `requirements-modelos.txt`: solo las necesita el cálculo de sus vectores, que queda fuera del flujo.

## Regenerar y verificar

Desde la raíz del repositorio, sin acceso a red:

```bash
python -m src.flujo     # regenera todas las salidas y verifica los conteos de config/corpus.toml
pytest                  # comprueba que la regeneración coincide con lo versionado (mismo texto, finales LF)
```

El flujo ejecuta 27 pasos:

1. Aplica la revisión manual de cada fuente (libros `data/metadata/*_revision_manual_v2.xlsx`).
2. Calibra el puntaje de aptitud con las decisiones del revisor y puntúa todas las imágenes.
3. Regenera la serie congelada del primer avance (consolidado v1).
4. Arma el corpus principal v2, el núcleo de anotación y los grupos de piezas relacionadas, y construye el consolidado v2.
5. Valida y exporta la anotación v2 y comprueba que coincide con la copia congelada v2.1.
6. En la parte experimental, solo sobre las consultas de desarrollo:
   - comprueba que no haya fugas entre particiones;
   - calcula los rankings de M0 a M4 y arma el conjunto de pares por juzgar;
   - informa la selección de pesos de M4, el efecto mínimo detectable y la sensibilidad del descriptor a la revisión de la anotación;
   - valida las consultas T1.
7. Mide el acuerdo intra-anotador.

El flujo termina con código distinto de cero si algún paso o conteo falla. Tras un cambio curatorial eso es lo esperado: se actualiza `config/corpus.toml` y se documenta el motivo.

## Trazabilidad del proceso

Cada fuente recorre la misma cadena, y cada eslabón deja un archivo versionado:

1. **Extracción.** El colector consulta la API del museo, aplica el filtro textil andino (`src/preprocessing/textile_filters.py`) y escribe la lista de candidatos con los textos originales de la fuente (`data/metadata/*_candidates.csv`; en MET, el corpus v1 congelado).
2. **Decisión.** El libro de revisión (`data/metadata/<fuente>_revision_manual_v2.xlsx`) es el único lugar donde se registran decisiones: `corpus_final`, `decision_revision`, `motivo_revision`, `revisor`, `fecha_revision` y `origen_curacion` (manual, regla automática documentada, validación ciega o revisión v2). Las reglas automáticas firman con `revisor = auto` y el revisor puede corregirlas; nunca se edita un CSV a mano.
3. **Aplicación.** El flujo lee cada libro y escribe un CSV por subconjunto y un resumen de movimientos (`outputs/reports/<fuente>_resumen_revision_manual_v2.md`).
4. **Etiquetas de imagen.** Las medidas de imagen y la ficha de aptitud (`data/metadata/aptitud_*_v2.csv`) apoyan la decisión con una justificación legible; no deciden por sí solas, salvo las reglas verificables (fotografía monocroma, resolución, sin imagen y pertinencia por metadatos). La tabla de trazabilidad de cada decisión está en `docs/protocolo_aptitud_v2.md`.
5. **Verificación.** `config/corpus.toml` fija los conteos; `pytest` comprueba que cada salida regenerada tiene el mismo texto que la versionada, con finales de línea LF; los libros se comparan por contenido (hojas, celdas, listas y formato), porque openpyxl guarda la fecha de creación dentro del archivo.

Las rutas de los archivos de cada fuente se definen una sola vez en `src/utils/fuentes.py`; los libros se leen siempre con `src/utils/libros.py` y los CSV e informes se escriben con `src/utils/archivos.py`.

## Pasos que requieren red o trabajo manual

Fuera del flujo, porque dependen de la red, de imágenes locales o de una decisión humana. Todos escriben insumos versionados y ninguno sobrescribe decisiones manuales sin `--forzar`.

```bash
# Recolección desde las API (por defecto escriben en data/raw/, fuera de git)
python -m src.collectors.cma_collector
python -m src.collectors.aic_collector

# Imágenes del consolidado v1 (manifiesto versionado; las imágenes no se versionan)
python -m src.imagenes.descargar_imagenes

# Puntaje de aptitud: copias de evaluación y medidas (ver docs/protocolo_aptitud_v2.md)
python -m src.imagenes.descargar_evaluacion
python -m src.imagenes.medidas
python -m src.imagenes.aptitud_workbooks --fuente aic          # ficha en el libro de AIC
python -m src.imagenes.aptitud_workbooks --fuente met --fuente cma --solo-reglas
python -m src.imagenes.validacion --crear | (sin opciones: evaluar) | --trasladar

# Anotación manual
python -m src.anotacion.workbook                 # crea o actualiza data/metadata/anotacion_met_cma_v1.xlsx (conserva lo anotado)
python -m src.anotacion.workbook --corpus v2     # crea o actualiza data/metadata/anotacion_v2.xlsx (núcleo y resto del principal v2)
python -m src.anotacion.workbook --corpus v2 --reanotacion   # re-anotación ciega del lote 1 (acuerdo intra-anotador)
python -m src.anotacion.revision_criterios --crear           # revisión de bandas y simetría en los lotes 2 a 5 (conserva lo escrito)
python -m src.anotacion.congelacion_v21 --congelar           # congela la anotación v2.1 (una sola vez; hecho el 2026-11-17)
python -m src.anotacion.acuerdo                  # acuerdo entre la primera anotación y la re-anotación

# Sistemas de recuperación (docs/protocolo_experimental_v2.md); dependencias opcionales:
#   pip install -r requirements-modelos.txt
python -m src.modelos.m1_vision                  # M1: color Lab y textura LBP del textil (solo numpy y Pillow)
python -m src.modelos.m2_openclip                # M2: vectores OpenCLIP de las copias de evaluación (CPU)

# Grupos de piezas relacionadas (unidad de partición del protocolo)
python -m src.imagenes.dhash_evaluacion          # dHash de las copias de evaluación (insumo versionado)
python -m src.grupos.workbook                    # crea o actualiza data/metadata/grupos_revision_v2.xlsx y la galería de pares

# Instantánea experimental (particiones y consultas T3; el flujo comprueba que no haya fugas)
python -m src.experimento.snapshot --crear       # una vez: no sobrescribe sin --forzar
python -m src.experimento.snapshot --reemplazar  # regla de reemplazo de consultas tras corregir la anotación
python -m src.experimento.consultas_t1 --crear   # libro de las consultas T1 (conserva lo escrito)
python -m src.experimento.juicios --crear        # libro ciego de juicios de desarrollo y su galería (conserva los juicios)

# Ejecución única del test (solo con el protocolo autorizado; ver docs/protocolo_experimental_v2.md, sección 9)
python -m src.experimento.ejecucion_prueba --comprobar           # condiciones de suspensión; no ejecuta nada
python -m src.modelos.m2_openclip --textos-t1                    # vectores de texto de las consultas T1
python -m src.experimento.ejecucion_prueba --rankings            # una sola vez: sella los insumos, luego rankings y pool
python -m src.experimento.ejecucion_prueba --crear-juicios       # libros ciegos de juicios de prueba (T3 y T1)
python -m src.experimento.ejecucion_prueba --cerrar-juicios      # valida y sella los juicios
python -m src.experimento.ejecucion_prueba --crear-revision-h3   # fichas ciegas de la revisión descriptiva de H3
python -m src.experimento.ejecucion_prueba --evaluar             # comprueba las huellas; H1 a H3, ablaciones y controles
# Cada estado se anota en docs/registro_custodia.md y sus huellas se envían al asesor.

# Galerías HTML de revisión (locales, no se versionan)
python -m src.review.galerias --fuente met     # una galería por decisión del libro (también cma o aic)
python -m src.imagenes.informe_aptitud         # una galería por banda de aptitud
```

## Estructura del repositorio

| Carpeta | Uso |
|---|---|
| `config/corpus.toml` | Conteos esperados por fuente y etapa, con el motivo de cada cambio |
| `config/vocabulario.toml` | Vocabulario controlado vigente; la serie v1 lee su copia congelada en `data/metadata/v1_congelado/` |
| `config/anotacion.toml` | Núcleo de anotación v2, cultura agrupada, capas, re-anotación, revisión de criterios, congelación y acuerdo intra-anotador |
| `config/aptitud.toml`, `config/aptitud_modelo.json` | Parámetros comentados del puntaje de aptitud y modelo calibrado |
| `config/grupos.toml` | Señales y umbrales de los candidatos a duplicado |
| `config/experimento.toml`, `config/modelos.toml` | Particiones, consultas, juicios y métricas del experimento; parámetros de M0 a M4 |
| `data/raw/` | Respuestas originales de las API; no se versiona |
| `data/images/` | Imágenes locales (consolidado y copias de evaluación); no se versiona |
| `data/processed/` | Corpus MET v1 congelado, consolidados v1 y v2, corpus principal y complementario v2, rankings y pool de desarrollo |
| `data/metadata/` | Candidatos, libros de revisión, anotación, grupos, consultas y juicios (decisiones humanas), subconjuntos revisados, medidas, puntajes y vectores de M1 y M2 |
| `data/metadata/v1_congelado/`, `data/metadata/v2_1_congelado/` | Entradas congeladas del consolidado v1 y anotación v2.1 congelada, con sus sumas |
| `data/historico/met_v1/` | Auditoría manual que formó el corpus MET v1 |
| `docs/` | Protocolos, especificaciones, registro de decisiones, revisión bibliográfica, manuscrito y documentos entregados al asesor |
| `outputs/reports/` | Informes generados por el flujo |
| `outputs/review/` | Galerías HTML locales (no se versionan) |
| `src/collectors/` | Recolección por fuente (CMA y AIC) |
| `src/preprocessing/` | Filtros, normalización y libros de revisión (estructura común y un generador por fuente) |
| `src/metadata/` | Construcción, auditoría y aplicación de la revisión manual |
| `src/imagenes/` | Descargas, medidas, calibración, ficha de aptitud y validación |
| `src/consolidado/` | Esquema armonizado y constructor de los consolidados |
| `src/anotacion/` | Corpus principal v2, núcleo de anotación, libros de anotación, validación, acuerdo, revisión de criterios y congelación |
| `src/grupos/` | Candidatos a duplicado y grupos de piezas relacionadas |
| `src/modelos/` | Sistemas M0 a M4 |
| `src/experimento/` | Particiones, consultas, rankings, juicios, pesos de M4, potencia, sensibilidad y métricas |
| `src/review/` | Galerías HTML de revisión |
| `src/utils/` | Registro de fuentes, lectura de libros, archivos, configuración, vocabulario, métricas de acuerdo, fechas, texto y HTTP |
| `src/flujo.py` | Punto de entrada único del flujo reproducible |
| `tests/` | Pruebas de reproducibilidad y de cada etapa |

## Documentación

| Documento | Propósito |
|---|---|
| `docs/README.md` | Índice de la documentación |
| `docs/manuscrito/` | Capítulos de la segunda parte de la tesis (borrador en Markdown) |
| `docs/protocolo_experimental_v2.md` | Experimento de recuperación estructural: hipótesis, galería, tareas, sistemas, particiones, juicios, métricas y criterios de suspensión |
| `docs/especificacion_m3.md` | Descriptor estructural M3: palabra de bandas, adyacencias, máscara de observabilidad, disimilitud mixta y sus propiedades |
| `docs/registro_decisiones.md` | Decisiones del investigador desde el 12-11-2026 (R01 a R39) |
| `docs/protocolo_anotacion_v2.md` | Anotación estructural: capas, bandas, estados, regla de los treinta segundos, núcleo y acuerdo intra-anotador |
| `docs/protocolo_aptitud_v2.md` | Criterio de selección v2, etapas, medidas, puntaje y validación |
| `docs/fuentes.md`, `docs/met_protocolo_fuente_v2.md`, `docs/cma_protocolo_fuente_v2.md` | Fuentes incluidas y descartadas; protocolo y cadena de curación por fuente |
| `docs/revision_bibliografica_2026-11/` | Revisión de alcance: búsqueda, 48 fichas de lectura, síntesis y referencias |
| `docs/revision_asesor_2026-11/`, `docs/informe_integrado_2026-11-08/`, `docs/auditoria_2026-10-20/` | Documentos entregados al asesor y recibidos de él |
| `docs/corpus/` | Ficha, protocolo, taxonomía, guía de anotación, trazabilidad y uso ético del consolidado v1; taxonomía vigente |
| `docs/esquema_consolidado_met_cma_v1.md`, `docs/esquema_consolidado_met_cma_aic_v2.md` | Esquemas de los consolidados (generados por el flujo) |
| `docs/historico.md` | Archivos retirados del repositorio y dónde recuperarlos |
| `docs/MCC701_05-07-2026.pdf` | Primer avance de tesis |

## Uso previsto

Investigación académica en ciencias de la computación: recuperación de imágenes de patrimonio textil, representación de la organización visible de los textiles y evaluación de sistemas con juicios humanos.

## Uso no previsto

No se recomienda usar este corpus para comercializar motivos patrimoniales, reproducir diseños textiles sin contexto, clasificar culturas de forma automática sin revisión humana, sostener interpretaciones históricas o rituales concluyentes sin validación experta, ni sustituir la investigación etnográfica, arqueológica o curatorial especializada (`docs/corpus/uso_etico_met_cma_v1.md`). Las piezas son de origen indígena y una parte procede de contextos funerarios; la licencia abierta de las imágenes no resuelve las cuestiones de gobernanza que plantean los principios CARE.

## Versiones

- `corpus-met-cma-v1.0`: primer consolidado MET+CMA (288 registros).
- `corpus-met-cma-v1.1`: MET:312615 a complementario; tipo de objeto, material y técnica normalizados con origen.
- `corpus-met-cma-v1.2`: vocabulario controlado, flujo de anotación, documentación del corpus y 9 registros MET pendientes. **Respaldo del primer avance.**
- `corpus-met-cma-aic-v2.0`: consolidado v2 MET+CMA+AIC (principal y complementario), curado con el criterio de aptitud analítica, con grupos de piezas relacionadas decididos por el revisor, licencias por fuente, manifiesto de imágenes y SHA-256 (`data/processed/corpus_textiles_andinos_met_cma_aic_v2_*`). Sin anotación estructural. Incluye las particiones y las consultas congeladas del protocolo experimental.
- `anotacion-v2.1`: anotación estructural del núcleo (150 piezas) congelada en `data/metadata/v2_1_congelado/`, con sus sumas SHA-256: re-anotación del lote 1, revisión de criterios de los lotes 2 a 5 y anotaciones trasladadas (decisiones R14 y R18 a R23). Es la base de M3 y de la fusión.

Versiones anteriores: `v1.0-corpus-met-textiles-andinos` (corpus MET v1 con notebooks) y `archivo/cma-v1` (primera curación CMA).
