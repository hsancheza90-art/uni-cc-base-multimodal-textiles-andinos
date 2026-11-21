# F15 · Buckley (2007)

**Bias and the limits of pooling for large collections**

| Campo | Valor |
|---|---|
| Autores | Buckley, C.; Dimmick, D.; Soboroff, I.; Voorhees, E. |
| Año y sede | 2007. Information Retrieval 10, 491–508 (Springer; recibido el 12-10-2006, aceptado el 31-07-2007, publicado en línea el 21-08-2007; p. 1) |
| Identificador | doi:10.1007/s10791-007-9032-x |
| PDF | `pdfs/F15_buckley_2007_sesgo_pooling.pdf` · https://link.springer.com/content/pdf/10.1007/s10791-007-9032-x.pdf |
| Eje | G. Evaluación de recuperación |
| Origen del registro | OpenAlex (G1) |
| Nivel de lectura | completo (texto extraído del PDF, 18 páginas; revisado el 20-11-2026). Las figuras 1-5 solo se leen por sus leyendas y ejes |

## Qué hace

- **Datos.** AQUAINT (1 033 461 documentos, 50 temas, 50 ejecuciones de TREC 2005 con profundidad 55) (p. 6), comparada con Disks4&5 (mismos temas) y con las colecciones Terabyte de 2004 y 2005 (25 M de páginas web, profundidad 85 y 100) y TREC-8 ad hoc y small web (tabla 1, pp. 12-13). El tamaño de Disks4&5 aparece como 528 542 en la p. 6 y 528 155 en la tabla 1: discrepancia interna del texto.
- **Tarea y protocolo.** Si el pooling de tamaño fijo sesga los juicios cuando la colección crece; medida principal MAP (p. 3).
- **Método.** Definen titlestat, la proporción de documentos que contienen palabras del título del tema (p. 7), con variantes titlestat_rel y titlestat_rank (pp. 8-9). Aplican la prueba leave-out-uniques (LOU) de Zobel en su variante estricta: retiran del juicio todos los documentos que solo aportaron ejecuciones del mismo grupo y comparan el MAP (p. 4).
- **Comparadores.** No aplica.
- **Resultados.** La ejecución sab05ror1 aportó 405 relevantes únicos de 2 750 documentos y pierde 23 % de MAP al retirarlos (0,266 frente a 0,202); MARY05C1, 12 %; el resto, 8 % o menos (p. 7). titlestat_rel: 0,719 en AQUAINT frente a 0,588 en Disks4&5, mayor en 48 de 50 temas (p. 8). El sesgo no depende del número de relevantes por tema (p. 11, fig. 4). Terabyte 2004: caída media 9,6 %, máxima 45,5 %; Terabyte 2005: 3,9 % y 17,7 % (p. 12). Zobel (1998) observó degradación sustancial de la colección con profundidad 10 pero no con 50; la profundidad mínima es relativa al tamaño de la colección (p. 11).
- **Limitaciones declaradas.** La evidencia de sesgo en Terabyte es circunstancial (p. 15). No se sabe construir una submuestra justa de juicios (p. 15). Proponen: temas más precisos, pools más profundos (move-to-front recupera 79 % de los relevantes; muestreo aleatorio estima MAP con 10-20 % del pool, sin saber cómo interactúa con el sesgo), más diversidad de ejecuciones y submuestreo de juicios con bpref (pp. 14-15). El sesgo es conservador: solo baja la puntuación del sistema afectado; un sistema basado en conceptos semánticos puede quedar infravalorado; la mera presencia de muchos no juzgados no prueba injusticia (pp. 16-17).
- **Código y datos.** No aplica.

## Aporte a la tesis

Fundamenta el punto 6.b del asesor. Un sistema cuyos candidatos no entraron al pool queda infravalorado, porque lo no juzgado cuenta como no relevante. Por eso los candidatos de M3, M3-sin-orden y M4 deben entrar al pool antes de evaluar, y por eso conviene informar, por sistema, cuánto del top 10 está juzgado y repetir la evaluación retirando los pares que solo aportó cada sistema.

## Cautela al citar

El problema estudiado es de colecciones enormes; con una galería de 150 piezas y profundidad 10 el riesgo es menor, pero no nulo para los sistemas estructurales. La prueba LOU del artículo retira los documentos aportados solo por un grupo y mide el cambio de MAP; si se adapta a nDCG@10, declararlo como adaptación.

## Actualización del 20 de noviembre de 2026

- Verificado en el texto completo: cifras de sab05ror1 y MARY05C1 (p. 7), Terabyte 2004 (p. 12), definición de LOU en su variante estricta por grupo (p. 4); se completaron las recomendaciones y limitaciones (pp. 14-17), antes solo en el resumen automático.
- Agregado: Terabyte 2005 (3,9 % y 17,7 %), la observación de Zobel sobre profundidad 10 frente a 50 y el argumento de que la profundidad necesaria es relativa al tamaño de la colección (p. 11).
- Afecta al diseño: la profundidad 10 está justo en el valor que Zobel encontró degradado en colecciones grandes; con una galería de cientos de piezas la proporción juzgada es alta, pero conviene informar la proporción del top 10 juzgada por sistema y la prueba LOU por sistema. Los 10 candidatos al azar del pool coinciden con la vía de muestreo aleatorio que el artículo propone, aunque advierte que su interacción con el sesgo es desconocida (p. 15). Como el sesgo es conservador (p. 16), un sistema que no aportó al pool solo puede salir perjudicado: relevante para M3 y M4 si se agregan después.
- Sin pendientes de verificación en el texto.

---
Leído el 11 de noviembre de 2026 y completado el 20 de noviembre de 2026 con asistencia computacional, sobre el texto completo extraído del PDF. «NV» marca lo que no se pudo comprobar.
