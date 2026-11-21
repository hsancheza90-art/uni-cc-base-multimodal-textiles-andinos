# F07 · Artstein (2008)

**Inter-Coder Agreement for Computational Linguistics**

| Campo | Valor |
|---|---|
| Autores | Artstein, R.; Poesio, M. |
| Año y sede | 2008. Computational Linguistics 34(4), pp. 555–596 (artículo de revisión, «Survey Article») |
| Identificador | doi:10.1162/coli.07-034-r2 |
| PDF | `pdfs/F07_artstein_poesio_2008_acuerdo.pdf` · https://aclanthology.org/J08-4004.pdf |
| Eje | H. Fiabilidad de la anotación |
| Origen del registro | auditoría (S16), ahora leído |
| Nivel de lectura | completo (texto extraído del PDF, 42 páginas; revisado el 20-11-2026). Las páginas se citan con la numeración de la revista (página del PDF + 554); la lista de referencias (pp. 591–596) solo se consultó por búsqueda |

## Qué hace

- **Datos.** Artículo de revisión; ejemplos ilustrativos con 100 enunciados y dos o tres codificadores (tablas 1, 3 y 4, pp. 558, 563, 568).
- **Tarea y protocolo.** Cómo medir el acuerdo entre anotadores en la anotación de corpus.
- **Método.** Compara S, pi, kappa, alfa de Krippendorff y kappa ponderado según su modelo de azar (pp. 559–570). Alfa generaliza con una función de distancia y admite varios codificadores, distintas magnitudes de desacuerdo y valores faltantes (p. 564); kappa ponderado de Cohen solo se define para dos codificadores y no impone restricciones a los pesos (p. 567).
- **Comparadores.** No aplica.
- **Resultados.** En el ejemplo de la tabla 1: acuerdo observado 0,70, S = 0,40, pi ≈ 0,341, kappa ≈ 0,348 (tabla 2, p. 560). En el ejemplo integrado de tres categorías con pesos, alfa ≈ 0,8156 y kappa ponderado ≈ 0,8163 (p. 570). Para medir fiabilidad recomiendan coeficientes de distribución única (pi, alfa), aunque la diferencia con kappa es pequeña y decrece con más codificadores (pp. 571–572). Para etiquetas de conjunto presentan las distancias de Passonneau, Jaccard, Dice y MASI (producto de la de Passonneau por la de Jaccard; p. 584); con los mismos datos, alfa va de 0,642 (Jaccard) a 0,691 (Dice) (p. 585), y en otra tarea de 0,122 a 0,998 según la distancia, por lo que con coeficientes ponderados no valen las reglas de interpretación habituales (p. 586). La introducción recoge que kappa y K pueden quedar a distintos lados del umbral de 0,67 (p. 556).
- **Umbrales.** Repasan las escalas de Landis y Koch y de Krippendorff (0,8 bueno; 0,67–0,8 conclusiones tentativas) y que Krippendorff considera 0,8 el mínimo absoluto (p. 576). En las conclusiones: «if a threshold needs to be set, 0.8 is a good value», pero dudan de que un único punto de corte sirva para todo, coinciden con Craggs y McGee Wood en que fijar un umbral no debe ser requisito para publicar y piden informar el método (número de codificadores, independencia, uso del manual), la significación y la matriz de confusión o tabla de acuerdos (p. 591). Los pesos complican aún más la interpretación (pp. 576–577, 591).
- **Limitaciones declaradas.** Parte del material quedó en una versión extendida (p. 556). Tratan solo el acuerdo entre codificadores (reproducibilidad); exigen codificadores que trabajen independientemente, idealmente tres o más (pp. 574–575). El texto no usa los términos estabilidad ni test-retest ni trata el acuerdo intra-anotador (búsqueda en todo el texto).
- **Código y datos.** No aplica.

## Aporte a la tesis

Fundamenta tres decisiones del informe de estabilidad: un mismo acuerdo observado produce coeficientes muy distintos, así que hay que informar el coeficiente y el acuerdo bruto; los ordinales requieren ponderación (ya se hace con kappa lineal); en los campos múltiples el valor depende de la distancia elegida (p. 585), de modo que el Jaccard debe declararse como elección y no como estándar. Desaconseja fijar 0,6 como umbral único.

Actualización del 12 de noviembre (decisión R02 de `docs/registro_decisiones.md`): los autores proponen 0,8 si es imprescindible fijar un umbral, desaconsejan que un umbral sea requisito y piden informar el método, el coeficiente y la tabla de acuerdos (p. 591; las «páginas 22 y 37» citadas entonces eran páginas del PDF, es decir, pp. 576 y 591 de la revista). Por eso el estudio usa 0,6 solo como señal de revisión y declara que queda por debajo de esa propuesta.

## Cautela al citar

Citar con páginas de la revista (pp. 576 y 591 para umbrales; p. 584 para MASI y Jaccard). El 0,8 se propone para coeficientes corregidos por azar (K, alfa) en estudios entre codificadores; aplicarlo al acuerdo intra-anotador es una extrapolación de la tesis. El Jaccard medio sin corrección por azar no es lo que discuten (allí Jaccard es una distancia dentro de alfa).

## Actualización del 20 de noviembre de 2026

- Se leyó el texto completo (42 páginas; referencias solo por búsqueda) y se fijaron las páginas reales: Computational Linguistics 34(4), pp. 555–596.
- Confirmado con página: la propuesta de 0,8 «si es imprescindible fijar un umbral» y la objeción a usar un umbral como requisito (p. 591); MASI, Jaccard y Dice como distancias para etiquetas de conjunto (p. 584) y su efecto en alfa (pp. 585–586); kappa ponderado (pp. 567–568, 570) y alfa (pp. 564–567, 591).
- Corregido: la referencia a «páginas 22 y 37» del 12 de noviembre era de páginas del PDF; en la revista son pp. 576 y 591.
- **Matiz respecto del uso en la tesis.** El artículo no trata la estabilidad ni el acuerdo intra-anotador: todo se refiere a reproducibilidad entre codificadores independientes. La frase «por debajo del 0,8 que proponen Artstein y Poesio» es correcta como cita, pero conviene aclarar que la tesis traslada ese valor a un test-retest con un solo anotador y que los autores prefieren pi o alfa a kappa de Cohen para medir fiabilidad (p. 572).

---
Leído el 11 de noviembre de 2026 y completado el 20 de noviembre de 2026 con asistencia computacional, sobre el texto completo extraído del PDF. «NV» marca lo que no se pudo comprobar.
