# F26 · Koh (2020)

**Concept Bottleneck Models**

| Campo | Valor |
|---|---|
| Autores | Koh, P. W.; Nguyen, T.; Tang, Y. S.; et al. |
| Año y sede | 2020. ICML 2020, PMLR 119 |
| Identificador | arXiv:2007.04612 |
| PDF | `pdfs/F26_koh_2020_concept_bottleneck.pdf` · https://arxiv.org/pdf/2007.04612 |
| Eje | I. Interpretabilidad y fidelidad |
| Origen del registro | auditoría (S11), ahora leído |
| Nivel de lectura | parcial: primeros ~40 000 caracteres literales; el resto, resumen automático |

## Qué hace

- **Datos.** Radiografías de rodilla OAI (36 369 casos, 10 conceptos clínicos ordinales) y aves CUB (11 788 imágenes, 112 atributos binarios).
- **Tarea y protocolo.** Si un modelo que pasa por conceptos anotados iguala al modelo de extremo a extremo y permite intervenir sobre los conceptos.
- **Método.** Se predicen conceptos a partir de la imagen y la etiqueta a partir de los conceptos. La intervención en prueba sustituye conceptos predichos por los correctos y recalcula la salida.
- **Comparadores.** Modelo estándar de extremo a extremo.
- **Resultados.** Tabla 1: en OAI el modelo conjunto obtiene RMSE 0,418 frente a 0,441 del estándar; en CUB el error es 0,199 frente a 0,175. Intervenir en dos conceptos de OAI baja el RMSE de más de 0,4 a cerca de 0,3 (sec. 6.1).
- **Limitaciones declaradas.** Requiere conceptos anotados en entrenamiento; la ganancia por intervención depende del modo de entrenar; los resultados de intervención en CUB son optimistas.
- **Código y datos.** NV: github.com/yewsiang/ConceptBottleneck

## Aporte a la tesis

Es el marco conceptual más próximo a M3 y M4. Los atributos estructurales anotados cumplen el papel de conceptos, y la prueba de intervención de H3 (retirar o cambiar un atributo y ver si el ranking cambia como predice la fórmula) es la intervención en prueba de este trabajo. La diferencia que debe declararse: aquí los conceptos se predicen desde la imagen tras el entrenamiento; en la tesis los anota una persona para toda la galería.

## Cautela al citar

Tareas de clasificación supervisada, no de recuperación.

---
Leído el 11 de noviembre de 2026 con asistencia computacional. «NV» marca lo que no se vio en el texto literal del documento y debe comprobarse en el PDF antes de citarlo.
