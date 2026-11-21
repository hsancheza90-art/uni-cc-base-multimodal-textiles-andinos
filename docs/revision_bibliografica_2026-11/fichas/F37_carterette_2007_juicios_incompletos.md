# F37 · Carterette (2007)

**Hypothesis Testing with Incomplete Relevance Judgments**

| Campo | Valor |
|---|---|
| Autores | Carterette, B.; Smucker, M. D. (University of Massachusetts Amherst) |
| Año y sede | 2007. CIKM '07 (ACM Conference on Information and Knowledge Management), 6-8 de noviembre de 2007, Lisboa (p. 1). El texto no da las páginas en las actas, el título completo de las actas ni el número de edición |
| Identificador | ISBN 978-1-59593-803-9 (p. 1). El DOI no figura en el texto |
| PDF | `pdfs/IR-620.pdf` |
| Eje | Evaluación de recuperación (juicios incompletos y pruebas de significación) |
| Origen del registro | aportado por el investigador (20-11-2026) |
| Nivel de lectura | completo (texto extraído del PDF, 10 páginas). Las figuras 2-8 se leen por sus leyendas y el texto que las comenta |

## Qué hace

- **Datos.** 249 temas y 110 sistemas de la TREC 2004 Robust track; los 249 temas se tratan como «población» de la que se muestrea (p. 4). Medida: AP y MAP (p. 6).
- **Tarea y protocolo.** Cómo afectan los juicios incompletos a las conclusiones de una prueba de hipótesis, con foco en la potencia (p. 1). Estudian **solo la prueba de signos** unilateral, por su simplicidad; dejan la t y Wilcoxon para trabajo futuro (pp. 2 y 10).
- **Método.** Modelan la incertidumbre por juicios incompletos como la probabilidad λ de acertar el signo de la diferencia en un tema (p. 5). Deducen que, para mantener la potencia, hacen falta n′ = n · (1/(2λ − 1))² temas (ec. 3, p. 5). Estiman la probabilidad del signo con la esperanza y la varianza de ΔAP, poniendo p = 1/2 como probabilidad de relevancia de cada documento no juzgado (p. 6). Ajustan un modelo de Poisson del número de juicios necesario según λ y n (ec. 6, p. 7; R² = 0,95) y una función de coste temas-juicios (ec. 7, p. 8). Proponen un piloto de 10 temas para calibrar el modelo en una tarea nueva (p. 9).
- **Comparadores.** Más temas con pocos juicios frente a pocos temas (25) con juicios completos y frente a un pool de profundidad 100 (pp. 8-9).
- **Resultados.** Potencia observada cercana a la teórica, aunque algo mayor y con errores típicos altos (cuadro 2, pp. 4-5). Evaluar 192 temas con 68 % de confianza (menos de 5 juicios por tema) es tan bueno como 25 temas con unos 166 juicios por tema: 85 % menos esfuerzo y ningún error adicional (p. 1). En 2000 pares, el 83 % de los pares con efecto 0,5 resultó significativo con 192 temas (p. 8). Si los temas cuestan 20 veces más que un juicio, conviene a menudo juzgar 25 temas por completo (pp. 9-10).
- **Limitaciones declaradas.** El modelo que predice el número de juicios tiene mucha varianza (correlación 0,43 entre lo predicho y lo real; pp. 9-10). Solo comparan pares de sistemas: el problema de comparaciones múltiples queda fuera del alcance (p. 10). Solo se analiza la prueba de signos (p. 10).
- **Código y datos.** No se publica código; usan datos de la TREC 2004 Robust track (p. 4).

## Aporte a la tesis

- **¿Los juicios incompletos afectan a las pruebas de significación?** **Matiza.** Según el análisis, la incertidumbre por juicios incompletos **no afecta a la exactitud** (el error de tipo I): si la hipótesis nula es cierta, el número esperado de éxitos sigue siendo n/2 (sección 3.4.1, p. 5; también p. 1, «cuando la incertidumbre se tiene en cuenta»). En cambio, **reduce la potencia**, y recuperarla exige más temas o más juicios (pp. 5-6). La conclusión depende de un supuesto: los errores de signo se reparten por igual entre los dos sistemas (λ simétrica, p. 5). Si los no juzgados perjudican más a un sistema que a otro, el supuesto no se cumple; el artículo no trata ese caso (observación propia).
- **Contar como 0 los no juzgados.** El texto reconoce que suponer no relevante todo lo no juzgado es «la suposición estándar en la evaluación de RI», pero objeta que no permite asignar una probabilidad a la predicción (p. 6). Su modelo usa p = 1/2 para los no juzgados al estimar la confianza (p. 6). Por tanto, el artículo **no respalda ni evalúa directamente** el efecto de contar como 0 sobre la prueba; solo lo describe como práctica estándar. Para la tesis (inferencia propia): los sistemas que aportaron sus 10 primeros al pool no tienen documentos sin juzgar dentro del corte de nDCG@10, así que el riesgo se concentra en sistemas que no aportaron al pool (por ejemplo, M4 si se evalúa después) y en el cálculo del DCG ideal. Para el sesgo del pool, ver F15 (Buckley et al., 2007).
- **Pocas consultas.** **Matiza**: la potencia de la prueba de signos con 25 temas es baja (0,22-0,73 según el efecto; cuadro 2, p. 5), y un único contraste no basta para conclusiones fuertes (p. 4). La tesis no usa la prueba de signos, pero el aviso sobre la potencia con pocas consultas vale para las 10 de desarrollo.

## Citas útiles

- Cuando la incertidumbre se tiene en cuenta, los juicios incompletos no afectan a la exactitud de la prueba; el efecto recae en la potencia (pp. 1 y 5).
- A medida que aumenta la incertidumbre, el número de temas necesario para mantener la potencia crece de forma exponencial (pp. 5-6, fig. 3).
- Suponer no relevante lo no juzgado es la suposición estándar en RI, pero no permite asignar una probabilidad a la predicción (p. 6).
- Muchos temas con pocos juicios evalúan tan bien como pocos temas con muchos juicios y con mucho menos esfuerzo (pp. 1 y 10).
- Las conclusiones de una prueba pueden variar mucho de una muestra de temas a otra; un solo contraste no basta para conclusiones fuertes (p. 4).
- Si se elimina un tema como empate, la prueba de signos pierde menos potencia que asignándolo al azar (p. 5).
- Con varios sistemas aparece el problema de comparaciones múltiples, que exige ajustar las tasas de error y queda fuera del trabajo (p. 10).

## Cautela al citar

Todo el análisis es para la prueba de signos unilateral con AP/MAP; no se puede trasladar sin más a la permutación por cambio de signo sobre nDCG@10. La afirmación de que la exactitud se mantiene supone errores de signo simétricos entre los dos sistemas. No dice que contar como 0 los no juzgados sea inocuo. La «población» de temas son los 249 de Robust 2004, en la que la hipótesis nula nunca es exactamente cierta (pp. 8-9).

---
Leído el 20 de noviembre de 2026 con asistencia computacional, sobre el texto completo extraído del PDF.
