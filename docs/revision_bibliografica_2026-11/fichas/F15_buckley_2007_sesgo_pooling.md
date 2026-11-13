# F15 · Buckley (2007)

**Bias and the limits of pooling for large collections**

| Campo | Valor |
|---|---|
| Autores | Buckley, C.; Dimmick, D.; Soboroff, I.; Voorhees, E. |
| Año y sede | 2007. Information Retrieval 10, 491–508 |
| Identificador | doi:10.1007/s10791-007-9032-x |
| PDF | `pdfs/F15_buckley_2007_sesgo_pooling.pdf` · https://link.springer.com/content/pdf/10.1007/s10791-007-9032-x.pdf |
| Eje | G. Evaluación de recuperación |
| Origen del registro | OpenAlex (G1) |
| Nivel de lectura | parcial: primeros ~40 000 caracteres literales; el resto, resumen automático |

## Qué hace

- **Datos.** AQUAINT (1 033 461 documentos, 50 temas, 50 ejecuciones de TREC 2005 con profundidad 55) y colecciones Terabyte de 2004 y 2005.
- **Tarea y protocolo.** Si el pooling de tamaño fijo sesga los juicios cuando la colección crece.
- **Método.** Definen titlestat, la proporción de documentos que contienen palabras del título del tema, y aplican la prueba de excluir los documentos que solo aportó un sistema (leave-out-uniques).
- **Comparadores.** No aplica.
- **Resultados.** Un sistema que aportó 405 documentos relevantes únicos pierde 23 % de MAP al retirarlos (0,266 frente a 0,202); otro, 12 %; el resto, 8 % o menos (sec. 3.2). En Terabyte 2004 la caída media es 9,6 % y la máxima 45,5 %.
- **Limitaciones declaradas.** Recomendaciones y limitaciones solo en el tramo no literal.
- **Código y datos.** No aplica.

## Aporte a la tesis

Fundamenta el punto 6.b del asesor. Un sistema cuyos candidatos no entraron al pool queda infravalorado, porque lo no juzgado cuenta como no relevante. Por eso los candidatos de M3, M3-sin-orden y M4 deben entrar al pool antes de evaluar, y por eso conviene informar, por sistema, cuánto del top 10 está juzgado y repetir la evaluación retirando los pares que solo aportó cada sistema.

## Cautela al citar

El problema estudiado es de colecciones enormes; con una galería de 150 piezas y profundidad 10 el riesgo es menor, pero no nulo para los sistemas estructurales.

---
Leído el 11 de noviembre de 2026 con asistencia computacional. «NV» marca lo que no se vio en el texto literal del documento y debe comprobarse en el PDF antes de citarlo.
