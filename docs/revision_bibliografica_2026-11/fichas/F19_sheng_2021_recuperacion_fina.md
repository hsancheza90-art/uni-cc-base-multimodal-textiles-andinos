# F19 · Sheng (2021)

**Fine-Grained Cross-Modal Retrieval for Cultural Items with Focal Attention and Hierarchical Encodings**

| Campo | Valor |
|---|---|
| Autores | Sheng, S.; Laenen, K.; Van Gool, L.; Moens, M.-F. (KU Leuven; p. 1) |
| Año y sede | 2021. Computers 10, 105 (p. 1; el número 9 solo se deduce del DOI). Recibido el 13-07-2021, aceptado el 19-08-2021, publicado el 25-08-2021; CC BY (p. 1) |
| Identificador | doi:10.3390/computers10090105 |
| PDF | `pdfs/F19_sheng_2021_recuperacion_fina.pdf` · https://www.mdpi.com/2073-431X/10/9/105/pdf |
| Eje | C. Recuperación multimodal en patrimonio |
| Origen del registro | OpenAlex (C2) |
| Nivel de lectura | completo (texto extraído del PDF, 20 páginas; revisado el 20-11-2026). Solo salió como códigos «/gid000..» el distintivo gráfico de la p. 1; tablas legibles, figuras no visibles |

## Qué hace

- **Datos.** Dos conjuntos de alineación adaptados de conjuntos de subtítulos de arte antiguo egipcio y chino de los mismos autores (p. 4): chino con 6 086 obras de entrenamiento y 761 de validación; egipcio con 14 352 y 1 795; conjuntos de referencia («golden») de 500 obras, 1 134 fragmentos y 2 234 sintagmas (chino) y 536 obras, 1 225 fragmentos y 2 724 sintagmas (egipcio), con regiones marcadas a mano (tabla 1, p. 5). Cada sintagma corresponde a un solo fragmento (p. 4). El texto no indica de qué museos proceden las imágenes.
- **Tarea y protocolo.** Confirmado: anotación (de fragmento de imagen a sintagma nominal) y búsqueda (de sintagma a fragmento); entrenamiento débil a nivel de obra, ajuste fino y evaluación con validación cruzada de cuatro pliegues sobre el conjunto de referencia (pp. 4 y 11). Métrica: recall@1, 5 y 10; prueba F (ANOVA) entre pliegues (pp. 12–13).
- **Método.** Confirmado: modelo débilmente supervisado sobre SCAN y BFAN con atención cruzada, filtro SIFT (descarta regiones con menos de z = 2 puntos clave) y codificación jerárquica (fragmento y obra completa); 10 regiones por obra de Faster R-CNN con ResNet-101 preentrenada en Visual Genome y sintagmas extraídos con NPFST y codificados con BERT-base (pp. 6–12).
- **Comparadores.** Confirmado: DeepFrag, SCAN y BFAN (p. 11); el resumen habla de dos métodos del estado del arte (p. 1) y las contribuciones de tres líneas base, dos de ellas del estado del arte (p. 3).
- **Resultados.** Anotación: en el chino, BFAN_SF_GB llega a recall@10 de 49,0 frente a 43,3 de BFAN (+5,7); en el egipcio, BFAN_SF llega a 39,6 frente a 33,7 (+5,9) (tabla 4, p. 13; p. 13). Búsqueda: mejora pequeña, +0,6 en recall@10 (chino) y +0,3 en recall@1 con SCAN_GB (p. 15). Usar tokens o sustantivos en lugar de sintagmas hunde el resultado (recall@10 de 2,7 y 3,5; tabla 6, p. 15). El aumento visual no ayudó (p. 14).
- **Limitaciones declaradas.** El recall@K es estricto porque los subtítulos son incompletos y hay recuperaciones pertinentes ausentes de la referencia, por lo que el rendimiento real podría ser mayor (pp. 16–18); conjunto de referencia pequeño (p. 4); la representación global mete ruido en el conjunto egipcio, de anotación peor (p. 14); pesos fijos de las pérdidas «rígidos» (p. 14); la búsqueda de imágenes queda por mejorar (p. 19).
- **Código y datos.** No figura enlace al código; la declaración de datos dice solo «Data is contained within the article» (p. 19).

## Aporte a la tesis

Define recuperación fina como correspondencia entre regiones de la pieza y fragmentos de texto, frente al emparejamiento de imagen completa. Es la dirección a la que apuntaría una versión automática de M3: localizar bandas y regiones en lugar de anotarlas. Útil para trabajo futuro y para situar T1.

## Cautela al citar

Las cifras ya están verificadas con página, pero son recall a nivel de fragmento con relevancia binaria, no comparables con nDCG graduado. Sus dominios (arte egipcio y chino) no incluyen textiles.

## Actualización del 20 de noviembre de 2026

- Se completaron resultados, limitaciones, tamaños de los conjuntos y disponibilidad de datos con página.
- Se completaron los cuatro autores y las fechas; el número 9 del volumen no figura en el texto (solo en el DOI).
- Se añadió una cautela útil para T1: los autores reconocen que la referencia incompleta subestima el rendimiento, el mismo riesgo de los juicios parciales.
- Sigue sin saberse de qué museos proceden las imágenes y no hay código publicado.

---
Leído el 11 de noviembre de 2026 y completado el 20 de noviembre de 2026 con asistencia computacional, sobre el texto completo extraído del PDF. «NV» marca lo que no se pudo comprobar.
