# F04 · Bruch (2023)

**An Analysis of Fusion Functions for Hybrid Retrieval**

| Campo | Valor |
|---|---|
| Autores | Bruch, S.; Gai, S.; Ingber, A. |
| Año y sede | 2023. arXiv v2, 4 de mayo de 2023 (p. 1). La sede editorial no figura en el texto |
| Identificador | arXiv:2210.11934 |
| PDF | `pdfs/F04_bruch_2023_fusion.pdf` · https://arxiv.org/pdf/2210.11934 |
| Eje | F. Fusión tardía de scores |
| Origen del registro | búsqueda dirigida |
| Nivel de lectura | completo (texto extraído del PDF, 36 páginas; revisado el 20-11-2026). Las figuras no son legibles en el texto extraído; sí sus leyendas |

## Qué hace

- **Datos.** MS MARCO Passage v1 (8,8 M de pasajes, 6 980 consultas del conjunto dev pequeño) y ocho colecciones BEIR (tabla 1, p. 5).
- **Tarea y protocolo.** Recuperación híbrida léxica y densa; Recall@1000 y NDCG@1000 (corte 100 en SciFact y NFCorpus) (p. 6); ajuste de α en la validación de los conjuntos dentro de dominio y evaluación en la partición de prueba, dentro y fuera de dominio (p. 15).
- **Método.** Fusionan BM25 (PISA, k1 = 0,9, b = 0,4) y all-MiniLM-L6-v2 sobre la unión de los 1000 primeros candidatos; las puntuaciones faltantes se calculan antes de fusionar (pp. 4-5). Comparan la combinación convexa de scores normalizados con Reciprocal Rank Fusion (η = 60 por defecto, ec. 7, p. 15) y analizan la normalización. Adoptan la min-max «teórica» (ínfimo de la función: 0 para BM25, −1 para el coseno), llamada TM2C2, por ser más estable entre conjuntos (pp. 7 y 15). Apéndices A-D: otros pares (Splade, Tas-B).
- **Comparadores.** BM25 solo, denso solo, RRF (η = 60 y paramétrico), SRRF (RRF suavizado) y un oráculo con α por consulta (p. 15).
- **Resultados.** La combinación convexa supera a RRF dentro y fuera de dominio en NDCG en los nueve conjuntos de la tabla 2 (p. 16; MS MARCO 0,454 frente a 0,425, confirmado), con prueba t pareada bilateral, p < 0,01. RRF es sensible a sus parámetros y, ajustado dentro de dominio, generaliza mal fuera de él (tabla 3, p. 20). Las normalizaciones lineales son equivalentes en orden salvo un reajuste de pesos (lema 4.2, p. 10; teorema 4.5, p. 11). α ∈ [0,6; 0,8] mejora de forma consistente (p. 25). Con menos del 5 % de las consultas de entrenamiento α converge (fig. 12, p. 23-24, media de 5 ensayos). En los apéndices la ventaja no es universal: con Tas-B + BM25, RRF supera a M2C2 en HotpotQA y SciFact (tabla 6, p. 32); con Tas-B + MiniLM, en NQ, Quora, NFCorpus, SciFact y FiQA (tabla 8, p. 36).
- **Limitaciones declaradas.** Confirmado (p. 25): solo fusionan dos sistemas; el análisis «puede extenderse», pero piden validar si el papel de la normalización cambia con tres o más modelos y lo dejan como trabajo futuro. También que una recta puede no bastar por consulta (p. 25).
- **Código y datos.** No figura en el texto un repositorio de código; los datos son públicos (MS MARCO, BEIR, p. 5).

## Aporte a la tesis

Respalda el diseño de M4: fusión convexa de scores normalizados por consulta, con pesos ajustados en pocas consultas de desarrollo. También advierte que el análisis cubre dos componentes y M4 fusiona tres.

## Cautela al citar

La eficiencia muestral se mide en proporción del conjunto de entrenamiento («menos del 5 %», p. 23), que en MS MARCO son miles de consultas; la frase «a handful of labeled queries» (p. 2) no da un número. No sirve para defender que 10 consultas de desarrollo bastan para ajustar α; a lo sumo, para apoyar que un solo peso es más fácil de ajustar que los parámetros de RRF.

## Actualización del 20 de noviembre de 2026

- Verificado en el texto completo: cifras de la tabla 2 (p. 16), lema 4.2 y teorema 4.5 (pp. 10-11), limitación a dos sistemas (p. 25) y rango α ∈ [0,6; 0,8] (p. 25).
- Corregido: la eficiencia muestral se expresa como menos del 5 % del entrenamiento, no como «unas pocas consultas» en número absoluto; la superioridad de la combinación convexa sobre RRF no se mantiene en todos los pares de los apéndices (tablas 6 y 8).
- Afecta al diseño de M4: (a) los autores no validan la fusión de tres sistemas, por lo que el uso con BM25, OpenCLIP y el descriptor estructural es una extensión no probada; (b) recomiendan la normalización con el ínfimo teórico (0 para BM25, −1 para el coseno) por su estabilidad; conviene declarar cuál se usa; (c) calculan las puntuaciones faltantes en la unión de candidatos en lugar de dejarlas en cero; (d) RRF con k = 60 es razonable como variante sin parámetros, pero el artículo muestra que no es neutral respecto de k.
- Sigue sin verificar: la sede editorial (no figura en el texto) y el contenido de las figuras.

---
Leído el 11 de noviembre de 2026 y completado el 20 de noviembre de 2026 con asistencia computacional, sobre el texto completo extraído del PDF. «NV» marca lo que no se pudo comprobar.
