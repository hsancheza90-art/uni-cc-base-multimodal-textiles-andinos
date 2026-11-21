# F39 · Passonneau (2006)

**Measuring Agreement on Set-valued Items (MASI) for Semantic and Pragmatic Annotation**

| Campo | Valor |
|---|---|
| Autores | Passonneau, R. (Columbia University, Nueva York) |
| Año y sede | 2006. Actas de la *International Conference on Language Resources and Evaluation* (LREC 2006), Génova, pp. 831–836. El PDF no rotula la sede: el año y la conferencia se infieren de la autocita «Passonneau et al., 2006 … LREC, Genoa» (p. 836) y del nombre del archivo (`636_pdf`, patrón de las actas de LREC 2006); la paginación 831–836 figura al pie de cada página. |
| Identificador | Sin DOI en el PDF. URL probable de las actas: http://www.lrec-conf.org/proceedings/lrec2006/pdf/636_pdf.pdf (inferida del nombre del archivo; no figura en el texto). |
| PDF | `pdfs/636_pdf.pdf` |
| Eje | Acuerdo de anotación (campos de conjunto) |
| Origen del registro | aportado por el investigador (20-11-2026) |
| Nivel de lectura | completo (texto extraído del PDF, 6 páginas) |

## Qué hace

- **Datos.** Cinco pares de «pirámides» construidas de forma independiente por dos anotadores sobre cinco conjuntos de documentos de DUC 2003, con siete resúmenes modelo por conjunto; en promedio 725 palabras y 92 unidades de contenido (SCU) distintas por pirámide (pp. 832, 835).
- **Tarea y protocolo.** Cada anotador agrupa fragmentos de resúmenes en SCU, es decir, en clases de equivalencia; el número de clases no está fijado de antemano (pp. 832–833). Se mide acuerdo **entre** anotadores, no intra-anotador.
- **Método.** Propone MASI, una distancia entre conjuntos que se usa como función δ dentro de alfa de Krippendorff (pp. 833, 835). Definición (p. 834): MASI = J × M, donde J es Jaccard (|P ∩ Q| / |P ∪ Q|) y M es un término de monotonía: 1 si los conjuntos son idénticos, 2/3 si uno es subconjunto del otro, 1/3 si la intersección y ambas diferencias son no vacías, 0 si son disjuntos. MASI va de 1 (idénticos) a 0 (disjuntos). En alfa se usa 1 − MASI como desacuerdo (p. 835). En la anotación por clases de equivalencia se retira la propia unidad antes de comparar sus conjuntos (p. 834).
- **Comparadores.** Alfa con distancia nominal (todo conjunto no idéntico cuenta como desacuerdo total), alfa con Jaccard y alfa con MASI (Tablas 1 y 2, pp. 835).
- **Resultados.** Alfa nominal entre 0,01 y 0,24; con Jaccard entre 0,39 y 0,58; con MASI entre 0,68 y 0,80 (Tabla 2, p. 835). Con MASI el valor sube aproximadamente la mitad de la distancia entre Jaccard y 1, lo que la autora interpreta como que la mayoría de las diferencias son monótonas (subconjuntos) (p. 836). En una validación externa, las puntuaciones de 16 sistemas calculadas con pirámides de distintos anotadores se correlacionan entre 0,84 y 0,91 (p. 836).
- **Limitaciones declaradas.** Usar segmentos en lugar de palabras como unidades subestima las decisiones del anotador (p. 835). Qué acuerdo es suficiente depende del uso de los datos; no hay un umbral universal (pp. 831, 833, 836).
- **Código y datos.** No se publica código ni datos en el artículo.

## Aporte a la tesis

1. **Jaccard como una de varias distancias defendibles para conjuntos: RESPALDA, con matiz (pp. 833–836).** El artículo presenta Jaccard y Dice como medidas de asociación entre conjuntos, construye MASI sobre Jaccard (p. 833) y reporta tres distancias en paralelo porque juntas caracterizan mejor los datos: la nominal indica cuántas coincidencias exactas hay, Jaccard cuánto se solapan y MASI si el solapamiento es monótono (pp. 835–836). Matiz: Passonneau no usa el Jaccard medio en bruto como medida de acuerdo, sino como distancia dentro de alfa, que corrige por azar. El Jaccard medio de la tesis no corrige por azar; conviene decirlo al citarla.
2. **MASI como alternativa: RESPALDA (p. 834).** MASI = J × M es aplicable a cualquier campo de conjunto de etiquetas, como los motivos. Penaliza más un desacuerdo cruzado (cada anotación añade una etiqueta que la otra no tiene) que uno de inclusión (una anotación añade etiquetas a la otra).
3. **Advertencia sobre la comparación numérica (deducción de la definición, p. 834).** Como M ≤ 1, MASI es siempre menor o igual que Jaccard para el mismo par de conjuntos. Los valores más altos de la Tabla 2 se deben a que MASI entra como distancia en alfa, donde el desacuerdo esperado también se calcula con MASI. Un MASI medio en bruto de la tesis saldría por debajo de su Jaccard medio, no por encima.
4. **Casos que el artículo no trata.** No define qué pasa cuando ambos conjuntos están vacíos (por ejemplo, motivo `ausente` en las dos anotaciones); la tesis debe fijar esa convención por su cuenta. Tampoco trata el acuerdo intra-anotador: la extensión a una re-anotación de la misma persona es de la tesis.
5. **Interpretación del acuerdo.** Recuerda que Krippendorff ofreció el umbral de 0,67 en un contexto concreto y dijo que «no hay una respuesta fija» (p. 833), y propone relacionar el acuerdo con una evaluación independiente (estudio «paradigmático») (pp. 833, 836). Esto apoya presentar el acuerdo de la tesis como descriptivo y ligado al uso del corpus.

## Citas útiles

- Las anotaciones con selecciones múltiples o categorías graduadas exigen nuevas formas de medir el acuerdo (p. 831).
- MASI es una distancia para comparar dos conjuntos, parecida a Jaccard o Dice, e incorpora a Jaccard; al ser independiente del cálculo del acuerdo esperado, puede usarse en cualquier métrica ponderada, como alfa de Krippendorff (p. 833).
- MASI = J × M; M vale 1 para conjuntos idénticos, 2/3 si uno contiene al otro, 1/3 si se solapan sin inclusión y 0 si son disjuntos (p. 834).
- Aplicar una métrica no ponderada a anotaciones de conjuntos muy parecidas pero rara vez idénticas da valores engañosamente bajos (p. 833).
- Con alfa nominal, Jaccard y MASI, los cinco pares de pirámides dan 0,01–0,24, 0,39–0,58 y 0,68–0,80, respectivamente (p. 835).
- Usar varias métricas con relaciones conocidas caracteriza mejor un conjunto de datos que una sola (p. 836).
- Lo que es suficientemente fiable para una tarea puede no serlo para otra (p. 836).

## Cautela al citar

- No presentar los valores de alfa con MASI como comparables con un Jaccard medio sin corregir por azar.
- El dominio es la anotación lingüística (resúmenes y correferencia), con dos anotadores; la transferencia a etiquetas de motivos y a un solo anotador es una decisión de la tesis.
- La sección 3.2 no aparece en el texto (se pasa de 3.1 a 3.3); no se perdió contenido en la extracción, es la numeración del original.
- La sede y la URL no figuran en el PDF; verificarlas antes de la referencia definitiva.

---
Leído el 20 de noviembre de 2026 con asistencia computacional, sobre el texto completo extraído del PDF.
