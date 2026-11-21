# F03 · Balauca (2024)

**Taming CLIP for Fine-grained and Structured Visual Understanding of Museum Exhibits**

| Campo | Valor |
|---|---|
| Autores | Balauca, A.-A.; Paudel, D. P.; Toutanova, K.; Van Gool, L. (INSAIT, Sofia University; ETH Zurich; Google DeepMind) (p. 1) |
| Año y sede | 2024. arXiv v1 del 03-09-2024 (p. 1). La sede (ECCV 2024 según los autores) no figura en el texto del preprint; solo se agradece a «revisores anónimos» (p. 14) |
| Identificador | arXiv:2409.01690 |
| PDF | `pdfs/F03_balauca_2024_muze.pdf` · https://arxiv.org/pdf/2409.01690 |
| Eje | C. Recuperación multimodal en patrimonio |
| Origen del registro | auditoría (S03), releído |
| Nivel de lectura | completo (texto extraído del PDF, 29 páginas; revisado el 20-11-2026). Las figuras 3, 4, 6, 7 y 9 (gráficos) y las imágenes de los cuadros 12–15 no son legibles en la extracción; los cuadros numéricos sí |

## Qué hace

- **Datos.** MUZE: 210 000 pares imagen-tabla («200K+» en el resumen) de objetos de museo (p. 1, 4, 5): A-MUZE procede del Victoria and Albert Museum (18 atributos) y B-MUZE del British Museum (12 atributos) (p. 6, 20). Particiones de unos 178k / 16k / 33k para entrenamiento, validación y prueba (p. 6); estas cifras suman unos 227k, más que los 210K declarados, y el texto no lo explica. Curación: se eliminan términos de incertidumbre («probably», «possibly»), se resumen textos largos con YAKE y se normalizan las fechas a siglos (p. 6).
- **Tarea y protocolo.** Predecir valores de atributos faltantes de una pieza a partir de su imagen y de los atributos conocidos, ordenando todos los valores posibles del atributo por coseno (p. 10). Métricas: precisión media por clase, exactitud media por muestra, Acc@1 y Hit@5 (p. 10–11).
- **Método.** Embeddings de CLIP ViT-B/32 (OpenCLIP, `laion2b_s34b_b79k`) (p. 11) alimentan parseNet, un transformer de 2 capas, 512 de ancho y 8 cabezas (p. 9), que recibe la imagen, los atributos consultados con [MASK] y los pares atributo-valor de contexto; pérdida de coseno; se entrena un modelo por atributo (p. 9–11). 8 GPU NVIDIA L4 (p. 11).
- **Comparadores.** CLIP preentrenado y dos afinados: CLIP-FC (pies concatenados) y CLIP-FA (por atributo) (p. 6, 11); en el apéndice, CLIP con contexto (CLIP-CTX), con texto afinado y con frases (p. 21–23).
- **Resultados.** A-MUZE (cuadro 3, p. 12), exactitud media: CLIP 3,12, CLIP-FA 15,60, MUZE 23,51. B-MUZE (cuadro 4, p. 12): 2,53 / 22,66 / 30,36. Confirmados. Precisión: en el cuadro 3 la columna de MUZE se rotula MUZE-CFA, pero el cuadro 5 (p. 14) y el cuadro 10 (p. 24) asignan 23,51 a MUZE-CFC (MUZE-CFA da 22,70 en A-MUZE); el texto dice que en A-MUZE la mejor variante es MUZE-CFC (p. 13). Más contexto mejora el resultado, y imagen más contexto supera a solo contexto (fig. 6, p. 13–14). Los errores se concentran en objetos rotos, muy pequeños o de vidrio (p. 13).
- **Limitaciones declaradas.** El texto no tiene una sección de limitaciones. Control de calidad (apéndice C, p. 20–21): 3 expertos puntuaron 500 pares imagen-texto de 1 a 5 (media 4,507); 9 piezas se consideraron mal emparejadas con su texto (confirmado).
- **Código y datos.** github.com/insait-institute/MUZE (p. 1, 11). Licencia: los autores «planean» publicar la curación bajo CC BY-NC 4.0 con enlace a las imágenes, que conservan sus derechos (p. 21).

## Aporte a la tesis

Antecedente más cercano en combinar CLIP con atributos estructurados de museo. Diferencias que delimitan la contribución: MUZE aprende con 210 000 piezas y predice metadatos; la tesis no entrena, usa 150 piezas anotadas y evalúa recuperación por estructura con juicios humanos. También muestra lo bajo que rinde CLIP sin adaptar en atributos finos de museo. Su curación elimina expresiones de incertidumbre (p. 6), lo contrario de la tesis, que las conserva como «posiblemente» o estados `no_observable`.

## Cautela al citar

Métrica y tarea distintas: no comparar cifras con nDCG@10. Citar la cifra de 23,51 sin atribuirla a una variante concreta, o aclarar la discrepancia entre los cuadros 3 y 5. La sede ECCV 2024 no consta en el preprint.

## Actualización del 20 de noviembre de 2026

- Se leyó el texto completo (29 páginas, con apéndices A–J); se completaron afiliaciones y la asignación de cada subconjunto a su museo (V&A y British Museum).
- NV resueltos: las 9 de 500 piezas mal emparejadas (p. 21) y la licencia CC BY-NC 4.0, que es un plan declarado y no un hecho (p. 21). La sección de limitaciones no figura en el texto.
- Correcciones: el peso preentrenado es `laion2b_s34b_b79k`; la cifra 23,51 de A-MUZE corresponde a MUZE-CFC según los cuadros 5 y 10, aunque el cuadro 3 la rotula MUZE-CFA; las particiones suman más que el total declarado.
- Sigue sin verificar: la sede ECCV 2024 (no figura en el preprint) y el contenido de los gráficos.

---
Leído el 11 de noviembre de 2026 y completado el 20 de noviembre de 2026 con asistencia computacional, sobre el texto completo extraído del PDF. «NV» marca lo que no se pudo comprobar.
