# F28 · Rudin (2019)

**Stop Explaining Black Box Machine Learning Models for High Stakes Decisions and Use Interpretable Models Instead**

| Campo | Valor |
|---|---|
| Autores | Rudin, C. |
| Año y sede | 2019. arXiv v3 [stat.ML], 22 de septiembre de 2019 (p. 1). La sede editorial no figura en el texto; solo indica que una versión preliminar apareció en el NeurIPS 2018 Workshop on Critiquing and Correcting Trends in Machine Learning (p. 1; ref. 13, p. 16) |
| Identificador | arXiv:1811.10154 |
| PDF | `pdfs/F28_rudin_2019_modelos_interpretables.pdf` · https://arxiv.org/pdf/1811.10154 |
| Eje | I. Interpretabilidad y fidelidad |
| Origen del registro | búsqueda dirigida |
| Nivel de lectura | completo (texto extraído del PDF, 20 páginas; revisado el 20-11-2026). La figura 4 (sistema de puntuación) no es legible en el texto extraído |

## Qué hace

- **Datos.** Artículo de posición con ejemplos de justicia penal (COMPAS, CORELS), calidad del aire (BreezoMeter), salud, riesgo crediticio (FICO) y visión (redes de prototipos).
- **Tarea y protocolo.** Si conviene explicar cajas negras o usar modelos interpretables por diseño, en decisiones de alto riesgo y en la depuración de modelos (p. 1).
- **Método.** Argumenta que una explicación a posteriori no puede ser del todo fiel al modelo que explica: si lo fuera, sería el modelo (p. 3). La interpretabilidad es una restricción del modelo propia de cada dominio: monotonía, causalidad, aditividad, dispersión, razonamiento por casos (p. 1). Propone tres retos algorítmicos: modelos lógicos óptimos, sistemas de puntuación dispersos y definiciones de interpretabilidad por dominio, incluida la visión (pp. 9-13).
- **Comparadores.** No aplica.
- **Resultados.** Afirma que no hay necesariamente un compromiso entre exactitud e interpretabilidad, sobre todo con datos estructurados y atributos con significado (p. 2; apéndice B, p. 19). Ejemplo: un modelo CORELS de tres reglas (edad, antecedentes y, opcionalmente, sexo) tiene tasas de verdaderos y falsos positivos similares a COMPAS en Broward County (fig. 3 y tabla 1, p. 6). Un modelo aditivo, globalmente interpretable, ganó el premio de reconocimiento del FICO Explainable ML Challenge 2018 (p. 14). Los mapas de saliencia solo dicen dónde mira la red, no qué hace (pp. 4-5). Argumento del conjunto Rashomon (p. 14).
- **Limitaciones declaradas.** Construir modelos interpretables exige esfuerzo computacional y de conocimiento del dominio (p. 8); admite que podría haber dominios que requieran una caja negra, aunque dice no haberlos encontrado (p. 3); en visión la interpretabilidad es más difícil de definir y la dispersión en píxeles no tiene sentido (p. 12).
- **Código y datos.** No aplica (cita el código abierto de CORELS, p. 6).

## Aporte a la tesis

Respalda la decisión de diseño de M4: un score aditivo que se explica a sí mismo, en lugar de explicar M2 a posteriori. Permite formular la contribución como una elección de familia de modelos y no como una mejora de rendimiento, que es lo que pide el asesor en 2.c.

## Cautela al citar

El artículo trata decisiones de alto riesgo; aquí el argumento se usa por analogía. La tesis de que no hay compromiso entre exactitud e interpretabilidad se apoya en datos estructurados con atributos con significado (p. 2); para imágenes la autora reconoce que el aprendizaje profundo aporta ganancias importantes (p. 2), de modo que no sirve para anticipar que M3 o M4 igualen a M2.

## Actualización del 20 de noviembre de 2026

- Verificado con página: el argumento de fidelidad (p. 3), la aditividad como forma de interpretabilidad (p. 1), el ejemplo de tres reglas frente a COMPAS (p. 6) y la reserva sobre dominios que requieran caja negra (p. 3).
- Corregido: fecha exacta de la versión arXiv (22-09-2019) y origen en un taller de NeurIPS 2018; la sede de publicación definitiva no figura en el texto. Se precisó que el ejemplo de tres reglas compara tasas de error, no «exactitud» en general.
- Afecta al diseño de M4 y H3: la descomposición aditiva del score es fiel por construcción, pero el término de OpenCLIP sigue siendo una caja negra dentro de la suma, de modo que la explicación es fiel al score sin explicar ese término; conviene decirlo al formular H3. El apéndice B (p. 19) advierte del sesgo de ajustar más el método propio que las líneas base: argumento para fijar los pesos de M4 solo con las 10 consultas de desarrollo y aplicar el mismo esfuerzo de ajuste a los comparadores.
- Sigue sin verificar: la sede editorial definitiva (no figura en el texto).

---
Leído el 11 de noviembre de 2026 y completado el 20 de noviembre de 2026 con asistencia computacional, sobre el texto completo extraído del PDF. «NV» marca lo que no se pudo comprobar.
