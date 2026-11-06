# Plan de cierre de la tesis: cuatro semanas

Del lunes 26 de octubre al domingo 22 de noviembre de 2026. Plan de actividades para cerrar la segunda parte de la tesis (Seminario de Tesis II). Integra el plan que estaba en curso (hitos F2-H1 a F2-H3) con las observaciones de la auditoría del asesor del 20 de octubre de 2026 (carpeta `RevisionAsesor/auditoria`, en adelante «la auditoría»; los identificadores MET01, DAT01, SW01, etc., son los de su informe 09).

## Punto de partida (24 de octubre)

| Elemento | Estado | Observación de la auditoría |
|---|---|---|
| Corpus v1.2 (MET+CMA, 288 registros) | Congelado | Verificado; no se toca |
| Corpus v2 (MET+CMA+AIC) | 874 decisiones: 462 principal, 153 secundario, 259 descartados | Verificado; falta definir la unidad experimental (objeto, registro, imagen, grupo) |
| Puntaje de aptitud | Implementado y reproducible | Validación de desarrollo: escalado global, pliegues por registro, umbrales elegidos sobre las mismas predicciones. LOMO: AIC 0,563, MET 0,556, CMA 0,931 |
| Anotación estructural v2 | Núcleo de 150 piezas en 5 lotes (74 AIC, 42 MET, 34 CMA), workbook vacío, kappa implementado | Solo categorías globales: no registra el orden de las bandas ni el estado de observabilidad |
| Consultas y juicios de relevancia (qrels) | No existen | Bloquean la hipótesis central |
| Modelos M0–M4 | No existen (encargo OpenCLIP en pausa) | Bloquean la hipótesis central |
| Código | 208 pruebas en verde | Cinco fallos de contrato reproducidos (SW01–SW05); SW01, SW05 y SW08 siguen en `HEAD`, SW02 está resuelto en parte |
| Revisión bibliográfica | Mapeo parcial hecho por la auditoría: 64 registros, 4 con lectura completa | Falta búsqueda nativa y lectura propia; faltan Brownlow et al. (2015) y Ngo et al. (2021) |
| Capítulo 5 | Formalización extensa | Inconsistencias en 5.24–5.30 y 5.66; hipótesis 5.69–5.71 sin operacionalizar |
| Avance estimado por la auditoría | 32 % (rango 25–40 %); experimento central 0–5 % | Estimación orientativa, no nota oficial |

## Alcance que se compromete

**Objetivo de las cuatro semanas.** Un experimento de recuperación multimodal válido que aísle el aporte de la estructura combinatoria, más el informe de Seminario II que lo reporte, sea el resultado positivo o negativo. Corresponde al horizonte H1 de la auditoría.

**Pregunta.** En un conjunto congelado de textiles andinos fotografiados por museos, ¿añadir el orden de las bandas y las relaciones entre regiones a las señales textuales y visuales mejora la recuperación estructural juzgada por expertos, y permite explicar fielmente el ranking?

**Hipótesis que se contrastan** (redacción final en el protocolo experimental, semana 1):

1. *Primaria:* M4 (fusión con estructura) mejora nDCG@10 respecto de M2 (OpenCLIP congelado) en consultas estructurales.
2. *Mecanismo:* M3 con secuencia y adyacencias supera a M3 con los mismos atributos sin orden.
3. *Interpretabilidad:* la suma de contribuciones reconstruye el score y retirar un atributo cambia el ranking como predice la fórmula.

**Fuera del alcance de estas cuatro semanas** (la auditoría lo desaconseja antes de validar M0–M4): cuarta fuente (F2-H3), ajuste fino de modelos, GNN o hipergrafos, interfaz web, validación externa de la aptitud (APT02), SigLIP, DINO y kernels de grafos (EXT01).

## Decisiones previas (lunes 26 de octubre)

Sin ellas no se puede arrancar. Se registran en el protocolo experimental y en este plan.

| ID | Decisión | Opción recomendada | Decide |
|---|---|---|---|
| D1 | Segundo anotador y evaluadores de relevancia: quiénes y cuántas horas | Al menos una persona además del investigador; si no hay, el estudio se declara piloto (ver Riesgos) | Investigador y asesor |
| D2 | Papel del puntaje de aptitud en la tesis | Apoyo exploratorio de la curación, rotulado como desarrollo; no se corrige su validación (SW06–SW07) en estas cuatro semanas | Investigador y asesor |
| D3 | Ampliación del esquema de anotación | Agregar `secuencia_bandas` (eje de lectura documentado), anchos relativos y estado por atributo (observado, ausente, no_observable, desconocido) | Investigador y asesor |
| D4 | Galería del benchmark | El núcleo de 150 piezas, ya estratificado, después de agrupar duplicados | Investigador y asesor |
| D5 | Umbral práctico y métrica primaria | ΔnDCG@10 = 0,03; bootstrap pareado de 10 000 réplicas con semilla fija | Investigador y asesor |
| D6 | Nuevas dependencias para M2 (torch, open_clip) | Aprobarlas con versiones exactas y un checkpoint con licencia verificada | Investigador |
| D7 | Versionar `RevisionAsesor/` e integración continua (SW12) | Versionar la auditoría en `docs/`; CI después de la semana 4 | Investigador |

## Semana 1 (26 de octubre al 1 de noviembre): protocolo, esquema y contratos

| ID | Actividad | Referencia | Responsable | Entregable |
|---|---|---|---|---|
| S1.1 | Tomar las decisiones D1–D7 | Informe 12 | Investigador y asesor | Este plan actualizado |
| S1.2 | Subir el commit pendiente (`f450b2f`) tras verificarlo en un clon limpio | Plan anterior | Investigador | `main` al día |
| S1.3 | Redactar y congelar el protocolo experimental: tareas T1–T3, M0–M4, métricas, particiones por grupo, reglas de ajuste solo en desarrollo, criterios de suspensión del test | MET01, informe 08 | Investigador; aprueba el asesor | `docs/protocolo_experimental_v2.md` fechado |
| S1.4 | Corregir los contratos SW01, SW02 (ID vacío y no escribir si hay hallazgos), SW04 y SW05, cada uno con su prueba de regresión y sin cambiar ninguna salida versionada | Informe 06 | Investigador | Pruebas nuevas en verde |
| S1.5 | Corregir redacciones: «874 decisiones de procedencia manual y automática», no «874 revisiones manuales»; aptitud rotulada como desarrollo; «igualdad textual con LF» en lugar de «byte a byte» | APT01, SW08, informe 01 | Investigador | README, `notas_para_tesis.md`, `protocolo_aptitud_v2.md` |
| S1.6 | Ampliar el esquema de anotación v2 según D3 y regenerar el workbook v2 (está vacío) | ANN01, informe 05 | Investigador | `config/anotacion.toml`, protocolo de anotación y workbook actualizados |
| S1.7 | Detectar candidatos a duplicado: hashes exactos, dHash dentro y entre museos, vistas de un mismo objeto; preparar un workbook de grupos para la decisión humana | DAT02, F2-H1b | Investigador | Workbook de grupos con candidatos |
| S1.8 | Anotar el lote 1 (30 piezas) por el anotador 1 y medir el tiempo por pieza | ANN01 | Investigador | Lote 1 anotado |
| S1.9 | Búsquedas nativas en Scopus y Web of Science con acceso UNI; exportaciones guardadas | BIB01, informe 03 | Investigador | Exportaciones y cadenas literales |

**Puerta de salida:** protocolo aprobado por el asesor, esquema de anotación cerrado y lote 1 anotado.

## Semana 2 (2 al 8 de noviembre): datos congelados y anotación

| ID | Actividad | Referencia | Responsable | Entregable |
|---|---|---|---|---|
| S2.1 | Anotar el lote 1 por el anotador 2, medir el acuerdo antes de adjudicar y ajustar la guía | ANN01, F2-H2 | Anotador 2, investigador | `outputs/reports/anotacion_acuerdo_v2.md`; guía cerrada |
| S2.2 | Decidir las uniones de duplicados en el workbook de grupos y congelar el mapa de grupos | DAT02 | Investigador | Grupos decididos |
| S2.3 | Construir el consolidado v2 y el snapshot experimental: objetos, imágenes, grupos y particiones de desarrollo y prueba disjuntas por grupo; comprobación automática de ausencia de fugas | DAT01, F2-H1b | Investigador | Consolidado `_v2_`, `groups.csv`, `splits.csv`, etiqueta `corpus-met-cma-aic-v2.0` |
| S2.4 | Anotar los lotes 2 a 5 (anotador 1) | ANN01 | Investigador | 150 piezas anotadas |
| S2.5 | Especificar el descriptor M3: palabra de bandas canonizada bajo reversión, histograma de adyacencias, histograma sin orden (control), máscara de observabilidad y disimilitud mixta; pruebas de propiedades | MAT01, informe 05 | Investigador | Especificación y pruebas |
| S2.6 | Implementar M0 (BM25 sobre texto real; el crédito MET no entra como descripción, SW10) y M1 (color y textura con numpy y Pillow) | MOD01 | Investigador | Rankings de desarrollo reproducibles |
| S2.7 | Redactar las consultas: 10 a 12 de desarrollo y 30 a 40 de prueba, por familia estructural, sin mirar rankings | ANN02 | Evaluadores | `queries.csv` |
| S2.8 | Corregir el capítulo 5: separar elegibilidad de restricciones (5.24–5.30), retirar la suma de embeddings sin alineación (5.66), reformular 5.69–5.71 como hipótesis contrastables, Burnside y Pólya solo como fundamento | Informe 05 | Investigador | Capítulo 5 revisado |

**Puerta de salida:** acuerdo del piloto documentado, grupos y particiones congelados, consultas redactadas.

## Semana 3 (9 al 15 de noviembre): modelos congelados y juicios de relevancia

| ID | Actividad | Referencia | Responsable | Entregable |
|---|---|---|---|---|
| S3.1 | Implementar M2 (OpenCLIP congelado, checkpoint exacto), M3 con su control sin orden y M4 (fusión tardía de scores con pesos elegidos solo en desarrollo) | MOD01, MOD02 | Investigador | Rankings de desarrollo; descomposición exacta del score |
| S3.2 | Juicios de relevancia de desarrollo; medir el tiempo por juicio y fijar el tamaño final del test | ANN02 | Evaluadores | Qrels de desarrollo; tamaño del test decidido |
| S3.3 | Congelar los sistemas: manifiesto de ejecución con commit, hashes de insumos, checkpoint, parámetros, hardware y semilla | Informe 08 | Investigador | `run_manifest.json` |
| S3.4 | Generar el pool de prueba (primeros 10 de cada sistema, más muestra aleatoria y positivos propuestos por el experto) y obtener juicios ciegos dobles en escala 0–3, con adjudicación posterior | ANN02 | Evaluadores | `qrels.csv` de prueba sellado |
| S3.5 | Redactar los capítulos 3 (estado del arte con el mapeo bibliográfico, Brownlow y Ngo) y 4 (datos y anotación: versiones, grupos, acuerdo) | BIB01, informe 11 | Investigador | Borradores |

**Puerta de salida:** sistemas congelados y test sellado; ningún ajuste se hizo con datos de prueba.

## Semana 4 (16 al 22 de noviembre): evaluación, informe y reproducción

| ID | Actividad | Referencia | Responsable | Entregable |
|---|---|---|---|---|
| S4.1 | Ejecutar el test una sola vez: nDCG@10 por consulta, diferencia pareada M4–M2 con intervalo de confianza, métricas secundarias | EXP01 | Investigador | `metrics_by_query.csv` y tablas T5 |
| S4.2 | Ablaciones (sin estructura, sin texto, sin orden, sin color), robustez por museo y calidad, análisis de errores | EXP01 | Investigador | Tablas T6 y T7; panel de errores |
| S4.3 | Evaluar la fidelidad de la explicación: reconstrucción del score, intervención sobre atributos y revisión ciega de una muestra | Informe 08 | Investigador y evaluadores | Tabla T8 |
| S4.4 | Completar el documento de uso ético con el contexto funerario y los principios CARE | F2-H2, informe 07 | Investigador | Documento de uso ético v2 |
| S4.5 | Redactar resultados, discusión, conclusiones por objetivo y limitaciones del informe de Seminario II | Informe 11 | Investigador | Informe II completo |
| S4.6 | Matriz de respuesta al asesor: observación, acción, evidencia y estado | Auditoría | Investigador | Matriz entregada |
| S4.7 | Verificar en un clon limpio (flujo, pruebas, árbol limpio) y entregar el paquete para que el asesor lo reproduzca | REP01 | Investigador; reproduce el asesor | Etiqueta de entrega |

**Puerta de salida:** el asesor reproduce los resultados y cada conclusión enlaza a un resultado real.

## Cobertura de las observaciones de la auditoría

| ID | Observación | Dónde se atiende |
|---|---|---|
| MET01 | Congelar protocolo, métricas y comparadores | S1.3 |
| DAT01, DAT02 | Unidades, duplicados y snapshot v2 | S1.7, S2.2, S2.3 |
| ANN01 | Anotación estructural y acuerdo | S1.6, S1.8, S2.1, S2.4 |
| ANN02 | Consultas y qrels independientes | S2.7, S3.2, S3.4 |
| MAT01 | Descriptor y propiedades formales | S2.5, S2.8 |
| MOD01, MOD02 | M0–M4 | S2.6, S3.1, S3.3 |
| EXP01 | Evaluación, ablaciones, robustez | S4.1–S4.3 |
| REP01 | Informe y paquete reproducible | S4.5–S4.7 |
| BIB01 | Revisión bibliográfica | S1.9, S3.5 |
| APT01 | Rotular la aptitud como desarrollo | S1.5 |
| SW01, SW02, SW04, SW05 | Contratos de código | S1.4 |
| SW08 | «Byte a byte» | S1.5 |
| SW10 | Crédito MET como descripción | S2.6 (no entra al índice textual) |
| SW06, SW07 | Validación agrupada de la aptitud | Diferido si D2 confirma uso exploratorio |
| SW03 | Caché de medidas | Diferido: solo afecta si se vuelve a medir |
| SW09, SW11, SW12 | Reintentos POST, escritura atómica, CI | Diferido a después de la semana 4 |
| APT02, EXT01, PUB01 | Validación externa, modelos alternativos, publicación | Horizontes H2 y H3 |

## Correspondencia con el plan anterior

| Plan anterior | Destino en este plan |
|---|---|
| Anotar el núcleo (usuario) | Se mantiene, con el esquema ampliado (S1.6) y doble anotación del lote 1 (S2.1) |
| F2-H1b: consolidado v2, imágenes AIC, fragmentos entre museos, etiqueta v2.0 | S1.7, S2.2 y S2.3 |
| F2-H2: acuerdo entre anotadores y contexto funerario | S2.1 y S4.4 |
| Encargo de línea base multimodal (OpenCLIP), en pausa | Se retoma como M2 dentro del protocolo (S3.1) |
| F2-H3: cuarta fuente | Postergada a H2 |
| Embeddings OpenCLIP como medidas de aptitud | Postergado; la aptitud queda como apoyo exploratorio |

## Carga estimada de anotación y juicios

Son supuestos para planificar; se reemplazan por tiempos medidos en las semanas 1 y 3.

| Tarea | Volumen | Supuesto | Horas |
|---|---|---|---:|
| Anotación del núcleo (anotador 1) | 150 piezas | 4 min por pieza | 10 |
| Doble anotación del piloto (anotador 2) | 30 piezas | 4 min por pieza | 2 |
| Juicios de prueba con pooling, por evaluador | 35 consultas × unos 40 candidatos = 1400 pares | 30 s por juicio | 12 |
| Juicios de desarrollo, por evaluador | 10 consultas × 40 candidatos = 400 pares | 30 s por juicio | 3,5 |

La evaluación exhaustiva (150 piezas × 35 consultas = 5250 pares por evaluador, unas 44 horas) no cabe en cuatro semanas; por eso se usa pooling y se reporta la proporción juzgada, como recomienda la auditoría.

## Riesgos y contingencias

| Riesgo | Señal | Respuesta |
|---|---|---|
| No hay segundo anotador o evaluador | D1 sin respuesta al cierre de la semana 1 | Declarar el estudio como piloto con un solo evaluador y documentarlo como limitación; no inventar un test sintético |
| El acuerdo del piloto es bajo | Kappa bajo en atributos críticos en S2.1 | Reducir atributos ambiguos antes de anotar los lotes 2–5 |
| Los juicios superan la capacidad | Tiempo por juicio medido en S3.2 | Reducir consultas de prueba antes de abrir el test, nunca después |
| Sin GPU para M2 | S3.1 | Checkpoint compacto en CPU y registro de tiempos |
| M4 no mejora a M2 | S4.1 | Se reporta igual: con un diseño válido, una hipótesis no confirmada es un resultado de maestría |
| El calendario institucional exige otra estructura | Sílabo o rúbrica de Seminario II | Contrastar con el asesor en S1.1 |

**El test no se abre** si quedan grupos duplicados repartidos entre particiones, qrels derivados del descriptor o de CLIP, cambios de guía sin registrar, pesos ajustados con datos de prueba o imágenes sin verificar (informe 10).

## Seguimiento

Al cierre de cada semana se marca aquí el estado de cada actividad (hecho, en curso, diferido) y se registra cualquier cambio de alcance con su fecha y motivo. Los conteos del corpus siguen viviendo solo en `config/corpus.toml`.

### Cierre de la semana 1 (3 de noviembre)

La puerta de salida de la semana 1 no se cruzó.

| ID | Estado |
|---|---|
| S1.1 | En curso: D1 decidida (abajo); D2–D7 pendientes con el asesor |
| S1.2 | En curso: cinco commits locales por subir (`f450b2f` y los cuatro del 26 de octubre) |
| S1.3 | No iniciada |
| S1.4 | Hecho (26 de octubre) |
| S1.5 | Hecho (26 de octubre) |
| S1.6 | Hecho (3 de noviembre): ver D3 abajo |
| S1.7 | No iniciada |
| S1.8 | No iniciada: la pieza llenada el 22 de octubre era una prueba y se descartó; el workbook v2 vuelve a estar vacío |
| S1.9 | Sin registro en el repositorio |

**Decisiones del investigador (3 de noviembre):**

- **D1.** No hay segundo anotador ni evaluador. El estudio se declara piloto con un solo anotador y un solo evaluador, como prevé la tabla de riesgos. La doble anotación del lote 1 (S2.1) y los juicios dobles con adjudicación (S3.4) no se pueden hacer; se reportan como limitación.
- **Alcance.** Se mantiene el cierre del 22 de noviembre con alcance reducido. El recorte concreto (consultas, modelos y tareas) se fija en el protocolo experimental (S1.3) antes de ver cualquier dato de prueba.
- **Acuerdo sin segundo anotador.** Reemplaza a S2.1: el anotador re-anota a ciegas el lote 1 (30 piezas, otro orden) al menos 7 días después de la primera anotación, y se mide el acuerdo intra-anotador (test-retest). Se reporta como estabilidad de la anotación, no como acuerdo entre personas.
- **D3 (esquema de anotación).** Se agregan `eje_bandas` y `secuencia_bandas`: la palabra de bandas con el tipo de cada banda (`lisa`, `geometrica`, `figurativa`, `mixta`, `no_determinada`, y `laguna` para un tramo que no se ve), sin color ni anchos. Los estados `ausente`, `no_observable` y `desconocido` se escriben en la misma celda del atributo. Detalle: `docs/protocolo_anotacion_v2.md`.

### Avance de la semana 2 (5 de noviembre)

| ID | Estado |
|---|---|
| S1.8 y S2.4 | Hecho (5 de noviembre): los cinco lotes del núcleo, 150 piezas, anotación manual en una sola fecha. El tiempo por pieza no quedó medido |
| Validación v2 | Hecho (5 de noviembre): el flujo valida los dos workbooks v2 y exporta `data/metadata/anotaciones_v2.csv`; informe en `outputs/reports/anotacion_v2_validacion.md` |
| S2.1 (re-anotación del lote 1) | Desde el 12 de noviembre (7 días después) |
| S1.3 | En curso (5 de noviembre): `docs/protocolo_experimental_v2.md`, versión 0.2 propuesta, pendiente de aprobación del asesor |
| S1.7 | Hecho (5 de noviembre): candidatos a duplicado por cinco señales (imagen idéntica, inventario, descripción, dHash y M2) en `data/metadata/grupos_revision_v2.xlsx`, con galería local de pares |
| S2.2 | Hecho (6 de noviembre): 100 pares decididos por el investigador sobre el principal y el complementario (65 unir, 35 separar); 577 grupos para 615 piezas; el núcleo queda en 146 grupos |
| F2-H1b (parte de S2.3) | Hecho (6 de noviembre): complementario v2 (153) y consolidado v2 MET+CMA+AIC (615 registros) con grupos, licencias por fuente, manifiesto de imágenes y SHA-256; la anotación v2 entra en la v2.1 |
| S3.1 (parte M2, adelantada) | Hecho en desarrollo (5 de noviembre): embeddings OpenCLIP congelados de las 873 copias de evaluación, en CPU (la compilación CUDA para Python 3.15 no carga en el equipo); sin consultas ni rankings de la galería. Sus vecinos más cercanos aportan candidatos a duplicado para S1.7 |

**Decisiones del investigador (5 de noviembre):**

- **Estado de anotación.** El núcleo queda como `anotado_manual`. Se agrega `anotado_asistido` al vocabulario, reservado para uso futuro; no se usa en el núcleo.
- **Criterios y vocabulario después del retest.** Las observaciones marcan 104 piezas con `DUDA`, `CRITERIO` o `VOCAB`: huecos del vocabulario (colores, motivos vegetales y animales, damero, simetría rotacional, técnica de amarre) y criterios por unificar (esquinas de borde, varias tiras en una foto, listados, paneles a lo largo de una tira). Se deciden después de la re-anotación del lote 1, para no cambiar la guía entre las dos pasadas. Las piezas afectadas se corrigen luego en el workbook.
- **D6 (dependencias y checkpoint de M2).** Se aprueban `torch` 2.15.0 (CPU), `torchvision` 0.29.2 y `open_clip_torch` 3.3.0 como dependencias opcionales (`requirements-modelos.txt`), fuera del flujo. Checkpoint `xlm-roberta-base-ViT-B-32` / `laion5b_s13b_b90k` (licencia MIT, verificada en la ficha del modelo), multilingüe para las consultas T1 en español.
- **Protocolo experimental (S1.3).** Tarea primaria T3 (estructura por ejemplar) y T1 (texto a imagen) como secundaria exploratoria; 10 consultas de desarrollo y 30 de prueba en T3, más 6 de T1; juicio ciego sobre imágenes, con un doble juicio parcial de 5 consultas de prueba por el asesor u otra persona; D2 y D4–D7 entran como propuestas que el asesor ratifica antes de abrir el test.
