# 2. Problema, objetivos e hipótesis

> **Borrador 0.2, 23 de noviembre de 2026** (alcance de H1, regla secuencial y H3 según el dictamen del asesor del 21 de noviembre; protocolo 0.6.6). Capítulo de la segunda parte de la tesis. Integra el capítulo 2 del primer avance, que no se corrige, con la formulación contrastable que exigió la evaluación del asesor. La sección 2.2 registra qué se conserva del primer avance, qué se precisa y qué se aplaza. Las marcas **[verificar: …]** señalan afirmaciones que dependen de una obra no leída en el proyecto.

## 2.1 Planteamiento del problema

Una parte considerable del diseño textil andino prehispánico se organiza en unidades que se repiten y se ordenan sobre la superficie: listas y franjas, paneles, retículas, cenefas y campos centrales. Esa organización no es un ornamento añadido a posteriori. En los tejidos de faz de urdimbre, las bandas con diseño resultan del contraste entre hilos que se urden juntos, y el urdido fija qué colores puede tener cada banda antes de empezar a tejer (Desrosiers, 2013, pp. 480 y 482). La disposición de las bandas es, en esos casos, una decisión previa al tejido. Al mismo tiempo, esa organización es visible en una fotografía de museo y constituye, para quien estudia las piezas, un criterio habitual de comparación: dos tejidos pueden parecerse por la disposición de sus bandas aunque difieran en color, en iconografía o en estado de conservación.

Las colecciones digitales de los museos ofrecen dos vías de acceso a estas piezas, y ninguna recoge esa organización de forma explícita. La primera es la ficha curatorial, que describe material, técnica, cultura atribuida y fecha con un vocabulario que varía entre instituciones. En el corpus de esta tesis, la descripción curatorial existe en 29 de 155 registros del Metropolitan Museum of Art, en 53 de 108 del Cleveland Museum of Art y en 43 de 352 del Art Institute of Chicago (capítulo 4, sección 4.2.2). La segunda vía es la imagen, que los codificadores visión-lenguaje preentrenados convierten en una representación general. La evidencia disponible indica que estos codificadores tratan el contenido de forma cercana a una bolsa de elementos: en pruebas diseñadas para ello, CLIP acierta el 56 % de las relaciones espaciales entre objetos, con el azar en 50 % (Yuksekgonul et al., 2023, p. 4), y queda por debajo del azar cuando dos imágenes solo difieren en la disposición de los mismos elementos (Thrush et al., 2022, p. 6). Esa evidencia procede de la correspondencia entre texto e imagen en fotografías naturales y no demuestra que ocurra lo mismo al comparar un textil con otro. Motiva la pregunta; no la responde.

La recuperación de textiles por su estructura tiene antecedentes, pero a otra escala. Helmer y Ngo (2015) y Ngo et al. (2021) recuperan tejidos por la estructura de sus cruces de hilos, modelada a mano para cada pieza, y los evalúan contra categorías de tejido. Brownlow et al. (2015) registran en una ontología técnicas y estructuras examinadas por especialistas y las consultan por coincidencia exacta de atributos. En los trabajos de recuperación patrimonial revisados, la pertinencia de un resultado se toma de la identidad de la pieza, de la coincidencia de metadatos o de la pertenencia a una categoría (Ypsilantis et al., 2021; Rei et al., 2023; Dorozynski y Rottensteiner, 2022), y en ningún caso de un juicio humano graduado sobre la organización visible del diseño (capítulo 3, sección 3.5). En la búsqueda realizada, de alcance parcial, no se encontró un estudio que evalúe con juicios humanos graduados y ciegos si la secuencia de bandas visible en fotografías de museo añade utilidad de recuperación a un codificador visión-lenguaje congelado. El trabajo de Phillips (2018) sobre patrones de franjas de color en textiles de faz de urdimbre es el antecedente con más probabilidad de acercarse y no pudo consultarse [localizado, no leído]; por ello la ausencia de antecedentes se afirma solo respecto de lo recuperado (capítulo 3, sección 3.9).

El problema que aborda la tesis es, en consecuencia, de representación y de evidencia. De representación, porque es preciso formalizar la organización visible de un textil de modo que pueda compararse entre piezas, registrando lo que la fotografía muestra y distinguiendo lo ausente de lo que no puede observarse. De evidencia, porque es preciso comprobar, con un diseño que no favorezca al método propuesto, si esa representación aporta algo que las señales textuales y visuales generales no aportan ya.

## 2.2 Del primer avance a una pregunta contrastable

El primer avance formuló el problema como la construcción de una representación computacional multimodal de textiles andinos que integrara información visual, atributos estructurales, descripciones textuales y contexto cultural, y que permitiera tareas de similitud, recuperación y agrupamiento sin reducir el textil a una imagen ni asumir un desciframiento cultural. Esa formulación sigue vigente como orientación general de la tesis, y dos de sus principios se mantienen sin cambios: representar no es descifrar, y la representación computacional no sustituye la interpretación arqueológica, antropológica o comunitaria.

Como pregunta de investigación, sin embargo, la formulación del primer avance no fijaba un criterio de éxito. No precisaba con qué se compararía la representación propuesta, en qué tarea, con qué medida ni quién decidiría qué resultado es pertinente. La evaluación del asesor de octubre de 2026 lo señaló al observar que las hipótesis del capítulo 5 del primer avance (ecuaciones 5.69 a 5.71) enunciaban como relaciones matemáticas lo que son afirmaciones empíricas, sin operacionalizarlas. La segunda parte de la tesis conserva el problema y estrecha la pregunta: elige una tarea, una medida, un árbitro y una comparación principal, la del sistema combinado con el codificador visual que contiene, acompañada de ablaciones que examinan qué parte de la diferencia corresponde a la estructura. El Cuadro 2.1 resume la correspondencia.

**Cuadro 2.1.** Correspondencia entre la formulación del primer avance y la de la segunda parte.

| Primer avance | Segunda parte | Motivo del cambio |
|---|---|---|
| Pregunta general: representación multimodal para similitud, recuperación y agrupamiento | Pregunta sobre recuperación por similitud estructural, con comparación, medida y árbitro fijados (sección 2.3) | Sin criterio de éxito la pregunta no es contrastable |
| PE1. Atributos relevantes para describir los textiles | PE1 y OE2: esquema de anotación de la macroestructura visible, con estados de observación (capítulo 4) | Se acota a lo que la fotografía permite registrar |
| PE2. El textil como configuración en un espacio combinatorio de atributos | PE2 y OE3: palabra de bandas, descriptor estructural y disimilitud (capítulo 5) | El espacio de configuraciones no intervenía en ningún cálculo y se retiró (sección 5.16) |
| PE3. Integrar imagen, ficha, atributos y contexto en una representación conjunta | Fusión tardía de puntuaciones de sistemas separados (M4) | Los espacios de representación no están alineados, y la fusión aditiva permite verificar la explicación (sección 5.10) |
| PE4. Mejora frente a imagen sola o texto solo, en recuperación, similitud y agrupamiento | PE3 y H1: M4 frente a M2; comparaciones exploratorias frente a M0 y M1 | El agrupamiento se aplaza: carece de un criterio externo de validez en este corpus |
| PE5. Limitaciones del uso de modelos preentrenados | Amenazas a la validez (capítulo 7) y limitaciones (capítulo 11) | Se tratan como condiciones del diseño y no como pregunta |
| Hipótesis de trabajo (ecuaciones 2.1 y 2.2) | H1, H2 y H3, con regla de decisión (sección 2.5) | Una hipótesis contrastable debe indicar qué resultado la sostiene y cuál no |

Dos tareas del plan experimental preliminar quedan fuera del estudio. La recuperación imagen-texto en sentido inverso, de la imagen a la descripción, no responde a la pregunta sobre la organización visible. El agrupamiento exploratorio, evaluado con índices de cohesión interna como el de Silhouette, mide la organización del espacio de representación y no su pertinencia para quien compara piezas; sin una partición de referencia validada, sus resultados no podrían sostener ni refutar ninguna hipótesis. La recuperación de texto a imagen se conserva como tarea secundaria y exploratoria (T1, capítulo 7).

## 2.3 Preguntas de investigación

**Pregunta general.**

> En un conjunto congelado de textiles andinos fotografiados por museos, ¿añadir el orden de las bandas y las relaciones entre regiones, mediante un descriptor estructural derivado de anotación humana, mejora la recuperación por similitud estructural respecto de las señales textuales y visuales generales, según juicios humanos independientes de los sistemas? ¿Permite, además, explicar el ranking de forma fiel?

La pregunta es contrastable porque fija los términos de la comparación: los sistemas que se comparan, la tarea (recuperación por ejemplar, T3), la medida (nDCG@10 por consulta) y el árbitro (juicios humanos ciegos en una escala de cuatro grados).

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

**Cuadro 2.2.** Objetivos específicos, productos verificables y correspondencia con el primer avance.

| | Objetivo | Producto verificable | Capítulo | Objetivo del primer avance |
|---|---|---|---|---|
| OE1 | Construir y documentar un corpus multimodal de textiles andinos procedentes de colecciones abiertas, con criterios de selección explícitos y con agrupación de las piezas relacionadas | Corpus v2.0 con grupos, licencias y sumas de verificación | 4 | OE3 |
| OE2 | Formalizar la macroestructura observable y anotarla con un protocolo que registre lo que no puede observarse, midiendo la estabilidad de la anotación | Esquema de anotación, anotación congelada v2.1 e informe de estabilidad | 4 | OE1 |
| OE3 | Definir un descriptor estructural y una disimilitud entre piezas, con sus propiedades demostradas o verificadas, y un control que aísle el efecto del orden | Formalización, implementación de M3 y M3-sin-orden, y pruebas de propiedades | 5 y 6 | OE2 |
| OE4 | Evaluar, con un protocolo fijado de antemano y juicios humanos ciegos, la utilidad del descriptor solo y en fusión con texto e imagen, frente a un codificador visión-lenguaje congelado | Resultados por consulta, con intervalos, ablaciones y control negativo | 7 y 8 | OE4 y OE5 |
| OE5 | Comprobar que la puntuación del sistema combinado se descompone exactamente en las contribuciones de sus componentes | Reconstrucción e intervención sobre los resultados de prueba | 5 y 8 | OE5 (interpretabilidad) |

El sexto objetivo del primer avance, analizar críticamente los límites del enfoque, no se formula como objetivo separado: atraviesa todos los capítulos y se reúne en el capítulo 11.

## 2.5 Hipótesis

Las tres hipótesis se formulan sobre resultados observables en la tarea T3. Para cada una se indica qué resultado la sostendría y cuál no. Los sistemas se describen en el capítulo 7: M0 es una búsqueda léxica BM25 sobre el texto de la ficha; M1, una medida de color y textura; M2, el codificador visión-lenguaje OpenCLIP congelado; M3, el descriptor estructural; M3-sin-orden, el mismo descriptor con la palabra de bandas reducida al histograma de sus tipos; y M4, la fusión tardía de M0, M2 y M3.

**H1 (primaria).** La fusión enriquecida recupera mejor que el codificador visión-lenguaje congelado: la diferencia media por consulta de nDCG@10 entre M4 y M2 es distinta de cero en la prueba de permutación y la diferencia observada es igual o superior a 0,03.

**H2 (mecanismo).** El orden importa: el descriptor con secuencia de bandas y adyacencias (M3) obtiene mejor nDCG@10 que el mismo descriptor reducido al histograma de tipos de banda (M3-sin-orden).

**H3 (fidelidad computacional).** Para cada resultado, la puntuación de M4 es exactamente la suma de las contribuciones de sus componentes, y retirar un componente la modifica como predice la fórmula de fusión.

**Alcance de H1.** M4 añade a M2 dos señales, el texto de la ficha (M0) y la estructura (M3). H1 mide la utilidad del sistema combinado frente a M2 y no aísla el aporte de la estructura: una diferencia favorable podría proceder del texto. El aporte de la estructura se examina en las ablaciones (M4 sin M3, y M4 con M3-sin-orden en lugar de M3) y, para el orden, en H2; las ablaciones son exploratorias.

**Comparaciones confirmatorias.** H1 y H2 son confirmatorias y se contrastan en una secuencia fija. H1 se contrasta primero, con α = 0,05. H2 solo recibe una conclusión confirmatoria si H1 cumple su regla completa; en caso contrario se informa como exploratoria, con su estimación, su intervalo y su p. El control de la tasa de error por familia depende de rechazar la hipótesis nula de H1, y la exigencia de una diferencia de al menos 0,03 lo hace más conservador. Con la potencia disponible, la secuencia hace improbable una conclusión confirmatoria sobre H2. Las demás comparaciones (frente a M0 y M1, las ablaciones, el control negativo, el análisis por museo y la tarea T1) son exploratorias y se presentan como tales.

**Cuadro 2.3.** Correspondencia entre hipótesis y prueba.

| | Variable de resultado | Comparación | Unidad de análisis | Prueba y regla de decisión | Veredictos posibles |
|---|---|---|---|---|---|
| H1 | nDCG@10 en T3 | M4 − M2, pareada por consulta | 30 consultas de prueba | Permutación pareada bilateral con 100 000 réplicas fijas y error de Monte Carlo, α = 0,05; intervalo de confianza del 95 % por bootstrap pareado. Se sostiene si p < 0,05 y Δ ≥ 0,03 | Se sostiene; mejora distinta de cero por debajo del umbral práctico; inferior al sistema de referencia; dirección favorable sin evidencia suficiente; no se detectó una mejora |
| H2 | nDCG@10 en T3 | M3 − M3-sin-orden, con las mismas consultas y candidatos | 30 consultas de prueba; las 9 cuya pieza tiene palabra de bandas se describen aparte | La misma regla, con la p exacta por enumeración de los cambios de signo, y solo si H1 se sostiene | Los de H1, o exploratoria si H1 no se sostiene |
| H3 | Error de reconstrucción y efecto de retirar un componente | Puntuación frente a la suma de contribuciones | Cada resultado del top 10 de M4 en prueba | Error ≤ 10⁻⁹ en todos los resultados; intervención conforme a la fórmula. La revisión humana de 10 explicaciones es descriptiva y no interviene | Se sostiene; no se sostiene |

Dos precisiones condicionan la lectura de H2 y de H1, y ambas se fijaron antes de ejecutar ninguna consulta de prueba. La primera concierne a H2. Cuando la pieza de consulta no tiene palabra de bandas, porque no las tiene o porque no pueden observarse, M3 y su control asignan la misma puntuación a todos los candidatos, y la diferencia pareada es cero por construcción (capítulo 5, sección 5.13). En las consultas de prueba ocurre en 21 de 30. Por eso, junto a la regla de H2 sobre las 30 consultas, se describe la misma comparación restringida a las 9 consultas con palabra de bandas, donde la diferencia puede ser distinta de cero. Son dos magnitudes distintas, la utilidad media sobre las 30 consultas y la utilidad condicionada a que haya bandas, y el subgrupo no puede confirmar H2. Con a lo sumo nueve diferencias distintas de cero, la p de H2 se calcula de forma exacta, y si menos de seis son distintas de cero no puede bajar de 0,05. La segunda concierne a la potencia. Con la variabilidad observada en las consultas de desarrollo, el efecto mínimo detectable con 30 consultas y potencia del 80 % es de 0,087 en H1, con un rango de 0,060 a 0,159. Es una estimación aproximada de planificación, hecha con diez consultas, y no una frontera: no garantiza que un efecto mayor se detecte ni impide que uno menor resulte significativo. Detectar el umbral práctico de 0,03 exigiría unas 250 consultas (capítulo 7, sección 7.8). Un resultado no significativo se informará, por tanto, como «no se detectó una mejora», y no como ausencia de efecto.

**H3 como afirmación sobre el algoritmo.** H3 se refiere a la fidelidad de la explicación, entendida como la correspondencia entre la explicación y lo que el sistema calcula, y no a su plausibilidad, es decir, a que resulte convincente para una persona (Jacovi y Goldberg, 2020). M4 es un modelo aditivo que produce su propia explicación, en el sentido que defiende Rudin (2019). Que la contribución estructural a un ranking sea exacta no dice nada sobre el significado cultural de las bandas ni sobre las razones por las que quien tejió la pieza las dispuso así. Esa interpretación queda fuera de la tesis.

**Relación con la hipótesis de trabajo del primer avance.** El primer avance representaba cada textil como una tupla multimodal

$$x_i = (x_{v,i},\, x_{s,i},\, x_{t,i},\, x_{c,i}), \tag{2.1}$$

con información visual, estructural, textual y contextual, y proponía aprender una representación conjunta $z_i = f(x_{v,i}, x_{s,i}, x_{t,i}, x_{c,i})$ (ecuación 2.2 del primer avance). La segunda parte conserva la tupla (2.1) como descripción de las modalidades disponibles y precisa el papel de cada una: la imagen $x_{v,i}$ alimenta a M1 y M2; la anotación estructural $x_{s,i}$, a M3; el texto de la ficha $x_{t,i}$, a M0. El contexto $x_{c,i}$ (museo, cultura atribuida, fecha) no se usa como señal de similitud, porque la atribución cultural es heterogénea entre museos y falta en 94 registros, y porque un sistema que la usara recuperaría por atribución y no por organización visible; se usa para estratificar las particiones y para el análisis por museo. La representación conjunta aprendida se sustituye por una fusión tardía de puntuaciones,

$$s(q, i) = \sum_{c \in C(q,i)} \alpha'_c\, \hat{s}_c(q, i), \tag{2.2}$$

definida en el capítulo 5 (ecuación 5.21). La sustitución responde a tres razones: no hay datos supervisados para aprender $f$ con 150 piezas anotadas; los espacios de representación de cada sistema no están alineados, de modo que sumar sus vectores carece de sentido; y la forma aditiva es la que permite contrastar H3.

## 2.6 Contribución

La contribución se define por el método y por la evidencia, no por el número de técnicas empleadas.

1. **Una formalización de la macroestructura observable** de un textil a partir de su fotografía: una palabra de bandas sobre un alfabeto finito, considerada salvo reversión, sus adyacencias, un conjunto de atributos de región y una máscara que distingue lo ausente de lo que no pudo observarse. Se sitúa en una escala distinta de la estructura de hilos de Helmer y Ngo (2015) y Ngo et al. (2021), y no adopta la clasificación por grupos de simetría, que Frame (2006a) considera inadecuada para parte de los patrones andinos.
2. **Un descriptor y una disimilitud** definidos sobre esa formalización, con propiedades demostradas o verificadas por pruebas automáticas, y un control sin orden que permite atribuir una eventual diferencia a la secuencia de las bandas y no a su composición por tipos.
3. **Una evaluación controlada** de su utilidad en un corpus museográfico: partición por grupos de piezas relacionadas, consultas fijadas antes de ejecutar los sistemas, juicios humanos graduados y ciegos, una sola ejecución de prueba y un control negativo.

Estas contribuciones no dependen del signo del resultado. Si H1 o H2 no se sostienen, la tesis aporta una medición controlada de que, en este corpus y con este descriptor, la estructura anotada no añade utilidad apreciable a un codificador general. Existe un precedente andino en ese sentido: en khipus, Contreras (2026), en una prepublicación sin arbitraje, no halló que el orden de los tipos de nudo mejorara la clasificación de procedencia frente a rasgos agregados.

## 2.7 Alcance de las conclusiones

**Población.** Los resultados se refieren a la colección digital elegible del corpus principal v2: piezas de tres museos estadounidenses (MET, CMA y AIC), con imagen de dominio público o con licencia CC0, seleccionadas con el criterio de aptitud del capítulo 4. El experimento se realiza sobre un núcleo de 150 piezas anotadas. La población no es «los textiles andinos»: está determinada por lo que esos museos adquirieron, fotografiaron y publicaron, por las condiciones de conservación que favorecen a la costa desértica (Desrosiers, 2024, pp. 2–3) y por un criterio que privilegia piezas cuyos colores y figuras se distinguen a primera vista.

**Comparabilidad de los sistemas.** M3 y M4 son sistemas asistidos por anotación: disponen de etiquetas asignadas por una persona. M2 opera solo sobre los píxeles. Una mejora de M4 respaldaría la utilidad del conocimiento estructural aportado por la anotación humana. No respaldaría que ese conocimiento pueda extraerse automáticamente de la imagen, ni que un método de extracción sea superior a otro. Tampoco mide el costo de la anotación, que no se registró, ni demuestra que esté disponible a escala.

**Lo que la tesis no afirma.**

- No interpreta el significado de los motivos ni atribuye cultura, función o cronología.
- No sostiene que la palabra de bandas describa cómo se concibió el diseño. Es una codificación elegida por el investigador a partir de lo visible en una fotografía.
- No mide la estructura técnica del tejido (ligamento, dirección de la urdimbre, número de hilos).
- No generaliza a piezas de otras colecciones, a otras condiciones fotográficas ni a otras tradiciones textiles.
- No presenta la fidelidad de H3 como explicación causal o cultural.

**Resultado negativo o inconcluso.** La pregunta y los objetivos se mantienen cualquiera que sea el resultado. Con 30 consultas de prueba, el estudio tiene alcance de piloto. Una diferencia positiva no significativa se informará como «dirección favorable sin evidencia suficiente», con su intervalo, y no como confirmación ni como refutación. Con potencia limitada, una diferencia que resulte significativa puede estar sobrestimada, sin que ello implique que lo esté.

**Gobernanza del corpus.** Las imágenes se usan bajo licencia CC0 o de dominio público. Ese permiso legal no responde por sí solo a las preguntas que plantean los principios CARE sobre datos de origen indígena (Carroll et al., 2020): parte de los textiles andinos conservados en museos procede de contextos funerarios, y ninguna comunidad de origen participó en su descripción. La tesis lo declara como límite y documenta el corpus con la estructura de las fichas de conjunto de datos (Gebru et al., 2021; capítulo 4, sección 4.12).

## 2.8 Cierre del capítulo

El capítulo conserva el problema del primer avance, la representación computacional de textiles andinos sin reducirlos a imágenes ni atribuirles significados, y lo convierte en una pregunta que el experimento puede responder. La multimodalidad se mantiene, pero se materializa en sistemas separados cuyas puntuaciones se combinan. La utilidad del sistema combinado se mide frente al codificador visual (H1); el aporte de la estructura se examina en las ablaciones, de carácter exploratorio, y el del orden frente a su control sin orden (H2). La fidelidad computacional de la descomposición (H3) se trata como una propiedad verificable del algoritmo, que no equivale a una validación de la explicación por especialistas. Los capítulos 4 y 5 responden a las preguntas de diseño; el capítulo 7 fija cómo se contrastan las hipótesis.

## Referencias

Brownlow, R., Capuzzi, S., Helmer, S., Martins, L., Normann, I., & Poulovassilis, A. (2015). An ontological approach to creating an Andean weaving knowledge base. *ACM Journal on Computing and Cultural Heritage*. https://doi.org/10.1145/2700427 [verificar: volumen, número y artículo]

Carroll, S. R., Garba, I., Figueroa-Rodríguez, O. L., Holbrook, J., Lovett, R., Materechera, S., Parsons, M., Raseroka, K., Rodriguez-Lonebear, D., Rowe, R., Sara, R., Walker, J. D., Anderson, J., & Hudson, M. (2020). The CARE principles for Indigenous data governance. *Data Science Journal, 19*, 43, 1–12. https://doi.org/10.5334/dsj-2020-043

Contreras, M. (2026). *Structural pattern mining in Inka khipus: Unsupervised clustering, provenance classification, and a computational validation of the Santa Valley match* (arXiv:2607.00185) [Prepublicación]. arXiv. https://arxiv.org/abs/2607.00185

Desrosiers, S. (2013). El textil como matriz para el desarrollo de las artes plásticas en los Andes. *Revista Española de Antropología Americana, 43*(2), 477–514. https://doi.org/10.5209/rev_REAA.2013.v43.n2.44020

Desrosiers, S. (2024). Creación textil en los Andes: el lenguaje de los hilos y su transmisión a través del tiempo. En *Arte y saber del textil* (pp. 1–27). Banco de Crédito del Perú. [verificar: editores e ISBN]

Dorozynski, M., & Rottensteiner, F. (2022). Deep descriptor learning with auxiliary classification loss for retrieving images of silk fabrics in the context of preserving European silk heritage. *ISPRS International Journal of Geo-Information, 11*(2), 82. https://doi.org/10.3390/ijgi11020082

Frame, M. (2006a). *Elemental pathways in fiber structures: Approaching Andean symmetry patterns through an ancient technology* [Ponencia]. Textile Society of America 10th Biennial Symposium, Toronto. https://digitalcommons.unl.edu/cgi/viewcontent.cgi?article=1347&context=tsaconf [verificar: número y páginas de las actas]

Gebru, T., Morgenstern, J., Vecchione, B., Wortman Vaughan, J., Wallach, H., Daumé III, H., & Crawford, K. (2021). *Datasheets for datasets* (arXiv:1803.09010v8). arXiv. https://arxiv.org/abs/1803.09010

Helmer, S., & Ngo, V. M. (2015). A similarity measure for weaving patterns in textiles. En *Proceedings of the 38th International ACM SIGIR Conference on Research and Development in Information Retrieval* (pp. 163–172). https://doi.org/10.1145/2766462.2767735

Jacovi, A., & Goldberg, Y. (2020). *Towards faithfully interpretable NLP systems: How should we define and evaluate faithfulness?* (arXiv:2004.03685). arXiv. https://arxiv.org/abs/2004.03685 [verificar: sede]

Ngo, V. M., Helmer, S., Le-Khac, N.-A., & Kechadi, M.-T. (2021). Structural textile pattern recognition and processing based on hypergraphs. *Information Retrieval Journal, 24*, 137–173. https://doi.org/10.1007/s10791-020-09384-y

Rei, L., Mladenić, D., Dorozynski, M., Rottensteiner, F., Schleider, T., Troncy, R., Sebastián Lozano, J., & Gaitán Salvatella, M. (2023). Multimodal metadata assignment for cultural heritage artifacts. *Multimedia Systems, 29*, 847–869. https://doi.org/10.1007/s00530-022-01025-2

Rudin, C. (2019). *Stop explaining black box machine learning models for high stakes decisions and use interpretable models instead* (arXiv:1811.10154v3). arXiv. https://arxiv.org/abs/1811.10154 [verificar: sede]

Thrush, T., Jiang, R., Bartolo, M., Singh, A., Williams, A., Kiela, D., & Ross, C. (2022). *Winoground: Probing vision and language models for visio-linguistic compositionality* (arXiv:2204.03162). arXiv. https://arxiv.org/abs/2204.03162 [verificar: sede]

Ypsilantis, N.-A., Garcia, N., Han, G., Ibrahimi, S., van Noord, N., & Tolias, G. (2021). The Met dataset: Instance-level recognition for artworks. En *Thirty-fifth Conference on Neural Information Processing Systems (NeurIPS 2021), Track on Datasets and Benchmarks*. https://arxiv.org/abs/2202.01747

Yuksekgonul, M., Bianchi, F., Kalluri, P., Jurafsky, D., & Zou, J. (2023). When and why vision-language models behave like bags-of-words, and what to do about it? En *International Conference on Learning Representations (ICLR 2023)*. https://arxiv.org/abs/2210.01936

**Obra mencionada y no consultada en el proyecto:**

Phillips, A. (2018). Colored strip patterns and front-back symmetry in warp-faced pre-Columbian textiles. *Leonardo*. https://doi.org/10.1162/leon_a_01691 [localizado, no leído]
