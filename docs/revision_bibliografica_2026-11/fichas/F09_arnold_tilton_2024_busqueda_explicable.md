# F09 · Arnold (2024)

**Explainable Search and Discovery of Visual Cultural Heritage Collections with Multimodal Large Language Models**

| Campo | Valor |
|---|---|
| Autores | Arnold, T.; Tilton, L. |
| Año y sede | 2024. CHR 2024, CEUR Workshop Proceedings vol. 3834 |
| Identificador | sin DOI |
| PDF | `pdfs/F09_arnold_tilton_2024_busqueda_explicable.pdf` · https://ceur-ws.org/Vol-3834/paper1.pdf |
| Eje | I. Interpretabilidad y fidelidad |
| Origen del registro | auditoría (S20), ahora leído |
| Nivel de lectura | completo |

## Qué hace

- **Datos.** Unas 16 000 fotografías documentales de los años setenta (Documerica).
- **Tarea y protocolo.** Búsqueda, recomendación y agrupamiento en colecciones visuales sin metadatos finos; sin verdad de referencia.
- **Método.** Un modelo multimodal genera una descripción de cada imagen; la descripción se convierte en embedding de texto. La explicación de cada conjunto recomendado son los cinco sustantivos más característicos.
- **Comparadores.** Embeddings de imagen (EfficientNet). CLIP no se usa.
- **Resultados.** Recomendaciones simétricas: 36,5–49,8 % con el método multimodal frente a 22,4–28,9 % con imagen (tabla 1). Coincidencia de términos juzgada a mano en 120 imágenes: 99,6 % frente a 96,2 % (tabla 3).
- **Limitaciones declaradas.** Las descripciones no son infalibles; más del 80 % contiene expresiones de duda; los términos de género producen coincidencias estereotipadas. Sin estudio con usuarios.
- **Código y datos.** Descripciones en distantviewing.org/downloads.

## Aporte a la tesis

Es el contraste útil para H3. Aquí la explicación es un texto plausible generado aparte del cálculo de similitud. En M4 la explicación es la propia descomposición del score. Permite argumentar la diferencia entre explicación verosímil y explicación fiel con un ejemplo patrimonial reciente.

## Cautela al citar

Ellos mismos reconocen que no hay verdad de referencia: no es una evaluación de recuperación.

---
Leído el 11 de noviembre de 2026 con asistencia computacional. «NV» marca lo que no se vio en el texto literal del documento y debe comprobarse en el PDF antes de citarlo.
