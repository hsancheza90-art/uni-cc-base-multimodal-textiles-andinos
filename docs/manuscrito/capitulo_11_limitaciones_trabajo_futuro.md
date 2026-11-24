# 11. Limitaciones y trabajo futuro

Una limitación es pertinente en la medida en que condiciona lo que la tesis puede afirmar. Este capítulo no repite las amenazas a la validez que el diseño anticipó y mitigó (capítulo 7, sección 7.13), sino que examina cuáles de ellas subsisten a la vista de los resultados y qué alcance dejan a cada conclusión. Las agrupa según lo que comprometen: qué mide la representación (sección 11.1), si la diferencia observada puede atribuirse al método (11.2), con qué precisión se estima (11.3) y a qué se extiende (11.4). La sección 11.5 trata los límites éticos, y la 11.6, el trabajo futuro.

## 11.1 Qué mide la representación

**Una codificación del investigador.** La palabra de bandas describe lo visible en una fotografía con un alfabeto de cinco tipos elegido para este estudio. No se afirma que el diseño se haya concebido así ni que esos tipos correspondan a categorías de quienes tejieron las piezas. «Similitud estructural» significa, en esta tesis, semejanza en esa codificación y en los demás bloques del descriptor, no en la construcción técnica del tejido.

**La escala de la fotografía.** El descriptor no registra la estructura de los hilos, que es la escala de Helmer y Ngo (2015), Ngo et al. (2021) y Brownlow et al. (2015). La anotación no distingue si una franja se formó con hilos de urdimbre, con hilos de trama o con bordado, ni registra el color o el ancho de cada banda. Por eso el estudio no pudo comprobar la explicación que la discusión propone para el resultado de H2, que relaciona la simetría de las secuencias con la técnica de urdido (capítulo 9, sección 9.3).

**La orientación.** La equivalencia por reversión descarta el sentido de lectura de la pieza, lo que es razonable en un fragmento pero no en una prenda con extremos distinguibles, como una túnica con abertura de cuello. El eje registrado es el de la fotografía, no el del telar (capítulo 3, sección 3.2).

**Estructura, técnica y tradición.** Una similitud estructural alta puede reflejar en parte la pertenencia a una misma familia técnica o estilística, que un codificador visual también capta. El control negativo descarta que la ganancia proceda de la distribución de descriptores de cada museo, pero no separa la estructura de la tradición dentro de un mismo museo (capítulo 9, sección 9.2).

## 11.2 Si la diferencia puede atribuirse al método

**Anotador y evaluador son la misma persona.** Es la limitación principal del estudio y la que más condiciona H1. Las salvaguardas del diseño (consultas fijadas de antemano, juicio a ciegas y en orden aleatorio, sin acceso a rankings, puntuaciones ni anotación) impidieron que el evaluador supiera qué sistema propuso cada candidato, pero no que su criterio para reconocer una organización semejante coincidiera con el que aplicó al anotar. La ganancia de la estructura dentro de la fusión puede deberse en parte a esa coincidencia. El doble juicio parcial previsto en el protocolo, que habría estimado el efecto con un segundo evaluador, no se realizó.

**Estabilidad del evaluador y del anotador.** Los juicios de prueba se emitieron una sola vez, y su estabilidad no se midió. La estabilidad que se midió es la de la anotación, en 30 piezas: alta en diez de los once atributos con kappa, baja en el campo central (κ = 0,49) y nula en la decisión de si la composición es observable (κ = −0,10) (capítulo 4, sección 4.9). Es una cota optimista de la fiabilidad entre personas y no la sustituye.

**Asistencia en la anotación y en el desarrollo.** La anotación congelada incluye correcciones que partieron de propuestas de un modelo de visión y lenguaje, verificadas y firmadas por el anotador (capítulo 4, sección 4.10.1), y los juicios de desarrollo con que se eligieron los pesos de M4 se revisaron con la segunda opinión de un modelo (capítulo 7, sección 7.6.4). Los juicios de la evaluación final se emitieron sin asistencia, de modo que las conclusiones confirmatorias no descansan en juicios asistidos; M3 y M4, en cambio, usan una anotación cuya revisión la incluyó, y los pesos de la fusión heredan las reservas de los juicios de desarrollo. La variante sin pesos, que también supera al codificador visual, indica que la conclusión de H1 no depende de esos pesos (capítulo 9, sección 9.1).

**Información desigual entre sistemas.** M3 y M4 disponen de etiquetas humanas que M2 no tiene. La ventaja de M4 mide la utilidad de disponer de ese conocimiento, no la posibilidad de extraerlo de la imagen. El tiempo de anotación por pieza no se registró, de modo que el costo de esa ventaja no puede compararse con su beneficio.

**Pooling.** Los siete rankings que aportaron candidatos al pool quedaron juzgados por completo en sus diez primeros resultados, y ningún par se marcó como no evaluable, de modo que las comparaciones de H1 y H2 no dependen de juicios faltantes. Las ablaciones y el control negativo, que no aportaron candidatos, se evaluaron con juicios incompletos: sus valores son cotas inferiores, en particular el de la variante que solo usa los bloques de bandas, con un 40 % de su top 10 juzgado. La sensibilidad a los aportes exclusivos afecta sobre todo a M1 y M0, cuyos rankings comparten pocos candidatos con los demás (capítulo 8, sección 8.6).

**Preentrenamiento del codificador visual.** Las fotografías de los museos son públicas y pudieron formar parte de los datos de preentrenamiento de OpenCLIP (Baldrati et al., 2022). No puede medirse; si ocurrió, favorece a M2 y hace conservadora la diferencia observada.

**Revisión de las explicaciones.** La revisión de diez explicaciones la hizo el mismo evaluador que anotó la estructura, y el criterio para decidir cuándo una contribución era alta o baja se fijó durante la revisión, no antes. Es descriptiva y no interviene en H3.

## 11.3 Con qué precisión se estima

**H1.** La diferencia observada (0,112) supera el efecto mínimo detectable estimado en la planificación (0,087), y su intervalo excluye el cero. Con 30 consultas, el intervalo sigue siendo amplio (0,062 a 0,164), y un efecto seleccionado por resultar significativo con potencia limitada puede estar sobrestimado (Card et al., 2020). La mejora es clara en dirección; su magnitud exacta, no.

**H2.** La pregunta por el orden quedó mal servida por la composición del corpus. Solo 9 de las 30 consultas de prueba tenían palabra de bandas, y entre las 53 piezas con bandas de la galería solo 25 pares comparten la proporción de tipos y difieren en el orden (capítulo 5, sección 5.13). La prueba exacta podía alcanzar significación con las nueve diferencias distintas de cero, pero con tan pocas observaciones el intervalo del subgrupo es amplio (−0,121 a 0,020). El resultado no permite afirmar que el orden carezca de valor, sino que no se detectó en este corpus.

**Pesos con diez consultas.** Los pesos de M4 se eligieron una sola vez con diez consultas de desarrollo, un número que la literatura sobre fusión no respalda (Bruch et al., 2023). La variante sin pesos acota cuánto depende el resultado de ese ajuste, pero no corrige su inestabilidad.

**Grupos pequeños.** Los análisis por museo, por estado de la pieza y la tarea de texto a imagen, con entre 3 y 15 consultas por grupo, son descriptivos y no admiten inferencia.

## 11.4 A qué se extienden las conclusiones

**Población.** Las conclusiones valen para la galería de 150 piezas y, con cautela, para el corpus principal del que se extrajo. Esa población está determinada por lo que tres museos estadounidenses adquirieron, fotografiaron y publicaron con licencia abierta, y por un criterio de selección que privilegia las piezas cuyos colores y figuras se distinguen a primera vista. Quedan subrepresentadas las piezas muy fragmentarias, las monocromas y las de técnicas con poco contraste.

**Sesgo de conservación.** El clima de la costa desértica ha conservado textiles que en las tierras altas húmedas rara vez sobreviven (Desrosiers, 2024, pp. 2–3), de modo que las culturas costeras están sobrerrepresentadas y la distribución por cultura del corpus no representa la producción textil andina.

**Atribuciones no verificadas.** La cultura, la fecha y la procedencia son las de cada ficha y no se verificaron. No intervienen en el descriptor, pero condicionan la estratificación y cualquier lectura por cultura.

**Puntaje de aptitud.** El puntaje que apoyó la curación es una herramienta de desarrollo. Su transferencia a una fuente nueva no está demostrada: la validación ciega en MET y CMA quedó por debajo del umbral fijado (κ = 0,56) (capítulo 4, sección 4.4.3).

**Revisión bibliográfica.** La revisión la hizo un solo revisor, con una sola base consultada de forma nativa, y algunas obras de referencia del dominio no pudieron consultarse. La afirmación de que no se encontró un estudio equivalente vale para lo recuperado.

## 11.5 Límites éticos

La licencia abierta permite reutilizar las imágenes, pero no responde a las preguntas que los principios CARE plantean sobre los datos de origen indígena: beneficio colectivo, autoridad para controlar, responsabilidad y ética (Carroll et al., 2020). Parte de las piezas procede de contextos funerarios, mencionados de forma explícita en al menos 24 de los 615 registros del consolidado, y ninguna comunidad de origen participó en su descripción. La tesis no puede afirmar que cumple esos principios. Lo que sí hace es acotar el uso: la anotación describe la organización visible y no atribuye significados, las atribuciones se conservan como las publica cada museo, las imágenes no se redistribuyen y la ficha del corpus indica los usos para los que no está pensado (capítulo 4, sección 4.12).

## 11.6 Trabajo futuro

Las líneas de trabajo se ordenan de la más inmediata a la más amplia.

**Validez del juicio y de la anotación.**

1. **Segundo evaluador y segundo anotador.** Es la mejora de validez más valiosa y la de menor costo. El protocolo ya define el doble juicio de cinco consultas de prueba, con kappa ponderado y recálculo de la métrica principal; un segundo anotador del núcleo permitiría medir el acuerdo entre personas.
2. **Regla de observabilidad.** Una definición operativa de cuándo un atributo es observable, con ejemplos y su estabilidad medida, reduciría la principal fuente de variabilidad del descriptor.
3. **Costo de la anotación.** Registrar el tiempo por pieza permitiría comparar la ganancia de un sistema asistido por anotación con su costo.

**El orden de las bandas.**

4. **Una galería con más bandas.** Ampliar la galería con piezas que tengan palabra de bandas, elegidas por una regla fijada de antemano, aumentaría el número de consultas en que el orden puede actuar y permitiría contrastar H2 con potencia suficiente.
5. **Técnica y simetría.** Registrar la técnica de cada pieza permitiría contrastar la explicación propuesta para H2: que la simetría de las secuencias, ligada al urdido, hace que el inventario determine el orden. Esa línea debería empezar por la literatura sobre la simetría de los patrones de franjas en textiles de faz de urdimbre, localizada durante la revisión pero no consultada.
6. **Más consultas en general.** Detectar con potencia suficiente una diferencia de 0,03 exigiría unas 250 consultas, lo que requiere varios evaluadores y un diseño de juicio más económico, como la evaluación con juicios incompletos que analizan Carterette y Smucker (2007).

**Representación.**

7. **Extracción automática de la estructura.** Predecir la composición, el borde, la simetría y la palabra de bandas desde la imagen convertiría M3 en un sistema comparable con M2 en información disponible. El marco natural es el de los modelos con cuello de botella de conceptos (Koh et al., 2020), en que la decisión pasa por conceptos legibles que pueden intervenirse; la anotación congelada serviría como datos de entrenamiento y de evaluación. A la vista de los resultados, la extracción debería priorizar los bloques que sostuvieron la ganancia antes que la secuencia de bandas.
8. **Color, ancho y orientación de las bandas.** Una palabra con atributos por banda, y un descriptor que distinga una prenda de su reverso cuando sus extremos son distinguibles, acercarían la representación a lo que una persona compara, a costa de más anotación y de una distancia más compleja.
9. **Relaciones entre regiones.** Representar con grafos las relaciones entre motivos y regiones extendería el descriptor a las composiciones que no son de bandas, como los paneles y las retículas, que en el núcleo reúnen 72 de las 150 piezas.
10. **Utilidad de las explicaciones.** Evaluar con curadores e investigadores, distintos del autor y con una tarea definida, si la descomposición de la puntuación ayuda a entender y corregir los resultados.

**Corpus y gobernanza.**

11. **Nuevas fuentes.** Incorporar una cuarta colección con licencia abierta, como la Yale University Art Gallery o el Cooper Hewitt, con una validación ciega del puntaje de aptitud antes de usar sus sugerencias.
12. **Colecciones peruanas y participación de las comunidades.** El acceso a colecciones de museos peruanos requiere convenios institucionales, y la descripción de las piezas con participación de las comunidades de origen es la condición para avanzar hacia los principios CARE. Ambas exceden el plazo de una tesis de maestría y son, a la vez, las que más cambiarían el sentido del corpus.

## Referencias

Baldrati, A., Bertini, M., Uricchio, T., et al. (2022). Exploiting CLIP-based multi-modal approach for artwork classification and retrieval. Springer. https://doi.org/10.1007/978-3-031-20302-2_11

Brownlow, R., Capuzzi, S., Helmer, S., Martins, L., Normann, I., & Poulovassilis, A. (2015). An ontological approach to creating an Andean weaving knowledge base. *ACM Journal on Computing and Cultural Heritage*. https://doi.org/10.1145/2700427

Bruch, S., Gai, S., & Ingber, A. (2023). *An analysis of fusion functions for hybrid retrieval* (arXiv:2210.11934v2). arXiv. https://arxiv.org/abs/2210.11934

Card, D., Henderson, P., Khandelwal, U., Jia, R., Mahowald, K., & Jurafsky, D. (2020). *With little power comes great responsibility* (arXiv:2010.06595). arXiv. https://arxiv.org/abs/2010.06595

Carroll, S. R., Garba, I., Figueroa-Rodríguez, O. L., Holbrook, J., Lovett, R., Materechera, S., Parsons, M., Raseroka, K., Rodriguez-Lonebear, D., Rowe, R., Sara, R., Walker, J. D., Anderson, J., & Hudson, M. (2020). The CARE principles for Indigenous data governance. *Data Science Journal, 19*, 43, 1–12. https://doi.org/10.5334/dsj-2020-043

Carterette, B., & Smucker, M. D. (2007). Hypothesis testing with incomplete relevance judgments. En *Proceedings of the 16th ACM Conference on Information and Knowledge Management (CIKM '07)*. ACM. https://doi.org/10.1145/1321440.1321530

Desrosiers, S. (2024). Creación textil en los Andes: el lenguaje de los hilos y su transmisión a través del tiempo. En *Arte y saber del textil* (pp. 1–27). Banco de Crédito del Perú.

Helmer, S., & Ngo, V. M. (2015). A similarity measure for weaving patterns in textiles. En *Proceedings of the 38th International ACM SIGIR Conference on Research and Development in Information Retrieval* (pp. 163–172). https://doi.org/10.1145/2766462.2767735

Koh, P. W., Nguyen, T., Tang, Y. S., Mussmann, S., Pierson, E., Kim, B., & Liang, P. (2020). Concept bottleneck models. En *Proceedings of the 37th International Conference on Machine Learning* (Vol. 119). PMLR. https://arxiv.org/abs/2007.04612

Ngo, V. M., Helmer, S., Le-Khac, N.-A., & Kechadi, M.-T. (2021). Structural textile pattern recognition and processing based on hypergraphs. *Information Retrieval Journal, 24*, 137–173. https://doi.org/10.1007/s10791-020-09384-y
