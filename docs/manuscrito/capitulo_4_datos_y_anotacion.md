# 4. Datos y anotación

## 4.1 Introducción

Este capítulo describe el corpus sobre el que se construye y se evalúa la representación: su procedencia, el criterio de selección, sus unidades y la anotación de la organización visible de cada textil, con la consistencia que esa anotación alcanzó. El corpus amplía el del primer avance, que reunía piezas del Metropolitan Museum of Art (MET) y del Cleveland Museum of Art (CMA), con una tercera fuente, el Art Institute of Chicago (AIC); la serie del primer avance se conserva congelada y no se reescribe.

## 4.2 Fuentes y procedencia

### 4.2.1 Criterio de selección de fuentes

Una colección se incorpora solo si cumple cuatro condiciones: imágenes en dominio público o con licencia CC0 registrada por objeto; una interfaz de programación pública que permita reconstruir la extracción sin recurrir al raspado de páginas; metadatos curatoriales suficientes para la trazabilidad (identificador, enlace oficial, cultura o procedencia, fecha y material o técnica); y un volumen de piezas andinas que justifique el esfuerzo de integración.

Las tres fuentes incluidas satisfacen esas condiciones (Cuadro 4.1). Otras colecciones con fondos andinos, entre ellas las del British Museum, el Museo de Berlín, el Field Museum, el Penn Museum, el Smithsonian y el Museum of Fine Arts de Boston, se descartaron por licencia de imagen incompatible o por falta de una interfaz reutilizable. Las de museos peruanos solo serían accesibles mediante convenio institucional, que excede el plazo del estudio.

**Cuadro 4.1.** Fuentes del corpus v2.

| Fuente | Licencia de la imagen | Particularidades de la extracción |
|---|---|---|
| The Metropolitan Museum of Art (MET) | Dominio público (Open Access) | Parte de la curación MET del primer avance. Fechas en texto libre. Un registro (MET:312615) ya no tiene imagen en el museo |
| Cleveland Museum of Art (CMA) | CC0 | Consulta conservadora por cultura andina y término textil; una consulta por tipo «Textile» devolvió 2045 registros, casi todos no andinos, y se descartó |
| Art Institute of Chicago (AIC) | CC0; la descripción del museo tiene licencia CC BY 4.0 y se cita | Consultas estructuradas; servicio de imágenes limitado al ancho del original |

### 4.2.2 Mediación institucional

Las tres colecciones pertenecen a museos de Estados Unidos, y el corpus refleja decisiones ajenas al estudio: qué piezas se adquirieron, cómo se catalogaron y qué se fotografió. Su distribución por cultura estima lo que estas instituciones conservan y publican, no la producción textil andina. Las atribuciones culturales y cronológicas son las de cada ficha y se conservan sin corregir, junto a su versión normalizada.

La mediación tiene consecuencias medibles. Ninguna fuente informa un periodo estructurado; la descripción curatorial existe en 29 de 155 registros MET, 53 de 108 CMA y 43 de 352 AIC; y la cultura falta en 94 registros, todos de AIC. Las copias originales de MET y CMA tienen entre 3400 y 4000 píxeles de lado mayor, y las de AIC, 1686, una diferencia que, si no se controla, sesga las medidas de calidad entre museos (sección 4.4.3).

## 4.3 Recolección y candidatura

Cada fuente tiene un colector propio que consulta su interfaz pública y normaliza los registros a un esquema común. Un registro pasa a ser **candidato** cuando tiene imagen oficial, metadatos mínimos de trazabilidad, evidencia textil (clasificación o material textil, o términos como *textile*, *woven*, *tunic* o *tapestry*) y evidencia andina (Perú, Inca, Paracas, Nasca, Wari, Chancay u otras denominaciones), buscadas como palabra completa. Las herramientas de hilado y tejido se excluyen: son objetos textiles por su función, pero no superficies tejidas. Ser candidato no implica entrar al corpus: la decisión es manual y sigue el criterio de la sección siguiente. Las listas de candidatos se conservan como insumos fijos, porque sobre ellas se tomaron decisiones humanas (anexo A).

## 4.4 Criterio de aptitud analítica

### 4.4.1 Criterio

El primer avance incluía una pieza en el corpus principal si su imagen era «útil» y tenía «valor computacional», un juicio que no era reproducible. La segunda parte lo reemplaza por un criterio que se comprueba en la fotografía. Se fijó durante la revisión manual de las 508 candidatas de AIC, en octubre de 2026, y se aplicó igual a las tres fuentes:

- **Principal.** Los colores y las figuras del textil se identifican a primera vista.
- **Imagen de referencia** (subconjunto del principal). Además, el textil está completo y su completitud puede verificarse en la fotografía. Operativamente, el textil conserva sus orillos (los bordes terminados del tejido) y los extremos de la urdimbre (los hilos longitudinales que se tensan en el telar) visibles en la fotografía.
- **Complementario** (en los libros de revisión, «secundario»). La imagen no permite identificar bien colores o formas, por ejemplo en una fotografía monocroma o en una pieza muy deteriorada.
- **Descarte.** El registro no es pertinente o la imagen no sirve para el estudio: plumaria (piezas elaboradas con plumas), muñecos, piezas con fecha de inicio posterior a 1532, objetos no textiles o no andinos, herramientas e imágenes inexistentes.

El criterio del principal no exige que la pieza esté entera: el descriptor estructural necesita atributos identificables (colores, módulos, figuras, bandas), y un fragmento legible los conserva. Exigir piezas completas habría desplazado al complementario a las culturas que se conservan sobre todo en fragmentos; con el criterio adoptado, la proporción de candidatos que pasa al principal es del 92 % en Paracas, 78 % en Wari, 70 % en Chancay y 54 % en Nasca. La exclusión de las piezas posteriores a 1532 delimita la población al periodo prehispánico; la fecha se lee en el texto de cada ficha y, si es un intervalo, se usa su inicio.

### 4.4.2 Reglas verificables

Una parte de las decisiones no requiere juicio y se aplica mediante reglas explícitas (Cuadro 4.2). Las reglas firman como revisor «auto», el revisor humano puede corregirlas y ninguna reemplaza una decisión manual ya tomada.

**Cuadro 4.2.** Reglas automáticas de curación.

| Regla | Decisión | Fundamento |
|---|---|---|
| Plumaria (material o título), muñecos, fecha de inicio posterior a 1532 | Descarte | Pertinencia definida por el criterio |
| Posible figurilla («Figure» en singular, sin complemento) | Revisión manual | Prudencia: «Fragment with Figure» es un textil con una figura representada |
| Sin imagen o textil de menos de 300 píxeles | Descarte | No hay atributos que identificar |
| Fotografía monocroma | Complementario | El color no es identificable |

### 4.4.3 Puntaje de aptitud como apoyo a la revisión

Para acelerar la revisión de fuentes nuevas se desarrolló un puntaje de aptitud: el textil se separa del fondo en la copia de evaluación de cada imagen (1600 píxeles de lado mayor), se miden rasgos de la fotografía, del color y de la forma del diseño, y regresiones logísticas ajustadas con los motivos escritos por el revisor estiman la legibilidad del color y de las formas, la completitud y la condición de imagen de referencia. La nitidez que se compara entre museos se mide con el textil llevado a 600 píxeles, porque depende de la escala de la copia.

En AIC, con validación cruzada, el área bajo la curva ROC fue de 0,89 a 0,94 según la variable, cifras optimistas porque la estandarización usa todas las imágenes y los pliegues se forman por registro y no por objeto. En una validación ciega con 40 imágenes de MET y CMA, el acuerdo entre el revisor y el modelo calibrado con AIC fue κ = 0,56, por debajo del umbral de 0,6 fijado de antemano; por eso, en MET y CMA solo se aplicaron las reglas del Cuadro 4.2 y las decisiones del revisor. Recalibrado con las tres fuentes, el puntaje separa los registros útiles del resto, fuera de pliegue, con un área de 0,91 en AIC, 0,76 en MET y 0,83 en CMA, pero su transferencia a una fuente nueva exigiría otra muestra ciega. Es un apoyo exploratorio de la curación, no un clasificador validado.

## 4.5 Composición del corpus v2

El Cuadro 4.3 resume el resultado de la curación. Las 874 decisiones de inclusión o descarte tienen procedencia mixta: 227 provienen de reglas automáticas documentadas y 647 de la curación manual. No equivalen a 874 objetos independientes, porque varias fichas pueden mostrar el mismo objeto (sección 4.6).

**Cuadro 4.3.** Corpus v2 por fuente y subconjunto.

| Fuente | Principal | Complementario | Descartados | Total |
|---|---:|---:|---:|---:|
| MET | 130 | 25 | 65 | 220 |
| CMA | 104 | 4 | 38 | 146 |
| AIC | 228 | 124 | 156 | 508 |
| Total | 462 | 153 | 259 | 874 |

El consolidado v2 reúne el principal y el complementario: 615 registros con imagen útil y licencia abierta. Cada registro conserva el texto de la fuente junto a su versión normalizada (por ejemplo, la técnica tal como la escribe el museo y su código en el vocabulario controlado) e indica si cada valor normalizado proviene de la curación, de una regla o de la anotación. Las imágenes no se redistribuyen: se identifican por su enlace oficial y por la suma SHA-256 de la copia usada.

El principal se reparte de manera desigual: AIC aporta casi la mitad, concentra los registros sin cultura y la mayor parte de los Chancay, y MET aporta la mayor parte de los Paracas y Wari. El diseño experimental estratifica por museo (capítulo 7).

## 4.6 Unidades: registro, imagen y grupo

El primer avance trataba como una sola cosa el objeto, su ficha y su fotografía. Aquí se separan, porque si dos fichas muestran el mismo objeto, recuperar una a partir de la otra no prueba nada sobre la representación.

- El **registro** es la ficha de un museo, identificada por la fuente y el número de la ficha (por ejemplo, MET:312615).
- La **imagen** es la copia de evaluación de la fotografía principal del registro.
- El **grupo** reúne los registros que muestran un mismo objeto o partes de él: la misma fotografía, vistas distintas o fragmentos de una misma pieza.

En adelante, **pieza** designa un registro de la galería, es decir, del núcleo anotado sobre el que se evalúa la recuperación (sección 4.8); el textil físico se llama **objeto**.

Los grupos se construyeron en dos pasos. Primero, cinco señales automáticas propusieron pares candidatos: imagen idéntica; número de inventario con la misma base y sufijo de parte; descripción idéntica de 40 caracteres o más; distancia de Hamming entre huellas perceptuales (dHash) menor o igual a 4; y similitud coseno entre los vectores de OpenCLIP de al menos 0,95, o de 0,93 entre museos distintos. Ninguna señal basta sola; en particular, la similitud de un modelo visión-lenguaje no detecta bien las copias: Radford et al. [@radford2021, p. 44], autores de CLIP, descartaron su propio espacio de representación para ese fin porque asigna baja similitud a copias de una misma imagen con texturas finas o rayas reescaladas de forma distinta. Las señales propusieron 100 pares distintos, 3 de ellos entre museos. Los 13 pares de imagen idéntica se unieron mediante una regla automática, que el investigador podía corregir, y los 87 restantes los decidió el investigador; en total se unieron 65 pares y se separaron 35. Los grupos son las componentes conexas del grafo cuyos vértices son los registros y cuyas aristas son los pares unidos.

El resultado son 577 grupos para los 615 registros: 555 registros aislados y 22 grupos de dos a siete registros. Las 150 piezas del núcleo pertenecen a 146 grupos. El grupo, y no el registro, es la unidad de partición entre desarrollo y prueba, y una comprobación automática verifica que ningún grupo quede repartido entre ambas.

## 4.7 Esquema de anotación estructural

### 4.7.1 Capas y atributos

La anotación registra lo que una persona observa en la fotografía de cada pieza. No interpreta el significado de los motivos ni sustituye el juicio de especialistas en arqueología o etnografía textil. Cada pieza se anota en cinco capas y en un orden fijo (Cuadro 4.4).

**Cuadro 4.4.** Capas y atributos de la anotación estructural.

| Capa | Atributos |
|---|---|
| Cromática | color dominante, colores presentes, contraste, densidad visual |
| Estructural | composición, eje de bandas, secuencia de bandas, borde decorado, centro |
| Repetición y simetría | repetición, simetría |
| Iconográfica | motivos, familia iconográfica, motivo principal |
| Correcciones | tipo de objeto, tipo de superficie, material, técnica y estado de la imagen, cuando el valor de la ficha es incorrecto |

La **composición** es la organización dominante de la superficie: bandas, paneles, retícula, campo central, borde o composición libre. El **borde decorado** es una franja ornamental que enmarca la pieza; no es el orillo. El **centro** registra si hay un campo central diferenciado. Los **motivos** son las clases de figura presentes (geométrico, antropomorfo, zoomorfo, fitomorfo, abstracto), la **familia iconográfica** es la forma dominante de representación (geométrica, figurativa, mixta, abstracta) y el **motivo principal**, el más visible. Los valores pertenecen a un vocabulario controlado único, que extiende el del primer avance. En los datos se guardan códigos sin tildes (`fibra_de_camelido`), y en el texto de la tesis se usan las etiquetas correspondientes.

### 4.7.2 Valores y estados

La anotación distingue el valor de un atributo de su estado de observación. La distinción es sustantiva: un descriptor que confunde «el rasgo no está» con «el rasgo no se ve» compara piezas por la calidad de su fotografía y no por su organización. Cuando un atributo no tiene valor, se registra uno de tres estados (Figura 4.1):

- **Ausente.** La superficie pertinente se ve y el rasgo no está; por ejemplo, una pieza sin bandas.
- **No observable.** La superficie pertinente no se ve, por fragmentación, recorte, pliegue o encuadre parcial.
- **Desconocido.** La superficie se ve, pero el anotador no puede decidir entre valores.

![Figura 4.1. El mismo atributo, la secuencia de bandas, en dos estados: a) ausente, porque la superficie se ve y ninguna franja la cruza; b) no observable, porque el fragmento está cortado por todos los lados y no puede saberse si la pieza tenía bandas. Fotografías: CMA:137312 y MET:307679, dominio público (CC0).](figuras/fig_4_1_ausente_no_observable.png)

En el borde decorado y el centro, la no observación se registra con el valor «no visible». El estado ocupa la celda completa y no se combina con valores. Una celda vacía significa «no anotado» y nunca «ausente». La categoría «no determinada» de la familia iconográfica y del tipo de banda no es un estado: indica que se ve un rasgo que no corresponde a ninguna categoría del vocabulario.

La **regla de los treinta segundos** limita la presión por completar: si un atributo genera más de treinta segundos de duda, se anota como desconocido y la duda se describe en las observaciones. Un valor forzado entraría en el descriptor como si fuera un dato.

### 4.7.3 La palabra de bandas

La secuencia de bandas es la variable sobre la que descansa la segunda hipótesis del estudio (capítulo 2, sección 2.5). Una **banda** es una franja que atraviesa toda la superficie visible, perpendicular al eje de lectura y delimitada por un cambio de color o de diseño. No son bandas las franjas perimetrales, que se registran como borde decorado, ni las filas o columnas de una retícula, ni los paneles, que se registran en la composición. La composición dominante no decide si hay bandas: una pieza organizada en campo, paneles o retícula puede tener franjas que la cruzan de lado a lado, y esas franjas forman su palabra.

La definición es visual, pero tiene un correlato técnico. En un tejido de faz de urdimbre (aquel en que los hilos longitudinales, la urdimbre, cubren la superficie y forman el diseño), una banda suele coincidir con una franja de hilos de urdimbre de color; en el tapiz (aquel en que los hilos transversales, la trama, cubren la urdimbre y forman el diseño), con una franja tejida por la trama; y en el bordado, con una franja bordada sobre una tela lisa. La sección 3.2 expone por qué, en la faz de urdimbre, la banda la fija el urdido (la disposición de los hilos de urdimbre en el telar) antes de tejer.

Cada banda se registra por su tipo (lisa, geométrica, figurativa, mixta o no determinada), en el orden del eje, y la secuencia se escribe como una palabra, por ejemplo `lisa > geometrica > figurativa > geometrica > lisa` (Figura 4.2). Un tramo que no se ve por rotura o pliegue se registra como laguna, y el descriptor lo enmascara. No se registra el color ni el ancho de cada banda: el color ya está en la capa cromática, y estimar el ancho a ojo daría una precisión aparente.

![Figura 4.2. Palabra de bandas de una pieza con eje horizontal: a la izquierda, la fotografía; a la derecha, un esquema ilustrativo con las bandas en el orden anotado. La palabra geométrica > lisa > mixta > lisa > geométrica es palíndroma. Fotografía: AIC:51309, dominio público (CC0).](figuras/fig_4_2_palabra_bandas.png)

El eje es el de la fotografía y no el de la urdimbre: la anotación registra las bandas por su aspecto visible, sin distinguir su técnica. Como las túnicas de tapiz de la sierra se tejían con el decorado acostado y se giraban 90 grados al armar la prenda (sección 3.2), una misma organización puede aparecer horizontal o vertical según cómo se fotografió la pieza; por eso el eje no entra en el descriptor (capítulo 5).

### 4.7.4 Simetría y repetición

El vocabulario conserva dos categorías del primer avance que describen la repetición por traslación y que la primera anotación no separaba con nitidez. Se distinguen por la dimensión de la repetición. Es **traslacional** la de un motivo que se desplaza en una sola dirección y forma un friso, es decir, una franja decorativa continua. Es **repetición modular** la de un módulo con contorno propio (celda, cuadro o panel) que se repite como unidad en dos dimensiones, como en una retícula o un damero. La distinción sigue la que hace el análisis de simetría de patrones entre los patrones de una dimensión, que admiten siete tipos, y los de dos dimensiones, que admiten diecisiete [@crowe2001, pp. 6–9]. El descriptor no clasifica las piezas por grupo de simetría, sino que registra la simetría como un atributo nominal anotado: los métodos que detectan ese grupo en la imagen [@liu2004] no modelan las distorsiones geométricas y exigen una cámara perpendicular a la superficie [@liu2004, p. 368], condiciones que las fotografías de textiles fragmentados, plegados o con lagunas no garantizan.

## 4.8 Núcleo de anotación

Anotar los 462 registros del principal excede el plazo del estudio. Se anotó un **núcleo** de 150 piezas, elegido por muestreo estratificado. La cuota de cada fuente es proporcional a su peso en el principal, repartida por el método de los mayores restos: MET 42, CMA 34 y AIC 74. Dentro de cada fuente, los estratos combinan la cultura agrupada (Paracas, Nasca, Wari, Chancay, Inca, Chimú, otras y sin cultura) con el nivel que sugiere el puntaje de aptitud, que no decide la inclusión y solo asegura que el núcleo cubra fotografías de calidad distinta. Dentro de cada estrato se eligen los registros con menor suma SHA-256 de la cadena «semilla:identificador», con la semilla 20261020, de modo que la selección no depende de la versión del lenguaje ni de las bibliotecas. Las piezas se reparten en turno entre cinco lotes de 30 que replican la composición del núcleo; ningún lote supera el 60 % de una sola fuente. La anotación se hizo por lotes, uno por sesión, y concluyó el 5 de noviembre de 2026.

## 4.9 Estabilidad de la anotación

### 4.9.1 Diseño

El estudio tiene un solo anotador. Sin una segunda persona no puede medirse la reproducibilidad de la anotación (el acuerdo entre anotadores), pero sí su **estabilidad**: el acuerdo del anotador consigo mismo en el tiempo. Abercrombie et al. [@abercrombie2025] encontraron que menos del 0,07 % de los artículos de la ACL Anthology la informa, aunque los anotadores cambiaban cerca de una de cada cuatro etiquetas incluso con dos semanas de intervalo; y la estabilidad varía mucho de una categoría a otra [@beijbom2015, p. 10], lo que aconseja informarla por atributo.

El anotador volvió a anotar a ciegas las 30 piezas del lote 1, en otro orden y al menos siete días después de la primera pasada, sin consultar la primera anotación. Cada atributo se mide según su tipo: kappa de Cohen en los nominales, kappa ponderado lineal en los ordinales, índice de Jaccard medio en los de valores múltiples y, en la secuencia de bandas, la coincidencia exacta y la similitud de edición $1 - d/\max(\ell_1, \ell_2)$, con $d$ la distancia de Levenshtein y $\ell_1, \ell_2$ las longitudes de las dos secuencias, que no tiene un acuerdo esperado al azar definido y, por eso, no admite kappa. Siguiendo a Artstein y Poesio [@artstein2008], se informa el acuerdo observado junto a cada coeficiente, porque un mismo acuerdo bruto puede producir coeficientes muy distintos. Ni el índice de Jaccard ni alternativas como MASI [@passonneau2006, p. 834], usados como media por pieza, corrigen el acuerdo esperado por azar.

El umbral κ ≥ 0,6 es una señal para revisar la definición de un atributo, no un criterio de aprobación, y es una decisión operativa de este estudio. Queda por debajo del 0,8 que Artstein y Poesio [@artstein2008, p. 591] proponen para el acuerdo entre codificadores cuando es imprescindible fijar un umbral, aunque desaconsejan convertirlo en requisito y no tratan el acuerdo intra-anotador; la escala de Landis y Koch [@landis1977, p. 165], que sus autores reconocen como arbitraria, llama sustancial al acuerdo entre 0,61 y 0,80.

### 4.9.2 Resultados

**Cuadro 4.5.** Estabilidad intra-anotador en el lote 1 (30 piezas), sobre los pares observados en las dos pasadas.

| Capa | Atributo | Medida | n | Acuerdo observado | Coeficiente |
|---|---|---|---:|---:|---:|
| Cromática | Color dominante | κ | 29 | 0,966 | 0,949 |
| Cromática | Contraste | κ ponderado | 30 | 0,917 | 0,736 |
| Cromática | Densidad visual | κ ponderado | 30 | 0,933 | 0,776 |
| Cromática | Colores | Jaccard medio | 30 | 0,770 | — |
| Estructural | Composición | κ | 24 | 0,875 | 0,837 |
| Estructural | Eje de bandas | κ | 24 | 0,833 | 0,738 |
| Estructural | Secuencia de bandas | Similitud de edición | 24 | 0,797 | 17 de 24 idénticas |
| Estructural | Borde decorado | κ (sí/no) | 24 | 0,875 | 0,750 |
| Estructural | Centro | κ (sí/no) | 25 | 0,800 | 0,490 |
| Repetición y simetría | Repetición | κ ponderado | 27 | 0,944 | 0,799 |
| Repetición y simetría | Simetría | κ | 23 | 0,826 | 0,765 |
| Iconográfica | Motivos | Jaccard medio | 30 | 0,844 | — |
| Iconográfica | Familia iconográfica | κ | 29 | 0,828 | 0,751 |
| Iconográfica | Motivo principal | κ | 21 | 0,810 | 0,772 |

Diez de los once atributos con kappa superan la señal de 0,6 (Cuadro 4.5). El **centro** queda por debajo (κ = 0,49): se mantuvo en la anotación y en el descriptor, porque retirarlo a la vista de un solo lote de 30 piezas habría sido una decisión tomada con poca evidencia, y su baja estabilidad figura entre las amenazas a la validez (sección 7.13). En los atributos de valores múltiples, el desacuerdo se concentra en etiquetas concretas: el amarillo (κ = 0,48) y el ocre (κ = 0,28) entre los colores, y lo abstracto (κ = 0,47) entre los motivos. Son categorías de frontera difusa en la fotografía.

El cuadro muestra solo los pares que las dos pasadas pudieron observar, y esa restricción oculta una segunda fuente de variabilidad: la frontera entre «se ve» y «no se ve». Para la composición, el anotador consideró observable la misma pieza en las dos pasadas en 24 casos, solo en la primera en 4 y solo en la segunda en 2. El acuerdo sobre la observabilidad, corregido por azar, es nulo (κ = −0,10), aunque el acuerdo bruto sea de 0,80. Como la máscara de observabilidad decide qué bloques compara el descriptor (capítulo 5), esta inestabilidad lo afecta directamente (sección 4.13).

La decisión más inestable fue si una pieza tiene bandas: cuatro piezas pasaron de no tener bandas a una secuencia de dos a seis. La guía definía los tipos de banda, pero no qué cuenta como banda. La definición de la sección 4.7.3 se escribió a partir de este hallazgo.

### 4.9.3 Adjudicación del lote re-anotado

Cuando las dos pasadas del lote 1 difieren, prevalece la re-anotación, hecha con más experiencia y con la guía ya estabilizada; la primera pasada solo sirve para medir la estabilidad. El lote 1 de la versión final refleja, por tanto, la segunda lectura, y los lotes 2 a 5 la primera, con las correcciones de la sección siguiente.

## 4.10 Revisión de criterios y versión 2.1

La definición de banda y la distinción entre traslación y repetición modular se escribieron después de anotar los lotes 2 a 5. Para no congelar una anotación hecha con criterios distintos de los vigentes, el anotador volvió a mirar las piezas afectadas antes de cerrar la versión.

**Selección.** Una regla automática seleccionó 108 de las 120 piezas de los lotes 2 a 5: las que tenían palabra de bandas (52), simetría traslacional o modular (85), una duda anotada sobre un atributo que usa el descriptor (32) o una petición de verificar que la imagen correspondía al registro (22); una misma pieza podía cumplir varias condiciones. Quedaron fuera las dudas sobre atributos que el descriptor no usa (46 piezas) y los huecos del vocabulario (16 piezas).

**Procedimiento asistido.** Para cada pieza seleccionada, un modelo de visión y lenguaje generó una propuesta (confirmar o corregir, con los valores y el criterio aplicado) a partir de la imagen, la anotación vigente, las observaciones del anotador y el texto de los criterios. Ninguna propuesta se aplicó por sí misma: el anotador verificó cada una frente a la imagen, la corrigió cuando hizo falta y la firmó. De las 108 decisiones, 66 confirmaron la anotación y 42 la corrigieron, con 173 valores modificados. Frente a la propuesta del modelo, 58 decisiones coinciden con ella y 50 la modifican: las 42 correcciones, en las que el anotador revisó todos los atributos de la pieza y no solo los que la propuesta tocaba, y 8 confirmaciones de anotaciones desplazadas, cuya propuesta indicaba que la imagen no correspondía al registro. Cada cambio quedó registrado con el valor anterior, el nuevo y su motivo.

**Criterios fijados durante la revisión.** Al verificar las propuestas, el investigador fijó cuatro criterios que la guía no resolvía: las esquinas y los fragmentos con decoración perimetral se registran como borde decorado; una tira con recuadros sucesivos de contorno propio es una composición en paneles, sin palabra de bandas; una figura única es un campo central si un fondo la enmarca, y una composición libre si la pieza es la propia figura; y varias piezas sin relación en una sola fotografía llevan sus atributos estructurales como no observables.

**Identidad de las imágenes.** Ocho anotaciones describían la imagen de otro registro: seis formaban un ciclo y dos estaban intercambiadas. Las imágenes y los números de inventario mostraron que eran las anotaciones, y no las imágenes, las desplazadas. Cada anotación se trasladó a la fila del registro cuya imagen describía y se revisó con los criterios vigentes. Las doce piezas que no entraron en la revisión se compararon con sus imágenes, y todas coincidían. Una novena discrepancia, la de la pieza AIC:85278, pasó esta verificación: su identidad se revisó y se dio por coincidente, y el error se detectó después de la evaluación final, cuando la anotación ya estaba sellada (capítulo 11, sección 11.2).

**Efecto sobre la anotación.** Las correcciones redujeron las piezas con composición en bandas de 48 a 35 y aumentaron las de paneles de 24 a 41; las piezas con palabra de bandas pasaron de 66 a 53. El efecto principal fue separar las franjas que cruzan la pieza de las tiras de recuadros, que la primera anotación había registrado como bandas. Las observaciones en texto libre de la primera anotación se redactaron de nuevo, también con asistencia, para que describieran solo lo visible; ningún valor anotado cambió por ello.

**Congelación.** La anotación del núcleo quedó congelada como versión 2.1 el 17 de noviembre de 2026 (Cuadro 4.6). Desde entonces, cada regeneración compara la anotación exportada con la copia congelada y su suma SHA-256, y cualquier cambio posterior la detiene.

**Cuadro 4.6.** Composición dominante en la anotación v2.1 del núcleo (150 piezas).

| Composición | Piezas |
|---|---:|
| Paneles | 41 |
| Bandas | 35 |
| Retícula | 31 |
| Campo central | 22 |
| Composición libre | 10 |
| Borde | 6 |
| Desconocida | 4 |
| No observable | 1 |

### 4.10.1 Justificación y control de la asistencia

La asistencia se limitó a verificar anotaciones existentes frente a criterios escritos por el investigador: no generó anotaciones nuevas ni definió criterios. Ninguna propuesta se aplicó sin la verificación y la firma del anotador, y la congelación impone esa condición de forma automática. El modelo no tuvo acceso a *rankings*, juicios de relevancia ni resultados de los sistemas evaluados, y no es ninguno de ellos, de modo que no podía orientar la anotación a favor de un sistema. La estabilidad de la sección 4.9 se midió entre dos pasadas hechas sin asistencia. El procedimiento es más restrictivo que el modo semiautomático que Beijbom et al. [@beijbom2015, pp. 8–9 y 12] evaluaron con especialistas, en el que el clasificador decide por sí solo los puntos en que tiene más confianza: aquí ninguna decisión automática entra en la anotación sin que la persona la verifique.

El riesgo conocido es que quien verifica una propuesta tiende a aceptarla; este sesgo afecta también a usuarios expertos, y ni el entrenamiento ni la instrucción de verificar lo eliminan [@parasuraman2010, p. 397]. No puede saberse cuántas de las 58 decisiones que coinciden con la propuesta habría tomado igual el anotador sin ella. Por eso se informa la proporción de decisiones que la modificaron (50 de 108) y se midió cuánto depende el descriptor de la revisión.

**Análisis de sensibilidad.** Se compararon los *rankings* de desarrollo de M3 y de su control sin orden calculados con la anotación anterior a la revisión (con las ocho anotaciones desplazadas ya trasladadas, pero sin corregir) y con la versión 2.1. La revisión cambió al menos un atributo del descriptor en 46 de las 150 piezas, sobre todo la secuencia de bandas y la simetría (34 piezas cada una), la composición (28) y el borde decorado (24). En las diez consultas de desarrollo, los diez primeros resultados de M3 comparten entre 4 y 9 piezas entre ambas versiones, y la correlación de Spearman entre los *rankings* completos va de 0,56 a 0,91.

La revisión no es, por tanto, neutra para el descriptor: cambia de forma apreciable qué piezas recupera M3. No indica cuál de las dos anotaciones es más fiel a la imagen, sino que las conclusiones sobre M3 dependen de la versión, y por eso la versión se congeló antes del experimento. Las métricas de relevancia de ambas versiones no se comparan como evidencia: los pares juzgados se eligieron con la versión 2.1, de modo que la anterior tiene candidatos sin juicio, y la revisión de la anotación y la de los juicios de desarrollo usaron asistencia de la misma familia de modelos (sección 7.6.4), de modo que una coincidencia entre ambas podría reflejar ese criterio compartido.

## 4.11 Versionado y reproducibilidad

Cada decisión humana de curación, agrupamiento o anotación se registra en un libro de revisión con su autor y su fecha, y ningún archivo derivado se edita a mano. Un único punto de entrada regenera sin acceso a la red todos los derivados a partir de esos libros y de los insumos fijos, y las pruebas automatizadas comprueban que la regeneración coincide con lo versionado. Cada entrega (la serie del primer avance, el consolidado v2 y la anotación 2.1) se identifica por una etiqueta del repositorio y por las sumas SHA-256 de sus archivos; la serie del primer avance lee copias congeladas de sus insumos y se regenera idéntica. El anexo A detalla el procedimiento.

## 4.12 Uso ético y gobernanza de los datos

La licencia abierta permite reutilizar las imágenes, pero no agota la pregunta sobre su uso. Los textiles del corpus son objetos de origen indígena, y una parte proviene de contextos funerarios: las fichas lo mencionan de forma explícita (*burial*, *mummy*, *funerary*) en al menos 24 de los 615 registros, una cota inferior porque solo 125 tienen descripción curatorial. Los principios CARE para la gobernanza de datos indígenas [@carroll2020] advierten que las políticas de acceso abierto tratan todos los datos por igual, y proponen complementar los principios FAIR [@wilkinson2016] con criterios de beneficio colectivo, autoridad para controlar, responsabilidad y ética. Esta tesis no puede afirmar que los cumple: no hubo consulta con las comunidades de origen, que queda fuera de su alcance.

Lo que la tesis sí hace es acotar el uso y documentarlo. La anotación describe la organización visible y no atribuye significados culturales a motivos ni a composiciones. Las atribuciones de cultura, fecha y procedencia son las de cada museo y se tratan como revisables. Cada registro conserva su institución de origen, su enlace oficial y su licencia, y las imágenes no se redistribuyen. La ficha del corpus, siguiendo el cuestionario de Gebru et al. [@gebru2021] y la lista de preguntas de Lee [@lee2022] para colecciones patrimoniales usadas como datos de aprendizaje automático, indica quién curó y anotó los datos, con qué guía y en qué fechas, qué se descartó y por qué, y para qué usos no está pensado el corpus: la comercialización o imitación de diseños patrimoniales, la clasificación cultural automática sin validación experta y las afirmaciones sobre significado simbólico sin respaldo antropológico o arqueológico.

## 4.13 Limitaciones

- **Un solo curador y anotador.** La estabilidad intra-anotador no sustituye al acuerdo entre personas, y las categorías pueden reflejar la lectura de una persona.
- **Observabilidad inestable.** La frontera entre lo que se ve y lo que no se ve varió entre pasadas, sobre todo en la composición y la simetría, y afecta los bloques que compara el descriptor.
- **Asistencia en la revisión.** La versión 2.1 incluye correcciones que partieron de propuestas automáticas verificadas por el anotador, y la revisión cambia de forma apreciable los *rankings* de M3 (sección 4.10.1).
- **Esfuerzo no medido.** El tiempo de anotación por pieza no se registró, y el estudio no mide el costo de anotar.
- **Vocabulario técnico incompleto.** La categoría «tejido» es genérica, y faltan técnicas características del área andina, como la faz de urdimbre (sección 4.7.3) o el teñido por amarras (se atan partes de la tela o de los hilos para que no absorban el tinte). La técnica no interviene en el descriptor.
- **«Lana» en las fichas.** El vocabulario conserva el término de la fuente (*wool*), que no distingue la especie animal; en la literatura andina se habla de lana de camélido [@desrosiers2013, p. 499], y el término no debe leerse como lana de oveja.
- **Sesgo de conservación.** El clima muy árido de la costa, desde el sur de Lima hasta el norte de Chile, ha permitido conservar artefactos de fibra que en las tierras altas húmedas rara vez sobreviven [@desrosiers2024, pp. 2–3], de modo que las culturas costeras están sobrerrepresentadas en las colecciones.
- **Puntaje de aptitud sin validación externa.** Sus cifras son de desarrollo (sección 4.4.3).
