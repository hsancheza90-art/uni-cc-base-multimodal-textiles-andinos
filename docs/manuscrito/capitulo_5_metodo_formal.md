# 5. Formalización de la macroestructura observable

## 5.1 Propósito y alcance

Este capítulo define qué se compara cuando el método dice que dos textiles «se parecen por su estructura». El objeto formal no es el textil ni su tejido, sino su **macroestructura observable**: la organización de la superficie que una persona puede registrar al mirar la fotografía publicada por un museo (composición, secuencia de bandas, borde decorado, centro, simetría, repetición y motivos). Las secciones 5.3 a 5.5 fijan las unidades; las 5.6 a 5.11 definen el descriptor, la disimilitud y la fusión y demuestran sus propiedades; las 5.12 a 5.14 separan lo demostrado de lo que contrastó el experimento.

Los sistemas se describen en el capítulo 7: M3 ordena las piezas por el descriptor estructural, M3-sin-orden es su control sin el orden de las bandas y M4 es la fusión tardía de M0 (búsqueda léxica sobre el texto de la ficha), M2 (el codificador visión-lenguaje OpenCLIP) y M3. La formalización no modela la estructura técnica del tejido (ligamento, cruces de hilos), que es la escala de Helmer y Ngo [@helmer2015] y Ngo et al. [@ngo2021]; no infiere la estructura desde los píxeles, porque el descriptor se calcula sobre una anotación de la que responde una persona, de modo que M3 y M4 son sistemas **asistidos por anotación**; y no atribuye significado cultural a la organización que formaliza.

**Naturaleza de cada enunciado.** Cada enunciado lleva una de cuatro marcas: **[T]**, resultado conocido de la literatura, que no se reclama como aporte; **[D]**, decisión de diseño, que pudo ser otra y se justifica; **[P]**, propiedad demostrada en este capítulo y fijada en una prueba automatizada (anexo A), como las proposiciones 5.1 a 5.9 y el lema 5.1; y **[E]**, afirmación empírica, como las hipótesis H1 a H3, contrastadas en el capítulo 8, o la estabilidad de la anotación, medida en el capítulo 4.

El capítulo sustituye al capítulo 5 del primer avance, que no se corrige. De aquel se conservan, con una instancia concreta, los resultados de enumeración por órbitas; se retiran el espacio de configuraciones, los grafos, el índice de complejidad y la suma de vectores procedentes de espacios distintos; y las restricciones sobre la pieza y las hipótesis escritas como ecuaciones se reemplazan por la separación entre elegibilidad y estructura y por hipótesis contrastables. El anexo C da la correspondencia ecuación por ecuación.

## 5.2 Fundamento en el dominio textil

Las decisiones de diseño de las secciones siguientes responden a rasgos documentados del textil andino, que la sección 3.2 expone, y a los límites de la fuente, que es una fotografía de museo.

**Por qué bandas.** En los tejidos de faz de urdimbre (aquellos en que los hilos longitudinales, la urdimbre, cubren la superficie y forman el diseño), la banda y su paleta quedan fijadas al urdir (disponer los hilos de urdimbre en el telar), antes de tejer [@desrosiers2013] (sección 3.2). En buena parte del material, la franja transversal es, por tanto, una unidad que la propia técnica produce, y no solo una convención de quien describe. La relación no es una regla: en el tapiz la técnica no impone bandas, aunque hay bordados que imitan las bandas tejidas. La definición operativa de banda (sección 5.5) recoge el caso común a todas las técnicas: una franja que atraviesa toda la superficie visible.

**Por qué el orden.** Que la disposición de las bandas sea una decisión previa al tejido, y no un efecto secundario del decorado, hace del orden un candidato natural a rasgo de diseño. Que sea útil para recuperar piezas es otra cuestión: es H2 **[E]**.

**Por qué no una clasificación por grupos de simetría.** La clasificación cristalográfica de los patrones en siete tipos de friso y diecisiete del plano [@crowe2001, pp. 6–9] no es apropiada para todos los patrones andinos, cuya lógica deriva en parte de las estructuras de fibra [@frame2006a]; los diseños de pocas franjas tienen regularidades que ni los frisos ni los patrones del plano recogen [@chavey2015, pp. 85–87]; y la detección automática del grupo exige un patrón periódico fotografiado de frente y sin distorsiones [@liu2004, p. 368]. El descriptor registra la simetría como un atributo nominal anotado (sección 5.8.4), y la única equivalencia formal que impone es la reversión del sentido de lectura (sección 5.6).

**Por qué la reversión.** El sentido en que se lee una secuencia de bandas es una convención del anotador. Un fragmento no tiene extremo privilegiado; una prenda completa puede tenerlo (una túnica con abertura de cuello, un manto con cenefa, una franja decorativa, en un solo extremo), y la formalización lo descarta deliberadamente (sección 5.14).

**Por qué el eje no entra en el descriptor.** El eje registrado es el de la fotografía, no el del telar ni el de uso, y una misma organización puede aparecer horizontal o vertical según la toma (sección 3.2; capítulo 4, sección 4.7.3). La palabra de bandas no depende del eje, pero el atributo `eje_bandas` sí, y por eso queda fuera.

## 5.3 Unidades de análisis

El primer avance trataba como un solo objeto cinco cosas distintas, que aquí se separan.

**Definición 5.1 (unidades).** Las unidades de análisis y los datos que las materializan son las del Cuadro 5.1.

**Cuadro 5.1.** Unidades de análisis.

| Símbolo | Unidad | Definición | Dato que la materializa |
|---|---|---|---|
| $o$ | Objeto | El textil físico conservado en un museo. No se observa directamente | No tiene identificador propio en el corpus |
| $r$ | Registro | La ficha de un museo, con sus metadatos | Fila del consolidado, identificada por la fuente y el número de la ficha |
| $f(r)$ | Fotografía | Copia de evaluación de la fotografía principal del registro, de 1600 px de lado mayor | Archivo identificado por su suma SHA-256 |
| $G$ | Grupo | Clase de equivalencia de registros que muestran un mismo objeto o partes de él | Grupo decidido por el investigador (capítulo 4, sección 4.6) |
| $a(r)$ | Anotación | Lo que una persona registró al observar $f(r)$ | Fila de la anotación congelada v2.1 |

**Definición 5.2 (grupos) [D].** Sea $R$ el conjunto de registros utilizables del corpus v2.0 y $U \subseteq R \times R$ la relación formada por los pares que el investigador decidió unir. Los grupos son las clases de la clausura reflexiva, simétrica y transitiva de $U$; de forma equivalente, las componentes conexas del grafo $(R, U)$.

El grupo es una aproximación al objeto: dos registros de un mismo grupo no se suponen independientes. Por eso el grupo, y no el registro, es la unidad de partición entre desarrollo y prueba.

**Definición 5.3 (galería y candidatos).** La galería $\mathcal{G} \subset R$ es el conjunto de registros con anotación estructural (el núcleo). Para una consulta $q \in \mathcal{G}$, el conjunto de candidatos es

$$\mathcal{C}(q) = \mathcal{G} \setminus G(q), \tag{5.1}$$

donde $G(q)$ es el grupo de $q$. Una pieza, es decir, un registro de la galería, nunca se recupera a sí misma ni a otra vista del mismo objeto.

**Elegibilidad y estructura [D].** La pertenencia de un registro a $\mathcal{G}$ depende de criterios de calidad fotográfica y de curación (capítulo 4, sección 4.4). Esos criterios son una función de la fotografía y de la ficha, $E(r, f(r))$, y **definen la población**; no forman parte del descriptor. Dentro de $\mathcal{G}$ no se presupone que una pieza tenga bandas, motivos o simetría observables: cada atributo admite los estados de la sección siguiente.

## 5.4 Anotación y observabilidad

**Definición 5.4 (espacio de valores).** Sea $A$ el conjunto de atributos estructurales y $V_k$ el vocabulario controlado del atributo $k \in A$ (capítulo 4, sección 4.7). El valor anotado de cada atributo pertenece a una de tres clases disjuntas:

$$\underbrace{P_k}_{\text{presencia}} \;\cup\; \underbrace{Z_k}_{\text{ausencia observada}} \;\cup\; \underbrace{N_k}_{\text{sin observación}}. \tag{5.2}$$

$P_k$ reúne los valores que describen el rasgo; $Z_k$, el valor que registra que el rasgo se buscó y no está; $N_k$, los estados que indican que no pudo observarse o decidirse. Las tres clases no se codifican igual en todos los atributos, porque varios conservan los valores del vocabulario del primer avance. El Cuadro 5.2 fija la correspondencia, que es la que aplican el vocabulario y el código.

**Cuadro 5.2.** Codificación de presencia, ausencia observada y falta de observación por atributo.

| Atributo | Presencia $P_k$ | Ausencia observada $Z_k$ | Sin observación $N_k$ |
|---|---|---|---|
| `composicion` | Los seis tipos de composición | No aplica: toda pieza observada tiene alguna (`composicion_libre` si no se distingue organización) | `no_observable`, `desconocido` |
| `eje_bandas` | `horizontal`, `vertical` | `ausente` | `no_observable`, `desconocido` |
| `secuencia_bandas` | Una palabra (sección 5.5) | `ausente` | `no_observable`, `desconocido` |
| `borde`, `centro` | `si` | `no` | `no_visible`, `desconocido` |
| `simetria` | `bilateral`, `radial`, `traslacional`, `repeticion_modular` | `no_evidente` | `no_observable`, `desconocido` |
| `repeticion` | `si`, `parcial` | `no` | `no_observable`, `desconocido` |
| `motivos` | Un conjunto no vacío de clases de motivo | `ausente` | `no_observable`, `desconocido` |
| `familia_iconografica` | Las familias del vocabulario, incluida la residual `no_determinada` | `ausente` | `no_observable`, `desconocido` |

Un estado ocupa la celda completa y no puede combinarse con valores. La categoría residual `no_determinada` (en `familia_iconografica` y como tipo de banda) no es un estado: indica que el rasgo se ve y no corresponde a ninguna categoría del vocabulario, y se compara como un valor más **[D]**, de modo que dos rasgos `no_determinada` coinciden en el descriptor aunque solo compartan no encajar en el vocabulario. Su uso es marginal (sección 5.4.1).

**Ausente no es no observado [D].** Un valor de $Z_k$ es una **observación**, el rasgo podía verse y no está, y se compara como cualquier otro valor. Los estados de $N_k$ indican **falta de observación** y no se comparan. Así, una pieza sin bandas se anota `ausente` (su palabra es la palabra vacía, sección 5.5), mientras que una pieza cuyas bandas no pueden distinguirse se anota `no_observable` (el bloque no participa).

**Definición 5.5 (máscara).** Para cada bloque $b$ del descriptor (sección 5.8) y cada registro $r$,

$$m_b(r) = \begin{cases} 1 & \text{si el valor anotado no pertenece a } N_k,\\ 0 & \text{en caso contrario.} \end{cases} \tag{5.3}$$

Una celda vacía también apaga el bloque; la condición B8 de la sección 5.4.1 excluye ese caso de una versión congelada.

**La máscara es un juicio, no un dato fijo [E].** En la re-anotación ciega del lote 1, la frontera entre «se observa» y «no se observa» cambió en 6 de 30 piezas para la composición y en 6 de 30 para la simetría (capítulo 4, sección 4.9.2). La máscara es, por tanto, una fuente de variabilidad del descriptor, que la formalización no elimina y que se trata entre las amenazas a la validez.

### 5.4.1 Condiciones de buena formación de la anotación

Las definiciones de este capítulo presuponen diez condiciones sobre la anotación; si alguna falla, el descriptor sigue calculándose, pero deja de significar lo que aquí se dice. La validación de cada fila impone dos: todo valor pertenece al vocabulario de su atributo o es un estado admitido que ocupa la celda completa (B1), y el eje y la secuencia de bandas registran ambos bandas o ambos un estado (B2). La congelación y cada regeneración comprueban otras cinco sobre la anotación final: si eje y secuencia son estados, son el mismo (B3); una palabra contiene al menos un símbolo de $\Sigma$ (B4), pues de lo contrario $\tilde{w} = \varepsilon$ y «no se ve ninguna banda» se compararía como «no tiene bandas»; no hay dos lagunas contiguas (B5), de modo que los tramos de la definición 5.10 son únicos; si la composición es `bandas`, la secuencia no es `ausente` (B6); y `motivos` es `ausente` si y solo si `familia_iconografica` lo es (B7). Las tres restantes son condiciones del proceso: ningún atributo del descriptor queda vacío (B8), ninguna corrección de la revisión de criterios se aplica sin la firma del anotador (B9; capítulo 4, sección 4.10) y la anotación describe la imagen de su registro (B10), como exige la definición 5.1. La anotación congelada v2.1 cumple las diez; para B10 se trasladaron a su registro, antes de congelar, ocho anotaciones desplazadas. El anexo A detalla el control de cada condición.

**Casos admitidos.** En la versión 2.1, 53 piezas tienen palabra de bandas, 83 la tienen `ausente` y 14 no la tienen observada (11 `no_observable` y 3 `desconocido`). Cuatro situaciones son legítimas y no deben confundirse con incoherencias: 5 palabras tienen una sola banda, de modo que su bloque de adyacencias no es observable y $d_w$ frente a otra palabra de una banda solo vale 0 o 1; 21 tienen dos bandas contiguas del mismo tipo, admisibles porque una banda se delimita por un cambio de color **o** de diseño (definición 5.6), y la palabra no se comprime; 19 pertenecen a piezas cuya composición dominante no es de bandas (capítulo 4, sección 4.7.3); y 2 contienen el símbolo `no_determinada`. Las palabras tienen entre 1 y 14 símbolos, y la mitad tiene 3 o menos. Ninguna contiene una laguna: su tratamiento (definiciones 5.8 y 5.10) está definido y probado con casos sintéticos, pero **no se ejerce en el núcleo**.

## 5.5 La palabra de bandas

**Definición 5.6 (banda) [D].** Una banda es una franja que atraviesa toda la superficie visible en sentido perpendicular al eje de lectura y está delimitada por un cambio de color o de diseño. No son bandas las franjas perimetrales (se registran en `borde`), las filas o columnas de una retícula ni los paneles (se registran en `composicion`). La composición dominante no decide si hay bandas: una pieza de paneles o de campo puede tener franjas que la cruzan de lado a lado. El capítulo 4 (sección 4.7.3) da su correlato técnico en la faz de urdimbre, el tapiz y el bordado.

**Definición 5.7 (alfabeto) [D].**

$$\Sigma = \{\text{lisa} < \text{geométrica} < \text{figurativa} < \text{mixta} < \text{no determinada}\}, \qquad k = \lvert\Sigma\rvert = 5. \tag{5.4}$$

Cada símbolo es un **tipo** de banda. No codifica color ni anchura. El orden total es convencional y solo sirve para definir la forma canónica.

**Definición 5.8 (laguna).** El símbolo $\bot \notin \Sigma$ marca un tramo que no puede observarse (pérdida, pliegue, encuadre). No es un tipo de banda.

**Definición 5.9 (palabra).** La palabra de una pieza es

$$w = w_1 w_2 \cdots w_l \in (\Sigma \cup \{\bot\})^{*}, \tag{5.5}$$

leída a lo largo del eje registrado en `eje_bandas`, con al menos un símbolo de $\Sigma$ (condición B4). Se almacena en `secuencia_bandas` con los símbolos separados por ` > `. La palabra vacía $\varepsilon$ no se escribe: corresponde al estado `ausente`, es decir, la pieza se observó y no tiene bandas. Dos símbolos contiguos pueden ser iguales (sección 5.4.1).

**Definición 5.10 (tramos y palabra sin lagunas).** Los tramos de $w$ son sus subpalabras maximales sin lagunas. La palabra sin lagunas, $\tilde{w} \in \Sigma^{*}$, es la concatenación de sus tramos en orden.

*Nota sobre las lagunas* **[D]**. Al concatenar los tramos, $\tilde{w}$ pone en contacto dos bandas que en la pieza están separadas por un tramo perdido. La distancia entre palabras (sección 5.8.1) trabaja sobre $\tilde{w}$ y acepta esa aproximación; el histograma de adyacencias (sección 5.8.2) no la acepta, y cuenta los pares solo dentro de cada tramo. Con la condición B4, $\tilde{w} \neq \varepsilon$ para toda palabra anotada, y la palabra vacía queda reservada a `ausente`.

## 5.6 Equivalencia por reversión y forma canónica

**Definición 5.11 (reversión) [D].** Sea $\rho$ la aplicación que invierte una palabra: $\rho(w_1 \cdots w_l) = w_l \cdots w_1$. Como $\rho \circ \rho = \mathrm{id}$, el conjunto $C_2 = \{e, \rho\}$ es un grupo que actúa sobre $\Sigma^{*}$. Dos palabras son **equivalentes** si están en la misma órbita:

$$w \sim v \iff v \in \{w, \rho(w)\}. \tag{5.6}$$

No se incluye ninguna otra transformación. La rotación de 90° no conserva el dominio, porque la palabra se lee sobre un solo eje. La permutación de tipos destruiría la información que el alfabeto registra. El desplazamiento cíclico supondría una banda circular, que el corpus no justifica.

**Definición 5.12 (forma canónica).**

$$c(w) = \min\nolimits_{\text{lex}} \{w, \rho(w)\}, \tag{5.7}$$

con el orden lexicográfico inducido por el orden de $\Sigma$.

**Proposición 5.1 [P].** Para toda $w, v \in \Sigma^{*}$:

1. *Invariancia:* $c(\rho(w)) = c(w)$.
2. *Completitud:* $c(w) = c(v)$ si y solo si $w \sim v$.
3. *Costo:* $c(w)$ se calcula en $O(l)$.

*Demostración.* (1) $\{\rho(w), \rho(\rho(w))\} = \{\rho(w), w\}$, y el mínimo de un mismo conjunto es único. (2) Si $w \sim v$, las órbitas coinciden y por (1) también sus mínimos. Recíprocamente, $c(w)$ pertenece a la órbita de $w$ y $c(v)$ a la de $v$; si son iguales, las órbitas comparten un elemento y, al ser clases de equivalencia, coinciden. (3) Invertir y comparar dos palabras de longitud $l$ requiere $O(l)$ operaciones. $\blacksquare$

**Observación 5.1 (palíndromos y simetría bilateral).** Los puntos fijos de $\rho$ son los palíndromos: $\rho(w) = w$. Una palabra es un palíndromo exactamente cuando la secuencia de **tipos** de banda es simétrica respecto de la línea media perpendicular al eje de lectura. El palíndromo es, pues, la contraparte formal de una disposición bilateral de las bandas. La correspondencia es solo a nivel de tipos: dos bandas del mismo tipo pueden diferir en color o en anchura, que la palabra no registra.

## 5.7 Enumeración: cuánta información puede portar el orden

Los resultados de esta sección son conocidos. Su papel en la tesis es acotado: cuantifican cuántas configuraciones distingue la codificación elegida y, en particular, cuántas distingue el orden más allá del inventario de tipos. No prueban originalidad ni rendimiento.

**Teorema 5.1 (lema de conteo de órbitas) [T].** Sea $G$ un grupo finito que actúa sobre un conjunto finito $X$. El número de órbitas es

$$\lvert X / G \rvert = \frac{1}{\lvert G \rvert} \sum_{g \in G} \lvert \mathrm{Fix}(g) \rvert, \qquad \mathrm{Fix}(g) = \{x \in X : g \cdot x = x\}. \tag{5.8}$$

Es el resultado clásico de la teoría de grupos conocido como lema de Burnside.

**Corolario 5.1 [T].** El número de formas canónicas de longitud $l$ sobre $k$ símbolos es

$$N(k, l) = \frac{k^{l} + k^{\lceil l/2 \rceil}}{2}. \tag{5.9}$$

*Demostración.* Se aplica (5.8) con $X = \Sigma^{l}$ y $G = C_2$. La identidad fija las $k^{l}$ palabras. La reversión fija los palíndromos, que quedan determinados por sus primeras $\lceil l/2 \rceil$ letras. $\blacksquare$

Con $k = 2$ y $l = 4$: $(16 + 4)/2 = 10$. Con el alfabeto del descriptor ($k = 5$) y cuatro bandas: $(625 + 25)/2 = 325$. Una prueba automatizada enumera las órbitas con la función de forma canónica y las compara con (5.9) para $k \in \{2, 3, 5\}$ y $l \le 5$.

**Corolario 5.2 (formas canónicas con un contenido dado) [T].** Sea $(n_1, \dots, n_k)$ el contenido de una palabra: el número de bandas de cada tipo, con $\sum_i n_i = l$. Las palabras con ese contenido son

$$M = \frac{l!}{n_1! \cdots n_k!}, \tag{5.10}$$

y de ellas son palíndromos

$$P = \begin{cases} \dfrac{\lfloor l/2 \rfloor!}{\lfloor n_1/2 \rfloor! \cdots \lfloor n_k/2 \rfloor!} & \text{si a lo sumo un } n_i \text{ es impar},\\[2ex] 0 & \text{en caso contrario.} \end{cases} \tag{5.11}$$

El número de formas canónicas con ese contenido es $(M + P)/2$.

*Demostración.* El conjunto de palabras con un contenido fijo es invariante por $\rho$, de modo que (5.8) se aplica a ese conjunto. Un palíndromo queda determinado por su primera mitad, que contiene $\lfloor n_i/2 \rfloor$ letras de cada tipo; si hay un $n_i$ impar, esa letra ocupa el centro, y si hay más de uno no existe palíndromo. $\blacksquare$

Es el caso más simple de la enumeración de configuraciones con un contenido prescrito (teorema de enumeración de Pólya). Para $C_2$ el conteo es directo y no requiere el índice de ciclos.

**Ejemplo 5.1.** Con dos bandas de cada uno de dos tipos: $M = 6$, $P = 2$ (`abba` y `baab`) y, por tanto, 4 formas canónicas: `aabb`, `abab`, `abba`, `baab`. Las cuatro comparten inventario de tipos. Un descriptor sin orden las confunde; el descriptor con orden las separa.

**Alcance de estos resultados.** El cociente entre (5.9) y el número de contenidos posibles mide cuánta información *puede* portar el orden bajo la codificación elegida. No dice que esa información sea útil para recuperar piezas (H2 **[E]**), ni que el diseño andino se conciba como palabras bajo reversión, cuestión que queda fuera de la tesis. Tampoco describe el corpus: cuántas piezas de la galería comparten contenido y difieren en forma canónica es un dato empírico, que se informa en la sección 5.13.

## 5.8 Distancias por bloque

El descriptor de un registro es la tupla de sus bloques (Cuadro 5.3). Cada bloque $b$ tiene una distancia $d_b$ con valores en $[0, 1]$, definida solo cuando el bloque es observable en las dos piezas.

**Cuadro 5.3.** Bloques del descriptor estructural.

| Bloque | Atributo de la anotación | Distancia $d_b$ | Sección |
|---|---|---|---|
| Composición | `composicion` | Nominal | 5.8.4 |
| Bandas | `secuencia_bandas` | $d_w$ | 5.8.1 |
| Adyacencias | derivado de `secuencia_bandas` | $d_h$ | 5.8.2 |
| Borde decorado | `borde` | Nominal | 5.8.4 |
| Centro | `centro` | Nominal | 5.8.4 |
| Simetría | `simetria` | Nominal | 5.8.4 |
| Repetición | `repeticion` | Ordinal | 5.8.4 |
| Motivos | `motivos` | Jaccard | 5.8.4 |
| Familia iconográfica | `familia_iconografica` | Nominal | 5.8.4 |

**Exclusiones [D].** El color no forma parte del descriptor, para que una ganancia de M3 no pueda ser de origen cromático; el color ya está representado en M1 (color y textura) y en M2. El motivo principal tampoco: se solapa con los bloques de motivos y de familia iconográfica, y en la primera anotación 36 de las 150 piezas lo registraban como desconocido. El eje de las bandas queda fuera por la razón expuesta en la sección 5.2.

### 5.8.1 Distancia entre palabras

Sea $\mathrm{lev}(x, y)$ la distancia de Levenshtein: el número mínimo de inserciones, eliminaciones y sustituciones de un símbolo que transforman $x$ en $y$. Es una métrica en $\Sigma^{*}$ y se calcula en $O(\lvert x \rvert \cdot \lvert y \rvert)$ por programación dinámica con el algoritmo de Wagner y Fischer **[T]**.

**Lema 5.1 (la reversión es una isometría) [P].** Para toda $x, y \in \Sigma^{*}$, $\mathrm{lev}(\rho(x), \rho(y)) = \mathrm{lev}(x, y)$.

*Demostración.* Una sucesión de operaciones de edición que lleva $x$ a $y$ se convierte, aplicando cada operación en la posición reflejada, en una sucesión del mismo número de operaciones que lleva $\rho(x)$ a $\rho(y)$. La correspondencia es biyectiva porque $\rho$ es una involución; luego los mínimos coinciden. $\blacksquare$

**Proposición 5.2 (métrica entre órbitas, sin normalizar) [P].** La función

$$\delta(w, v) = \min\{\mathrm{lev}(w, v),\ \mathrm{lev}(w, \rho(v))\} \tag{5.12}$$

es una métrica en el conjunto de órbitas $\Sigma^{*}/C_2$: es simétrica, satisface la desigualdad triangular y $\delta(w, v) = 0$ si y solo si $w \sim v$.

*Demostración.* Por el lema 5.1, $\mathrm{lev}(w, \rho(v)) = \mathrm{lev}(\rho(w), v)$, de donde $\delta$ es simétrica y no depende del representante elegido en cada órbita. $\delta(w, v) = 0$ equivale a $v = w$ o $\rho(v) = w$. Para la desigualdad triangular, sean $g, g' \in C_2$ tales que $\delta(x, y) = \mathrm{lev}(x, g y)$ y $\delta(y, z) = \mathrm{lev}(y, g' z)$. Por el lema 5.1, $\mathrm{lev}(g y, g g' z) = \mathrm{lev}(y, g' z)$. Entonces

$$\delta(x, z) \le \mathrm{lev}(x, g g' z) \le \mathrm{lev}(x, g y) + \mathrm{lev}(g y, g g' z) = \delta(x, y) + \delta(y, z). \qquad \blacksquare$$

**Definición 5.13 (distancia normalizada entre palabras) [D].** Para dos palabras $w, v$ con palabras sin lagunas $\tilde{w}, \tilde{v}$,

$$d_w(w, v) = \frac{\delta(\tilde{w}, \tilde{v})}{\max(\lvert \tilde{w} \rvert, \lvert \tilde{v} \rvert)}, \qquad d_w(\varepsilon, \varepsilon) = 0. \tag{5.13}$$

La normalización hace comparables piezas con distinto número de bandas y lleva el bloque a la escala $[0, 1]$ que exige la disimilitud mixta. Su precio, la pérdida de la desigualdad triangular, se precisa en la proposición 5.4.

**Proposición 5.3 [P].** Para toda $w, v$:

1. *Rango:* $d_w(w, v) \in [0, 1]$. Una palabra vacía frente a una no vacía está a distancia 1.
2. *Simetría:* $d_w(w, v) = d_w(v, w)$.
3. *Invariancia:* $d_w(\rho(w), v) = d_w(w, \rho(v)) = d_w(w, v)$.
4. *Identidad en las órbitas:* $d_w(w, v) = 0$ si y solo si $\tilde{w} \sim \tilde{v}$.
5. *Costo:* $O(\lvert \tilde{w} \rvert \cdot \lvert \tilde{v} \rvert)$.

*Demostración.* (1) $\mathrm{lev}(x, y) \le \max(\lvert x \rvert, \lvert y \rvert)$: basta sustituir las posiciones comunes y luego insertar o eliminar las restantes. Si $x = \varepsilon$ e $y \neq \varepsilon$, $\mathrm{lev} = \lvert y \rvert$. (2)–(4) se siguen de la proposición 5.2, porque el denominador es simétrico e invariante por $\rho$, y $\rho$ conmuta con la eliminación de lagunas salvo reversión: $\widetilde{\rho(w)} = \rho(\tilde{w})$. (5) Dos ejecuciones del algoritmo de Wagner y Fischer. $\blacksquare$

**Proposición 5.4 ($d_w$ no es una métrica) [P].** La distancia normalizada (5.13) no satisface la desigualdad triangular.

*Contraejemplo.* Sean $x = \texttt{aab}$, $y = \texttt{aaba}$, $z = \texttt{aba}$. Entonces $d_w(x, y) = 1/4$, $d_w(y, z) = 1/4$ y $d_w(x, z) = 2/3 > 1/2$. $\blacksquare$

La normalización simple de la distancia de edición por la longitud pierde, en general, la desigualdad triangular. Aquí se mantiene la normalización por la longitud mayor porque es la más legible («fracción de bandas que hay que cambiar») y porque el método no usa la desigualdad triangular en ningún paso (sección 5.9). Si un trabajo posterior necesitara la garantía métrica (índices métricos, agrupamiento), dispone de $\delta$ sin normalizar (proposición 5.2).

### 5.8.2 Adyacencias

**Definición 5.14 [D].** $h(w)$ es el histograma normalizado de los pares **no ordenados** $\{w_j, w_{j+1}\}$ de símbolos contiguos dentro de cada tramo de $w$. Una laguna no forma pares. La distancia es

$$d_h(w, v) = \tfrac{1}{2} \lVert h(w) - h(v) \rVert_1 \in [0, 1], \tag{5.14}$$

la distancia de variación total entre dos distribuciones. Si alguna de las dos palabras no tiene ningún par (cero o una banda por tramo), el bloque no es observable **para ese par de piezas**: la observabilidad de este bloque depende del par, y no solo de cada pieza.

**Proposición 5.5 [P].** $h(\rho(w)) = h(w)$; por tanto, $d_h$ es invariante a la reversión en ambos argumentos.

*Demostración.* $\rho$ transforma cada par contiguo $(w_j, w_{j+1})$ en el par $(w_{j+1}, w_j)$ dentro del mismo tramo; como par no ordenado es el mismo. $\blacksquare$

Se eligen pares no ordenados precisamente para obtener esta invariancia sin fijar un sentido de lectura.

**Observación 5.2 (adyacencias y palabra no son redundantes).** `aabb` y `abab` tienen el mismo histograma de tipos y distintas adyacencias: $h(\texttt{aabb})$ reparte su masa por igual entre $\{a,a\}$, $\{a,b\}$ y $\{b,b\}$, y $h(\texttt{abab})$ la concentra en $\{a,b\}$. A la inversa, las adyacencias no determinan la palabra: `aabab` y `abaab` tienen el mismo histograma de adyacencias y formas canónicas distintas. Los dos bloques miden aspectos diferentes del orden: el primero, la secuencia completa; el segundo, la vecindad local.

El descriptor no prescribe qué vecindades son admisibles; describe cuáles se observan en cada pieza. Con un corpus finito, que una vecindad no se haya observado no significa que no esté permitida.

### 5.8.3 Control sin orden

**Definición 5.15 (M3-sin-orden) [D].** Sea $t(w)$ el histograma normalizado de los tipos de $\tilde{w}$. El control sustituye $d_w$ por

$$d_t(w, v) = \tfrac{1}{2} \lVert t(w) - t(v) \rVert_1, \tag{5.15}$$

con $d_t(\varepsilon, \varepsilon) = 0$ y $d_t = 1$ si exactamente una de las dos palabras es vacía, y omite el bloque de adyacencias. Usa los mismos pesos, sin reajustarlos. No hay otra diferencia en la definición, pero al omitir un bloque cambia además la normalización de $D$ (véase la interpretación de la proposición 5.6).

**Proposición 5.6 (en el bloque de bandas, el control acota inferiormente a la distancia con orden) [P].** Para toda $w, v$,

$$d_t(w, v) \le d_w(w, v). \tag{5.16}$$

En particular, $d_w(w, v) = 0$ implica $d_t(w, v) = 0$, y el recíproco es falso.

*Demostración.* Si alguna palabra es vacía, ambas distancias valen lo mismo (0 o 1). En otro caso, sean $x = \tilde{w}$, $y = \tilde{v}$ con $m = \lvert x \rvert \le n = \lvert y \rvert$, y sean $a_s, b_s$ el número de apariciones del símbolo $s$ en $x$ e $y$. En un alineamiento óptimo, cada posición de $y$ está emparejada con un símbolo igual de $x$ o cuesta al menos una operación; el número de emparejamientos iguales es a lo sumo $\sum_s \min(a_s, b_s)$. Luego $\mathrm{lev}(x, y) \ge n - \sum_s \min(a_s, b_s)$. Por otra parte, $d_t = 1 - \sum_s \min(a_s/m, b_s/n)$ y, como $m \le n$, $\min(a_s/m, b_s/n) \ge \min(a_s, b_s)/n$. Por tanto $d_t \le 1 - \sum_s \min(a_s, b_s)/n \le \mathrm{lev}(x, y)/n$. El mismo argumento vale para $\rho(y)$, que tiene los mismos conteos; luego $d_t \le \delta(x, y)/n = d_w$. El recíproco falla con `aabb` y `abab`: $d_t = 0$ y $d_w = 1/2$. $\blacksquare$

*Interpretación.* La proposición compara dos distancias entre palabras de bandas: la distancia con orden nunca es menor que la distancia entre los histogramas de tipos, y separa pares de palabras que el histograma confunde. Su alcance es ese bloque. No se extiende a la disimilitud agregada $D$ ni al ordenamiento de los candidatos: el control también omite el bloque de adyacencias y, al promediar sobre un bloque menos, cambia la normalización de los demás, de modo que la disimilitud agregada de M3-sin-orden puede ser mayor o menor que la de M3, y el orden relativo de dos candidatos puede invertirse aunque ambos tengan histogramas distintos del de la consulta. La diferencia entre M3 y M3-sin-orden reúne, por tanto, el orden, las adyacencias y esa renormalización, y su efecto sobre la recuperación solo puede establecerse empíricamente, en H2 **[E]**.

*Verificación.* Una prueba automatizada recorre por enumeración exhaustiva, con la implementación, todas las palabras de longitud 0 a 5 sobre un alfabeto de tres símbolos (132 496 pares) y no encuentra ninguna violación, salvo diferencias de redondeo del orden de $10^{-16}$; comprueba además el contraejemplo del recíproco.

### 5.8.4 Bloques nominales, ordinal y de conjunto

- **Nominal** (`composicion`, `borde`, `centro`, `simetria`, `familia_iconografica`): $d_b = 0$ si los valores coinciden y 1 si no. Los valores de ausencia observada ($Z_k$ en el Cuadro 5.2: `no`, `no_evidente`, `ausente`) son un valor más: dos piezas sin borde decorado coinciden en ese bloque.
- **Ordinal** (`repeticion`, con el orden no < parcial < sí): $d_b = \lvert \mathrm{rango}(u) - \mathrm{rango}(v) \rvert / 2$.
- **Conjunto** (`motivos`): distancia de Jaccard, $d_b(X, Y) = 1 - \lvert X \cap Y \rvert / \lvert X \cup Y \rvert$, con $d_b(\varnothing, \varnothing) = 0$. Es una métrica en los conjuntos finitos **[T]**.

Todas toman valores en $[0, 1]$, son simétricas y se anulan cuando los valores coinciden.

**Simetría y repetición como atributos anotados [D].** La simetría se registra con las categorías del vocabulario, que separan la repetición traslacional (en una dirección) de la modular (en dos) (capítulo 4, sección 4.7.4); no se calcula ningún grupo de simetría a partir de la imagen. La repetición es un atributo ordinal anotado, y el descriptor no calcula un periodo; calcularlo sobre la palabra de bandas, con tratamiento de lagunas, queda como extensión.

## 5.9 Disimilitud mixta

**Definición 5.16.** Sean $\lambda_b \ge 0$ los pesos de los bloques, iguales en la configuración inicial, y

$$B(i, j) = \{\, b : m_b(i) = m_b(j) = 1,\ d_b(i, j) \text{ definida},\ \lambda_b > 0 \,\} \tag{5.17}$$

el conjunto de bloques comparables para el par $(i, j)$. Si $B(i, j) \neq \varnothing$,

$$D(i, j) = \frac{\sum_{b \in B(i,j)} \lambda_b\, d_b(i, j)}{\sum_{b \in B(i,j)} \lambda_b}. \tag{5.18}$$

$D$ tiene la forma del coeficiente general de Gower para datos mixtos con valores faltantes: cada variable aporta una puntuación en $[0, 1]$ en su propia escala, y las variables no comparables para un par se excluyen del numerador y del denominador. La diferencia es que aquí dos de las «variables» son estructuradas (una palabra y un histograma) y tienen distancias propias **[T, D]**.

**Ausencia de evidencia [D].** Si $B(i, j) = \varnothing$, $D$ no está definida. El par queda «sin evidencia estructural»: no recibe similitud máxima ni mínima, y en el *ranking* de M3 se ubica después de todos los candidatos con evidencia, ordenado por identificador.

**Definición 5.17 (cobertura).**

$$\kappa(i, j) = \frac{\sum_{b \in B(i,j)} \lambda_b}{\sum_{b} \lambda_b} \in [0, 1]. \tag{5.19}$$

Se informa junto con $D$. Una disimilitud calculada sobre un solo bloque y otra calculada sobre nueve no tienen el mismo respaldo, y la cobertura lo hace visible.

**Definición 5.18 (*ranking* de M3).** Para una consulta $q$, los candidatos con evidencia se ordenan por $D(q, \cdot)$ ascendente; los empates se resuelven por identificador ascendente. El *ranking* es, por tanto, determinista. La puntuación que M3 entrega a la fusión es $s_{M3} = 1 - D$.

**Proposición 5.7 [P].** Cuando $D$ está definida:

1. *Rango.* $D(i, j) \in [0, 1]$.
2. *Simetría.* $D(i, j) = D(j, i)$.
3. *Reflexividad.* $D(i, i) = 0$.
4. *Descomposición exacta.* Con $c_b(i, j) = \lambda_b\, d_b(i, j) / \sum_{b' \in B(i,j)} \lambda_{b'}$, se cumple $\sum_{b \in B(i,j)} c_b = D(i, j)$.
5. *Intervención.* Anular $\lambda_b$ equivale a recalcular $D$ sobre $B(i, j) \setminus \{b\}$ con los pesos restantes renormalizados.
6. *Homogeneidad.* $D$ no cambia si todos los pesos se multiplican por una misma constante positiva; solo importan sus proporciones.

*Demostración.* (1) $D$ es una media ponderada, con pesos positivos, de valores en $[0, 1]$. (2) $B(i, j) = B(j, i)$ y cada $d_b$ es simétrica. (3) $d_b(i, i) = 0$ para todo bloque. (4) Es la definición (5.18) escrita término a término. (5) Con $\lambda_b = 0$, el bloque sale de $B$ por (5.17), y (5.18) se evalúa sobre los restantes. (6) La constante se cancela entre numerador y denominador. $\blacksquare$

**Proposición 5.8 (lo que $D$ no cumple) [P].** Con máscaras variables:

1. $D$ no satisface la desigualdad triangular.
2. $D(i, j) = 0$ no implica que los descriptores de $i$ y $j$ coincidan.

*Contraejemplo.* Con pesos iguales, sean tres piezas con estos bloques observados: $i$, composición (bandas) y simetría (traslacional); $j$, composición (bandas) y borde (sí); $k$, borde (sí) y simetría (bilateral). Entonces $B(i, j) = \{\text{composición}\}$ y $D(i, j) = 0$; $B(j, k) = \{\text{borde}\}$ y $D(j, k) = 0$; $B(i, k) = \{\text{simetría}\}$ y $D(i, k) = 1$. Luego $D(i, k) > D(i, j) + D(j, k)$, y $D(i, j) = 0$ con descriptores distintos. $\blacksquare$

El fallo tiene dos orígenes independientes: la máscara variable (este contraejemplo) y la normalización de $d_w$ (proposición 5.4). Tampoco se afirma que $1 - D$ sea un núcleo semidefinido positivo, propiedad que con valores faltantes no está garantizada.

**Consecuencia para el método.** $D$ es una **disimilitud**, no una distancia métrica. El método solo ordena candidatos por $D$ dentro de cada consulta y no usa índices métricos, agrupamiento, inmersión ni núcleos, de modo que ningún paso depende de las propiedades que no se cumplen. Una prueba automatizada fija los dos contraejemplos.

## 5.10 Fusión tardía

**Espacios separados [D].** Cada sistema opera en su propio espacio: M0, en los términos de la ficha; M2, en el espacio de vectores de OpenCLIP; M3, en el espacio de descriptores. **No se combinan representaciones** ni se supone alineación alguna entre esos espacios: sumar un vector visual y un descriptor estructural exigiría la misma dimensión y un espacio compatible, y ninguna de las dos condiciones se cumple. La fusión es tardía y actúa sobre puntuaciones.

**Definición 5.19 (normalización por consulta).** Para una consulta $q$, un componente $c \in \{\text{M0}, \text{M2}, \text{M3}\}$ y un candidato $i$ con puntuación $s_c(q, i)$,

$$\hat{s}_c(q, i) = \frac{s_c(q, i) - \min_{i'} s_c(q, i')}{\max_{i'} s_c(q, i') - \min_{i'} s_c(q, i')}, \tag{5.20}$$

con mínimo y máximo sobre los candidatos que tienen valor. Si todos coinciden, $\hat{s}_c = 0$ para todos: el componente no ordena esa consulta.

**Definición 5.20 (fusión).** Sea $C(q, i)$ el conjunto de componentes con evidencia para el par y $\alpha_c \ge 0$ los pesos. Entonces

$$s(q, i) = \sum_{c \in C(q,i)} \alpha'_c\, \hat{s}_c(q, i), \qquad \alpha'_c = \frac{\alpha_c}{\sum_{c' \in C(q,i)} \alpha_{c'}}. \tag{5.21}$$

Es una combinación convexa de puntuaciones normalizadas, la forma de fusión que Bruch et al. [@bruch2023] analizan frente a la fusión por posiciones. Su análisis cubre la fusión de dos sistemas; la extensión a tres componentes y el ajuste de los pesos con diez consultas de desarrollo no tienen respaldo cuantitativo en ese trabajo (capítulo 3, sección 3.7).

**Proposición 5.9 [P].**

1. *Rango.* $s(q, i) \in [0, 1]$.
2. *Descomposición exacta.* Las contribuciones $\alpha'_c\, \hat{s}_c$ suman $s$.
3. *Intervención.* Retirar un componente equivale a declararlo sin evidencia para todos los candidatos; los pesos restantes se renormalizan.
4. *Sin evidencia estructural.* Un par sin evidencia en M3 no recibe la puntuación máxima ni mínima de M3: su peso se reparte entre los demás componentes en proporción a sus pesos.
5. *Invariancia afín.* $\hat{s}_c$ no cambia si $s_c$ se sustituye por $a\, s_c + b$ con $a > 0$, para una misma consulta. En particular, usar $1 - D$ o $-D$ como puntuación de M3 produce la misma fusión.
6. *Dependencia del conjunto de candidatos.* $\hat{s}_c$ depende del mínimo y del máximo de la consulta. La puntuación de un par no es comparable entre consultas y solo se usa para ordenar dentro de cada una.

*Demostración.* (1) y (2): $s$ es una combinación convexa de valores en $[0, 1]$, y la suma de sus términos es $s$ por definición. (3) y (4) son la definición de $C(q, i)$ y de $\alpha'_c$. (5) La transformación afín positiva se cancela en (5.20). (6) Es inmediato de (5.20). $\blacksquare$

Las propiedades 2 y 3 son, respectivamente, la primera y la segunda comprobación de H3, y la 3 es además la forma de calcular las ablaciones. Que se cumplan como identidad algebraica no hace trivial a H3: lo que se contrastó en la evaluación final es que la implementación las satisface en **todos** los resultados de prueba, dentro de una tolerancia numérica fijada de antemano.

**Variante por posiciones recíprocas.** La fusión $\sum_c 1/(60 + r_c)$, con $r_c$ la posición del candidato en el *ranking* del componente $c$ [@cormack2009], no tiene pesos y no conserva la descomposición. Se implementa como variante de comparación (M4-RRF) y no interviene en H3.

**Relación con los modelos de cuello de botella de conceptos.** El marco más cercano es el de Koh et al. [@koh2020]: la decisión pasa por conceptos legibles. La diferencia es que allí los conceptos se predicen desde la imagen y aquí los anota una persona. M4 es aditivo y produce su propia explicación [@rudin2019]; lo que H3 comprueba es su fidelidad, no su plausibilidad [@jacovi2020].

## 5.11 Costo computacional

Sea $n = \lvert \mathcal{C}(q) \rvert$ el número de candidatos de una consulta, $\lvert B \rvert$ el número de bloques y $L$ la longitud máxima de una palabra de bandas en la galería. El Cuadro 5.4 resume el costo de cada operación.

**Cuadro 5.4.** Costo computacional del descriptor y de la fusión.

| Operación | Costo |
|---|---|
| Forma canónica de una palabra | $O(L)$ |
| Histogramas de tipos y de adyacencias | $O(L)$ |
| Distancia entre dos palabras | $O(L^2)$ |
| Disimilitud de un par | $O(\lvert B \rvert + L^2)$ |
| *Ranking* de una consulta en M3 | $O(n\,(\lvert B \rvert + L^2) + n \log n)$ |
| Fusión de una consulta | $O(n)$ por componente, más la ordenación |

Con una galería de unos cientos de piezas y palabras de pocas decenas de símbolos, el costo es despreciable frente al cálculo de los vectores de M2. No se hace ninguna afirmación de escalabilidad a colecciones grandes: sin desigualdad triangular no pueden usarse índices métricos, y la comparación es exhaustiva, consecuencia directa de la proposición 5.8.

## 5.12 De la formalización a las hipótesis

Las afirmaciones sobre la utilidad del descriptor no son relaciones matemáticas, sino hipótesis sobre resultados observables **[E]**, formuladas como en el capítulo 2 (sección 2.5) y contrastadas en la tarea T3 (capítulo 7):

- **H1 (primaria).** La diferencia media por consulta de nDCG@10 entre M4 y M2 es distinta de cero en la prueba de permutación (p < 0,05) y la diferencia observada es igual o superior a 0,03.
- **H2 (mecanismo).** M3 obtiene mejor nDCG@10 que M3-sin-orden, con las mismas consultas, candidatos y pesos.
- **H3 (fidelidad).** En todos los resultados de prueba, la puntuación de M4 coincide con la suma de sus contribuciones y responde a la retirada de un componente como predice (5.21).

El Cuadro 5.5 separa lo que la formalización establece de lo que solo el experimento podía establecer. El capítulo 8 informa el contraste: H1 y H3 se sostuvieron, y en H2 no se detectó una mejora atribuible al orden de las bandas.

**Cuadro 5.5.** Aporte de la formalización a cada hipótesis.

| Hipótesis | Lo que el capítulo establece | Lo que solo el experimento puede establecer |
|---|---|---|
| H1 | Que la fusión está bien definida, incluso cuando falta evidencia estructural (proposición 5.9) | Que la fusión supera a un codificador general; el aporte propio de la estructura solo se examina en ablaciones exploratorias |
| H2 | Que, en el bloque de bandas, la distancia con orden acota superiormente a la del histograma de tipos (proposición 5.6), y qué cambia el control: el bloque de bandas, la omisión de las adyacencias y la normalización (definición 5.15). No establece un refinamiento de la disimilitud agregada ni del orden de los candidatos | Si M3 recupera mejor que M3-sin-orden, una comparación empírica |
| H3 | Que la descomposición y la intervención son identidades de la fórmula (proposiciones 5.7 y 5.9) | Que la implementación las cumple en todos los resultados de prueba |

## 5.13 Palabras de bandas y coincidencias de inventario en el corpus

La composición de la galería respecto del orden de las bandas podía describirse antes del experimento, sin ningún juicio de relevancia **[E]**. En la anotación v2.1, solo 53 de las 150 piezas del núcleo tienen palabra de bandas, y el orden solo puede pesar cuando la consulta y el candidato la tienen. Entre esas 53 piezas hay 1378 pares. En 41 de ellos el control sin orden ve el mismo histograma normalizado de tipos, y en 25 de esos 41 la forma canónica difiere: son los únicos pares en que, en el bloque de bandas, el control da distancia cero y M3 no. Contando bandas en lugar de proporciones, solo 3 pares comparten inventario y difieren en el orden. Estos conteos describen las coincidencias que el control no distingue; no acotan cuántas veces el orden cambia la posición relativa de dos candidatos, que también puede cambiar entre piezas con histogramas distintos (sección 5.8.3).

Cuando la pieza de consulta no tiene palabra de bandas, porque su secuencia es `ausente` o no observable, $d_w$ y $d_t$ coinciden para todo candidato y el bloque de adyacencias no es observable. M3 y su control asignan entonces la misma puntuación a todos los candidatos, y la diferencia pareada de H2 es cero por construcción. En desarrollo ocurrió en 8 de las 10 consultas, en las que M3 y M3-sin-orden produjeron el mismo *ranking* completo. Por eso, antes de abrir la partición de prueba y sin ver ningún resultado, se mantuvo la regla de H2 sobre las 30 consultas de prueba y se añadió, como subgrupo descriptivo, la misma comparación en las consultas cuya pieza tiene palabra de bandas (capítulo 7, secciones 7.5 y 7.8).

Así ocurrió en la evaluación final: la diferencia fue cero por construcción en 21 de las 30 consultas, y solo las 9 con palabra de bandas aportaron diferencias distintas de cero. No se detectó una mejora atribuible al orden de las bandas (capítulo 8, sección 8.4). El resultado es compatible con la composición de la galería descrita aquí, con pocas piezas con palabra de bandas y pocas coincidencias de inventario con secuencias distintas, pero esos conteos no fijan por sí solos cuánto podía cambiar el orden los *rankings*.

## 5.14 Límites de la formalización

1. **Es una codificación del investigador.** La palabra de bandas describe lo visible en una fotografía con un alfabeto elegido. No se afirma que el diseño se haya concebido así, ni que las cinco clases del alfabeto correspondan a categorías de quienes tejieron las piezas.
2. **Depende de la anotación.** El descriptor hereda la variabilidad del anotador, incluida la de la máscara (sección 5.4). Hay un solo anotador y el acuerdo medido es intra-anotador. La versión 2.1 combina la re-anotación del lote 1, la primera anotación de los lotes 2 a 5 y, sobre esta, las correcciones de una revisión asistida que cambió al menos un atributo del descriptor en 46 de las 150 piezas, con efectos apreciables en los *rankings* de M3 (capítulo 4, sección 4.10.1).
3. **La reversión descarta la orientación de la prenda.** Es convencional en un fragmento y no lo es en una prenda con extremos distinguibles.
4. **El eje es fotográfico.** La palabra no depende de él, pero la decisión de qué cuenta como banda sí depende de cómo se muestra la pieza.
5. **La palabra no registra color ni anchura.** Dos piezas con la misma palabra pueden diferir mucho a la vista. Es deliberado (sección 5.8), y limita lo que «similitud estructural» significa aquí.
6. **La estructura no es independiente de la técnica ni de la tradición.** Como la técnica condiciona la organización en bandas (sección 3.2), una similitud estructural alta puede reflejar en parte la pertenencia a una misma técnica o tradición, que un codificador visual también capta. Una ganancia de M3 no se lee, por sí sola, como evidencia de una gramática estructural independiente del estilo.
7. **No es una métrica.** Sin consecuencias para el método, con consecuencias para su escalabilidad (sección 5.11).
8. **La población es la del corpus.** Lo formalizado se aplica a piezas de tres museos seleccionadas con un criterio que privilegia la legibilidad de colores y figuras. No describe «los textiles andinos».
