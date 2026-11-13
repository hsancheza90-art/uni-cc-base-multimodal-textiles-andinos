# F08 · Abercrombie (2025)

**Consistency is Key: Disentangling Label Variation in Natural Language Processing with Intra-Annotator Agreement**

| Campo | Valor |
|---|---|
| Autores | Abercrombie, G.; Dinkar, T.; Cercas Curry, A.; Rieser, V.; Hovy, D. |
| Año y sede | 2025. 4th Workshop on Perspectivist Approaches to NLP (NLPerspectives 2025), pp. 63–74 |
| Identificador | doi:10.18653/v1/2025.nlperspectives-1.6 |
| PDF | `pdfs/F08_abercrombie_2025_intra_anotador.pdf` · https://aclanthology.org/2025.nlperspectives-1.6.pdf |
| Eje | H. Fiabilidad de la anotación |
| Origen del registro | OpenAlex (I1) |
| Nivel de lectura | completo en el cuerpo; apéndices A y C no leídos literalmente |

## Qué hace

- **Datos.** Revisión sistemática de la ACL Anthology (56 artículos que informan acuerdo intra-anotador, menos del 0,07 % de más de 80 000) y un experimento con cuatro conjuntos en inglés, 50 ítems de alto desacuerdo cada uno y 16 anotadores.
- **Tarea y protocolo.** Si el acuerdo intra-anotador (estabilidad en el tiempo) aporta algo que el acuerdo entre anotadores no da.
- **Método.** Proponen una matriz que cruza fiabilidad (entre anotadores) y estabilidad (intra-anotador). Reanotación a las dos semanas.
- **Comparadores.** Acuerdo entre anotadores sobre los mismos ítems.
- **Resultados.** Estabilidad 74,2 % frente a fiabilidad 66,7 % (tabla 3); por anotador entre 67,5 % y 81,5 %. Los anotadores fueron inconsistentes cerca de una de cada cuatro veces. Los intervalos usados en trabajos previos van de minutos a un año. El kappa intra-anotador del apéndice: NV.
- **Limitaciones declaradas.** Pequeña escala; la calidad de los anotadores de plataforma puede explicar parte de la inconsistencia; los ítems se eligieron por su alto desacuerdo.
- **Código y datos.** github.com/HWU-NLP/consistency

## Aporte a la tesis

Convierte una debilidad en práctica defendible: la reanotación ciega del lote 1 mide algo que casi nadie informa. Da vocabulario (estabilidad frente a fiabilidad), sitúa el intervalo de 7 días dentro del rango de la literatura y ofrece una cifra de referencia: incluso con dos semanas, un cuarto de las etiquetas cambia.

## Cautela al citar

Es anotación de texto por anotadores de plataforma, no de imágenes por un especialista. La cifra orienta, no fija un umbral.

---
Leído el 11 de noviembre de 2026 con asistencia computacional. «NV» marca lo que no se vio en el texto literal del documento y debe comprobarse en el PDF antes de citarlo.
