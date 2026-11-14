# Formalización de la macroestructura observable y su correspondencia con la implementación

Propuesta al 13 de noviembre de 2026, en respuesta al punto 9 del informe integrado del asesor. Es la base para reescribir el capítulo matemático de la tesis. No introduce ninguna definición nueva en el método: ordena y precisa las de `docs/especificacion_m3.md` y del protocolo experimental, y las vincula con los datos y el código.

Cada enunciado lleva una de estas marcas, para no confundir su naturaleza:

- **[T]** teorema o resultado conocido, que se cita y no se reclama como aporte;
- **[D]** decisión de diseño del investigador, que pudo ser otra;
- **[P]** propiedad del descriptor, demostrada aquí y comprobada por una prueba automática;
- **[E]** afirmación empírica, que solo puede sostenerse con los resultados del experimento. Ninguna se da por establecida en este documento.

## 1. Unidades

Se distinguen cinco objetos que el primer avance trataba de forma indistinta.

| Símbolo | Definición | Dato concreto |
|---|---|---|
| *o* | **Objeto:** el textil físico conservado en un museo. No se observa directamente | No tiene identificador propio en el corpus |
| *r* | **Registro:** la ficha de un museo, con sus metadatos | Fila del consolidado, con clave `id_global` = `FUENTE:id_fuente` |
| *f(r)* | **Fotografía:** la copia de evaluación de la imagen de referencia del registro, de 1600 px de lado mayor | Archivo identificado por su suma SHA-256 en el manifiesto de evaluación |
| *G* | **Grupo:** clase de equivalencia de registros que muestran un mismo objeto o partes de él | Columna `grupo` de `data/metadata/particiones_v2.csv` |
| *a(r)* | **Anotación:** lo que una persona registró al observar *f(r)* | Fila de `data/metadata/anotaciones_v2.csv` |

**Grupos [D].** Sea *R* el conjunto de los 615 registros utilizables y *U* ⊆ *R* × *R* la relación formada por los pares que el investigador decidió unir. Los grupos son las clases de la clausura reflexiva, simétrica y transitiva de *U*, es decir, las componentes conexas del grafo (*R*, *U*). Resultan 577. El grupo es una aproximación al objeto: dos registros de un mismo grupo no se suponen independientes, y por eso el grupo, y no el registro, es la unidad de partición.

**Galería.** 𝒢 ⊂ *R* es el conjunto de los 150 registros con anotación estructural, repartidos en 146 grupos. Para una consulta *q* ∈ 𝒢, los candidatos son 𝒢 menos el grupo de *q*.

**Elegibilidad y estructura son cosas distintas [D].** Que un registro pertenezca a 𝒢 depende de criterios de calidad fotográfica y de curación (el criterio de aptitud v2). Esos criterios definen la población y no forman parte del descriptor. Dentro de 𝒢 no se presupone que una pieza tenga bandas, motivos o simetría observables: cada atributo admite los estados de la sección 2.

## 2. Anotación y observabilidad

Sea *A* el conjunto de atributos estructurales y *V_k* el vocabulario controlado del atributo *k* (`config/vocabulario.toml`). La anotación de un registro asigna a cada atributo un valor de

*V_k* ∪ {`ausente`} ∪ *N*, con *N* = {`no_observable`, `desconocido`}

(en `borde` y `centro`, además, `no_visible` ∈ *N*).

La distinción es sustantiva **[D]**:

- `ausente` es una **observación**: el rasgo podía verse y no está. Se compara como cualquier otro valor.
- Los estados de *N* indican **falta de observación**: la fotografía no permite decidir, o el anotador no pudo hacerlo. No se comparan.

**Máscara.** Para cada bloque *b* del descriptor (sección 5), *m_b(r)* = 1 si el valor anotado no pertenece a *N*, y 0 en caso contrario. En el código, un bloque con máscara 0 se representa con `None` (`valor` y `descriptor` en `src/modelos/m3_estructura.py`).

La máscara no es un dato fijo del objeto, sino el resultado de un juicio. En la re-anotación ciega del lote 1, la frontera entre «se observa» y «no se observa» cambió en 6 de 30 piezas para la composición (`outputs/reports/anotacion_acuerdo_v2.md`, tabla de observabilidad). Es una fuente de variabilidad del descriptor que se declara entre las amenazas a la validez.

## 3. La palabra de bandas

**Banda [D].** Franja que atraviesa toda la superficie visible en sentido perpendicular al eje de lectura y está delimitada por un cambio de color o de diseño. No son bandas las cenefas perimetrales, las filas de una retícula ni los paneles (decisión R12).

**Alfabeto [D].** Σ = {lisa, geométrica, figurativa, mixta, no determinada}, con ese orden total. Cada símbolo es un tipo de banda; no codifica color ni anchura.

**Laguna.** El símbolo ⊥ ∉ Σ marca un tramo que no puede observarse (pérdida, pliegue, encuadre). No es un tipo de banda.

**Palabra.** La palabra de una pieza es *w* = *w₁ w₂ … w_l* ∈ (Σ ∪ {⊥})\*, leída a lo largo del eje registrado en `eje_bandas`. Se almacena en `secuencia_bandas` con los símbolos separados por ` > `. La palabra vacía ε corresponde al estado `ausente`: la pieza se observó y no tiene bandas.

**Tramos.** Los tramos de *w* son sus subpalabras maximales sin lagunas (`tramos`). La palabra sin lagunas, *w̃*, es la concatenación de sus tramos (`sin_lagunas`).

**Eje.** El eje es el de la fotografía, no el de la urdimbre. Una misma organización puede aparecer horizontal o vertical según cómo se montó la pieza para fotografiarla. La palabra no depende del eje; el atributo `eje_bandas` sí refleja la toma, y por eso no forma parte del descriptor.

## 4. Equivalencia por reversión

**Acción del grupo [D].** El sentido de lectura a lo largo del eje es una convención. Se considera el grupo C₂ = {*e*, ρ}, donde ρ invierte la palabra: ρ(*w₁ … w_l*) = *w_l … w₁*. Dos palabras son equivalentes si están en la misma órbita, {*w*, ρ(*w*)}.

Es una simplificación. Para un fragmento, el sentido es arbitrario; para una túnica con abertura de cuello o un manto con cenefa en un solo extremo, la orientación de la prenda existe y aquí se descarta. No se incluyen otras transformaciones: ni la rotación de 90°, ni la permutación de tipos, ni el desplazamiento cíclico.

**Forma canónica [P].** *c*(*w*) = mín_lex {*w*, ρ(*w*)}, con el orden de Σ.

- *Invariancia:* *c*(ρ(*w*)) = *c*(*w*), porque ρ es una involución y {ρ(*w*), ρ(ρ(*w*))} = {*w*, ρ(*w*)}.
- *Completitud:* *c*(*w*) = *c*(*v*) si y solo si *v* ∈ {*w*, ρ(*w*)}. La forma canónica identifica exactamente la órbita.
- *Costo:* O(*l*).
- *Código y prueba:* `canonizar`; `test_la_forma_canonica_es_invariante_a_la_reversion`.

**Número de formas canónicas [T].** Por el lema de Burnside, el número de órbitas de un grupo finito que actúa sobre un conjunto es el promedio del número de elementos que fija cada elemento del grupo. Para palabras de longitud *l* sobre *k* símbolos, la identidad fija las *k^l* palabras y ρ fija los palíndromos, que son *k*^⌈*l*/2⌉. Por tanto,

*N*(*k*, *l*) = (*k^l* + *k*^⌈*l*/2⌉) / 2.

Con *k* = 2 y *l* = 4 resulta (16 + 4) / 2 = 10. Con el alfabeto del descriptor (*k* = 5) y cuatro bandas, (625 + 25) / 2 = 325. La prueba `test_el_numero_de_formas_canonicas_sigue_la_formula_de_burnside` enumera las órbitas con `canonizar` y las compara con la fórmula para *k* ∈ {2, 3, 5} y *l* ≤ 5.

**Lo que el orden distingue más allá del histograma [T].** El control M3-sin-orden reduce la palabra a su contenido, el número de bandas de cada tipo (*n₁*, …, *n_k*). El teorema de enumeración de Pólya generaliza el lema de Burnside para contar órbitas con un contenido dado; en el caso de C₂ el conteo es directo. Las palabras con contenido (*n₁*, …, *n_k*) son el coeficiente multinomial *M* = *l*! / (*n₁*! ⋯ *n_k*!), y de ellas *P* son palíndromos. El número de formas canónicas con ese contenido es (*M* + *P*) / 2.

Con dos bandas de cada uno de dos tipos: *M* = 6, *P* = 2 (`abba`, `baab`), y por tanto 4 formas canónicas (`aabb`, `abab`, `abba`, `baab`) que comparten histograma. M3-sin-orden las confunde y M3 las separa (`test_un_mismo_histograma_de_tipos_reune_varias_formas_canonicas`).

**Alcance de estos resultados.** Burnside y Pólya cuentan cuántas configuraciones admite la codificación bajo el grupo elegido. Indican cuánta información puede portar el orden; no indican que esa información sea útil para recuperar piezas, ni que el diseño andino se conciba como palabras bajo reversión. Lo primero es H2 **[E]**; lo segundo queda fuera de la tesis. Frame (2006; ficha F13) advierte que la clasificación cristalográfica por grupos de simetría no se ajusta a parte de los patrones andinos; el descriptor no clasifica por grupo de simetría, y la única equivalencia que impone es la reversión.

## 5. Bloques y distancias

El descriptor de un registro es la tupla de sus bloques. Cada bloque *b* tiene una distancia *d_b* con valores en [0, 1], definida solo cuando el bloque es observable en las dos piezas.

| Bloque | Atributo de la anotación | Distancia *d_b* | Código |
|---|---|---|---|
| Composición | `composicion` | 0 si coinciden; 1 si no | `nominal` |
| Bandas | `secuencia_bandas` | *d_w* (abajo) | `distancia_palabras` |
| Adyacencias | derivado de `secuencia_bandas` | *d_h* (abajo) | `histograma_adyacencias`, `distancia_l1_media` |
| Borde, centro | `borde`, `centro` | 0 si coinciden; 1 si no | `nominal` |
| Simetría | `simetria` | 0 si coinciden; 1 si no | `nominal` |
| Repetición | `repeticion`, con el orden no < parcial < sí | diferencia de rangos / 2 | `distancias_por_bloque` |
| Motivos | `motivos`, como conjunto | 1 − \|*X* ∩ *Y*\| / \|*X* ∪ *Y*\|; 0 si ambos son vacíos | `distancias_por_bloque` |
| Familia iconográfica | `familia_iconografica` | 0 si coinciden; 1 si no | `nominal` |

El color y el motivo principal no forman parte del descriptor **[D]**: el primero, para que una ganancia de M3 no pueda ser de origen cromático; el segundo, por ser la categoría más incierta de la anotación.

**Distancia entre palabras [D].** Con lev la distancia de Levenshtein y *w̃*, *ṽ* las palabras sin lagunas,

*d_w*(*w*, *v*) = mín{lev(*w̃*, *ṽ*), lev(*w̃*, ρ(*ṽ*))} / máx(\|*w̃*\|, \|*ṽ*\|), y *d_w*(ε, ε) = 0.

Propiedades **[P]**:

- *Rango:* lev(*x*, *y*) ≤ máx(\|*x*\|, \|*y*\|), luego *d_w* ∈ [0, 1]. Una palabra vacía frente a una no vacía está a distancia 1.
- *Simetría:* lev es simétrica y lev(*x*, ρ(*y*)) = lev(ρ(*x*), *y*), porque ρ transforma cada alineamiento en otro del mismo costo.
- *Invariancia:* *d_w*(ρ(*w*), *v*) = *d_w*(*w*, ρ(*v*)) = *d_w*(*w*, *v*). La distancia está bien definida sobre las órbitas.
- *Costo:* O(*l* · *l′*).
- *No es una métrica:* sin normalizar, el mínimo sobre la órbita de un grupo de isometrías es una métrica entre órbitas. La normalización por la longitud mayor rompe la desigualdad triangular. Contraejemplo: *x* = `aab`, *y* = `aaba`, *z* = `aba`; *d_w*(*x*, *z*) = 2/3 > *d_w*(*x*, *y*) + *d_w*(*y*, *z*) = 1/4 + 1/4.
- *Pruebas:* `test_distancia_de_palabras_simetrica_invariante_y_con_lagunas_enmascaradas`; `test_la_disimilitud_no_es_una_metrica`.

**Adyacencias [D].** *h*(*w*) es el histograma normalizado de los pares no ordenados {*w_j*, *w_(j+1)*} de símbolos contiguos dentro de cada tramo. Una laguna no forma pares. Por ser pares no ordenados, *h*(ρ(*w*)) = *h*(*w*) **[P]**. La distancia es *d_h* = ½ ‖*h*(*w*) − *h*(*v*)‖₁ ∈ [0, 1]. Si alguna de las dos palabras no tiene ningún par, el bloque no es observable para ese par de piezas: la observabilidad de este bloque depende del par y no solo de cada pieza.

Las adyacencias y la palabra no son redundantes: `aabb` y `abab` tienen el mismo histograma de tipos y distintas adyacencias (`test_el_control_sin_orden_no_distingue_lo_que_las_adyacencias_si`).

## 6. Disimilitud mixta

Sea *B*(*i*, *j*) el conjunto de bloques observables en las dos piezas y con peso positivo. Con pesos λ_b ≥ 0 (`[m3.pesos]` de `config/modelos.toml`),

*D*(*i*, *j*) = Σ_{b ∈ B(i,j)} λ_b *d_b*(*i*, *j*) / Σ_{b ∈ B(i,j)} λ_b.

Es un coeficiente de disimilitud para datos mixtos con valores faltantes: cada bloque aporta en su propia escala y los bloques no comparables se excluyen del numerador y del denominador.

**Ausencia de evidencia [D].** Si *B*(*i*, *j*) = ∅, *D* no está definida. El par queda «sin evidencia estructural», no recibe similitud máxima y se ubica al final del ranking de M3, ordenado por identificador. La **cobertura**, Σ_{b ∈ B(i,j)} λ_b / Σ_b λ_b, se informa junto con *D*.

**Propiedades [P]**, cuando *D* está definida:

1. *Rango.* *D* es una media ponderada de valores en [0, 1]; luego *D* ∈ [0, 1].
2. *Simetría.* *B*(*i*, *j*) = *B*(*j*, *i*) y cada *d_b* es simétrica.
3. *Reflexividad.* *D*(*i*, *i*) = 0, porque cada *d_b*(*i*, *i*) = 0.
4. *Descomposición exacta.* Con *c_b* = λ_b *d_b* / Σ_{B} λ, se cumple Σ_b *c_b* = *D*.
5. *Intervención.* Anular λ_b recalcula *D* sobre *B* ∖ {*b*} con los pesos restantes renormalizados.
6. *Costo.* Comparar dos piezas cuesta O(\|*B*\| + *l* · *l′*); ordenar los candidatos de una consulta, O(*n* · *l*²) más la ordenación, con *n* = \|𝒢\| − 1.

Pruebas: `test_disimilitud_mixta_simetrica_acotada_y_sin_evidencia` (1 a 3 y ausencia de evidencia); `test_la_suma_de_contribuciones_reconstruye_la_disimilitud_y_la_intervencion_es_exacta` (4 y 5).

**Lo que no se cumple, y no se afirma [P].**

- *D no satisface la desigualdad triangular.* Contraejemplo con máscaras: *i* tiene observadas la composición (bandas) y la simetría (traslacional); *j*, la composición (bandas) y el borde (sí); *k*, el borde (sí) y la simetría (bilateral). Entonces *D*(*i*, *j*) = 0, porque solo comparten la composición y coincide; *D*(*j*, *k*) = 0, porque solo comparten el borde y coincide; y *D*(*i*, *k*) = 1, porque solo comparten la simetría y difiere. Así, *D*(*i*, *k*) > *D*(*i*, *j*) + *D*(*j*, *k*).
- *D = 0 no implica igualdad de descriptores.* El mismo ejemplo lo muestra.
- *No se afirma que 1 − D sea un núcleo semidefinido positivo.*

*D* es, por tanto, una **disimilitud** y no una distancia métrica. El método solo ordena candidatos por *D* para cada consulta y no usa ninguna de esas propiedades: no hay índices métricos, agrupamiento ni inmersión. La prueba `test_la_disimilitud_no_es_una_metrica` fija los dos contraejemplos, para que el manuscrito no pueda afirmar lo contrario sin que una prueba falle.

**Control sin orden [D].** M3-sin-orden sustituye *d_w* por ½ ‖*t*(*w*) − *t*(*v*)‖₁, con *t* el histograma de tipos de la palabra sin lagunas, y omite el bloque de adyacencias. Usa los mismos pesos. Es la única diferencia con M3 (`comparar(..., sin_orden=True)`; `test_m3_sin_orden_ignora_el_orden_de_las_bandas`).

## 7. Fusión

Cada sistema opera en su propio espacio: M0, en términos de la ficha; M2, en el espacio de embeddings de OpenCLIP; M3, en el espacio de descriptores. **No se combinan representaciones** ni se supone alineación alguna entre esos espacios **[D]**. La fusión es tardía y actúa sobre puntuaciones.

Para una consulta *q* y un candidato *i*, sea *s_c*(*q*, *i*) la puntuación del componente *c* ∈ {M0, M2, M3} (en M3, 1 − *D*; indefinida si no hay evidencia). La normalización por consulta es

*ŝ_c*(*q*, *i*) = (*s_c*(*q*, *i*) − mín_i *s_c*) / (máx_i *s_c* − mín_i *s_c*),

tomando mínimo y máximo sobre los candidatos con valor; si todos coinciden, *ŝ_c* = 0. Sea *C*(*q*, *i*) el conjunto de componentes con evidencia para el par. Con pesos α_c ≥ 0,

*s*(*q*, *i*) = Σ_{c ∈ C(q,i)} α′_c *ŝ_c*(*q*, *i*), con α′_c = α_c / Σ_{c′ ∈ C(q,i)} α_c′.

Propiedades **[P]** (`src/modelos/m4_fusion.py`; `tests/test_m4.py`):

- *Rango:* *s* ∈ [0, 1], por ser combinación convexa de valores en [0, 1].
- *Descomposición exacta:* las contribuciones α′_c *ŝ_c* suman *s*. Es la primera comprobación de H3.
- *Intervención:* retirar un componente equivale a declararlo sin evidencia para todos los candidatos, y los pesos restantes se renormalizan. Es la segunda comprobación de H3 y la forma de calcular las ablaciones.
- *Sin evidencia estructural:* el par no recibe la puntuación máxima de M3; su peso se reparte entre los demás componentes.
- *Dependencia del conjunto de candidatos:* *ŝ_c* depende del mínimo y del máximo de la consulta, de modo que la puntuación de un par no es comparable entre consultas. Solo se usa para ordenar dentro de cada consulta.

La variante por posiciones recíprocas, Σ_c 1 / (60 + *r_c*) (Cormack, Clarke y Büttcher, 2009; ficha F22), no tiene pesos y no conserva la descomposición; por eso no interviene en H3.

**Relación con los modelos de cuello de botella de conceptos.** El marco más cercano es el de Koh et al. (2020; ficha F26): la decisión pasa por conceptos legibles. La diferencia es que allí los conceptos se predicen a partir de la imagen y aquí los anota una persona. M4 es aditivo y produce su propia explicación (Rudin, 2019; ficha F28); lo que H3 comprueba es su fidelidad, no su plausibilidad (Jacovi y Goldberg, 2020; ficha F27).

## 8. Qué es cada cosa

| Naturaleza | Enunciados |
|---|---|
| **[T]** Resultados conocidos | Lema de Burnside y enumeración de Pólya; propiedades de la distancia de Levenshtein; índice de Jaccard |
| **[D]** Decisiones de diseño | El alfabeto de cinco tipos; la definición de banda; el grupo C₂ y ninguna otra transformación; pares no ordenados en las adyacencias; normalización por la longitud mayor; exclusión del color y del motivo principal; pesos iguales de partida; tratamiento del par sin evidencia; fusión tardía con normalización por consulta |
| **[P]** Propiedades verificadas | Invariancia y completitud de la forma canónica; rango, simetría e invariancia de *d_w*; invariancia de *h*; rango, simetría, reflexividad, descomposición e intervención de *D* y de la fusión; fallo de la desigualdad triangular |
| **[E]** Afirmaciones empíricas, sin contrastar | Que el orden de las bandas mejora la recuperación (H2); que la estructura añade utilidad a un codificador general (H1); que la descomposición se cumple en todos los resultados de prueba (H3); que la anotación es estable más allá del lote medido |

## 9. Correspondencia entre fórmula, código y atributo

| Concepto | Fórmula | Función | Atributo o archivo | Prueba |
|---|---|---|---|---|
| Reversión | ρ(*w*) | `reverso` | `secuencia_bandas` | `test_la_forma_canonica_es_invariante_a_la_reversion` |
| Forma canónica | *c*(*w*) | `canonizar` | `secuencia_bandas` | La misma; `test_burnside_cuatro_posiciones_dos_simbolos_dan_diez_orbitas` |
| Tramos y lagunas | *w̃* | `tramos`, `sin_lagunas` | Símbolo `laguna` | `test_distancia_de_palabras_…` |
| Histograma de tipos | *t*(*w*) | `histograma_tipos` | `secuencia_bandas` | `test_el_control_sin_orden_…` |
| Adyacencias | *h*(*w*) | `histograma_adyacencias` | `secuencia_bandas` | La misma |
| Distancia de palabras | *d_w* | `distancia_palabras`, `distancia_edicion` | `secuencia_bandas` | `test_distancia_de_palabras_…` |
| Máscara | *m_b* | `valor`, `palabra_de_bandas`, `descriptor` | Estados de `[estados]` en `config/vocabulario.toml` | `test_disimilitud_mixta_…` |
| Distancias por bloque | *d_b* | `distancias_por_bloque` | Atributos de la sección 5 | Las de la sección 6 |
| Disimilitud y contribuciones | *D*, *c_b* | `comparar` | `[m3.pesos]` | `test_la_suma_de_contribuciones_…` |
| Normalización por consulta | *ŝ_c* | `normalizar` | — | `tests/test_m4.py` |
| Pesos efectivos | α′_c | `pesos_efectivos` | Rejilla del protocolo | `tests/test_m4.py` |
| Fusión | *s* | `fusionar` | — | `tests/test_m4.py` |
| Grupos | Componentes conexas de (*R*, *U*) | `src/grupos/grupos.py` | `grupos_revision_v2.xlsx` | `tests/test_grupos.py` |

Las funciones sin ruta están en `src/modelos/m3_estructura.py` (M3) o en `src/modelos/m4_fusion.py` (fusión), y las pruebas sin ruta, en `tests/test_sistemas.py`.

## 10. Pendiente

- Reescribir el capítulo matemático del manuscrito con esta notación y retirar de él toda afirmación de carácter **[E]** que no proceda de los resultados.
- Describir, sobre la anotación v2.1 una vez congelada, cuántas piezas de la galería comparten histograma de tipos y difieren en forma canónica. Ese dato indica cuánto puede distinguir el orden en este corpus antes de medir su utilidad, y no requiere ningún juicio de relevancia.
