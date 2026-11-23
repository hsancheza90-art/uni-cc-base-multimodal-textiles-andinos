# Protocolo experimental v2: recuperación estructural de textiles andinos

| | |
|---|---|
| Versión | 0.6.6, **propuesta**, 23 de noviembre de 2026 |
| Estado | El dictamen del asesor del 21 de noviembre, sobre la versión 0.6.5, es favorable al diseño piloto y condiciona la apertura del test a que se acrediten sus observaciones en un nuevo commit, con pruebas automáticas. Esta versión incorpora esas observaciones (decisiones R33 a R39). El test no se abre antes de la autorización del asesor (R30). Al autorizarse, el protocolo se congela: la fecha y el commit se registran en el «Historial» y en `docs/registro_custodia.md`, y desde entonces todo cambio se anota con su motivo antes de abrir el test |
| Responde a | Observación MET01 de la auditoría del asesor (20 de octubre de 2026), informe 08; actividad S1.3 del plan de cierre (`docs/plan_cierre_tesis.md`); dictamen del asesor del 21 de noviembre de 2026 (observaciones B1 a B8) |
| Alcance | Estudio **piloto**, con un solo anotador y un solo evaluador principal (decisión D1, 3 de noviembre) |

Este protocolo establece, antes de observar cualquier resultado de prueba, qué se compara, con qué datos, cómo se mide y qué se considerará evidencia a favor o en contra de cada hipótesis. A la fecha de esta versión no se ha ejecutado ningún sistema sobre las consultas de prueba. Las decisiones del plan de cierre que el asesor debe ratificar (D2, D4 y D5) aparecen marcadas como **[propuesta]**. Las decisiones D6, sobre las dependencias y el checkpoint de M2, y D7, sobre el versionado de la auditoría, las tomó el investigador el 5 y el 6 de noviembre.

## 1. Pregunta, hipótesis y población

**Pregunta de investigación.** En un conjunto congelado de textiles andinos fotografiados por museos, ¿añadir el orden de las bandas y las relaciones entre regiones a las señales textuales y visuales mejora la recuperación estructural, según juicios humanos independientes de los modelos? ¿Permite, además, explicar el ranking de forma fiel?

**Hipótesis.** Las tres se contrastan en la tarea primaria T3 (sección 3):

| | Hipótesis | Contraste | Regla de decisión |
|---|---|---|---|
| H1 (primaria) | La fusión enriquecida con la estructura recupera mejor que el codificador visual-textual congelado | nDCG@10 de M4 frente a M2, pareado por consulta | Se sostiene si la prueba de permutación pareada bilateral da p < 0,05 **y** la diferencia media es ≥ 0,03 (sección 7). La sección 7 separa las tres afirmaciones que componen la regla y el modo de informar cada combinación. El IC 95 % se informa siempre, como estimación de la magnitud |
| H2 (mecanismo) | El orden importa: el descriptor con secuencia y adyacencias supera al mismo descriptor sin orden | nDCG@10 de M3 frente a M3-sin-orden, sobre las 30 consultas de prueba | La misma regla que H1, con la p exacta de la sección 7, y solo si H1 se sostiene (regla secuencial, más abajo). Además, como análisis descriptivo fijado antes del test, la misma comparación restringida a las consultas cuya pieza tiene palabra de bandas (9 de 30): en las demás, M3 y su control asignan la misma puntuación a todos los candidatos y la diferencia es cero por construcción (R27). Ese subgrupo no puede confirmar H2 |
| H3 (fidelidad computacional) | La puntuación de M4 se descompone exactamente en las contribuciones de sus componentes | Reconstrucción e intervención (sección 8) | Se sostiene si se cumplen las dos comprobaciones de la sección 8. La revisión humana de las explicaciones es un análisis descriptivo aparte y no interviene en el veredicto |

**Comparaciones confirmatorias y multiplicidad (R33).** Hay dos comparaciones confirmatorias, H1 y H2, y se contrastan en una secuencia fija. H1 se contrasta primero con α = 0,05. H2 recibe una conclusión confirmatoria solo si H1 cumple su regla completa (p < 0,05 y diferencia media ≥ 0,03); en caso contrario, H2 se informa como exploratoria, con su estimación, su intervalo y su p, sin veredicto. El procedimiento secuencial controla la tasa de error por familia en α porque H2 solo se contrasta si se rechaza la hipótesis nula de H1; exigir además Δ ≥ 0,03 hace la compuerta más conservadora, no menos. Con la potencia disponible (sección 7), la compuerta hace improbable una conclusión confirmatoria sobre H2, y así se declara.

**Alcance de H1.** H1 compara la fusión M4, que suma a M2 el texto (M0) y la estructura (M3), con M2 solo. Un resultado favorable indica que la fusión enriquecida mejora a M2; no aísla el aporte de la estructura, porque M4 también añade el texto. El aporte de la estructura se examina en las ablaciones (M4 sin M3, M4 con M3-sin-orden) y en H2, y las ablaciones son exploratorias.

Cualquier otra comparación (M4 frente a M0, M1 o M3, las ablaciones, el control negativo, M4-RRF, el subgrupo de bandas o el análisis por museo y por estado) es **exploratoria** y se presentará como tal.

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

Todos los sistemas son deterministas y ninguno se entrena. Los empates en la puntuación se resuelven por `id_global` en orden ascendente.

| Sistema | Entrada y puntuación | Ajuste permitido (solo en desarrollo) |
|---|---|---|
| **M0** | BM25 sobre el texto de la ficha: título original, título sugerido en español, descripción del museo, material y técnica. No se incluye el texto de crédito de MET (SW10) ni su campo de descripción: en MET ese campo no es un texto del museo, sino una plantilla armada con los propios metadatos, y sus palabras fijas aproximarían las piezas MET entre sí solo por proceder del mismo museo. El texto se normaliza a minúsculas y sin tildes, se toman términos de tres caracteres o más y no se usa lista de palabras vacías. La mezcla de inglés y español se declara como característica del corpus | k1 y b en una rejilla pequeña; por defecto, 1,2 y 0,75 |
| **M1** | Visión convencional sobre el textil, separado del fondo con la misma segmentación que usa el puntaje de aptitud. Combina un histograma conjunto de CIELAB (4 × 8 × 8 cubetas) y un histograma de LBP de 8 vecinos invariante a la rotación (10 valores), calculados a 320 px de lado mayor. La disimilitud es la media ponderada de la mitad de la distancia L1 en cada bloque | Resolución y peso de cada bloque |
| **M2** | OpenCLIP congelado: embeddings de imagen (y de texto en T1) normalizados L2, comparados por coseno. El checkpoint quedó fijado el 5 de noviembre (D6): `xlm-roberta-base-ViT-B-32` con pesos `laion5b_s13b_b90k`. Es multilingüe, de modo que las consultas T1 no requieren traducción. El cálculo es en fp32, y antes del recorte central del modelo cada imagen se lleva a un cuadrado rellenado con el color de su borde, para no cortar los extremos de las piezas alargadas | Encuadre. En T1 se codifica la descripción sin plantilla, porque T1 no tiene desarrollo (R32) |
| **M3** | Descriptor estructural derivado de la anotación v2 (especificación completa en `docs/especificacion_m3.md`, conforme al informe 05). Considera la composición; la palabra de bandas en su forma canónica bajo reversión, c(w) = mínimo lexicográfico de {w, rev(w)}; el histograma de pares de bandas contiguas; borde, centro, simetría y repetición; los motivos y la familia iconográfica, y una máscara de observabilidad. La disimilitud mixta es D(i,j) = Σ λ_b m_ib m_jb d_b(i,j) / Σ λ_b m_ib m_jb. Si el denominador es cero, el par queda «sin evidencia estructural» y no recibe similitud máxima. **M3 no incluye el color**, para que una eventual ganancia no sea de origen cromático | Pesos λ_b y vocabulario |
| **M3-sin-orden** | Igual que M3, pero la palabra de bandas se sustituye por el histograma de sus tipos y se omiten las adyacencias | Los mismos pesos que M3, sin reajustar |
| **M4** | Fusión tardía y aditiva de puntuaciones: s = Σ_c α_c ŝ_c, con c ∈ {M0, M2, M3} y cada ŝ_c normalizado por consulta (mínimo y máximo sobre los candidatos). Cuando M3 no tiene evidencia para un par, su peso se reparte entre los demás componentes en proporción a sus pesos, según una regla fija, y se informa la cobertura | Pesos α_c en la rejilla {0; 0,25; 0,5; 0,75; 1}, normalizados a suma 1 (91 combinaciones) y elegidos por el nDCG@10 medio en desarrollo. En empate, la combinación más cercana a pesos iguales y, si persiste, la primera en orden lexicográfico descendente |
| **M4-RRF** | Variante de M4 por posiciones recíprocas (sección 7): Σ_c 1 / (60 + r_c) sobre los rankings de M0, M2 y M3 | Ninguno: k = 60 fijo |

M3 y M4 se declaran **sistemas asistidos por anotación**. La anotación que utilizan es la versión congelada en la fecha de congelación de los sistemas (sección 9).

**Parámetros fijados en desarrollo (decisiones R28 y R30).** Los pesos de M4 se eligieron una sola vez con la regla de esta sección y los 411 juicios de desarrollo vigentes el 21 de noviembre: M0 = 1/7, M2 = 4/7 y M3 = 2/7. No se vuelven a elegir, porque los candidatos de M4 dependen de los pesos y repetir la selección tras juzgarlos crearía un ciclo. M0, M1 y M3 conservan sus valores de partida (k₁ = 1,2 y b = 0,75; pesos iguales de color y textura; pesos de bloque iguales a 1): ajustar M3 cambiaría los candidatos de M4 y obligaría a repetir la selección de pesos.

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

**Reporte de `no_evaluable`.** Para cada consulta y cada sistema se informa cuántos de los 10 primeros quedaron `no_evaluable`, y en total por sistema. No se fija un umbral para excluir consultas o sistemas: un umbral elegido sin datos previos sería arbitrario. Las métricas se calculan con la regla anterior y la tabla permite al lector ver si algún sistema concentra los pares no evaluables.

**Selección de los pares a juzgar.** Para cada consulta se juzgan los 10 primeros de M0, M1, M2, M3, M3-sin-orden y M4, sin repetir pares. También entran los 10 primeros de la variante de M4 por posiciones recíprocas (sección 7). A ellos se suman 10 candidatos al azar (con semilla fija) y los positivos que proponga el evaluador. Las ablaciones y el control negativo (sección 7) se evalúan sobre ese mismo conjunto: los candidatos no juzgados cuentan como 0 y se informa qué proporción del top 10 quedó juzgada. Si se informan recall o mAP, se calculan respecto de este conjunto.

**Supuesto del pooling.** Los cuatro sistemas de H1 y H2 (M2, M3, M3-sin-orden y M4) aportan sus 10 primeros al pool, de modo que su nDCG@10 no depende de candidatos sin juzgar; solo el ideal de cada consulta puede quedar incompleto si un relevante no entró al pool. El supuesto de que un candidato no juzgado vale 0 afecta solo a las ablaciones y al control negativo, y los favorece o perjudica según cuánto se aparten sus rankings del pool. Por eso, para cada uno se informa la proporción juzgada de su top 10.

**Salvaguardas contra la circularidad.** El investigador anotó la estructura que utiliza M3 y es, además, el evaluador principal. Es la amenaza más seria para la validez del estudio (dictamen del asesor, pregunta 9), y se mitiga de cuatro maneras:

1. Las consultas se fijan antes de ejecutar cualquier sistema sobre ellas: las de T3 por sorteo y las de T1 por redacción.
2. Los juicios se hacen solo sobre las imágenes, sin consultar la anotación ni ver los rankings, las puntuaciones o el sistema que propuso cada candidato. Los candidatos de cada consulta se presentan en orden aleatorio. Una comprobación automática verifica, antes de entregar el libro de juicios, que no contiene el sistema, la puntuación ni la posición en ningún ranking y que el orden de presentación es el sorteado; el informe de la ejecución registra su resultado.
3. La escala y estos criterios se fijan antes de juzgar. Ningún juicio se deriva de la anotación, del descriptor ni de CLIP. Los juicios de desarrollo se revisaron con la segunda opinión ciega de un modelo de visión general, y el evaluador firmó cada grado (R25). Los juicios de prueba se hacen sin ninguna asistencia: el evaluador juzga solo, a ciegas, y su grado es el único que se usa (R27).
4. **Doble juicio parcial [sin segundo evaluador disponible a la fecha]:** el asesor, u otra persona con criterio estructural, juzga a ciegas los pools de 5 consultas de prueba elegidas al azar. Se informa el acuerdo entre ambos evaluadores (kappa ponderado lineal sobre la escala 0–3) antes de cualquier adjudicación, y la métrica primaria se recalcula con esos juicios como análisis de sensibilidad. Se conservan las dos versiones.

**Estabilidad del evaluador (R38).** Los juicios de prueba se emiten una sola vez. No se repite una muestra para estimar la estabilidad intraevaluador, de modo que esa estabilidad no se mide y se declara como limitación (sección 10). La estabilidad que se informa es la de la anotación (lote 1), que no es la de los juicios.

**Consultas sin relevantes.** Si ningún candidato de una consulta alcanza el grado 1, su nDCG no está definido. Esa consulta se excluye de la media, se informa cuántas hubo y cuáles fueron, y no se reemplaza.

## 7. Métricas, inferencia, ablaciones y controles

**Métrica primaria.** nDCG@10 por consulta de T3, con ganancia 2^rel − 1 y descuento log₂(r + 1). El ordenamiento ideal se calcula con todos los juicios de la consulta.

**Métricas secundarias.** P@10 y MRR con la relevancia binarizada en el grado 2, y la proporción juzgada del top 10. En T1 se informan las mismas métricas de forma descriptiva.

**Inferencia [propuesta, D5]:**

- **Estimandos.** Para H1, la media, sobre las consultas de prueba evaluables, de la diferencia pareada por consulta Δ_q = nDCG@10(M4) − nDCG@10(M2): la utilidad del sistema combinado frente a M2. Para la ablación M4 sin M3, la misma media con Δ_q = nDCG@10(M4) − nDCG@10(M4 sin M3): la parte de esa utilidad que se pierde al retirar la estructura, exploratoria. Para H2, la misma media con Δ_q = nDCG@10(M3) − nDCG@10(M3-sin-orden). Para el subgrupo de H2, la media de Δ_q en las consultas con palabra de bandas. Las consultas evaluables son las que tienen nDCG definido para los dos sistemas (sección 6, «Consultas sin relevantes»); n designa su número. La evaluación es transductiva sobre una galería fija, y la inferencia se refiere a estas consultas de la galería congelada (sección 1, población), no a otra colección. El museo, la fotografía, la técnica y la tradición pueden confundir las comparaciones; la heterogeneidad por museo solo se describe, con sus denominadores.
- **Empates.** Una diferencia con |Δ_q| ≤ 1e-12 cuenta como cero, en H1 y en H2, para que los redondeos de coma flotante no conviertan en distinta de cero una diferencia nula por construcción (R35).
- **Contraste de H1 (R34).** Prueba de permutación pareada por cambio de signo, bilateral, con un número fijo de réplicas B = 100 000, semilla fija declarada en la configuración y nivel 0,05. El estadístico es |Σ Δ_q|, y la p es (b + 1) / (B + 1), con b el número de réplicas cuyo estadístico iguala o supera al observado. Se informa el error de Monte Carlo de la p, √[p(1 − p)/B]. El cálculo se detiene solo al completar las B réplicas: no se amplía, no se repite con otra semilla y no se interrumpe a la vista de una p intermedia. Como comprobación se informa la t de Student pareada; si las dos pruebas discrepan, se informa la discrepancia y decide la permutación. En las simulaciones de Urbano, Lima y Hanjalic (2019), con 25 a 100 temas, estas dos pruebas se mantienen cerca del error de tipo I nominal, mientras que el bootstrap usado como prueba tiende a valores p pequeños. Su respaldo cubre las 30 consultas de prueba, pero no menos de 25.
- **Las tres afirmaciones de H1.** La regla de la sección 1 combina tres afirmaciones, que se informan por separado: (a) **frente a cero**, si la permutación da p < 0,05; (b) **estimación**, la diferencia media con su IC 95 %; (c) **relevancia práctica**, si la diferencia media es ≥ 0,03. H1 se sostiene solo si se cumplen (a) y (c). Las demás combinaciones se informan así:
  - p < 0,05 y 0 < Δ < 0,03: «mejora distinta de cero, por debajo del umbral práctico»; H1 no se sostiene.
  - p < 0,05 y Δ < 0: «inferior al sistema de referencia» (M4 inferior a M2); H1 no se sostiene.
  - p ≥ 0,05 y Δ > 0: «dirección favorable sin evidencia suficiente».
  - p ≥ 0,05 y Δ ≤ 0: «no se detectó una mejora».

  La permutación gobierna el contraste frente a cero y el intervalo describe la incertidumbre del efecto; si sus conclusiones aparentes discrepan, se informan ambas sin cambiar el método de decisión. La relevancia práctica se aplica a la diferencia observada: «se sostiene» no afirma que el efecto poblacional alcance 0,03, umbral que no se contrasta. Una p no significativa no demuestra que no haya mejora: con 30 consultas, el estudio solo tiene potencia para efectos del orden del efecto mínimo detectable (más abajo), y el intervalo muestra qué magnitudes siguen siendo compatibles con los datos. Con potencia limitada, un efecto seleccionado por significación puede estar sobrestimado, lo que no implica que necesariamente lo esté. Las 100 000 réplicas son una elección operacional de este estudio, no un mínimo general.
- **Contraste de H2 (R35).** Prueba de permutación pareada por cambio de signo, bilateral y **exacta**: se enumeran los 2^m vectores de signos de las m diferencias distintas de cero, y la p es la proporción de vectores cuyo estadístico |Σ Δ_q| iguala o supera al observado, con la tolerancia de 1e-12 en la comparación. Por construcción, m ≤ b, con b el número de consultas evaluables con palabra de bandas (9 de las 30 consultas de prueba, R27), de modo que la enumeración tiene a lo sumo 512 vectores. Se informan n, b, m y la p mínima alcanzable, 2^(1−m): con m ≤ 5 vale al menos 0,0625 y H2 no puede alcanzar p < 0,05 cualquiera sea el resultado. Si m = 0, p = 1. La t de Student no se informa en H2, porque con m ≤ 9 diferencias distintas de cero su aproximación no es fiable.
- **Supuesto de la prueba exacta.** Bajo la hipótesis nula, en cada consulta las etiquetas «M3» y «M3-sin-orden» son intercambiables, es decir, el signo de Δ_q es igualmente probable en un sentido y en el otro, y las consultas son independientes entre sí. La prueba contrasta la hipótesis nula de que no hay diferencia en ninguna consulta. Con una distribución discreta y pocos valores, la prueba es conservadora: el error de tipo I real puede quedar por debajo de 0,05.
- **Umbral de H2 en el subgrupo.** Como las diferencias son cero fuera del subgrupo de bandas, la media sobre las n consultas es b/n veces la media del subgrupo. El umbral práctico de 0,03 sobre las n consultas equivale, por tanto, a una diferencia media de 0,03 · n/b en el subgrupo: 0,10 con n = 30 y b = 9. Si b = 0, el subgrupo se informa como «no estimable».
- **Intervalo.** El IC 95 % de Δ se obtiene por bootstrap pareado de consultas (percentiles), con 10 000 réplicas, semilla fija y el mismo remuestreo para los dos sistemas. Describe la magnitud y su incertidumbre; no decide las hipótesis.
- Umbral práctico: Δ = 0,03.
- **Potencia.** Con la desviación estándar de Δ observada en las 10 consultas de desarrollo se estima el tamaño necesario, n ≈ [(z₀,₉₇₅ + z₀,₈) · DE(Δ) / 0,03]². Si n supera 30, el estudio se declarará sin potencia suficiente para ese umbral y se informará el intervalo obtenido. El número de consultas de prueba solo puede reducirse antes de abrir el test, nunca después. De forma equivalente, con 30 consultas el efecto mínimo detectable con potencia de 80 % es (z₀,₉₇₅ + z₀,₈) · DE(Δ) / √30 ≈ 0,51 · DE(Δ). No se calcula la potencia a posteriori con el efecto observado en prueba (Card et al., 2020). El cálculo se hizo el 21 de noviembre (R29): para H1, el efecto mínimo detectable es de 0,087, con un rango de 0,060 a 0,159. Es una estimación aproximada de planificación, hecha con la desviación de solo diez consultas, y no una frontera: no garantiza que un efecto mayor se detecte ni que uno menor no se detecte. Para H2 la aproximación normal no vale, porque la distribución de la prueba exacta es discreta y tiene a lo sumo 2^9 valores; en lugar de un efecto mínimo detectable se informa la p mínima alcanzable con el m observado (R35).

**Ablaciones.** Se calculan sobre las mismas consultas y candidatos:
- M4 sin M3, es decir, solo texto e imagen.
- M4 sin M0.
- M4 con M3-sin-orden en lugar de M3.
- M3 solo con bandas frente a M3 solo con motivos y relaciones. El primero usa los bloques de la palabra de bandas y de las adyacencias; el segundo, todos los demás bloques del descriptor (composición, borde, centro, simetría, repetición, motivos y familia iconográfica), de modo que los dos cubren el descriptor sin solaparse (R32).
- M4 por posiciones recíprocas (M4-RRF) **[propuesta]**: puntuación = Σ_c 1 / (60 + r_c), con r_c la posición del candidato en el ranking de c ∈ {M0, M2, M3} (Cormack, Clarke y Büttcher, 2009). No tiene pesos que ajustar, de modo que muestra cuánto del resultado de M4 depende del ajuste con las 10 consultas de desarrollo. Los pares sin evidencia estructural ocupan las últimas posiciones del ranking de M3, por `id_global`. Es exploratoria y no interviene en H3, porque al usar posiciones no conserva la descomposición de la puntuación.

**Control negativo.** M4 con los descriptores de M3 permutados al azar entre piezas del mismo museo, con una sola permutación de semilla fija declarada en la configuración. La permutación dentro del museo conserva la distribución de los descriptores en cada fuente y rompe solo su correspondencia con la imagen. Si el aporte de la estructura a M4 es real, la diferencia entre M4 y M4 con el control debe ser positiva, y el control no debería mejorar a M4 sin M3. Se informa como diferencia pareada con su IC 95 %, de forma descriptiva: una sola permutación no da una distribución nula y no decide ninguna hipótesis. No se usan permutaciones adicionales.

**Informe de resultados.** El informe de la ejecución (`outputs/reports/experimento_v2_resultados.md`) sigue una plantilla fijada antes del test, que genera el código y que una prueba automática comprueba. Todos los análisis previstos se informan, cualquiera sea el signo del resultado, incluidos los nulos. Tablas, en este orden:

1. Integridad de la corrida: identificador, estado, commit, huellas comprobadas y resultado de las comprobaciones de fugas y de cegamiento (sección 9).
2. Pool y juicios: por consulta, pares del pool, juzgados, relevantes y `no_evaluable`; por sistema, `no_evaluable` y proporción juzgada del top 10; consultas sin relevantes; y la sensibilidad al pooling, con el nDCG@10 de cada sistema recalculado tras tratar como no juzgados los pares que solo él aportó (Buckley et al., 2007).
3. H1: n, diferencia media, IC 95 %, p de la permutación con su error de Monte Carlo, t pareada, las tres afirmaciones y el veredicto.
4. H2: n, b, m, p exacta, p mínima alcanzable, diferencia media e IC 95 %; si se aplicó la compuerta de H1 y el veredicto o la indicación de «exploratoria». Subgrupo de bandas: diferencia media, IC 95 % y umbral equivalente.
5. H3: error máximo de reconstrucción y de intervención y número de resultados comprobados; aparte, el resumen descriptivo de la revisión humana (sección 8).
6. Métricas primaria y secundarias de todos los sistemas, por consulta y en media.
7. Ablaciones, control negativo y M4-RRF, como diferencias pareadas con su IC 95 %.
8. Robustez por museo y por estado de la pieza.
9. T1, descriptiva.
10. Desviaciones del protocolo, si las hubo, con su motivo.

**Robustez (exploratoria).** Resultados según el museo de la consulta y según el estado de la pieza. El estado es la completitud que el revisor escribió en el motivo de su decisión de curación: completo, incompleto o sin dato, porque 61 de las 150 piezas de la galería no la mencionan (R32). Con estos tamaños de muestra, el análisis es descriptivo.

**T1 (exploratoria).** M0 compara la descripción con el texto de las fichas; M2, el vector de texto de la descripción con los vectores de imagen; M3 solo participa si la consulta trae especificación estructural y compara solo esos bloques; M4 fusiona los componentes disponibles con los pesos de T3. La muestra al azar del pool se elige entre los candidatos que no proponen M0 ni M2 (R32). Sus métricas se informan de forma descriptiva.

## 8. Fidelidad computacional (H3) y revisión de las explicaciones

Para cada resultado del top 10 de M4 en prueba se registran las contribuciones α_c ŝ_c de cada componente, la máscara de observabilidad y la procedencia de cada valor. H3 afirma la fidelidad computacional de la descomposición de M4: que la explicación es la puntuación, y no una aproximación a ella. Se sostiene si se cumplen dos comprobaciones (R36):

1. **Reconstrucción:** la suma de las contribuciones coincide con la puntuación, con un error ≤ 1e-9, en todos los resultados.
2. **Intervención:** retirar un componente modifica la puntuación exactamente como predice la fórmula, incluida la regla de reparto de pesos, con el mismo error máximo. Se verifica con pruebas de propiedades y sobre todos los resultados de prueba.

H3 no afirma que las explicaciones sean útiles ni que coincidan con el criterio de un experto: eso no lo prueba la descomposición.

**Revisión humana de las explicaciones (descriptiva).** Es un análisis aparte, que no interviene en el veredicto de H3:

- **Clases.** Un *acierto* es un resultado del top 10 de M4 juzgado relevante (grado ≥ 2, la binarización de la sección 7); un *error*, un resultado del top 10 de M4 juzgado con grado 0 o 1. Los pares `no_evaluable` no entran en ninguna clase.
- **Muestra.** Se sortean 5 aciertos y 5 errores entre los resultados de prueba, con semilla fija declarada en la configuración. Si una clase tiene menos de 5 resultados, se usan todos y se informa cuántos había.
- **Ficha ciega.** Para cada resultado, la ficha muestra las dos imágenes y las contribuciones de cada componente con sus valores y su procedencia, sin la clase, el grado ni la posición en el ranking, y en orden aleatorio.
- **Juicio.** Con la rúbrica de la ficha, el evaluador indica si la explicación es correcta (las contribuciones corresponden a lo que se ve en las imágenes), incorrecta (alguna contribución contradice lo que se ve) o especulativa (atribuye a un componente un rasgo que no se puede verificar en las imágenes), o la marca `no_evaluable` si las imágenes no permiten decidir. Con incorrecta o especulativa registra el código de desacuerdo (el componente cuya contribución no corresponde: M0, M2, M3 o varios) y una justificación. Un validador comprueba los campos.
- **Denominador.** Las fichas sorteadas. Las `no_evaluable` se informan y no se reemplazan, y no se completan cuotas.
- **Límite.** La revisión no es independiente: el revisor es el evaluador y anotó la estructura que usa M3. Se informa como descripción de casos, sin tasas ni contraste.

## 9. Congelación y criterios de suspensión

El experimento sigue un orden obligatorio:

1. Se congelan los grupos, las particiones y la anotación. Las correcciones de criterios y de vocabulario que resulten de la re-anotación del lote 1 se aplican y se registran **antes** de este punto.
2. Desarrollo: rankings, juicios de desarrollo, ajuste de pesos y estimación de la potencia.
3. Autorización del protocolo por el asesor (R30) y congelación de los sistemas.
4. Ejecución única del test, en la secuencia de estados que sigue (R37).

**Secuencia y estados de la corrida.** Cada corrida tiene un identificador único y avanza por estados que se registran en el manifiesto de ejecución; ningún paso se ejecuta si el estado anterior no está registrado:

| Estado | Qué se hace | Qué queda sellado |
|---|---|---|
| `autorizada` | Se registran en `[ejecucion]` de `config/experimento.toml` la fecha, el commit y la suma SHA-256 de este protocolo, y se crea una etiqueta Git anotada en ese commit | Protocolo y código |
| `insumos_sellados` | Se escribe el manifiesto **antes** de calcular ningún ranking: commit, sumas SHA-256 de todos los insumos obligatorios (particiones, consultas, anotación congelada, vectores de M2, índices de M1, configuración, protocolo), huella de la rúbrica, las instrucciones y los parámetros de pooling de los libros de juicio, checkpoint, parámetros, semillas, versiones y hardware. Un insumo obligatorio ausente detiene la corrida, y también un archivo versionado con cambios sin commit | Insumos y reglas de juicio |
| `rankings_sellados` | Se calculan los rankings de prueba de T3 y T1 y el pool, y sus sumas se añaden al manifiesto | Rankings y pool |
| `juicios_cerrados` | Se entregan los libros ciegos, se juzgan (incluido el doble juicio parcial, si hay segundo evaluador) y se cierran; su suma se añade al manifiesto | Juicios |
| `evaluada` | Se recalculan todas las sumas del manifiesto; solo si coinciden se calculan las métricas y el informe | Resultados |

**Gestión de fallos.** Cada paso escribe sus salidas en archivos temporales y las publica de una vez al terminar, de modo que un fallo no deja salidas parciales con el nombre definitivo. Si un paso falla antes de publicar, el estado no avanza, el fallo se anota en el registro de custodia y el paso puede repetirse con el mismo código y los mismos insumos, que son deterministas; esa reanudación solo procede desde un estado sellado y cuando no existen resultados interpretables. Una vez sellados los rankings, una segunda ejecución de `--rankings` se rechaza. Los libros de juicio se comprueban contra el pool sellado y contra la rúbrica registrada antes de entregarse y al cerrarse. Si `--evaluar` encuentra una suma que no coincide, un archivo de otra corrida o un estado que falta, la corrida queda **suspendida**: no se calculan métricas, se informa al asesor y no se repite ningún paso sin su conformidad. Ningún ranking publicado se regenera con otro código ni con otros parámetros.

**Custodia (R37).** No se usa una firma criptográfica personal. La custodia se acredita con tres elementos: una etiqueta Git anotada en cada cambio de estado; el registro `docs/registro_custodia.md`, con la fecha, el responsable, el identificador de la corrida, el commit y las sumas SHA-256 de cada estado; y el envío de esas sumas al asesor por correo en el momento de sellarlas, que deja una constancia fuera del repositorio. El registro está bajo control de cambios en el repositorio, de modo que cualquier modificación posterior queda a la vista. El investigador adjunta, con la solicitud de autorización, una declaración escrita de no haber ejecutado ningún sistema sobre las consultas de prueba.

**El test no se abre** si se da alguna de estas condiciones (informe 10 de la auditoría):
- hay grupos de piezas relacionadas repartidos entre particiones;
- algún juicio se derivó del descriptor o de CLIP;
- la guía de anotación o este protocolo cambiaron sin registro;
- algún peso se ajustó con datos de prueba;
- alguna imagen no está verificada;
- falta el manifiesto de ejecución, o alguna suma registrada en él no coincide con el archivo.

Antes de abrir el test se ejecuta una comprobación automática de fugas: que ningún grupo esté en dos particiones y que ninguna consulta figure entre sus propios candidatos. La suspensión protege el test, pero no impide preparar código ni trabajar con los datos de desarrollo.

**Autorización y ejecución (R30, R32 y R37).** Al autorizarse el protocolo se registran en `[ejecucion]` de `config/experimento.toml` la fecha y el commit de la autorización y la suma SHA-256 de este documento. La comprobación previa (`python -m src.experimento.ejecucion_prueba --comprobar`) verifica las condiciones anteriores que pueden comprobarse en el repositorio: la aprobación y que el protocolo no cambió después, las particiones y las consultas, la anotación congelada y sus condiciones de buena formación, los pesos de M4, las sumas de las imágenes de M1 y M2, las consultas T1 y que el test no se haya ejecutado antes. La ejecución de los rankings se niega si encuentra un problema.

## 10. Amenazas a la validez y limitaciones

| Amenaza | Mitigación | Limitación que se declara |
|---|---|---|
| Circularidad: un mismo investigador anota, diseña y juzga | Juicio ciego y aleatorizado, consultas fijadas de antemano y doble juicio parcial preparado | Sesgo residual a favor de M3; es la limitación principal |
| Un solo evaluador | Doble juicio parcial en 5 consultas, preparado para cuando haya un segundo evaluador (no disponible a la fecha, R27) | Sin segundo evaluador, no se mide el acuerdo entre evaluadores; con él, se estimaría con una muestra pequeña |
| Juicios de desarrollo asistidos (R25) | Uso limitado a los pesos de M4 y a la potencia; juicios de prueba sin asistencia; archivo de auditoría con huella registrada (R39) | Los pesos y la potencia heredan la reserva, incluido el riesgo de que el evaluador se anclara en la segunda opinión |
| Estabilidad del evaluador en prueba | Juicio ciego con escala fijada de antemano | No se mide la estabilidad intraevaluador de los juicios de prueba: no hay rejuicio (R38) |
| Anotación con revisión asistida (R20) | Los juicios de prueba se emiten sin asistencia | M3 y M4 usan la anotación congelada, cuya revisión incluyó propuestas automáticas |
| H2 con pocas diferencias distintas de cero | Prueba exacta y análisis del subgrupo de bandas | Con m ≤ 5 la p no puede bajar de 0,05; la compuerta de H1 hace improbable una conclusión confirmatoria |
| Revisión humana de las explicaciones | Ficha ciega y muestra sorteada | No es independiente y no interviene en H3 |
| Control negativo con una sola permutación | Semilla fija y permutación dentro del museo | Es descriptivo; no da una distribución nula |
| Duplicados y vistas de una misma pieza | Grupos decididos antes de partir y comprobación de fugas | Relaciones que no detecte ninguna señal |
| Pocas consultas de prueba (30) | Prueba de permutación pareada, intervalo pareado y efecto mínimo detectable estimado en desarrollo | Intervalos amplios; alcance de piloto; potencia insuficiente para detectar una diferencia de 0,03 |
| Generalización | Población de inferencia declarada (sección 1) | Las conclusiones se restringen a la colección elegible de la galería congelada |
| Costo de la anotación | Se declara | M3 y M4 dependen de una anotación humana cuyo costo no se midió; el resultado no demuestra su disponibilidad a escala |
| Juicio solo de los primeros candidatos (pooling) | Unión de los 10 primeros de siete sistemas (M0, M1, M2, M3, M3-sin-orden, M4 y M4-RRF) más una muestra al azar | Sesgo hacia los sistemas que aportan candidatos; se informa la proporción juzgada |
| Diferencias de fotografía entre museos | Resultados por museo | Tamaños pequeños por museo |
| M3 asistido por anotación | Se declara, y M3 excluye el color | No mide la extracción automática de la estructura |
| Un solo anotador | Acuerdo intra-anotador en el lote 1, informado por atributo; kappa < 0,6 como señal de revisión | Mide estabilidad, no acuerdo entre personas; el criterio queda por debajo del 0,8 que proponen Artstein y Poesio (2008) |
| Pesos de M4 ajustados con 10 consultas | Rejilla pequeña, selección única (R28) y ablación sin pesos por posiciones recíprocas | El ajuste puede no ser estable |

## 11. Estado y calendario restante

| Etapa (plan de cierre) | Estado al 23 de noviembre |
|---|---|
| Protocolo (S1.3), grupos y particiones (S1.7, S2.2 y S2.3), especificación de M3 (S2.5), M0 y M1 (S2.6), consultas T1 (S2.7) | Hecho el 5 y el 6 de noviembre, salvo la aprobación del protocolo |
| Re-anotación del lote 1 (S2.1), aclaración de la guía, revisión de criterios y congelación de la anotación v2.1 | Hecho entre el 12 y el 17 de noviembre (R12 a R23) |
| Juicios de desarrollo (S3.2) | 419 pares juzgados (R24, R25 y R28) |
| Rankings de M3 y M4, pesos de M4 y efecto mínimo detectable | Hecho el 21 de noviembre (R28 y R29) |
| Dictamen del asesor sobre la versión 0.6.5 | Recibido el 21 de noviembre: favorable al diseño piloto; la apertura queda condicionada a acreditar sus observaciones en un nuevo commit con pruebas automáticas (R33 a R39) |
| Autorización del protocolo | Pendiente; el test no se abre antes (R30) |
| Congelación de los sistemas (S3.3), juicios de prueba y doble juicio parcial (S3.4) | Después de la autorización; el código del test se prepara con datos de desarrollo |
| Test, ablaciones e interpretabilidad (S4.1 a S4.3) | Después de los juicios de prueba |

El calendario original del plan de cierre preveía el test entre el 18 y el 19 de noviembre. Se desplazó por el atraso de los juicios de desarrollo y por la revisión de criterios de la anotación, y se fija ahora en función de la autorización del asesor.

**Carga estimada de juicios**, con un supuesto de 30 s por juicio:
- Prueba en T3: unos 1600 pares, alrededor de 13 h.
- T1: unos 240 pares, alrededor de 2 h.
- Doble juicio parcial: unos 200 pares, alrededor de 1,7 h para el segundo evaluador.

El número de consultas de prueba se mantiene en 30 (R27). Solo podría reducirse antes de abrir el test.

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
| Ejecución única del test | `python -m src.experimento.ejecucion_prueba` con `--comprobar`, `--rankings`, `--crear-juicios`, `--cerrar-juicios`, `--crear-revision-h3` y `--evaluar`, en ese orden; vectores de texto de T1 con `python -m src.modelos.m2_openclip --textos-t1`. Escribe el manifiesto de ejecución con sus estados, los rankings y el pool de prueba, los libros ciegos `data/metadata/juicios_prueba_v2.xlsx` y `juicios_t1_v2.xlsx`, las fichas de la revisión de H3 (`data/metadata/revision_h3_v2.xlsx`), las métricas por consulta y el informe de resultados |
| Custodia | `docs/registro_custodia.md` y etiquetas Git anotadas por estado (sección 9) |

El evaluador no abre los rankings, los archivos que registran qué sistema propuso cada par (`data/processed/experimento_v2_pool_desarrollo.csv` y, en prueba, `experimento_v2_pool_prueba.csv` y `experimento_v2_pool_t1.csv`), la clase de cada ficha de H3 (`data/processed/experimento_v2_revision_h3_muestra.csv`) ni los informes con el rendimiento de los sistemas en desarrollo (selección de pesos de M4). Hasta cerrar la re-anotación del lote 1, el 12 de noviembre, tampoco abrió `consultas_t3_v2.csv` ni `anotaciones_v2.csv`, porque contenían datos de la primera anotación. Los libros de consultas T1 y de juicios incluyen una hoja de ejemplos hipotéticos que ilustran el formato y la escala; no son piezas de la galería ni consultas.

Las equivalencias con los nombres del informe 08 son las siguientes: grupos (`groups.csv`), particiones (`splits.csv`), consultas (`queries.csv`), juicios (`qrels.csv`), métricas por consulta (`metrics_by_query.csv`), modelos (`models.toml`) y manifiesto de ejecución (`run_manifest.json`).

## Historial

| Fecha | Versión | Cambio |
|---|---|---|
| 2026-11-05 | 0.1 | Propuesta inicial para la aprobación del asesor |
| 2026-11-05 | 0.2 | M2: checkpoint, precisión y encuadre fijados (D6) al calcular los embeddings, antes de cualquier consulta, juicio o ranking de la galería. Sección 2: señales, umbrales y regla de duda de los grupos |
| 2026-11-06 | 0.3 | Sección 2: grupos también sobre el complementario. Sección 5: particiones y consultas T3 congeladas, regla de reemplazo y valores en `config/experimento.toml` |
| 2026-11-06 | 0.4 | Sección 4: M0 sin la descripción plantilla de MET; M1 sobre el textil segmentado; M3 especificado en `docs/especificacion_m3.md`. Rankings de desarrollo de M0, M1 y M2, sin ejecutar ninguna consulta de prueba. Sección 6: libros de consultas T1 y de juicios de desarrollo, con ejemplos hipotéticos |
| 2026-11-06 | 0.5 | Revisión de la redacción para la lectura del asesor y calendario actualizado; los detalles de implementación pasan a la sección 12. Sin cambios en el diseño |
| 2026-11-12 | 0.6 | Secciones 1 y 7: H1 y H2 se deciden con una prueba de permutación pareada y el bootstrap queda para el intervalo; el efecto mínimo detectable se calcula antes del test. Secciones 6 y 7: ablación de M4 por posiciones recíprocas, cuyos candidatos entran al pool. Sección 10: amenazas actualizadas. Son las decisiones R01 a R04 de `docs/registro_decisiones.md`, tomadas a partir de la revisión bibliográfica del 11 de noviembre. No se ha ejecutado ninguna consulta de prueba |
| 2026-11-12 | 0.6.1 | Correcciones de forma de la auditoría interna (R11): calendario al 12 de noviembre y D7 fuera de las decisiones por ratificar. Sin cambios en el diseño |
| 2026-11-19 | 0.6.2 | Sección 6, salvaguarda 3: los juicios de desarrollo se revisaron con una segunda opinión ciega y el evaluador firmó cada grado; queda pendiente decidir si los juicios de prueba se hacen igual (R25). No se ha ejecutado ninguna consulta de prueba |
| 2026-11-21 | 0.6.3 | Sección 1: H2 se decide sobre las 30 consultas de prueba y se añade un análisis secundario en las consultas con palabra de bandas, donde la diferencia puede ser distinta de cero. Sección 6: los juicios de prueba se hacen sin asistencia; no hay segundo evaluador disponible y el doble juicio queda preparado para cuando lo haya. Decisión R27 del investigador, tomada sin ejecutar ninguna consulta de prueba |
| 2026-11-21 | 0.6.4 | Estado y sección 9: el test espera la aprobación del asesor. Sección 4: regla de desempate de los pesos de M4, M4-RRF en la tabla de sistemas, pesos elegidos y parámetros de M0, M1 y M3 fijos en sus valores de partida. Sección 7: resultado del efecto mínimo detectable y alcance de la referencia sobre el error de tipo I. Sección 10: juicios de desarrollo asistidos y salvedad del doble juicio; siete sistemas en el pool. Sección 11: estado al 21 de noviembre. «Score» pasa a «puntuación». Decisiones R28 a R30; no se ha ejecutado ninguna consulta de prueba |
| 2026-11-21 | 0.6.5 | Sección 7: definición de la ablación de M3 por bloques, de la robustez por completitud (tres grupos) y del cálculo de T1. Sección 4: M2 en T1 sin plantilla. Sección 9: registro de la aprobación y comprobación previa automática. Sección 12: ejecución única del test. Decisión R32; no se ha ejecutado ninguna consulta de prueba |
| 2026-11-23 | 0.6.6 | Respuesta al dictamen del asesor del 21 de noviembre. Sección 1: regla secuencial de H1 y H2 en lugar de «al ser una sola»; alcance de H1 (la fusión enriquecida frente a M2, sin aislar la estructura); H3 como fidelidad computacional. Sección 6: reporte de `no_evaluable`, supuesto del pooling, comprobación del cegamiento y estabilidad del evaluador no medida. Sección 7: estimandos, tolerancia de empates, H1 con 100 000 réplicas fijas, error de Monte Carlo y tres afirmaciones; H2 con p exacta por enumeración; el efecto mínimo detectable como estimación de planificación y sin aproximación normal en H2; control negativo descriptivo; plantilla del informe de resultados. Sección 8: revisión humana descriptiva, con clases, muestreo y ficha ciega. Sección 9: estados de la corrida, manifiesto antes de los rankings, gestión de fallos y custodia. Sección 10: nuevas limitaciones. Sección 12: órdenes `--cerrar-juicios` y `--crear-revision-h3` y registro de custodia. Decisiones R33 a R39; no se ha ejecutado ninguna consulta de prueba |
