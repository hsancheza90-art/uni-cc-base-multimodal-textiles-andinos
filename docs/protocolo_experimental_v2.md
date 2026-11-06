# Protocolo experimental v2: recuperación estructural de textiles andinos

| | |
|---|---|
| Versión | 0.4, **propuesta**, 6 de noviembre de 2026 |
| Estado | Pendiente de aprobación del asesor. Se congela al aprobarse: la fecha y el commit de aprobación se registran en «Historial» y desde entonces cualquier cambio queda registrado allí con su motivo, antes de abrir el test |
| Responde a | MET01 de la auditoría del asesor (20 de octubre de 2026), informe 08; actividad S1.3 de `docs/plan_cierre_tesis.md` |
| Alcance | Estudio **piloto**: un solo anotador y un solo evaluador principal (decisión D1, 3 de noviembre) |

Este documento fija, antes de ver cualquier resultado de prueba, qué se compara, con qué datos, cómo se mide y qué cuenta como evidencia. Ningún modelo, consulta ni juicio de relevancia existe todavía; todo lo que sigue es plan. Las secciones marcadas **[propuesta]** recogen decisiones del plan de cierre (D2, D4, D5 y D7) que el asesor debe ratificar; D6 (dependencias y checkpoint de M2) la tomó el investigador el 5 de noviembre.

## 1. Pregunta, hipótesis y población

**Pregunta.** En un conjunto congelado de textiles andinos fotografiados por museos, ¿añadir el orden de las bandas y las relaciones entre regiones a las señales textuales y visuales mejora la recuperación estructural, según juicios humanos independientes de los modelos, y permite explicar el ranking de forma fiel?

**Hipótesis contrastables** (se evalúan en la tarea primaria T3, sección 3):

| | Hipótesis | Contraste | Regla de decisión |
|---|---|---|---|
| H1 (primaria) | La fusión con estructura recupera mejor que el codificador visual-textual congelado | nDCG@10 de M4 frente a M2, pareado por consulta | Se sostiene si la diferencia media es ≥ 0,03 **y** el límite inferior del IC 95 % es > 0. Si la diferencia es positiva pero el IC incluye 0: «dirección favorable sin evidencia suficiente». En otro caso: no se sostiene |
| H2 (mecanismo) | El orden importa: el descriptor con secuencia y adyacencias supera al mismo descriptor sin orden | nDCG@10 de M3 frente a M3-sin-orden | Misma regla que H1 |
| H3 (interpretabilidad) | El score de M4 se explica exactamente por sus componentes | Reconstrucción e intervención (sección 8) | Se sostiene si se cumplen las tres comprobaciones de la sección 8 |

H1 es la única comparación confirmatoria primaria. H2 es la única confirmatoria secundaria; como es una sola, no requiere corrección por multiplicidad. Toda otra comparación (M4 frente a M0, M1 o M3; ablaciones; análisis por museo) es **exploratoria** y se rotula así.

**Población de inferencia.** La colección digital elegible del corpus principal v2 (piezas MET, CMA y AIC con imagen CC0 o de dominio público, curadas con el criterio v2), no los textiles andinos en general. Un resultado negativo o nulo con este diseño es un resultado válido y se informa igual.

**Lo que este experimento no afirma.** No interpreta el significado cultural ni ritual de los motivos, no atribuye cultura de origen, no prueba invariancia al daño ni superioridad de extracción automática: M3 usa la anotación humana (sección 4) y M2 usa píxeles, así que la comparación mide la utilidad del sistema, no qué método extrae mejor la estructura.

## 2. Unidad experimental y galería

- **Galería [propuesta, D4].** Las 150 piezas del núcleo de anotación (`data/metadata/nucleo_anotacion_v2.csv`), las únicas con anotación estructural. El resto del principal v2 queda fuera del benchmark.
- **Unidad de partición: el grupo.** Antes de partir, se construyen grupos de piezas relacionadas (S1.7 y S2.2) sobre el principal y el complementario v2, porque una pieza complementaria puede unir por transitividad dos piezas de la galería. Proponen pares cinco señales: imagen idéntica, dHash de la copia (distancia ≤ 4, el umbral del consolidado v1), coseno de M2 (≥ 0,95; ≥ 0,93 entre museos), número de inventario con sufijo de parte y descripción curatorial idéntica. El investigador decide cada par en `data/metadata/grupos_revision_v2.xlsx` (`unir`, `separar` o `no_seguro`, que cuenta como unir para evitar fugas). Solo los pares de imagen idéntica entran propuestos como `unir` con `revisor = auto`, y se pueden corregir. Los grupos se forman por transitividad y se congelan cuando no quedan pares pendientes. Parámetros en `config/grupos.toml`.
- **Unidad de análisis: la consulta.** Las métricas se calculan por consulta y la inferencia remuestrea consultas.
- **Imagen.** Se usa la copia de evaluación de cada pieza (1600 px de lado mayor), la misma sobre la que se anotó. Ninguna imagen entra al test sin estar verificada en el manifiesto de evaluación.

## 3. Tareas

| Tarea | Consulta | Candidatos | Relevancia | Sistemas | Papel |
|---|---|---|---|---|---|
| **T3, estructura por ejemplar** | Una pieza de la galería (su imagen y, para M0, sus metadatos) | Las demás piezas de la galería, **excluido el grupo de la consulta** | Similitud estructural visible (sección 6) | M0–M4, M3-sin-orden, ablaciones y control | **Primaria**: H1 y H2 |
| T1, texto a imagen | Una descripción en español, redactada por el evaluador sin copiar fichas, más una especificación estructural opcional (tipo de composición y palabra de bandas) | Toda la galería | Cumplimiento visible de la descripción | M0, M2, M4 (M3 solo si la consulta trae especificación) | Secundaria, exploratoria |

- En T3, M0 recibe los metadatos de la pieza consultada: es una condición multimodal distinta (metadatos frente a imagen) y se rotula así. M1 no procesa texto, por lo que no participa en T1. Ninguna tabla se completa con valores de modalidades que un sistema no tiene.
- T2 (imagen a imagen por similitud general) y las tareas T4–T6 del informe 08 quedan fuera de este piloto.

## 4. Sistemas

Todos los sistemas son deterministas y se ejecutan sin entrenamiento. Los empates se resuelven por `id_global` ascendente.

| Sistema | Entrada y score | Ajuste permitido (solo en desarrollo) |
|---|---|---|
| **M0** | BM25 sobre el texto de la ficha: título original, título sugerido en español, descripción del museo, material y técnica. El texto de crédito de MET no entra (SW10), y tampoco su `descripcion`, que no es un texto del museo sino una plantilla armada con los metadatos (las 26 piezas MET con descripción la tienen; sus palabras fijas acercarían las piezas MET entre sí solo por su museo). Normalización a minúsculas y sin tildes; términos de 3 caracteres o más, sin lista de palabras vacías; el idioma mixto (inglés y español) se declara | k1 y b en una rejilla pequeña, o los valores por defecto 1,2 y 0,75 |
| **M1** | Visión convencional sobre el textil, separado del fondo con la misma segmentación del puntaje de aptitud: histograma conjunto de CIELAB (4 × 8 × 8 cubetas) y LBP de 8 vecinos invariante a la rotación (10 valores), a 320 px de lado mayor; disimilitud igual a la media ponderada de la mitad de la distancia L1 por bloque | Resolución y peso de cada bloque |
| **M2** | OpenCLIP congelado: embeddings de imagen (y de texto en T1) normalizados L2, similitud coseno. Checkpoint fijado el 5 de noviembre (D6, decisión del investigador): `xlm-roberta-base-ViT-B-32` con pesos `laion5b_s13b_b90k`, multilingüe para que T1 no requiera traducción; fp32; la imagen se lleva a un cuadrado con el color de su borde antes del recorte central del modelo, para no cortar los extremos de las piezas alargadas. Parámetros en `config/modelos.toml`; checkpoint, hash de los pesos y versiones en `data/metadata/m2_openclip_manifiesto_v2.json` | Plantilla de texto (T1); encuadre |
| **M3** | Descriptor estructural desde la anotación v2 (especificación completa en `docs/especificacion_m3.md`, siguiendo el informe 05): composición; palabra de bandas canonizada bajo reversión, c(w) = mínimo lexicográfico de {w, rev(w)}; histograma de pares de bandas adyacentes de c(w); borde, centro, simetría y repetición; histograma de motivos y familia iconográfica; máscara de observabilidad. Disimilitud mixta D(i,j) = Σ λ_b m_ib m_jb d_b(i,j) / Σ λ_b m_ib m_jb; si el denominador es 0, el par queda «sin evidencia estructural» y no recibe similitud máxima. **No incluye color**, para que una ganancia de M3 no sea cromática | Pesos λ_b y vocabulario |
| **M3-sin-orden** | Igual que M3, pero la palabra de bandas se reemplaza por el histograma de sus tipos y no hay adyacencias | Los mismos pesos que M3, sin reajustar |
| **M4** | Fusión tardía y aditiva de scores: s = Σ_c α_c ŝ_c con c ∈ {M0, M2, M3}, cada ŝ_c normalizado por consulta (mínimo-máximo sobre los candidatos). Si M3 no tiene evidencia para un par, su peso se reparte entre los demás en proporción a sus pesos (regla fija) y la cobertura se informa | Pesos α_c en la rejilla {0; 0,25; 0,5; 0,75; 1} normalizada a suma 1, elegidos por nDCG@10 medio en desarrollo |

M3 y M4 son **sistemas asistidos por anotación**, y así se declaran. La anotación que leen es la del workbook v2 congelada en la fecha de congelación de los sistemas (sección 9).

## 5. Particiones

- Los grupos se reparten en **desarrollo (30 %)** y **prueba (70 %)**, estratificados por museo, con semilla fija. Las proporciones se aplican a grupos, no a filas.
- **Consultas T3:** 10 de desarrollo, tomadas de grupos de desarrollo, y 30 de prueba, tomadas de grupos de prueba. Se eligen al azar con semilla fija, estratificadas por museo y por tipo de composición, entre las piezas cuya composición es observable. La selección no mira ningún ranking.
- **Consultas T1:** 6, solo de prueba, redactadas antes de ejecutar cualquier sistema sobre ellas. Usan los pesos fijados en T3, porque no tienen desarrollo propio.
- **Galería transductiva.** La galería es fija y contiene piezas de las dos particiones. Las relevancias de desarrollo se usan para ajustar y las de prueba nunca. Se declara como evaluación transductiva de recuperación.
- Todo lo que tenga un parámetro (normalización, vocabulario, pesos, plantillas, reglas) se fija con desarrollo. El test se ejecuta una sola vez, con los sistemas congelados.
- **Implementación** (6 de noviembre): `python -m src.experimento.snapshot --crear` fijó las particiones (`data/metadata/particiones_v2.csv`) y el sorteo (`data/metadata/consultas_t3_v2.csv`) con los valores de `config/experimento.toml`, y el flujo comprueba en cada ejecución que no haya fugas. Si una consulta deja de tener composición observable al corregir la anotación, se reemplaza con `--reemplazar` por la siguiente pieza elegible de su estrato, en el orden de la semilla. `consultas_t3_v2.csv` registra la composición de cada consulta: no se abre antes de cerrar la re-anotación del lote 1.

## 6. Consultas y juicios de relevancia

**Escala** (por par consulta-candidato):

| Grado | T3 (estructura) | T1 (texto) |
|---|---|---|
| 3 | Misma organización: tipo de composición, secuencia de bandas o regiones y relaciones, aunque cambien colores y motivos | Cumple toda la descripción |
| 2 | Misma composición con diferencias en la secuencia o en las relaciones | Cumple lo principal |
| 1 | Comparte un rasgo estructural parcial | Cumple un rasgo |
| 0 | Organización distinta | No cumple |

`no_evaluable` es un estado aparte (imagen ilegible para el juicio): no cuenta como 0, se excluye del ideal de la consulta y se informa su frecuencia. Cada juicio de grado 2 o 3 lleva una justificación breve que señala la evidencia visible.

**Pooling.** Por consulta se juzgan: los 10 primeros de M0, M1, M2, M3, M3-sin-orden y M4, sin repetir, más 10 candidatos al azar (semilla fija) y los positivos que el evaluador proponga. Las ablaciones y el control negativo (sección 7) se evalúan contra ese pool, con los no juzgados como 0, y se informa su proporción juzgada en el top 10. Recall y mAP, si se informan, son relativos al pool.

**Salvaguardas contra la circularidad.** El investigador anotó la estructura que lee M3 y es el evaluador principal; es la amenaza más seria del estudio (dictamen del asesor, pregunta 9). Se mitiga así:

1. Las consultas se fijan antes de ejecutar cualquier sistema sobre ellas: las de T3 por sorteo, las de T1 redactadas.
2. Los juicios se hacen sobre las imágenes, sin abrir los workbooks de anotación ni ver rankings, scores o el sistema que propuso cada candidato. El pool de cada consulta se presenta barajado.
3. La escala y estos criterios quedan fijos antes de juzgar. Ningún juicio se deriva de la anotación, del descriptor ni de CLIP.
4. **Doble juicio parcial [propuesta]:** el asesor, u otra persona con criterio estructural, juzga a ciegas los pools de 5 consultas de prueba elegidas al azar. Se informa el acuerdo (kappa ponderado lineal sobre la escala 0–3) antes de cualquier adjudicación, y la métrica primaria se recalcula con esos juicios como análisis de sensibilidad. Se conservan ambas versiones.

Los juicios y las consultas de T1 son decisiones humanas: viven en workbooks (`data/metadata/`) y el flujo los exporta a CSV, como el resto del corpus.

**Consultas sin relevantes.** Una consulta sin ningún candidato de grado ≥ 1 no tiene nDCG definido: se excluye de la media y se informa cuántas hubo y cuáles. No se reemplaza.

## 7. Métricas, inferencia, ablaciones y controles

**Métrica primaria:** nDCG@10 por consulta de T3, con ganancia 2^rel − 1 y descuento log₂(r + 1). El ideal se calcula con todos los juicios de la consulta.

**Secundarias:** P@10 y MRR con relevancia binarizada en grado ≥ 2, y proporción juzgada en el top 10. En T1 se informan las mismas métricas de forma descriptiva.

**Inferencia [propuesta, D5]:**

- Diferencia pareada por consulta, Δ = nDCG@10(M4) − nDCG@10(M2) (y M3 − M3-sin-orden para H2).
- IC 95 % por bootstrap pareado de consultas: 10 000 réplicas con semilla fija y el mismo remuestreo para los dos sistemas. Como sensibilidad, una prueba de permutación pareada por cambio de signo con 10 000 réplicas.
- Umbral práctico: Δ = 0,03.
- **Potencia.** Con la desviación estándar de Δ medida en las 10 consultas de desarrollo se estima n ≈ [(z₀,₉₇₅ + z₀,₈) · DE(Δ) / 0,03]². Si n supera 30, el estudio se declara sin potencia suficiente para el umbral y se informa con su IC. El número de consultas de prueba solo puede reducirse antes de abrir el test, nunca después.

**Ablaciones** (sobre las mismas consultas y candidatos): M4 sin M3 (texto e imagen solos); M4 sin M0; M4 con M3-sin-orden en lugar de M3; M3 solo con bandas frente a M3 solo con motivos y relaciones.

**Control negativo:** M4 con los descriptores de M3 permutados entre piezas del mismo museo (semilla fija). Si el aporte de la estructura es real, debe desaparecer.

**Robustez (exploratoria):** resultados por museo de la consulta y por estado de la pieza (fragmento o completa). Con estos tamaños son descriptivos.

## 8. Interpretabilidad (H3)

Para cada resultado del top 10 de M4 en prueba se registran las contribuciones α_c ŝ_c, la máscara y la procedencia de cada valor.

1. **Reconstrucción:** la suma de contribuciones coincide con el score con un error ≤ 1e-9 en todos los resultados.
2. **Intervención:** retirar un componente cambia el score exactamente como predice la fórmula, incluida la regla de reparto de pesos. Se verifica con pruebas de propiedades y sobre todos los resultados de prueba.
3. **Revisión humana:** en 10 resultados de prueba (5 aciertos y 5 errores, elegidos al azar), el evaluador juzga si la explicación es correcta y no especulativa, y se informan los desacuerdos.

## 9. Congelación, manifiesto y criterios de suspensión

**Orden obligatorio:**

1. Grupos, particiones y anotación congelados. Las correcciones de criterios y vocabulario que siguen a la re-anotación del lote 1 se aplican y registran **antes** de este punto.
2. Desarrollo: rankings, juicios de desarrollo, ajuste de pesos y estimación de potencia.
3. Congelación de los sistemas: un manifiesto de ejecución con el commit, los hashes SHA-256 de todos los insumos, el checkpoint, los parámetros, el hardware y las semillas.
4. Pool y juicios de prueba (y el doble juicio parcial).
5. Una sola ejecución del test.

**El test no se abre si ocurre alguna de estas condiciones** (informe 10 de la auditoría): grupos duplicados repartidos entre particiones; juicios derivados del descriptor o de CLIP; cambios de la guía de anotación o de este protocolo sin registrar; pesos ajustados con datos de prueba; imágenes sin verificar. Una comprobación automática de fugas (ningún grupo en dos particiones, ninguna consulta en su propio pool) se ejecuta antes de abrir el test. La suspensión protege el test, no impide preparar código ni trabajar en desarrollo.

**Archivos.** Se crean con nombres nuevos y sin tocar la v1.2. Se usan nombres en español, como en el resto del repositorio; la equivalencia con el informe 08 va entre paréntesis.
- Decisiones humanas, en workbooks de `data/metadata/`: grupos, consultas de T1 y juicios de desarrollo y de prueba.
- Archivos generados: grupos (`groups.csv`), particiones (`splits.csv`), consultas (`queries.csv`), juicios (`qrels.csv`), rankings, métricas por consulta (`metrics_by_query.csv`), modelos (`models.toml`) y manifiesto de ejecución (`run_manifest.json`).
- Los valores numéricos de este protocolo (semillas, proporciones, k, profundidad del pool, réplicas y umbral) pasan a `config/experimento.toml` cuando se implemente el primer sistema (S2.6), y una prueba comprueba que coinciden con este documento.

## 10. Amenazas a la validez y limitaciones que se declaran

| Amenaza | Mitigación | Lo que queda |
|---|---|---|
| Circularidad: el mismo investigador anota, diseña y juzga | Juicio ciego y barajado, consultas previas, doble juicio parcial | Sesgo residual a favor de M3; se declara como limitación principal |
| Un solo evaluador | Doble juicio parcial de 5 consultas | Acuerdo estimado con poca muestra |
| Duplicados y vistas de una misma pieza | Grupos decididos antes de partir; comprobación de fugas | Relaciones no detectadas |
| Pocas consultas (30) | IC pareado, potencia estimada en desarrollo | IC amplio; alcance piloto |
| Pooling | Unión de los top 10 de seis sistemas más muestra al azar | Sesgo hacia los sistemas del pool; se informa la proporción juzgada |
| Diferencias de fotografía entre museos | Resultados por museo | Tamaños pequeños por museo |
| M3 asistido por anotación | Declarado; M3 sin color | No mide extracción automática |
| Anotación de un solo anotador | Acuerdo intra-anotador del lote 1 (`outputs/reports/anotacion_acuerdo_v2.md`) | Estabilidad, no acuerdo entre personas |

## 11. Calendario restante

| Fechas (2026) | Actividad (plan de cierre) |
|---|---|
| 5–7 nov | Este protocolo (S1.3) y candidatos a duplicado (S1.7) |
| 8–11 nov | Grupos y particiones (S2.2, S2.3), especificación de M3 (S2.5), M0 y M1 (S2.6), consultas (S2.7) |
| 12–13 nov | Re-anotación del lote 1 (S2.1); decisiones de criterios y vocabulario; congelación de la anotación |
| 12–15 nov | M2, M3 y M4 (S3.1); juicios de desarrollo y potencia (S3.2) |
| 16–17 nov | Congelación de los sistemas (S3.3); pool y juicios de prueba (S3.4) |
| 18–19 nov | Test, ablaciones, interpretabilidad (S4.1–S4.3) |
| 20–22 nov | Informe de Seminario II y paquete reproducible (S4.5–S4.7) |

**Carga estimada de juicios** (supuesto: 30 s por juicio, unos 40 candidatos por consulta): T3 son 40 consultas, unos 1600 juicios y alrededor de 13 h; T1 son 6 consultas, unos 240 juicios y alrededor de 2 h; el doble juicio parcial son unos 200 juicios y alrededor de 1,7 h para el segundo evaluador. El tiempo real se mide en los juicios de desarrollo; si no cabe, se reducen consultas de prueba antes de abrir el test.

## Historial

| Fecha | Versión | Cambio |
|---|---|---|
| 2026-11-05 | 0.1 | Propuesta inicial para la aprobación del asesor |
| 2026-11-05 | 0.2 | M2: checkpoint, precisión y encuadre fijados (D6) al calcular los embeddings de las imágenes, antes de cualquier consulta, juicio o ranking de la galería. Sección 2: señales, umbrales y regla de duda de los grupos |
| 2026-11-06 | 0.3 | Sección 2: grupos también sobre el complementario. Sección 5: particiones y consultas T3 congeladas, regla de reemplazo y valores en `config/experimento.toml` |
| 2026-11-06 | 0.4 | Sección 4: M0 sin la descripción plantilla de MET; M1 sobre el textil segmentado, con sus parámetros; M3 especificado en `docs/especificacion_m3.md`. Rankings de desarrollo de M0, M1 y M2, sin ejecutar ninguna consulta de prueba |
