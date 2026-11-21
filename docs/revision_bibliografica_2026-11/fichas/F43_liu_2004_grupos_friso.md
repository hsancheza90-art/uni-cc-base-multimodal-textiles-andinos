# F43 · Liu, Collins y Tsin (2004)

**A Computational Model for Periodic Pattern Perception Based on Frieze and Wallpaper Groups**

| Campo | Valor |
|---|---|
| Autores | Liu, Y.; Collins, R. T.; Tsin, Y. (Robotics Institute, Carnegie Mellon University) |
| Año y sede | 2004. *IEEE Transactions on Pattern Analysis and Machine Intelligence*, 26(3), 354–371 (marzo de 2004). Recibido el 25-6-2002, revisado el 15-7-2003, aceptado el 8-8-2003 (p. 354). |
| Identificador | El DOI no figura en el texto extraído. DOI que corresponde a este artículo según conocimiento previo, por verificar: 10.1109/TPAMI.2004.1262332. Número de registro IEEECS 116853 (p. 354). |
| PDF | `pdfs/a-computational-model-for-periodic-pattern-perception-based-4uj7cxl1yy.pdf` |
| Eje | Simetría y estructura de patrones (alternativa automática) |
| Origen del registro | aportado por el investigador (20-11-2026) |
| Nivel de lectura | completo (texto extraído del PDF, 18 páginas = pp. 354–371). Se cita la paginación de la revista. Las tablas 1 a 3 y la tabla de puntuaciones de la alfombra no se extrajeron como texto. |

## Qué hace

- **Datos.** Ejemplos, no un banco de evaluación: un friso dibujado a mano, patrones sintéticos de los 17 grupos del plano tomados de un sitio web, fotografías del entorno (alfombras, rejas metálicas, panal, ventanas, pisos y muros de baldosas, superficies cromadas, una tela) y patrones espacio-temporales de la marcha humana y de un perro, incluidos 25 sujetos de la base CMU MoBo (pp. 358–365).
- **Tarea y protocolo.** Dada una imagen dominada por un patrón periódico, (1) recuperar la red de traslación, (2) clasificar su grupo de simetría y (3) extraer un motivo representativo (p. 354). No aborda la detección automática del patrón periódico dentro de una imagen mayor (p. 354).
- **Método.**
  - *Red:* picos de la autocorrelación ordenados por «región de dominancia» (distancia al pico más alto más cercano) en lugar de por altura, y transformada de Hough para hallar los dos vectores de traslación más cortos, con ángulo entre 60° y 90° (pp. 355–356).
  - *Clasificación:* se recorta y alinea cada celda, se calcula una celda mediana y un modelo de ruido, y se prueba cada rotación (180°, 120°, 90°, 60°) y reflexión (sobre lados y diagonales de la celda) con un error residual normalizado y recortado, comparado con una prueba χ² (dmed/N′ < 1); luego se distingue reflexión de reflexión con deslizamiento. La combinación de respuestas sí/no identifica uno de los 7 grupos de friso (Tabla 1) o de los 17 del plano (Tabla 2) (pp. 357–358).
  - *Patrones casi periódicos:* distancia de simetría a la «celda perfecta» de cada grupo y selección de modelo con AIC geométrico, para no favorecer siempre el grupo más general en la jerarquía de subgrupos (pp. 360–363).
  - *Motivo:* centrar la celda en el centro de rotación de mayor orden, enumerando los centros de órbitas distintas (pp. 366–367).
- **Comparadores.** Detección de la red frente al método de umbral libre de Lin et al. (1997), solo de forma cualitativa (Figs. 1 y 2, p. 355). No hay comparación cuantitativa de la clasificación de grupos.
- **Resultados.** Clasificación correcta de los 17 grupos en los patrones sintéticos del sitio de referencia (p. 359); grupos asignados a cada fotografía real (por ejemplo, cmm para una alfombra oriental dañada, pmm para tela y alfombra con ligera distorsión afín) (pp. 359–363). En la marcha de 25 sujetos de perfil: 16 en F3, 7 en F7 y 2 en F5 (p. 365). En un trabajo relacionado, tasas de clasificación de la marcha de 81 % a 100 % (p. 366).
- **Limitaciones declaradas.** Mide la simetría solo con la intensidad de los píxeles y supone ruido gaussiano en la intensidad; las distorsiones geométricas no se modelan, solo se mitigan con la tasa de recorte (p. 368). La correlación necesita una buena distribución de colores o grises; falla, por ejemplo, con muros de ladrillo (p. 368). Se restringe a transformaciones euclídeas escaladas: la cámara debe estar perpendicular a la superficie (p. 368). Los métodos de autocorrelación suponen que un único patrón periódico ocupa gran parte de la imagen (p. 355). En imágenes reales las puntuaciones de simetrías presentes y ausentes quedan cerca del umbral (p. 360). Cuál de los motivos candidatos prefiere la percepción humana es un problema abierto (p. 369).
- **Código y datos.** No se menciona la publicación del código.

## Aporte a la tesis

1. **Existe detección automática de los 7 grupos de friso y los 17 del plano a partir de imágenes: RESPALDA (pp. 354, 357–359).** Es la alternativa automática que la tesis debe mencionar frente a su anotación manual de la simetría. Los autores afirman ser los primeros en ofrecer un enfoque computacional para analizar la estructura de grupo de simetría en imágenes (p. 354).
2. **Supuestos: RESPALDA, con detalle (pp. 354–358, 368).**
   - Imagen dominada por un patrón periódico, ya segmentado; el método no lo localiza (pp. 354–355, 358).
   - Red de traslación recuperable con varias repeticiones; la autocorrelación funciona incluso con dos o tres ciclos (p. 355).
   - Un patrón periódico requiere una traslación no trivial; quedan excluidos los patrones de franjas idénticas a lo largo de la dirección de traslación (p. 357).
   - Simetría definida por igualdad de gris o color en cada píxel (p. 357); el resumen habla de patrones «monocromos» para los grupos de friso (p. 354).
   - Vista frontal sin perspectiva y ruido gaussiano de intensidad (p. 368).
3. **Patrones casi periódicos o ruidosos: MATIZA (pp. 358, 360–363, 368, 370).** El artículo no se limita a patrones perfectos: tolera ruido moderado con la celda mediana y la tasa de recorte (p. 358), clasifica una alfombra dañada (pp. 359–360) y propone el AIC geométrico para patrones casi periódicos (pp. 360–363). Pero reconoce que en imágenes reales las decisiones quedan cerca del umbral (p. 360), que la distorsión geométrica no se modela (p. 368) y que los patrones muy distorsionados pueden no corresponder a ningún conjunto válido de simetrías (p. 370). No hay una evaluación cuantitativa de la exactitud sobre un conjunto de fotografías reales.
4. **Por qué no encaja con fotografías de textiles fragmentados: base parcial en el texto; el resto es inferencia.**
   - *Con base en el texto:* exige que el patrón periódico domine la imagen y no lo localiza (pp. 354–355); exige vista perpendicular y no modela pliegues ni deformaciones (p. 368); depende de la intensidad y del color exacto (pp. 357, 368).
   - *Inferencia de la tesis, no del artículo:* un fragmento con lagunas, bordes rotos, pocas repeticiones, hilos desvanecidos o arrugas rompe la red de traslación y el modelo de ruido; una pieza en bandas con motivos distintos en cada banda no es un único patrón periódico, por lo que el método se aplicaría banda por banda tras segmentarla, y no a la pieza completa; las bandas lisas no tienen una traslación no trivial en su dirección; y la simetría por igualdad exacta de color no recoge el intercambio de colores habitual en los textiles andinos. Ninguna de estas afirmaciones se prueba en el artículo, que no trata textiles andinos.
5. **Encaje con la decisión de la tesis.** La tesis anota la simetría como atributo nominal observado y no como grupo cristalográfico calculado; F43 permite justificar esa elección por los supuestos que exige la vía automática, y señalarla como trabajo futuro (por ejemplo, sobre bandas segmentadas y fotografías frontales).

## Citas útiles

- En el plano, siete grupos de friso describen los patrones que se repiten en una dirección y 17 grupos del plano los que se repiten en dos direcciones independientes (p. 354).
- El modelo encuentra la red subyacente, identifica el grupo de simetría y extrae motivos representativos; se extiende a patrones casi periódicos con AIC geométrico (p. 354).
- No abordan la detección automática de un patrón periódico dentro de una imagen mayor (p. 354).
- La autocorrelación supone que un único patrón periódico ocupa gran parte de la imagen (p. 355).
- La clasificación del plano requiere verificar solo cuatro rotaciones y cuatro reflexiones (p. 358).
- En patrones reales, las puntuaciones de simetrías presentes y ausentes pueden quedar cerca del umbral por el ruido (p. 360).
- Limitaciones: solo intensidad, ruido gaussiano, sin modelar distorsiones geométricas y con cámara perpendicular a la superficie (p. 368).
- Washburn y Crowe ilustraron la mayoría de los 17 grupos en textiles y cerámica africanos, y distintas culturas prefieren distintos subconjuntos de grupos (p. 370).

## Cautela al citar

- Las pruebas son ejemplos ilustrativos más un caso de 25 sujetos de marcha; no hay exactitud medida sobre un conjunto de fotografías de textiles.
- Los «textiles» aparecen solo como ejemplos de patrones periódicos (alfombras, una tela); el artículo no trata textiles arqueológicos ni andinos.
- Es de 2004; hay trabajos posteriores de los mismos autores y de otros sobre texturas casi regulares que esta ficha no cubre.
- El DOI no figura en el texto extraído; verificarlo antes de la referencia definitiva.
- Las tablas de simetrías por grupo (Tablas 1 y 2) no se extrajeron como texto; consultarlas en el PDF si se reproducen.

---
Leído el 20 de noviembre de 2026 con asistencia computacional, sobre el texto completo extraído del PDF.
