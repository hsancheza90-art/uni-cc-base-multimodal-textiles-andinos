# F14 · Contreras (2026)

**Structural Pattern Mining in Inka Khipus: Unsupervised Clustering, Provenance Classification, and a Computational Validation of the Santa Valley Match**

| Campo | Valor |
|---|---|
| Autores | Contreras, M. |
| Año y sede | 2026. arXiv, prepublicación de una sola autora, sin arbitraje |
| Identificador | arXiv:2607.00185 |
| PDF | `pdfs/F14_contreras_2026_khipus.pdf` · https://arxiv.org/pdf/2607.00185 |
| Eje | A. Cómputo sobre artefactos andinos |
| Origen del registro | OpenAlex (A2) |
| Nivel de lectura | completo |

## Qué hace

- **Datos.** Open Khipu Repository: 619 khipus, 54 403 cuerdas, 110 677 nudos; 135 ejemplares con etiqueta de región usados para clasificar.
- **Tarea y protocolo.** Agrupamiento no supervisado y clasificación de procedencia en siete clases con validación cruzada de cinco pliegues.
- **Método.** Cada khipu se resume en un vector de 27 rasgos agregados (estructura de cuerdas, torsión, nudos, color). El orden de los tipos de nudo se prueba solo como bigramas TF-IDF.
- **Comparadores.** Modelo con bigramas frente a modelo de rasgos agregados; comparación con Medrano y Urton (2018).
- **Resultados.** Tres grupos con silueta 0,769; F1 ponderado 0,46 en procedencia (tabla 1). Añadir los bigramas de orden no mejora (ΔF1 ≈ −0,006).
- **Limitaciones declaradas.** Muestra etiquetada pequeña, etiquetas de región que pueden no coincidir con límites culturales, sesgo de colección y de registro, datos de torsión imputados con cero.
- **Código y datos.** Repositorio en GitHub y cuaderno en Kaggle; datos del OKR (doi:10.5281/zenodo.18025748).

## Aporte a la tesis

Caso andino cercano en el que la información de orden no añadió señal sobre los rasgos agregados. Es un precedente honesto para la discusión si H2 no se sostiene, y un ejemplo de cómo informar un resultado negativo sobre secuencias. También recuerda los sesgos de colección que comparte el corpus de museos.

## Cautela al citar

Prepublicación sin revisión por pares y con evaluación débil (F1 0,46). No apoyarse en ella como evidencia; citarla, si acaso, como trabajo relacionado y marcando su estado.

---
Leído el 11 de noviembre de 2026 con asistencia computacional. «NV» marca lo que no se vio en el texto literal del documento y debe comprobarse en el PDF antes de citarlo.
