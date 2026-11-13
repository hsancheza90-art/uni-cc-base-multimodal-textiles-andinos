# F04 · Bruch (2023)

**An Analysis of Fusion Functions for Hybrid Retrieval**

| Campo | Valor |
|---|---|
| Autores | Bruch, S.; Gai, S.; Ingber, A. |
| Año y sede | 2023. arXiv v2, mayo de 2023 (sede editorial no vista) |
| Identificador | arXiv:2210.11934 |
| PDF | `pdfs/F04_bruch_2023_fusion.pdf` · https://arxiv.org/pdf/2210.11934 |
| Eje | F. Fusión tardía de scores |
| Origen del registro | búsqueda dirigida |
| Nivel de lectura | parcial: primeros ~40 000 caracteres literales; el resto, resumen automático |

## Qué hace

- **Datos.** MS MARCO Passage v1 (8,8 M de pasajes, 6 980 consultas de desarrollo) y ocho colecciones BEIR.
- **Tarea y protocolo.** Recuperación híbrida léxica y densa; Recall@1000 y NDCG@1000; ajuste en MS MARCO y evaluación dentro y fuera de dominio.
- **Método.** Fusionan BM25 y un codificador denso sobre la unión de los 1000 primeros candidatos. Comparan la combinación convexa de scores normalizados con Reciprocal Rank Fusion y analizan la normalización.
- **Comparadores.** BM25 solo, denso solo, RRF.
- **Resultados.** El resumen afirma que la combinación convexa supera a RRF dentro y fuera de dominio y que RRF es sensible a sus parámetros. La combinación aprendida es en general indiferente a la normalización elegida; las normalizaciones lineales son equivalentes en orden salvo un reajuste de pesos (lema 4.2, teorema 4.5). Bastan unas pocas consultas etiquetadas para ajustar el peso. Cifras de la tabla 2 (por ejemplo MS MARCO 0,454 frente a 0,425): NV.
- **Limitaciones declaradas.** NV: solo analizan dos recuperadores; la extensión a más sistemas queda abierta.
- **Código y datos.** No visto.

## Aporte a la tesis

Respalda el diseño de M4: fusión convexa de scores normalizados por consulta, con pesos ajustados en pocas consultas de desarrollo. También advierte que el análisis cubre dos componentes y M4 fusiona tres.

## Cautela al citar

Verificar en el PDF la afirmación sobre el número de consultas necesarias antes de usarla para defender las 10 consultas de desarrollo.

---
Leído el 11 de noviembre de 2026 con asistencia computacional. «NV» marca lo que no se vio en el texto literal del documento y debe comprobarse en el PDF antes de citarlo.
