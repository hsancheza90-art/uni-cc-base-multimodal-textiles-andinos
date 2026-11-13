# F10 · Helmer (2015)

**A Similarity Measure for Weaving Patterns in Textiles**

| Campo | Valor |
|---|---|
| Autores | Helmer, S.; Ngo, V. M. |
| Año y sede | 2015. SIGIR 2015 según OpenAlex; leído en la versión de arXiv (2018) |
| Identificador | doi:10.1145/2766462.2767735; arXiv:1810.04604 |
| PDF | `pdfs/F10_helmer_ngo_2015_similitud_tejidos.pdf` · https://arxiv.org/pdf/1810.04604 |
| Eje | B. Representación y recuperación de textiles |
| Origen del registro | OpenAlex (B2) |
| Nivel de lectura | parcial: primeros ~40 000 caracteres literales; el resto, resumen automático |

## Qué hace

- **Datos.** Unas 1 200 muestras textiles en 12 categorías de 100; en promedio 25 352 vértices y 6 311 cruces por muestra. La introducción cita textiles andinos y el proyecto previo de base de conocimiento andina.
- **Tarea y protocolo.** Agrupamiento jerárquico frente a las categorías conocidas y recuperación en la que cada textil es consulta y son relevantes los de su misma categoría.
- **Método.** Cada textil es un hipergrafo de cruces de hilos. Cada cruce recibe una etiqueta de vecindad de radio k y el textil se representa como multiconjunto de etiquetas, comparado con Jaccard, Hamming o coseno.
- **Comparadores.** Solo variantes de distancia entre sí; ninguna línea base externa vista.
- **Resultados.** MAP cercano a 0,93 según la introducción. El resto de cifras: NV.
- **Limitaciones declaradas.** NV: modelado manual de cada textil, necesidad de más datos.
- **Código y datos.** No visto.

## Aporte a la tesis

Antecedente directo de recuperación por estructura textil, con raíz en el trabajo andino de Birkbeck. Delimita la brecha con precisión: trabajan a escala de hilos, modelan cada pieza a mano, toman la categoría como verdad y no se comparan con ningún modelo visual. La tesis trabaja con la macroestructura visible en fotografías, juicios graduados ciegos y comparación con OpenCLIP.

## Cautela al citar

Año y sede no aparecen en el PDF leído; tomados de OpenAlex.

---
Leído el 11 de noviembre de 2026 con asistencia computacional. «NV» marca lo que no se vio en el texto literal del documento y debe comprobarse en el PDF antes de citarlo.
