# F17 · Santini (2023)

**Multimodal Search on Iconclass using Vision-Language Pre-Trained Models**

| Campo | Valor |
|---|---|
| Autores | Santini, C.; Tan, M. A.; Posthumus, E.; et al. |
| Año y sede | 2023. JCDL 2023 según OpenAlex (no visto en el texto leído) |
| Identificador | doi:10.1109/jcdl57899.2023.00061; arXiv:2306.16529 |
| PDF | `pdfs/F17_santini_2023_iconclass.pdf` · https://arxiv.org/pdf/2306.16529 |
| Eje | C. Recuperación multimodal en patrimonio |
| Origen del registro | OpenAlex (C1) |
| Nivel de lectura | completo |

## Qué hace

- **Datos.** Unas 531 172 imágenes de obras anotadas con notaciones Iconclass (iniciativa Arkyves).
- **Tarea y protocolo.** Una consulta de texto o imagen devuelve notaciones Iconclass a partir de las imágenes anotadas más cercanas en el espacio de CLIP.
- **Método.** Embeddings de CLIP, índice Faiss y agregación de las notaciones de los vecinos por frecuencia. La jerarquía de Iconclass no interviene en el modelo.
- **Comparadores.** La búsqueda TF-IDF existente.
- **Resultados.** Encuesta de preferencia con 10 voluntarios: 105 preferencias por el sistema multimodal y 104 por TF-IDF; en precisión 64 frente a 72 y en exhaustividad 30 frente a 17 (tabla 1).
- **Limitaciones declaradas.** Sin verdad de referencia objetiva, la calidad de CLIP queda por estimar; proponen el sistema como complemento.
- **Código y datos.** github.com/ISE-FIZKarlsruhe/iconclass

## Aporte a la tesis

Caso patrimonial con vocabulario iconográfico controlado en el que CLIP no supera con claridad a una línea base léxica. Apoya mantener M0 como comparador serio y no como formalidad. También muestra el costo de no tener qrels: solo pudieron hacer una encuesta de preferencia.

## Cautela al citar

Diez voluntarios y sin prueba estadística.

---
Leído el 11 de noviembre de 2026 con asistencia computacional. «NV» marca lo que no se vio en el texto literal del documento y debe comprobarse en el PDF antes de citarlo.
