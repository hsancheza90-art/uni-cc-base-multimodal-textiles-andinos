# F34 · Parry (2025)

**Variations in Relevance Judgments and the Shelf Life of Test Collections**

| Campo | Valor |
|---|---|
| Autores | Parry, A.; Fröbe, M.; Scells, H.; Schlatt, F.; Faggioli, G.; Zerhoudi, S.; MacAvaney, S.; Yang, E. |
| Año y sede | 2025. Proceedings of the 48th International ACM SIGIR Conference on Research and Development in Information Retrieval (SIGIR '25), 13-18 de julio de 2025, Padua; ACM, 11 páginas (p. 1). Artículo de reproducibilidad (p. 1) |
| Identificador | doi:10.1145/3726302.3730308 · arXiv:2502.20937v2 (21 de mayo de 2025) |
| PDF | `pdfs/2502.20937v2.pdf` |
| Eje | Evaluación de recuperación (variación entre evaluadores y estabilidad del orden de sistemas) |
| Origen del registro | aportado por el investigador (20-11-2026) |
| Nivel de lectura | completo (texto extraído del PDF, 11 páginas). Las figuras 1-5 solo se leen por sus leyendas y el texto que las comenta |

## Qué hace

- **Datos.** Colección TREC Deep Learning 2019, tarea de pasajes (MS MARCO, unos 8,8 millones de pasajes; 43 temas) con relevancia graduada 0-3 (pp. 3-4). Los juicios oficiales se tratan como los del evaluador «primario»; ocho académicos, coautores del trabajo, actúan como evaluadores «secundarios», dos por tema, en cuatro grupos (p. 3 y nota 3). El pool secundario incluye todo lo juzgado con grado ≥ 1 más 100 no relevantes muestreados por evaluador; carga media de 1125 pares por evaluador (p. 4).
- **Tarea y protocolo.** Reproducir el estudio de Voorhees (2000) en una colección moderna: temas sin descripción ni narrativa, documentos cortos, cuatro grados y sistemas neuronales (p. 1). Los evaluadores recibieron la guía original de grados, sabían que los pares ya estaban juzgados pero no vieron los grados; para familiarizarse con los temas solo podían usar el buscador ChatNoir (p. 4). Estudio piloto previo con 10 temas al azar (p. 5). Además, se fijaron narrativas en tres temas de acuerdo bajo, mediano y alto para aislar el efecto de la intención (pp. 4 y 7).
- **Método.** Acuerdo con solapamiento, kappa de Cohen (4 grados y binario) y kappa de Fleiss (p. 5). Medida de sistemas: nDCG@10. Estabilidad del orden con tau de Kendall, rho de Spearman y RBO entre el orden oficial y el obtenido con combinaciones de evaluadores; probabilidad de intercambio de cada par de sistemas sobre 10 000 combinaciones de juicios (pp. 3, 5 y 8, fig. 3). Diferencias de efectividad con t pareada y corrección de Bonferroni; cambios de rango con Wilcoxon (p. 5). Los evaluadores también se tratan como «ejecuciones» para estimar un techo humano (pp. 4 y 8-9).
- **Comparadores.** 75 sistemas del pool original de DL'19 (léxicos, neuronales y con modelos de lenguaje) y sistemas modernos: ColBERT, SPLADE ED++, monoT5, monoELECTRA, Set-Encoder, RankZephyr y RankGPT con GPT-4, GPT-4 Turbo y GPT-4o (pp. 4-5, cuadro 2).
- **Resultados.** El acuerdo es bajo: kappa de Cohen de 0,11 a 0,19 con 4 grados entre primario y secundarios, y de 0,28 a 0,31 en binario; entre secundarios, de 0,19 a 0,27 y de 0,34 a 0,47 (cuadro 4, p. 5); el kappa de Fleiss con 4 grados indica un acuerdo «casi aleatorio» (p. 5). Aun así, el orden de sistemas se mantiene: tau 0,879 (combinaciones) y 0,897 (en muestra), rho 0,972 y 0,977, RBO 0,888 y 0,902 (cuadro 5, p. 7). Con los juicios nuevos, los valores absolutos de nDCG@10 bajan (p. 7). El orden no es del todo estable: los sistemas basados en LLM o destilados de ellos son atípicos; las ejecuciones con GPT-4o sobre BM25 bajan de rango de forma significativa (p. 7). Fijar la narrativa mejora el acuerdo, pero los autores concluyen que el mayor factor de desacuerdo es la ambigüedad de la consulta (p. 7). Techo humano realista de nDCG@10 ≈ 0,81 en DL'19 (pp. 2 y 9, cuadro 6).
- **Limitaciones declaradas.** La re-anotación es «increíblemente costosa» (p. 9). Los evaluadores son coautores, lo que reconocen como solapamiento (p. 3, nota 3). Los evaluadores de fuera de EE. UU. tuvieron dificultades con temas centrados en ese país; el sesgo por nacionalidad queda para trabajo futuro (p. 5). No se juzgó todo el pool (p. 4).
- **Código y datos.** github.com/Parry-Parry/sigir25-annotation, con código y juicios (p. 2, nota 2).

## Aporte a la tesis

- **¿La variación entre evaluadores cambia el orden de los sistemas?** **Respalda, con matices.** Con kappa bajo, el orden global se conserva (tau ≈ 0,88-0,90; cuadro 5, p. 7; conclusión, p. 9). Pero el texto matiza: pares con diferencias grandes de nDCG también se intercambian con frecuencia (fig. 3, p. 7), los sistemas basados en LLM o destilados cambian de rango (p. 7) y el nDCG absoluto baja con otros evaluadores (p. 7). Para la tesis, la estabilidad se midió con 43 temas y unos 75 sistemas mediante tau. Con 4-5 sistemas (M0-M4) y un solo evaluador, el resultado no se transfiere directamente. Respalda que la tesis informe diferencias relativas entre sistemas y no valores absolutos de nDCG@10 como verdad. También respalda tratar con cautela un sistema neuronal como M2 (OpenCLIP), porque los sistemas neuronales grandes fueron los menos estables (p. 7).
- **Doble juicio parcial en 5 consultas.** Lo respalda de forma indirecta. El estudio usa dos evaluadores secundarios y un piloto de 10 temas (pp. 3 y 5); el doble juicio permite estimar el acuerdo, pero el texto muestra que un kappa bajo no implica un orden inestable.
- **LLM como evaluadores.** **No lo trata.** En el artículo, los LLM son sistemas de ranking (RankGPT, RankZephyr) y maestros de destilación (pp. 2 y 5), no evaluadores. Solo menciona de pasada que, en la anotación con «sistemas generativos» en el bucle, la interpretación de la narrativa puede tener implicaciones de control (p. 7), y deja como trabajo futuro sacar conclusiones sin un esfuerzo humano extenso (p. 9). Cita a Soboroff (2024), «Don't Use LLMs to Make Relevance Judgments» [42], pero solo para apoyar afirmaciones sobre desacuerdo entre evaluadores y tamaño del pool de evaluadores (pp. 1 y 4), no para discutir juicios automáticos. Para la segunda opinión del modelo de visión y lenguaje en la tesis, este texto no aporta respaldo ni objeción; hay que remitir a F16.

## Citas útiles

- Aunque el acuerdo entre evaluadores es bajo, el orden de los sistemas en DL'19 se correlaciona mucho con el de los juicios originales, incluso con relevancia de cuatro grados (p. 7).
- Con relevancia graduada, todos los valores de acuerdo bajan respecto de estudios anteriores; con cuatro grados, el kappa de Fleiss indica un acuerdo cercano al azar y mejora unos 10 puntos al binarizar (p. 5).
- Los sistemas basados en LLM o destilados de ellos son los que más varían de rango al cambiar de evaluadores (p. 7).
- El mayor factor de desacuerdo parece ser la ambigüedad del lenguaje natural de la consulta, más allá de la narrativa que se aplique (p. 7).
- Fijar una narrativa común mejora el kappa de Cohen entre grupos de evaluadores en las consultas difíciles (p. 7).
- Puntuaciones de sistemas por encima del acuerdo humano (nDCG@10 ≈ 0,81 en DL'19) pueden indicar sobreajuste a los juicios y no un sistema mejor (pp. 2 y 9).
- Un solo evaluador por tema es la práctica habitual, reduce costes y se ha validado con estudios de acuerdo (p. 2).

## Cautela al citar

El resultado de estabilidad usa tau sobre decenas de sistemas y 43 temas; no habla de pruebas de significación entre dos sistemas con 10 o 30 consultas. Los evaluadores son académicos de RI y coautores, el material es texto y la relevancia es graduada 0-3; la tesis juzga imágenes de textiles con un evaluador. No atribuir al artículo ninguna postura sobre LLM como evaluadores: no la tiene. El techo de 0,81 es propio de DL'19 y no se generaliza.

---
Leído el 20 de noviembre de 2026 con asistencia computacional, sobre el texto completo extraído del PDF.
