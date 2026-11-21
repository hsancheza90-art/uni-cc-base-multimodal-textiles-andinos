# F21 · Card (2020)

**With Little Power Comes Great Responsibility**

| Campo | Valor |
|---|---|
| Autores | Card, D.; Henderson, P.; Khandelwal, U.; Jia, R.; Mahowald, K.; Jurafsky, D. |
| Año y sede | 2020. arXiv v1, 13 de octubre de 2020 (p. 1). La sede editorial no figura en el texto |
| Identificador | arXiv:2010.06595 |
| PDF | `pdfs/F21_card_2020_potencia.pdf` · https://arxiv.org/pdf/2010.06595 |
| Eje | G. Evaluación de recuperación |
| Origen del registro | búsqueda dirigida |
| Nivel de lectura | completo (texto extraído del PDF, 32 páginas; revisado el 20-11-2026). Las figuras y las páginas 29-32 (gráficos de solapamiento) solo se leen por sus etiquetas |

## Qué hace

- **Datos.** Tareas de GLUE (14 artículos, 119 comparaciones y 57 afirmaciones de mejora), SQuAD 2.0 (144 modelos), WMT inglés-alemán 2016-2019 y 117 comparaciones con escala Likert de 41 artículos de EMNLP 2019 (pp. 4, 7, 16).
- **Tarea y protocolo.** Si las comparaciones habituales tienen potencia para detectar los efectos que se afirman.
- **Método.** Análisis de potencia por simulación (algoritmo de la fig. 2, p. 3): proceso generativo con efecto supuesto, prueba elegida de antemano, repetición y proporción de resultados significativos con el signo correcto. Parámetros estimados con datos de validación, regresión sobre resultados publicados o supuestos neutros (Lachenbruch) (pp. 4-5). Pruebas: McNemar (exactitud), aleatorización con intercambio de pares con probabilidad 0,5 (BLEU y otras métricas, pp. 6 y 21), modelos mixtos (Likert).
- **Comparadores.** No aplica.
- **Resultados.** Ejemplo ilustrativo: potencia ≈ 30 % con n = 25 frente a más del 80 % con n = 100 (fig. 1, p. 1). En WNLI, MRPC y SST-2 la mejora media publicada está por debajo del efecto mínimo detectable (tabla 2, p. 5); solo el 46 % de las comparaciones de GLUE habría tenido potencia adecuada (p. 5). Un conjunto de 2000 frases tiene ≈ 75 % de potencia para 1 punto BLEU (p. 7). El diseño humano más común (3 evaluadores, 100 ítems) no tiene potencia salvo para efectos ≥ 0,2 en escala [0, 1] (p. 9). Ejemplo numérico: n = 500, potencia ≈ 0,25 y error de tipo M de 1,9 (p. 15). No se recomienda calcular la potencia a posteriori con el efecto observado (p. 2, nota 2; p. 13).
- **Limitaciones declaradas.** Confirmado: los priores por regresión ajustan de forma imperfecta (R² = 0,69 para el efecto, p. 4; «no es un prior perfecto», p. 19). Estimar con datos de validación puede dar exceso de confianza si la validación está inflada; recomiendan combinarla con priores razonables (p. 16). Las estimaciones de MT se basan en un solo par de idiomas (p. 7).
- **Código y datos.** github.com/dallascard/NLP-power-analysis (p. 1).

## Aporte a la tesis

Da el marco para el análisis de potencia que pide el asesor en 8.e. Con 30 consultas, lo honesto es informar el efecto mínimo detectable calculado antes del test con la varianza de desarrollo, no una potencia calculada después con el efecto observado. Si Δ = 0,03 queda por debajo de ese mínimo, el estudio se declara sin potencia para ese umbral y se informa el intervalo.

## Cautela al citar

Los ejemplos son de procesamiento de lenguaje; el razonamiento es general. Ninguno de los casos estudiados tiene tamaños del orden de 30 consultas: el menor es n = 25 en el ejemplo ilustrativo de la fig. 1.

## Actualización del 20 de noviembre de 2026

- Verificado con página: fig. 1 (p. 1), tabla 2 (p. 5), advertencia sobre potencia a posteriori (p. 2 y p. 13) y limitación de los priores (pp. 4 y 19), antes NV.
- Agregado: el algoritmo de simulación cuenta como detección solo los resultados significativos con el signo correcto (p. 3) y la definición de errores de tipo M y S (pp. 14-15).
- Afecta al diseño: el efecto mínimo detectable debe calcularse antes del test, para un rango de valores y no solo para una estimación puntual (p. 3), y con la prueba que se usará (aquí, permutación por cambio de signo). Estimar la varianza solo con las 10 consultas de desarrollo es la vía «datos de validación», que el artículo advierte que puede dar exceso de confianza (p. 16): conviene informar la sensibilidad del efecto mínimo a esa varianza. Si Δ = 0,03 queda por debajo del mínimo detectable, un resultado significativo tendría riesgo alto de exagerar el efecto (tipo M).
- Sigue sin verificar: la sede editorial (no figura en el texto).

---
Leído el 11 de noviembre de 2026 y completado el 20 de noviembre de 2026 con asistencia computacional, sobre el texto completo extraído del PDF. «NV» marca lo que no se pudo comprobar.
