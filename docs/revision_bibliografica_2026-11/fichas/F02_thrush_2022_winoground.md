# F02 · Thrush (2022)

**Winoground: Probing Vision and Language Models for Visio-Linguistic Compositionality**

| Campo | Valor |
|---|---|
| Autores | Thrush, T.; Jiang, R.; Bartolo, M.; Singh, A.; Williams, A.; Kiela, D.; Ross, C. (Hugging Face, Facebook AI Research, University of Waterloo, University College London) (p. 1) |
| Año y sede | 2022. arXiv v2 del 22-04-2022 (p. 1). La sede no figura en el texto del preprint; F01 (Yuksekgonul et al., 2023, p. 14) lo cita como CVPR 2022, pp. 5238–5248 |
| Identificador | arXiv:2204.03162 |
| PDF | `pdfs/F02_thrush_2022_winoground.pdf` · https://arxiv.org/pdf/2204.03162 |
| Eje | E. Orden y composición en modelos visión-lenguaje |
| Origen del registro | búsqueda dirigida |
| Nivel de lectura | completo (texto extraído del PDF, 18 páginas; revisado el 20-11-2026). Las imágenes de los ejemplos, los mapas de calor (fig. 4 y apéndice D) y los gráficos del apéndice B no son legibles en la extracción; el cuadro 2 del apéndice C sale con las columnas fusionadas |

## Qué hace

- **Datos.** 400 ejemplos curados a mano por cuatro anotadores expertos; 1 600 pares imagen-texto (800 correctos y 800 incorrectos), 800 pies e imágenes únicos (p. 2–4). Imágenes de Getty Images con licencia para investigación (p. 3); solo inglés (p. 8). 70 etiquetas lingüísticas finas agrupadas en objeto (141), relación (233) y ambos (26), más etiquetas visuales: simbólico (41), serie (31), pragmática (24) (p. 3, cuadro 1).
- **Tarea y protocolo.** Emparejar dos imágenes con dos pies que contienen exactamente las mismas palabras en distinto orden; puntajes de texto, imagen y grupo (ec. 1–3, p. 4). Intervalos de confianza del 95 % con t de Student sobre 4 grupos iguales (apéndice A, p. 13).
- **Método.** Solo benchmark: se puntúan modelos preentrenados y una línea base humana con Amazon Mechanical Turk, al menos 10 anotadores por par, que ven un par imagen-pie a la vez (p. 5; criterios de admisión en p. 17).
- **Comparadores.** UNITER, ViLLA, VinVL, ViLT, LXMERT, ViLBERT, UniT, VisualBERT, FLAVA (ITM y contrastivo), CLIP ViT-B/32, VSE++ y VSRN (p. 4–6) y humanos.
- **Resultados.** Cuadro 3 (p. 6), texto / imagen / grupo: humanos 89,50 / 88,50 / 85,50; azar 25,00 / 25,00 / 16,67; CLIP 30,75 / 10,50 / 8,00 (IC 95 % del grupo [4,56; 11,44], p. 13). CLIP queda por debajo del azar en imagen y grupo. Todos los modelos están por debajo del azar en el puntaje de grupo (p. 5). En la etiqueta «serie» (imágenes de la misma sesión fotográfica) la mayoría obtiene 0 % de grupo (p. 6, cuadro 5). El puntaje baja con la longitud del pie en los mejores modelos (CLIP r = −0,22, cuadro 6, p. 8) y correlaciona con el tamaño de los datos de preentrenamiento si se excluyen CLIP y FLAVA (r entre 0,71 y 0,84, cuadro 7, p. 8).
- **Limitaciones declaradas.** Solo inglés, tamaño reducido, curación costosa, anotadores (y quizá trabajadores) mayoritariamente de EE. UU. (p. 8); la línea base humana subestima la pragmática porque se mostraba un par a la vez (p. 6).
- **Código y datos.** Datos en huggingface.co/datasets/facebook/winoground (p. 1); un repositorio de código no figura en el texto.

## Aporte a la tesis

Segunda fuente, independiente de ARO, de que los modelos tipo CLIP no distinguen configuraciones con los mismos elementos en otro orden. Es el análogo lingüístico de dos textiles con el mismo histograma de bandas y distinta secuencia, que es exactamente lo que separa M3 de M3-sin-orden. El fracaso en la etiqueta «serie» (imágenes muy parecidas entre sí, p. 6) es pertinente para piezas de un mismo estilo.

## Cautela al citar

400 ejemplos y un dominio distinto. Usarlo junto con F01 y sin extrapolar cifras. La sede (CVPR 2022) no está en el preprint; tomarla de la versión publicada antes de citarla.

## Actualización del 20 de noviembre de 2026

- Se leyó el texto completo (18 páginas, con apéndices A–F); se completaron autores y afiliaciones.
- Se confirmaron con página las cifras del cuadro 3, el número de anotadores humanos y las limitaciones declaradas; se añadieron los conteos de etiquetas, los intervalos de confianza y las correlaciones con longitud y tamaño de datos.
- Sede: no figura en el texto del preprint; solo se dispone de la cita de F01 (CVPR 2022). Un repositorio de código no figura en el texto.
- Sigue sin verificar el contenido de los mapas de calor y gráficos (no legibles en la extracción).

---
Leído el 11 de noviembre de 2026 y completado el 20 de noviembre de 2026 con asistencia computacional, sobre el texto completo extraído del PDF. «NV» marca lo que no se pudo comprobar.
