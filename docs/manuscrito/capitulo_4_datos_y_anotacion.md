# 4. Datos y anotación

> **Borrador 0.1, 19 de noviembre de 2026.** Capítulo de la segunda parte de la tesis. Las cifras corresponden a las versiones congeladas del corpus (`corpus-met-cma-aic-v2.0`) y de la anotación (`anotacion-v2.1`). Las marcas **[verificar: …]** señalan afirmaciones que dependen de una obra no leída en el proyecto y deben comprobarse contra la fuente antes de la versión final.

## 4.1 Introducción

Este capítulo describe los datos sobre los que se construye y se evalúa la representación propuesta: de dónde provienen, cómo se seleccionaron, qué unidades los componen y cómo se registró la organización visible de cada textil. Responde a tres exigencias que el primer avance dejó abiertas. La primera es reemplazar el juicio general de «imagen útil» por un criterio de aptitud verificable. La segunda es distinguir el registro museográfico del objeto físico, porque varias fichas pueden mostrar la misma pieza. La tercera es documentar la anotación estructural con la consistencia que realmente alcanza, y no con la que se supone.

El capítulo amplía el corpus del primer avance, que reunía piezas del Metropolitan Museum of Art (MET) y del Cleveland Museum of Art (CMA), con una tercera fuente, el Art Institute of Chicago (AIC). La serie del primer avance se conserva congelada y no se modifica: los cambios que aquí se describen producen una versión nueva y no reescriben la anterior.

## 4.2 Fuentes y procedencia

### 4.2.1 Criterio de selección de fuentes

Una colección se incorpora solo si cumple cuatro condiciones: imágenes en dominio público o con licencia CC0 registrada por objeto; una interfaz de programación pública que permita reconstruir la extracción sin recurrir al raspado de páginas; metadatos curatoriales suficientes para la trazabilidad (identificador, enlace oficial, cultura o procedencia, fecha y material o técnica); y un volumen de piezas andinas que justifique el esfuerzo de integración.

Las tres fuentes incluidas satisfacen esas condiciones (Cuadro 4.1). Se evaluaron y descartaron, por licencia de imagen incompatible o por falta de una interfaz reutilizable, el British Museum, el Museo de Berlín, el Field Museum, el Penn Museum, el Museum of Fine Arts de Boston, las colecciones del Smithsonian (NMAI y NMNH), el Brooklyn Museum y el Los Angeles County Museum of Art. Las colecciones de museos peruanos solo serían accesibles mediante convenio institucional, que excede el plazo del estudio.

**Cuadro 4.1.** Fuentes del corpus v2.

| Fuente | Licencia de la imagen | Particularidades de la extracción |
|---|---|---|
| The Metropolitan Museum of Art (MET) | Dominio público (Open Access) | Parte de la curación MET del primer avance. Fechas en texto libre. Una pieza (MET:312615) ya no tiene imagen en el museo |
| Cleveland Museum of Art (CMA) | CC0 | Consulta conservadora por cultura andina y término textil; una consulta por tipo «Textile» devolvió 2045 registros, casi todos no andinos, y se descartó |
| Art Institute of Chicago (AIC) | CC0; la descripción del museo tiene licencia CC BY 4.0 y se cita | Consultas estructuradas; servicio IIIF limitado al ancho del original |

### 4.2.2 Mediación institucional

Las tres colecciones pertenecen a museos de Estados Unidos. El corpus refleja, por tanto, decisiones ajenas al estudio: qué piezas se adquirieron, cómo se catalogaron, qué se fotografió y con qué encuadre. La distribución por cultura del corpus no estima la de la producción textil andina, sino la de lo que estas instituciones conservan y publican. Las atribuciones culturales y cronológicas son las de cada ficha y se conservan como texto de la fuente, junto a su versión normalizada, sin corregirlas.

Esta mediación tiene consecuencias medibles. Las fichas difieren en qué campos documentan: ninguna de las tres fuentes informa un periodo estructurado; la descripción curatorial existe en 29 de 155 registros MET, 53 de 108 CMA y 43 de 352 AIC; y la cultura falta en 94 registros, todos de AIC. Difieren también en la fotografía: las copias originales de MET y CMA tienen entre 3400 y 4000 píxeles de lado mayor, mientras que el servicio de AIC entrega 1686 píxeles. La sección 4.4.3 muestra que esta diferencia, si no se controla, sesga las medidas de calidad entre museos.

## 4.3 Recolección y candidatura

Cada fuente tiene un colector propio que consulta su interfaz pública y normaliza los registros a un esquema común. Un registro recuperado pasa a ser **candidato** cuando tiene imagen oficial, metadatos mínimos de trazabilidad, evidencia textil (clasificación o material textil, o términos como *textile*, *woven*, *tunic*, *mantle* o *tapestry*) y evidencia andina (Perú, Inca, Paracas, Nasca, Wari, Chancay, Moche, Tiwanaku u otras denominaciones). Los términos se buscan como palabra completa, de modo que una subcadena no produce un falso positivo. Las herramientas de hilado y tejido se excluyen de forma automática, porque son objetos textiles por su función, pero no superficies tejidas.

Ser candidato no implica entrar al corpus: la decisión es manual y sigue el criterio de aptitud de la sección siguiente. Las listas de candidatos se versionan como insumos y no se regeneran sin autorización expresa, porque sobre ellas se tomaron decisiones humanas.

## 4.4 Criterio de aptitud analítica

### 4.4.1 Criterio

El primer avance incluía una pieza en el corpus principal si su imagen era «útil» y tenía «valor computacional». Ese juicio no era reproducible. La segunda parte lo reemplaza por un criterio que se puede comprobar en la fotografía. Se fijó durante la revisión manual de las 508 candidatas de AIC, en octubre de 2026, y se aplicó igual a las tres fuentes:

- **Principal.** Los colores y las figuras del textil se identifican a primera vista.
- **Imagen de referencia** (subconjunto del principal). Además, el textil está completo y su completitud puede verificarse en la fotografía.
- **Complementario** (en los libros de revisión, «secundario»). La imagen no permite identificar bien colores o formas, por ejemplo en una fotografía monocroma o en una pieza muy deteriorada.
- **Descarte.** La pieza no es pertinente o la imagen no sirve para el estudio: plumaria, muñecos, piezas con fecha de inicio posterior a 1532, objetos no textiles o no andinos, herramientas e imágenes inexistentes.

El criterio no exige que la pieza esté entera. El descriptor estructural necesita atributos identificables (colores, módulos, figuras, bandas), y un fragmento legible los conserva. Exigir piezas completas habría desplazado al complementario a las culturas que se conservan sobre todo en fragmentos. Con el criterio adoptado, la proporción de piezas que pasan al principal entre los candidatos de cada cultura se mantiene alta: 92 % en Paracas, 78 % en Wari, 70 % en Chancay y 54 % en Nasca.

La exclusión de las piezas posteriores a 1532 delimita la población al periodo prehispánico. La fecha se interpreta desde el texto de cada ficha; cuando la ficha da un intervalo, se usa su inicio.

### 4.4.2 Reglas verificables

Una parte de las decisiones no requiere juicio y se aplica mediante reglas explícitas, que firman como revisor «auto» y que el revisor humano puede corregir:

| Regla | Decisión | Fundamento |
|---|---|---|
| Plumaria (material o título), muñecos, fecha de inicio posterior a 1532 | Descarte | Pertinencia definida por el criterio |
| Posible figurilla («Figure» en singular, sin complemento) | Revisión manual | Prudencia: «Fragment with Figure» es un textil con una figura representada |
| Sin imagen o textil de menos de 300 píxeles | Descarte | No hay atributos que identificar |
| Fotografía monocroma | Complementario | El color no es identificable |

Una regla automática nunca suaviza una decisión manual: si el revisor ya decidió, la regla no la reemplaza.

### 4.4.3 Puntaje de aptitud como apoyo a la revisión

Para acelerar la revisión de fuentes nuevas se desarrolló un puntaje de aptitud. Sobre la copia de evaluación de cada imagen (1600 píxeles de lado mayor), el textil se separa del fondo y se miden rasgos de la fotografía (nitidez, resolución, croma), del color (número de tonos, separabilidad y contraste cromáticos), de la forma del diseño (densidad de bordes cromáticos) y de la pieza (compacidad, lagunas, fragmentos, contacto con el encuadre). Con los motivos que el revisor escribió para cada decisión se ajustan regresiones logísticas para la legibilidad del color, la legibilidad de las formas, la completitud y la condición de imagen de referencia.

Dos decisiones de medición deben declararse. La nitidez depende de la escala de la copia: reducir una imagen a la mitad la multiplica por un factor de entre 1,2 y 1,55. Por eso la nitidez que se compara entre museos se mide con el textil llevado a 600 píxeles de lado mayor. Además, cuando el textil llena el encuadre, su contorno no es visible, y las medidas de contorno dejan de informar sobre la completitud.

Las cifras del puntaje deben leerse como **validación de desarrollo**. En AIC, con validación cruzada de cinco pliegues, el área bajo la curva ROC fue de 0,94 para el color, 0,90 para las formas, 0,89 para la completitud y 0,91 para la separación entre principal y descarte por imagen. Estas cifras son optimistas por tres motivos: la estandarización de las medidas usa todas las imágenes antes de dividir en pliegues; los pliegues se forman por registro y no por pieza, de modo que dos vistas de un mismo objeto pueden quedar a ambos lados; y los umbrales se eligen con las mismas predicciones que se informan. Un diagnóstico que reserva un museo completo dio un área de 0,56 en AIC, 0,56 en MET y 0,93 en CMA.

La transferencia se puso a prueba con una validación ciega: el revisor clasificó 40 imágenes de MET y CMA sin ver el puntaje ni la decisión anterior. El acuerdo entre el revisor y el modelo calibrado solo con AIC fue κ = 0,56 (0,44 en MET y 0,66 en CMA), por debajo del umbral de 0,6 fijado de antemano. En consecuencia, en MET y CMA solo se aplicaron las reglas de la sección 4.4.2 y las decisiones del revisor, y no las sugerencias del modelo. El diagnóstico mostró que la relación entre las medidas y la legibilidad cambia con la fotografía y con los tipos de pieza de cada museo. Al recalibrar con las tres fuentes, la separación entre piezas útiles y el resto, fuera de pliegue, fue de 0,91 en AIC, 0,76 en MET y 0,83 en CMA. Como esa muestra ya forma parte del ajuste, afirmar que el puntaje transfiere a una fuente nueva exige otra muestra ciega. En esta tesis el puntaje se presenta como apoyo exploratorio de la curación, no como un clasificador validado.

## 4.5 Composición del corpus v2

El Cuadro 4.2 resume el resultado de la curación. Las 874 decisiones de inclusión o descarte tienen procedencia mixta: 227 provienen de reglas automáticas documentadas y 647 de etapas de curación manual. No equivalen a 874 objetos independientes, porque varias fichas pueden mostrar la misma pieza (sección 4.6).

**Cuadro 4.2.** Corpus v2 por fuente y subconjunto (versión `corpus-met-cma-aic-v2.0`).

| Fuente | Principal | Complementario | Descartados | Total |
|---|---:|---:|---:|---:|
| MET | 130 | 25 | 65 | 220 |
| CMA | 104 | 4 | 38 | 146 |
| AIC | 228 | 124 | 156 | 508 |
| Total | 462 | 153 | 259 | 874 |

El consolidado v2 reúne el principal y el complementario: 615 registros, todos con imagen útil y licencia abierta (dominio público en MET, CC0 en CMA y AIC). Cada registro conserva el texto de la fuente junto a su versión normalizada (por ejemplo, la técnica tal como la escribe el museo y su código en el vocabulario controlado), e indica si cada valor normalizado proviene de la curación, de una regla o de la anotación. Las imágenes no se redistribuyen: se identifican por su enlace oficial y por la suma SHA-256 de la copia usada.

Las piezas del principal se reparten de manera desigual entre culturas y museos. AIC aporta casi la mitad del principal, concentra los registros sin cultura y reúne la mayor parte de las piezas Chancay; MET aporta la mayor parte de las piezas Paracas y Wari. El diseño experimental tiene en cuenta esta heterogeneidad al estratificar por museo (capítulo 7).

## 4.6 Unidades: registro, imagen y grupo

El primer avance trataba como una sola cosa la pieza, su ficha y su fotografía. La segunda parte las separa, porque confundirlas invalida cualquier evaluación de recuperación: si dos fichas muestran el mismo objeto, recuperar una a partir de la otra no prueba nada sobre la representación.

- El **registro** es la ficha de un museo, identificada por `FUENTE:id_fuente`.
- La **imagen** es la copia de evaluación de la fotografía de referencia del registro.
- El **grupo** reúne los registros que muestran un mismo objeto o partes de él: la misma fotografía, vistas distintas o fragmentos de una misma pieza.

Los grupos se construyeron en dos pasos. Primero, cinco señales automáticas propusieron pares candidatos: imagen idéntica; número de inventario con la misma base y sufijo de parte; descripción idéntica de 40 caracteres o más; distancia de Hamming entre huellas perceptuales (dHash) menor o igual a 4; y similitud coseno entre los vectores de OpenCLIP de al menos 0,95, o de 0,93 entre museos distintos. Las señales propusieron 100 pares distintos, 3 de ellos entre museos. Después, el investigador decidió cada par: unió 65 y separó 35. Los 13 pares de imagen idéntica se unieron mediante una regla automática. Los grupos son las componentes conexas del grafo cuyos vértices son los registros y cuyas aristas son los pares unidos.

El resultado son 577 grupos para los 615 registros: 555 registros aislados y 22 grupos de dos a siete registros. Las 150 piezas del núcleo de anotación (sección 4.8) pertenecen a 146 grupos. El grupo, y no el registro, es la unidad de partición entre desarrollo y prueba: una comprobación automática verifica que ningún grupo quede repartido entre ambas particiones.

## 4.7 Esquema de anotación estructural

### 4.7.1 Capas y atributos

La anotación registra lo que una persona observa en la fotografía de cada pieza. No interpreta el significado de los motivos ni sustituye el juicio de especialistas en arqueología o etnografía textil. Cada pieza se anota en cinco capas y en un orden fijo:

| Capa | Atributos |
|---|---|
| Cromática | color dominante, colores presentes, contraste, densidad visual |
| Estructural | composición, eje de bandas, secuencia de bandas, borde, centro |
| Repetición y simetría | repetición, simetría |
| Iconográfica | motivos, familia iconográfica, motivo principal |
| Correcciones | tipo de objeto, tipo de superficie, material, técnica y estado de la imagen, cuando el valor de la ficha es incorrecto |

Los valores pertenecen a un vocabulario controlado único, que extiende los cuadros 6.3 a 6.8 del primer avance. En los datos se guardan códigos sin tildes (`fibra_de_camelido`), y en el texto de la tesis se usan las etiquetas correspondientes.

### 4.7.2 Valores y estados

La anotación distingue el valor de un atributo de su estado de observación. La distinción es sustantiva: un descriptor que confunde «el rasgo no está» con «el rasgo no se ve» compara piezas por la calidad de su fotografía y no por su organización. Cuando un atributo no tiene valor, se registra uno de tres estados:

- **Ausente.** La superficie pertinente se ve y el rasgo no está; por ejemplo, una pieza sin bandas.
- **No observable.** La superficie pertinente no se ve, por fragmentación, recorte, pliegue o encuadre parcial.
- **Desconocido.** La superficie se ve, pero el anotador no puede decidir entre valores.

El estado ocupa la celda completa y no se combina con valores. Una celda vacía significa «no anotado» y nunca «ausente». La categoría `no_determinada` de la familia iconográfica y del tipo de banda no es un estado: indica que se ve un rasgo que no corresponde a ninguna categoría del vocabulario.

La **regla de los treinta segundos** limita la presión por completar: si un atributo genera más de treinta segundos de duda, se anota como desconocido y la duda se describe en las observaciones. Un valor forzado entraría en el descriptor como si fuera un dato.

### 4.7.3 La palabra de bandas

La secuencia de bandas es la variable sobre la que descansa la segunda hipótesis del estudio (capítulo 5). Una **banda** es una franja que atraviesa toda la superficie visible, perpendicular al eje de lectura y delimitada por un cambio de color o de diseño. No son bandas las cenefas perimetrales, que se registran como borde, ni las filas o columnas de una retícula, ni los paneles, que se registran en la composición. La composición dominante no decide si hay bandas: una pieza organizada en campo, paneles o retícula puede tener franjas que la cruzan de lado a lado, y esas franjas forman su palabra.

Cada banda se registra por su tipo (lisa, geométrica, figurativa, mixta o no determinada), en el orden del eje, y la secuencia se escribe como una palabra, por ejemplo `lisa > geometrica > figurativa > geometrica > lisa`. Un tramo que no se ve por rotura o pliegue se registra como laguna y el descriptor lo enmascara. No se registra el color ni el ancho de cada banda: el color ya está en la capa cromática y estimar el ancho a ojo daría una precisión aparente.

El eje es el de la fotografía y no el de la urdimbre. La anotación trabaja sobre la imagen y no distingue las listas de urdimbre de las franjas de trama ni de los registros bordados; registra las bandas por su aspecto visible. Esta decisión tiene una consecuencia en piezas que el museo fotografía en una orientación distinta de la de uso, como las túnicas de tapiz, en las que la urdimbre queda horizontal cuando la prenda se viste [verificar: Rowe, 1977, o fuente equivalente sobre la orientación de la urdimbre en túnicas wari e inca]. Por eso el eje no entra en el descriptor (capítulo 5).

### 4.7.4 Simetría y repetición

El vocabulario conserva dos categorías del primer avance que describen la repetición por traslación y que la primera anotación no separaba con nitidez. Se distinguen por la dimensión de la repetición. Es **traslacional** la de un motivo que se desplaza en una sola dirección y forma un friso continuo. Es **repetición modular** la de un módulo con contorno propio (celda, cuadro o panel) que se repite como unidad en dos dimensiones, como en una retícula o un damero. La distinción sigue la que hace el análisis de simetría de patrones entre los grupos de friso y los del plano [verificar: Washburn y Crowe, 1988, capítulo sobre patrones de una y dos dimensiones]. El descriptor no clasifica las piezas por grupo cristalográfico: registra la simetría como un atributo nominal anotado.

## 4.8 Núcleo de anotación

Anotar las 462 piezas del principal excede el plazo del estudio. Se anotó un **núcleo** de 150 piezas, elegido por muestreo estratificado:

1. La cuota de cada fuente es proporcional a su peso en el principal y se reparte por el método de los mayores restos: MET 42, CMA 34 y AIC 74.
2. Dentro de cada fuente, los estratos combinan la cultura agrupada (Paracas, Nasca, Wari, Chancay, Inca, Chimú, otras y sin cultura) con la banda que sugiere el puntaje de aptitud. La banda no decide la inclusión, porque todas las piezas están en el principal por decisión del revisor. Solo asegura que el núcleo cubra fotografías de calidad distinta.
3. Dentro de cada estrato se eligen las piezas con menor suma SHA-256 de la cadena «semilla:identificador», con la semilla 20261020. La selección no depende de la versión del lenguaje ni de las bibliotecas.
4. Las piezas se reparten en turno entre cinco lotes de 30, de modo que cada lote replique la composición del núcleo, y ningún lote supera el 60 % de una sola fuente.

La anotación se hizo por lotes, uno por sesión, y concluyó el 5 de noviembre de 2026. Las piezas del principal que no entraron en el núcleo quedan sin anotar.

## 4.9 Estabilidad de la anotación

### 4.9.1 Diseño

El estudio tiene un solo anotador. Sin una segunda persona no puede medirse la reproducibilidad de la anotación, es decir, el acuerdo entre anotadores, pero sí su **estabilidad**: el acuerdo del anotador consigo mismo en el tiempo. Abercrombie et al. (2025) encontraron que menos del 0,07 % de los artículos de la ACL Anthology informa el acuerdo intra-anotador, y que incluso con dos semanas de intervalo los anotadores cambiaban cerca de una de cada cuatro etiquetas. Beijbom et al. (2015) muestran, en la anotación de imágenes por especialistas, que la estabilidad varía mucho de una categoría a otra, lo que aconseja informarla por atributo y no como un número global.

El anotador volvió a anotar a ciegas las 30 piezas del lote 1, en otro orden y al menos siete días después de la primera pasada, sin consultar la primera anotación. Para cada atributo se usa la medida que corresponde a su tipo: kappa de Cohen en los nominales, kappa ponderado lineal en los ordinales, índice de Jaccard medio en los de valores múltiples y, en la secuencia de bandas, la coincidencia exacta y la similitud de edición 1 − d/máx(ℓ₁, ℓ₂), con d la distancia de Levenshtein. La secuencia no tiene un acuerdo esperado al azar definido, de modo que no se le calcula kappa. Siguiendo a Artstein y Poesio (2008), se informa el acuerdo observado junto a cada coeficiente, porque un mismo acuerdo bruto puede producir coeficientes muy distintos. El umbral κ ≥ 0,6 se usa solo como señal para revisar la definición de un atributo, no como criterio de aprobación. Queda por debajo del 0,8 que esos autores proponen cuando es imprescindible fijar un umbral.

### 4.9.2 Resultados

**Cuadro 4.3.** Estabilidad intra-anotador en el lote 1 (30 piezas), sobre los pares observados en las dos pasadas.

| Capa | Atributo | Medida | n | Acuerdo observado | Coeficiente |
|---|---|---|---:|---:|---:|
| Cromática | Color dominante | κ | 29 | 0,966 | 0,949 |
| Cromática | Contraste | κ ponderado | 30 | 0,917 | 0,736 |
| Cromática | Densidad visual | κ ponderado | 30 | 0,933 | 0,776 |
| Cromática | Colores | Jaccard medio | 30 | 0,770 | — |
| Estructural | Composición | κ | 24 | 0,875 | 0,837 |
| Estructural | Eje de bandas | κ | 24 | 0,833 | 0,738 |
| Estructural | Secuencia de bandas | Similitud de edición | 24 | 0,797 | 17 de 24 idénticas |
| Estructural | Borde | κ (sí/no) | 24 | 0,875 | 0,750 |
| Estructural | Centro | κ (sí/no) | 25 | 0,800 | 0,490 |
| Repetición y simetría | Repetición | κ ponderado | 27 | 0,944 | 0,799 |
| Repetición y simetría | Simetría | κ | 23 | 0,826 | 0,765 |
| Iconográfica | Motivos | Jaccard medio | 30 | 0,844 | — |
| Iconográfica | Familia iconográfica | κ | 29 | 0,828 | 0,751 |
| Iconográfica | Motivo principal | κ | 21 | 0,810 | 0,772 |

Diez de los once atributos con kappa superan la señal de 0,6. El atributo **centro** queda por debajo (κ = 0,49): se mantuvo en la anotación y en el descriptor, porque retirarlo a la vista de un solo lote de 30 piezas sería una decisión tomada con poca evidencia. Su baja estabilidad se declara como amenaza a la validez. En los atributos de valores múltiples, el desacuerdo se concentra en etiquetas concretas: el amarillo (κ = 0,48) y el ocre (κ = 0,28) entre los colores, y lo abstracto (κ = 0,47) entre los motivos. Son categorías de frontera difusa en la fotografía.

El cuadro muestra solo los pares que las dos pasadas pudieron observar, y esa restricción oculta una segunda fuente de variabilidad: la frontera entre «se ve» y «no se ve». Para la composición, el anotador consideró observable la misma pieza en las dos pasadas en 24 casos, solo en la primera en 4 y solo en la segunda en 2. El acuerdo sobre la observabilidad, corregido por azar, es nulo (κ = −0,10), aunque el acuerdo bruto sea de 0,80. Como la máscara de observabilidad decide qué bloques compara el descriptor (capítulo 5), esta inestabilidad lo afecta directamente y se declara como limitación.

La decisión más inestable fue si una pieza tiene bandas: cuatro piezas pasaron de no tener bandas a una secuencia de dos a seis. La guía definía los tipos de banda, pero no qué cuenta como banda. La definición de la sección 4.7.3 se escribió a partir de este hallazgo.

### 4.9.3 Adjudicación del lote re-anotado

Cuando las dos pasadas del lote 1 difieren, prevalece la re-anotación, hecha con más experiencia y con la guía ya estabilizada. La primera pasada solo sirve para medir la estabilidad. En consecuencia, el lote 1 de la versión final refleja la segunda lectura y los lotes 2 a 5 la primera, con las correcciones de la sección siguiente.

## 4.10 Revisión de criterios y versión 2.1

La definición de banda y la distinción entre traslación y repetición modular se escribieron después de anotar los lotes 2 a 5. Para no congelar una anotación hecha con criterios distintos de los vigentes, el anotador volvió a mirar las piezas afectadas antes de cerrar la versión.

**Selección.** Una regla automática seleccionó 108 de las 120 piezas de los lotes 2 a 5: las 52 con palabra de bandas, las 85 con simetría traslacional o modular, las 32 cuyas observaciones registraban una duda sobre un atributo que usa el descriptor y las 22 cuyas observaciones pedían verificar que la imagen correspondía al registro. Una misma pieza podía cumplir varias condiciones. Quedaron fuera las dudas sobre atributos que el descriptor no usa (46 piezas) y los huecos del vocabulario (16 piezas), que se declaran como limitación.

**Procedimiento asistido.** Para cada pieza seleccionada, un modelo de visión y lenguaje generó una propuesta (confirmar o corregir, con los valores y el criterio aplicado) a partir de la imagen, la anotación vigente, las observaciones del anotador y el texto de los criterios. El modelo no tuvo acceso a rankings, juicios de relevancia ni resultados de ningún sistema. Ninguna propuesta se aplicó por sí misma. El anotador verificó cada una frente a la imagen, la corrigió cuando hizo falta y la firmó. De las 108 decisiones verificadas, 58 coinciden con la propuesta y 50 la modifican. En total, el anotador confirmó 66 piezas y corrigió 42, con 173 valores modificados. La revisión se registró con el valor anterior, el valor nuevo y el motivo de cada cambio.

**Criterios fijados durante la revisión.** Al verificar las propuestas, el investigador fijó cuatro criterios que la guía no resolvía:

- las esquinas y los fragmentos con decoración perimetral se registran como borde;
- una tira con recuadros sucesivos de contorno propio es una composición en paneles, sin palabra de bandas;
- una figura única es un campo central si un fondo la enmarca, y una composición libre si la pieza es la propia figura;
- varias piezas sin relación en una sola fotografía llevan sus atributos estructurales como no observables.

**Identidad de las imágenes.** La revisión detectó que ocho anotaciones describían la imagen de otro registro: seis formaban un ciclo y dos estaban intercambiadas. Se comprobó con las imágenes y con los números de inventario que las imágenes correspondían a sus registros y que eran las anotaciones las desplazadas. Cada anotación se trasladó a la fila del registro cuya imagen describía y se revisó con los criterios vigentes. Las doce piezas que no entraron en la revisión se compararon con sus imágenes y todas coincidían.

**Efecto sobre la anotación.** Las correcciones redujeron las piezas con composición en bandas de 48 a 35 y aumentaron las de paneles de 24 a 41. Las piezas con palabra de bandas pasaron de 66 a 53. El efecto principal fue separar las franjas que cruzan la pieza de las tiras de recuadros, que la primera anotación había registrado como bandas.

**Observaciones.** Las observaciones en texto libre de la primera anotación se redactaron de nuevo, también con asistencia, para que describieran solo lo que se ve en la imagen y expresaran las dudas como posibilidad. Ningún valor anotado cambió por esta redacción.

**Congelación.** La anotación del núcleo quedó congelada como versión 2.1 el 17 de noviembre de 2026. Su composición es la del Cuadro 4.4. Desde entonces, una comprobación automática compara en cada ejecución la anotación exportada con la copia congelada y su suma SHA-256: un cambio posterior en los libros de anotación detiene la regeneración del corpus. Una versión nueva de la anotación requiere una decisión registrada y una copia nueva.

**Cuadro 4.4.** Composición dominante en la anotación v2.1 del núcleo (150 piezas).

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

La asistencia se limitó a verificar anotaciones existentes frente a criterios escritos por el investigador: no generó anotaciones nuevas ni definió criterios. Ninguna propuesta se aplicó sin la verificación y la firma del anotador, y el procedimiento de congelación impone esa condición de forma automática: la versión no puede cerrarse mientras quede una propuesta sin firmar. El modelo no tuvo acceso a rankings, juicios de relevancia ni resultados de los sistemas evaluados, y no es ninguno de ellos, de modo que no podía orientar la anotación a favor de un sistema. La estabilidad informada en la sección 4.9 se midió entre dos pasadas del anotador hechas sin asistencia. El esquema corresponde al modo semiautomático de anotación de imágenes, en el que la persona confirma o corrige una propuesta (Beijbom et al., 2015).

El procedimiento tiene un riesgo conocido: quien verifica una propuesta tiende a aceptarla [verificar: Parasuraman y Manzey, 2010]. Las 66 confirmaciones coinciden con la propuesta, y no puede saberse cuántas habría confirmado el anotador sin ella. Por eso se informa la proporción de decisiones que modificaron la propuesta (50 de 108) y se midió cuánto depende el descriptor de la revisión.

**Análisis de sensibilidad.** Se compararon los rankings de desarrollo de M3 y de su control sin orden calculados con dos anotaciones: la anterior a la revisión, con las ocho anotaciones desplazadas trasladadas a su registro pero sin corregir, y la versión 2.1. La revisión cambió al menos un atributo del descriptor en 46 de las 150 piezas, sobre todo la secuencia de bandas y la simetría (34 piezas cada una), la composición (28) y el borde (24). En las diez consultas de desarrollo, los diez primeros resultados de M3 comparten entre 4 y 9 piezas entre ambas versiones, y la correlación de Spearman entre los rankings completos va de 0,56 a 0,91.

La revisión, por tanto, no es neutra para el descriptor: cambia de forma apreciable qué piezas recupera M3. Este resultado no indica cuál de las dos anotaciones es más fiel a la imagen. Indica que las conclusiones sobre M3 dependen de la versión de la anotación, y por eso la versión se fija, se congela y se declara. Las métricas de relevancia de ambas versiones no se comparan como evidencia, por dos razones. El conjunto de pares juzgados se construyó con la versión 2.1, de modo que la anterior tiene candidatos sin juicio. Además, la revisión de la anotación y la de los juicios de desarrollo usaron asistencia de la misma familia de modelos, y una coincidencia entre ambas podría reflejar ese criterio compartido.

## 4.11 Versionado y reproducibilidad

Cada decisión humana (de curación, de agrupamiento o de anotación) se registra en un libro de revisión con su autor y su fecha, y no se edita a mano ningún archivo derivado. Un único punto de entrada regenera, sin acceso a la red, todos los archivos derivados a partir de esos libros y de los insumos versionados (listas de candidatos, medidas de imagen, vectores de los modelos). Una batería de pruebas automáticas verifica que la regeneración coincide con lo versionado. El flujo falla si un conteo no coincide con el esperado, de modo que un cambio curatorial no puede pasar inadvertido.

Cada entrega del corpus se asocia a una etiqueta del repositorio y a las sumas SHA-256 de sus archivos: `corpus-met-cma-v1.2` para la serie del primer avance, `corpus-met-cma-aic-v2.0` para el consolidado v2 y `anotacion-v2.1` para la anotación congelada. Los experimentos citan la etiqueta que usaron. La serie v1 lee copias congeladas de sus insumos y se regenera idéntica aunque cambien los libros de la v2.

## 4.12 Uso ético y gobernanza de los datos

La licencia abierta permite reutilizar las imágenes, pero no agota la pregunta sobre su uso. Los textiles del corpus son objetos de origen indígena, y una parte proviene de contextos funerarios. Las fichas lo mencionan de forma explícita en al menos 24 de los 615 registros del consolidado, mediante términos como *burial*, *mummy* o *funerary*. Solo 125 registros tienen descripción curatorial, de modo que esa cifra es una cota inferior. Los principios CARE para la gobernanza de datos indígenas (Carroll et al., 2020) advierten que las políticas de acceso abierto tratan todos los datos por igual, y proponen complementar los principios FAIR (Wilkinson et al., 2016) con criterios de beneficio colectivo, autoridad para controlar, responsabilidad y ética. Esta tesis no puede afirmar que los cumple: no hubo consulta con las comunidades de origen, y esa consulta queda fuera de su alcance.

Lo que la tesis sí hace es acotar el uso y documentarlo:

- La anotación describe la organización visible y no atribuye significados culturales a motivos ni a composiciones.
- Las atribuciones de cultura, fecha y procedencia son las de cada museo, se conservan junto a su normalización y se tratan como revisables.
- Cada registro conserva su institución de origen, su enlace oficial y su licencia. La descripción de AIC, con licencia CC BY 4.0, se cita.
- Las imágenes no se redistribuyen: se obtienen de las fuentes oficiales.
- La ficha del corpus declara, siguiendo el cuestionario de Gebru et al. (2021), quién curó y anotó los datos, con qué guía y en qué fechas, qué se descartó y por qué, y para qué usos no está pensado el corpus. Entre esos usos excluidos están la comercialización o imitación de diseños patrimoniales, la clasificación cultural automática sin validación experta y las afirmaciones sobre significado simbólico sin respaldo antropológico o arqueológico.

## 4.13 Limitaciones

- **Un solo curador y anotador.** La estabilidad intra-anotador no sustituye al acuerdo entre personas. Las categorías pueden reflejar la lectura de una persona.
- **Observabilidad inestable.** La frontera entre lo que se ve y lo que no se ve varió entre pasadas, sobre todo en la composición y la simetría, y afecta los bloques que compara el descriptor.
- **Asistencia en la revisión.** La versión 2.1 incluye correcciones que partieron de propuestas automáticas verificadas por el anotador. Coinciden con la propuesta 58 de las 108 decisiones, y la revisión cambia de forma apreciable los rankings de M3 (sección 4.10.1).
- **Esfuerzo no medido.** El tiempo de anotación por pieza no se registró. El costo de anotar se informará como estimación.
- **Vocabulario técnico incompleto.** La categoría «tejido» es genérica, y faltan técnicas diagnósticas del área andina, como la cara de urdimbre, las urdimbres complementarias, las urdimbres y tramas discontinuas, la gasa, el teñido por amarras y el anillado [verificar: Emery, 1966, para la terminología de estructuras]. La técnica no interviene en el descriptor estructural.
- **«Lana» en las fichas.** El vocabulario conserva el término de la fuente. En piezas prehispánicas, *wool* designa por lo general fibra de camélido, porque la oveja llegó con la conquista [verificar: fuente sobre fibras en textiles prehispánicos].
- **Sesgo de conservación y de colección.** La distribución por cultura refleja lo que los museos conservan y fotografían, y las culturas de la costa, donde la conservación es mejor, están sobrerrepresentadas [verificar: fuente sobre condiciones de conservación en la costa peruana].
- **Puntaje de aptitud sin validación externa.** Sus cifras son de desarrollo; su transferencia a una fuente nueva no está demostrada.

## 4.14 Cierre del capítulo

El corpus v2 amplía el del primer avance con una tercera fuente, reemplaza el juicio de utilidad por un criterio verificable y separa el registro del objeto mediante grupos decididos por el investigador. La anotación estructural del núcleo distingue el valor del estado de observación, define con precisión qué cuenta como banda y declara su estabilidad atributo por atributo. Cuando un criterio cambió, el cambio se aplicó antes de congelar la versión, con registro de cada adjudicación. Sobre esta versión congelada se define el descriptor del capítulo 5 y se diseña la evaluación del capítulo 7.

## Referencias

Abercrombie, G., Dinkar, T., Cercas Curry, A., Rieser, V., & Hovy, D. (2025). Consistency is key: Disentangling label variation in natural language processing with intra-annotator agreement. En *Proceedings of the 4th Workshop on Perspectivist Approaches to NLP (NLPerspectives 2025)* (pp. 63–74). https://doi.org/10.18653/v1/2025.nlperspectives-1.6

Artstein, R., & Poesio, M. (2008). Inter-coder agreement for computational linguistics. *Computational Linguistics, 34*(4), 555–596. https://doi.org/10.1162/coli.07-034-R2

Beijbom, O., Edmunds, P. J., Roelfsema, C., et al. (2015). Towards automated annotation of benthic survey images: Variability of human experts and operational modes of automation. *PLoS ONE, 10*(7), e0130312. https://doi.org/10.1371/journal.pone.0130312 [verificar: lista completa de autores]

Carroll, S. R., Garba, I., Figueroa-Rodríguez, O. L., et al. (2020). The CARE principles for Indigenous data governance. *Data Science Journal, 19*, 43. https://doi.org/10.5334/dsj-2020-043 [verificar: lista completa de autores]

Gebru, T., Morgenstern, J., Vecchione, B., Vaughan, J. W., Wallach, H., Daumé III, H., & Crawford, K. (2021). *Datasheets for datasets* (arXiv:1803.09010v8). arXiv. https://arxiv.org/abs/1803.09010

Wilkinson, M. D., Dumontier, M., Aalbersberg, I. J., Appleton, G., Axton, M., Baak, A., et al. (2016). The FAIR guiding principles for scientific data management and stewardship. *Scientific Data, 3*, 160018. https://doi.org/10.1038/sdata.2016.18 [verificar: lista completa de autores]

**Obras citadas con la marca [verificar] (sin ficha de lectura en el proyecto):**

Emery, I. (1966). *The primary structures of fabrics: An illustrated classification*. The Textile Museum.

Parasuraman, R., & Manzey, D. H. (2010). Complacency and bias in human use of automation: An attentional integration. *Human Factors, 52*(3), 381–410. https://doi.org/10.1177/0018720810376055 [verificar: leer antes de citar]

Rowe, A. P. (1977). *Warp-patterned weaves of the Andes*. The Textile Museum. [verificar: título, editorial y pertinencia]

Washburn, D. K., & Crowe, D. W. (1988). *Symmetries of culture: Theory and practice of plane pattern analysis*. University of Washington Press.
