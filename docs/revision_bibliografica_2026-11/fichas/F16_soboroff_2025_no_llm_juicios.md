# F16 · Soboroff (2025)

**Don't Use LLMs to Make Relevance Judgments**

| Campo | Valor |
|---|---|
| Autores | Soboroff, I. |
| Año y sede | 2025. Information Retrieval Research 1(1), 29–46 |
| Identificador | doi:10.54195/irrj.19625 |
| PDF | `pdfs/F16_soboroff_2025_no_llm_juicios.pdf` · https://irrj.org/article/download/19625/25085/60555 |
| Eje | G. Evaluación de recuperación |
| Origen del registro | OpenAlex (G1) |
| Nivel de lectura | completo |

## Qué hace

- **Datos.** Sin experimentos propios; la figura 1 procede de Soboroff et al. (2001) sobre TREC-8.
- **Tarea y protocolo.** Por qué no deben generarse juicios de relevancia con un modelo.
- **Método.** Argumento: la clave de respuestas es un techo. Como lo no juzgado cuenta como no relevante, un sistema que encuentra relevantes nuevos puntúa peor. Si el modelo que juzga está entre los sistemas evaluados, esos sistemas parecen peores aunque lo superen (sec. 6).
- **Comparadores.** No aplica.
- **Resultados.** Sin cifras propias. Sostiene que los juicios hechos por un modelo solo pueden medir sistemas peores que ese modelo, y que el argumento vale para cualquier juez, humano o máquina.
- **Limitaciones declaradas.** El argumento cubre al modelo como clave de respuestas; admite que un modelo ayude a detectar errores de los evaluadores.
- **Código y datos.** No aplica.

## Aporte a la tesis

Da la razón teórica de dos reglas del protocolo: los qrels no pueden derivarse de CLIP ni de la fórmula de M3, y el juicio debe ser ciego al sistema. Además obliga a nombrar una circularidad propia: la misma persona produce las etiquetas que usa M3 y los juicios con los que se evalúa. El argumento del techo se aplica también ahí, y es la mejor justificación del doble juicio parcial.

## Cautela al citar

Es un artículo de posición. Citarlo como argumento, no como resultado empírico.

---
Leído el 11 de noviembre de 2026 con asistencia computacional. «NV» marca lo que no se vio en el texto literal del documento y debe comprobarse en el PDF antes de citarlo.
