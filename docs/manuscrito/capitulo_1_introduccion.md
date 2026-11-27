# 1. Introducción

## 1.1 Contexto

Los textiles andinos prehispánicos se cuentan entre los objetos mejor conservados y más estudiados del patrimonio americano. En ellos convergen decisiones sobre la fibra, la técnica, el color, el motivo y la organización de la superficie, y una parte de esas decisiones se tomaba antes de tejer. En los tejidos de faz de urdimbre, aquellos en que los hilos longitudinales (la urdimbre) cubren la superficie y forman el diseño, la disposición de esos hilos antes de empezar a tejer fija qué colores puede tener cada banda [@desrosiers2013, pp. 480 y 482] (capítulo 3, sección 3.2). La disposición de bandas, paneles, retículas y campos centrales es, por eso, un rasgo que quienes estudian estas piezas usan para compararlas, y que una fotografía de museo permite ver.

Muchas de estas piezas están hoy en museos fuera del Perú que publican sus fotografías con licencias abiertas. El acceso computacional a ellas tiene dos vías: la ficha curatorial, con un vocabulario que cambia de un museo a otro y que a menudo carece de descripción, y la imagen, que los modelos visión-lenguaje preentrenados convierten en una representación general. Ninguna de las dos registra de forma explícita cómo está organizada la superficie del textil, y la evidencia disponible indica que esos modelos tienden a tratar el contenido de una imagen como un conjunto de elementos sin orden [@yuksekgonul2023; @thrush2022].

## 1.2 Problema y pregunta

La tesis aborda un problema de representación y de evidencia: cómo formalizar la organización visible de un textil de modo que pueda compararse entre piezas, y cómo comprobar, con un diseño que no favorezca al método propuesto, si esa representación aporta algo que las señales textuales y visuales generales no aportan ya. La pregunta que orienta el trabajo es la siguiente:

> En un conjunto congelado de textiles andinos fotografiados por museos, ¿añadir el orden de las bandas y las relaciones entre regiones, mediante un descriptor estructural derivado de anotación humana, mejora la recuperación por similitud estructural respecto de las señales textuales y visuales generales, según juicios humanos independientes de los sistemas? ¿Permite, además, explicar el *ranking* de forma fiel?

El capítulo 2 desarrolla el problema, las preguntas específicas, los objetivos y las tres hipótesis que la responden.

## 1.3 Enfoque

El enfoque descansa en cuatro decisiones.

**Representar no es descifrar.** La tesis no traduce el significado cultural de los textiles ni sustituye la interpretación arqueológica, antropológica o comunitaria: representa lo que una persona puede registrar al mirar la fotografía de una pieza.

**La macroestructura observable como objeto.** El objeto formal no es el tejido ni su técnica, sino la organización visible de la superficie: la composición general, la secuencia de tipos de banda, la presencia de un borde decorado (una franja ornamental que enmarca la pieza) y de un campo central, la simetría, la repetición y los motivos. La secuencia de bandas se representa como una palabra sobre un alfabeto de cinco tipos, considerada igual a su reverso, y la anotación distingue lo que está ausente de lo que la fotografía no permite observar (capítulos 4 y 5).

**Sistemas separados y fusión de puntuaciones.** Cada modalidad tiene su propio sistema: una búsqueda léxica sobre la ficha (M0), una medida de color y textura (M1), un codificador visión-lenguaje congelado (M2) y un descriptor estructural sobre la anotación (M3), acompañado de un control que conserva los tipos de banda y descarta su orden y sus adyacencias (M3-sin-orden). Las puntuaciones de M0, M2 y M3 se combinan en una fusión aditiva (M4), cuya puntuación se descompone exactamente en las contribuciones de sus componentes.

**Evaluación controlada con juicios humanos.** La tarea es la recuperación por ejemplar: dada una pieza, ordenar las demás por la semejanza de su organización. La hipótesis principal compara la fusión con el codificador visión-lenguaje solo; la parte de la diferencia que corresponde a la estructura se examina con ablaciones, y el aporte del orden, frente a su control. Las consultas se sortearon antes de ejecutar los sistemas, la relevancia la decidieron juicios graduados emitidos a ciegas, y la evaluación final se ejecutó una sola vez, conforme a un protocolo fijado de antemano (capítulo 7).

## 1.4 Continuidad con el primer avance

El primer avance de la tesis, de julio de 2026, estableció los fundamentos conceptuales, propuso una formalización combinatoria preliminar, documentó un corpus de 288 registros del Metropolitan Museum of Art (MET) y del Cleveland Museum of Art (CMA) y planteó un plan experimental. Ese documento no se corrige, y su corpus se conserva congelado.

La revisión del primer avance identificó cuatro carencias: el corpus no distinguía la pieza de su ficha ni de su fotografía; el criterio para incluir una imagen no era verificable; la formalización mezclaba objetos de tipos distintos y enunciaba como ecuaciones afirmaciones empíricas; y el plan experimental no fijaba qué resultado sostendría o refutaría las hipótesis. En respuesta, la segunda parte:

- amplió el corpus con una tercera fuente, el Art Institute of Chicago (AIC), y lo curó con un criterio de aptitud que se comprueba en la fotografía;
- separó registro, imagen y grupo de piezas relacionadas, y usó el grupo como unidad de partición;
- anotó la macroestructura de un núcleo de 150 piezas con estados de observación y midió la estabilidad de la anotación;
- sustituyó la formalización del primer avance por una más acotada, con propiedades demostradas y verificadas por pruebas automatizadas;
- convirtió el plan experimental en un protocolo con hipótesis contrastables, reglas de decisión, controles y criterios de suspensión, fijado antes de la evaluación final.

El cambio de mayor alcance es de orientación. El primer avance preguntaba cómo construir una representación multimodal rica; la segunda parte pregunta si la parte estructural de esa representación aporta algo que pueda medirse, y acepta como resultado válido que no se detecte una mejora. El anexo C reúne la correspondencia detallada entre ambas partes.

## 1.5 Contribuciones y resultados

La tesis aporta una formalización de la macroestructura visible de los textiles a partir de fotografías de museo, con un descriptor y una disimilitud de propiedades demostradas y un control sin orden basado en el inventario de los tipos de banda; un corpus multimodal documentado de tres colecciones abiertas, con una anotación estructural congelada y su estabilidad medida; y una evaluación controlada de un sistema que combina esa estructura con el texto y la imagen frente a un codificador visión-lenguaje congelado (capítulo 2, sección 2.6).

En la evaluación final, con los juicios de un único evaluador que también anotó las piezas, la fusión superó al codificador visual solo en nDCG@10, una medida de la calidad del orden de los diez primeros resultados: 0,604 frente a 0,492, con una diferencia de 0,112 (intervalo de confianza del 95 %: 0,062 a 0,164; p = 0,00015), de modo que la hipótesis principal se sostuvo; en una ablación exploratoria, al retirar la estructura de la fusión, el resultado bajó a 0,523. No se detectó una mejora atribuible al orden de las bandas respecto de su inventario de tipos, y la puntuación combinada se descompuso sin error en sus contribuciones en los 300 resultados comprobados. Los capítulos 8 y 9 presentan y discuten estos resultados, y el capítulo 10 formula las conclusiones.

## 1.6 Organización del documento

El documento se organiza en once capítulos y tres anexos. El capítulo 2 plantea el problema, las preguntas, los objetivos y las hipótesis H1, H2 y H3 con su regla de decisión. El capítulo 3 revisa la literatura sobre el textil andino, la recuperación patrimonial, los modelos visión-lenguaje, la fusión de señales, la interpretabilidad y la evaluación con juicios humanos, y formula la brecha. El capítulo 4 describe las fuentes, el criterio de aptitud, el corpus, el esquema de anotación y su estabilidad. El capítulo 5 formaliza la macroestructura observable y demuestra las propiedades del descriptor, la disimilitud y la fusión. El capítulo 6 describe la implementación y su verificación, y el capítulo 7, el protocolo experimental. El capítulo 8 informa los resultados; el 9 los discute; el 10 responde a la pregunta y a los objetivos, y el 11 reúne las limitaciones y el trabajo futuro. El anexo A documenta la implementación y la reproducibilidad; el anexo B, la custodia de la evaluación final y la trazabilidad de las decisiones, y el anexo C, la correspondencia con el primer avance.
