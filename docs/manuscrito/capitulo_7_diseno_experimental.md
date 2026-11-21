# 7. Diseño experimental

> **Borrador 0.1, 21 de noviembre de 2026.** Capítulo de la segunda parte de la tesis. Sustituye al capítulo 7 del primer avance («Plan experimental preliminar»), que no se corrige. Describe el protocolo experimental en su versión 0.6.5, pendiente de aprobación, y las decisiones registradas hasta la R32. A la fecha de este borrador no se ha ejecutado ningún sistema sobre las consultas de prueba. El capítulo no informa el rendimiento de ningún sistema en desarrollo: el evaluador debe juzgar la prueba sin conocerlo.

## 7.1 Principios del diseño

El plan experimental del primer avance proponía comparar una línea base visión-lenguaje, un descriptor combinatorio y un modelo híbrido en cuatro tareas, con relevancia definida a partir de coincidencias de tipo de objeto, técnica, cultura o composición. Ese plan dejaba abiertas tres cuestiones que deciden si un resultado puede atribuirse al método: qué cuenta como resultado pertinente y quién lo decide, cómo se evita que el ajuste de los sistemas use los mismos datos con que se evalúan, y qué resultado sostendría o refutaría cada hipótesis. Este capítulo las resuelve con cinco principios.

1. **Protocolo previo.** Qué se compara, con qué datos, cómo se mide y qué se considera evidencia se fija por escrito antes de observar cualquier resultado de prueba. Todo cambio posterior se registra con su fecha y su motivo.
2. **Separación entre desarrollo y prueba.** Todo lo que tiene un parámetro se fija con datos de desarrollo. La prueba se ejecuta una sola vez, con los sistemas congelados.
3. **Relevancia juzgada por una persona y a ciegas.** La pertinencia no se deriva de metadatos, de la anotación ni de un modelo: la decide un evaluador que ve solo las imágenes, sin saber qué sistema propuso cada candidato.
4. **Una comparación que aísla el componente propuesto.** El efecto de la estructura se mide frente al codificador visual que la fusión contiene (H1), y el efecto del orden frente a un control que conserva todo lo demás (H2).
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

La unión de los primeros resultados de todos los sistemas comparados protege a M3 y M4 del sesgo conservador del pooling, que infravalora a los sistemas cuyos resultados no entraron al pool (Buckley et al., 2007, pp. 16–17). La muestra al azar ofrece una referencia independiente de los sistemas y coincide con una de las vías que esos autores proponen, aunque su interacción con el sesgo no está estudiada (p. 15).

En desarrollo, el pool reúne 419 pares. En prueba se estima en unos 1600 pares, alrededor de 13 horas de juicio con 30 segundos por par.

### 7.6.3 Salvaguardas frente a la circularidad

El investigador definió el esquema de anotación, anotó las 150 piezas y es el evaluador. Su noción de similitud estructural se formó con las mismas categorías que usa M3, de modo que sus juicios pueden favorecer al descriptor sin que medie intención. Soboroff (2025) formula el principio general: un juez que comparte información con un sistema evaluado deja de ser un árbitro independiente. Las salvaguardas son de procedimiento:

1. Las consultas se fijaron antes de ejecutar cualquier sistema sobre ellas: las de T3 por sorteo y las de T1 por redacción.
2. Los juicios se hacen solo sobre las imágenes, sin consultar la anotación ni ver los rankings, las puntuaciones o el sistema que propuso cada candidato. Los candidatos de cada consulta se presentan en orden aleatorio, que evita favorecer a los documentos que muchos sistemas devuelven arriba (Sakai et al., 2022, pp. 16–17).
3. La escala y sus criterios se fijaron antes de juzgar. Ningún juicio se deriva de la anotación, del descriptor ni de CLIP.
4. El evaluador no abre ningún informe que contenga el rendimiento de los sistemas en desarrollo.

Estas medidas impiden que el evaluador sepa qué sistema propuso cada candidato. No impiden que su criterio coincida con el del descriptor. La mitigación externa prevista es un doble juicio parcial: otra persona con criterio estructural juzga a ciegas los pools de 5 consultas de prueba elegidas al azar, se informa el acuerdo entre ambos (kappa ponderado lineal sobre la escala 0–3) antes de cualquier adjudicación, y la métrica primaria se recalcula con esos juicios como análisis de sensibilidad. A la fecha no hay un segundo evaluador disponible. Si no se obtiene antes de cerrar el estudio, la tesis declara un evaluador único y no presenta los juicios como una verdad independiente de quien los emitió.

### 7.6.4 Juicios de desarrollo y su revisión asistida

Los juicios de desarrollo tuvieron dos etapas que deben distinguirse.

**Primera etapa.** El 12 de noviembre, el evaluador juzgó los 345 pares del pool inicial (M0, M1, M2 y la muestra al azar). Una comprobación posterior mostró que esos juicios apenas se relacionaban con la composición que el mismo investigador había registrado en la anotación: entre los pares con la misma composición anotada, el 14 % recibió grado 2 o 3; entre los de composición distinta, el 11 %. De los 40 juicios de grado 2 o 3, solo 5 llevaban la justificación exigida. La coincidencia de composición no es el patrón oro, y exigir que los juicios la reprodujeran reintroduciría la circularidad; pero el hallazgo indicaba que la rúbrica se había aplicado, al menos en parte, con un criterio de parecido global y no estructural. El investigador decidió conservar los juicios y someter la cuestión al asesor (decisión R17).

**Segunda etapa.** El 19 de noviembre, los juicios de desarrollo, ya ampliados con los candidatos de M3 y M3-sin-orden, se revisaron con la segunda opinión ciega de un modelo de visión y lenguaje de uso general (Claude, de Anthropic), que no es CLIP ni ninguno de los sistemas evaluados. El modelo vio solo las dos imágenes de cada par y la rúbrica; no tuvo acceso a los grados del evaluador, a los rankings, a los sistemas ni a la anotación. El evaluador revisó cada par con esa opinión a la vista y firmó el grado y la justificación finales. Antes de la revisión, el acuerdo entre el evaluador y la segunda opinión era bajo (kappa ponderado lineal de 0,16), y después los grados firmados coinciden casi siempre con ella. Los juicios de desarrollo vigentes son, por tanto, juicios humanos asistidos por un modelo, y así se declaran (decisión R25). Los grados de la primera etapa se conservan fuera del repositorio. Los ocho pares que la fusión añadió después al pool los juzgó el evaluador sin asistencia.

**Alcance y justificación.** Los juicios de desarrollo intervienen en dos decisiones: la elección de los pesos de M4 (sección 7.9) y la estimación del efecto mínimo detectable (sección 7.8). No intervienen en ninguna hipótesis. El argumento de Soboroff (2025) contra los juicios de relevancia hechos por modelos de lenguaje se apoya en que el conjunto de juicios actúa como techo: lo no juzgado cuenta como no relevante, y si el juez está entre los sistemas evaluados, los que lo superen parecerán peores. Ese mecanismo no opera aquí del mismo modo, porque el modelo revisor no es ninguno de los sistemas comparados y no propuso candidatos. Queda, sin embargo, un riesgo más difuso: un modelo visión-lenguaje de propósito general puede compartir con M2 una noción de semejanza visual, y unos pesos elegidos con juicios influidos por él podrían favorecer al componente visual de la fusión o, al revés, penalizar al estructural. La dirección de ese sesgo no puede establecerse. Por eso la prueba se juzga sin ninguna asistencia (sección 7.6.5): las conclusiones confirmatorias no dependen de juicios de un modelo, y la influencia de la asistencia queda limitada a los pesos de M4 y a la planificación de la potencia, donde se declara.

### 7.6.5 Juicios de prueba

Los juicios de prueba se hacen sin asistencia: el evaluador juzga solo y a ciegas, y su grado es el único que se usa (decisión R27). La decisión responde a la pregunta de investigación, que pide juicios humanos independientes de los sistemas, y al argumento de Soboroff (2025), que admite el uso de un modelo para detectar errores de los evaluadores pero no como fuente de los juicios con que se decide una comparación.

**Consultas sin relevantes.** Si ningún candidato de una consulta alcanza el grado 1, su nDCG no está definido. La consulta se excluye de la media, se informa cuántas hubo y cuáles fueron, y no se reemplaza.

## 7.7 Métricas e inferencia

**Métrica primaria.** nDCG@10 por consulta de T3, con ganancia 2^rel − 1 y descuento log₂(r + 1); el ordenamiento ideal se calcula con todos los juicios de la consulta.

**Métricas secundarias.** Precisión en 10 y rango recíproco medio, con la relevancia binarizada en el grado 2, y la proporción juzgada del top 10. En T1 se informan las mismas métricas de forma descriptiva.

**Contraste.** Para H1 se calcula la diferencia pareada por consulta Δ = nDCG@10(M4) − nDCG@10(M2), y para H2, Δ = nDCG@10(M3) − nDCG@10(M3-sin-orden). Cada hipótesis se decide con una prueba de permutación pareada por cambio de signo, bilateral, con 10 000 réplicas, semilla fija y nivel 0,05. Como comprobación se informa la t de Student pareada; si las dos pruebas discrepan, se informa la discrepancia y decide la permutación. La elección se apoya en dos comparaciones empíricas de pruebas de significación en recuperación de información: Smucker et al. (2007, pp. 631–632) recomiendan la aleatorización siempre que sea aplicable, y Urbano et al. (2019, pp. 6–7) muestran que, con 25 temas, la permutación y la t mantienen el error de tipo I cerca del nominal mientras que el bootstrap usado como prueba resulta demasiado optimista. Ninguno de los dos estudios trata nDCG@10 ni menos de 25 temas; 30 consultas quedan dentro de su rango, las 10 de desarrollo no.

**Intervalo.** El intervalo de confianza del 95 % de Δ se obtiene por bootstrap pareado de consultas, por percentiles, con 10 000 réplicas, semilla fija y el mismo remuestreo para los dos sistemas. Describe la magnitud y su incertidumbre; no decide las hipótesis.

**Regla de decisión.** Una hipótesis comparativa se sostiene si Δ ≥ 0,03 y p < 0,05. Si la diferencia es positiva pero p ≥ 0,05, se informa como «dirección favorable sin evidencia suficiente». En cualquier otro caso, no se sostiene. El umbral de 0,03 es una decisión del estudio: representa una mejora pequeña pero apreciable en la posición de los relevantes dentro de los diez primeros resultados.

**Comparaciones múltiples.** H1 es la única comparación confirmatoria primaria y H2 la única secundaria. Al ser una por nivel, no se corrige por comparaciones múltiples. El análisis secundario de H2 en las consultas con palabra de bandas, las comparaciones frente a M0, M1 y M3, las ablaciones y los análisis por museo son exploratorios: se informan con su intervalo, sin interpretar su valor p como confirmación.

## 7.8 Potencia y efecto mínimo detectable

La potencia se planifica antes del experimento y no se calcula a posteriori con el efecto observado, una práctica que Card et al. (2020, p. 2, nota 2) desaconsejan. Con la desviación estándar de las diferencias pareadas observada en las diez consultas de desarrollo, el efecto mínimo detectable con 30 consultas, potencia del 80 % y α = 0,05 bilateral es

$$\text{EMD} = \frac{(z_{0{,}975} + z_{0{,}8})\, \widehat{\sigma}_\Delta}{\sqrt{30}} \approx 0{,}51\, \widehat{\sigma}_\Delta, \tag{7.1}$$

y el número de consultas necesario para detectar el umbral práctico es $n \approx [(z_{0{,}975} + z_{0{,}8})\, \widehat{\sigma}_\Delta / 0{,}03]^2$. El rango del efecto se obtiene del intervalo del 95 % de la desviación estimada con diez observaciones, bajo normalidad de las diferencias. El cálculo se hizo el 21 de noviembre con los 419 juicios de desarrollo y los pesos de M4 ya fijados (decisión R29). No se informa el nDCG medio de ningún sistema ni el signo de las diferencias.

**Cuadro 7.4.** Efecto mínimo detectable antes del test.

| Comparación | Desviación de las diferencias en desarrollo | EMD con 30 consultas | Rango del EMD | Consultas necesarias para 0,03 |
|---|---:|---:|---:|---:|
| H1: M4 frente a M2 | 0,169 | 0,087 | 0,060 a 0,159 | unas 250 |
| H2: M3 frente a M3-sin-orden | 0,051 | 0,026 | 0,018 a 0,048 | — |
| H2, consultas con palabra de bandas | No estimable (2 consultas de desarrollo) | — | — | — |

La lectura de cada fila es distinta.

- **H1.** El estudio solo detectará con fiabilidad diferencias del orden de 0,09, unas tres veces el umbral práctico. No tiene potencia para 0,03. Un resultado no significativo se informará como «no se detectó una mejora de la magnitud detectable», no como ausencia de efecto.
- **H2.** La desviación es pequeña porque 8 de las 10 diferencias de desarrollo son exactamente cero: cuando la consulta no tiene palabra de bandas, M3 y su control dan la misma puntuación a todos los candidatos (capítulo 5, sección 5.13). El efecto medio se diluye en la misma proporción. Si el orden solo actúa en las 9 consultas de prueba con bandas, en ellas tendría que ser unas 30/9 veces mayor, del orden de 0,09, para detectarse en la media de las 30.
- **Análisis secundario de H2.** Con dos consultas de desarrollo con bandas no hay base para estimar su variabilidad. Se informará de forma descriptiva, con su intervalo.

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

**Control negativo.** M4 se recalcula con los descriptores de M3 permutados al azar entre piezas del mismo museo, con semilla fija. Si el aporte de la estructura es real, debe desaparecer en esta condición. La permutación dentro de cada museo conserva la distribución de descriptores por museo, de modo que el control también comprueba que una eventual ganancia no procede de que la anotación capture, indirectamente, el museo de procedencia.

**Robustez.** Los resultados se informan según el museo de la consulta y según el estado de la pieza consultada. El estado es la completitud que el revisor escribió al decidir la curación de cada pieza: completo, incompleto o sin dato. Se mantiene el tercer grupo porque 61 de las 150 piezas de la galería no mencionan la completitud, y asignarlas a uno de los otros dos introduciría un error de clasificación. Con estos tamaños de muestra, el análisis es descriptivo.

**Tarea T1.** Las seis consultas escritas se ejecutan con M0, que compara la descripción con el texto de las fichas; con M2, que compara el vector de texto de la descripción, codificada sin plantilla porque T1 no tiene consultas de desarrollo, con los vectores de imagen; con M3, solo cuando la consulta trae especificación estructural y solo sobre los bloques especificados; y con M4, que fusiona los componentes disponibles con los pesos de T3. Sus resultados son descriptivos.

## 7.11 Interpretabilidad (H3)

Para cada resultado del top 10 de M4 en prueba se registran las contribuciones α′_c ŝ_c de cada componente, la máscara de observabilidad y la procedencia de cada valor. H3 se sostiene si se cumplen tres comprobaciones:

1. **Reconstrucción.** La suma de las contribuciones coincide con la puntuación, con un error ≤ 10⁻⁹, en todos los resultados.
2. **Intervención.** Retirar un componente modifica la puntuación exactamente como predice la fórmula, incluida la regla de reparto de pesos. Se verifica con pruebas de propiedades y sobre todos los resultados de prueba.
3. **Revisión humana.** En 10 resultados de prueba elegidos al azar (5 aciertos y 5 errores), el evaluador juzga si la explicación es correcta y no especulativa. Se informan los desacuerdos.

Las dos primeras comprobaciones son identidades de la fórmula (capítulo 5, proposición 5.9); lo que el experimento contrasta es que la implementación las satisface en todos los resultados, dentro de la tolerancia fijada. La tercera es la única que involucra un juicio. M4-RRF no interviene en H3, porque al operar sobre posiciones no conserva la descomposición de la puntuación.

## 7.12 Orden de ejecución y criterios de suspensión

El experimento sigue un orden obligatorio:

1. Congelación de los grupos, las particiones y la anotación (anotación v2.1, 17 de noviembre).
2. Desarrollo: rankings, juicios de desarrollo, selección de los pesos de M4 y estimación de la potencia (completado el 21 de noviembre).
3. Aprobación del protocolo por el asesor y congelación de los sistemas, con un manifiesto de ejecución que registra el commit, las sumas SHA-256 de todos los insumos, el punto de control de M2, los parámetros, el equipo y las semillas.
4. Selección de los pares de prueba y juicios de prueba, incluido el doble juicio parcial si hay segundo evaluador.
5. Una única ejecución del test.

**El test no se abre** si se da alguna de estas condiciones: hay grupos de piezas relacionadas repartidos entre particiones; algún juicio de prueba se derivó del descriptor, de CLIP o de cualquier otro modelo; la guía de anotación o el protocolo cambiaron sin registro; algún peso se ajustó con datos de prueba; o alguna imagen no está verificada. Antes de abrirlo se ejecuta una comprobación automática que reúne las condiciones verificables en el repositorio: la aprobación del protocolo y que no cambió después de aprobarse, la ausencia de fugas entre particiones, la anotación congelada y sus condiciones de buena formación, los pesos de M4, las sumas de las imágenes y la existencia de las consultas T1. La ejecución de los rankings de prueba se niega si encuentra un problema. La suspensión protege el test, pero no impide preparar código ni trabajar con los datos de desarrollo.

## 7.13 Amenazas a la validez

Las amenazas se ordenan por el tipo de validez que comprometen. Para cada una se indica qué se hizo para mitigarla y qué limitación subsiste.

**Cuadro 7.5.** Amenazas a la validez.

| Amenaza | Tipo de validez | Mitigación | Limitación que subsiste |
|---|---|---|---|
| A1. Una misma persona anota la estructura que usa M3 y juzga la relevancia | Interna y de constructo | Juicio ciego y aleatorizado; consultas fijadas de antemano; doble juicio parcial preparado | Sesgo residual a favor de M3; sin segundo evaluador a la fecha. Es la limitación principal |
| A2. Los juicios de desarrollo se aplicaron con un criterio de parecido global y después se revisaron con asistencia | De constructo | Uso restringido a pesos y potencia; prueba sin asistencia (sección 7.6.4) | Los pesos de M4 y la potencia heredan ambas reservas |
| A3. Un solo anotador | De constructo | Re-anotación ciega de 30 piezas; estabilidad informada por atributo | Mide estabilidad, no acuerdo entre personas |
| A4. La frontera entre lo observable y lo no observable es inestable | De constructo | Cobertura de bloques informada con cada comparación | Los bloques que compara M3 dependen de un juicio variable |
| A5. La anotación combina lecturas distintas y una revisión asistida | Interna | Criterios escritos y revisión de los lotes 2 a 5 antes de congelar; análisis de sensibilidad | La revisión cambia de forma apreciable los rankings de M3 (capítulo 4, sección 4.10.1) |
| A6. El eje y el sentido de lectura dependen de la fotografía | De constructo | Equivalencia por reversión; el eje no entra en el descriptor | Se pierde la orientación de las prendas que la tienen |
| A7. La estructura no es independiente de la técnica ni de la tradición | De constructo | Control sin orden; control negativo dentro de cada museo | Una ganancia de M3 puede reflejar pertenencia a una tradición |
| A8. Solo se juzgan los primeros candidatos de cada sistema | Interna | Pool con todos los sistemas más una muestra al azar; proporción juzgada informada | Sesgo contra sistemas ajenos al pool |
| A9. Piezas relacionadas en particiones distintas | Interna | Grupos decididos antes de partir; comprobación automática | Relaciones que ninguna señal propuso |
| A10. Las fotografías pudieron formar parte del preentrenamiento de M2 | Interna | Se declara | No puede medirse; favorecería a M2 |
| A11. Pocas consultas de prueba | De conclusión estadística | Permutación pareada; intervalo; efecto mínimo detectable fijado antes del test | Sin potencia para el umbral de 0,03 en H1; H2 diluida por las consultas sin bandas |
| A12. Pesos de M4 elegidos con diez consultas | De conclusión estadística | Rejilla pequeña, selección única y variante sin pesos | Ajuste posiblemente inestable |
| A13. M3 dispone de información humana que M2 no tiene | De constructo y externa | Se declara; M3 excluye el color | No se mide la extracción automática; el costo de anotar no se midió |
| A14. El corpus no es una muestra de los textiles andinos | Externa | Población definida de forma restrictiva; resultados por museo | No hay generalización fuera de la colección elegible |
| A15. Diferencias fotográficas entre museos | Interna y externa | Copia de evaluación común; M1 sobre el textil segmentado; análisis por museo | Tamaños pequeños por museo |

Tres de estas amenazas requieren un comentario adicional.

**A7. Estructura, técnica y tradición.** La organización visible no es independiente de cómo se tejió la pieza: en la faz de urdimbre la banda la fija el urdido, el tapiz deja libre la composición y algunos bordados imitan las bandas tejidas (Desrosiers, 2013, pp. 480–499). Una similitud estructural alta puede reflejar, en parte, la pertenencia a una misma tradición técnica, que un codificador visual también capta por la textura y el color. El control sin orden aísla el efecto de la secuencia respecto de la composición por tipos; el control negativo comprueba que el efecto no procede del museo. Ninguno separa por completo estructura y tradición, y el análisis por cultura atribuida será descriptivo.

**A10. Preentrenamiento.** Las fotografías de MET, CMA y AIC son públicas y pudieron formar parte de los datos con que se entrenó el codificador de M2, como reconocen Baldrati et al. (2022) para colecciones de arte. Esa posible fuga favorecería a M2 y hace más conservadora la comparación de H1.

**A13. Costo de la anotación.** Una comparación entre un sistema asistido por anotación y uno que solo usa píxeles exige conocer el costo de anotar. El tiempo por pieza no se registró, de modo que el manuscrito solo puede ofrecer una estimación, declarada como tal.

**Lo que estas amenazas implican para las conclusiones.**

- Un resultado favorable a H1 respaldará la utilidad de la estructura **anotada** en **esta colección**, con el sesgo residual de A1 declarado.
- Un resultado favorable a H2 indicará que la secuencia aporta más que la composición por tipos, sin separar por completo estructura y tradición (A7).
- Un resultado nulo será, con alta probabilidad, inconcluso y no negativo, por la potencia disponible (A11).
- H3 es independiente de todas las amenazas anteriores, porque es una propiedad del algoritmo; a cambio, no dice nada sobre el significado de las contribuciones.

## 7.14 Cierre del capítulo

El diseño convierte la pregunta del capítulo 2 en dos comparaciones pareadas y una verificación algorítmica, con un protocolo fijado antes de ver resultados de prueba. Las decisiones que dependían de datos (los pesos de la fusión y la potencia) se tomaron en desarrollo y una sola vez; las que dependían del juicio humano se rodearon de salvaguardas de procedimiento, y la asistencia usada en desarrollo se declara y se excluye de la prueba. El diseño tiene dos debilidades que no se pueden corregir con el tiempo disponible: un evaluador que también anotó, y una potencia que solo permite detectar efectos grandes. Ambas se declaran antes de conocer el resultado, para que este se lea en su justa medida. El capítulo 8 informará los resultados con la misma estructura.

## Referencias

Baldrati, A., Bertini, M., Uricchio, T., et al. (2022). Exploiting CLIP-based multi-modal approach for artwork classification and retrieval. Springer. https://doi.org/10.1007/978-3-031-20302-2_11 [verificar: autores restantes, título del volumen y páginas; versión leída: arXiv:2309.12110]

Bruch, S., Gai, S., & Ingber, A. (2023). *An analysis of fusion functions for hybrid retrieval* (arXiv:2210.11934v2). arXiv. https://arxiv.org/abs/2210.11934 [verificar: sede]

Buckley, C., Dimmick, D., Soboroff, I., & Voorhees, E. (2007). Bias and the limits of pooling for large collections. *Information Retrieval, 10*, 491–508. https://doi.org/10.1007/s10791-007-9032-x

Card, D., Henderson, P., Khandelwal, U., Jia, R., Mahowald, K., & Jurafsky, D. (2020). *With little power comes great responsibility* (arXiv:2010.06595). arXiv. https://arxiv.org/abs/2010.06595 [verificar: sede]

Cormack, G. V., Clarke, C. L. A., & Büttcher, S. (2009). Reciprocal rank fusion outperforms Condorcet and individual rank learning methods. En *Proceedings of the 32nd International ACM SIGIR Conference on Research and Development in Information Retrieval*. ACM. [verificar: páginas y DOI]

Desrosiers, S. (2013). El textil como matriz para el desarrollo de las artes plásticas en los Andes. *Revista Española de Antropología Americana, 43*(2), 477–514. https://doi.org/10.5209/rev_REAA.2013.v43.n2.44020

Sakai, T., Tao, S., & Zeng, Z. (2022). *Relevance assessments for web search evaluation: Should we randomise or prioritise the pooled documents? (Corrected version)* (arXiv:2211.00981). arXiv. https://arxiv.org/abs/2211.00981 [verificar: DOI de la versión de revista]

Smucker, M. D., Allan, J., & Carterette, B. (2007). A comparison of statistical significance tests for information retrieval evaluation. En *Proceedings of the 16th ACM Conference on Information and Knowledge Management (CIKM '07)* (pp. 623–632). ACM. https://doi.org/10.1145/1321440.1321528

Soboroff, I. (2025). Don't use LLMs to make relevance judgments. *Information Retrieval Research, 1*(1), 29–46. https://doi.org/10.54195/irrj.19625

Urbano, J., Lima, H., & Hanjalic, A. (2019). Statistical significance testing in information retrieval: An empirical analysis of type I, type II and type III errors. En *Proceedings of the 42nd International ACM SIGIR Conference on Research and Development in Information Retrieval (SIGIR '19)*. ACM. https://doi.org/10.1145/3331184.3331259
