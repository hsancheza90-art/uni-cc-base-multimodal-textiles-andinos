# Inventario del estado del proyecto

Estado al 13 de noviembre de 2026. Responde al punto 1 del informe integrado del asesor. Cada elemento remite al archivo que lo contiene y al commit que lo introdujo. Los conteos vigentes del corpus se fijan en `config/corpus.toml` y el flujo los comprueba en cada ejecución; aquí se citan para identificar las unidades, no como fuente.

**Criterio de lectura.** La columna «Naturaleza de la evidencia» distingue tres niveles que no deben confundirse:

- **Software:** el artefacto existe, se regenera de forma determinista y lo verifican pruebas automáticas.
- **Medición:** hay un dato empírico obtenido con un procedimiento declarado (por ejemplo, la estabilidad de la anotación).
- **Contraste:** una hipótesis fue puesta a prueba conforme al protocolo. **Ningún elemento alcanza hoy este nivel.**

## 1. Unidades del corpus

Las cuatro cifras cuentan cosas distintas y no son intercambiables.

| Unidad | Cantidad | Qué cuenta | Archivo | Commit |
|---|---:|---|---|---|
| Decisiones curatoriales | 874 | Registros de museo revisados por el investigador, uno por ficha de la fuente (MET, CMA, AIC) | `data/metadata/*_revision_manual_v2.xlsx` | Revisión cerrada el 20-10-2026 |
| Registros utilizables | 615 | Decisiones con resultado principal (462) o complementario (153). Los 259 restantes se descartaron | `data/processed/corpus_textiles_andinos_met_cma_aic_v2_*` | `f3b0caf` |
| Grupos | 577 | Clases de registros que muestran un mismo objeto o partes de él, formadas por transitividad a partir de 100 pares decididos (65 unir, 35 separar) | `data/metadata/grupos_revision_v2.xlsx`; `outputs/reports/grupos_v2.md` | `f3b0caf` |
| Núcleo experimental | 150 piezas en 146 grupos | Registros del conjunto principal con anotación estructural; es la galería del experimento | `data/metadata/anotaciones_v2.csv` | `4ee20d3`, `d0bce67` |

Cada registro del conjunto principal tiene una fotografía de referencia, verificada por su suma SHA-256. «Pieza» designa en este proyecto el registro con su fotografía; el objeto físico puede corresponder a varios registros, y esa relación es la que recogen los grupos.

## 2. Versiones

| Versión | Contenido | Estado | Referencia |
|---|---|---|---|
| Corpus MET+CMA v1.2 | 288 registros del primer avance | Congelado; no se modifica | Etiqueta `corpus-met-cma-v1.2`; `data/metadata/v1_congelado/` |
| Corpus MET+CMA+AIC v2.0 | 615 registros, grupos, licencias, manifiesto de imágenes con SHA-256. **No contiene la anotación estructural** | Congelado | Etiqueta `corpus-met-cma-aic-v2.0` (`0143686`) |
| Anotación estructural v2.1 | 150 piezas, 19 atributos, con la guía y el vocabulario finales | **Sin congelar.** El lote 1 refleja la re-anotación (R14); los lotes 2 a 5 están por revisar con R12 y R16 | `data/metadata/anotaciones_v2.csv` (`d0bce67`) |
| Protocolo experimental | Versión 0.6.1 | Propuesto, sin aprobar | `docs/protocolo_experimental_v2.md` (`ba18dc3`) |

## 3. Diseño experimental fijado

| Elemento | Valor | Archivo | Commit | Naturaleza de la evidencia |
|---|---|---|---|---|
| Particiones por grupo | 44 grupos de desarrollo y 102 de prueba, estratificados por museo, con semilla fija | `data/metadata/particiones_v2.csv` | `0143686` | Software |
| Consultas T3 | 10 de desarrollo y 30 de prueba, sorteadas antes de calcular rankings; una sustituida por la regla de reemplazo (T3-P27) | `data/metadata/consultas_t3_v2.csv` | `0143686`, `d0bce67` | Software |
| Consultas T1 | 6, redactadas por el evaluador antes de ejecutar sistemas | `data/metadata/consultas_t1_v2.xlsx` | `8a826f8` | Software |
| Parámetros | Métrica, umbral, réplicas, semillas y tamaños de pool; una prueba comprueba que coinciden con el protocolo | `config/experimento.toml`; `tests/test_experimento.py` | `0143686`, `4dff235` | Software |

## 4. Sistemas

| Sistema | Qué es | Implementación | Rankings de desarrollo | Commit | Naturaleza de la evidencia |
|---|---|---|---|---|---|
| M0 | BM25 sobre el texto de la ficha, sin la descripción plantilla de MET | `src/modelos/m0_texto.py` | Sí | `75a281e` | Software |
| M1 | Histograma CIELAB y LBP sobre el textil segmentado | `src/modelos/m1_vision.py` | Sí | `75a281e` | Software |
| M2 | OpenCLIP congelado (`xlm-roberta-base-ViT-B-32`, pesos `laion5b_s13b_b90k`), fp32, CPU | `src/modelos/m2_openclip.py`; manifiesto en `data/metadata/m2_openclip_manifiesto_v2.json` | Sí | `c3d186a` | Software |
| M3 | Descriptor estructural con palabra de bandas, adyacencias y máscara | `src/modelos/m3_estructura.py`; `docs/especificacion_m3.md` | No: espera la anotación v2.1 | `75a281e` | Software |
| M3-sin-orden | Control: histograma de tipos, sin adyacencias | Mismo módulo (`sin_orden=True`) | No | `75a281e` | Software |
| M4 | Fusión tardía de M0, M2 y M3, y su variante por posiciones recíprocas | `src/modelos/m4_fusion.py` (funciones; sin conectar a los rankings) | No | `9f520f5` | Software |
| Evaluación | nDCG@10, P@10, MRR, proporción juzgada, permutación, t pareada, bootstrap, efecto mínimo detectable | `src/experimento/evaluacion.py` | — | `4dff235` | Software (datos sintéticos) |

## 5. Datos humanos

| Elemento | Estado | Archivo | Commit | Naturaleza de la evidencia |
|---|---|---|---|---|
| Anotación del núcleo | 150 de 150 piezas, un anotador | `data/metadata/anotacion_v2.xlsx` | `4ee20d3` | Medición |
| Re-anotación ciega del lote 1 | 30 de 30, con siete días de intervalo | `data/metadata/anotacion_v2_reanotacion.xlsx` | `d0bce67` | Medición |
| Estabilidad intra-anotador | `composicion` κ = 0,84; `eje_bandas` κ = 0,74; palabra de bandas idéntica en 17 de 24 piezas; `centro` κ = 0,49. Observabilidad inestable | `outputs/reports/anotacion_acuerdo_v2.md` | `d0bce67` | Medición (n = 30, un anotador) |
| Juicios de desarrollo | 345 de 345 pares, un evaluador; con una reserva sobre la aplicación de la rúbrica | `data/metadata/juicios_desarrollo_v2.csv` | `408362c` | Medición, bajo reserva |
| Juicios de prueba | No iniciados | — | — | — |

## 6. Reproducibilidad

| Elemento | Estado | Referencia |
|---|---|---|
| Flujo sin red | 23 pasos; termina sin hallazgos | `python -m src.flujo` |
| Pruebas automáticas | 429; comprueban, entre otras cosas, que lo regenerado coincide con lo versionado | `pytest` |
| Verificación en clon limpio | Antes de cada publicación en `main` | `README.md` («Regenerar y verificar») |
| Decisiones | D1 a D7 en el plan de cierre; R01 a R17 en el registro | `docs/plan_cierre_tesis.md`; `docs/registro_decisiones.md` |

## 7. Pendientes, en orden de dependencia

1. Aprobación del protocolo y ratificación de R01 a R04 y R10 (asesor).
2. Decisión sobre la reserva de los juicios de desarrollo (asesor e investigador).
3. Revisión de bandas y simetría en los lotes 2 a 5, decisión sobre `centro`, registro de adjudicaciones y congelación de la anotación v2.1 (investigador).
4. Rankings de M3 y de M3-sin-orden; conexión de M4; ampliación del pool de desarrollo y sus juicios.
5. Selección de pesos, efecto mínimo detectable para M4 frente a M2 y manifiesto de congelación.
6. Pool y juicios de prueba, incluido el segundo juicio parcial si se dispone de otra persona.
7. Ejecución única del test, resultados, ablaciones y control negativo.
8. Capítulos de resultados y discusión; traslado de la formalización al capítulo 5; cierre de la bibliografía.

## 8. Lo que no puede afirmarse todavía

- Que la estructura mejora la recuperación (H1) o que el orden de las bandas aporta (H2): no hay rankings de M3 ni de M4 y no se ha abierto el test.
- Que la explicación de M4 es fiel en los datos (H3): la reconstrucción y la intervención están verificadas como propiedades del código, no sobre resultados de prueba.
- Que la anotación es fiable entre personas: solo se midió la estabilidad de un anotador en 30 piezas.
- Que los juicios de desarrollo miden similitud estructural: la comprobación disponible no lo confirma.
