# F12 · Dorozynski (2022)

**Deep Descriptor Learning with Auxiliary Classification Loss for Retrieving Images of Silk Fabrics in the Context of Preserving European Silk Heritage**

| Campo | Valor |
|---|---|
| Autores | Dorozynski, M.; Rottensteiner, F. |
| Año y sede | 2022. ISPRS International Journal of Geo-Information 11(2), 82 |
| Identificador | doi:10.3390/ijgi11020082 |
| PDF | `pdfs/F12_dorozynski_2022_descriptores_seda.pdf` · https://www.mdpi.com/2220-9964/11/2/82/pdf |
| Eje | B. Representación y recuperación de textiles |
| Origen del registro | OpenAlex (B1) |
| Nivel de lectura | parcial: primeros ~40 000 caracteres literales; el resto, resumen automático |

## Qué hace

- **Datos.** Imágenes de tejidos de seda con registros SILKNOW anotados en varias variables (lugar, época, etc.). Tamaño no visto.
- **Tarea y protocolo.** Recuperación de imágenes; la evaluación se hace por clasificación kNN de las variables anotadas.
- **Método.** Aprendizaje de descriptores con una pérdida de tripletas de similitud gradual y una pérdida auxiliar de clasificación. La similitud entre dos piezas se define por cuántas variables anotadas coinciden.
- **Comparadores.** El mismo modelo sin la pérdida auxiliar y el trabajo previo de los autores.
- **Resultados.** La pérdida auxiliar mejora 2,7 puntos de exactitud y 5,6 de F1 (resumen). No se vio ninguna métrica de ranking.
- **Limitaciones declaradas.** No vistos.
- **Código y datos.** No visto.

## Aporte a la tesis

Muestra la alternativa que la tesis evita: derivar la relevancia de los metadatos. Aquí dos sedas son parecidas si comparten lugar o época, no porque alguien las juzgue parecidas. Es el argumento para sostener qrels humanos e independientes (ANN02) y para explicar por qué las fichas de museo no bastan como verdad de referencia estructural. Aporta además la idea de similitud gradual, compatible con la escala 0–3.

## Cautela al citar

Evaluación indirecta por clasificación: no es comparable con nDCG.

---
Leído el 11 de noviembre de 2026 con asistencia computacional. «NV» marca lo que no se vio en el texto literal del documento y debe comprobarse en el PDF antes de citarlo.
