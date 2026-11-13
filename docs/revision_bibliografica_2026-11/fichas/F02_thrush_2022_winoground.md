# F02 · Thrush (2022)

**Winoground: Probing Vision and Language Models for Visio-Linguistic Compositionality**

| Campo | Valor |
|---|---|
| Autores | Thrush, T.; Jiang, R.; Bartolo, M.; et al. |
| Año y sede | 2022. arXiv v2 (sede no vista en el texto leído) |
| Identificador | arXiv:2204.03162 |
| PDF | `pdfs/F02_thrush_2022_winoground.pdf` · https://arxiv.org/pdf/2204.03162 |
| Eje | E. Orden y composición en modelos visión-lenguaje |
| Origen del registro | búsqueda dirigida |
| Nivel de lectura | parcial: primeros ~40 000 caracteres literales; el resto, resumen automático |

## Qué hace

- **Datos.** 400 ejemplos curados por expertos (1 600 pares imagen-texto), imágenes de Getty, solo inglés.
- **Tarea y protocolo.** Emparejar dos imágenes con dos pies que usan las mismas palabras en distinto orden; puntajes de texto, imagen y grupo.
- **Método.** Solo benchmark: se puntúan modelos preentrenados y una línea base humana (al menos 10 anotadores por par).
- **Comparadores.** UNITER, ViLLA, VinVL, ViLT, LXMERT, ViLBERT, UniT, VisualBERT, FLAVA, CLIP ViT-B/32, VSE++, VSRN y humanos.
- **Resultados.** Tabla 3 (texto / imagen / grupo): humanos 89,50 / 88,50 / 85,50; azar 25,00 / 25,00 / 16,67; CLIP 30,75 / 10,50 / 8,00. CLIP queda por debajo del azar en imagen y grupo.
- **Limitaciones declaradas.** Solo inglés, tamaño reducido, curación costosa, anotadores mayoritariamente de EE. UU.
- **Código y datos.** Datos en huggingface.co/datasets/facebook/winoground; código no visto.

## Aporte a la tesis

Segunda fuente, independiente de ARO, de que los modelos tipo CLIP no distinguen configuraciones con los mismos elementos en otro orden. Es el análogo lingüístico de dos textiles con el mismo histograma de bandas y distinta secuencia, que es exactamente lo que separa M3 de M3-sin-orden.

## Cautela al citar

400 ejemplos y un dominio distinto. Usarlo junto con F01 y sin extrapolar cifras.

---
Leído el 11 de noviembre de 2026 con asistencia computacional. «NV» marca lo que no se vio en el texto literal del documento y debe comprobarse en el PDF antes de citarlo.
