# Protocolo experimental v2: recuperación estructural de textiles andinos

| | |
|---|---|
| Versión | 0.5, **propuesta**, 6 de noviembre de 2026 |
| Estado | Pendiente de aprobación del asesor. Al aprobarse, el protocolo se congela: la fecha y el commit de aprobación se registran en el «Historial», y desde entonces todo cambio se anota allí con su motivo antes de abrir el test |
| Responde a | Observación MET01 de la auditoría del asesor (20 de octubre de 2026), informe 08; actividad S1.3 del plan de cierre (`docs/plan_cierre_tesis.md`) |
| Alcance | Estudio **piloto**, con un solo anotador y un solo evaluador principal (decisión D1, 3 de noviembre) |

Este protocolo establece, antes de observar cualquier resultado de prueba, qué se compara, con qué datos, cómo se mide y qué se considerará evidencia a favor o en contra de cada hipótesis. A la fecha de esta versión no se ha ejecutado ningún sistema sobre las consultas de prueba. Las decisiones del plan de cierre que el asesor debe ratificar (D2, D4, D5 y D7) aparecen marcadas como **[propuesta]**. La decisión D6, sobre las dependencias y el checkpoint de M2, la tomó el investigador el 5 de noviembre.

## 1. Pregunta, hipótesis y población

**Pregunta de investigación.** En un conjunto congelado de textiles andinos fotografiados por museos, ¿añadir el orden de las bandas y las relaciones entre regiones a las señales textuales y visuales mejora la recuperación estructural, según juicios humanos independientes de los modelos? ¿Permite, además, explicar el ranking de forma fiel?

**Hipótesis.** Las tres se contrastan en la tarea primaria T3 (sección 3):

| | Hipótesis | Contraste | Regla de decisión |
|---|---|---|---|
| H1 (primaria) | La fusión que incorpora la estructura recupera mejor que el codificador visual-textual congelado | nDCG@10 de M4 frente a M2, pareado por consulta | Se sostiene si la diferencia media es ≥ 0,03 **y** el límite inferior del IC 95 % es > 0. Si la diferencia es positiva pero el intervalo incluye el cero, se informa como «dirección favorable sin evidencia suficiente». En cualquier otro caso, no se sostiene |
| H2 (mecanismo) | El orden importa: el descriptor con secuencia y adyacencias supera al mismo descriptor sin orden | nDCG@10 de M3 frente a M3-sin-orden | La misma regla que H1 |
| H3 (interpretabilidad) | El score de M4 se explica exactamente por la suma de sus componentes | Reconstrucción e intervención (sección 8) | Se sostiene si se cumplen las tres comprobaciones de la sección 8 |

H1 es la única comparación confirmatoria primaria y H2 la única confirmatoria secundaria; al ser una sola, no requiere corrección por comparaciones múltiples. Cualquier otra comparación (M4 frente a M0, M1 o M3, las ablaciones o el análisis por museo) es **exploratoria** y se presentará como tal.

**Población de inferencia.** Los resultados se refieren a la colección digital elegible del corpus principal v2: piezas de MET, CMA y AIC con imagen CC0 o de dominio público, curadas con el criterio v2. No se generalizan a los textiles andinos en su conjunto. Con este diseño, un resultado negativo o nulo es igualmente válido y se informará del mismo modo que uno positivo.

**Alcance de las conclusiones.** El experimento no interpreta el significado cultural o ritual de los motivos, no atribuye la cultura de origen y no prueba la invariancia de los sistemas al deterioro de las piezas. Tampoco compara métodos de extracción automática de la estructura: M3 se apoya en la anotación humana y M2 en los píxeles, de modo que la comparación mide la utilidad de cada sistema y no qué método extrae mejor la estructura.

## 2. Unidad experimental y galería

**Galería [propuesta, D4].** La galería está formada por las 150 piezas del núcleo de anotación, que son las únicas con anotación estructural. El resto del principal v2 queda fuera del benchmark.

**Unidad de partición: el grupo.** Antes de partir la galería se agrupan los registros que muestran el mismo objeto o partes de él (S1.7 y S2.2). La agrupación se hace sobre el principal y el complementario v2, porque una pieza complementaria puede unir por transitividad dos piezas de la galería. Los pares candidatos a «mismo objeto» se proponen con cinco señales: imagen idéntica, dHash de la copia de evaluación (distancia ≤ 4, el umbral del consolidado v1), coseno de M2 (≥ 0,95 dentro de un museo y ≥ 0,93 entre museos), número de inventario con sufijo de parte y descripción curatorial idéntica.

El investigador decide cada par como `unir`, `separar` o `no_seguro`. Esta última cuenta como unir, para evitar que dos vistas de un mismo objeto terminen en particiones distintas. Solo los pares de imagen idéntica se proponen de antemano como `unir`, y el investigador puede corregirlos. Los grupos se forman por transitividad y se congelan cuando no queda ningún par pendiente.

**Unidad de análisis: la consulta.** Las métricas se calculan por consulta, y la inferencia remuestrea consultas.

**Imagen.** Todos los sistemas usan la copia de evaluación de cada pieza (1600 px de lado mayor), que es la misma sobre la que se hizo la anotación. Ninguna imagen entra al test sin haberse verificado contra su suma SHA-256 en el manifiesto de evaluación.

## 3. Tareas

| Tarea | Consulta | Candidatos | Relevancia | Sistemas | Papel |
|---|---|---|---|---|---|
| **T3: estructura por ejemplar** | Una pieza de la galería: su imagen y, para M0, sus metadatos | Las demás piezas de la galería, **excluido el grupo de la consulta** | Similitud estructural visible (sección 6) | M0–M4, M3-sin-orden, ablaciones y control negativo | **Primaria**: H1 y H2 |
| T1: texto a imagen | Una descripción en español redactada por el evaluador, sin copiar fichas, con una especificación estructural opcional (tipo de composición y palabra de bandas) | Toda la galería | Cumplimiento visible de la descripción | M0, M2 y M4; M3 solo si la consulta trae especificación | Secundaria y exploratoria |

En T3, M0 recibe los metadatos de la pieza consultada en lugar de su imagen; se trata de una condición distinta y se identificará como tal. M1 no procesa texto, por lo que no participa en T1. Ninguna tabla de resultados se completará con valores para modalidades que un sistema no tiene. La tarea T2 (imagen a imagen por similitud general) y las tareas T4 a T6 del informe 08 quedan fuera de este piloto.

## 4. Sistemas

Todos los sistemas son deterministas y ninguno se entrena. Los empates en el score se resuelven por `id_global` en orden ascendente.

| Sistema | Entrada y score | Ajuste permitido (solo en desarrollo) |
|---|---|---|
| **M0** | BM25 sobre el texto de la ficha: título original, título sugerido en español, descripción del museo, material y técnica. No se incluye el texto de crédito de MET (SW10) ni su campo de descripción: en MET ese campo no es un texto del museo, sino una plantilla armada con los propios metadatos, y sus palabras fijas aproximarían las piezas MET entre sí solo por proceder del mismo museo. El texto se normaliza a minúsculas y sin tildes, se toman términos de tres caracteres o más y no se usa lista de palabras vacías. La mezcla de inglés y español se declara como característica del corpus | k1 y b en una rejilla pequeña; por defecto, 1,2 y 0,75 |
| **M1** | Visión convencional sobre el textil, separado del fondo con la misma segmentación que usa el puntaje de aptitud. Combina un histograma conjunto de CIELAB (4 × 8 × 8 cubetas) y un histograma de LBP de 8 vecinos invariante a la rotación (10 valores), calculados a 320 px de lado mayor. La disimilitud es la media ponderada de la mitad de la distancia L1 en cada bloque | Resolución y peso de cada bloque |
| **M2** | OpenCLIP congelado: embeddings de imagen (y de texto en T1) normalizados L2, comparados por coseno. El checkpoint quedó fijado el 5 de noviembre (D6): `xlm-roberta-base-ViT-B-32` con pesos `laion5b_s13b_b90k`. Es multilingüe, de modo que las consultas T1 no requieren traducción. El cálculo es en fp32, y antes del recorte central del modelo cada imagen se lleva a un cuadrado rellenado con el color de su borde, para no cortar los extremos de las piezas alargadas | Plantilla de texto (T1) y encuadre |
| **M3** | Descriptor estructural derivado de la anotación v2 (especificación completa en `docs/especificacion_m3.md`, conforme al informe 05). Considera la composición; la palabra de bandas en su forma canónica bajo reversión, c(w) = mínimo lexicográfico de {w, rev(w)}; el histograma de pares de bandas contiguas; borde, centro, simetría y repetición; los motivos y la familia iconográfica, y una máscara de observabilidad. La disimilitud mixta es D(i,j) = Σ λ_b m_ib m_jb d_b(i,j) / Σ λ_b m_ib m_jb. Si el denominador es cero, el par queda «sin evidencia estructural» y no recibe similitud máxima. **M3 no incluye el color**, para que una eventual ganancia no sea de origen cromático | Pesos λ_b y vocabulario |
| **M3-sin-orden** | Igual que M3, pero la palabra de bandas se sustituye por el histograma de sus tipos y se omiten las adyacencias | Los mismos pesos que M3, sin reajustar |
| **M4** | Fusión tardía y aditiva de scores: s = Σ_c α_c ŝ_c, con c ∈ {M0, M2, M3} y cada ŝ_c normalizado por consulta (mínimo y máximo sobre los candidatos). Cuando M3 no tiene evidencia para un par, su peso se reparte entre los demás componentes en proporción a sus pesos, según una regla fija, y se informa la cobertura | Pesos α_c en la rejilla {0; 0,25; 0,5; 0,75; 1}, normalizados a suma 1 y elegidos por el nDCG@10 medio en desarrollo |

M3 y M4 se declaran **sistemas asistidos por anotación**. La anotación que utilizan es la versión congelada en la fecha de congelación de los sistemas (sección 9).

## 5. Particiones

Los grupos de la galería se reparten en **desarrollo (30 %)** y **prueba (70 %)**, estratificados por museo y con semilla fija. Las proporciones se aplican a grupos y no a registros.

- **Consultas T3:** 10 de desarrollo, tomadas de grupos de desarrollo, y 30 de prueba, tomadas de grupos de prueba. Se sortean con semilla fija entre las piezas cuya composición es observable, estratificadas por museo y por tipo de composición, con a lo sumo una consulta por grupo. El sorteo no consulta ningún ranking.
- **Regla de reemplazo:** si, al corregir la anotación después de la re-anotación, una consulta deja de tener composición observable, se reemplaza por la siguiente pieza elegible de su estrato, en el orden que fija la semilla.
- **Consultas T1:** 6, solo de prueba, redactadas antes de ejecutar ningún sistema sobre ellas. Como no tienen desarrollo propio, se usan los pesos fijados en T3.
- **Galería transductiva:** la galería es fija y contiene piezas de las dos particiones. Las relevancias de desarrollo se usan para ajustar los sistemas; las de prueba, nunca. Por eso la evaluación se declara como recuperación transductiva.
- **Ajuste:** todo lo que tenga un parámetro (normalización, vocabulario, pesos, plantillas o reglas) se fija con los datos de desarrollo. El test se ejecuta una sola vez, con los sistemas congelados.

## 6. Consultas y juicios de relevancia

**Escala.** Cada par formado por una consulta y un candidato se juzga en cuatro grados:

| Grado | T3 (estructura) | T1 (texto) |
|---|---|---|
| 3 | Misma organización: tipo de composición, secuencia de bandas o regiones y relaciones, aunque cambien colores y motivos | Cumple toda la descripción |
| 2 | Misma composición, con diferencias en la secuencia o en las relaciones | Cumple lo principal |
| 1 | Comparte un rasgo estructural parcial | Cumple un rasgo |
| 0 | Organización distinta | No la cumple |

Además existe el estado `no_evaluable`, para imágenes que no permiten juzgar. No equivale a 0: el par se excluye del ideal de la consulta y se informa su frecuencia. Todo juicio de grado 2 o 3 lleva una justificación breve que indique la evidencia visible.

**Selección de los pares a juzgar.** Para cada consulta se juzgan los 10 primeros de M0, M1, M2, M3, M3-sin-orden y M4, sin repetir pares. A ellos se suman 10 candidatos al azar (con semilla fija) y los positivos que proponga el evaluador. Las ablaciones y el control negativo (sección 7) se evalúan sobre ese mismo conjunto: los candidatos no juzgados cuentan como 0 y se informa qué proporción del top 10 quedó juzgada. Si se informan recall o mAP, se calculan respecto de este conjunto.

**Salvaguardas contra la circularidad.** El investigador anotó la estructura que utiliza M3 y es, además, el evaluador principal. Es la amenaza más seria para la validez del estudio (dictamen del asesor, pregunta 9), y se mitiga de cuatro maneras:

1. Las consultas se fijan antes de ejecutar cualquier sistema sobre ellas: las de T3 por sorteo y las de T1 por redacción.
2. Los juicios se hacen solo sobre las imágenes, sin consultar la anotación ni ver los rankings, los scores o el sistema que propuso cada candidato. Los candidatos de cada consulta se presentan en orden aleatorio.
3. La escala y estos criterios se fijan antes de juzgar. Ningún juicio se deriva de la anotación, del descriptor ni de CLIP.
4. **Doble juicio parcial [propuesta]:** el asesor, u otra persona con criterio estructural, juzga a ciegas los pools de 5 consultas de prueba elegidas al azar. Se informa el acuerdo entre ambos evaluadores (kappa ponderado lineal sobre la escala 0–3) antes de cualquier adjudicación, y la métrica primaria se recalcula con esos juicios como análisis de sensibilidad. Se conservan las dos versiones.

**Consultas sin relevantes.** Si ningún candidato de una consulta alcanza el grado 1, su nDCG no está definido. Esa consulta se excluye de la media, se informa cuántas hubo y cuáles fueron, y no se reemplaza.

## 7. Métricas, inferencia, ablaciones y controles

**Métrica primaria.** nDCG@10 por consulta de T3, con ganancia 2^rel − 1 y descuento log₂(r + 1). El ordenamiento ideal se calcula con todos los juicios de la consulta.

**Métricas secundarias.** P@10 y MRR con la relevancia binarizada en el grado 2, y la proporción juzgada del top 10. En T1 se informan las mismas métricas de forma descriptiva.

**Inferencia [propuesta, D5]:**

- Se calcula la diferencia pareada por consulta, Δ = nDCG@10(M4) − nDCG@10(M2), y, para H2, Δ = nDCG@10(M3) − nDCG@10(M3-sin-orden).
- El intervalo IC 95 % se obtiene por bootstrap pareado de consultas, con 10 000 réplicas, semilla fija y el mismo remuestreo para los dos sistemas. Como análisis de sensibilidad se añade una prueba de permutación pareada por cambio de signo, también con 10 000 réplicas.
- Umbral práctico: Δ = 0,03.
- **Potencia.** Con la desviación estándar de Δ observada en las 10 consultas de desarrollo se estima el tamaño necesario, n ≈ [(z₀,₉₇₅ + z₀,₈) · DE(Δ) / 0,03]². Si n supera 30, el estudio se declarará sin potencia suficiente para ese umbral y se informará el intervalo obtenido. El número de consultas de prueba solo puede reducirse antes de abrir el test, nunca después.

**Ablaciones.** Se calculan sobre las mismas consultas y candidatos:
- M4 sin M3, es decir, solo texto e imagen.
- M4 sin M0.
- M4 con M3-sin-orden en lugar de M3.
- M3 solo con bandas frente a M3 solo con motivos y relaciones.

**Control negativo.** M4 con los descriptores de M3 permutados al azar entre piezas del mismo museo, con semilla fija. Si el aporte de la estructura es real, debe desaparecer en esta condición.

**Robustez (exploratoria).** Resultados según el museo de la consulta y según el estado de la pieza (fragmento o pieza completa). Con estos tamaños de muestra, el análisis es descriptivo.

## 8. Interpretabilidad (H3)

Para cada resultado del top 10 de M4 en prueba se registran las contribuciones α_c ŝ_c de cada componente, la máscara de observabilidad y la procedencia de cada valor. H3 se sostiene si se cumplen tres comprobaciones:

1. **Reconstrucción:** la suma de las contribuciones coincide con el score, con un error ≤ 1e-9, en todos los resultados.
2. **Intervención:** retirar un componente modifica el score exactamente como predice la fórmula, incluida la regla de reparto de pesos. Se verifica con pruebas de propiedades y sobre todos los resultados de prueba.
3. **Revisión humana:** en 10 resultados de prueba elegidos al azar (5 aciertos y 5 errores), el evaluador juzga si la explicación es correcta y no especulativa. Se informan los desacuerdos.

## 9. Congelación y criterios de suspensión

El experimento sigue un orden obligatorio:

1. Se congelan los grupos, las particiones y la anotación. Las correcciones de criterios y de vocabulario que resulten de la re-anotación del lote 1 se aplican y se registran **antes** de este punto.
2. Desarrollo: rankings, juicios de desarrollo, ajuste de pesos y estimación de la potencia.
3. Congelación de los sistemas, con un manifiesto de ejecución que registra el commit, las sumas SHA-256 de todos los insumos, el checkpoint, los parámetros, el hardware y las semillas.
4. Selección de los pares de prueba y juicios de prueba, incluido el doble juicio parcial.
5. Una única ejecución del test.

**El test no se abre** si se da alguna de estas condiciones (informe 10 de la auditoría):
- hay grupos de piezas relacionadas repartidos entre particiones;
- algún juicio se derivó del descriptor o de CLIP;
- la guía de anotación o este protocolo cambiaron sin registro;
- algún peso se ajustó con datos de prueba;
- alguna imagen no está verificada.

Antes de abrir el test se ejecuta una comprobación automática de fugas: que ningún grupo esté en dos particiones y que ninguna consulta figure entre sus propios candidatos. La suspensión protege el test, pero no impide preparar código ni trabajar con los datos de desarrollo.

## 10. Amenazas a la validez y limitaciones

| Amenaza | Mitigación | Limitación que se declara |
|---|---|---|
| Circularidad: un mismo investigador anota, diseña y juzga | Juicio ciego y aleatorizado, consultas fijadas de antemano y doble juicio parcial | Sesgo residual a favor de M3; es la limitación principal |
| Un solo evaluador | Doble juicio parcial en 5 consultas | Acuerdo estimado con una muestra pequeña |
| Duplicados y vistas de una misma pieza | Grupos decididos antes de partir y comprobación de fugas | Relaciones que no detecte ninguna señal |
| Pocas consultas de prueba (30) | Intervalo pareado y potencia estimada en desarrollo | Intervalos amplios; alcance de piloto |
| Juicio solo de los primeros candidatos (pooling) | Unión de los 10 primeros de seis sistemas más una muestra al azar | Sesgo hacia los sistemas que aportan candidatos; se informa la proporción juzgada |
| Diferencias de fotografía entre museos | Resultados por museo | Tamaños pequeños por museo |
| M3 asistido por anotación | Se declara, y M3 excluye el color | No mide la extracción automática de la estructura |
| Un solo anotador | Acuerdo intra-anotador en el lote 1 | Mide estabilidad, no acuerdo entre personas |

## 11. Calendario restante

| Fechas (2026) | Actividad (plan de cierre) | Estado al 6 de noviembre |
|---|---|---|
| 5 y 6 nov | Protocolo (S1.3), grupos y particiones (S1.7, S2.2 y S2.3), especificación de M3 (S2.5), M0 y M1 (S2.6), consultas T1 (S2.7) | Hecho, salvo la aprobación del protocolo |
| 6 a 11 nov | Juicios de desarrollo de los candidatos de M0, M1 y M2 (S3.2) | En curso |
| 12 y 13 nov | Re-anotación del lote 1 (S2.1), decisión de criterios y vocabulario, congelación de la anotación | Programado |
| 13 a 15 nov | M3 y M4 (S3.1), sus juicios de desarrollo y la estimación de la potencia | Programado |
| 16 y 17 nov | Congelación de los sistemas (S3.3), juicios de prueba y doble juicio parcial (S3.4) | Programado |
| 18 y 19 nov | Test, ablaciones e interpretabilidad (S4.1 a S4.3) | Programado |
| 20 a 22 nov | Informe de Seminario II y paquete reproducible (S4.5 a S4.7) | Programado |

**Carga estimada de juicios**, con un supuesto de 30 s por juicio:
- Desarrollo: 345 pares con los candidatos de M0, M1 y M2, a los que se sumarán los de M3 y M4.
- Prueba en T3: unos 1600 pares, alrededor de 13 h.
- T1: unos 240 pares, alrededor de 2 h.
- Doble juicio parcial: unos 200 pares, alrededor de 1,7 h para el segundo evaluador.

El tiempo real se medirá en los juicios de desarrollo. Si la carga no cabe en el calendario, se reducirá el número de consultas de prueba antes de abrir el test.

## 12. Implementación en el repositorio

Todos los parámetros numéricos de este protocolo están en `config/experimento.toml` (particiones, consultas, juicios y métricas) y en `config/modelos.toml` (sistemas), y una prueba automática comprueba que coinciden con este documento. Las decisiones humanas (grupos, consultas T1 y juicios) se registran en libros de Excel en `data/metadata/`, y el flujo del repositorio las valida y exporta.

| Elemento | Archivo o comando |
|---|---|
| Grupos de piezas relacionadas | `data/metadata/grupos_revision_v2.xlsx` (decisiones), `data/metadata/grupos_v2.csv` y `config/grupos.toml` |
| Particiones y consultas T3 | `python -m src.experimento.snapshot --crear` (una sola vez) y `--reemplazar` (regla de reemplazo); `data/metadata/particiones_v2.csv` y `data/metadata/consultas_t3_v2.csv` |
| Consultas T1 | `data/metadata/consultas_t1_v2.xlsx` |
| Juicios de desarrollo | `data/metadata/juicios_desarrollo_v2.xlsx`, con los pares en orden aleatorio y sin sistema ni posición, y una galería local de imágenes |
| Rankings de desarrollo | `data/processed/experimento_v2_rankings_desarrollo.csv` |
| Checkpoint de M2 | `data/metadata/m2_openclip_manifiesto_v2.json` (sumas de los pesos y versiones) |

El evaluador no abre los rankings ni el archivo que registra qué sistema propuso cada par (`data/processed/experimento_v2_pool_desarrollo.csv`). Hasta cerrar la re-anotación del lote 1, tampoco abre `consultas_t3_v2.csv` ni `anotaciones_v2.csv`, porque contienen datos de la primera anotación. Los libros de consultas T1 y de juicios incluyen una hoja de ejemplos hipotéticos que ilustran el formato y la escala; no son piezas de la galería ni consultas.

Las equivalencias con los nombres del informe 08 son las siguientes: grupos (`groups.csv`), particiones (`splits.csv`), consultas (`queries.csv`), juicios (`qrels.csv`), métricas por consulta (`metrics_by_query.csv`), modelos (`models.toml`) y manifiesto de ejecución (`run_manifest.json`).

## Historial

| Fecha | Versión | Cambio |
|---|---|---|
| 2026-11-05 | 0.1 | Propuesta inicial para la aprobación del asesor |
| 2026-11-05 | 0.2 | M2: checkpoint, precisión y encuadre fijados (D6) al calcular los embeddings, antes de cualquier consulta, juicio o ranking de la galería. Sección 2: señales, umbrales y regla de duda de los grupos |
| 2026-11-06 | 0.3 | Sección 2: grupos también sobre el complementario. Sección 5: particiones y consultas T3 congeladas, regla de reemplazo y valores en `config/experimento.toml` |
| 2026-11-06 | 0.4 | Sección 4: M0 sin la descripción plantilla de MET; M1 sobre el textil segmentado; M3 especificado en `docs/especificacion_m3.md`. Rankings de desarrollo de M0, M1 y M2, sin ejecutar ninguna consulta de prueba. Sección 6: libros de consultas T1 y de juicios de desarrollo, con ejemplos hipotéticos |
| 2026-11-06 | 0.5 | Revisión de la redacción para la lectura del asesor y calendario actualizado; los detalles de implementación pasan a la sección 12. Sin cambios en el diseño |
