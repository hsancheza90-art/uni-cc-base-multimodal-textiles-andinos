# 11. Limitaciones y trabajo futuro

> **Borrador 0.2, 23 de noviembre de 2026** (lista de limitaciones fijada antes del test y estabilidad del evaluador, según el dictamen del asesor del 21 de noviembre). Capítulo de la segunda parte de la tesis. Reúne las limitaciones declaradas en los capítulos 4, 5 y 7 y las ordena según lo que comprometen. Se redactó antes de ejecutar la prueba: las limitaciones que dependan del resultado (por ejemplo, la proporción juzgada del top 10 o la frecuencia de pares no evaluables) se añadirán después de los capítulos 8 y 9. Las marcas **[verificar: …]** señalan afirmaciones que dependen de una obra no leída en el proyecto.

## 11.1 Criterio de organización

Una limitación es pertinente en la medida en que condiciona lo que la tesis puede afirmar. Por eso este capítulo no repite cada salvedad de los capítulos anteriores, sino que las agrupa según el tipo de conclusión que limitan: qué mide la representación (sección 11.2), si la diferencia observada puede atribuirse al método (11.3), con qué precisión se estima (11.4) y a qué se extiende (11.5). La sección 11.6 trata los límites éticos y de gobernanza, y la 11.7 propone el trabajo futuro que se desprende de cada grupo.

**Limitaciones fijadas antes del test.** Las siguientes quedaron escritas en el protocolo antes de ejecutar ningún sistema sobre las consultas de prueba, y se mantienen cualquiera sea el resultado:

1. M3 y M4 dependen de una anotación humana, cuyo costo no se midió (sección 11.3).
2. Un solo evaluador, que además anotó la estructura (sección 11.3).
3. El pool es parcial: solo se juzgan los diez primeros de cada sistema y una muestra al azar, y lo no juzgado cuenta como 0 (sección 11.3).
4. La potencia es insuficiente para detectar una diferencia de 0,03 (sección 11.4).
5. Los pesos de M4 se eligieron con diez consultas (sección 11.4).
6. La generalización se restringe a la colección elegible (sección 11.5).
7. **No se estimó la estabilidad intraevaluador de los juicios de relevancia de prueba**, porque no se rejuzgó ninguna submuestra (sección 11.3).

## 11.2 Qué mide la representación

**Una codificación del investigador.** La palabra de bandas describe lo visible en una fotografía con un alfabeto de cinco tipos elegido para este estudio. No se afirma que el diseño se haya concebido así ni que esos tipos correspondan a categorías de quienes tejieron las piezas (capítulo 5, sección 5.14). «Similitud estructural» significa, en esta tesis, semejanza en esa codificación y en los demás bloques del descriptor, no en la estructura técnica del tejido.

**La escala de la fotografía.** El descriptor no registra la estructura de hilos (ligamento, dirección de la urdimbre, número de hilos), que es la escala de Helmer y Ngo (2015) y Ngo et al. (2021) y la que registran los especialistas en la ontología de Brownlow et al. (2015). La anotación no distingue una lista de urdimbre de una franja de trama ni de un registro bordado: registra las bandas por su aspecto. Tampoco registra el color ni el ancho de cada banda, de modo que dos piezas con la misma palabra pueden diferir mucho a la vista.

**La orientación.** La reversión descarta el sentido de lectura, lo que es convencional en un fragmento pero no en una prenda con extremos distinguibles, como una túnica con abertura de cuello. El eje registrado es el de la fotografía y no el del telar ni el de uso; en las túnicas de tapiz de la sierra el decorado se tejía acostado y la tela se giraba al armar la prenda (Desrosiers, 2024, pp. 10–11).

**Estructura, técnica y tradición.** La organización visible no es independiente de la técnica: en la faz de urdimbre la banda la fija el urdido, el tapiz deja libre la composición y algunos bordados imitan las bandas tejidas (Desrosiers, 2013, pp. 480–499). Una similitud estructural alta puede reflejar en parte la pertenencia a una tradición técnica, que un codificador visual también capta. Ni el control sin orden ni el control negativo por museo separan por completo estructura y tradición.

**Vocabulario técnico incompleto.** La categoría «tejido» es genérica, y faltan técnicas diagnósticas del área andina, como la faz de urdimbre, las urdimbres complementarias, las urdimbres y tramas discontinuas, la gasa, el teñido por amarras y el anillado [verificar: Emery, 1966, para la terminología de estructuras]. El término «lana» de las fichas no distingue la especie animal. Ninguno de esos campos interviene en el descriptor, pero limitan el uso del corpus para preguntas técnicas.

## 11.3 Si la diferencia puede atribuirse al método

**Circularidad entre anotación y juicio.** Una misma persona definió el esquema, anotó las 150 piezas y juzga la relevancia. Las salvaguardas de procedimiento (consultas fijadas de antemano, juicio ciego y en orden aleatorio, sin acceso a rankings ni a la anotación) impiden que el evaluador sepa qué sistema propuso cada candidato, pero no que su criterio coincida con el del descriptor. Es la limitación principal del estudio. Sin un segundo evaluador, los juicios no pueden presentarse como una verdad independiente de quien los emitió (capítulo 7, sección 7.6.3).

**Estabilidad del evaluador.** Los juicios de relevancia de prueba se emiten una sola vez. No se estimó la estabilidad intraevaluador de los juicios de prueba: ninguna submuestra se juzgó dos veces (decisión R38). La estabilidad medida en la tesis es la de la anotación, en otro procedimiento y con otra escala, y no la sustituye. Con un evaluador único puede haber variabilidad en sus propios juicios que el estudio no cuantifica.

**Un solo anotador.** La estabilidad intra-anotador, medida en 30 piezas, es una cota optimista de la fiabilidad entre personas y no la sustituye. Los atributos de los que depende H2 resultaron estables en ese lote (composición, κ = 0,84; palabra idéntica en 17 de 24 piezas), pero el atributo centro quedó en κ = 0,49 y la estabilidad de los lotes posteriores no se midió (capítulo 4, sección 4.9).

**Observabilidad inestable.** La decisión de si un atributo puede observarse fue menos estable que el valor anotado: en la composición, el acuerdo sobre la observabilidad corregido por azar fue nulo (κ = −0,10). Como la máscara decide qué bloques compara el descriptor, la disimilitud entre dos piezas depende en parte de un juicio que no se reproduce bien.

**Revisión asistida de la anotación.** La versión 2.1 incluye correcciones que partieron de propuestas de un modelo de visión y lenguaje, verificadas y firmadas por el anotador. 58 de las 108 decisiones coinciden con la propuesta, y no puede saberse cuántas habría tomado igual sin ella (Parasuraman y Manzey, 2010, p. 397). La revisión cambió al menos un atributo del descriptor en 46 de las 150 piezas y modificó de forma apreciable los rankings de desarrollo de M3: entre 4 y 9 piezas comunes en el top 10 y correlación de Spearman entre 0,56 y 0,91 (capítulo 4, sección 4.10.1). Las conclusiones sobre M3 valen para la versión congelada y no para la anotación en abstracto.

**Juicios de desarrollo asistidos.** Los juicios con que se eligieron los pesos de M4 y se estimó la potencia se revisaron con la segunda opinión de un modelo de visión y lenguaje. El acuerdo previo entre el evaluador y el modelo era bajo (κ = 0,161); en la revisión, el evaluador cambió 246 de los 411 grados, y la justificación firmada coincide con la del modelo en 406. El riesgo de que el evaluador se anclara en la propuesta del modelo no puede descartarse. Antes, esos juicios se habían aplicado con un criterio de parecido global más que estructural. Los pesos de la fusión y la planificación de la potencia heredan ambas reservas. El material de la revisión se conserva en un archivo de auditoría con su huella registrada. Los juicios de relevancia de prueba se emitirán sin asistencia de modelos, de modo que las conclusiones confirmatorias no dependen de juicios asistidos (capítulo 7, sección 7.6.4).

**Revisión de las explicaciones.** La revisión humana de diez explicaciones de M4 la hace el mismo evaluador que anotó la estructura, de modo que no es independiente. Es descriptiva y no interviene en H3, que solo verifica la fidelidad de la descomposición a la fórmula (capítulo 7, sección 7.11).

**Pooling.** Solo se juzgan los diez primeros candidatos de cada sistema y una muestra al azar; lo no juzgado cuenta como no relevante, lo que infravalora a los sistemas ajenos al pool (Buckley et al., 2007). Todos los sistemas comparados aportan al pool, pero las ablaciones que no aportan candidatos se evalúan con juicios incompletos.

**Preentrenamiento del codificador visual.** Las fotografías de los museos son públicas y pudieron formar parte de los datos de preentrenamiento de M2 (Baldrati et al., 2022). No puede medirse. Si ocurrió, favorece a M2.

**Sistemas con información desigual.** M3 y M4 disponen de etiquetas humanas que M2 no tiene. Una ventaja de M4 mide la utilidad de disponer de ese conocimiento, no la posibilidad de extraerlo de la imagen. El tiempo de anotación por pieza no se registró, de modo que el costo de esa ventaja solo puede estimarse.

## 11.4 Con qué precisión se estima

**Potencia.** Con 30 consultas de prueba, el efecto mínimo detectable en H1 se estima en 0,087 en nDCG@10 (rango de 0,060 a 0,159), unas tres veces el umbral práctico de 0,03; detectar ese umbral exigiría unas 250 consultas (capítulo 7, sección 7.8). Es una estimación aproximada de planificación, basada en diez consultas, y no una frontera de detectabilidad. Un resultado no significativo será, con alta probabilidad, inconcluso y no negativo, y un resultado significativo puede sobrestimar el efecto.

**H2 diluida por construcción.** En 21 de las 30 consultas de prueba la pieza no tiene palabra de bandas, y M3 y su control asignan la misma puntuación a todos los candidatos. La diferencia media de H2 se diluye en esa proporción, y el subgrupo de las 9 consultas restantes tiene muy pocas observaciones. La p de H2 es exacta y discreta: si menos de seis de esas diferencias son distintas de cero, no puede bajar de 0,05 cualquiera sea el resultado. Además, H2 solo es confirmatoria si H1 se sostiene, de modo que una conclusión confirmatoria sobre el orden es improbable. Solo 53 de las 150 piezas del núcleo tienen palabra de bandas, y solo 25 de los 1378 pares entre ellas difieren en el orden con el mismo histograma de tipos (capítulo 5, sección 5.13). La pregunta sobre el orden queda, por tanto, mal servida por la composición del corpus, con independencia de la calidad del descriptor.

**Pesos con diez consultas.** Los pesos de M4 se eligieron una sola vez, en una rejilla pequeña, con diez consultas de desarrollo. El respaldo de la combinación convexa con pocas consultas proviene de fusiones de dos sistemas y de colecciones con miles de consultas (Bruch et al., 2023). La variante sin pesos permite estimar cuánto depende el resultado de ese ajuste, pero no corrige su inestabilidad.

**Tamaños por museo.** Los análisis por museo y por estado de la pieza son descriptivos: con 30 consultas repartidas en tres museos, no admiten inferencia.

## 11.5 A qué se extienden las conclusiones

**Población.** Las conclusiones valen para la colección digital elegible del corpus principal v2 y, dentro de ella, para el núcleo de 150 piezas. Esa población está determinada por lo que tres museos estadounidenses adquirieron, fotografiaron y publicaron con licencia abierta, y por un criterio que privilegia las piezas cuyos colores y figuras se distinguen a primera vista. Quedan subrepresentadas las piezas muy fragmentarias, las monocromas y las de técnicas con poco contraste.

**Sesgo de conservación.** El clima de la costa desértica ha conservado textiles que en las tierras altas húmedas rara vez sobreviven (Desrosiers, 2024, pp. 2–3; 2013, p. 506). Las culturas costeras están sobrerrepresentadas, y la distribución por cultura del corpus no estima la de la producción textil andina.

**Atribuciones no verificadas.** La cultura, la fecha y la procedencia son las de cada ficha y no se verificaron. Ninguno de esos campos interviene en el descriptor, pero condicionan la estratificación y cualquier lectura por cultura.

**Puntaje de aptitud sin validación externa.** Las cifras del puntaje que apoyó la curación son de desarrollo. Su transferencia a una fuente nueva no está demostrada: la validación ciega en MET y CMA quedó por debajo del umbral fijado (κ = 0,56), y la recalibración posterior incluyó esa misma muestra (capítulo 4, sección 4.4.3).

**Revisión bibliográfica parcial.** La revisión la hizo un solo revisor, con una sola base consultada de forma nativa, y no pudo acceder a obras de referencia del dominio, entre ellas Washburn y Crowe (1988), Cereceda (1978) y Phillips (2018) (capítulo 3, sección 3.1). La afirmación de que no se encontró un estudio equivalente vale para lo recuperado.

## 11.6 Límites éticos y de gobernanza

La licencia abierta permite reutilizar las imágenes, pero no responde a las preguntas que los principios CARE plantean sobre datos de origen indígena: beneficio colectivo, autoridad para controlar, responsabilidad y ética (Carroll et al., 2020). Parte de las piezas procede de contextos funerarios, mencionados de forma explícita en al menos 24 de los 615 registros del consolidado, y ninguna comunidad de origen participó en su descripción. La tesis no puede afirmar que cumple esos principios. Lo que sí hace es acotar el uso: la anotación no atribuye significados, las atribuciones se conservan como las de cada museo, las imágenes no se redistribuyen y la ficha del corpus declara los usos para los que no está pensado (capítulo 4, sección 4.12).

Una limitación de otro orden es la asistencia de un modelo de lenguaje en dos procedimientos del estudio: la revisión de criterios de la anotación y la revisión de los juicios de desarrollo. Ambas se declaran y se acotan. Los juicios de relevancia de prueba se emitirán sin asistencia de modelos; M3 y M4 utilizarán, no obstante, la anotación congelada cuya revisión incluyó asistencia. Las dos revisiones introducen en datos de desarrollo y en la anotación un criterio que no es el del investigador ni el de un especialista, y cuya relación con los sistemas evaluados solo puede discutirse, no medirse (capítulo 7, sección 7.6.4).

## 11.7 Trabajo futuro

Cada grupo de limitaciones sugiere una línea de trabajo. Se ordenan de la más inmediata a la más amplia.

**Validez del juicio y de la anotación.**

1. **Segundo evaluador y segundo anotador.** El doble juicio parcial está preparado (cinco consultas de prueba juzgadas a ciegas por otra persona, con kappa ponderado y recálculo de la métrica). Es la mejora de validez más valiosa y la de menor costo. Un segundo anotador del núcleo permitiría medir el acuerdo entre personas, que la tesis solo aproxima con la estabilidad.
2. **Regla de observabilidad.** Una definición operativa de cuándo un atributo es observable, con ejemplos, y su estabilidad medida, reduciría la principal fuente de variabilidad del descriptor.
3. **Costo de la anotación.** Registrar el tiempo por pieza permitiría comparar la ganancia de un sistema asistido por anotación con su costo.

**Potencia y alcance de H2.**

4. **Más consultas con bandas.** Ampliar el núcleo con piezas con palabra de bandas, seleccionadas por una regla fijada de antemano y sin mirar resultados, aumentaría la proporción de consultas en que el orden puede actuar. La alternativa de completar la anotación congelada a la vista de los resultados se descartó porque alteraría datos observados (decisión R27).
5. **Más consultas en general.** El efecto mínimo detectable indica el orden de magnitud necesario para el umbral de 0,03 en H1: unas 250 consultas. Un estudio de ese tamaño exige varios evaluadores y un diseño de pooling más económico, como la evaluación con juicios incompletos que analizan Carterette y Smucker (2007).

**Representación.**

6. **Extracción automática de la estructura.** Predecir la palabra de bandas y los demás bloques desde la imagen convertiría M3 en un sistema comparable con M2 en información disponible. El marco natural es el de los modelos con cuello de botella de conceptos (Koh et al., 2020), en que la decisión pasa por conceptos legibles que pueden intervenirse. La anotación v2.1 serviría como datos de entrenamiento y de evaluación.
7. **Color y proporción de las bandas.** Una palabra con atributos por símbolo (color dominante, ancho relativo) acercaría la representación a lo que una persona compara, a costa de más anotación y de una distancia más compleja.
8. **Orientación.** Para las prendas completas con extremos distinguibles, un descriptor que no identifique una palabra con su reverso conservaría información que la reversión descarta.
9. **Distancia métrica.** Sustituir la normalización por la longitud mayor por una que conserve la desigualdad triangular (Marzal y Vidal, 1993; Yujian y Bo, 2007) [verificar: citas exactas] permitiría usar índices métricos y agrupamiento, la tarea del primer avance que la tesis aplazó.
10. **Relaciones entre regiones.** El primer avance proponía representar las relaciones entre motivos y regiones con grafos (ecuaciones 5.50 a 5.52), una línea que la tesis retiró por requerir relaciones tipadas y anotación adicional. Sigue siendo la extensión natural de la palabra de bandas a composiciones que no son de bandas, como los paneles y las retículas, que en el núcleo reúnen 72 de las 150 piezas.
11. **Escalas combinadas.** Vincular la macroestructura visible con la estructura técnica, en piezas para las que existan ambas descripciones, permitiría estudiar empíricamente la relación entre técnica y organización visible que la tesis solo puede declarar.

**Corpus y gobernanza.**

12. **Nuevas fuentes.** La incorporación de una cuarta colección con licencia abierta, como la Yale University Art Gallery o el Cooper Hewitt, exigiría una validación ciega del puntaje de aptitud antes de usar sus sugerencias.
13. **Colecciones peruanas y participación de las comunidades.** El acceso a colecciones de museos peruanos requiere convenios institucionales, y la descripción de las piezas con participación de las comunidades de origen es la condición para avanzar hacia los principios CARE. Ambas exceden el plazo de una tesis de maestría y son, a la vez, las que más cambiarían el sentido del corpus.

**Revisión bibliográfica.**

14. **Búsqueda completa.** Repetir las búsquedas en Scopus, Web of Science, IEEE Xplore y ACM Digital Library con acceso institucional, y leer las obras localizadas que no pudieron consultarse, en particular Phillips (2018) sobre patrones de franjas en textiles de faz de urdimbre y Cereceda (1978) sobre la disposición de las listas en las talegas de Isluga.

## 11.8 Cierre del capítulo

Las limitaciones de la tesis son las de un estudio piloto con una sola persona en los papeles de anotador y evaluador, una galería de 150 piezas y 30 consultas de prueba. Ninguna invalida el diseño, pero todas acotan lo que puede concluirse: la tesis puede responder si, en esta colección y con esta anotación, la fusión que incluye la estructura mejora de forma detectable a un codificador general, explorar con las ablaciones qué parte corresponde a la estructura, y verificar que la explicación de la fusión es fiel a su cálculo. No puede responder si la estructura textil andina, en general, es recuperable desde fotografías, ni qué significa para quienes la tejieron. El trabajo futuro más inmediato, un segundo evaluador y más consultas con bandas, está al alcance de una extensión del mismo estudio.

## Referencias

Baldrati, A., Bertini, M., Uricchio, T., et al. (2022). Exploiting CLIP-based multi-modal approach for artwork classification and retrieval. Springer. https://doi.org/10.1007/978-3-031-20302-2_11 [verificar: autores restantes, título del volumen y páginas; versión leída: arXiv:2309.12110]

Brownlow, R., Capuzzi, S., Helmer, S., Martins, L., Normann, I., & Poulovassilis, A. (2015). An ontological approach to creating an Andean weaving knowledge base. *ACM Journal on Computing and Cultural Heritage*. https://doi.org/10.1145/2700427 [verificar: volumen, número y artículo]

Bruch, S., Gai, S., & Ingber, A. (2023). *An analysis of fusion functions for hybrid retrieval* (arXiv:2210.11934v2). arXiv. https://arxiv.org/abs/2210.11934 [verificar: sede]

Buckley, C., Dimmick, D., Soboroff, I., & Voorhees, E. (2007). Bias and the limits of pooling for large collections. *Information Retrieval, 10*, 491–508. https://doi.org/10.1007/s10791-007-9032-x

Carroll, S. R., Garba, I., Figueroa-Rodríguez, O. L., Holbrook, J., Lovett, R., Materechera, S., Parsons, M., Raseroka, K., Rodriguez-Lonebear, D., Rowe, R., Sara, R., Walker, J. D., Anderson, J., & Hudson, M. (2020). The CARE principles for Indigenous data governance. *Data Science Journal, 19*, 43, 1–12. https://doi.org/10.5334/dsj-2020-043

Carterette, B., & Smucker, M. D. (2007). Hypothesis testing with incomplete relevance judgments. En *Proceedings of the 16th ACM Conference on Information and Knowledge Management (CIKM '07)*. ACM. https://doi.org/10.1145/1321440.1321530 [verificar: páginas]

Desrosiers, S. (2013). El textil como matriz para el desarrollo de las artes plásticas en los Andes. *Revista Española de Antropología Americana, 43*(2), 477–514. https://doi.org/10.5209/rev_REAA.2013.v43.n2.44020

Desrosiers, S. (2024). Creación textil en los Andes: el lenguaje de los hilos y su transmisión a través del tiempo. En *Arte y saber del textil* (pp. 1–27). Banco de Crédito del Perú. [verificar: editores e ISBN]

Helmer, S., & Ngo, V. M. (2015). A similarity measure for weaving patterns in textiles. En *Proceedings of the 38th International ACM SIGIR Conference on Research and Development in Information Retrieval* (pp. 163–172). https://doi.org/10.1145/2766462.2767735

Koh, P. W., Nguyen, T., Tang, Y. S., Mussmann, S., Pierson, E., Kim, B., & Liang, P. (2020). Concept bottleneck models. En *Proceedings of the 37th International Conference on Machine Learning* (Vol. 119). PMLR. https://arxiv.org/abs/2007.04612 [verificar: páginas]

Ngo, V. M., Helmer, S., Le-Khac, N.-A., & Kechadi, M.-T. (2021). Structural textile pattern recognition and processing based on hypergraphs. *Information Retrieval Journal, 24*, 137–173. https://doi.org/10.1007/s10791-020-09384-y

Parasuraman, R., & Manzey, D. H. (2010). Complacency and bias in human use of automation: An attentional integration. *Human Factors, 52*(3), 381–410. https://doi.org/10.1177/0018720810376055

**Obras citadas sin ficha de lectura en el proyecto (verificar la cita exacta):**

Cereceda, V. (1978). Sémiologie des tissus andins: les talegas d'Isluga. *Annales. Économies, Sociétés, Civilisations, 33*(5–6), 1017–1035.

Emery, I. (1966). *The primary structures of fabrics: An illustrated classification*. The Textile Museum.

Marzal, A., & Vidal, E. (1993). Computation of normalized edit distance and applications. *IEEE Transactions on Pattern Analysis and Machine Intelligence, 15*(9), 926–932.

Phillips, A. (2018). Colored strip patterns and front-back symmetry in warp-faced pre-Columbian textiles. *Leonardo*. https://doi.org/10.1162/leon_a_01691 [localizado, no leído]

Washburn, D. K., & Crowe, D. W. (1988). *Symmetries of culture: Theory and practice of plane pattern analysis*. University of Washington Press.

Yujian, L., & Bo, L. (2007). A normalized Levenshtein distance metric. *IEEE Transactions on Pattern Analysis and Machine Intelligence, 29*(6), 1091–1095.
