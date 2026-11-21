# 1. Introducción

> **Borrador 0.1, 21 de noviembre de 2026.** Capítulo de la segunda parte de la tesis. Sustituye a la introducción del primer avance, que no se corrige. Se redactó antes de ejecutar la prueba; la sección 1.5 y el resumen se completarán con los resultados del capítulo 8.

## 1.1 Contexto

Los textiles andinos prehispánicos se cuentan entre los objetos mejor conservados y más estudiados del patrimonio americano. En ellos convergen decisiones sobre la fibra, la técnica, el color, el motivo y la organización de la superficie, y una parte de esas decisiones se tomaba antes de tejer: en los tejidos de faz de urdimbre, el urdido fija qué colores puede tener cada banda (Desrosiers, 2013, pp. 480 y 482). La disposición de bandas, paneles, retículas y campos centrales es, por eso, un rasgo que quienes estudian estas piezas usan para compararlas, y que una fotografía de museo permite ver.

Buena parte de estas piezas se encuentra hoy en museos fuera del Perú, y varias de esas instituciones publican sus fotografías con licencias abiertas. El acceso computacional a ellas se hace por dos vías: la ficha curatorial, con un vocabulario que cambia de un museo a otro y que a menudo carece de descripción, y la imagen, que los modelos visión-lenguaje preentrenados convierten en una representación general. Ninguna de las dos registra de forma explícita cómo está organizada la superficie del textil, y la evidencia disponible indica que esos modelos tienden a tratar el contenido de una imagen como un conjunto de elementos sin orden (Yuksekgonul et al., 2023; Thrush et al., 2022).

## 1.2 Problema y pregunta

La tesis aborda un problema de representación y de evidencia: cómo formalizar la organización visible de un textil de modo que pueda compararse entre piezas, y cómo comprobar, con un diseño que no favorezca al método propuesto, si esa representación aporta algo que las señales textuales y visuales generales no aportan ya. La pregunta que orienta el trabajo es la siguiente:

> En un conjunto congelado de textiles andinos fotografiados por museos, ¿añadir el orden de las bandas y las relaciones entre regiones, mediante un descriptor estructural derivado de anotación humana, mejora la recuperación por similitud estructural respecto de las señales textuales y visuales generales, según juicios humanos independientes de los sistemas? ¿Permite, además, explicar el ranking de forma fiel?

El capítulo 2 desarrolla el problema, las preguntas específicas, los objetivos y las tres hipótesis que la responden.

## 1.3 Enfoque

El enfoque descansa en cuatro decisiones.

**Representar no es descifrar.** La tesis no busca traducir el significado cultural de los textiles ni sustituir la interpretación arqueológica, antropológica o comunitaria. Representa lo que una persona puede registrar al mirar la fotografía de una pieza y compara piezas por esa representación.

**La macroestructura observable como objeto.** El objeto formal no es el tejido ni su técnica, sino la organización visible de la superficie: la composición general, la secuencia de tipos de banda, la presencia de borde y de centro, la simetría, la repetición y los motivos. La secuencia de bandas se representa como una palabra sobre un alfabeto de cinco tipos, considerada igual a su reverso, y la anotación distingue lo que está ausente de lo que la fotografía no permite observar (capítulos 4 y 5).

**Sistemas separados y fusión de puntuaciones.** Cada modalidad tiene su propio sistema: una búsqueda léxica sobre la ficha (M0), una medida de color y textura (M1), un codificador visión-lenguaje congelado (M2) y un descriptor estructural sobre la anotación (M3), con un control que conserva los tipos de banda y descarta su orden. Las puntuaciones de M0, M2 y M3 se combinan en una fusión aditiva (M4), cuya puntuación se descompone exactamente en las contribuciones de sus componentes.

**Evaluación controlada con juicios humanos.** La utilidad de la estructura se mide en una tarea de recuperación por ejemplar, con consultas sorteadas antes de ejecutar los sistemas, una partición por grupos de piezas relacionadas, juicios de relevancia graduados emitidos a ciegas sobre las imágenes, un protocolo fijado antes de la prueba y una única ejecución de esta (capítulo 7).

## 1.4 Continuidad con el primer avance

Esta tesis se presenta en dos partes. El primer avance, de julio de 2026, estableció los fundamentos conceptuales, propuso una formalización combinatoria preliminar, documentó un corpus de 288 registros del Metropolitan Museum of Art (MET) y del Cleveland Museum of Art (CMA), y planteó un plan experimental. Ese documento no se corrige: su corpus se conserva congelado y se regenera idéntico, y las diferencias con la segunda parte se documentan en cada capítulo.

La segunda parte respondió a la evaluación del asesor de octubre y noviembre de 2026, que señaló cuatro carencias: el corpus no distinguía la pieza de su ficha ni de su fotografía; el criterio para incluir una imagen no era verificable; la formalización mezclaba objetos de tipos distintos y enunciaba como ecuaciones afirmaciones empíricas; y el plan experimental no fijaba qué resultado sostendría o refutaría las hipótesis. En respuesta, la segunda parte:

- amplía el corpus con una tercera fuente, el Art Institute of Chicago (AIC), y lo cura con un criterio de aptitud que se comprueba en la fotografía;
- separa registro, imagen y grupo de piezas relacionadas, y usa el grupo como unidad de partición;
- anota la macroestructura de un núcleo de 150 piezas con estados de observación y mide la estabilidad de la anotación;
- sustituye la formalización del primer avance por una más acotada, con propiedades demostradas y verificadas por pruebas automáticas;
- convierte el plan experimental en un protocolo con hipótesis contrastables, reglas de decisión, controles y criterios de suspensión, fijado antes de la prueba.

El cambio de mayor alcance es de orientación. El primer avance preguntaba cómo construir una representación multimodal rica; la segunda parte pregunta si la parte estructural de esa representación aporta algo que pueda medirse, y acepta como resultado válido que no aporte.

## 1.5 Contribuciones

La tesis aporta una formalización de la macroestructura visible de los textiles a partir de fotografías de museo, con un descriptor y una disimilitud de propiedades demostradas y un control que aísla el efecto del orden; un corpus multimodal documentado de tres colecciones abiertas, con una anotación estructural congelada y su estabilidad medida; y una evaluación controlada de la utilidad de esa estructura frente a un codificador visión-lenguaje congelado. Estas contribuciones no dependen del signo del resultado (capítulo 2, sección 2.6). [Pendiente: síntesis de los resultados del capítulo 8.]

## 1.6 Organización del documento

El documento se organiza en once capítulos.

- **Capítulo 2. Problema, objetivos e hipótesis.** Plantea el problema, concilia la formulación del primer avance con la de la segunda parte y define las hipótesis H1, H2 y H3 con su regla de decisión.
- **Capítulo 3. Estado del arte.** Revisa la literatura sobre la organización del textil andino y su análisis de simetría, la representación computacional de textiles, la recuperación en colecciones patrimoniales, los límites de los modelos visión-lenguaje, la fusión de señales, la interpretabilidad y la evaluación con juicios humanos, y formula la brecha. Integra el marco teórico del textil andino que el primer avance presentaba en un capítulo propio.
- **Capítulo 4. Datos y anotación.** Describe las fuentes, el criterio de aptitud, la composición del corpus, las unidades de registro, imagen y grupo, el esquema de anotación, su estabilidad y la versión congelada.
- **Capítulo 5. Formalización de la macroestructura observable.** Define la palabra de bandas, su forma canónica, las distancias por bloque, la disimilitud mixta y la fusión, y demuestra sus propiedades.
- **Capítulo 6. Implementación.** Describe el flujo reproducible, los sistemas, la evaluación y su verificación.
- **Capítulo 7. Diseño experimental.** Presenta el protocolo: galería, particiones, consultas, juicios, métricas, inferencia, potencia, ablaciones, controles y amenazas a la validez.
- **Capítulo 8. Resultados.** Informa los resultados de prueba de H1, H2 y H3, las ablaciones y los análisis exploratorios.
- **Capítulo 9. Discusión.** Interpreta los resultados a la luz de la literatura y de las amenazas a la validez.
- **Capítulo 10. Conclusiones.** Responde a la pregunta de investigación y a los objetivos.
- **Capítulo 11. Limitaciones y trabajo futuro.** Reúne las limitaciones del estudio y las líneas que se desprenden de ellas.

## Referencias

Desrosiers, S. (2013). El textil como matriz para el desarrollo de las artes plásticas en los Andes. *Revista Española de Antropología Americana, 43*(2), 477–514. https://doi.org/10.5209/rev_REAA.2013.v43.n2.44020

Thrush, T., Jiang, R., Bartolo, M., Singh, A., Williams, A., Kiela, D., & Ross, C. (2022). *Winoground: Probing vision and language models for visio-linguistic compositionality* (arXiv:2204.03162). arXiv. https://arxiv.org/abs/2204.03162 [verificar: sede]

Yuksekgonul, M., Bianchi, F., Kalluri, P., Jurafsky, D., & Zou, J. (2023). When and why vision-language models behave like bags-of-words, and what to do about it? En *International Conference on Learning Representations (ICLR 2023)*. https://arxiv.org/abs/2210.01936
