# F28 · Rudin (2019)

**Stop Explaining Black Box Machine Learning Models for High Stakes Decisions and Use Interpretable Models Instead**

| Campo | Valor |
|---|---|
| Autores | Rudin, C. |
| Año y sede | 2019. arXiv v3, septiembre de 2019 (sede no vista en el texto leído) |
| Identificador | arXiv:1811.10154 |
| PDF | `pdfs/F28_rudin_2019_modelos_interpretables.pdf` · https://arxiv.org/pdf/1811.10154 |
| Eje | I. Interpretabilidad y fidelidad |
| Origen del registro | búsqueda dirigida |
| Nivel de lectura | parcial: primeros ~40 000 caracteres literales; el resto, resumen automático |

## Qué hace

- **Datos.** Artículo de posición con ejemplos de justicia penal, salud y visión.
- **Tarea y protocolo.** Si conviene explicar cajas negras o usar modelos interpretables por diseño.
- **Método.** Argumenta que una explicación a posteriori no puede ser del todo fiel al modelo que explica y que la interpretabilidad es una restricción del modelo (por ejemplo, la aditividad).
- **Comparadores.** No aplica.
- **Resultados.** Afirma que no hay necesariamente un compromiso entre exactitud e interpretabilidad y da un ejemplo en el que un modelo de tres reglas iguala a uno opaco. Reconoce que construir modelos interpretables exige esfuerzo y que puede haber dominios que requieran una caja negra.
- **Limitaciones declaradas.** Los ya indicados.
- **Código y datos.** No aplica.

## Aporte a la tesis

Respalda la decisión de diseño de M4: un score aditivo que se explica a sí mismo, en lugar de explicar M2 a posteriori. Permite formular la contribución como una elección de familia de modelos y no como una mejora de rendimiento, que es lo que pide el asesor en 2.c.

## Cautela al citar

El artículo trata decisiones de alto riesgo; aquí el argumento se usa por analogía.

---
Leído el 11 de noviembre de 2026 con asistencia computacional. «NV» marca lo que no se vio en el texto literal del documento y debe comprobarse en el PDF antes de citarlo.
