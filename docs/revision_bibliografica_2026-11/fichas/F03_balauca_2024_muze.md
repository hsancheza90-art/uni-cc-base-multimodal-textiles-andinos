# F03 · Balauca (2024)

**Taming CLIP for Fine-grained and Structured Visual Understanding of Museum Exhibits**

| Campo | Valor |
|---|---|
| Autores | Balauca, A.-A.; Paudel, D. P.; Toutanova, K.; Van Gool, L. |
| Año y sede | 2024. ECCV 2024 según los autores (no visto en el texto leído) |
| Identificador | arXiv:2409.01690 |
| PDF | `pdfs/F03_balauca_2024_muze.pdf` · https://arxiv.org/pdf/2409.01690 |
| Eje | C. Recuperación multimodal en patrimonio |
| Origen del registro | auditoría (S03), releído |
| Nivel de lectura | parcial: primeros ~40 000 caracteres literales; el resto, resumen automático |

## Qué hace

- **Datos.** MUZE: unos 210 000 pares imagen-tabla de objetos de museo (British Museum y V&A); 178k/16k/33k para entrenamiento, validación y prueba; subconjuntos A-MUZE (18 atributos) y B-MUZE (12).
- **Tarea y protocolo.** Predecir valores de atributos faltantes de una pieza a partir de su imagen y de los atributos conocidos, ordenando candidatos por coseno.
- **Método.** Embeddings de CLIP ViT-B/32 (OpenCLIP, laion2b) alimentan parseNet, un transformer de 2 capas que recibe la imagen, los atributos consultados con máscara y los pares atributo-valor de contexto.
- **Comparadores.** CLIP preentrenado y dos afinados (por pies y por atributo).
- **Resultados.** A-MUZE (tabla 3): exactitud media CLIP 3,12, CLIP afinado por atributo 15,60, MUZE 23,51. B-MUZE (tabla 4): 2,53 / 22,66 / 30,36.
- **Limitaciones declaradas.** No vistos en el texto literal. NV: 9 de 500 piezas muestreadas mal emparejadas con su texto.
- **Código y datos.** github.com/insait-institute/MUZE; licencia CC BY-NC 4.0 NV.

## Aporte a la tesis

Antecedente más cercano en combinar CLIP con atributos estructurados de museo. Diferencias que delimitan la contribución: MUZE aprende con 210 000 piezas y predice metadatos; la tesis no entrena, usa 150 piezas anotadas y evalúa recuperación por estructura con juicios humanos. También muestra lo bajo que rinde CLIP sin adaptar en atributos finos de museo.

## Cautela al citar

Métrica y tarea distintas: no comparar cifras con nDCG@10.

---
Leído el 11 de noviembre de 2026 con asistencia computacional. «NV» marca lo que no se vio en el texto literal del documento y debe comprobarse en el PDF antes de citarlo.
