# F10 · Helmer (2015)

**A Similarity Measure for Weaving Patterns in Textiles**

| Campo | Valor |
|---|---|
| Autores | Helmer, S.; Ngo, V. M. |
| Año y sede | 2015, SIGIR 2015 según OpenAlex y según la cita de F11 («Proceedings of the 38th SIGIR, pp. 163–172», F11 p. 172); este PDF no lo dice. El texto extraído no trae sede, año, afiliaciones, sello de arXiv ni nota de publicación previa; el 2018 sale solo del identificador arXiv:1810.04604 (depósito posterior a la publicación original). La referencia más reciente es de 2014 (refs. 1, 14 y 31, p. 10), compatible con 2015 |
| Identificador | doi:10.1145/2766462.2767735; arXiv:1810.04604 |
| PDF | `pdfs/F10_helmer_ngo_2015_similitud_tejidos.pdf` · https://arxiv.org/pdf/1810.04604 |
| Eje | B. Representación y recuperación de textiles |
| Origen del registro | OpenAlex (B2) |
| Nivel de lectura | completo (texto extraído del PDF, 10 páginas; revisado el 20-11-2026). Las fórmulas y figuras de pp. 3–9 salieron desordenadas; las cifras de las figuras 11–15 no son legibles como números |

## Qué hace

- **Datos.** 1 200 muestras modeladas a mano con el editor SAWU y divididas por un experto en 12 categorías de 100; en promedio 25 352 vértices, 6 311 cruces y 12 679 aristas (p. 7). Las categorías son ligamentos (tafetán, cinco sargas, raso), una de tejidos andinos (la más compleja, fig. 9h, p. 8), tejido triaxial, trenza, punto y «warp above weave» (pp. 7–8). Se introdujeron imperfecciones y rotaciones o reflejos en algunas muestras (p. 8). La introducción cita textiles andinos y el proyecto previo «Weaving Communities of Practice» de base de conocimiento andina (p. 1). No se usan fotografías de museo.
- **Tarea y protocolo.** Agrupamiento jerárquico aglomerativo (UPGMA) frente a las 12 categorías, medido con índice de Rand, precisión, exhaustividad y F (pp. 6–7); recuperación en la que cada textil es consulta y son relevantes los de su misma categoría, con MAP y curvas PR y FR de 11 puntos (p. 7).
- **Método.** Cada textil es un hipergrafo cuyo elemento básico es el cruce de dos hilos (definición 1, p. 3). Cada cruce recibe una k-vecindad que sigue los cuatro hilos y marca cada tramo como alterno, no alterno o terminado (definiciones 3 y 5, pp. 4–5); el textil es el multiconjunto de esas vecindades (huella), invariante a rotación y reflejo (p. 4), comparado con Jaccard, Hamming (booleana y de frecuencias) o coseno (frecuencias y TF-IDF). Cálculo en O(nk) (p. 6). **Escala:** estructura de hilos (ligamento); el texto define «estructura textil» como relaciones espaciales entre hilos (p. 2) y no menciona bandas, franjas, su orden, color ni motivos.
- **Comparadores.** Confirmado: solo las cinco variantes de distancia y distintos k entre sí; ninguna línea base externa (pp. 8–9).
- **Resultados.** MAP «de alrededor de 0,93» solo aparece en la introducción (p. 1); la figura 14 (p. 9) no es legible como cifras. Jaccard es la mejor en agrupamiento y recuperación; con k = 4 su precisión se mantiene sobre 90 % hasta cierto nivel de exhaustividad y luego cae a cerca de 75 % (p. 9); k > 4 no mejora (pp. 8–9). Hamming booleana empeora al crecer k (p. 8).
- **Limitaciones declaradas.** Confirmado el modelado manual; proponen extraer la estructura de hilos por procesamiento de imágenes y evaluar en otros conjuntos de datos (p. 10). «Necesidad de más datos» no figura como tal en el texto.
- **Código y datos.** No figura en el texto (solo la web weavingcommunities.org con ejemplos andinos, p. 8).

## Aporte a la tesis

Antecedente directo de recuperación por estructura textil, con raíz en el trabajo andino de Birkbeck. Delimita la brecha con precisión: trabajan a escala de hilos, modelan cada pieza a mano, toman la categoría como verdad y no se comparan con ningún modelo visual. La tesis trabaja con la macroestructura visible en fotografías, juicios graduados ciegos y comparación con OpenCLIP.

## Cautela al citar

Año y sede no aparecen en este PDF; se toman de OpenAlex y de la cita en F11. Citar el MAP de 0,93 como afirmación de la introducción, no como resultado tabulado.

## Actualización del 20 de noviembre de 2026

- Se confirmó la escala: cruces de hilos (ligamento), no la organización visible del diseño; no hay ninguna mención de bandas, franjas ni de su orden.
- Se precisó el papel andino: una de las 12 categorías es de tejidos andinos (p. 8), modelados a mano, no fotografías.
- Se resolvieron los «NV» de limitaciones y datos; «necesidad de más datos» no figura y se corrigió.
- La sede no figura en este PDF, pero F11 (Ngo et al. 2021) cita este trabajo como «Helmer & Ngo (2015), Proceedings of the 38th SIGIR, pp. 163–172» y se declara su extensión (F11, pp. 171–172), lo que respalda el año 2015 frente al 2018 del depósito en arXiv. F11 también da las cifras de agrupamiento de 2015 (Rand 0,938, precisión 0,577, exhaustividad 0,922, F 0,71; F11, p. 166), que este texto no da en números.
- Siguen sin verificar en este texto las cifras exactas de las figuras 11–15.

---
Leído el 11 de noviembre de 2026 y completado el 20 de noviembre de 2026 con asistencia computacional, sobre el texto completo extraído del PDF. «NV» marca lo que no se pudo comprobar.
