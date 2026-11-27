# Relación de cambios: informe de revisión final del 27 de noviembre de 2026

Respuesta al «Informe de revisión final del proyecto de tesis 2» (pendiente de conformidad por B1-01 y B1-02), sobre el commit `4ddab6d`. Versión corregida: commit `d7e7df2`, archivos `MCC702_informe_seminario_II_2026-11-27.docx` y `.pdf`.

No se modificaron datos, anotaciones, consultas, rankings, juicios, pesos, código experimental ni resultados sellados, y las cifras de H1, H2 y H3 no cambian. `git diff --stat 4ddab6d..d7e7df2` solo muestra cambios en `docs/`. Los tres contraejemplos del informe se comprobaron con la implementación del repositorio, sin modificarla: disimilitud agregada 1/4 con orden frente a 1/3 sin orden; inversión del orden relativo con la consulta `aab` y los candidatos `a` y `aacc`; nDCG de 1 a 0,33735.

## B1-01. Alcance de la proposición 5.6

| Ubicación | Antes | Ahora |
|---|---|---|
| Sección 5.8.3, título de la proposición 5.6 | «el control acota inferiormente a la distancia con orden» | «en el bloque de bandas, el control acota inferiormente a la distancia con orden». La demostración no cambia |
| Sección 5.8.3, interpretación | «M3 refina a su control… autoriza a leer una diferencia entre M3 y M3-sin-orden como efecto del orden» | La proposición compara la distancia entre palabras con la distancia entre histogramas de tipos y su alcance es ese bloque. El control omite además el bloque de adyacencias y cambia la normalización, de modo que la disimilitud agregada puede ser mayor o menor y el orden relativo de dos candidatos puede invertirse. El efecto sobre la recuperación se establece empíricamente en H2 |
| Sección 5.12, Cuadro 5.5, fila H2 | «Que M3 refina a su control y que la única diferencia entre ambos es el orden» | Propiedad por bloque y lo que cambia el control (bandas, adyacencias y normalización), sin refinamiento de la disimilitud agregada ni del orden de los candidatos; la comparación entre M3 y M3-sin-orden queda como empírica |
| Sección 5.13 | «pueden diferir en grado… pero rara vez en el orden relativo»; «con tan pocos pares en que el orden puede cambiar la posición relativa…» | Se conservan los conteos (53, 1378, 41, 25 y 3) como coincidencias que el control no distingue; se indica que no acotan los cambios de posición |
| Sección 9.3 | «Es en esos pares, y casi solo en ellos, donde el orden puede cambiar la posición relativa de dos candidatos»; «casi todas las secuencias se deducen de su inventario» | Se retira la inferencia; los conteos describen la galería y no acotan las inversiones |
| Secciones 7.8 y 11.3 (H2) | Conteo de 25 pares presentado como margen del orden | Se precisa que es un dato descriptivo de la galería, no una cota de los cambios de posición |
| Sección 10.1, OE3 | «el descriptor con orden refina a su control»; «control que conserva todo salvo el orden» | Se conserva que se definió un descriptor con propiedades demostradas; la cota pertenece al bloque de bandas y el efecto sobre la recuperación se evaluó empíricamente en H2 |
| Secciones 1.5 y 10.3 | «control que separa el orden de las bandas del inventario de sus tipos» | «control sin orden basado en el inventario de sus tipos» |
| Sección 5.8.3, definición 5.15 | «Es la única diferencia con M3» | No hay otra diferencia en la definición, pero al omitir un bloque cambia además la normalización |
| Sección 5.13, título y apertura | «Margen del orden en el corpus»; «El margen que tenía H2… podía medirse» | «Palabras de bandas y coincidencias de inventario en el corpus»; la composición de la galería «podía describirse» |
| Secciones 7.8 y 9.3 | «El margen del orden es estrecho por construcción»; «El corpus ofrece poco margen al orden»; «el inventario determina casi siempre la secuencia» | El subgrupo en que el orden puede actuar es pequeño; pocas piezas tienen palabra de bandas; la simetría se presenta como hipótesis |
| Capítulos 1, 2, 3 y 7 (A7) | El control «permite atribuir una eventual diferencia a la secuencia»; «separa la secuencia de la composición por tipos» | El control sustituye la palabra por el histograma y omite las adyacencias; contrasta la secuencia y las adyacencias con el inventario |
| Capítulo 6 y anexo A | «cota del control sin orden» | «cota del control sin orden en el bloque de bandas» |

## B1-02. nDCG y juicios parciales de relevancia

| Ubicación | Antes | Ahora |
|---|---|---|
| Sección 3.8 | La unión de los diez primeros «protege a M3 y M4 del sesgo conservador»; «el sesgo es conservador» | Evita que M3 y M4 queden entre los sistemas ausentes del *pool*; la dirección del sesgo se atribuye a Buckley et al. en su estudio |
| Sección 7.6.2 | «su nDCG@10 no depende de ese supuesto…»; la unión «protege a M3 y M4 del sesgo del *pooling*» | La ganancia del top 10 de los sistemas de H1 y H2 está juzgada por completo, pero el ordenamiento ideal puede quedar incompleto; el nDCG@10 con juicios parciales no es una cota inferior. La unión evita que M3 y M4 queden entre los sistemas ausentes del *pool* |
| Sección 8.2 | «sus métricas son, por tanto, cotas inferiores» | Estimaciones bajo los juicios disponibles, que con juicios completos podrían cambiar en cualquier dirección |
| Sección 8.5 | «de modo que es una cota inferior» (0,105) | Se conservan 0,105 y el 39,7 %; la cobertura parcial limita la comparación con 0,347 |
| Sección 8.6 y Cuadro 8.6 | «sin sus aportes exclusivos, la ventaja de M4 sobre M2 sería mayor… H1 no está favorecida por el *pool*» | M4 baja 0,002 (pequeño, pero distinto de cero) y M2, 0,049; cada retiro cambia un conjunto distinto de juicios y mide sensibilidad, no el signo del sesgo |
| Sección 9.1 | «retirarlos no cambia su puntuación… Si el *pool* sesgara la comparación, lo haría a favor de M2» | Se retiran ambas afirmaciones con la misma redacción que 8.6 |
| Sección 11.2, *pooling* | «las comparaciones de H1 y H2 no dependen de juicios faltantes… sus valores son cotas inferiores» | La cobertura completa del top 10 de los siete *rankings* del *pool* no equivale a relevancias exhaustivas; la ganancia ideal de H1 y H2 puede depender de juicios faltantes; las variantes con cobertura parcial son estimaciones que piden más cautela |

## Otros cambios

- Portada: nota del asesor (20), código UNI del tesista y líneas de firma del asesor y del tesista.
- Decisión R43 en `docs/registro_decisiones.md` y en el anexo B.
