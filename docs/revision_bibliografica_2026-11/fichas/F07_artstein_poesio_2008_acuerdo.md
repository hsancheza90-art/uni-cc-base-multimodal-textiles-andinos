# F07 · Artstein (2008)

**Inter-Coder Agreement for Computational Linguistics**

| Campo | Valor |
|---|---|
| Autores | Artstein, R.; Poesio, M. |
| Año y sede | 2008. Computational Linguistics 34(4) |
| Identificador | doi:10.1162/coli.07-034-r2 |
| PDF | `pdfs/F07_artstein_poesio_2008_acuerdo.pdf` · https://aclanthology.org/J08-4004.pdf |
| Eje | H. Fiabilidad de la anotación |
| Origen del registro | auditoría (S16), ahora leído en parte |
| Nivel de lectura | parcial: se leyó literalmente hasta la p. 567 (cerca del 36 %); secciones 3–4 y conclusiones solo por resumen automático |

## Qué hace

- **Datos.** Artículo de revisión; ejemplo ilustrativo con 100 enunciados y dos codificadores.
- **Tarea y protocolo.** Cómo medir el acuerdo entre anotadores en la anotación de corpus.
- **Método.** Compara S, pi, kappa, alfa de Krippendorff y kappa ponderado según su modelo de azar; alfa generaliza con una función de distancia.
- **Comparadores.** No aplica.
- **Resultados.** En el ejemplo de la tabla 1: acuerdo observado 0,70, S ≈ 0,40, pi ≈ 0,341, kappa ≈ 0,348 (tabla 2). El resumen sostiene que los coeficientes ponderados convienen a muchas tareas pero son más difíciles de interpretar. Para etiquetas de conjunto hay varias distancias defendibles que dan valores de alfa distintos (sec. 2.6). La introducción recoge la objeción al umbral de 0,67.
- **Limitaciones declaradas.** El texto leído no usa los términos estabilidad ni reproducibilidad ni trata el acuerdo intra-anotador. La discusión de MASI y de umbrales está en la parte no leída literalmente.
- **Código y datos.** No aplica.

## Aporte a la tesis

Fundamenta tres decisiones del informe de estabilidad: un mismo acuerdo observado produce coeficientes muy distintos, así que hay que informar el coeficiente y el acuerdo bruto; los ordinales requieren ponderación (ya se hace con kappa lineal); en los campos múltiples el valor depende de la distancia elegida, de modo que el Jaccard debe declararse como elección y no como estándar. Desaconseja fijar 0,6 como umbral único.

## Cautela al citar

Leer las secciones 3 y 4 en el PDF antes de citar recomendaciones concretas sobre alfa, MASI o umbrales.

---
Leído el 11 de noviembre de 2026 con asistencia computacional. «NV» marca lo que no se vio en el texto literal del documento y debe comprobarse en el PDF antes de citarlo.
