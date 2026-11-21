# F26 · Koh (2020)

**Concept Bottleneck Models**

| Campo | Valor |
|---|---|
| Autores | Koh, P. W.; Nguyen, T.; Tang, Y. S.; Mussmann, S.; Pierson, E.; Kim, B.; Liang, P. (los tres primeros con contribución igual; p. 1) |
| Año y sede | 2020. Proceedings of the 37th International Conference on Machine Learning (ICML), en línea, PMLR 119 (p. 1) |
| Identificador | arXiv:2007.04612 (v3, 29 de diciembre de 2020) |
| PDF | `pdfs/F26_koh_2020_concept_bottleneck.pdf` · https://arxiv.org/pdf/2007.04612 |
| Eje | I. Interpretabilidad y fidelidad |
| Origen del registro | auditoría (S11), ahora leído |
| Nivel de lectura | completo (texto extraído del PDF, 19 páginas; revisado el 20-11-2026). Las figuras 2-5 solo se leen por sus leyendas |

## Qué hace

- **Datos.** Radiografías de rodilla OAI (36 369 observaciones de 4 172 pacientes; 10 conceptos clínicos ordinales tras filtrar 8 dispersos; grado KLG reducido a 4 niveles) y aves CUB (11 788 imágenes, 200 especies, 112 atributos binarios a nivel de clase por voto mayoritario) (p. 4; apéndice A, pp. 13-14). Variante TravelingBirds con fondos cambiados (p. 8-9).
- **Tarea y protocolo.** Si un modelo que pasa por conceptos anotados iguala al modelo de extremo a extremo y permite intervenir sobre los conceptos.
- **Método.** Se predicen conceptos a partir de la imagen (g: x → c) y la etiqueta a partir de los conceptos (f: c → y), con tres formas de entrenar: independiente, secuencial y conjunta (sec. 3, p. 3). La intervención en prueba sustituye conceptos predichos por los verdaderos (oráculo) y recalcula la salida; en OAI con un orden fijo calculado en validación, en CUB por grupos en orden aleatorio (sec. 6; apéndice B.3, p. 15). La intervención es sobre el concepto predicho dentro del modelo, no sobre el concepto en la realidad (p. 3).
- **Comparadores.** Modelo estándar de extremo a extremo, sin capa cuello de botella, multitarea, y sondas lineales a posteriori sobre el estándar y sobre SENN (pp. 4-6).
- **Resultados.** Tabla 1 (p. 4), confirmada: en OAI los modelos conjunto y secuencial obtienen RMSE 0,418 frente a 0,441 del estándar; en CUB el conjunto tiene error 0,199 frente a 0,175 del estándar. Las sondas lineales a posteriori predicen peor los conceptos (OAI: RMSE 0,68 frente a 0,53; CUB: 0,09 frente a 0,03) (p. 6). Intervenir en dos conceptos de OAI baja el RMSE de más de 0,4 a cerca de 0,3 (p. 6-7). La exactitud de tarea y de conceptos no basta para prever la eficacia de la intervención; con un c → y lineal la intervención fue menos eficaz (p. 8). Con fondos cambiados, error 0,482 (conjunto) frente a 0,627 (estándar) (tabla 3, p. 8).
- **Limitaciones declaradas.** Confirmadas: requiere conceptos anotados en entrenamiento (p. 9); la ganancia por intervención depende del modo de entrenar y de la arquitectura (pp. 7-8, 10); los resultados de intervención en CUB son optimistas porque suponen que el experto no se equivoca y que todas las aves de una especie comparten conceptos (p. 8). Un canal lateral x → y impide intervenir limpiamente sobre un concepto (pp. 3 y 9). La robustez depende del conjunto de conceptos elegido (p. 9).
- **Código y datos.** Confirmado: github.com/yewsiang/ConceptBottleneck y hoja de CodaLab para CUB; OAI no se publica, se solicita a nda.nih.gov/oai (p. 10).

## Aporte a la tesis

Es el marco conceptual más próximo a M3 y M4. Los atributos estructurales anotados cumplen el papel de conceptos, y la prueba de intervención de H3 (retirar o cambiar un atributo y ver si el ranking cambia como predice la fórmula) es la intervención en prueba de este trabajo. La diferencia que debe declararse: aquí los conceptos se predicen desde la imagen tras el entrenamiento; en la tesis los anota una persona para toda la galería.

## Cautela al citar

Tareas de clasificación supervisada, no de recuperación. La intervención del artículo cambia el valor que el modelo usa, no la realidad (p. 3): citarlo para H3 en ese sentido.

## Actualización del 20 de noviembre de 2026

- Verificado con página: cifras de la tabla 1 (p. 4), efecto de intervenir en dos conceptos (pp. 6-7), limitaciones (pp. 8-10) y repositorio de código (p. 10), antes NV.
- Corregido: lista completa de siete autores; en OAI el RMSE 0,418 lo obtienen tanto el modelo conjunto como el secuencial.
- Afecta al diseño de H3: el artículo advierte que con un canal lateral x → y no se puede intervenir limpiamente sobre un concepto (pp. 3 y 9). En M4, BM25 y OpenCLIP actúan como canales laterales respecto del descriptor estructural; la prueba de intervención sobre atributos solo valida la parte estructural del score, y conviene declararlo. También señala que la validez de la intervención depende de que los conceptos usados coincidan con los verdaderos (p. 2): en la tesis ese papel lo cumple la fiabilidad de la anotación (acuerdo intra-anotador).
- Sin pendientes de verificación en el texto.

---
Leído el 11 de noviembre de 2026 y completado el 20 de noviembre de 2026 con asistencia computacional, sobre el texto completo extraído del PDF. «NV» marca lo que no se pudo comprobar.
