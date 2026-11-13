# F21 · Card (2020)

**With Little Power Comes Great Responsibility**

| Campo | Valor |
|---|---|
| Autores | Card, D.; Henderson, P.; Khandelwal, U.; Jia, R.; Mahowald, K.; Jurafsky, D. |
| Año y sede | 2020. arXiv v1 (sede no vista en el texto leído) |
| Identificador | arXiv:2010.06595 |
| PDF | `pdfs/F21_card_2020_potencia.pdf` · https://arxiv.org/pdf/2010.06595 |
| Eje | G. Evaluación de recuperación |
| Origen del registro | búsqueda dirigida |
| Nivel de lectura | parcial: primeros ~40 000 caracteres literales; el resto, resumen automático |

## Qué hace

- **Datos.** Tareas de GLUE, SQuAD 2.0, conjuntos de WMT y 117 comparaciones con escala Likert de 41 artículos.
- **Tarea y protocolo.** Si las comparaciones habituales tienen potencia para detectar los efectos que se afirman.
- **Método.** Análisis de potencia por simulación, con priores estimados a partir de resultados publicados.
- **Comparadores.** No aplica.
- **Resultados.** Un conjunto de prueba pequeño hace grande el efecto mínimo detectable. Ejemplo ilustrativo: potencia cercana al 30 % con n = 25 frente a más del 80 % con n = 100 (figura 1). En varios conjuntos pequeños las mejoras publicadas están por debajo del efecto mínimo detectable (sec. 3.3). Advierten que no se recomienda calcular la potencia a posteriori con el efecto observado.
- **Limitaciones declaradas.** NV: los priores ajustan de forma imperfecta.
- **Código y datos.** github.com/dallascard/NLP-power-analysis

## Aporte a la tesis

Da el marco para el análisis de potencia que pide el asesor en 8.e. Con 30 consultas, lo honesto es informar el efecto mínimo detectable calculado antes del test con la varianza de desarrollo, no una potencia calculada después con el efecto observado. Si Δ = 0,03 queda por debajo de ese mínimo, el estudio se declara sin potencia para ese umbral y se informa el intervalo.

## Cautela al citar

Los ejemplos son de procesamiento de lenguaje; el razonamiento es general.

---
Leído el 11 de noviembre de 2026 con asistencia computacional. «NV» marca lo que no se vio en el texto literal del documento y debe comprobarse en el PDF antes de citarlo.
