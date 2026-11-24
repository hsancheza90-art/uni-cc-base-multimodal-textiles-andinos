# 2. Problema, objetivos e hipótesis

## 2.1 Planteamiento del problema

Una parte considerable del diseño textil andino prehispánico se organiza en unidades que se repiten y se ordenan sobre la superficie: franjas o bandas, paneles, retículas, bordes decorados y campos centrales. Esa organización no es un ornamento añadido a posteriori. En los tejidos de faz de urdimbre, aquellos en que los hilos longitudinales (la urdimbre) cubren la superficie y forman el diseño, la disposición de esos hilos antes de empezar a tejer fija qué colores puede tener cada banda (Desrosiers, 2013, pp. 480 y 482; capítulo 3, sección 3.2). Es, además, visible en una fotografía de museo y es un criterio habitual de comparación para quien estudia las piezas: dos tejidos pueden parecerse por la disposición de sus bandas aunque difieran en color, en iconografía o en estado de conservación.

Las colecciones digitales de los museos ofrecen dos vías de acceso a estas piezas, y ninguna recoge esa organización de forma explícita. La primera es la ficha curatorial, que describe material, técnica, cultura atribuida y fecha con un vocabulario que varía entre instituciones. En el corpus de esta tesis, la descripción curatorial existe en 29 de 155 registros del Metropolitan Museum of Art (MET), en 53 de 108 del Cleveland Museum of Art (CMA) y en 43 de 352 del Art Institute of Chicago (AIC) (capítulo 4, sección 4.2.2). La segunda vía es la imagen, que los codificadores visión-lenguaje preentrenados convierten en un vector, una representación numérica general de su contenido. Estos codificadores tienden a tratar el contenido como una bolsa de elementos sin orden: CLIP acierta el 56 % de las relaciones espaciales entre objetos, con el azar en 50 % (Yuksekgonul et al., 2023, p. 4), y queda por debajo del azar cuando dos imágenes solo difieren en la disposición de los mismos elementos (Thrush et al., 2022, p. 6). Esa evidencia procede de fotografías naturales y no demuestra que ocurra lo mismo al comparar textiles: motiva la pregunta, no la responde.

La recuperación de textiles por su estructura tiene antecedentes, pero a otra escala: la estructura de los cruces de hilos, modelada a mano para cada pieza y evaluada contra categorías de tejido (Helmer y Ngo, 2015; Ngo et al., 2021), o las técnicas registradas por especialistas en una ontología y consultadas por coincidencia exacta de atributos (Brownlow et al., 2015). En los trabajos de recuperación patrimonial revisados, la pertinencia de un resultado se toma de la identidad de la pieza, de los metadatos o de una categoría (Ypsilantis et al., 2021; Rei et al., 2023; Dorozynski y Rottensteiner, 2022), y en ningún caso de un juicio humano graduado sobre la organización visible del diseño (capítulo 3, sección 3.5). En la búsqueda realizada, de alcance parcial, no se encontró un estudio que evalúe con juicios de ese tipo si la secuencia de bandas visible en fotografías de museo añade utilidad a un codificador visión-lenguaje congelado (capítulo 3, sección 3.9).

El problema que aborda la tesis es, en consecuencia, de representación y de evidencia. De representación, porque es preciso formalizar la organización visible de un textil de modo que pueda compararse entre piezas, registrando lo que la fotografía muestra y distinguiendo lo ausente de lo que no puede observarse. De evidencia, porque es preciso comprobar, con un diseño que no favorezca al método propuesto, si esa representación aporta algo que las señales textuales y visuales generales no aportan ya.

## 2.2 Del primer avance a una pregunta contrastable

El primer avance formuló el problema como la construcción de una representación multimodal de textiles andinos que integrara imagen, atributos estructurales, texto y contexto cultural, para tareas de similitud, recuperación y agrupamiento. Esa formulación sigue siendo la orientación general de la tesis, con sus dos principios: representar no es descifrar, y la representación computacional no sustituye la interpretación arqueológica, antropológica o comunitaria. Como pregunta de investigación, sin embargo, no fijaba un criterio de éxito: no precisaba con qué se compararía la representación, en qué tarea, con qué medida ni quién decidiría qué resultado es pertinente. La segunda parte conserva el problema y estrecha la pregunta: elige una tarea, una medida, un árbitro y una comparación principal.

La multimodalidad se mantiene, pero cambia de forma. El primer avance representaba cada textil como una tupla de información visual, estructural, textual y contextual, y proponía aprender a partir de ella una representación conjunta. En la segunda parte, cada modalidad alimenta un sistema separado (la imagen, a M1 y M2; la anotación estructural, a M3; el texto de la ficha, a M0) y las puntuaciones se combinan en una fusión tardía (capítulo 5, sección 5.10). Hay tres razones: con 150 piezas anotadas no hay datos supervisados para aprender una representación conjunta; los espacios de los sistemas no están alineados, de modo que sumar sus vectores carece de sentido; y la forma aditiva es la que permite contrastar la fidelidad de la explicación (H3). El contexto curatorial (museo, cultura atribuida, fecha) no se usa como señal de similitud, porque recuperaría por atribución y no por organización visible; sirve para estratificar las particiones y para el análisis por museo. De las tareas del plan preliminar, la recuperación de texto a imagen se conserva como tarea exploratoria (T1); la de imagen a texto y el agrupamiento exploratorio quedan fuera, porque la primera no responde a la pregunta sobre la organización visible y el segundo carece en este corpus de una partición de referencia que permita sostener o refutar una hipótesis. El anexo C detalla la correspondencia entre ambas formulaciones.

## 2.3 Preguntas de investigación

**Pregunta general.**

> En un conjunto congelado de textiles andinos fotografiados por museos, ¿añadir el orden de las bandas y las relaciones entre regiones, mediante un descriptor estructural derivado de anotación humana, mejora la recuperación por similitud estructural respecto de las señales textuales y visuales generales, según juicios humanos independientes de los sistemas? ¿Permite, además, explicar el ranking de forma fiel?

La pregunta es contrastable porque fija los términos de la comparación: los sistemas que se comparan, la tarea (recuperación por ejemplar, T3), la medida y el árbitro. La medida es nDCG@10 por consulta, la ganancia acumulada descontada normalizada en los diez primeros resultados, que vale 1 cuando el sistema coloca los candidatos en el orden ideal de relevancia (capítulo 7, sección 7.7); el árbitro, los juicios de una persona que, sin saber qué sistema propuso cada candidato, gradúa su semejanza con la consulta en una escala de cuatro grados.

**Preguntas específicas.**

1. **PE1.** ¿Qué parte de la organización visible de un textil puede registrarse sobre una fotografía de museo con un vocabulario controlado, distinguiendo lo ausente de lo que no puede observarse, y con qué estabilidad?
2. **PE2.** ¿Cómo formalizar esa organización como un objeto comparable entre piezas, con propiedades demostrables, y cómo aislar la contribución del orden de las bandas respecto de su composición por tipos?
3. **PE3.** ¿Recupera mejor la fusión del codificador visión-lenguaje congelado con el texto de la ficha y la estructura anotada que el codificador solo? ¿Qué parte de esa diferencia se pierde al retirar la estructura?
4. **PE4.** ¿Aporta el orden de las bandas más que el inventario de sus tipos?
5. **PE5.** ¿Puede descomponerse la puntuación del sistema combinado en contribuciones exactas de sus componentes, de modo que la explicación del ranking sea fiel al cálculo?

PE1 y PE2 son preguntas de diseño y se responden en los capítulos 4 y 5. PE3, PE4 y PE5 se responden con las hipótesis H1, H2 y H3; la segunda parte de PE3, con la ablación de M4 sin M3, que es exploratoria.

## 2.4 Objetivos

**Objetivo general.** Determinar si un descriptor de la macroestructura visible de los textiles andinos, que considera el orden de las bandas y las relaciones entre regiones, aporta utilidad a la recuperación por similitud estructural frente a representaciones textuales y visuales generales, y si su aporte puede explicarse de forma fiel.

**Objetivos específicos.**

**Cuadro 2.1.** Objetivos específicos y productos verificables.

| | Objetivo | Producto verificable | Capítulo |
|---|---|---|---|
| OE1 | Construir y documentar un corpus multimodal de textiles andinos procedentes de colecciones abiertas, con criterios de selección explícitos y con agrupación de las piezas relacionadas | Corpus versión 2.0 con grupos, licencias y sumas de verificación | 4 |
| OE2 | Formalizar la macroestructura observable y anotarla con un protocolo que registre lo que no puede observarse, midiendo la estabilidad de la anotación | Esquema de anotación, anotación congelada (versión 2.1) e informe de estabilidad | 4 |
| OE3 | Definir un descriptor estructural y una disimilitud entre piezas, con sus propiedades demostradas o verificadas, y un control que aísle el efecto del orden | Formalización, implementación de M3 y M3-sin-orden, y pruebas de propiedades | 5 y 6 |
| OE4 | Evaluar, con un protocolo fijado de antemano y juicios humanos ciegos, la utilidad del descriptor solo y en fusión con texto e imagen, frente a un codificador visión-lenguaje congelado | Resultados por consulta, con intervalos, ablaciones y control negativo | 7 y 8 |
| OE5 | Comprobar que la puntuación del sistema combinado se descompone exactamente en las contribuciones de sus componentes | Reconstrucción e intervención sobre los resultados de la evaluación final | 5 y 8 |

El análisis crítico de los límites del enfoque no se formula como objetivo separado: atraviesa todos los capítulos y se reúne en el capítulo 11. El anexo C relaciona estos objetivos con los del primer avance.

## 2.5 Hipótesis

Las tres hipótesis se formulan sobre resultados observables en la tarea T3. Intervienen cinco sistemas (M0–M4), un control (M3-sin-orden) y una variante (M4-RRF), descritos en el capítulo 7 (sección 7.4): M0 es una búsqueda léxica BM25 sobre el texto de la ficha; M1, una medida de color y textura; M2, el codificador visión-lenguaje OpenCLIP congelado; M3, el descriptor estructural; M4, la fusión tardía de M0, M2 y M3; M3-sin-orden, el mismo descriptor con la palabra de bandas reducida al histograma de sus tipos, y M4-RRF, una fusión de los mismos componentes por posiciones, sin pesos.

**H1 (primaria).** La fusión enriquecida recupera mejor que el codificador visión-lenguaje congelado: la diferencia media por consulta de nDCG@10 entre M4 y M2 es distinta de cero en la prueba de permutación (p < 0,05) y la diferencia observada es igual o superior a 0,03.

**H2 (mecanismo).** El orden importa: el descriptor con secuencia de bandas y adyacencias (M3) obtiene mejor nDCG@10 que el mismo descriptor reducido al histograma de tipos de banda (M3-sin-orden).

**H3 (fidelidad computacional).** Para cada resultado, la puntuación de M4 es exactamente la suma de las contribuciones de sus componentes, y retirar un componente la modifica como predice la fórmula de fusión.

**Alcance de H1.** M4 añade a M2 dos señales, el texto de la ficha (M0) y la estructura (M3). H1 mide la utilidad del sistema combinado frente a M2 y no aísla el aporte de la estructura: una diferencia favorable podría proceder del texto. El aporte de la estructura se examina en las ablaciones (M4 sin M3, y M4 con M3-sin-orden en lugar de M3) y, para el orden, en H2; las ablaciones son exploratorias.

**Comparaciones confirmatorias.** H1 y H2 son confirmatorias y se contrastan en una secuencia fija. H1 se contrasta primero, con α = 0,05. H2 solo recibe una conclusión confirmatoria si H1 cumple su regla completa; en caso contrario se informa como exploratoria. La secuencia controla la tasa de error por familia, y la exigencia de una diferencia de al menos 0,03 la hace más conservadora. Como H1 se sostuvo, H2 se contrastó de forma confirmatoria (capítulo 8). Las demás comparaciones (frente a M0 y M1, las ablaciones, el control negativo, el análisis por museo y la tarea T1) son exploratorias.

**Cuadro 2.2.** Correspondencia entre hipótesis y prueba.

| | Variable de resultado | Comparación | Unidad de análisis | Prueba y regla de decisión | Veredictos posibles |
|---|---|---|---|---|---|
| H1 | nDCG@10 en T3 | M4 − M2, pareada por consulta | 30 consultas de prueba | Permutación pareada bilateral con 100 000 réplicas fijas y error de Monte Carlo, α = 0,05; intervalo de confianza del 95 % por bootstrap pareado. Se sostiene si p < 0,05 y Δ ≥ 0,03 | Se sostiene; mejora distinta de cero por debajo del umbral práctico; inferior al sistema de referencia; dirección favorable sin evidencia suficiente; no se detectó una mejora |
| H2 | nDCG@10 en T3 | M3 − M3-sin-orden, con las mismas consultas y candidatos | 30 consultas de prueba; las 9 cuya pieza tiene palabra de bandas se describen aparte | La misma regla, con la p exacta por enumeración de los cambios de signo, y solo si H1 se sostiene | Los de H1, o exploratoria si H1 no se sostiene |
| H3 | Error de reconstrucción y efecto de retirar un componente | Puntuación frente a la suma de contribuciones | Cada uno de los diez primeros resultados de M4 en las consultas de prueba | Error ≤ 10⁻⁹ en todos los resultados; intervención conforme a la fórmula. La revisión humana de 10 explicaciones es descriptiva y no interviene | Se sostiene; no se sostiene |

Dos precisiones, fijadas antes de ejecutar ninguna consulta de prueba, condicionan la lectura de las hipótesis. Cuando la pieza de consulta no tiene palabra de bandas, porque no las tiene o porque no pueden observarse, M3 y su control asignan la misma puntuación a todos los candidatos y la diferencia de H2 es cero por construcción, como ocurre en la mayoría de las consultas de prueba (capítulo 5, sección 5.13). Por eso se describe aparte la misma comparación en las 9 consultas con palabra de bandas, las únicas en que puede ser distinta de cero; ese subgrupo es descriptivo y no puede confirmar H2. La segunda precisión concierne a la potencia: con 30 consultas, el estudio solo podía detectar con probabilidad razonable diferencias bastante mayores que el umbral práctico de 0,03 (capítulo 7, sección 7.8), de modo que un resultado no significativo se lee como «no se detectó una mejora» y no como ausencia de efecto.

**H3 como afirmación sobre el algoritmo.** H3 se refiere a la fidelidad de la explicación, entendida como la correspondencia entre la explicación y lo que el sistema calcula, y no a su plausibilidad, es decir, a que resulte convincente para una persona (Jacovi y Goldberg, 2020). M4 es un modelo aditivo que produce su propia explicación, en el sentido que defiende Rudin (2019). Que la contribución estructural a un ranking sea exacta no dice nada sobre el significado cultural de las bandas.

## 2.6 Contribución

La contribución se define por el método y por la evidencia, no por el número de técnicas empleadas.

1. **Una formalización de la macroestructura observable** de un textil a partir de su fotografía: una palabra de bandas sobre un alfabeto finito, considerada igual a su reverso, sus adyacencias, un conjunto de atributos de región y una máscara que distingue lo ausente de lo que no pudo observarse. Se sitúa en una escala distinta de la estructura de hilos de Helmer y Ngo (2015) y Ngo et al. (2021), y no adopta la clasificación por grupos de simetría, que Frame (2006a) considera inadecuada para parte de los patrones andinos.
2. **Un descriptor y una disimilitud** definidos sobre esa formalización, con propiedades demostradas o verificadas por pruebas automatizadas, y un control sin orden que permite atribuir una eventual diferencia a la secuencia de las bandas y no a su composición por tipos.
3. **Una evaluación controlada** de su utilidad en un corpus museográfico: partición por grupos de piezas relacionadas, consultas fijadas antes de ejecutar los sistemas, juicios humanos graduados y ciegos, una sola ejecución de la evaluación final y un control negativo.

Estas contribuciones no dependían del signo del resultado: el diseño permitía afirmar que la estructura anotada no añade utilidad apreciable a un codificador general con la misma solidez que lo contrario.

## 2.7 Alcance de las conclusiones

**Población.** Los resultados se refieren a la colección digital elegible del corpus principal: piezas de tres museos estadounidenses (MET, CMA y AIC), con imagen de dominio público o con licencia CC0, seleccionadas con el criterio de aptitud del capítulo 4. El experimento se realizó sobre un núcleo de 150 piezas anotadas. La población no es «los textiles andinos»: está determinada por lo que esos museos adquirieron, fotografiaron y publicaron, por las condiciones de conservación que favorecen a la costa desértica (Desrosiers, 2024, pp. 2–3) y por un criterio que privilegia piezas cuyos colores y figuras se distinguen a primera vista.

**Comparabilidad de los sistemas.** M3 y M4 son sistemas asistidos por anotación: disponen de etiquetas asignadas por una persona. M2 opera solo sobre los píxeles. La mejora de M4 respalda la utilidad del conocimiento estructural aportado por la anotación humana. No respalda que ese conocimiento pueda extraerse automáticamente de la imagen, ni que un método de extracción sea superior a otro. Tampoco mide el costo de la anotación, que no se registró, ni demuestra que esté disponible a escala.

**Lo que la tesis no afirma.**

- No interpreta el significado de los motivos ni atribuye cultura, función o cronología.
- No sostiene que la palabra de bandas describa cómo se concibió el diseño. Es una codificación elegida por el investigador a partir de lo visible en una fotografía.
- No mide la estructura técnica del tejido (ligamento, dirección de la urdimbre, número de hilos).
- No generaliza a piezas de otras colecciones, a otras condiciones fotográficas ni a otras tradiciones textiles.
- No presenta la fidelidad de H3 como explicación causal o cultural.

**Alcance de piloto.** Con 30 consultas de prueba y un único evaluador, el estudio tiene alcance de piloto. La regla de decisión distingue entre una diferencia positiva no significativa, que se lee como «dirección favorable sin evidencia suficiente», y una diferencia nula o negativa no significativa, que se lee como «no se detectó una mejora»; ninguna de las dos es una confirmación ni una refutación (capítulo 7, sección 7.7). Con potencia limitada, una diferencia significativa puede estar sobrestimada, sin que ello implique que lo esté.

**Gobernanza del corpus.** Las imágenes se usan bajo licencia CC0 o de dominio público. Ese permiso legal no responde por sí solo a las preguntas que plantean los principios CARE sobre datos de origen indígena (Carroll et al., 2020): parte de los textiles andinos conservados en museos procede de contextos funerarios, y ninguna comunidad de origen participó en su descripción. La tesis lo reconoce como límite y documenta el corpus con la estructura de las fichas de conjunto de datos (Gebru et al., 2021; capítulo 4, sección 4.12).

## Referencias

Brownlow, R., Capuzzi, S., Helmer, S., Martins, L., Normann, I., & Poulovassilis, A. (2015). An ontological approach to creating an Andean weaving knowledge base. *ACM Journal on Computing and Cultural Heritage*. https://doi.org/10.1145/2700427

Carroll, S. R., Garba, I., Figueroa-Rodríguez, O. L., Holbrook, J., Lovett, R., Materechera, S., Parsons, M., Raseroka, K., Rodriguez-Lonebear, D., Rowe, R., Sara, R., Walker, J. D., Anderson, J., & Hudson, M. (2020). The CARE principles for Indigenous data governance. *Data Science Journal, 19*, 43, 1–12. https://doi.org/10.5334/dsj-2020-043

Desrosiers, S. (2013). El textil como matriz para el desarrollo de las artes plásticas en los Andes. *Revista Española de Antropología Americana, 43*(2), 477–514. https://doi.org/10.5209/rev_REAA.2013.v43.n2.44020

Desrosiers, S. (2024). Creación textil en los Andes: el lenguaje de los hilos y su transmisión a través del tiempo. En *Arte y saber del textil* (pp. 1–27). Banco de Crédito del Perú.

Dorozynski, M., & Rottensteiner, F. (2022). Deep descriptor learning with auxiliary classification loss for retrieving images of silk fabrics in the context of preserving European silk heritage. *ISPRS International Journal of Geo-Information, 11*(2), 82. https://doi.org/10.3390/ijgi11020082

Frame, M. (2006a). *Elemental pathways in fiber structures: Approaching Andean symmetry patterns through an ancient technology* [Ponencia]. Textile Society of America 10th Biennial Symposium, Toronto. https://digitalcommons.unl.edu/cgi/viewcontent.cgi?article=1347&context=tsaconf

Gebru, T., Morgenstern, J., Vecchione, B., Wortman Vaughan, J., Wallach, H., Daumé III, H., & Crawford, K. (2021). *Datasheets for datasets* (arXiv:1803.09010v8). arXiv. https://arxiv.org/abs/1803.09010

Helmer, S., & Ngo, V. M. (2015). A similarity measure for weaving patterns in textiles. En *Proceedings of the 38th International ACM SIGIR Conference on Research and Development in Information Retrieval* (pp. 163–172). https://doi.org/10.1145/2766462.2767735

Jacovi, A., & Goldberg, Y. (2020). *Towards faithfully interpretable NLP systems: How should we define and evaluate faithfulness?* (arXiv:2004.03685). arXiv. https://arxiv.org/abs/2004.03685

Ngo, V. M., Helmer, S., Le-Khac, N.-A., & Kechadi, M.-T. (2021). Structural textile pattern recognition and processing based on hypergraphs. *Information Retrieval Journal, 24*, 137–173. https://doi.org/10.1007/s10791-020-09384-y

Rei, L., Mladenić, D., Dorozynski, M., Rottensteiner, F., Schleider, T., Troncy, R., Sebastián Lozano, J., & Gaitán Salvatella, M. (2023). Multimodal metadata assignment for cultural heritage artifacts. *Multimedia Systems, 29*, 847–869. https://doi.org/10.1007/s00530-022-01025-2

Rudin, C. (2019). *Stop explaining black box machine learning models for high stakes decisions and use interpretable models instead* (arXiv:1811.10154v3). arXiv. https://arxiv.org/abs/1811.10154

Thrush, T., Jiang, R., Bartolo, M., Singh, A., Williams, A., Kiela, D., & Ross, C. (2022). *Winoground: Probing vision and language models for visio-linguistic compositionality* (arXiv:2204.03162). arXiv. https://arxiv.org/abs/2204.03162

Ypsilantis, N.-A., Garcia, N., Han, G., Ibrahimi, S., van Noord, N., & Tolias, G. (2021). The Met dataset: Instance-level recognition for artworks. En *Thirty-fifth Conference on Neural Information Processing Systems (NeurIPS 2021), Track on Datasets and Benchmarks*. https://arxiv.org/abs/2202.01747

Yuksekgonul, M., Bianchi, F., Kalluri, P., Jurafsky, D., & Zou, J. (2023). When and why vision-language models behave like bags-of-words, and what to do about it? En *International Conference on Learning Representations (ICLR 2023)*. https://arxiv.org/abs/2210.01936
