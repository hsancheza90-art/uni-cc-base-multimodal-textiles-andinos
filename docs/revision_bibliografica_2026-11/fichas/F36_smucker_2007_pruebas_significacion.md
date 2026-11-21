# F36 · Smucker (2007)

**A Comparison of Statistical Significance Tests for Information Retrieval Evaluation**

| Campo | Valor |
|---|---|
| Autores | Smucker, M. D.; Allan, J.; Carterette, B. (University of Massachusetts Amherst) |
| Año y sede | 2007. CIKM '07 (ACM Conference on Information and Knowledge Management), 6-8 de noviembre de 2007, Lisboa; pp. 623-632 (p. 623). El texto no da el título completo de las actas ni el número de edición |
| Identificador | ISBN 978-1-59593-803-9 (p. 623). El DOI no figura en el texto |
| PDF | `pdfs/IR-591.pdf` |
| Eje | Evaluación de recuperación (pruebas de significación) |
| Origen del registro | aportado por el investigador (20-11-2026) |
| Nivel de lectura | completo (texto extraído del PDF, 10 páginas, pp. 623-632). Las figuras 4-7 se leen por sus leyendas y el texto que las comenta |

## Qué hace

- **Datos.** Ejecuciones ad hoc de TREC 3 y 5-8; todos los pares de ejecuciones dentro de cada edición: 18 820 pares (780, 1830, 2701, 5253 y 8256), cada uno sobre **50 temas**; medida principal MAP con trec_eval (pp. 626-627).
- **Tarea y protocolo.** Comparar los valores p que dan cinco pruebas pareadas sobre los mismos pares. Si dos pruebas dan valores p casi iguales, no hay diferencia práctica entre ellas (p. 623).
- **Método.** t de Student pareada y Wilcoxon (R), prueba de signos y signos con diferencia mínima de 0,01, bootstrap con desplazamiento y aleatorización de Fisher (permutación) implementados en C++. Todos bilaterales (p. 627). La aleatorización intercambia las etiquetas A/B dentro de cada tema (2^50 permutaciones posibles) y se estima por Monte Carlo con 100 000 muestras; como patrón de referencia usan 20 millones (pp. 625 y 627). Dan la fórmula del coeficiente de variación del valor p estimado: cv = ((1 − p)/(p·B))^1/2, dividiendo p a la mitad para el caso bilateral; con 100 000 muestras, un valor p bilateral de 0,05 tiene un error de ≈ 2 % (±0,001) (p. 627). Acuerdo entre pruebas con la raíz del error cuadrático medio (RMSE) (p. 627).
- **Comparadores.** Las cinco pruebas (seis variantes) entre sí; la aleatorización con 20 millones de muestras sirve de referencia para medir omisiones y falsas alarmas de Wilcoxon y signos (pp. 629-630).
- **Resultados.** La aleatorización, el bootstrap y la t coinciden: RMSE ≈ 0,01 entre ellas (0,007-0,011; cuadro 1, p. 627) y 0,006 en el tramo de valores p entre 0,01 y 0,1 (p. 627). Wilcoxon y signos discrepan de las demás y entre sí (RMSE 0,15-0,26; cuadro 1); frente a la aleatorización omiten diferencias significativas y dan falsas alarmas (pp. 628-630). El bootstrap muestra un sesgo sistemático, pequeño pero visible, hacia valores p menores (p. 628). Con P@10, MRR y R-precision el comportamiento es similar al de MAP (p. 631). En el ejemplo de TREC 3: aleatorización p = 0,0138, t p = 0,0153, bootstrap p = 0,0107, Wilcoxon p = 0,0560 y signos p = 0,3222 (p. 626).
- **Limitaciones declaradas.** Todos los experimentos usan N = 50 temas, que es «una muestra grande»; con muestras menores, las violaciones de normalidad pueden causar errores en la t (p. 630). El sesgo del bootstrap podría deberse a su implementación (p. 631). La concordancia entre las hipótesis nulas de las tres pruebas «puede no darse siempre» (p. 630).
- **Código y datos.** No se publica el código; usan trec_eval y las ejecuciones de TREC (pp. 627 y 632).

## Aporte a la tesis

- **¿t, bootstrap y permutación coinciden?** **Respalda**, con 50 temas y MAP (p. 623; cuadro 1, p. 627; conclusión, p. 632). Recomiendan la aleatorización «en todos los casos en que sea aplicable», con un estadístico que coincida con el que se informa (pp. 624, 631 y 632). Esto respalda el diseño de la tesis: permutación pareada por cambio de signo sobre la diferencia de medias de nDCG@10 como prueba principal y t pareada como comprobación. Es el uso que Fisher dio a la aleatorización, como comprobación independiente de la t, en orden inverso (p. 627). La t solo sirve para diferencias de medias (p. 631).
- **¿Wilcoxon y signos no son recomendables?** **Respalda**: piden dejar de usarlos para medir la significación de una diferencia de medias (pp. 623 y 632). La prueba de signos conserva su validez solo si lo único medible es una preferencia sin escala (p. 631).
- **¿Con cuántos temas?** Siempre 50 (pp. 626 y 630). **Matiza** el uso con pocas consultas: advierten que con menos temas la t puede fallar por falta de normalidad y que la aleatorización es la opción segura (pp. 630-631). Con 30 consultas de prueba el texto no da evidencia directa. Con 10 consultas de desarrollo, tampoco. La recomendación favorece que la tesis decida con la permutación y no con la t.
- **Bootstrap solo para el intervalo.** **Respalda**: el bootstrap como prueba tiende a dar valores p menores (pp. 628 y 631) y tiene muchas variantes que requieren experiencia (p. 631). El artículo no evalúa intervalos de confianza por bootstrap.
- **Número de réplicas.** Con su fórmula (p. 627), 10 000 réplicas dan un coeficiente de variación de ≈ 6 % para un valor p bilateral de 0,05, es decir, unos ±0,003 (cálculo propio). F20, con la fórmula de Urbano et al., da ≈ 0,0022. Conviene informar el error de Monte Carlo cuando un valor p quede cerca de 0,05.

## Citas útiles

- Con las ejecuciones ad hoc de TREC, la aleatorización, el bootstrap y la t pareada dan valores p comparables; no hay diferencia práctica entre ellas (pp. 623 y 632).
- Wilcoxon y signos son variantes simplificadas de la aleatorización con otro estadístico; pueden predecir significación de forma incorrecta y no detectar resultados significativos (pp. 623 y 632).
- Una prueba debe contrastar el mismo estadístico que se informa; la t solo es apropiada para la diferencia de medias (pp. 623-624 y 631).
- La aleatorización no supone muestreo aleatorio de una población, lo que conviene en RI porque los temas de TREC se eligen a mano (p. 631).
- Con N = 50 la preocupación por la normalidad de la t no parece justificada; con muestras menores puede haber errores (p. 630).
- El bootstrap con desplazamiento muestra un sesgo sistemático hacia valores p menores que la aleatorización y la t (pp. 628 y 631).
- Prefieren informar el valor p y marcar los resultados que cumplen el criterio, en lugar de reducirlo a una decisión binaria (p. 629).

## Cautela al citar

La coincidencia entre pruebas se demuestra con 50 temas, MAP y ejecuciones de TREC 3 y 5-8; no se estudia nDCG@10 ni muestras de 10 o 30 consultas. El artículo compara valores p entre pruebas, no errores de tipo I con una hipótesis nula conocida: para eso, ver F20 (Urbano et al., 2019). La aleatorización del artículo permuta etiquetas dentro de cada tema, lo que equivale a cambiar el signo de cada diferencia; la palabra «cambio de signo» no aparece en el texto.

---
Leído el 20 de noviembre de 2026 con asistencia computacional, sobre el texto completo extraído del PDF.
