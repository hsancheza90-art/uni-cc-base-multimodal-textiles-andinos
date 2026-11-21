# F35 · Sakai (2022)

**Relevance Assessments for Web Search Evaluation: Should We Randomise or Prioritise the Pooled Documents? (CORRECTED VERSION)**

| Campo | Valor |
|---|---|
| Autores | Sakai, T.; Tao, S.; Zeng, Z. (Waseda University) |
| Año y sede | 2022. Versión corregida publicada en arXiv (2 de noviembre de 2022), 30 páginas. Es la versión corregida del artículo de acceso abierto de ACM Transactions on Information Systems (TOIS) 40(4), artículo 76 (2022), que tenía un error grave explicado en un corrigendum (p. 1, nota 1; ref. [36], p. 30) |
| Identificador | arXiv:2211.00981v1. El DOI de TOIS no figura en el texto (la cabecera trae un DOI genérico `10.1145/nnnnnnn.nnnnnnn`, p. 1) |
| PDF | `pdfs/2211.00981v1.pdf` |
| Eje | Evaluación de recuperación (construcción de juicios de relevancia) |
| Origen del registro | aportado por el investigador (20-11-2026) |
| Nivel de lectura | completo (texto extraído del PDF, 30 páginas). Las figuras 4-7 se leen por sus leyendas y el texto que las comenta |

## Qué hace

- **Datos.** Conjunto WWW3E8: 160 temas de la subtarea en inglés de NTCIR-15 WWW-3 (corpus clueweb12-B13), pools de profundidad 15 a partir de 37 ejecuciones de 9 equipos; 32 375 pares tema-documento, cada uno con 8 etiquetas independientes (4 con orden aleatorio y 4 con orden priorizado): 259 000 etiquetas (pp. 1, 6-7). Unos 202 documentos por tema (p. 7).
- **Tarea y protocolo.** Comparar dos formas de ordenar los documentos del pool para el evaluador: RND (orden aleatorio, la recomendación de TREC) y PRI (priorizado por NTCIRPOOL: primero los documentos que más ejecuciones devuelven y en mejor posición) (p. 2). 24 estudiantes de informática en tres grupos de ocho; los temas y el tipo de pool se asignaron al azar, de modo que cada evaluador pasó por ambas condiciones. Los evaluadores no sabían que se comparaban dos órdenes (pp. 7-8). Escala: muy relevante, relevante, no relevante y error, convertida a 2/1/0 (p. 8).
- **Método.** Cuatro preguntas: eficiencia (RQ1, registros de actividad, Tukey HSD pareada), acuerdo entre evaluadores (RQ2, alfa de Krippendorff ordinal y kappa ponderado cuadrático), acuerdo entre órdenes de sistemas (RQ3, tau de Kendall con nDCG, Q, nERR e iRBU a profundidad 10) y robustez ante sistemas nuevos (RQ4, dejar fuera un equipo) (pp. 3, 10-19). Experimentos adicionales con pools equivalentes a profundidad 5 y con ejecuciones peores (pp. 22-23).
- **Comparadores.** RND frente a PRI; cuatro versiones de juicios de cada uno.
- **Resultados.** (a) Sin diferencia sustancial en el tiempo por documento; PRI puede ayudar a encontrar antes el primer documento muy relevante (pp. 11-12). (b) Acuerdo: alfa global 0,425 (todos), 0,433 (RND) y 0,423 (PRI) (cuadro 4, p. 13); alfa medio por tema 0,293 (RND) frente a 0,279 (PRI), t = 0,949, p = 0,344, Δ de Glass = 0,0859; harían falta 1098 temas para un 70 % de potencia; concluyen que el efecto del orden sobre el acuerdo es «despreciable» (cuadro 5 y p. 13). (c) Los órdenes de sistemas dentro de PRI se parecen algo más entre sí que dentro de RND, sin importancia práctica; pero un orden RND y uno PRI pueden diferir bastante: PRI lleva al evaluador a favorecer documentos «populares», devueltos arriba por muchos sistemas (pp. 14-17). En PRI se acumulan más etiquetas de relevante en las primeras posiciones mostradas; una explicación posible es que el evaluador sobrevalora lo que ve primero (p. 16). (d) Los juicios PRI son algo más robustos ante sistemas que no aportaron al pool (pp. 17-19).
- **Limitaciones declaradas.** Los evaluadores son estudiantes (evaluadores «bronce»), no autores de los temas; anuncian un estudio con evaluadores «oro» en NTCIR-16 WWW-4 (pp. 8-9 y 28). La fatiga queda fuera del alcance porque cada evaluador organizó su trabajo durante dos meses (p. 5). Los experimentos adicionales son «algo artificiales» (p. 22).
- **Código y datos.** WWW3E8 corregido en https://waseda.box.com/WWW3E8corrected (p. 3, nota 7); temas en https://waseda.box.com/www2www3topics-E (p. 7, nota 12).

## Aporte a la tesis

- **Orden aleatorio frente a priorizado y acuerdo entre evaluadores.** **Respalda** la decisión de presentar los candidatos en orden aleatorio, **con un matiz**. El orden no cambia de forma apreciable el acuerdo (RQ2, cuadros 4-5, p. 13; conclusión, p. 28), así que aleatorizar no tiene coste en fiabilidad. Además, el orden priorizado empuja al evaluador hacia los documentos que muchos sistemas ponen arriba (pp. 16-17 y 28). En la tesis, el pool reúne los 10 primeros de cada sistema; priorizar por coincidencia entre sistemas favorecería justo lo que M0-M3 comparten y sesgaría la comparación entre ellos. El matiz: los autores no recomiendan con fuerza ninguna de las dos estrategias y señalan que PRI da colecciones algo más reutilizables (p. 28). Esa ventaja importa poco en la tesis, que no busca reutilizar los juicios con sistemas nuevos, salvo M4 si no entra en el pool (inferencia propia). La escala tampoco es comparable: 24 evaluadores, unos 202 documentos de texto web por tema y acuerdo entre personas distintas. En la tesis hay un evaluador, imágenes, pools pequeños y solo un doble juicio parcial.
- **Damessie et al. (2018), según este texto.** Compararon tres órdenes: la priorización de NTCIRPOOL, el orden aleatorio y un método propio por bloques, con documentos probablemente no relevantes seguidos de uno pseudorrelevante. Sus resultados sugerían que la priorización logra **más acuerdo** que el orden aleatorio. Sakai et al. advierten que ese estudio usó solo 240 pares tema-documento (8 temas: 4 de TREC-7 y 4 de TREC-8, con 30 documentos cada uno) y no midió la eficiencia (pp. 5-6). También atribuyen a Damessie et al. la observación de que ordenar por identificador de documento puede agrupar por fuente cuando el identificador lleva un prefijo; por eso Damessie et al. pasaron de ordenar por identificador a aleatorizar (pp. 2 y 6). Referencia: CIKM 2018, pp. 723-732 (ref. [10], p. 29). Con 259 000 etiquetas, el estudio de Sakai et al. no reproduce esa ventaja de acuerdo (p. 13).
- **Relación con la tesis.** La observación sobre los prefijos aplica directamente: los identificadores `MET:`, `CMA:` y `AIC:` agruparían por museo si se ordenara por identificador. El orden aleatorio lo evita (inferencia propia a partir de p. 2).

## Citas útiles

- La práctica temprana de TREC ordenaba el pool por identificador de documento para que el evaluador no supiera cuántos sistemas, ni cuáles, habían recuperado cada documento (p. 2).
- La diferencia de acuerdo entre evaluadores con orden aleatorio y con orden priorizado probablemente no tiene importancia práctica (pp. 3, 13 y 28).
- El orden priorizado tiende a que el evaluador favorezca documentos «populares», devueltos arriba por muchos sistemas (pp. 17 y 28).
- El orden de presentación sí afecta a qué documentos se juzgan relevantes y, en cierta medida, al orden de los sistemas (p. 28).
- Eisenberg y Barry (1988) observaron un efecto de «cobertura»: los evaluadores evitan poner notas extremas a los primeros documentos y recomendaron aleatorizar el orden de presentación (p. 4).
- Huang y Wang (2004) no observaron efectos de orden con 5 ni con 75 documentos y atribuyeron lo segundo posiblemente a la fatiga (p. 5).
- Los juicios con orden priorizado resultan algo más robustos para evaluar sistemas que no aportaron al pool (pp. 19 y 28).

## Cautela al citar

Citar la versión corregida de arXiv: la de TOIS tenía un error grave y sus cifras no son válidas; también están afectados los resultados del piloto de Sakai y Xiao (2019) (pp. 1 y 6). El acuerdo se mide entre evaluadores distintos (alfa de Krippendorff); el texto no habla de acuerdo intra-evaluador. El resultado sobre Damessie et al. viene de este texto, no de la lectura del original. La escala de relevancia tiene tres grados más «error»; los resultados son de búsqueda web en texto.

---
Leído el 20 de noviembre de 2026 con asistencia computacional, sobre el texto completo extraído del PDF.
