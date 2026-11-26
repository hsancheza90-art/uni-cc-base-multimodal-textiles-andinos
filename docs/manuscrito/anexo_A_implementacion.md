# Anexo A. Implementación y reproducibilidad

Este anexo reúne el detalle técnico de la implementación descrita en el capítulo 6: la estructura del código, los pasos que quedan fuera del flujo reproducible, las funciones de los sistemas y de la evaluación, el desglose de las pruebas automatizadas, el entorno y las órdenes con que se ejecutó la evaluación final. Las rutas son relativas a la raíz del repositorio.

## A.1 Estructura del código

El código está escrito en Python. Cada módulo ejecutable expone una función `main` y se invoca como `python -m src.paquete.modulo`; no se usan cuadernos interactivos. El punto de entrada del flujo reproducible es `python -m src.flujo`, y las pruebas se ejecutan con `python -m pytest`. El Cuadro A.1 resume la responsabilidad de cada paquete.

**Cuadro A.1.** Paquetes del código y su responsabilidad.

| Paquete | Responsabilidad |
|---|---|
| `collectors` | Recolección desde las interfaces públicas de MET, CMA y AIC (con red) |
| `preprocessing` | Filtros de evidencia textil y andina, normalización y estructura común de los libros de revisión |
| `metadata` | Construcción de las salidas de MET, auditorías y aplicación de la revisión manual de cada fuente |
| `imagenes` | Descarga de copias de evaluación, medidas de imagen, calibración y aplicación del puntaje de aptitud |
| `consolidado` | Esquema armonizado y construcción de los consolidados v1 y v2 |
| `anotacion` | Corpus principal v2, núcleo de anotación, libros de anotación, validación, acuerdo intra-anotador, revisión de criterios, condiciones de buena formación y congelación |
| `grupos` | Candidatos a duplicado y grupos de piezas relacionadas |
| `modelos` | Sistemas M0 a M4 y lectura de los vectores del codificador visual |
| `experimento` | Particiones, consultas, *rankings*, *pool* de juicios, selección de pesos, efecto mínimo detectable, sensibilidad, métricas y ejecución única de la evaluación final |
| `review` | Galerías HTML locales para la revisión visual |
| `utils` | Registro de fuentes, lectura de libros, lectura y escritura de archivos, configuración, vocabulario, métricas de acuerdo, fechas y texto |

La configuración se reparte en archivos TOML por ámbito, en `config/`: conteos esperados (`corpus.toml`), vocabulario controlado (`vocabulario.toml`), anotación (`anotacion.toml`), puntaje de aptitud (`aptitud.toml`, con el modelo calibrado en `aptitud_modelo.json`), grupos (`grupos.toml`), experimento (`experimento.toml`) y sistemas (`modelos.toml`). Una prueba automatizada comprueba que los parámetros numéricos de `experimento.toml` coinciden con los del protocolo experimental (`docs/protocolo_experimental_v2.md`).

## A.2 Flujo reproducible y pasos fuera del flujo

El punto de entrada `python -m src.flujo` ejecuta 27 pasos en un orden fijo, agrupados en las etapas del Cuadro A.2, y termina con una verificación de conteos contra `config/corpus.toml`. Si un paso devuelve un código distinto de cero, el flujo se detiene.

**Cuadro A.2.** Etapas del flujo reproducible.

| Etapa | Pasos | Insumos | Salidas principales |
|---|---|---|---|
| Curación por fuente | 1–6 | Candidatos de cada museo y libros de revisión | Subconjuntos principal, complementario y descartados de MET, CMA y AIC, con sus informes |
| Puntaje de aptitud | 7–9 | Medidas de imagen y decisiones del revisor | Modelo calibrado, puntaje por imagen e informe de calibración |
| Serie del primer avance | 10–13 | Copias congeladas y vocabulario congelado | Taxonomía, anotación v1, consolidado MET+CMA v1 y comparación de filtros |
| Corpus v2 y anotación | 14–18 | Subconjuntos revisados, huella perceptual (dHash), libros de grupos y de anotación | Principal v2, núcleo de anotación, grupos, consolidado v2, anotación exportada |
| Congelación | 19 | Copia congelada de la anotación v2.1 y sus sumas | Comprobación de que la exportación no cambió |
| Experimento de desarrollo | 20–26 | Particiones, consultas, características de M1, vectores de M2, juicios de desarrollo | Comprobación de fugas, *rankings* de desarrollo, *pool*, pesos de M4, efecto mínimo detectable, sensibilidad de la anotación, consultas T1 |
| Estabilidad de la anotación | 27 | Primera anotación y re-anotación del lote 1 | Informe de acuerdo intra-anotador |

**Cuadro A.3.** Pasos que se ejecutan fuera del flujo reproducible.

| Paso | Por qué queda fuera | Insumo versionado que escribe |
|---|---|---|
| Colectores de MET, CMA y AIC | Necesitan red | Listas de candidatos con los textos originales de la fuente |
| Descarga de copias de evaluación | Necesita red | Manifiesto de imágenes con sumas SHA-256 (las imágenes no se versionan) |
| Medidas de imagen y huella perceptual (dHash) | Necesitan las imágenes locales | Tablas de medidas y de dHash |
| Características de M1 | Necesitan las imágenes locales | Matriz de histogramas de color y textura con su índice |
| Vectores de M2 | Necesitan las imágenes y el modelo (unos 600 MB de dependencias) | Matriz de vectores, índice y manifiesto con las sumas de los pesos y las versiones |
| Generadores de libros (`--crear`) | Preparan el trabajo del revisor; conservan lo ya escrito | Libros de revisión, de anotación, de grupos, de consultas T1 y de juicios |
| Sorteo de particiones y consultas | Se ejecuta una sola vez | Particiones y consultas T3 |
| Congelación de la anotación | Se ejecuta una sola vez y se niega si hay pendientes | Copia congelada v2.1 y sus sumas |

Ninguno de los pasos del Cuadro A.3 sobrescribe un archivo con decisiones manuales salvo con la opción explícita `--forzar`.

**Vectores de M2.** Se calcularon con `python -m src.modelos.m2_openclip`, con el modelo `xlm-roberta-base-ViT-B-32` y los pesos `laion5b_s13b_b90k`, en CPU y con precisión fp32, porque la compilación de PyTorch con GPU no cargaba en el equipo disponible. El cálculo comprueba su propio determinismo: recalcula una muestra de 32 piezas y exige una diferencia máxima de $10^{-5}$ por componente entre pasadas. El manifiesto (`data/metadata/m2_openclip_manifiesto_v2.json`) registra las sumas SHA-256 de los archivos de pesos y las versiones de las bibliotecas, de modo que una ejecución posterior puede verificar que usa el mismo punto de control. Los vectores de texto de las consultas T1 se calcularon con la misma orden y la opción `--textos-t1`, solo después de la autorización del protocolo.

## A.3 Funciones de los sistemas y de la evaluación

Los sistemas están en `src/modelos/` (un módulo por sistema) y la evaluación en `src/experimento/evaluacion.py` (Cuadro A.4). Todas las funciones citadas son puras: no leen ni escriben archivos.

**M0** (`m0_texto.py`). BM25 de Okapi implementado sin bibliotecas de recuperación. El documento de cada pieza es la unión de los campos configurados en `config/modelos.toml`, normalizados a minúsculas y sin tildes; los términos son secuencias de letras y dígitos de al menos tres caracteres.

**M1** (`m1_vision.py`). Histogramas de color en CIELAB y de patrones binarios locales invariantes a la rotación, calculados con NumPy y Pillow sobre la máscara del textil. La disimilitud por bloque es la mitad de la distancia L1 entre histogramas normalizados, en $[0, 1]$.

**M2** (`m2_openclip.py`, `embeddings.py`). Lectura de los vectores congelados y similitud coseno entre vectores normalizados; el encuadre con relleno cuadrado, la arquitectura y los pesos se declaran en `config/modelos.toml`.

**M3** (`m3_estructura.py`). `reverso` (la reversión), `tramos` y `sin_lagunas` (tratamiento de las lagunas), `histograma_tipos` e `histograma_adyacencias`, `distancia_edicion` y `distancia_palabras` (distancia normalizada entre palabras, mínima entre una palabra y la otra o su reverso), `descriptor` (bloques y máscara de observabilidad), `distancias_por_bloque` y `comparar` (disimilitud mixta, cobertura y contribuciones de cada bloque). El argumento `sin_orden=True` de `comparar` produce el control M3-sin-orden. La función `canonizar`, que calcula la forma canónica, se usa solo en las pruebas de invariancia y de conteo de órbitas.

**M4** (`m4_fusion.py`). `normalizar` (mínimo y máximo por consulta), `pesos_efectivos` (reparto del peso de un componente sin evidencia), `fusionar` (puntuación y contribuciones), `posiciones_reciprocas` (variante M4-RRF, con $k = 60$), `rejilla` (enumeración de las combinaciones normalizadas de pesos) y `elegir` (regla de selección con sus criterios de desempate).

**Cuadro A.4.** Funciones de evaluación.

| Función | Qué calcula |
|---|---|
| `ndcg`, `precision`, `rango_reciproco` | nDCG@k, precisión y rango recíproco; un candidato sin juicio cuenta como 0 y un par `no_evaluable` se retira del *ranking* y del ideal |
| `proporcion_juzgada`, `sin_aportes_unicos` | Proporción juzgada del top k y métrica sin los pares que solo aportó un sistema |
| `diferencias`, `sin_empates` | Diferencias pareadas por consulta, excluidas las consultas sin relevantes; diferencias con $\lvert\Delta_q\rvert \le 10^{-12}$ tratadas como cero |
| `permutacion_pareada`, `error_monte_carlo` | Prueba de permutación por cambio de signo, bilateral, con réplicas y semilla fijas, y su error de Monte Carlo (H1) |
| `permutacion_exacta`, `p_minima` | p exacta por enumeración de los cambios de signo y p mínima alcanzable (H2) |
| `t_pareada`, `beta_incompleta` | t de Student pareada como comprobación, con la función beta incompleta regularizada |
| `intervalo_bootstrap` | Intervalo de percentiles por *bootstrap* pareado |
| `decidir`, `comparar`, `compuerta` | Regla de decisión de H1 y H2 y secuencia fija (H2 solo es confirmatoria si H1 se sostiene) |
| `efecto_minimo_detectable`, `consultas_necesarias`, `rango_desviacion` | Planificación de la potencia (capítulo 7, sección 7.8) |

## A.4 Pruebas automatizadas

La batería, en `tests/`, reúne 504 pruebas automatizadas en 21 archivos; 503 se ejecutan y una se omite por diseño, porque protege la apertura de la evaluación final ya autorizada. El Cuadro A.5 las agrupa por clase.

**Cuadro A.5.** Pruebas automatizadas por clase.

| Clase | Qué comprueba | Pruebas |
|---|---|---:|
| Regeneración | Que cada salida versionada se regenera idéntica, con finales LF, y que los conteos coinciden con la configuración; que una revisión con errores termina con código 1 sin reemplazar salidas; que los generadores no sobrescriben decisiones | 120 |
| Curación, aptitud y consolidados | Filtros de evidencia textil y andina, reglas y calibración del puntaje, esquema y construcción de los consolidados, colectores | 144 |
| Anotación | Validación de la anotación v1 y v2, estados de observación, condiciones de buena formación, revisión de criterios, congelación y grupos | 87 |
| Sistemas | Propiedades del descriptor y de la fusión: invariancia de la forma canónica, conteo de órbitas, simetría y cotas de la disimilitud, cota del control sin orden, contraejemplos de la desigualdad triangular, descomposición exacta, intervención, renormalización, posiciones recíprocas | 87 |
| Experimento y evaluación | Particiones y consultas sin fugas, coherencia del protocolo con la configuración y el código, métricas con ejemplos calculados a mano, contrastes estadísticos, selección de pesos, planificación de la potencia, sensibilidad y ejecución de la evaluación final: ensayo con desarrollo, sellado, fallos, cegamiento y revisión de H3 | 66 |

**Pruebas de aceptación.** Ocho pruebas, incluidas en la batería, comprueban los requisitos de la ejecución única (Cuadro A.6). En los comentarios del código figuran como pruebas T1 a T8; aquí se denominan PA1 a PA8 para no confundirlas con las tareas T1 y T3. Cada una puede comprender varias funciones de prueba.

**Cuadro A.6.** Pruebas de aceptación de la ejecución única.

| Prueba | Qué comprueba | Archivo |
|---|---|---|
| PA1 | Secuencia fija de H1 y H2: sin H1 sostenida, H2 no recibe un veredicto confirmatorio | `test_evaluacion.py` |
| PA2 | p exacta de H2 con $m$ diferencias distintas de cero entre ceros, frente a una enumeración independiente | `test_evaluacion.py`, `test_potencia.py` |
| PA3 | Regla de H1 con réplicas fijas: una mejora significativa menor que el umbral práctico no se confunde con una nula | `test_evaluacion.py` |
| PA4 | La alteración de un byte en un archivo sellado, un archivo sellado ausente o un manifiesto de otra corrida suspenden la corrida antes de producir métricas | `test_ejecucion_prueba.py` |
| PA5 | Una interrupción parcial no deja salidas ni hace avanzar el estado; el paso de los *rankings* exige todos los insumos y una segunda ejecución se rechaza | `test_ejecucion_prueba.py` |
| PA6 | La muestra de la revisión de H3 usa todos los casos si una clase tiene menos de cinco, y la ficha es ciega y se valida | `test_ejecucion_prueba.py` |
| PA7 | El libro de juicios es ciego de extremo a extremo, y un cambio en las reglas de juicio selladas se detecta | `test_ejecucion_prueba.py` |
| PA8 | Coherencia entre el protocolo, la configuración y el código | `test_experimento.py` |

**Verificación en copia limpia.** Antes de cada entrega se clona el repositorio en un directorio temporal, se instalan las dependencias fijadas, se ejecutan `python -m src.flujo` y `python -m pytest`, y se comprueba con `git status` que el árbol de trabajo queda sin cambios. Esa verificación detectó, por ejemplo, un informe que había quedado desactualizado tras incorporar juicios nuevos.

## A.5 Entorno y versiones

El flujo y las pruebas requieren Python 3.11 o superior y cuatro bibliotecas (Cuadro A.7). Las versiones exactas están fijadas en `requirements.txt` y los rangos compatibles en `pyproject.toml`; la verificación de referencia se hizo con Python 3.15.2.

**Cuadro A.7.** Dependencias del flujo y de las pruebas.

| Biblioteca | Versión fijada | Rango declarado |
|---|---|---|
| NumPy | 2.5.3 | ≥ 2.0 |
| openpyxl | 3.1.5 | ≥ 3.1 |
| Pillow | 12.3.0 | ≥ 10.1 |
| requests | 2.34.2 | ≥ 2.31 |

Las dependencias del codificador visual están en un archivo separado, `requirements-modelos.txt`, porque solo las necesita el cálculo de los vectores de M2, fuera del flujo. Las principales son PyTorch 2.15.0 (compilación para CPU), torchvision 0.29.2, open_clip_torch 3.3.0, transformers 5.22.1 y sentencepiece 0.2.3; el archivo fija también sus dependencias indirectas. PyYAML 6.0.3 se instala en su versión en Python puro (variable de entorno `PYYAML_FORCE_LIBYAML=0`), porque no publica una rueda para Python 3.15.

## A.6 Órdenes de la ejecución única

La evaluación final se ejecutó con el módulo `src/experimento/ejecucion_prueba.py`, cuyas órdenes son mutuamente excluyentes y se ejecutan en secuencia. Cada una escribe en archivos temporales y publica sus salidas al terminar, junto con el manifiesto de ejecución (`data/processed/experimento_v2_manifiesto_ejecucion.json`). Los estados y las fechas de la corrida están en el anexo B.

1. **`--comprobar`.** Verifica las condiciones de suspensión que pueden comprobarse en el repositorio, sin ejecutar ningún sistema. La primera es la autorización del protocolo: la sección `[ejecucion]` de `config/experimento.toml` registra la fecha y el *commit* de la autorización y la suma SHA-256 del protocolo, y la comprobación exige que el documento no haya cambiado después. Comprueba además las particiones y las consultas, la anotación congelada y sus condiciones de buena formación, los pesos de M4, las sumas de las imágenes de M1 y M2, la existencia de las consultas T1 y que la evaluación no se haya ejecutado antes.
2. **`--rankings`.** Una sola vez. Antes de calcular nada, exige todos los insumos y un árbol de trabajo sin cambios en archivos versionados, y escribe el manifiesto con el *commit*, las sumas SHA-256 de los insumos, la huella de las reglas de juicio, el punto de control de M2, los parámetros y el entorno (estado `insumos_sellados`). Después calcula los *rankings* de las 30 consultas de T3 y las 6 de T1 y el *pool*, y los sella (`rankings_sellados`). Los vectores de texto de T1 se calculan antes, con `python -m src.modelos.m2_openclip --textos-t1`, con el mismo codificador y la misma condición de autorización.
3. **`--crear-juicios`.** Crea los libros ciegos de T3 y de T1, con la misma estructura que los de desarrollo y una galería local por tarea, y conserva lo ya juzgado si se regeneran. Un validador comprueba, antes de entregarlos, que no contienen el sistema, la puntuación ni la posición, que conservan el orden sorteado y que su guía coincide con la rúbrica sellada.
4. **`--cerrar-juicios`.** Valida que los juicios estén completos y sin errores, repite la comprobación del cegamiento y sella los libros y su exportación (`juicios_cerrados`).
5. **`--crear-revision-h3`.** Sortea con semilla los aciertos y errores del top 10 de M4 y escribe las fichas ciegas de la revisión descriptiva, con su validador de campos.
6. **`--evaluar`.** Recalcula todas las sumas del manifiesto y, solo si coinciden, calcula H1 con sus tres afirmaciones y su error de Monte Carlo, H2 con su p exacta y la compuerta de H1, la reconstrucción y la intervención de H3, la cobertura y la sensibilidad del *pool*, las ablaciones, el control negativo, la robustez por museo y por completitud y las métricas descriptivas de T1, en un informe con la plantilla fijada en el protocolo (`outputs/reports/experimento_v2_resultados.md`) (`evaluada`).

Sin autorización registrada, `--rankings` termina con error y no escribe nada; una vez sellados los *rankings*, una segunda ejecución se rechaza.

## A.7 Correspondencia entre fórmula, implementación y prueba

Cada definición y propiedad del capítulo 5 tiene su contraparte en el código, y las propiedades **[P]** están fijadas en pruebas automatizadas que se ejecutan con cada cambio. El Cuadro A.8 permite comprobar esa correspondencia. Las funciones sin ruta están en `src/modelos/m3_estructura.py` (M3) o en `src/modelos/m4_fusion.py` (fusión); las pruebas sin ruta, en `tests/test_sistemas.py`.

**Cuadro A.8.** Correspondencia entre fórmula, función y prueba.

| Concepto | Fórmula | Función | Atributo o archivo | Prueba |
|---|---|---|---|---|
| Grupos | Def. 5.2 | `src/grupos/grupos.py` | `grupos_revision_v2.xlsx`; columna `grupo` | `tests/test_grupos.py` |
| Máscara | (5.3) | `valor`, `palabra_de_bandas`, `descriptor` | `[estados]` de `config/vocabulario.toml` | `test_disimilitud_mixta_simetrica_acotada_y_sin_evidencia` |
| Estados y buena formación | (5.2), sec. 5.4.1 | `validar_fila` en `src/anotacion/aplicar_anotaciones_v2.py`; `Campo.invalidos` en `src/utils/vocabulario.py` | `config/vocabulario.toml` | `tests/test_anotacion_v2.py` (B1, B2); `tests/test_buena_formacion.py` (B3 a B7, en `src/anotacion/buena_formacion.py`); B8, aviso de validación |
| Palabra, tramos y lagunas | (5.5), def. 5.10 | `palabra_de_bandas`, `tramos`, `sin_lagunas` | `secuencia_bandas`; símbolo `laguna` | `test_distancia_de_palabras_simetrica_invariante_y_con_lagunas_enmascaradas` |
| Reversión | $\rho$ | `reverso` | `secuencia_bandas` | `test_la_forma_canonica_es_invariante_a_la_reversion` |
| Forma canónica | (5.7) | `canonizar` | `secuencia_bandas` | La anterior |
| Conteo de órbitas | (5.9) | `canonizar` (enumeración) | — | `test_burnside_cuatro_posiciones_dos_simbolos_dan_diez_orbitas`; `test_el_numero_de_formas_canonicas_sigue_la_formula_de_burnside` |
| Contenido y orden | (5.10)–(5.11) | `histograma_tipos`, `canonizar` | `secuencia_bandas` | `test_un_mismo_histograma_de_tipos_reune_varias_formas_canonicas` |
| Distancia entre palabras | (5.12)–(5.13) | `distancia_edicion`, `distancia_palabras` | `secuencia_bandas` | `test_distancia_de_palabras_…`; `test_la_disimilitud_no_es_una_metrica` |
| Adyacencias | (5.14) | `histograma_adyacencias`, `distancia_l1_media` | `secuencia_bandas` | `test_el_control_sin_orden_no_distingue_lo_que_las_adyacencias_si` |
| Control sin orden | (5.15) | `histograma_tipos`; `comparar(..., sin_orden=True)` | `secuencia_bandas` | `test_m3_sin_orden_ignora_el_orden_de_las_bandas` |
| Cota del control | (5.16) | `distancias_por_bloque` | `secuencia_bandas` | `test_el_control_sin_orden_acota_inferiormente_la_distancia_con_orden` (enumeración exhaustiva) |
| Distancias por bloque | Sec. 5.8.4 | `nominal`, `distancias_por_bloque` | Atributos del Cuadro 5.3 | Las de $D$ |
| Disimilitud, cobertura y contribuciones | (5.17)–(5.19) | `comparar` | `[m3.pesos]` de `config/modelos.toml` | `test_disimilitud_mixta_…`; `test_la_suma_de_contribuciones_…` |
| Normalización por consulta | (5.20) | `normalizar` | — | `tests/test_m4.py` |
| Fusión y pesos efectivos | (5.21) | `fusionar`, `pesos_efectivos` | Rejilla del protocolo | `tests/test_m4.py` |
| Posiciones recíprocas | Sec. 5.10 | `posiciones_reciprocas` | — | `tests/test_m4.py` |

### Control de las condiciones de buena formación

El Cuadro A.9 detalla, para cada condición de la sección 5.4.1, qué la exige, cómo se controla y cuántas piezas la incumplen en la anotación congelada v2.1 (150 piezas). Las condiciones B3 a B7 se comprueban sobre la anotación final, después de las correcciones de la revisión de criterios, y no sobre los libros: la primera anotación podía incumplirlas antes de corregirse. La congelación se niega a escribir una copia que las incumpla, el flujo se detiene si la copia congelada las incumple, y el informe de la congelación da, para cada condición, las piezas que la incumplen.

**Cuadro A.9.** Condiciones de buena formación de la anotación y su control.

| | Condición | Por qué la necesita el capítulo 5 | Control | Incumplen en v2.1 |
|---|---|---|---|---|
| B1 | Todo valor pertenece al vocabulario del atributo o es un estado admitido, y un estado ocupa la celda completa | Definición 5.4 | Regla de validación | 0 |
| B2 | `eje_bandas` y `secuencia_bandas` concuerdan: las dos registran bandas o las dos un estado | Definición 5.9 | Regla de validación | 0 |
| B3 | Si las dos son un estado, es el mismo | Evita que una pieza sea `ausente` en una y `no_observable` en la otra | Regla de la congelación y del flujo | 0 |
| B4 | Una palabra contiene al menos un símbolo de $\Sigma$: no está formada solo por lagunas | Si no, $\tilde{w} = \varepsilon$ y «no se ve ninguna banda» se compararía como «no tiene bandas» ($d_w = 0$ frente a `ausente`) | Regla de la congelación y del flujo | 0 |
| B5 | No hay dos lagunas contiguas | Un tramo perdido es una sola laguna; así los tramos de la definición 5.10 son únicos | Regla de la congelación y del flujo | 0 |
| B6 | Si `composicion` es `bandas`, la secuencia no es `ausente` | Los dos atributos no pueden afirmar y negar las bandas a la vez | Regla de la congelación y del flujo | 0 |
| B7 | `motivos` es `ausente` si y solo si `familia_iconografica` lo es | Coherencia entre los dos bloques iconográficos | Regla de la congelación y del flujo | 0 |
| B8 | Ningún atributo del descriptor está vacío | Una celda vacía apaga el bloque sin que conste un juicio de no observación | Aviso de validación | 0 |
| B9 | Ninguna corrección de la revisión de criterios se aplica sin la firma del anotador | Una propuesta automática sin verificar no es anotación (capítulo 4, sección 4.10) | Condición de la congelación | 0 pendientes |
| B10 | La anotación describe la imagen de su registro | Definición 5.1: $a(r)$ es lo observado en $f(r)$ | Revisión manual de la identidad de las imágenes | 0 (ocho anotaciones desplazadas se trasladaron a su registro antes de congelar) |

### Casos admitidos en la palabra de bandas

En la versión 2.1, 53 piezas tienen palabra de bandas, 83 la tienen `ausente` y 14 no la tienen observada (11 `no_observable` y 3 `desconocido`). El Cuadro A.10 recoge las situaciones legítimas con las definiciones del capítulo 5 que no deben confundirse con incoherencias.

**Cuadro A.10.** Casos admitidos en las 53 palabras de bandas de la anotación v2.1.

| Caso | Piezas | Tratamiento |
|---|---|---|
| Palabra de una sola banda | 5 de 53 | Admitida. El bloque de adyacencias no es observable para esa pieza, y $d_w$ frente a otra palabra de una banda solo vale 0 o 1 |
| Dos bandas contiguas del mismo tipo | 21 de 53 | Admitida: una banda se delimita por un cambio de color **o** de diseño (definición 5.6), y la palabra no registra el color. La palabra no se comprime; su longitud cuenta bandas, no cambios de tipo |
| Palabra en una pieza cuya composición no es `bandas` | 19 de 53 | Admitida: una pieza de paneles o de campo central puede tener además franjas que cruzan la superficie (capítulo 4, sección 4.7.3) |
| Símbolo `no_determinada` en una palabra | 2 de 53 (3 símbolos) | Admitido como categoría residual (sección 5.4) |

Las palabras tienen entre 1 y 14 símbolos; la mitad tiene 3 o menos. Ninguna contiene una laguna.
