# 5. Formalización de la macroestructura observable

> **Borrador 0.3, 21 de noviembre de 2026.** Capítulo de la segunda parte de la tesis. Sustituye al capítulo 5 del primer avance (ecuaciones 5.1 a 5.78), que no se corrige; la sección 5.16 detalla qué cambia y por qué. Los datos citados corresponden a la anotación congelada (`anotacion-v2.1`). Las marcas **[verificar: …]** señalan citas que deben comprobarse contra la fuente antes de la versión final.

**Naturaleza de cada enunciado.** Todo enunciado del capítulo lleva una de cuatro marcas, para que no se confunda lo que se demuestra con lo que se decide o con lo que solo el experimento puede sostener:

- **[T]** resultado conocido de la literatura. Se cita y no se reclama como aporte.
- **[D]** decisión de diseño del investigador. Pudo ser otra, y se justifica.
- **[P]** propiedad del descriptor, demostrada en este capítulo y, salvo indicación expresa, comprobada por una prueba automática (sección 5.15).
- **[E]** afirmación empírica. Ninguna se da por establecida aquí: se contrastan en el capítulo de resultados.

## 5.1 Propósito y alcance

Este capítulo define con precisión qué se compara cuando el método dice que dos textiles «se parecen por su estructura». El objeto formal no es el textil ni su tejido, sino su **macroestructura observable**: la organización de la superficie que una persona puede registrar al mirar la fotografía publicada por un museo. Comprende la composición general, la secuencia de bandas, la presencia de borde y de centro, la simetría, la repetición y los motivos.

El capítulo hace tres cosas:

1. Fija las unidades de análisis y su correspondencia con datos concretos del corpus (secciones 5.3 a 5.5).
2. Define el descriptor estructural, la disimilitud entre piezas y la fusión con los demás sistemas, y demuestra las propiedades que el método usa (secciones 5.6 a 5.12).
3. Separa lo demostrado de lo que queda como hipótesis (sección 5.13) y declara los límites (sección 5.14).

No hace tres cosas que el capítulo del primer avance sugería:

- No modela la estructura técnica del tejido (ligamento, cruces de hilos). Esa escala es la de Helmer y Ngo (2015) y Ngo et al. (2021), y exige datos que una fotografía general no garantiza.
- No infiere la estructura desde los píxeles. El descriptor se calcula sobre una anotación de la que responde una persona; M3 y M4 son sistemas **asistidos por anotación**. En la versión 2.1, una parte de las correcciones partió de propuestas automáticas que el anotador verificó y firmó una a una (capítulo 4, sección 4.10); se declara entre los límites (sección 5.14).
- No atribuye significado cultural a la organización que formaliza, ni afirma que el diseño se haya concebido como la codificación que aquí se elige.

## 5.2 Fundamento en el dominio textil

Las decisiones de diseño de las secciones siguientes responden a rasgos documentados del textil andino y a los límites de la fuente, que es una fotografía de museo. Esta sección los resume; el capítulo 3 (secciones 3.2 y 3.3) los desarrolla.

**Por qué bandas.** En los tejidos de faz de urdimbre, las bandas con diseño resultan del contraste entre hilos que se urden juntos, y el urdido fija qué colores puede tener cada banda antes de tejer (Desrosiers, 2013, pp. 480 y 482); las telas de uso diario muestran a menudo rayas, barras o cuadros por el uso de hilos de colores distintos (Desrosiers, 2024, p. 8). En buena parte del material, la franja transversal es, por tanto, una unidad que la propia técnica produce, y no solo una convención de quien describe. La relación no es una regla: las urdimbres discontinuas permiten cambios de color en sentido transversal (Desrosiers, 2024, p. 12). En el tapiz la banda no viene impuesta por la técnica, que da a la tejedora una libertad comparable a la de una pintora (Desrosiers, 2013, p. 495; 2024, p. 9), y aun así hay bordados que imitan la forma de las bandas tejidas con urdimbres complementarias (Desrosiers, 2013, pp. 498–499). La definición operativa de banda (sección 5.5) recoge el caso común a todas las técnicas: una franja que atraviesa toda la superficie visible.

**Por qué el orden.** La literatura que se pudo leer documenta que, en la faz de urdimbre, las bandas y su paleta quedan fijadas en el urdido, antes de tejer, mientras que la técnica condiciona qué figuras caben en cada una (Desrosiers, 2013, pp. 480–486): la disposición de las bandas es una decisión previa al tejido, no un efecto secundario del decorado. El estudio semiológico de Cereceda sobre las talegas de Isluga, que el primer avance citaba por la disposición de las listas, no se pudo consultar en este trabajo [verificar: Cereceda, 1978], y el análisis de las secuencias de color en los bordados de Paracas Necrópolis tampoco [verificar: Paul, 1997]. Que el orden sea pertinente para el diseño no implica que sea útil para recuperar piezas: eso es H2 **[E]**.

**Por qué no una clasificación por grupos de simetría.** El análisis de simetría de patrones clasifica los patrones de una dimensión en siete tipos y los de dos dimensiones en diecisiete, según las isometrías que admiten (Crowe, 2001, pp. 6–9). Frame (2006a) sostiene que esa clasificación cristalográfica no es apropiada para todos los patrones andinos, cuya lógica deriva en parte de las estructuras de fibra, y Chavey et al. (2015, pp. 85–87) muestran que los diseños de pocas franjas tienen regularidades que ni los frisos ni los patrones del plano recogen. La detección automática del grupo exige, además, un patrón periódico dominante fotografiado de frente y sin distorsiones (Liu et al., 2004, p. 368). El descriptor no clasifica patrones por grupo de simetría: registra la simetría como un atributo nominal anotado (sección 5.8.4), y la única equivalencia formal que impone es la reversión del sentido de lectura (sección 5.6).

**Por qué la reversión.** El sentido en que se lee una secuencia de bandas es una convención del anotador. Para un fragmento no hay extremo privilegiado. Para una prenda completa sí puede haberlo (una túnica con abertura de cuello, un manto con cenefa en un solo extremo), y la formalización lo descarta de manera deliberada. Es una simplificación declarada (sección 5.14).

**Por qué el eje no entra en el descriptor.** El eje registrado es el de la fotografía, no el del telar ni el de uso. En las túnicas de tapiz de la sierra, el decorado se tejía acostado en el telar y la tela se giraba 90 grados al armar la prenda (Desrosiers, 2024, pp. 10–11), y el observador tiende a orientar la tela por la urdimbre sin advertirlo (Desrosiers, 2010, pp. 260–262). Una misma organización puede aparecer, por tanto, horizontal o vertical según cómo se tomó la fotografía. La palabra de bandas no depende del eje; el atributo `eje_bandas` sí refleja la toma, y por eso queda fuera.

## 5.3 Unidades de análisis

El primer avance trataba como un solo objeto cinco cosas distintas. Se separan así.

**Definición 5.1 (unidades).**

| Símbolo | Unidad | Definición | Dato que la materializa |
|---|---|---|---|
| $o$ | Objeto | El textil físico conservado en un museo. No se observa directamente | No tiene identificador propio en el corpus |
| $r$ | Registro | La ficha de un museo, con sus metadatos | Fila del consolidado; clave `FUENTE:id_fuente` |
| $f(r)$ | Fotografía | Copia de evaluación de la imagen de referencia del registro, de 1600 px de lado mayor | Archivo identificado por su suma SHA-256 |
| $G$ | Grupo | Clase de equivalencia de registros que muestran un mismo objeto o partes de él | Grupo decidido por el investigador (capítulo 4, sección 4.6) |
| $a(r)$ | Anotación | Lo que una persona registró al observar $f(r)$ | Fila de la anotación congelada v2.1 |

**Definición 5.2 (grupos) [D].** Sea $R$ el conjunto de registros utilizables del corpus v2.0 y $U \subseteq R \times R$ la relación formada por los pares que el investigador decidió unir. Los grupos son las clases de la clausura reflexiva, simétrica y transitiva de $U$; de forma equivalente, las componentes conexas del grafo $(R, U)$.

El grupo es una aproximación al objeto: dos registros de un mismo grupo no se suponen independientes. Por eso el grupo, y no el registro, es la unidad de partición entre desarrollo y prueba, y una comprobación automática verifica que ningún grupo queda partido. Los conteos de registros, grupos y núcleo figuran en el capítulo 4.

**Definición 5.3 (galería y candidatos).** La galería $\mathcal{G} \subset R$ es el conjunto de registros con anotación estructural (el núcleo). Para una consulta $q \in \mathcal{G}$, el conjunto de candidatos es

$$\mathcal{C}(q) = \mathcal{G} \setminus G(q), \tag{5.1}$$

donde $G(q)$ es el grupo de $q$. Una pieza nunca se recupera a sí misma ni a otra vista del mismo objeto.

**Elegibilidad y estructura [D].** La pertenencia de un registro a $\mathcal{G}$ depende de criterios de calidad fotográfica y de curación (el criterio de aptitud del capítulo 4, sección 4.4). Esos criterios son una función de la fotografía y de la ficha, $E(r, f(r))$, y **definen la población**. No forman parte del descriptor. Dentro de $\mathcal{G}$ no se presupone que una pieza tenga bandas, motivos o simetría observables: cada atributo admite los estados de la sección siguiente. Con esto se corrige la inconsistencia de tipos que la auditoría señaló en las ecuaciones 5.24–5.30 del primer avance, donde restricciones sobre la pieza, la imagen y los metadatos se escribían como funciones del patrón.

## 5.4 Anotación y observabilidad

**Definición 5.4 (espacio de valores).** Sea $A$ el conjunto de atributos estructurales y $V_k$ el vocabulario controlado del atributo $k \in A$ (capítulo 4, sección 4.7). El valor anotado de cada atributo pertenece a una de tres clases disjuntas:

$$\underbrace{P_k}_{\text{presencia}} \;\cup\; \underbrace{Z_k}_{\text{ausencia observada}} \;\cup\; \underbrace{N_k}_{\text{sin observación}}. \tag{5.2}$$

$P_k$ reúne los valores que describen el rasgo; $Z_k$, el valor que registra que el rasgo se buscó y no está; $N_k$, los estados que indican que no pudo observarse o decidirse. Las tres clases no se codifican igual en todos los atributos, porque varios conservan los valores de la tesis (Cuadro 6.4 del primer avance). La tabla fija la correspondencia, que es la que aplican el vocabulario y el código:

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

Un estado ocupa la celda completa: no puede combinarse con valores. El vocabulario declara qué estados admite cada atributo, y la validación de la anotación rechaza los demás.

*Dos categorías residuales* **[D]**. `no_determinada` (en `familia_iconografica` y como tipo de banda) no es un estado de no observación: indica que el rasgo se ve y no corresponde a ninguna categoría del vocabulario. Es un valor de la tesis y se compara como tal. La consecuencia se declara: dos rasgos `no_determinada` coinciden en el descriptor aunque solo compartan no encajar en el vocabulario. En la exportación vigente su uso es marginal (sección 5.4.1).

**Ausente no es no observado [D].** La distinción es sustantiva y recorre todo el capítulo:

- Un valor de $Z_k$ (`ausente`, `no` o `no_evidente`, según el atributo) es una **observación**: el rasgo podía verse y no está. Se compara como cualquier otro valor.
- Los estados de $N_k$ indican **falta de observación**: la fotografía no permite decidir, o el anotador no pudo hacerlo. No se comparan.

El ejemplo de las ecuaciones 5.74–5.77 del primer avance codificaba «sin bandas» y «sin periodo» con ceros, sin distinguir ambos casos. Aquí, una pieza sin bandas se anota `ausente` (y su palabra es la palabra vacía, sección 5.5), mientras que una pieza cuyas bandas no pueden distinguirse se anota `no_observable` (y el bloque no participa).

**Definición 5.5 (máscara).** Para cada bloque $b$ del descriptor (sección 5.8) y cada registro $r$,

$$m_b(r) = \begin{cases} 1 & \text{si el valor anotado no pertenece a } N_k,\\ 0 & \text{en caso contrario.} \end{cases} \tag{5.3}$$

Una celda vacía también apaga el bloque; la condición B8 de la sección 5.4.1 excluye ese caso de una versión congelada.

**La máscara es un juicio, no un dato fijo [E].** En la re-anotación ciega del lote 1, la frontera entre «se observa» y «no se observa» cambió en 6 de 30 piezas para la composición y en 6 de 30 para la simetría (capítulo 4, sección 4.9.2). La máscara es, por tanto, una fuente de variabilidad del descriptor. Se declara entre las amenazas a la validez y no se oculta tras la formalización.

### 5.4.1 Condiciones de buena formación de la anotación

Las definiciones de este capítulo presuponen que la anotación cumple ciertas condiciones. Si alguna falla, el descriptor sigue calculándose, pero deja de significar lo que el capítulo dice. Por eso se enuncian aquí y se contrastan con la anotación congelada v2.1 (150 piezas). La columna «Control» indica si la condición la impone una regla automática o si se cumple por la práctica de anotación y se verificó al congelar.

| | Condición | Por qué la necesita el capítulo | Control | Incumplen en v2.1 |
|---|---|---|---|---|
| B1 | Todo valor pertenece al vocabulario del atributo o es un estado admitido, y un estado ocupa la celda completa | Definición 5.4 | Regla de validación | 0 |
| B2 | `eje_bandas` y `secuencia_bandas` concuerdan: las dos registran bandas o las dos un estado | Definición 5.9 | Regla de validación | 0 |
| B3 | Si las dos son un estado, es el mismo | Evita que una pieza sea `ausente` en una y `no_observable` en la otra | Verificación al congelar | 0 |
| B4 | Una palabra contiene al menos un símbolo de $\Sigma$: no está formada solo por lagunas | Si no, $\tilde{w} = \varepsilon$ y «no se ve ninguna banda» se compararía como «no tiene bandas» ($d_w = 0$ frente a `ausente`), contra la sección 5.4 | Verificación al congelar | 0 |
| B5 | No hay dos lagunas contiguas | Un tramo perdido es una sola laguna; así los tramos de la definición 5.10 son únicos | Verificación al congelar | 0 |
| B6 | Si `composicion` es `bandas`, la secuencia no es `ausente` | Los dos atributos no pueden afirmar y negar las bandas a la vez | Verificación al congelar | 0 |
| B7 | `motivos` es `ausente` si y solo si `familia_iconografica` lo es | Coherencia entre los dos bloques iconográficos | Verificación al congelar | 0 |
| B8 | Ningún atributo del descriptor está vacío | Una celda vacía apaga el bloque sin que conste un juicio de no observación | Aviso de validación | 0 |
| B9 | Ninguna corrección de la revisión de criterios se aplica sin la firma del anotador | Una propuesta automática sin verificar no es anotación (capítulo 4, sección 4.10) | Condición de la congelación | 0 pendientes |
| B10 | La anotación describe la imagen de su registro | Definición 5.1: $a(r)$ es lo observado en $f(r)$ | Revisión manual de la identidad de las imágenes | 0 (ocho anotaciones desplazadas se trasladaron a su registro antes de congelar) |

Las condiciones B3 a B7 se cumplen en la versión congelada, pero no las protege una regla automática: una versión posterior de la anotación debería convertirlas en errores de validación antes de modificar valores.

**Casos admitidos, que no son errores.** Cuatro situaciones son legítimas con las definiciones adoptadas y se declaran para que no se confundan con incoherencias. En la versión 2.1, 53 piezas tienen palabra de bandas, 83 la tienen `ausente` y 14 no la tienen observada (11 `no_observable` y 3 `desconocido`):

| Caso | Piezas | Tratamiento |
|---|---|---|
| Palabra de una sola banda | 5 de 53 | Admitida. El bloque de adyacencias no es observable para esa pieza, y $d_w$ frente a otra palabra de una banda solo vale 0 o 1 |
| Dos bandas contiguas del mismo tipo | 21 de 53 | Admitida: una banda se delimita por un cambio de color **o** de diseño (definición 5.6), y la palabra no registra el color. La palabra no se comprime; su longitud cuenta bandas, no cambios de tipo |
| Palabra en una pieza cuya composición no es `bandas` | 19 de 53 | Admitida: una pieza de paneles o de campo central puede tener además franjas que cruzan la superficie (capítulo 4, sección 4.7.3) |
| Símbolo `no_determinada` en una palabra | 2 de 53 (3 símbolos) | Admitido como categoría residual (sección 5.4) |

Las palabras tienen entre 1 y 14 símbolos; la mitad tiene 3 o menos.

**Lagunas.** Ninguna de las 53 palabras de la versión 2.1 contiene una laguna. El tratamiento de las lagunas (definiciones 5.8 y 5.10) está definido y probado con casos sintéticos, pero **no se ejerce en el núcleo**, y no se presenta como algo evaluado.

## 5.5 La palabra de bandas

**Definición 5.6 (banda) [D].** Una banda es una franja que atraviesa toda la superficie visible en sentido perpendicular al eje de lectura y está delimitada por un cambio de color o de diseño. No son bandas las cenefas perimetrales (se registran en `borde`), las filas o columnas de una retícula ni los paneles (se registran en `composicion`). La composición dominante no decide si hay bandas: una pieza de paneles o de campo puede tener franjas que la cruzan de lado a lado.

**Definición 5.7 (alfabeto) [D].**

$$\Sigma = \{\text{lisa} < \text{geométrica} < \text{figurativa} < \text{mixta} < \text{no determinada}\}, \qquad k = \lvert\Sigma\rvert = 5. \tag{5.4}$$

Cada símbolo es un **tipo** de banda. No codifica color ni anchura. El orden total es convencional y solo sirve para definir la forma canónica.

**Definición 5.8 (laguna).** El símbolo $\bot \notin \Sigma$ marca un tramo que no puede observarse (pérdida, pliegue, encuadre). No es un tipo de banda.

**Definición 5.9 (palabra).** La palabra de una pieza es

$$w = w_1 w_2 \cdots w_l \in (\Sigma \cup \{\bot\})^{*}, \tag{5.5}$$

leída a lo largo del eje registrado en `eje_bandas`, con al menos un símbolo de $\Sigma$ (condición B4). Se almacena en `secuencia_bandas` con los símbolos separados por ` > `. La palabra vacía $\varepsilon$ no se escribe: corresponde al estado `ausente`, es decir, la pieza se observó y no tiene bandas. Dos símbolos contiguos pueden ser iguales (sección 5.4.1).

**Definición 5.10 (tramos y palabra sin lagunas).** Los tramos de $w$ son sus subpalabras maximales sin lagunas. La palabra sin lagunas, $\tilde{w} \in \Sigma^{*}$, es la concatenación de sus tramos en orden (`tramos`, `sin_lagunas`).

*Nota sobre las lagunas* **[D]**. Al concatenar los tramos, $\tilde{w}$ pone en contacto dos bandas que en la pieza están separadas por un tramo perdido. La distancia entre palabras (sección 5.8.1) trabaja sobre $\tilde{w}$ y acepta esa aproximación; el histograma de adyacencias (sección 5.8.2) no la acepta, y cuenta los pares solo dentro de cada tramo. Con la condición B4, $\tilde{w} \neq \varepsilon$ para toda palabra anotada, y la palabra vacía queda reservada a `ausente`.

## 5.6 Equivalencia por reversión y forma canónica

**Definición 5.11 (reversión) [D].** Sea $\rho$ la aplicación que invierte una palabra: $\rho(w_1 \cdots w_l) = w_l \cdots w_1$. Como $\rho \circ \rho = \mathrm{id}$, el conjunto $C_2 = \{e, \rho\}$ es un grupo que actúa sobre $\Sigma^{*}$. Dos palabras son **equivalentes** si están en la misma órbita:

$$w \sim v \iff v \in \{w, \rho(w)\}. \tag{5.6}$$

No se incluye ninguna otra transformación. La rotación de 90° no conserva el dominio (la palabra se lee sobre un solo eje). La permutación de tipos destruiría la información que el alfabeto registra. El desplazamiento cíclico supondría una banda circular, que el corpus no justifica. El primer avance (ecuaciones 5.44–5.46) proponía un grupo $G$ genérico con reflexiones, rotaciones, traslaciones y simetrías de friso sin definir su acción; aquí el grupo y su acción quedan fijados.

**Definición 5.12 (forma canónica).**

$$c(w) = \min\nolimits_{\text{lex}} \{w, \rho(w)\}, \tag{5.7}$$

con el orden lexicográfico inducido por el orden de $\Sigma$.

**Proposición 5.1 [P].** Para toda $w, v \in \Sigma^{*}$:

1. *Invariancia:* $c(\rho(w)) = c(w)$.
2. *Completitud:* $c(w) = c(v)$ si y solo si $w \sim v$.
3. *Costo:* $c(w)$ se calcula en $O(l)$.

*Demostración.* (1) $\{\rho(w), \rho(\rho(w))\} = \{\rho(w), w\}$, y el mínimo de un mismo conjunto es único. (2) Si $w \sim v$, las órbitas coinciden y por (1) también sus mínimos. Recíprocamente, $c(w)$ pertenece a la órbita de $w$ y $c(v)$ a la de $v$; si son iguales, las órbitas comparten un elemento y, al ser clases de equivalencia, coinciden. (3) Invertir y comparar dos palabras de longitud $l$ requiere $O(l)$ operaciones. $\blacksquare$

**Observación 5.1 (palíndromos y simetría bilateral).** Los puntos fijos de $\rho$ son los palíndromos: $\rho(w) = w$. Una palabra es un palíndromo exactamente cuando la secuencia de **tipos** de banda es simétrica respecto de la línea media perpendicular al eje de lectura. El palíndromo es, pues, la contraparte formal de una disposición bilateral de las bandas [verificar: Cereceda, 1978, para la disposición de las listas en las talegas de Isluga]. La correspondencia es solo a nivel de tipos: dos bandas del mismo tipo pueden diferir en color o en anchura, que la palabra no registra.

## 5.7 Enumeración: cuánta información puede portar el orden

Los resultados de esta sección son conocidos. Su papel en la tesis es acotado: cuantifican cuántas configuraciones distingue la codificación elegida, y en particular cuántas distingue el orden más allá del inventario de tipos. No prueban originalidad ni rendimiento.

**Teorema 5.1 (lema de conteo de órbitas) [T].** Sea $G$ un grupo finito que actúa sobre un conjunto finito $X$. El número de órbitas es

$$\lvert X / G \rvert = \frac{1}{\lvert G \rvert} \sum_{g \in G} \lvert \mathrm{Fix}(g) \rvert, \qquad \mathrm{Fix}(g) = \{x \in X : g \cdot x = x\}. \tag{5.8}$$

Se conoce como lema de Burnside, aunque el resultado es anterior y se debe a Cauchy y a Frobenius (Burnside, 1897; Frobenius, 1887; Neumann, 1979) [verificar: citas exactas].

**Corolario 5.1 [T].** El número de formas canónicas de longitud $l$ sobre $k$ símbolos es

$$N(k, l) = \frac{k^{l} + k^{\lceil l/2 \rceil}}{2}. \tag{5.9}$$

*Demostración.* Se aplica (5.8) con $X = \Sigma^{l}$ y $G = C_2$. La identidad fija las $k^{l}$ palabras. La reversión fija los palíndromos, que quedan determinados por sus primeras $\lceil l/2 \rceil$ letras. $\blacksquare$

Con $k = 2$ y $l = 4$: $(16 + 4)/2 = 10$. Con el alfabeto del descriptor ($k = 5$) y cuatro bandas: $(625 + 25)/2 = 325$. Una prueba automática enumera las órbitas con la función de forma canónica y las compara con (5.9) para $k \in \{2, 3, 5\}$ y $l \le 5$.

**Corolario 5.2 (formas canónicas con un contenido dado) [T].** Sea $(n_1, \dots, n_k)$ el contenido de una palabra: el número de bandas de cada tipo, con $\sum_i n_i = l$. Las palabras con ese contenido son

$$M = \frac{l!}{n_1! \cdots n_k!}, \tag{5.10}$$

y de ellas son palíndromos

$$P = \begin{cases} \dfrac{\lfloor l/2 \rfloor!}{\lfloor n_1/2 \rfloor! \cdots \lfloor n_k/2 \rfloor!} & \text{si a lo sumo un } n_i \text{ es impar},\\[2ex] 0 & \text{en caso contrario.} \end{cases} \tag{5.11}$$

El número de formas canónicas con ese contenido es $(M + P)/2$.

*Demostración.* El conjunto de palabras con un contenido fijo es invariante por $\rho$, de modo que (5.8) se aplica a ese conjunto. Un palíndromo queda determinado por su primera mitad, que contiene $\lfloor n_i/2 \rfloor$ letras de cada tipo; si hay un $n_i$ impar, esa letra ocupa el centro, y si hay más de uno no existe palíndromo. $\blacksquare$

Es el caso más simple del teorema de enumeración de Pólya (1937) [verificar: cita exacta], que generaliza el conteo de órbitas a configuraciones con un contenido prescrito. Para $C_2$ el conteo es directo y no requiere el índice de ciclos.

**Ejemplo 5.1.** Con dos bandas de cada uno de dos tipos: $M = 6$, $P = 2$ (`abba` y `baab`) y, por tanto, 4 formas canónicas: `aabb`, `abab`, `abba`, `baab`. Las cuatro comparten inventario de tipos. Un descriptor sin orden las confunde; el descriptor con orden las separa.

**Alcance de estos resultados.** El cociente entre (5.9) y el número de contenidos posibles mide cuánta información *puede* portar el orden bajo la codificación elegida. No dice que esa información sea útil para recuperar piezas (H2 **[E]**), ni que el diseño andino se conciba como palabras bajo reversión, cuestión que queda fuera de la tesis. Tampoco describe el corpus: cuántas piezas de la galería comparten contenido y difieren en forma canónica es un dato empírico, que se informa en la sección 5.13.

## 5.8 Distancias por bloque

El descriptor de un registro es la tupla de sus bloques. Cada bloque $b$ tiene una distancia $d_b$ con valores en $[0, 1]$, definida solo cuando el bloque es observable en las dos piezas.

| Bloque | Atributo de la anotación | Distancia $d_b$ | Sección |
|---|---|---|---|
| Composición | `composicion` | Nominal | 5.8.4 |
| Bandas | `secuencia_bandas` | $d_w$ | 5.8.1 |
| Adyacencias | derivado de `secuencia_bandas` | $d_h$ | 5.8.2 |
| Borde | `borde` | Nominal | 5.8.4 |
| Centro | `centro` | Nominal | 5.8.4 |
| Simetría | `simetria` | Nominal | 5.8.4 |
| Repetición | `repeticion` | Ordinal | 5.8.4 |
| Motivos | `motivos` | Jaccard | 5.8.4 |
| Familia iconográfica | `familia_iconografica` | Nominal | 5.8.4 |

**Exclusiones [D].** El color no forma parte del descriptor, para que una ganancia de M3 no pueda ser de origen cromático (el color ya está representado en M1 y M2). El motivo principal tampoco, por ser la categoría más incierta de la anotación. El eje de las bandas queda fuera por la razón expuesta en la sección 5.2.

### 5.8.1 Distancia entre palabras

Sea $\mathrm{lev}(x, y)$ la distancia de Levenshtein (1966): el número mínimo de inserciones, eliminaciones y sustituciones de un símbolo que transforman $x$ en $y$. Es una métrica en $\Sigma^{*}$ y se calcula en $O(\lvert x \rvert \cdot \lvert y \rvert)$ por programación dinámica (Wagner y Fischer, 1974) **[T]** [verificar: citas exactas].

**Lema 5.1 (la reversión es una isometría) [P].** Para toda $x, y \in \Sigma^{*}$, $\mathrm{lev}(\rho(x), \rho(y)) = \mathrm{lev}(x, y)$.

*Demostración.* Una sucesión de operaciones de edición que lleva $x$ a $y$ se convierte, aplicando cada operación en la posición reflejada, en una sucesión del mismo número de operaciones que lleva $\rho(x)$ a $\rho(y)$. La correspondencia es biyectiva porque $\rho$ es una involución; luego los mínimos coinciden. $\blacksquare$

**Proposición 5.2 (métrica entre órbitas, sin normalizar) [P].** La función

$$\delta(w, v) = \min\{\mathrm{lev}(w, v),\ \mathrm{lev}(w, \rho(v))\} \tag{5.12}$$

es una métrica en el conjunto de órbitas $\Sigma^{*}/C_2$: es simétrica, satisface la desigualdad triangular y $\delta(w, v) = 0$ si y solo si $w \sim v$.

*Demostración.* Por el lema 5.1, $\mathrm{lev}(w, \rho(v)) = \mathrm{lev}(\rho(w), v)$, de donde $\delta$ es simétrica y no depende del representante elegido en cada órbita. $\delta(w, v) = 0$ equivale a $v = w$ o $\rho(v) = w$. Para la desigualdad triangular, sean $g, g' \in C_2$ tales que $\delta(x, y) = \mathrm{lev}(x, g y)$ y $\delta(y, z) = \mathrm{lev}(y, g' z)$. Por el lema 5.1, $\mathrm{lev}(g y, g g' z) = \mathrm{lev}(y, g' z)$. Entonces

$$\delta(x, z) \le \mathrm{lev}(x, g g' z) \le \mathrm{lev}(x, g y) + \mathrm{lev}(g y, g g' z) = \delta(x, y) + \delta(y, z). \qquad \blacksquare$$

**Definición 5.13 (distancia normalizada entre palabras) [D].** Para dos palabras $w, v$ con palabras sin lagunas $\tilde{w}, \tilde{v}$,

$$d_w(w, v) = \frac{\delta(\tilde{w}, \tilde{v})}{\max(\lvert \tilde{w} \rvert, \lvert \tilde{v} \rvert)}, \qquad d_w(\varepsilon, \varepsilon) = 0. \tag{5.13}$$

La normalización hace comparables piezas con distinto número de bandas y lleva el bloque a la escala $[0, 1]$ que exige la disimilitud mixta. Su costo se declara en la proposición siguiente.

**Proposición 5.3 [P].** Para toda $w, v$:

1. *Rango:* $d_w(w, v) \in [0, 1]$. Una palabra vacía frente a una no vacía está a distancia 1.
2. *Simetría:* $d_w(w, v) = d_w(v, w)$.
3. *Invariancia:* $d_w(\rho(w), v) = d_w(w, \rho(v)) = d_w(w, v)$.
4. *Identidad en las órbitas:* $d_w(w, v) = 0$ si y solo si $\tilde{w} \sim \tilde{v}$.
5. *Costo:* $O(\lvert \tilde{w} \rvert \cdot \lvert \tilde{v} \rvert)$.

*Demostración.* (1) $\mathrm{lev}(x, y) \le \max(\lvert x \rvert, \lvert y \rvert)$: basta sustituir las posiciones comunes y luego insertar o eliminar las restantes. Si $x = \varepsilon$ e $y \neq \varepsilon$, $\mathrm{lev} = \lvert y \rvert$. (2)–(4) se siguen de la proposición 5.2, porque el denominador es simétrico e invariante por $\rho$, y $\rho$ conmuta con la eliminación de lagunas salvo reversión: $\widetilde{\rho(w)} = \rho(\tilde{w})$. (5) Dos ejecuciones del algoritmo de Wagner y Fischer. $\blacksquare$

**Proposición 5.4 ($d_w$ no es una métrica) [P].** La distancia normalizada (5.13) no satisface la desigualdad triangular.

*Contraejemplo.* Sean $x = \texttt{aab}$, $y = \texttt{aaba}$, $z = \texttt{aba}$. Entonces $d_w(x, y) = 1/4$, $d_w(y, z) = 1/4$ y $d_w(x, z) = 2/3 > 1/2$. $\blacksquare$

El fenómeno es conocido: las normalizaciones simples de la distancia de edición por la longitud pierden la desigualdad triangular, y existen normalizaciones alternativas que la conservan (Marzal y Vidal, 1993; Yujian y Bo, 2007) [verificar: citas exactas]. Aquí se mantiene la normalización por la longitud mayor porque es la más legible («fracción de bandas que hay que cambiar») y porque el método no usa la desigualdad triangular en ningún paso (sección 5.9). Si un trabajo posterior necesitara la garantía métrica (índices métricos, agrupamiento), dispone de $\delta$ sin normalizar (proposición 5.2).
### 5.8.2 Adyacencias

**Definición 5.14 [D].** $h(w)$ es el histograma normalizado de los pares **no ordenados** $\{w_j, w_{j+1}\}$ de símbolos contiguos dentro de cada tramo de $w$. Una laguna no forma pares. La distancia es

$$d_h(w, v) = \tfrac{1}{2} \lVert h(w) - h(v) \rVert_1 \in [0, 1], \tag{5.14}$$

la distancia de variación total entre dos distribuciones. Si alguna de las dos palabras no tiene ningún par (cero o una banda por tramo), el bloque no es observable **para ese par de piezas**: la observabilidad de este bloque depende del par, y no solo de cada pieza.

**Proposición 5.5 [P].** $h(\rho(w)) = h(w)$; por tanto, $d_h$ es invariante a la reversión en ambos argumentos.

*Demostración.* $\rho$ transforma cada par contiguo $(w_j, w_{j+1})$ en el par $(w_{j+1}, w_j)$ dentro del mismo tramo; como par no ordenado es el mismo. $\blacksquare$

Se eligen pares no ordenados precisamente para obtener esta invariancia sin fijar un sentido de lectura.

**Observación 5.2 (adyacencias y palabra no son redundantes).** `aabb` y `abab` tienen el mismo histograma de tipos y distintas adyacencias: $h(\texttt{aabb})$ reparte su masa por igual entre $\{a,a\}$, $\{a,b\}$ y $\{b,b\}$, y $h(\texttt{abab})$ la concentra en $\{a,b\}$. A la inversa, las adyacencias no determinan la palabra: `aabab` y `abaab` tienen el mismo histograma de adyacencias y formas canónicas distintas. Los dos bloques miden aspectos diferentes del orden: el primero, la secuencia completa; el segundo, la vecindad local.

El primer avance (ecuaciones 5.40–5.43) proponía una matriz de adyacencia $A \in \{0,1\}^{k \times k}$ de combinaciones «permitidas» y el conteo $\mathbf{1}^{\top} A^{n-1} \mathbf{1}$. Se retira: identificaba «no observado» con «no permitido», lo cual no puede sostenerse con un corpus finito, y no interviene en el método. El descriptor no prescribe qué vecindades son admisibles; describe cuáles se observan en cada pieza.

### 5.8.3 Control sin orden

**Definición 5.15 (M3-sin-orden) [D].** Sea $t(w)$ el histograma normalizado de los tipos de $\tilde{w}$. El control sustituye $d_w$ por

$$d_t(w, v) = \tfrac{1}{2} \lVert t(w) - t(v) \rVert_1, \tag{5.15}$$

con $d_t(\varepsilon, \varepsilon) = 0$ y $d_t = 1$ si exactamente una de las dos palabras es vacía, y omite el bloque de adyacencias. Usa los mismos pesos, sin reajustarlos. Es la única diferencia con M3.

**Proposición 5.6 (el control acota inferiormente a la distancia con orden) [P].** Para toda $w, v$,

$$d_t(w, v) \le d_w(w, v). \tag{5.16}$$

En particular, $d_w(w, v) = 0$ implica $d_t(w, v) = 0$, y el recíproco es falso.

*Demostración.* Si alguna palabra es vacía, ambas distancias valen lo mismo (0 o 1). En otro caso, sean $x = \tilde{w}$, $y = \tilde{v}$ con $m = \lvert x \rvert \le n = \lvert y \rvert$, y sean $a_s, b_s$ el número de apariciones del símbolo $s$ en $x$ e $y$. En un alineamiento óptimo, cada posición de $y$ está emparejada con un símbolo igual de $x$ o cuesta al menos una operación; el número de emparejamientos iguales es a lo sumo $\sum_s \min(a_s, b_s)$. Luego $\mathrm{lev}(x, y) \ge n - \sum_s \min(a_s, b_s)$. Por otra parte, $d_t = 1 - \sum_s \min(a_s/m, b_s/n)$ y, como $m \le n$, $\min(a_s/m, b_s/n) \ge \min(a_s, b_s)/n$. Por tanto $d_t \le 1 - \sum_s \min(a_s, b_s)/n \le \mathrm{lev}(x, y)/n$. El mismo argumento vale para $\rho(y)$, que tiene los mismos conteos; luego $d_t \le \delta(x, y)/n = d_w$. El recíproco falla con `aabb` y `abab`: $d_t = 0$ y $d_w = 1/2$. $\blacksquare$

*Interpretación.* M3 **refina** a su control: todo lo que el control distingue, M3 lo distingue al menos en la misma medida, y M3 separa además pares que el control confunde. Esto es lo que autoriza a leer una diferencia entre M3 y M3-sin-orden como efecto del orden (junto con las adyacencias) y no del inventario de tipos. Que ese refinamiento mejore la recuperación es H2 **[E]**.

*Estado de la verificación.* La proposición se demuestra aquí y se comprobó por enumeración exhaustiva con la implementación (alfabeto de tres símbolos, longitudes 0 a 5: 132 496 pares, ninguna violación), pero todavía no está fijada en una prueba automática, a diferencia de las demás propiedades **[P]**.

### 5.8.4 Bloques nominales, ordinal y de conjunto

- **Nominal** (`composicion`, `borde`, `centro`, `simetria`, `familia_iconografica`): $d_b = 0$ si los valores coinciden y 1 si no (`nominal`). Los valores de ausencia observada ($Z_k$ en la tabla de la sección 5.4: `no`, `no_evidente`, `ausente`) son un valor más: dos piezas sin borde coinciden en ese bloque.
- **Ordinal** (`repeticion`, con el orden no < parcial < sí): $d_b = \lvert \mathrm{rango}(u) - \mathrm{rango}(v) \rvert / 2$.
- **Conjunto** (`motivos`): distancia de Jaccard (1912) [verificar: cita exacta], $d_b(X, Y) = 1 - \lvert X \cap Y \rvert / \lvert X \cup Y \rvert$, con $d_b(\varnothing, \varnothing) = 0$. Es una métrica en los conjuntos finitos **[T]**.

Todas toman valores en $[0, 1]$, son simétricas y se anulan cuando los valores coinciden.

**Simetría y repetición como atributos anotados [D].** La simetría se registra con las categorías de la tesis (Cuadro 6.4 del primer avance), separadas por la dimensión de la repetición (capítulo 4, sección 4.7.4): `traslacional` cuando un motivo se desplaza en una sola dirección y forma un friso; `repeticion_modular` cuando un módulo con contorno propio se repite como unidad en dos dimensiones. No se calcula ningún grupo de simetría a partir de la imagen. La repetición es un atributo ordinal anotado. El periodo fundamental $p^{*}$ del primer avance (ecuaciones 5.35–5.39) se retira del capítulo: el descriptor no lo usa. La implementación conserva una función informativa de periodo que no interviene en la disimilitud; calcular un periodo sobre la palabra de bandas, con soporte mínimo y tratamiento de lagunas, queda como extensión.

## 5.9 Disimilitud mixta

**Definición 5.16.** Sean $\lambda_b \ge 0$ los pesos de los bloques, iguales en la configuración inicial, y

$$B(i, j) = \{\, b : m_b(i) = m_b(j) = 1,\ d_b(i, j) \text{ definida},\ \lambda_b > 0 \,\} \tag{5.17}$$

el conjunto de bloques comparables para el par $(i, j)$. Si $B(i, j) \neq \varnothing$,

$$D(i, j) = \frac{\sum_{b \in B(i,j)} \lambda_b\, d_b(i, j)}{\sum_{b \in B(i,j)} \lambda_b}. \tag{5.18}$$

$D$ pertenece a la familia del coeficiente general de Gower (1971) [verificar: cita exacta] para datos mixtos con valores faltantes: cada variable aporta una puntuación en $[0, 1]$ en su propia escala, y las variables no comparables para un par se excluyen del numerador y del denominador. La diferencia es que aquí dos de las «variables» son estructuradas (una palabra y un histograma) y tienen distancias propias **[T, D]**.

**Ausencia de evidencia [D].** Si $B(i, j) = \varnothing$, $D$ no está definida. El par queda «sin evidencia estructural»: no recibe similitud máxima ni mínima, y en el ranking de M3 se ubica después de todos los candidatos con evidencia, ordenado por identificador.

**Definición 5.17 (cobertura).**

$$\kappa(i, j) = \frac{\sum_{b \in B(i,j)} \lambda_b}{\sum_{b} \lambda_b} \in [0, 1]. \tag{5.19}$$

Se informa junto con $D$. Una disimilitud calculada sobre un solo bloque y otra calculada sobre nueve no tienen el mismo respaldo, y la cobertura lo hace visible.

**Definición 5.18 (ranking de M3).** Para una consulta $q$, los candidatos con evidencia se ordenan por $D(q, \cdot)$ ascendente; los empates se resuelven por identificador ascendente. El ranking es, por tanto, determinista. La puntuación que M3 entrega a la fusión es $s_{M3} = 1 - D$.

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

El fallo tiene dos orígenes independientes: la máscara variable (este contraejemplo) y la normalización de $d_w$ (proposición 5.4). Tampoco se afirma que $1 - D$ sea un núcleo semidefinido positivo: es sabido que esa propiedad del coeficiente de Gower no está garantizada cuando hay valores faltantes (Gower, 1971) [verificar: página].

**Consecuencia para el método.** $D$ es una **disimilitud**, no una distancia métrica. El método solo ordena candidatos por $D$ para cada consulta. No usa índices métricos, agrupamiento, inmersión ni núcleos, de modo que ningún paso depende de las propiedades que no se cumplen. Una prueba automática fija los dos contraejemplos, para que no pueda afirmarse lo contrario sin que la prueba falle. Con esto se sustituye la similitud coseno sobre un vector de conteos del primer avance (ecuaciones 5.58–5.60), que mezclaba escalas sin máscara.

## 5.10 Fusión tardía

**Espacios separados [D].** Cada sistema opera en su propio espacio: M0, en los términos de la ficha; M2, en el espacio de embeddings de OpenCLIP; M3, en el espacio de descriptores. **No se combinan representaciones** ni se supone alineación alguna entre esos espacios. La ecuación 5.66 del primer avance sumaba un embedding visual y un vector combinatorio; se retira, porque la suma exige la misma dimensión y un espacio compatible, y ninguna de las dos condiciones se cumple. La fusión es tardía y actúa sobre puntuaciones.

**Definición 5.19 (normalización por consulta).** Para una consulta $q$, un componente $c \in \{\text{M0}, \text{M2}, \text{M3}\}$ y un candidato $i$ con puntuación $s_c(q, i)$,

$$\hat{s}_c(q, i) = \frac{s_c(q, i) - \min_{i'} s_c(q, i')}{\max_{i'} s_c(q, i') - \min_{i'} s_c(q, i')}, \tag{5.20}$$

con mínimo y máximo sobre los candidatos que tienen valor. Si todos coinciden, $\hat{s}_c = 0$ para todos: el componente no ordena esa consulta.

**Definición 5.20 (fusión).** Sea $C(q, i)$ el conjunto de componentes con evidencia para el par y $\alpha_c \ge 0$ los pesos. Entonces

$$s(q, i) = \sum_{c \in C(q,i)} \alpha'_c\, \hat{s}_c(q, i), \qquad \alpha'_c = \frac{\alpha_c}{\sum_{c' \in C(q,i)} \alpha_{c'}}. \tag{5.21}$$

Es una combinación convexa de puntuaciones normalizadas, la forma de fusión que Bruch et al. (2023) analizan frente a la fusión por posiciones. Su análisis cubre la fusión de dos sistemas; la extensión a tres componentes y el ajuste de los pesos con diez consultas de desarrollo no tienen respaldo cuantitativo en ese trabajo (capítulo 3, sección 3.7).

**Proposición 5.9 [P].**

1. *Rango.* $s(q, i) \in [0, 1]$.
2. *Descomposición exacta.* Las contribuciones $\alpha'_c\, \hat{s}_c$ suman $s$.
3. *Intervención.* Retirar un componente equivale a declararlo sin evidencia para todos los candidatos; los pesos restantes se renormalizan.
4. *Sin evidencia estructural.* Un par sin evidencia en M3 no recibe la puntuación máxima ni mínima de M3: su peso se reparte entre los demás componentes en proporción a sus pesos.
5. *Invariancia afín.* $\hat{s}_c$ no cambia si $s_c$ se sustituye por $a\, s_c + b$ con $a > 0$, para una misma consulta. En particular, usar $1 - D$ o $-D$ como puntuación de M3 produce la misma fusión.
6. *Dependencia del conjunto de candidatos.* $\hat{s}_c$ depende del mínimo y del máximo de la consulta. La puntuación de un par no es comparable entre consultas y solo se usa para ordenar dentro de cada una.

*Demostración.* (1) y (2): $s$ es una combinación convexa de valores en $[0, 1]$, y la suma de sus términos es $s$ por definición. (3) y (4) son la definición de $C(q, i)$ y de $\alpha'_c$. (5) La transformación afín positiva se cancela en (5.20). (6) Es inmediato de (5.20). $\blacksquare$
Las propiedades 2 y 3 son, respectivamente, la primera y la segunda comprobación de H3, y la 3 es además la forma de calcular las ablaciones. Que se cumplan como identidad algebraica no hace trivial a H3: lo que se contrasta en el experimento es que la implementación las satisface en **todos** los resultados de prueba, dentro de una tolerancia numérica fijada de antemano.

**Variante por posiciones recíprocas.** La fusión $\sum_c 1/(60 + r_c)$, con $r_c$ la posición del candidato en el ranking del componente $c$ (Cormack, Clarke y Büttcher, 2009), no tiene pesos y no conserva la descomposición. Se implementa como comparación exploratoria y no interviene en H3.

**Relación con los modelos de cuello de botella de conceptos.** El marco más cercano es el de Koh et al. (2020): la decisión pasa por conceptos legibles. La diferencia es que allí los conceptos se predicen desde la imagen y aquí los anota una persona. M4 es aditivo y produce su propia explicación (Rudin, 2019); lo que H3 comprueba es su fidelidad, no su plausibilidad (Jacovi y Goldberg, 2020).

## 5.11 Costo computacional

Sea $n = \lvert \mathcal{C}(q) \rvert$ el número de candidatos de una consulta, $\lvert B \rvert$ el número de bloques y $L$ la longitud máxima de una palabra de bandas en la galería.

| Operación | Costo |
|---|---|
| Forma canónica de una palabra | $O(L)$ |
| Histogramas de tipos y de adyacencias | $O(L)$ |
| Distancia entre dos palabras | $O(L^2)$ |
| Disimilitud de un par | $O(\lvert B \rvert + L^2)$ |
| Ranking de una consulta en M3 | $O(n\,(\lvert B \rvert + L^2) + n \log n)$ |
| Fusión de una consulta | $O(n)$ por componente, más la ordenación |

Con una galería de unos cientos de piezas y palabras de pocas decenas de símbolos, el costo es despreciable frente al cálculo de embeddings de M2. No se hace ninguna afirmación de escalabilidad a colecciones grandes: sin desigualdad triangular no pueden usarse índices métricos, y la comparación es exhaustiva. Es una consecuencia directa de la proposición 5.8.

## 5.12 Qué es cada cosa

| Naturaleza | Enunciados |
|---|---|
| **[T]** Resultados conocidos | Lema de conteo de órbitas y enumeración de Pólya; distancia de Levenshtein y su cálculo; distancia de Jaccard; coeficiente de Gower; variación total entre histogramas |
| **[D]** Decisiones de diseño | Codificación de presencia, ausencia y no observación por atributo; categorías residuales; condiciones de buena formación; definición de banda; alfabeto de cinco tipos; el grupo $C_2$ y ninguna otra transformación; tratamiento de las lagunas; pares no ordenados en las adyacencias; normalización por la longitud mayor; exclusión del color, del motivo principal y del eje; simetría y repetición como atributos anotados; pesos iguales de partida; tratamiento del par sin evidencia; fusión tardía con normalización por consulta |
| **[P]** Propiedades demostradas | Invariancia y completitud de la forma canónica (5.1); isometría de la reversión (lema 5.1); métrica entre órbitas sin normalizar (5.2); rango, simetría, invariancia e identidad de $d_w$ (5.3) y su carácter no métrico (5.4); invariancia de $h$ (5.5); cota del control (5.6); propiedades de $D$ (5.7) y contraejemplos (5.8); propiedades de la fusión (5.9) |
| **[E]** Afirmaciones empíricas, sin contrastar | H1, H2 y H3 (sección 5.13); que la anotación y la máscara son estables más allá del lote medido; cuánto distingue el orden en este corpus |

## 5.13 De la formalización a las hipótesis

Las ecuaciones 5.69–5.71 del primer avance enunciaban como relaciones matemáticas lo que son afirmaciones empíricas (por ejemplo, que la similitud híbrida «mejora» a la multimodal). Se sustituyen por las tres hipótesis del protocolo experimental, formuladas sobre resultados observables **[E]**:

- **H1 (primaria).** La diferencia media por consulta de nDCG@10 entre M4 y M2 en la tarea T3 es positiva e igual o superior a 0,03.
- **H2 (mecanismo).** M3 obtiene mejor nDCG@10 que M3-sin-orden, con las mismas consultas, candidatos y pesos.
- **H3 (fidelidad).** En todos los resultados de prueba, la puntuación de M4 coincide con la suma de sus contribuciones y responde a la retirada de un componente como predice (5.21).

Lo que este capítulo aporta a cada una:

| Hipótesis | Lo que el capítulo establece | Lo que solo el experimento puede establecer |
|---|---|---|
| H1 | Que la fusión está bien definida, incluso cuando falta evidencia estructural (5.9) | Que la estructura añade utilidad a un codificador general |
| H2 | Que M3 refina a su control y que la única diferencia entre ambos es el orden (5.6, definición 5.15) | Que ese refinamiento mejora la recuperación |
| H3 | Que la descomposición y la intervención son identidades de la fórmula (5.7, 5.9) | Que la implementación las cumple en todos los resultados de prueba |

**Un dato previo al experimento [E].** El margen que tiene H2 en este corpus puede medirse sin ningún juicio de relevancia. En la anotación v2.1, solo 53 de las 150 piezas del núcleo tienen palabra de bandas, y el orden solo puede pesar cuando la consulta y el candidato la tienen. Entre esas 53 piezas hay 1378 pares. En 41 de ellos el control sin orden ve el mismo histograma normalizado de tipos, y en 25 de esos 41 la forma canónica difiere: son los únicos pares en que, en el bloque de bandas, el control da distancia cero y M3 no. Contando bandas en lugar de proporciones, solo 3 pares comparten inventario y difieren en el orden. En el resto de los pares, M3 y su control pueden diferir en grado, porque $d_t \le d_w$ (proposición 5.6), pero rara vez en el orden relativo de los candidatos. Así ocurrió en desarrollo: con los pesos iniciales, M3 y M3-sin-orden produjeron el mismo ranking completo en 8 de las 10 consultas. Si la proporción se repite en prueba, la diferencia pareada de H2 será cero en la mayoría de las consultas y el veredicto más probable será «evidencia insuficiente» por construcción del corpus, no por la calidad del descriptor. El alcance de H2 frente a esta limitación es una decisión pendiente, que debe tomarse antes de abrir el test y sin ver ningún resultado de prueba (capítulo 7).

## 5.14 Límites de la formalización

1. **Es una codificación del investigador.** La palabra de bandas describe lo visible en una fotografía con un alfabeto elegido. No se afirma que el diseño se haya concebido así, ni que las cinco clases del alfabeto correspondan a categorías de quienes tejieron las piezas.
2. **Depende de la anotación.** El descriptor hereda la variabilidad del anotador, incluida la de la máscara (sección 5.4). Hay un solo anotador; el acuerdo medido es intra-anotador. La versión 2.1 combina tres lecturas: la re-anotación en el lote 1, la primera anotación en los lotes 2 a 5 y, sobre esta, las correcciones de la revisión de criterios, que partieron de propuestas automáticas verificadas por el anotador. De las 108 decisiones de esa revisión, 58 coinciden con la propuesta y 50 la modifican, y la revisión cambió al menos un atributo del descriptor en 46 de las 150 piezas, con efectos apreciables en los rankings de M3 (capítulo 4, sección 4.10.1).
3. **La reversión descarta la orientación de la prenda.** Es convencional en un fragmento y no lo es en una prenda con extremos distinguibles.
4. **El eje es fotográfico.** La palabra no depende de él, pero la decisión de qué cuenta como banda sí depende de cómo se muestra la pieza.
5. **La palabra no registra color ni anchura.** Dos piezas con la misma palabra pueden diferir mucho a la vista. Es deliberado (sección 5.8), y limita lo que «similitud estructural» significa aquí.
6. **La estructura no es independiente de la técnica ni de la tradición.** En la faz de urdimbre la banda la fija el urdido, el tapiz deja libre la composición y algunos bordados imitan las bandas tejidas (sección 5.2; Desrosiers, 2013, pp. 480–499). Una similitud estructural alta puede reflejar en parte la pertenencia a una misma técnica o tradición, que un codificador visual también capta. Una ganancia de M3 no se leerá, por sí sola, como evidencia de una gramática estructural independiente del estilo.
7. **No es una métrica.** Sin consecuencias para el método, con consecuencias para su escalabilidad (sección 5.11).
8. **La población es la del corpus.** Lo formalizado se aplica a piezas de tres museos seleccionadas con un criterio que privilegia la legibilidad de colores y figuras. No describe «los textiles andinos».

## 5.15 Correspondencia entre fórmula, implementación y prueba

Cada definición y propiedad del capítulo tiene su contraparte en el código del repositorio de la tesis, y las propiedades **[P]** están fijadas en pruebas automáticas que se ejecutan con cada cambio. El cuadro sirve para auditar esa correspondencia.

| Concepto | Fórmula | Función | Atributo o archivo | Prueba |
|---|---|---|---|---|
| Grupos | Def. 5.2 | `src/grupos/grupos.py` | `grupos_revision_v2.xlsx`; columna `grupo` | `tests/test_grupos.py` |
| Máscara | (5.3) | `valor`, `palabra_de_bandas`, `descriptor` | `[estados]` de `config/vocabulario.toml` | `test_disimilitud_mixta_simetrica_acotada_y_sin_evidencia` |
| Estados y buena formación | (5.2), sec. 5.4.1 | `validar_fila` en `src/anotacion/aplicar_anotaciones_v2.py`; `Campo.invalidos` en `src/utils/vocabulario.py` | `config/vocabulario.toml` | `tests/test_anotacion_v2.py` (B1, B2); B3–B8 verificadas al congelar, sin regla automática |
| Palabra, tramos y lagunas | (5.5), def. 5.10 | `palabra_de_bandas`, `tramos`, `sin_lagunas` | `secuencia_bandas`; símbolo `laguna` | `test_distancia_de_palabras_simetrica_invariante_y_con_lagunas_enmascaradas` |
| Reversión | $\rho$ | `reverso` | `secuencia_bandas` | `test_la_forma_canonica_es_invariante_a_la_reversion` |
| Forma canónica | (5.7) | `canonizar` | `secuencia_bandas` | La anterior |
| Conteo de órbitas | (5.9) | `canonizar` (enumeración) | — | `test_burnside_cuatro_posiciones_dos_simbolos_dan_diez_orbitas`; `test_el_numero_de_formas_canonicas_sigue_la_formula_de_burnside` |
| Contenido y orden | (5.10)–(5.11) | `histograma_tipos`, `canonizar` | `secuencia_bandas` | `test_un_mismo_histograma_de_tipos_reune_varias_formas_canonicas` |
| Distancia entre palabras | (5.12)–(5.13) | `distancia_edicion`, `distancia_palabras` | `secuencia_bandas` | `test_distancia_de_palabras_…`; `test_la_disimilitud_no_es_una_metrica` |
| Adyacencias | (5.14) | `histograma_adyacencias`, `distancia_l1_media` | `secuencia_bandas` | `test_el_control_sin_orden_no_distingue_lo_que_las_adyacencias_si` |
| Control sin orden | (5.15) | `histograma_tipos`; `comparar(..., sin_orden=True)` | `secuencia_bandas` | `test_m3_sin_orden_ignora_el_orden_de_las_bandas` |
| Cota del control | (5.16) | — | — | Sin prueba automática; comprobada por enumeración (sección 5.8.3) |
| Distancias por bloque | Sec. 5.8.4 | `nominal`, `distancias_por_bloque` | Atributos de la tabla de 5.8 | Las de $D$ |
| Disimilitud, cobertura y contribuciones | (5.17)–(5.19) | `comparar` | `[m3.pesos]` de `config/modelos.toml` | `test_disimilitud_mixta_…`; `test_la_suma_de_contribuciones_…` |
| Normalización por consulta | (5.20) | `normalizar` | — | `tests/test_m4.py` |
| Fusión y pesos efectivos | (5.21) | `fusionar`, `pesos_efectivos` | Rejilla del protocolo | `tests/test_m4.py` |
| Posiciones recíprocas | Sec. 5.10 | `posiciones_reciprocas` | — | `tests/test_m4.py` |

Las funciones sin ruta están en `src/modelos/m3_estructura.py` (M3) o en `src/modelos/m4_fusion.py` (fusión); las pruebas sin ruta, en `tests/test_sistemas.py`.

## 5.16 Cambios respecto del primer avance

El primer avance no se corrige. Esta tabla documenta qué ocurre con cada grupo de ecuaciones de su capítulo 5, según el diagnóstico de la auditoría del asesor.

| Ecuaciones del primer avance | Contenido | Destino | Motivo |
|---|---|---|---|
| 5.1–5.3 | Imagen como matriz simbólica | Reemplazadas por las unidades de 5.3 | Imagen y patrón eran objetos distintos sin aplicación definida entre ellos; el descriptor no se extrae de los píxeles |
| 5.4–5.7 | Alfabeto con color, forma, orientación, rol y técnica | Reemplazadas por $\Sigma$ (5.4) y por los bloques | Atributos de escalas y observabilidad distintas en un solo símbolo; la técnica no se asigna por celda |
| 5.8–5.20 | Espacio de configuraciones: 9600 símbolos, $20^{100}$ patrones | Retiradas | Aritmética correcta, pero no son datos observados ni intervienen en el método |
| 5.21–5.23 | $\Omega_{obs} \subseteq \Omega_{plaus}$ | Retiradas | La inclusión de una muestra finita no prueba regularidad cultural |
| 5.24–5.30 | Restricciones | Reemplazadas por la separación entre elegibilidad y estructura (5.3) | Inconsistencia de tipos; exigían bandas y simetría a toda pieza |
| 5.31–5.34 | Motivos y diccionario | Reemplazadas por el bloque de motivos (5.8.4) | Un diccionario por pieza impedía comparar |
| 5.35–5.39 | Bandas y periodo $p^{*}$ | Bandas: 5.5. Periodo: retirado | El descriptor usa la repetición como atributo ordinal anotado |
| 5.40–5.43 | Matriz de adyacencia y conteo $\mathbf{1}^{\top}A^{n-1}\mathbf{1}$ | Reemplazadas por el histograma de adyacencias (5.8.2) | «No observado» no equivale a «prohibido» |
| 5.44–5.46 | Grupo $G$ genérico | Reemplazadas por $C_2$ (5.6) | Acción no definida; varias transformaciones no conservan el dominio |
| 5.47–5.49 | Burnside y Pólya | Conservadas como **[T]**, con una instancia concreta (5.7) | Faltaba una instancia útil; no son prueba de rendimiento |
| 5.50–5.52 | Grafos | Retiradas; trabajo futuro | Fuera del alcance; requieren relaciones tipadas y anotación adicional |
| 5.53–5.57 | Vector de conteos, índice de complejidad, entropía | Retiradas | El índice no tenía interpretación justificada; la entropía de un histograma no mide orden |
| 5.58–5.60 | Similitud coseno y mezcla | Reemplazadas por $D$ (5.9) | Sin máscara ni escalas comunes; la mezcla no es métrica |
| 5.61–5.65 | Codificadores e interfaces | Pasan al capítulo de implementación | Son interfaces, no formalización |
| 5.66 | Suma de embeddings | Retirada | Sin alineación entre espacios |
| 5.67–5.68 | Fusión de puntuaciones | Reemplazadas por (5.20)–(5.21) | Faltaban la normalización y el caso sin evidencia |
| 5.69–5.71 | «Hipótesis» como ecuaciones | Reemplazadas por H1–H3 (5.13) | Son afirmaciones empíricas |
| 5.72–5.73, 5.78 | Diagramas de flujo | Retirados | $\Omega_{obs}$ es una colección, no una transformación de una pieza |
| 5.74–5.77 | Ejemplo con vectores | Reemplazado por los ejemplos 5.1 y de 5.8 | Los ceros confundían ausente con no observado |

## Referencias

Bruch, S., Gai, S., & Ingber, A. (2023). *An analysis of fusion functions for hybrid retrieval* (arXiv:2210.11934v2). arXiv. https://arxiv.org/abs/2210.11934 [verificar: sede]

Chavey, D., Meissen, M., O'Bryan, T., & Terry, G. (2015). Double strip patterns: Between strip patterns and wallpaper patterns. En *Proceedings of Bridges 2015: Mathematics, Music, Art, Architecture, Culture* (pp. 85–92). https://archive.bridgesmathart.org/2015/bridges2015-85.html [verificar: editores]

Cormack, G. V., Clarke, C. L. A., & Büttcher, S. (2009). Reciprocal rank fusion outperforms Condorcet and individual rank learning methods. En *Proceedings of the 32nd International ACM SIGIR Conference on Research and Development in Information Retrieval*. ACM. [verificar: páginas y DOI]

Crowe, D. W. (2001). Symmetries of culture. En *Bridges: Mathematical connections in art, music, and science* (pp. 1–20). https://archive.bridgesmathart.org/2001/bridges2001-1.html [verificar: editores]

Desrosiers, S. (2010). Retour sur « Les techniques de tissage ont-elles un sens ? ». *Techniques & Culture, 54-55*, 260–262. http://journals.openedition.org/tc/5182

Desrosiers, S. (2013). El textil como matriz para el desarrollo de las artes plásticas en los Andes. *Revista Española de Antropología Americana, 43*(2), 477–514. https://doi.org/10.5209/rev_REAA.2013.v43.n2.44020

Desrosiers, S. (2024). Creación textil en los Andes: el lenguaje de los hilos y su transmisión a través del tiempo. En *Arte y saber del textil* (pp. 1–27). Banco de Crédito del Perú. [verificar: editores e ISBN]

Frame, M. (2006a). *Elemental pathways in fiber structures: Approaching Andean symmetry patterns through an ancient technology* [Ponencia]. Textile Society of America 10th Biennial Symposium, Toronto. https://digitalcommons.unl.edu/cgi/viewcontent.cgi?article=1347&context=tsaconf [verificar: número y páginas de las actas]

Helmer, S., & Ngo, V. M. (2015). A similarity measure for weaving patterns in textiles. En *Proceedings of the 38th International ACM SIGIR Conference on Research and Development in Information Retrieval* (pp. 163–172). https://doi.org/10.1145/2766462.2767735

Jacovi, A., & Goldberg, Y. (2020). *Towards faithfully interpretable NLP systems: How should we define and evaluate faithfulness?* (arXiv:2004.03685). arXiv. https://arxiv.org/abs/2004.03685 [verificar: sede]

Koh, P. W., Nguyen, T., Tang, Y. S., Mussmann, S., Pierson, E., Kim, B., & Liang, P. (2020). Concept bottleneck models. En *Proceedings of the 37th International Conference on Machine Learning* (Vol. 119). PMLR. https://arxiv.org/abs/2007.04612 [verificar: páginas]

Liu, Y., Collins, R. T., & Tsin, Y. (2004). A computational model for periodic pattern perception based on frieze and wallpaper groups. *IEEE Transactions on Pattern Analysis and Machine Intelligence, 26*(3), 354–371. https://doi.org/10.1109/TPAMI.2004.1262332

Ngo, V. M., Helmer, S., Le-Khac, N.-A., & Kechadi, M.-T. (2021). Structural textile pattern recognition and processing based on hypergraphs. *Information Retrieval Journal, 24*, 137–173. https://doi.org/10.1007/s10791-020-09384-y

Rudin, C. (2019). *Stop explaining black box machine learning models for high stakes decisions and use interpretable models instead* (arXiv:1811.10154v3). arXiv. https://arxiv.org/abs/1811.10154 [verificar: sede]

**Resultados clásicos citados sin ficha de lectura (verificar la cita exacta):**

Burnside, W. (1897). *Theory of groups of finite order*. Cambridge University Press.

Frobenius, G. (1887). Über die Congruenz nach einem aus zwei endlichen Gruppen gebildeten Doppelmodul. *Journal für die reine und angewandte Mathematik, 101*, 273–299.

Gower, J. C. (1971). A general coefficient of similarity and some of its properties. *Biometrics, 27*(4), 857–871.

Jaccard, P. (1912). The distribution of the flora in the alpine zone. *New Phytologist, 11*(2), 37–50.

Levenshtein, V. I. (1966). Binary codes capable of correcting deletions, insertions, and reversals. *Soviet Physics Doklady, 10*(8), 707–710.

Marzal, A., & Vidal, E. (1993). Computation of normalized edit distance and applications. *IEEE Transactions on Pattern Analysis and Machine Intelligence, 15*(9), 926–932.

Neumann, P. M. (1979). A lemma that is not Burnside's. *The Mathematical Scientist, 4*(2), 133–141.

Pólya, G. (1937). Kombinatorische Anzahlbestimmungen für Gruppen, Graphen und chemische Verbindungen. *Acta Mathematica, 68*, 145–254.

Wagner, R. A., & Fischer, M. J. (1974). The string-to-string correction problem. *Journal of the ACM, 21*(1), 168–173.

Yujian, L., & Bo, L. (2007). A normalized Levenshtein distance metric. *IEEE Transactions on Pattern Analysis and Machine Intelligence, 29*(6), 1091–1095.

**Obras mencionadas y no consultadas en el proyecto:**

Cereceda, V. (1978). Sémiologie des tissus andins: les talegas d'Isluga. *Annales. Économies, Sociétés, Civilisations, 33*(5–6), 1017–1035.

Paul, A. (1997). [verificar: título y sede; el registro localizado en tDAR se titula «Color patterns and aspects of significance in the Paracas Necropolis»].
