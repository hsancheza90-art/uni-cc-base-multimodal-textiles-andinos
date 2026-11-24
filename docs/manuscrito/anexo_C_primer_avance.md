# Anexo C. Correspondencia con el primer avance

El primer avance de la tesis no se corrige. Este anexo documenta cómo se relacionan con él la formulación del problema y la formalización de la segunda parte, para que el lector pueda seguir cada cambio sin que el cuerpo de la tesis tenga que hacerlo.

## C.1 Problema, hipótesis de trabajo y tareas

### C.1.1 Del problema del primer avance a una pregunta contrastable

El primer avance formuló el problema como la construcción de una representación computacional multimodal de textiles andinos que integrara información visual, atributos estructurales, descripciones textuales y contexto cultural, y que permitiera tareas de similitud, recuperación y agrupamiento. Como orientación general, esa formulación sigue vigente. Como pregunta de investigación, no fijaba un criterio de éxito: no precisaba con qué se compararía la representación propuesta, en qué tarea, con qué medida ni quién decidiría qué resultado es pertinente. Las hipótesis de su capítulo 5 (ecuaciones 5.69 a 5.71) enunciaban además como relaciones matemáticas lo que son afirmaciones empíricas. La segunda parte conservó el problema y estrechó la pregunta. El Cuadro C.1 resume la correspondencia entre ambas formulaciones, y el Cuadro C.2, la de los objetivos.

**Cuadro C.1.** Correspondencia entre la formulación del primer avance y la de la segunda parte.

| Primer avance | Segunda parte | Motivo del cambio |
|---|---|---|
| Pregunta general: representación multimodal para similitud, recuperación y agrupamiento | Pregunta sobre recuperación por similitud estructural, con comparación, medida y árbitro fijados (capítulo 2, sección 2.3) | Sin criterio de éxito, la pregunta no es contrastable |
| PE1. Atributos relevantes para describir los textiles | PE1 y OE2: esquema de anotación de la macroestructura visible, con estados de observación (capítulo 4) | Se acota a lo que la fotografía permite registrar |
| PE2. El textil como configuración en un espacio combinatorio de atributos | PE2 y OE3: palabra de bandas, descriptor estructural y disimilitud (capítulo 5) | El espacio de configuraciones no intervenía en ningún cálculo y se retiró (véase en este anexo la correspondencia de las ecuaciones del capítulo 5) |
| PE3. Integrar imagen, ficha, atributos y contexto en una representación conjunta | Fusión tardía de las puntuaciones de sistemas separados (M4) | Los espacios de representación no están alineados, y la fusión aditiva permite verificar la explicación (capítulo 5, sección 5.10) |
| PE4. Mejora frente a imagen sola o texto solo, en recuperación, similitud y agrupamiento | PE3 y H1: M4 frente a M2; comparaciones exploratorias frente a M0 y M1 | El agrupamiento queda fuera: carece de un criterio externo de validez en este corpus |
| PE5. Limitaciones del uso de modelos preentrenados | Amenazas a la validez (capítulo 7) y limitaciones (capítulo 11) | Se tratan como condiciones del diseño y no como pregunta |
| Hipótesis de trabajo (ecuaciones 2.1 y 2.2) | H1, H2 y H3, con regla de decisión (capítulo 2, sección 2.5) | Una hipótesis contrastable debe indicar qué resultado la sostiene y cuál no |

**Cuadro C.2.** Correspondencia entre los objetivos específicos de la segunda parte y los del primer avance.

| Segunda parte | Objetivo | Primer avance |
|---|---|---|
| OE1 | Construir y documentar el corpus multimodal, con criterios de selección explícitos y agrupación de las piezas relacionadas | OE3 (diseñar y documentar un corpus multimodal piloto) |
| OE2 | Formalizar y anotar la macroestructura observable, midiendo la estabilidad de la anotación | OE1 (identificar y sistematizar los atributos relevantes) |
| OE3 | Definir el descriptor estructural, la disimilitud y el control sin orden, con sus propiedades | OE2 (formular un modelo combinatorio preliminar) |
| OE4 | Evaluar la utilidad del descriptor, solo y en fusión, con un protocolo fijado de antemano | OE4 (implementar una línea base multimodal) y OE5 (evaluar la representación) |
| OE5 | Comprobar la descomposición exacta de la puntuación del sistema combinado | OE5, en su vertiente de interpretabilidad |

El sexto objetivo del primer avance, analizar críticamente los límites del enfoque, no se formula como objetivo separado en la segunda parte: atraviesa todos los capítulos y se reúne en el capítulo 11.

### C.1.2 Tupla multimodal y fusión tardía

La hipótesis de trabajo del primer avance representaba cada textil como una tupla multimodal

$$x_i = (x_{v,i},\, x_{s,i},\, x_{t,i},\, x_{c,i}), \tag{C.1}$$

con información visual ($x_{v,i}$), estructural ($x_{s,i}$), textual ($x_{t,i}$) y contextual ($x_{c,i}$), y proponía aprender a partir de ella una representación conjunta

$$z_i = f(x_{v,i},\, x_{s,i},\, x_{t,i},\, x_{c,i}) \tag{C.2}$$

que permitiera comparar textiles, recuperar objetos relevantes y explorar agrupamientos (ecuaciones 2.1 y 2.2 del primer avance).

La segunda parte conserva la tupla (C.1) como descripción de las modalidades disponibles y precisa el papel de cada una. La imagen $x_{v,i}$ alimenta a M1 y M2; la anotación estructural $x_{s,i}$, a M3; el texto de la ficha $x_{t,i}$, a M0. El contexto $x_{c,i}$ (museo, cultura atribuida, fecha) no se usa como señal de similitud, por dos motivos: la atribución cultural es heterogénea entre museos y falta en 94 registros, todos del Art Institute of Chicago (capítulo 4, sección 4.2.2); y un sistema que la usara recuperaría por atribución y no por organización visible. El contexto se usa para estratificar las particiones y para el análisis por museo.

La representación conjunta aprendida (C.2) se sustituye por una fusión tardía de puntuaciones,

$$s(q, i) = \sum_{c \in C(q,i)} \alpha'_c\, \hat{s}_c(q, i), \tag{C.3}$$

donde $\hat{s}_c(q, i)$ es la puntuación del componente $c$ normalizada en la consulta $q$, $C(q, i)$ el conjunto de componentes con evidencia para el par y $\alpha'_c$ los pesos renormalizados sobre ese conjunto; la definición completa es la ecuación 5.21 del capítulo 5. La sustitución responde a tres razones. Primera, no hay datos supervisados para aprender $f$ con 150 piezas anotadas. Segunda, los espacios de representación de cada sistema no están alineados, de modo que sumar sus vectores carece de sentido. Tercera, la forma aditiva es la que permite contrastar H3, porque la puntuación se descompone exactamente en las contribuciones de sus componentes.

### C.1.3 Tareas del plan experimental preliminar

El plan experimental del primer avance proponía cuatro tareas para la línea base multimodal. El Cuadro C.3 indica qué ocurrió con cada una. Las tareas que se conservan mantienen su número: por eso el experimento solo tiene las tareas T1 y T3.

**Cuadro C.3.** Destino de las tareas del plan experimental preliminar.

| Tarea del primer avance | Destino en la segunda parte | Motivo |
|---|---|---|
| 1. Recuperación de texto a imagen | Se conserva como T1, secundaria y exploratoria, con seis consultas redactadas por el evaluador | Permite consultar con una descripción en lenguaje natural; sus resultados se informan de forma descriptiva (capítulo 7, sección 7.3) |
| 2. Recuperación de imagen a texto | Retirada | Recuperar descripciones o etiquetas a partir de una imagen no responde a la pregunta sobre la organización visible |
| 3. Recuperación de imagen a imagen | Se conserva como T3, tarea primaria, redefinida como recuperación por ejemplar según la similitud de la organización visible, con juicios humanos graduados y ciegos | Es la tarea sobre la que se formulan y contrastan las hipótesis |
| 4. Agrupamiento exploratorio | Retirada | Los índices de cohesión interna, como el de Silhouette, miden la organización del espacio de representación y no su pertinencia para quien compara piezas; sin una partición de referencia validada, sus resultados no podrían sostener ni refutar ninguna hipótesis |

## C.2 Formalización: correspondencia ecuación por ecuación

El capítulo 5 de la segunda parte sustituye al capítulo 5 del primer avance (ecuaciones 5.1 a 5.78). El Cuadro C.4 indica qué ocurre con cada grupo de ecuaciones de aquel capítulo y por qué. Las ecuaciones del primer avance se citan con su número original; las secciones, definiciones y ecuaciones de destino son las del capítulo 5 de esta tesis.

**Cuadro C.4.** Destino de las ecuaciones del capítulo 5 del primer avance.

| Ecuaciones del primer avance | Contenido | Destino en la segunda parte | Motivo |
|---|---|---|---|
| 5.1–5.3 | Imagen como matriz simbólica | Reemplazadas por las unidades de la sección 5.3 | Imagen y patrón eran objetos distintos sin aplicación definida entre ellos; el descriptor no se extrae de los píxeles |
| 5.4–5.7 | Alfabeto con color, forma, orientación, rol y técnica | Reemplazadas por el alfabeto $\Sigma$ (ecuación 5.4) y por los bloques del descriptor | Atributos de escalas y observabilidad distintas en un solo símbolo; la técnica no se asigna por celda |
| 5.8–5.20 | Espacio de configuraciones: 9600 símbolos, $20^{100}$ patrones | Retiradas | Aritmética correcta, pero no son datos observados ni intervienen en el método |
| 5.21–5.23 | $\Omega_{obs} \subseteq \Omega_{plaus}$ | Retiradas | La inclusión de una muestra finita no prueba regularidad cultural |
| 5.24–5.30 | Restricciones | Reemplazadas por la separación entre elegibilidad y estructura (sección 5.3) | Inconsistencia de tipos; exigían bandas y simetría a toda pieza (sección C.3) |
| 5.31–5.34 | Motivos y diccionario | Reemplazadas por el bloque de motivos (sección 5.8.4) | Un diccionario por pieza impedía comparar |
| 5.35–5.39 | Bandas y periodo $p^{*}$ | Bandas: sección 5.5. Periodo: retirado | El descriptor usa la repetición como atributo ordinal anotado |
| 5.40–5.43 | Matriz de adyacencia y conteo $\mathbf{1}^{\top}A^{n-1}\mathbf{1}$ | Reemplazadas por el histograma de adyacencias (sección 5.8.2) | «No observado» no equivale a «prohibido» |
| 5.44–5.46 | Grupo $G$ genérico | Reemplazadas por $C_2$ (sección 5.6) | Acción no definida; varias transformaciones no conservan el dominio |
| 5.47–5.49 | Burnside y Pólya | Conservadas como resultados conocidos, con una instancia concreta (sección 5.7) | Faltaba una instancia útil; no son prueba de rendimiento |
| 5.50–5.52 | Grafos | Retiradas; trabajo futuro | Fuera del alcance; requieren relaciones tipadas y anotación adicional |
| 5.53–5.57 | Vector de conteos, índice de complejidad, entropía | Retiradas | El índice no tenía interpretación justificada; la entropía de un histograma no mide orden |
| 5.58–5.60 | Similitud coseno y mezcla | Reemplazadas por la disimilitud $D$ (sección 5.9) | Sin máscara ni escalas comunes; la mezcla no es métrica |
| 5.61–5.65 | Codificadores e interfaces | Pasan al capítulo de implementación | Son interfaces, no formalización |
| 5.66 | Suma de vectores | Retirada | Sin alineación entre espacios (sección C.3) |
| 5.67–5.68 | Fusión de puntuaciones | Reemplazadas por las ecuaciones 5.20 y 5.21 | Faltaban la normalización y el caso sin evidencia |
| 5.69–5.71 | «Hipótesis» como ecuaciones | Reemplazadas por H1 a H3 (sección 5.12) | Son afirmaciones empíricas |
| 5.72–5.73, 5.78 | Diagramas de flujo | Retirados | $\Omega_{obs}$ es una colección, no una transformación de una pieza |
| 5.74–5.77 | Ejemplo con vectores | Reemplazado por el ejemplo 5.1 y los ejemplos de la sección 5.8 | Los ceros confundían ausente con no observado |

## C.3 Notas sobre los cambios principales

**Restricciones (ecuaciones 5.24–5.30).** El primer avance escribía como funciones del patrón restricciones que en realidad recaían sobre la pieza, la imagen y los metadatos, y exigía bandas y simetría a toda pieza. Era una inconsistencia de tipos: una condición sobre la calidad de la fotografía o sobre la ficha no puede ser una propiedad del patrón. La segunda parte separa las dos cosas. Los criterios de calidad fotográfica y de curación son una función de la fotografía y de la ficha, $E(r, f(r))$, que define la población de la galería y no forma parte del descriptor; dentro de la galería no se presupone que una pieza tenga bandas, motivos o simetría observables, y cada atributo admite los estados de ausencia y no observación (capítulo 5, secciones 5.3 y 5.4).

**Suma de vectores (ecuación 5.66).** El primer avance sumaba un vector visual y un vector combinatorio para obtener una representación conjunta. La suma exige que ambos vectores tengan la misma dimensión y vivan en un espacio compatible, y ninguna de las dos condiciones se cumple: el vector de OpenCLIP y el descriptor estructural no están alineados. La segunda parte mantiene cada sistema en su propio espacio y combina sus puntuaciones normalizadas por consulta mediante una fusión tardía (capítulo 5, sección 5.10), que además permite descomponer la puntuación y contrastar la fidelidad de la explicación (H3).

**Matriz de adyacencia (ecuaciones 5.40–5.43).** La matriz $A \in \{0,1\}^{k \times k}$ de combinaciones «permitidas» y el conteo $\mathbf{1}^{\top} A^{n-1} \mathbf{1}$ identificaban «no observado» con «no permitido», lo que no puede sostenerse con un corpus finito, y no intervenían en el método. El histograma de adyacencias (capítulo 5, definición 5.14) describe qué vecindades se observan en cada pieza, sin prescribir cuáles son admisibles.

**Grupo de transformaciones (ecuaciones 5.44–5.46).** El primer avance proponía un grupo $G$ genérico con reflexiones, rotaciones, traslaciones y simetrías de friso, sin definir su acción sobre las secuencias. La segunda parte fija el grupo $C_2 = \{e, \rho\}$ de la reversión y su acción sobre las palabras, y justifica por qué no incluye otras transformaciones (capítulo 5, definición 5.11).

**Periodo fundamental (ecuaciones 5.35–5.39).** El periodo $p^{*}$ se retira del capítulo y de la implementación porque el descriptor no lo usa: la repetición se registra como atributo ordinal anotado. Calcular un periodo sobre la palabra de bandas queda como extensión.

**Similitud coseno (ecuaciones 5.58–5.60).** La similitud coseno sobre un vector de conteos mezclaba escalas sin máscara de observabilidad. La disimilitud mixta $D$ (capítulo 5, ecuación 5.18) compara cada bloque en su escala, excluye los bloques no comparables y declara qué propiedades no cumple (proposición 5.8).

**Hipótesis (ecuaciones 5.69–5.71).** El primer avance enunciaba como relaciones matemáticas afirmaciones empíricas, por ejemplo que la similitud híbrida «mejora» a la multimodal. La segunda parte las formula como hipótesis sobre resultados observables, con su prueba y su regla de decisión (capítulo 2, sección 2.5; capítulo 5, sección 5.12).

**Ejemplo con vectores (ecuaciones 5.74–5.77).** El ejemplo codificaba «sin bandas» y «sin periodo» con ceros, sin distinguir la ausencia observada de la falta de observación. En la segunda parte, una pieza sin bandas se anota `ausente` y su palabra es la palabra vacía, mientras que una pieza cuyas bandas no pueden distinguirse se anota `no_observable` y el bloque no participa en la comparación (capítulo 5, sección 5.4).

**Vocabulario.** Los valores de varios atributos (composición, simetría, repetición, borde, centro, motivos) conservan las categorías de los cuadros 6.3 a 6.8 del primer avance, en particular del Cuadro 6.4. Por eso la ausencia observada no se codifica igual en todos los atributos (`ausente`, `no` o `no_evidente`), y el Cuadro 5.2 fija la correspondencia.
