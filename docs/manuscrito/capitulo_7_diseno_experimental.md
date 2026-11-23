# 7. Diseño experimental

> **Borrador 0.2, 23 de noviembre de 2026.** Capítulo de la segunda parte de la tesis. Sustituye al capítulo 7 del primer avance («Plan experimental preliminar»), que no se corrige. Describe el protocolo experimental en su versión 0.6.6, que incorpora las observaciones del dictamen del asesor del 21 de noviembre y espera su autorización, y las decisiones registradas hasta la R39. A la fecha de este borrador no se ha ejecutado ningún sistema sobre las consultas de prueba. El capítulo no informa el rendimiento de ningún sistema en desarrollo: el evaluador debe juzgar la prueba sin conocerlo.

## 7.1 Principios del diseño

El plan experimental del primer avance proponía comparar una línea base visión-lenguaje, un descriptor combinatorio y un modelo híbrido en cuatro tareas, con relevancia definida a partir de coincidencias de tipo de objeto, técnica, cultura o composición. Ese plan dejaba abiertas tres cuestiones que deciden si un resultado puede atribuirse al método: qué cuenta como resultado pertinente y quién lo decide, cómo se evita que el ajuste de los sistemas use los mismos datos con que se evalúan, y qué resultado sostendría o refutaría cada hipótesis. Este capítulo las resuelve con cinco principios.

1. **Protocolo previo.** Qué se compara, con qué datos, cómo se mide y qué se considera evidencia se fija por escrito antes de observar cualquier resultado de prueba. Todo cambio posterior se registra con su fecha y su motivo.
2. **Separación entre desarrollo y prueba.** Todo lo que tiene un parámetro se fija con datos de desarrollo. La prueba se ejecuta una sola vez, con los sistemas congelados.
3. **Relevancia juzgada por una persona y a ciegas.** La pertinencia no se deriva de metadatos, de la anotación ni de un modelo: la decide un evaluador que ve solo las imágenes, sin saber qué sistema propuso cada candidato.
4. **Comparaciones de alcance declarado.** La utilidad del sistema combinado se mide frente al codificador visual que contiene (H1). Esa comparación no aísla la estructura, porque la fusión también añade el texto de la ficha; el aporte de la estructura se examina en las ablaciones, que son exploratorias, y el del orden frente a un control que conserva todo lo demás (H2).
5. **Resultados negativos válidos.** El diseño permite afirmar que la estructura no aporta, si ese es el resultado, con la misma solidez que lo contrario.

Los dos primeros principios siguen la práctica del registro previo de análisis y de la separación estricta entre ajuste y evaluación; el tercero responde al riesgo de circularidad entre anotación, sistema y juicio, que es la amenaza más seria del estudio (sección 7.13).

## 7.2 Galería, unidades y particiones

**Galería.** La galería está formada por las 150 piezas del núcleo de anotación, que son las únicas con anotación estructural (capítulo 4, sección 4.8). El resto del corpus principal queda fuera del experimento.

**Unidad de partición.** Varios registros pueden mostrar un mismo objeto o partes de él, y recuperar uno a partir de otro no prueba nada sobre la representación. Por eso la galería se parte por grupos de piezas relacionadas y no por registros (capítulo 4, sección 4.6; capítulo 5, definición 5.2). Las 150 piezas pertenecen a 146 grupos. Los grupos se reparten en desarrollo (30 %) y prueba (70 %), estratificados por museo, con una semilla fija: 44 grupos de desarrollo y 102 de prueba. Una comprobación automática verifica, en cada ejecución del flujo, que ningún grupo esté en las dos particiones y que ninguna consulta figure entre sus propios candidatos.

**Unidad de análisis.** Las métricas se calculan por consulta, y la inferencia remuestrea consultas.

**Galería transductiva.** La galería es fija y contiene piezas de las dos particiones: una consulta de desarrollo puede recuperar una pieza de prueba y viceversa. Los juicios de desarrollo se usan para ajustar los sistemas; los de prueba, nunca. Los sistemas ven las piezas de prueba, pero no sus relevancias. La evaluación se declara, por tanto, como recuperación transductiva.

**Imagen.** Todos los sistemas usan la copia de evaluación de cada pieza (1600 píxeles de lado mayor), que es la misma sobre la que se hizo la anotación, verificada contra su suma SHA-256.

## 7.3 Tareas

**Cuadro 7.1.** Tareas del experimento.

| Tarea | Consulta | Candidatos | Relevancia | Sistemas | Papel |
|---|---|---|---|---|---|
| T3: estructura por ejemplar | Una pieza de la galería: su imagen y, para M0, el texto de su ficha | Las demás piezas de la galería, excluido el grupo de la consulta | Similitud de la organización visible (sección 7.6) | M0 a M4, M3-sin-orden, ablaciones y control negativo | Primaria: H1, H2 y H3 |
| T1: texto a imagen | Una descripción en español redactada por el evaluador, sin copiar fichas, con una especificación estructural opcional | Toda la galería | Cumplimiento visible de la descripción | M0, M2 y M4; M3 solo si la consulta trae especificación | Secundaria y exploratoria |

En T3, M0 recibe el texto de la ficha de la pieza consultada en lugar de su imagen; es una condición distinta y se identifica como tal. M1 no procesa texto y no participa en T1. Ninguna tabla se completa con valores para modalidades que un sistema no tiene. Las tareas del primer avance que quedan fuera (recuperación de imagen a texto y agrupamiento exploratorio) se justifican en el capítulo 2, sección 2.2.

## 7.4 Sistemas

Todos los sistemas son deterministas y ninguno se entrena. Los empates en la puntuación se resuelven por el identificador global de la pieza, en orden ascendente.

**Cuadro 7.2.** Sistemas comparados.

| Sistema | Entrada y puntuación | Parámetros y su origen |
|---|---|---|
| M0 | BM25 sobre el texto de la ficha: título original, título sugerido en español, descripción del museo, material y técnica. Se excluye la descripción de MET, que no es un texto del museo sino una plantilla armada con los propios metadatos; sus palabras fijas aproximarían las piezas de MET entre sí solo por proceder del mismo museo | k₁ = 1,2 y b = 0,75, valores habituales de Okapi BM25; términos de tres caracteres o más, sin lista de palabras vacías |
| M1 | Visión convencional sobre el textil separado del fondo: histograma conjunto en CIELAB (4 × 8 × 8 cubetas) e histograma de patrones binarios locales de 8 vecinos invariante a la rotación (10 valores), calculados a 320 píxeles de lado mayor. Disimilitud: media de la mitad de la distancia L1 por bloque | Pesos iguales de color y textura |
| M2 | OpenCLIP congelado, `xlm-roberta-base-ViT-B-32` con pesos `laion5b_s13b_b90k`: vectores de imagen normalizados, comparados por coseno. Cálculo en fp32. Antes del recorte central del modelo, cada imagen se lleva a un cuadrado rellenado con el color de su borde, para no cortar los extremos de las piezas alargadas | Punto de control y encuadre fijados el 5 de noviembre, antes de cualquier consulta |
| M3 | Descriptor estructural sobre la anotación congelada v2.1: composición, palabra de bandas en forma canónica, adyacencias, borde, centro, simetría, repetición, motivos y familia iconográfica, con máscara de observabilidad. Disimilitud mixta D(i, j) (capítulo 5, ecuación 5.17). No incluye el color, para que una eventual ganancia no sea de origen cromático | Pesos de bloque iguales a 1 |
| M3-sin-orden | Igual que M3, con la palabra de bandas sustituida por el histograma de sus tipos y sin adyacencias | Los mismos pesos que M3 |
| M4 | Fusión tardía aditiva de M0, M2 y M3 con puntuaciones normalizadas por consulta; si M3 no tiene evidencia para un par, su peso se reparte entre los demás (capítulo 5, ecuación 5.21) | Pesos 1/7, 4/7 y 2/7, elegidos en desarrollo (sección 7.9) |
| M4-RRF | Fusión por posiciones recíprocas: Σ_c 1 / (60 + r_c) sobre los rankings de M0, M2 y M3 (Cormack et al., 2009). Los pares sin evidencia estructural ocupan las últimas posiciones del ranking de M3 | Sin pesos; k = 60 fijo |

M3 y M4 se declaran **sistemas asistidos por anotación**: disponen de etiquetas asignadas por una persona. La comparación con M2 mide la utilidad de disponer de ese conocimiento, no la capacidad de extraerlo de la imagen.

Los parámetros de M0, M1 y M3 conservan los valores de partida declarados antes de ejecutar ninguna consulta. El protocolo permitía ajustarlos en desarrollo, pero el investigador decidió no hacerlo mientras el asesor no se pronunciara sobre la reserva que afectaba a los juicios de desarrollo (decisiones R17 y R24; sección 7.6.4). Una vez elegidos los pesos de M4 con M3 en sus valores de partida, ajustar M3 cambiaría los candidatos de la fusión y obligaría a repetir esa selección (sección 7.9), de modo que los valores de partida quedan fijos. El único ajuste realizado con datos de desarrollo es el de los pesos de M4.

## 7.5 Consultas

**Consultas de T3.** Se sortearon 10 consultas de desarrollo entre los grupos de desarrollo y 30 de prueba entre los grupos de prueba, con una semilla fija, a lo sumo una por grupo y solo entre piezas cuya composición es observable. El sorteo se estratificó por museo y por tipo de composición, con cuotas por el método de los mayores restos, y no consultó ningún ranking. Se hizo el 6 de noviembre, antes de ejecutar cualquier sistema.

**Regla de reemplazo.** Si, al corregir la anotación, una consulta deja de tener composición observable, se reemplaza por la siguiente pieza elegible de su estrato, en el orden que fija la semilla. La regla se aplicó una vez: la consulta de prueba T3-P06 se había sorteado sobre una pieza cuya anotación describía, por un desplazamiento de filas, la imagen de otro registro; con la anotación correcta, su composición no es observable, y la sustituyó la siguiente pieza de su estrato (capítulo 4, sección 4.10). Ninguna consulta de prueba tenía rankings ni juicios en ese momento.

**Consultas de T1.** Seis consultas, solo de prueba, redactadas por el evaluador antes de ejecutar ningún sistema sobre ellas. Al no tener desarrollo propio, usan los pesos fijados en T3.

**Consultas con palabra de bandas.** De las 30 consultas de prueba, 9 corresponden a piezas con palabra de bandas; en desarrollo, 2 de 10. Este dato, que procede solo de la anotación, condiciona la potencia de H2 (sección 7.8).

## 7.6 Juicios de relevancia

### 7.6.1 Escala

Cada par formado por una consulta y un candidato se juzga en cuatro grados.

**Cuadro 7.3.** Escala de relevancia.

| Grado | T3 (estructura) | T1 (texto) |
|---|---|---|
| 3 | Misma organización: tipo de composición, secuencia de bandas o regiones y relaciones, aunque cambien colores y motivos | Cumple toda la descripción |
| 2 | Misma composición, con diferencias en la secuencia o en las relaciones | Cumple lo principal |
| 1 | Comparte un rasgo estructural parcial | Cumple un rasgo |
| 0 | Organización distinta | No la cumple |

El estado `no_evaluable` se reserva para imágenes que no permiten juzgar. No equivale a 0: el par se excluye del ordenamiento ideal de la consulta y se informa su frecuencia. Todo juicio de grado 2 o 3 lleva una justificación breve que indique la evidencia visible.

### 7.6.2 Selección de los pares

Para cada consulta se juzgan los 10 primeros candidatos de M0, M1, M2, M3, M3-sin-orden, M4 y M4-RRF, sin repetir pares, más 10 candidatos elegidos al azar con semilla fija entre los que no proponen M0, M1 ni M2. La muestra al azar se define respecto de los sistemas del pool inicial para que no cambie al añadir otros sistemas: el pool solo crece. Los candidatos no juzgados cuentan como 0, y se informa qué proporción del top 10 de cada sistema quedó juzgada. Las ablaciones y el control negativo se evalúan sobre el mismo conjunto de juicios.

Ese valor 0 es un supuesto de evaluación y no un juicio: no juzgado no es lo mismo que juzgado irrelevante. Como los cuatro sistemas de H1 y H2 aportan sus diez primeros al pool, su nDCG@10 no depende de él; solo el ordenamiento ideal puede quedar incompleto si un relevante no entró al pool. El supuesto sí afecta a las ablaciones y al control negativo. Por eso el informe incluye, por consulta, el tamaño del pool, los pares juzgados, los relevantes y los `no_evaluable`, y por sistema, la proporción juzgada de su top 10 y una sensibilidad: su nDCG@10 recalculado tras tratar como no juzgados los pares que solo él aportó, la prueba que proponen Buckley et al. (2007). Los `no_evaluable` se cuentan por consulta y sistema, sin un umbral de exclusión, que habría que fijar sin datos que lo justificaran.

La unión de los primeros resultados de todos los sistemas comparados protege a M3 y M4 del sesgo conservador del pooling, que infravalora a los sistemas cuyos resultados no entraron al pool (Buckley et al., 2007, pp. 16–17). La muestra al azar ofrece una referencia independiente de los sistemas y coincide con una de las vías que esos autores proponen, aunque su interacción con el sesgo no está estudiada (p. 15).

En desarrollo, el pool reúne 419 pares. En prueba se estima en unos 1600 pares, alrededor de 13 horas de juicio con 30 segundos por par.

### 7.6.3 Salvaguardas frente a la circularidad

El investigador definió el esquema de anotación, anotó las 150 piezas y es el evaluador. Su noción de similitud estructural se formó con las mismas categorías que usa M3, de modo que sus juicios pueden favorecer al descriptor sin que medie intención. Soboroff (2025) formula el principio general: un juez que comparte información con un sistema evaluado deja de ser un árbitro independiente. Las salvaguardas son de procedimiento:

1. Las consultas se fijaron antes de ejecutar cualquier sistema sobre ellas: las de T3 por sorteo y las de T1 por redacción.
2. Los juicios se hacen solo sobre las imágenes, sin consultar la anotación ni ver los rankings, las puntuaciones o el sistema que propuso cada candidato. Los candidatos de cada consulta se presentan en orden aleatorio, que evita favorecer a los documentos que muchos sistemas devuelven arriba (Sakai et al., 2022, pp. 16–17). La columna «orden» del libro es ese orden de presentación, no una posición en ningún ranking. Una comprobación automática verifica, antes de entregar el libro y al cerrarlo, que no contiene el sistema, la puntuación ni la posición, que conserva el orden sorteado y que su guía coincide con la rúbrica y las instrucciones selladas al iniciar la corrida.
3. La escala y sus criterios se fijaron antes de juzgar. Ningún juicio se deriva de la anotación, del descriptor ni de CLIP.
4. El evaluador no abre ningún informe que contenga el rendimiento de los sistemas en desarrollo.

Estas medidas impiden que el evaluador sepa qué sistema propuso cada candidato. No impiden que su criterio coincida con el del descriptor. La mitigación externa prevista es un doble juicio parcial: otra persona con criterio estructural juzga a ciegas los pools de 5 consultas de prueba elegidas al azar, se informa el acuerdo entre ambos (kappa ponderado lineal sobre la escala 0–3) antes de cualquier adjudicación, y la métrica primaria se recalcula con esos juicios como análisis de sensibilidad. A la fecha no hay un segundo evaluador disponible. Si no se obtiene antes de cerrar el estudio, la tesis declara un evaluador único y no presenta los juicios como una verdad independiente de quien los emitió.

### 7.6.4 Juicios de desarrollo y su revisión asistida

Los juicios de desarrollo tuvieron dos etapas que deben distinguirse.

**Primera etapa.** El 12 de noviembre, el evaluador juzgó los 345 pares del pool inicial (M0, M1, M2 y la muestra al azar). Una comprobación posterior mostró que esos juicios apenas se relacionaban con la composición que el mismo investigador había registrado en la anotación: entre los pares con la misma composición anotada, el 14 % recibió grado 2 o 3; entre los de composición distinta, el 11 %. De los 40 juicios de grado 2 o 3, solo 5 llevaban la justificación exigida. La coincidencia de composición no es el patrón oro, y exigir que los juicios la reprodujeran reintroduciría la circularidad; pero el hallazgo indicaba que la rúbrica se había aplicado, al menos en parte, con un criterio de parecido global y no estructural. El investigador decidió conservar los juicios y someter la cuestión al asesor (decisión R17).

**Segunda etapa.** El 19 de noviembre, los juicios de desarrollo, ya ampliados con los candidatos de M3 y M3-sin-orden, se revisaron con la segunda opinión ciega de un modelo de visión y lenguaje de uso general (Claude, de Anthropic), que no es CLIP ni ninguno de los sistemas evaluados. El modelo vio solo las dos imágenes de cada par y la rúbrica; no tuvo acceso a los grados del evaluador, a los rankings, a los sistemas ni a la anotación. El evaluador revisó cada par con esa opinión a la vista y firmó el grado y la justificación finales. Antes de la revisión, el acuerdo entre el evaluador y la segunda opinión era bajo: kappa ponderado lineal de 0,161, el único acuerdo independiente, porque se midió antes de que el evaluador viera la opinión. Después de la revisión, el evaluador había cambiado 246 de los 411 grados, el acuerdo con la segunda opinión subió a 0,925 y la justificación firmada coincidía con la del modelo en 406 de los 411 pares. Los juicios de desarrollo vigentes son, por tanto, juicios humanos asistidos por un modelo, y así se declaran (decisión R25). Firmar cada grado establece la responsabilidad humana del juicio, pero no lo convierte en una validación independiente.

**Riesgo de anclaje.** Esas cifras indican que el evaluador adoptó casi siempre la propuesta del modelo. La literatura sobre sesgo de automatización describe ese riesgo: quien revisa la salida de una ayuda automática tiende a usarla como sustituto de la búsqueda atenta de información, incluso con experiencia en el dominio y con instrucciones de verificar (Parasuraman y Manzey, 2010, pp. 391 y 397). Esa revisión no trata modelos de visión y lenguaje, y su extensión a este caso es de la tesis. La segunda opinión pudo corregir errores del evaluador o desplazar su criterio hacia el del modelo, y los datos no permiten distinguir entre ambas cosas: las confirmaciones que coinciden con la propuesta no separan la verificación de la aceptación. El riesgo se declara y su alcance queda limitado a lo que esos juicios decidieron.

**Archivo de auditoría.** El material de la revisión se conserva en un archivo de auditoría privado, fuera del repositorio: los grados y justificaciones del evaluador antes de la revisión, la opinión del modelo con su confianza y su justificación, la decisión de mantener o cambiar cada grado y el informe de la comparación. El archivo separa los 411 juicios con que se eligieron los pesos de M4 de los 8 que la fusión añadió después al pool, que el evaluador juzgó sin asistencia y que no se usaron para reajustar nada. El archivo identifica el modelo usado (Claude Opus 5.5, en cinco instancias con las mismas instrucciones), las instrucciones completas, las imágenes que vio y sus respuestas. En el repositorio se registran su suma SHA-256 y una descripción de su contenido (`docs/auditoria_juicios_desarrollo.md`; decisión R39).

**Alcance y justificación.** Los juicios de desarrollo intervienen en dos decisiones: la elección de los pesos de M4 (sección 7.9) y la estimación del efecto mínimo detectable (sección 7.8). No intervienen en ninguna hipótesis. El argumento de Soboroff (2025) contra los juicios de relevancia hechos por modelos de lenguaje se apoya en que el conjunto de juicios actúa como techo: lo no juzgado cuenta como no relevante, y si el juez está entre los sistemas evaluados, los que lo superen parecerán peores. Ese mecanismo no opera aquí del mismo modo, porque el modelo revisor no es ninguno de los sistemas comparados y no propuso candidatos. Queda, sin embargo, un riesgo más difuso: un modelo visión-lenguaje de propósito general puede compartir con M2 una noción de semejanza visual, y unos pesos elegidos con juicios influidos por él podrían favorecer al componente visual de la fusión o, al revés, penalizar al estructural. La dirección de ese sesgo no puede establecerse. Por eso la prueba se juzga sin ninguna asistencia (sección 7.6.5): las conclusiones confirmatorias no dependen de juicios de un modelo, y la influencia de la asistencia queda limitada a los pesos de M4 y a la planificación de la potencia, donde se declara.

### 7.6.5 Juicios de prueba

Los juicios de relevancia de prueba se emitirán sin asistencia de modelos: el evaluador juzga solo y a ciegas, y su grado es el único que se usa (decisión R27). M3 y M4 utilizarán, no obstante, la anotación congelada, cuya revisión incluyó asistencia (capítulo 4, sección 4.10). La decisión responde a la pregunta de investigación, que pide juicios humanos independientes de los sistemas, y al argumento de Soboroff (2025), que admite el uso de un modelo para detectar errores de los evaluadores pero no como fuente de los juicios con que se decide una comparación.

**Estabilidad del evaluador.** Los juicios de prueba se emiten una sola vez: no se rejuzga una submuestra, de modo que no se estima la estabilidad intraevaluador de los juicios de prueba (decisión R38). La estabilidad que la tesis informa es la de la anotación (capítulo 4), que no la sustituye. La limitación se declara en el capítulo 11.

**Consultas sin relevantes.** Si ningún candidato de una consulta alcanza el grado 1, su nDCG no está definido. La consulta se excluye de la media, se informa cuántas hubo y cuáles fueron, y no se reemplaza.

## 7.7 Métricas e inferencia

**Métrica primaria.** nDCG@10 por consulta de T3, con ganancia 2^rel − 1 y descuento log₂(r + 1); el ordenamiento ideal se calcula con todos los juicios de la consulta.

**Métricas secundarias.** Precisión en 10 y rango recíproco medio, con la relevancia binarizada en el grado 2, y la proporción juzgada del top 10. En T1 se informan las mismas métricas de forma descriptiva.

**Estimandos.** Para H1, la media sobre las consultas de prueba evaluables de la diferencia pareada Δ_q = nDCG@10(M4) − nDCG@10(M2), es decir, la utilidad del sistema combinado frente a M2; para la ablación M4 sin M3, la media de nDCG@10(M4) − nDCG@10(M4 sin M3); para H2, la media de Δ_q = nDCG@10(M3) − nDCG@10(M3-sin-orden), y para el subgrupo de H2, esa media en las consultas con palabra de bandas. Una consulta es evaluable si tiene nDCG definido en los dos sistemas; n es su número. La evaluación es transductiva sobre una galería fija, y el museo, la fotografía, la técnica y la tradición pueden confundir las comparaciones; la heterogeneidad por museo solo se describe. Una diferencia con |Δ_q| ≤ 10⁻¹² cuenta como cero, para que un redondeo no convierta en distinta de cero una diferencia nula por construcción.

**Contraste de H1.** Prueba de permutación pareada por cambio de signo, bilateral, con nivel 0,05. Con 30 consultas, enumerar los 2³⁰ cambios de signo es impracticable, y la p se estima con un número fijo de réplicas, B = 100 000, con semilla fija: p = (b + 1)/(B + 1), donde b es el número de réplicas al menos tan extremas como la observada. El cálculo termina solo al completar las B réplicas, sin ampliarlas ni reducirlas a la vista de la p, y se informa su error de Monte Carlo, √[p(1 − p)/B], de unas 0,0007 cerca de p = 0,05. Las 100 000 réplicas son una elección operacional del estudio, no un mínimo general. Como comprobación se informa la t de Student pareada; si las dos pruebas discrepan, se informa la discrepancia y decide la permutación. La elección se apoya en dos comparaciones empíricas de pruebas de significación en recuperación de información: Smucker et al. (2007, pp. 631–632) recomiendan la aleatorización siempre que sea aplicable, y Urbano et al. (2019, pp. 6–7) muestran que, con 25 temas, la permutación y la t mantienen el error de tipo I cerca del nominal mientras que el bootstrap usado como prueba resulta demasiado optimista. Ninguno de los dos estudios trata nDCG@10 ni menos de 25 temas, ni valida este diseño; 30 consultas quedan dentro de su rango, las 10 de desarrollo no.

**Contraste de H2.** Solo pueden ser distintas de cero las diferencias de las consultas con palabra de bandas, que en prueba son 9. Con tan pocas, la distribución de referencia puede calcularse exactamente: se enumeran los 2^m vectores de signos de las m diferencias distintas de cero (m ≤ 9) y la p bilateral es la proporción de vectores cuyo estadístico iguala o supera al observado. La p mínima alcanzable es 2/2^m: con m ≤ 5 vale al menos 0,0625 y H2 no puede alcanzar p < 0,05, cualquiera sea el resultado; con m = 0, p = 1. La prueba supone que, bajo la hipótesis nula, los signos son intercambiables en cada consulta y que las consultas son independientes; la exactitud del cálculo no corrige un sesgo de selección ni la incertidumbre de una muestra tan pequeña. Se informan n, b (consultas evaluables con palabra de bandas), m, la p exacta y la p mínima. Como las diferencias son cero fuera del subgrupo, el umbral práctico de 0,03 sobre las n consultas equivale a 0,03 · n/b en el subgrupo: 0,10 con 30 y 9.

**Intervalo.** El intervalo de confianza del 95 % de Δ se obtiene por bootstrap pareado de consultas, por percentiles, con 10 000 réplicas, semilla fija y el mismo remuestreo para los dos sistemas. Describe la magnitud y su incertidumbre; no decide las hipótesis. Si la p y el intervalo parecen discrepar, se informan ambos sin cambiar el método de decisión.

**Regla de decisión.** La regla separa tres afirmaciones, que se informan por separado: la evidencia frente a una diferencia nula (p < 0,05), la estimación de Δ con su intervalo y la relevancia práctica de la diferencia observada (Δ ≥ 0,03). Una hipótesis comparativa se sostiene solo con la primera y la tercera. Las demás combinaciones tienen su propia lectura: «mejora distinta de cero, por debajo del umbral práctico» (p < 0,05 y 0 < Δ < 0,03), «inferior al sistema de referencia» (p < 0,05 y Δ < 0), «dirección favorable sin evidencia suficiente» (p ≥ 0,05 y Δ > 0) y «no se detectó una mejora» (p ≥ 0,05 y Δ ≤ 0). El umbral de 0,03 es una decisión del estudio, que representa una mejora pequeña pero apreciable en la posición de los relevantes dentro de los diez primeros resultados, y se aplica a la diferencia observada: que H1 se sostenga no significa que el efecto poblacional alcance 0,03, umbral que no se contrasta. Una p no significativa no demuestra ausencia de mejora, y con potencia limitada un efecto seleccionado por significación puede estar sobrestimado, sin que ello implique que lo esté (Card et al., 2020).

**Comparaciones múltiples.** H1 y H2 son confirmatorias y se contrastan en una secuencia fija (decisión R33). H1 se contrasta primero con α = 0,05. H2 solo recibe una conclusión confirmatoria si H1 cumple su regla completa; si no, se informa como exploratoria, con su estimación, su intervalo y su p. El control formal de la tasa de error por familia depende de rechazar la hipótesis nula de H1, porque H2 solo se contrasta en ese caso; la exigencia de Δ ≥ 0,03 es adicional y más conservadora. Se eligió la secuencia fija y no el procedimiento de Holm porque H1 es la hipótesis primaria de la tesis. Con la potencia disponible, la secuencia hace improbable una conclusión confirmatoria sobre H2. El subgrupo de H2, las comparaciones frente a M0, M1 y M3, las ablaciones, el control negativo y los análisis por museo son exploratorios: se informan con su intervalo, sin interpretar su valor p como confirmación, y cualquiera sea el signo de su resultado.

## 7.8 Potencia y efecto mínimo detectable

La potencia se planifica antes del experimento y no se calcula a posteriori con el efecto observado, una práctica que Card et al. (2020, p. 2, nota 2) desaconsejan. Con la desviación estándar de las diferencias pareadas observada en las diez consultas de desarrollo, el efecto mínimo detectable con 30 consultas, potencia del 80 % y α = 0,05 bilateral es

$$\text{EMD} = \frac{(z_{0{,}975} + z_{0{,}8})\, \widehat{\sigma}_\Delta}{\sqrt{30}} \approx 0{,}51\, \widehat{\sigma}_\Delta, \tag{7.1}$$

y el número de consultas necesario para detectar el umbral práctico es $n \approx [(z_{0{,}975} + z_{0{,}8})\, \widehat{\sigma}_\Delta / 0{,}03]^2$. El rango del efecto se obtiene del intervalo del 95 % de la desviación estimada con diez observaciones, bajo normalidad de las diferencias. El cálculo se hizo el 21 de noviembre con los 419 juicios de desarrollo y los pesos de M4 ya fijados (decisión R29). No se informa el nDCG medio de ningún sistema ni el signo de las diferencias.

**Cuadro 7.4.** Planificación de la potencia antes del test.

| Comparación | Base del cálculo | Resultado |
|---|---|---|
| H1: M4 frente a M2 | Desviación de las diferencias en 10 consultas de desarrollo: 0,169 | EMD con 30 consultas: 0,087 (rango de 0,060 a 0,159); unas 250 consultas para 0,03 |
| H2: M3 frente a M3-sin-orden | Prueba exacta con m ≤ b = 9 diferencias distintas de cero | p mínima alcanzable: 0,0039 si m = 9; hacen falta al menos 6 diferencias distintas de cero para que p < 0,05 sea posible |
| H2, consultas con palabra de bandas | 2 consultas de desarrollo y 9 de prueba | Umbral equivalente: 0,10; descriptivo |

La lectura de cada fila es distinta.

- **H1.** El valor de 0,087 es una estimación aproximada de planificación, basada en diez consultas, y no una frontera: no impide que un efecto menor resulte significativo ni garantiza que uno mayor se detecte. Indica que el estudio no tiene potencia para el umbral de 0,03. Un resultado no significativo se informará como «no se detectó una mejora», no como ausencia de efecto.
- **H2.** El EMD por aproximación normal (0,026, decisión R29) se retiró: con a lo sumo nueve diferencias distintas de cero, la distribución de la prueba es discreta y la aproximación no vale (decisión R35). En su lugar se informa la p mínima alcanzable. Además, H2 solo es confirmatoria si H1 se sostiene (sección 7.7).
- **Subgrupo de H2.** Con dos consultas de desarrollo con bandas no hay base para estimar su variabilidad. Se informará de forma descriptiva, con su intervalo y el umbral equivalente.

El número de consultas de prueba no se modifica después de abrir el test. Se mantuvo en 30 porque es lo que el calendario de juicios permite; aumentarlo hasta la potencia deseada para H1 exigiría unas 250 consultas y, con ellas, más de 13 000 pares por juzgar.

Las estimaciones tienen dos debilidades que se declaran. Proceden de diez consultas, y Card et al. (2020, p. 16) advierten que estimar la varianza con datos de validación puede inducir exceso de confianza. Y dependen de juicios de desarrollo asistidos (sección 7.6.4).

## 7.9 Selección de los pesos de M4

Los pesos de M4 se eligen en la rejilla {0; 0,25; 0,5; 0,75; 1} para cada componente, normalizados a suma 1, lo que da 91 combinaciones distintas. La regla, fijada en el protocolo, toma la combinación con mayor nDCG@10 medio en desarrollo; en caso de empate, la más cercana a pesos iguales, y después la primera en orden lexicográfico descendente.

La selección se hizo **una sola vez**, el 21 de noviembre, con los 411 juicios de desarrollo vigentes en ese momento, y eligió M0 = 1/7, M2 = 4/7 y M3 = 2/7 (decisión R28). La razón de no repetirla es que los candidatos de M4 dependen de los pesos: los diez primeros de la fusión con los pesos elegidos incluían pares todavía sin juzgar, y volver a elegir los pesos tras juzgarlos convertiría la selección en un ciclo. Los ocho pares que añadió la fusión se juzgaron después y se usan para estimar la potencia, no para cambiar los pesos. Un paso del flujo informa, sin modificarlos, si la regla sigue eligiendo los mismos pesos con los juicios vigentes; con los 419 juicios, los elige.

Bruch et al. (2023) muestran que la combinación convexa necesita pocas consultas etiquetadas para ajustar su peso, pero su análisis cubre dos sistemas y no ofrece un número absoluto que respalde diez consultas (capítulo 3, sección 3.7). La variante M4-RRF, que no tiene pesos, permite estimar cuánto del resultado de M4 depende de ese ajuste.

## 7.10 Ablaciones y control negativo

Las ablaciones se calculan sobre las mismas consultas y candidatos que la comparación principal, y son exploratorias:

- M4 sin M3, es decir, solo texto e imagen;
- M4 sin M0;
- M4 con M3-sin-orden en lugar de M3;
- M3 solo con los bloques de bandas (palabra y adyacencias) frente a M3 con todos los demás bloques del descriptor (composición, borde, centro, simetría, repetición, motivos y familia iconográfica), de modo que los dos lados cubren el descriptor sin solaparse;
- M4-RRF, la fusión por posiciones sin pesos.

Retirar un componente de M4 equivale a declararlo sin evidencia para todos los candidatos, con renormalización de los pesos restantes (capítulo 5, proposición 5.9). Las ablaciones usan, por tanto, la misma fórmula que el sistema completo.

**Control negativo.** M4 se recalcula con los descriptores de M3 permutados al azar entre piezas del mismo museo, con una sola permutación de semilla fija y sin permutaciones adicionales. Si el aporte de la estructura es real, debe desaparecer en esta condición. Una sola permutación no ofrece una distribución nula, de modo que el control es descriptivo y no decide ninguna hipótesis. La permutación dentro de cada museo conserva la distribución de descriptores por museo, de modo que el control también comprueba que una eventual ganancia no procede de que la anotación capture, indirectamente, el museo de procedencia.

**Robustez.** Los resultados se informan según el museo de la consulta y según el estado de la pieza consultada. El estado es la completitud que el revisor escribió al decidir la curación de cada pieza: completo, incompleto o sin dato. Se mantiene el tercer grupo porque 61 de las 150 piezas de la galería no mencionan la completitud, y asignarlas a uno de los otros dos introduciría un error de clasificación. Con estos tamaños de muestra, el análisis es descriptivo.

**Tarea T1.** Las seis consultas escritas se ejecutan con M0, que compara la descripción con el texto de las fichas; con M2, que compara el vector de texto de la descripción, codificada sin plantilla porque T1 no tiene consultas de desarrollo, con los vectores de imagen; con M3, solo cuando la consulta trae especificación estructural y solo sobre los bloques especificados; y con M4, que fusiona los componentes disponibles con los pesos de T3. Sus resultados son descriptivos.

## 7.11 Fidelidad computacional (H3) y revisión de las explicaciones

Para cada resultado del top 10 de M4 en prueba se registran las contribuciones α′_c ŝ_c de cada componente, la máscara de observabilidad y la procedencia de cada valor. H3 se delimita como la fidelidad computacional de la descomposición de M4 (decisión R36) y se sostiene si se cumplen dos comprobaciones:

1. **Reconstrucción.** La suma de las contribuciones coincide con la puntuación, con un error ≤ 10⁻⁹, en todos los resultados.
2. **Intervención.** Retirar un componente modifica la puntuación exactamente como predice la fórmula, incluida la regla de reparto de pesos, con el mismo error máximo. Se verifica con pruebas de propiedades y sobre todos los resultados de prueba.

Las dos comprobaciones son identidades de la fórmula (capítulo 5, proposición 5.9); lo que el experimento contrasta es que la implementación las satisface en todos los resultados, dentro de la tolerancia fijada. Demuestran fidelidad a la implementación y a su fórmula aditiva, no la inteligibilidad de la explicación, su adecuación semántica ni su utilidad para especialistas, una distinción que Jacovi y Goldberg (2020) trazan entre fidelidad y plausibilidad. M4-RRF no interviene en H3, porque al operar sobre posiciones no conserva la descomposición de la puntuación.

**Revisión humana de las explicaciones.** Se informa aparte, como análisis descriptivo, y no interviene en el veredicto de H3:

- Un *acierto* es un resultado del top 10 de M4 juzgado relevante (grado 2 o 3); un *error*, uno juzgado con grado 0 o 1. Los pares `no_evaluable` no entran en ninguna clase.
- Se sortean 5 aciertos y 5 errores con una semilla fija, sin selección a la vista de los casos. Si una clase tiene menos de 5, se usan todos y se informa cuántos había, sin completar la cuota.
- Cada ficha muestra las dos imágenes, las contribuciones de cada componente y su procedencia, sin la clase, el grado ni la posición, en orden aleatorio. El evaluador la valora como correcta, incorrecta, especulativa o no evaluable, con un código de desacuerdo que indica el componente cuya contribución no corresponde y una justificación; un validador comprueba los campos.
- El denominador son las fichas sorteadas; las no evaluables se informan y no se reemplazan.
- La revisión no es independiente: el revisor es el evaluador, que anotó la estructura que usa M3. Se informa como descripción de casos, sin tasas ni contraste.

## 7.12 Orden de ejecución y criterios de suspensión

El experimento sigue un orden obligatorio:

1. Congelación de los grupos, las particiones y la anotación (anotación v2.1, 17 de noviembre).
2. Desarrollo: rankings, juicios de desarrollo, selección de los pesos de M4 y estimación de la potencia (completado el 21 de noviembre).
3. Autorización del protocolo por el asesor y congelación de los sistemas.
4. Una única ejecución del test, que avanza por estados sellados (decisión R37).

**Estados de la corrida.** Cada corrida tiene un identificador y pasa por cinco estados que se registran en un manifiesto de ejecución, sin que ningún paso pueda ejecutarse antes de que el anterior esté registrado. En `autorizada` se registran la fecha y el commit de la autorización y la suma del protocolo. En `insumos_sellados` se escribe el manifiesto, antes de calcular ningún ranking, con el commit, las sumas SHA-256 de todos los insumos obligatorios, la huella de la rúbrica, las instrucciones y los parámetros de pooling, el punto de control de M2, los parámetros, el equipo y las semillas; un insumo ausente o un archivo versionado con cambios sin registrar detienen la corrida. En `rankings_sellados` se calculan los rankings de prueba y el pool y se añaden sus sumas. En `juicios_cerrados` se cierran y sellan los juicios, incluido el doble juicio parcial si hay segundo evaluador. En `evaluada` se recalculan todas las sumas y solo si coinciden se calculan las métricas.

**Fallos y custodia.** Cada paso escribe en archivos temporales y los publica al terminar, junto con el manifiesto actualizado, de modo que un fallo no deja salidas parciales con el nombre definitivo. Un paso que falla antes de publicar puede repetirse desde el último estado sellado, con los mismos insumos y anotando la incidencia; una vez sellados los rankings, una segunda ejecución se rechaza. Si una suma no coincide, falta un archivo sellado o aparece un artefacto de otra corrida, la corrida queda suspendida y no se calcula ninguna métrica. La custodia no depende de una firma criptográfica personal: se acredita con una etiqueta Git anotada en cada estado, un registro de custodia versionado con la fecha, el responsable, la corrida, el commit y las sumas, y el envío de las sumas al asesor por correo al sellarlas. El investigador declara por escrito que no ejecutó ningún sistema sobre las consultas de prueba antes de la autorización.

**El test no se abre** si se da alguna de estas condiciones: hay grupos de piezas relacionadas repartidos entre particiones; algún juicio de prueba se derivó del descriptor, de CLIP o de cualquier otro modelo; la guía de anotación o el protocolo cambiaron sin registro; algún peso se ajustó con datos de prueba; alguna imagen no está verificada; o falta el manifiesto de ejecución o alguna de sus sumas no coincide. Antes de abrirlo se ejecuta una comprobación automática que reúne las condiciones verificables en el repositorio: la aprobación del protocolo y que no cambió después de aprobarse, la ausencia de fugas entre particiones, la anotación congelada y sus condiciones de buena formación, los pesos de M4, las sumas de las imágenes y la existencia de las consultas T1. La ejecución de los rankings de prueba se niega si encuentra un problema. La suspensión protege el test, pero no impide preparar código ni trabajar con los datos de desarrollo.

## 7.13 Amenazas a la validez

Las amenazas se ordenan por el tipo de validez que comprometen. Para cada una se indica qué se hizo para mitigarla y qué limitación subsiste.

**Cuadro 7.5.** Amenazas a la validez.

| Amenaza | Tipo de validez | Mitigación | Limitación que subsiste |
|---|---|---|---|
| A1. Una misma persona anota la estructura que usa M3 y juzga la relevancia | Interna y de constructo | Juicio ciego y aleatorizado; consultas fijadas de antemano; doble juicio parcial preparado | Sesgo residual a favor de M3; sin segundo evaluador a la fecha. Es la limitación principal |
| A2. Los juicios de desarrollo se aplicaron con un criterio de parecido global y después se revisaron con asistencia | De constructo | Uso restringido a pesos y potencia; prueba sin asistencia; archivo de auditoría con huella (sección 7.6.4) | Los pesos de M4 y la potencia heredan ambas reservas y el riesgo de anclaje en la opinión del modelo |
| A3. Un solo anotador | De constructo | Re-anotación ciega de 30 piezas; estabilidad informada por atributo | Mide estabilidad, no acuerdo entre personas |
| A4. La frontera entre lo observable y lo no observable es inestable | De constructo | Cobertura de bloques informada con cada comparación | Los bloques que compara M3 dependen de un juicio variable |
| A5. La anotación combina lecturas distintas y una revisión asistida | Interna | Criterios escritos y revisión de los lotes 2 a 5 antes de congelar; análisis de sensibilidad | La revisión cambia de forma apreciable los rankings de M3 (capítulo 4, sección 4.10.1) |
| A6. El eje y el sentido de lectura dependen de la fotografía | De constructo | Equivalencia por reversión; el eje no entra en el descriptor | Se pierde la orientación de las prendas que la tienen |
| A7. La estructura no es independiente de la técnica ni de la tradición | De constructo | Control sin orden; control negativo dentro de cada museo | Una ganancia de M3 puede reflejar pertenencia a una tradición |
| A8. Solo se juzgan los primeros candidatos de cada sistema | Interna | Pool con todos los sistemas más una muestra al azar; proporción juzgada informada | Sesgo contra sistemas ajenos al pool |
| A9. Piezas relacionadas en particiones distintas | Interna | Grupos decididos antes de partir; comprobación automática | Relaciones que ninguna señal propuso |
| A10. Las fotografías pudieron formar parte del preentrenamiento de M2 | Interna | Se declara | No puede medirse; favorecería a M2 |
| A11. Pocas consultas de prueba | De conclusión estadística | Permutación pareada; intervalo; planificación de la potencia antes del test; p exacta en H2 | Sin potencia para el umbral de 0,03 en H1; en H2, con menos de seis diferencias distintas de cero la p no baja de 0,05 |
| A16. Estabilidad del evaluador en prueba | De conclusión estadística | Juicio ciego con escala fijada de antemano | No se estima la estabilidad intraevaluador de los juicios de prueba: no hay rejuicio |
| A12. Pesos de M4 elegidos con diez consultas | De conclusión estadística | Rejilla pequeña, selección única y variante sin pesos | Ajuste posiblemente inestable |
| A13. M3 dispone de información humana que M2 no tiene | De constructo y externa | Se declara; M3 excluye el color | No se mide la extracción automática; el costo de anotar no se midió |
| A14. El corpus no es una muestra de los textiles andinos | Externa | Población definida de forma restrictiva; resultados por museo | No hay generalización fuera de la colección elegible |
| A15. Diferencias fotográficas entre museos | Interna y externa | Copia de evaluación común; M1 sobre el textil segmentado; análisis por museo | Tamaños pequeños por museo |

Tres de estas amenazas requieren un comentario adicional.

**A7. Estructura, técnica y tradición.** La organización visible no es independiente de cómo se tejió la pieza: en la faz de urdimbre la banda la fija el urdido, el tapiz deja libre la composición y algunos bordados imitan las bandas tejidas (Desrosiers, 2013, pp. 480–499). Una similitud estructural alta puede reflejar, en parte, la pertenencia a una misma tradición técnica, que un codificador visual también capta por la textura y el color. El control sin orden aísla el efecto de la secuencia respecto de la composición por tipos; el control negativo comprueba que el efecto no procede del museo. Ninguno separa por completo estructura y tradición, y el análisis por cultura atribuida será descriptivo.

**A10. Preentrenamiento.** Las fotografías de MET, CMA y AIC son públicas y pudieron formar parte de los datos con que se entrenó el codificador de M2, como reconocen Baldrati et al. (2022) para colecciones de arte. Esa posible fuga favorecería a M2 y hace más conservadora la comparación de H1.

**A13. Costo de la anotación.** Una comparación entre un sistema asistido por anotación y uno que solo usa píxeles exige conocer el costo de anotar. El tiempo por pieza no se registró, de modo que el manuscrito solo puede ofrecer una estimación, declarada como tal.

**Lo que estas amenazas implican para las conclusiones.**

- Un resultado favorable a H1 respaldará la utilidad del sistema combinado, que incluye la estructura **anotada**, en **esta colección**, con el sesgo residual de A1 declarado. No atribuirá la mejora a la estructura: esa lectura corresponde a las ablaciones, que son exploratorias.
- Un resultado favorable a H2, si H1 se sostiene, indicará que la secuencia aporta más que la composición por tipos, sin separar por completo estructura y tradición (A7).
- Un resultado nulo será, con alta probabilidad, inconcluso y no negativo, por la potencia disponible (A11).
- H3 es independiente de todas las amenazas anteriores, porque es una propiedad del algoritmo; a cambio, no dice nada sobre el significado de las contribuciones ni equivale a una validación por especialistas.

## 7.14 Cierre del capítulo

El diseño convierte la pregunta del capítulo 2 en dos comparaciones pareadas y una verificación algorítmica, con un protocolo fijado antes de ver resultados de prueba. Las decisiones que dependían de datos (los pesos de la fusión y la potencia) se tomaron en desarrollo y una sola vez; las que dependían del juicio humano se rodearon de salvaguardas de procedimiento. La asistencia usada en desarrollo se declara: los juicios de relevancia de prueba se emitirán sin asistencia de modelos, y M3 y M4 utilizarán, no obstante, la anotación congelada cuya revisión incluyó asistencia. El diseño tiene dos debilidades que no se pueden corregir con el tiempo disponible: un evaluador que también anotó, y una potencia que solo permite detectar efectos grandes. Ambas se declaran antes de conocer el resultado, para que este se lea en su justa medida. El capítulo 8 informará los resultados con la misma estructura.

## Referencias

Baldrati, A., Bertini, M., Uricchio, T., et al. (2022). Exploiting CLIP-based multi-modal approach for artwork classification and retrieval. Springer. https://doi.org/10.1007/978-3-031-20302-2_11 [verificar: autores restantes, título del volumen y páginas; versión leída: arXiv:2309.12110]

Bruch, S., Gai, S., & Ingber, A. (2023). *An analysis of fusion functions for hybrid retrieval* (arXiv:2210.11934v2). arXiv. https://arxiv.org/abs/2210.11934 [verificar: sede]

Buckley, C., Dimmick, D., Soboroff, I., & Voorhees, E. (2007). Bias and the limits of pooling for large collections. *Information Retrieval, 10*, 491–508. https://doi.org/10.1007/s10791-007-9032-x

Card, D., Henderson, P., Khandelwal, U., Jia, R., Mahowald, K., & Jurafsky, D. (2020). *With little power comes great responsibility* (arXiv:2010.06595). arXiv. https://arxiv.org/abs/2010.06595 [verificar: sede]

Cormack, G. V., Clarke, C. L. A., & Büttcher, S. (2009). Reciprocal rank fusion outperforms Condorcet and individual rank learning methods. En *Proceedings of the 32nd International ACM SIGIR Conference on Research and Development in Information Retrieval*. ACM. [verificar: páginas y DOI]

Desrosiers, S. (2013). El textil como matriz para el desarrollo de las artes plásticas en los Andes. *Revista Española de Antropología Americana, 43*(2), 477–514. https://doi.org/10.5209/rev_REAA.2013.v43.n2.44020

Jacovi, A., & Goldberg, Y. (2020). *Towards faithfully interpretable NLP systems: How should we define and evaluate faithfulness?* (arXiv:2004.03685). arXiv. https://arxiv.org/abs/2004.03685 [verificar: sede; el dictamen del asesor la cita en ACL 2020, DOI 10.18653/v1/2020.acl-main.386]

Parasuraman, R., & Manzey, D. H. (2010). Complacency and bias in human use of automation: An attentional integration. *Human Factors, 52*(3), 381–410. https://doi.org/10.1177/0018720810376055

Sakai, T., Tao, S., & Zeng, Z. (2022). *Relevance assessments for web search evaluation: Should we randomise or prioritise the pooled documents? (Corrected version)* (arXiv:2211.00981). arXiv. https://arxiv.org/abs/2211.00981 [verificar: DOI de la versión de revista]

Smucker, M. D., Allan, J., & Carterette, B. (2007). A comparison of statistical significance tests for information retrieval evaluation. En *Proceedings of the 16th ACM Conference on Information and Knowledge Management (CIKM '07)* (pp. 623–632). ACM. https://doi.org/10.1145/1321440.1321528

Soboroff, I. (2025). Don't use LLMs to make relevance judgments. *Information Retrieval Research, 1*(1), 29–46. https://doi.org/10.54195/irrj.19625

Urbano, J., Lima, H., & Hanjalic, A. (2019). Statistical significance testing in information retrieval: An empirical analysis of type I, type II and type III errors. En *Proceedings of the 42nd International ACM SIGIR Conference on Research and Development in Information Retrieval (SIGIR '19)*. ACM. https://doi.org/10.1145/3331184.3331259
