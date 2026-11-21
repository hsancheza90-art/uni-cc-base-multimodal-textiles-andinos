# F42 · Varshney et al. (2024)

**Content-based image retrieval of Indian traditional textile motifs using deep feature fusion**

| Campo | Valor |
|---|---|
| Autores | Varshney, S.; Singh, S.; Vasantha Lakshmi, C.; Patvardhan, C. (Dayalbagh Educational Institute, Agra, India) |
| Año y sede | 2024. *Scientific Reports*, 14, artículo 10035 (17 pp.). Recibido el 30-10-2023, aceptado el 6-3-2024 (p. 15). Acceso abierto, CC BY 4.0 (p. 17). |
| Identificador | https://doi.org/10.1038/s41598-024-56465-9 |
| PDF | `pdfs/41598_2024_Article_56465.pdf` |
| Eje | Recuperación de imágenes de textiles (antecedente directo) |
| Origen del registro | aportado por el investigador (20-11-2026) |
| Nivel de lectura | completo (texto extraído del PDF, 17 páginas) |

## Qué hace

- **Datos.** TIAD (*Traditional Indian Art Forms Dataset*): 22 547 imágenes JPEG de 300 × 300 píxeles de nueve estilos (Bagh, Bandhani, Batik, Chikankari, Ikat, Kalamkari, Kashida, Madhubani y Warli), ampliación de trabajos previos de los autores. Se reunieron con conocedores en ferias (Taj Mahotsav, Delhi Haat) y de sitios web comerciales y Pinterest (p. 4). Además, Corel-1K (1000 imágenes, 10 clases) y Caltech-101 (9144 imágenes, 101 clases) (p. 4).
- **Tarea y protocolo.** Recuperación por contenido (CBIR) de imagen a imagen: dada una imagen de consulta, devolver las 20 más parecidas (alcance 20) (pp. 5–7). La motivación es acelerar el diseño de nuevas telas y el comercio electrónico (pp. 1–2).
- **Método.** Rasgos de la penúltima capa de InceptionResNetV2 (1536 dimensiones) e InceptionV3 (2048) preentrenadas en ImageNet, concatenados (3584) (p. 4, p. 10); distancia Manhattan, elegida frente a Euclídea, Jeffrey y Tanimoto (p. 6); PCA a 1024 componentes en TIAD y 100 en Caltech-101 (p. 10); agrupamiento «Navrattan»: un modelo fusionado ajustado predice el estilo de la consulta y la búsqueda se limita a ese estilo (pp. 10–12); retroalimentación de relevancia de varias iteraciones (pp. 13–14); mapas de saliencia por oclusión (SBFGSM) para explicar la similitud (pp. 8–10).
- **Comparadores.** Modelos individuales (InceptionResNetV2, InceptionV3, VGG16, VGG19, Xception) (Tabla 1, p. 6) y métodos publicados sobre Corel-1K y Caltech-101, con Maji y Bose (2021) como línea base (Tabla 4, p. 9).
- **Resultados.** En TIAD, precisión media a 20 de 92,46 % y exhaustividad de 19,51 % (Tabla 3, p. 7); 92,95 % con PCA (p. 10); 95,18 % con el agrupamiento por estilo (p. 12); 99,00 % tras cuatro iteraciones de retroalimentación (Tabla 7, p. 13). En Corel-1K, 96,99 % frente a 96,11 % de la línea base; en Caltech-101, 83,24 % frente a 82,02 % (Tabla 4, p. 9). Tiempo medio de recuperación de 0,45 a 0,74 s según la variante (Tablas 5 y 6, pp. 11–12).
- **Limitaciones declaradas.** Solo como trabajo futuro: recuperar la misma imagen con otra orientación, y la posible influencia de la resolución y la calidad de imagen de cada conjunto (p. 14).
- **Código y datos.** No públicos: datos y código «a pedido razonable» al autor de correspondencia (p. 15).

## Aporte a la tesis

1. **Qué hace: CBIR de motivos textiles con rasgos profundos (pp. 1, 4).** Es un antecedente directo de recuperación por imagen en textiles tradicionales no occidentales. RESPALDA que la recuperación de textiles por contenido visual con redes preentrenadas es una línea activa, con datos propios y métricas de precisión a k.
2. **¿Usa organización estructural del diseño? NO (pp. 4, 10–12).** Solo usa rasgos visuales globales de CNN preentrenadas. No anota ni modela bandas, secuencia, simetría ni motivos como conjunto; la «estructura» que menciona es la de los vectores de rasgos (p. 2). Los autores rechazan la anotación por palabras clave por subjetiva, costosa y poco expresiva (p. 1), justo la opción que la tesis adopta y controla con un protocolo y una medida de acuerdo.
3. **Relevancia definida por estilo (deducción de la lectura, pp. 6–7).** La precisión se calcula por clase de estilo; la relevancia equivale en la práctica a pertenecer al mismo estilo. Los «expertos humanos» y los «criterios de relevancia definidos» se mencionan solo para dos o tres consultas de ejemplo, sin describirlos (pp. 7, 12). La tesis, en cambio, juzga la relevancia con una rúbrica estructural sobre pares. Por eso los porcentajes de F42 no son comparables con los de la tesis.
4. **Comparación con la tesis.** F42 sirve como contraste: corpus grande de imágenes comerciales y de ferias, de una sola fuente cultural, sin licencias por objeto ni procedencia museística (p. 4), y con evaluación por clase. La tesis trabaja con fotografías de museo con licencia abierta, pocas piezas, anotación estructural explícita y comparación de sistemas (texto, visión, visión y lenguaje, estructural). F42 es el tipo de línea base visual (M1/M2) que la tesis compara con su representación estructural.

## Citas útiles

- Las palabras clave tienen poca capacidad expresiva para los atributos de los textiles indios, y su asignación manual es subjetiva, costosa y lenta (p. 1).
- La brecha semántica entre los rasgos visuales de bajo nivel y la percepción humana de alto nivel es el obstáculo central de la recuperación por contenido (p. 2).
- TIAD reúne 22 547 imágenes de nueve estilos de textiles tradicionales indios, a 300 × 300 píxeles (p. 4).
- La fusión de rasgos de InceptionResNetV2 e InceptionV3 con distancia Manhattan alcanza 92,46 % de precisión media a 20 en TIAD (pp. 6–7).
- Restringir la búsqueda al estilo predicho para la consulta sube la precisión a 95,18 % y reduce el tiempo de respuesta (p. 12).
- Los datos y el código solo están disponibles a pedido (p. 15).

## Cautela al citar

- Hay inconsistencias numéricas internas: con alcance 20 y unas 1500 a 3200 imágenes por estilo (p. 4), una exhaustividad media de 19,51 % no es posible si todo el estilo cuenta como relevante; en un ejemplo el total de relevantes es 40 (p. 7) y en otro 60, pero se divide entre 50 (p. 7). La definición de «relevante» no queda clara (deducción de la lectura).
- El agrupamiento «Navrattan» compara la etiqueta de la consulta con la clase predicha antes de restringir la búsqueda (pp. 11–12); si se usa la etiqueta real de la consulta, hay fuga de información en la evaluación (deducción de la lectura, no declarada por los autores).
- Los mapas de saliencia (SBFGSM) se evalúan solo de forma cualitativa (p. 10).
- Las imágenes proceden de webs comerciales y Pinterest; el artículo no trata licencias ni procedencia (p. 4).
- No citar las cifras de Corel-1K y Caltech-101 como evidencia sobre textiles: son bancos de objetos generales.

---
Leído el 20 de noviembre de 2026 con asistencia computacional, sobre el texto completo extraído del PDF.
