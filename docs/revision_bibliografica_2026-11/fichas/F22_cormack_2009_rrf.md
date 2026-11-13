# F22 · Cormack (2009)

**Reciprocal Rank Fusion outperforms Condorcet and individual Rank Learning Methods**

| Campo | Valor |
|---|---|
| Autores | Cormack, G. V.; Clarke, C. L. A.; Büttcher, S. |
| Año y sede | 2009. SIGIR 2009 |
| Identificador | sin DOI |
| PDF | `pdfs/F22_cormack_2009_rrf.pdf` · https://cormack.uwaterloo.ca/cormacksigir09-rrf.pdf |
| Eje | F. Fusión tardía de scores |
| Origen del registro | búsqueda dirigida |
| Nivel de lectura | completo |

## Qué hace

- **Datos.** Ejecuciones de TREC (Robust 2004, TREC 3, 5 y 9) y LETOR 3.
- **Tarea y protocolo.** Si una fusión sin entrenamiento supera a los sistemas individuales y a otros métodos de fusión.
- **Método.** RRF(d) = suma sobre los rankings de 1 / (k + posición de d), con k = 60 fijado en un piloto; el resultado es estable para k entre 10 y 100.
- **Comparadores.** Mejor sistema individual, Condorcet Fuse, CombMNZ y métodos de aprendizaje de rankings.
- **Resultados.** MAP (tabla 2), RRF frente al mejor individual: Robust 0,3686 frente a 0,3586; TREC 5 0,3394 frente a 0,3165. CombMNZ gana en TREC 3. En LETOR 3, RRF 0,6051 y CombMNZ 0,6107, diferencia no significativa.
- **Limitaciones declaradas.** Ninguno declarado; informan solo MAP.
- **Código y datos.** No visto.

## Aporte a la tesis

Ofrece un comparador de fusión sin parámetros. Una variante de M4 con RRF no necesita ajustar pesos, así que no puede sobreajustarse a las 10 consultas de desarrollo. Si M4 con pesos y M4 con RRF coinciden, el resultado no depende del ajuste; si difieren, se sabe cuánto aporta el ajuste. Tendría que declararse en el protocolo antes del test, como ablación.

## Cautela al citar

RRF usa posiciones y descarta la magnitud del score, de modo que no sirve para H3: la descomposición exacta solo vale para la fusión de scores.

---
Leído el 11 de noviembre de 2026 con asistencia computacional. «NV» marca lo que no se vio en el texto literal del documento y debe comprobarse en el PDF antes de citarlo.
