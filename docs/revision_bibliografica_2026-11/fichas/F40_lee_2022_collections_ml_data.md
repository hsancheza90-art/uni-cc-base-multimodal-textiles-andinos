# F40 · Lee (2022)

**The "Collections as ML Data" Checklist for Machine Learning & Cultural Heritage**

| Campo | Valor |
|---|---|
| Autores | Lee, B. C. G. (University of Washington) |
| Año y sede | 2022. Preprint en arXiv (cs.LG), versión 1 del 6 de julio de 2022; 32 páginas. Existe una versión de revista (*Journal of the Association for Information Science and Technology*, 2025) que **no se leyó**; esta ficha describe solo el preprint. |
| Identificador | arXiv:2207.02960v1 |
| PDF | `pdfs/2207.02960v1.pdf` |
| Eje | Documentación del corpus y ética del patrimonio cultural |
| Origen del registro | aportado por el investigador (20-11-2026) |
| Nivel de lectura | completo (texto extraído del PDF, 32 páginas: 20 de cuerpo, apéndice con el checklist en pp. 21–25, notas y referencias) |

## Qué hace

- **Datos.** No hay datos experimentales. El insumo es una revisión de guías de aprendizaje automático (agrupadas en cuatro tipos: evaluaciones de conjuntos de datos, de modelos, de impacto algorítmico, y herramientas y enfoques éticos, pp. 7–9) y de informes del sector patrimonial (Cordell, Padilla, LC Labs, Europeana) (pp. 5–6).
- **Tarea y protocolo.** Redactar un checklist para quien ejecuta un proyecto concreto de aprendizaje automático con colecciones patrimoniales, no para la institución (p. 5). Se probó con cinco casos elegidos por diversidad de institución, medio, tema, método, disciplina, público y entregable: The Real Face of White Australia, Citizen DJ, Distant Viewing, Transkribus y Newspaper Navigator, este último del propio autor (pp. 9–11, Tabla 1).
- **Método.** Revisión de literatura, traducción de recomendaciones a preguntas, refinamiento iterativo con los casos (viñetas) y comentarios de colegas y de un curso de posgrado de ética computacional (pp. 6–7).
- **Comparadores.** No hay comparación cuantitativa. Se sitúa frente a Datasheets for Datasets, Data Statements, Dataset Nutrition Label, Data Cards, Model Cards y las «25 preguntas» de Cordell, la única lista previa para practicantes del sector (pp. 5, 8).
- **Resultados.** Un checklist en cuatro componentes (pp. 11–12; texto completo en pp. 21–25): (1) la colección como datos: composición, proceso de colección y razones de curaduría, cadena de digitalización, procedencia, trabajo de colaboración abierta y modificaciones adicionales; (2) el modelo: descripción, entrenamiento, evaluación, despliegue, publicación e impacto ambiental; (3) consideraciones organizacionales: partes interesadas, necesidad de usar aprendizaje automático, contexto organizacional y lanzamiento; (4) derechos de autor, transparencia y reutilización, documentación, privacidad y mantenimiento.
- **Limitaciones declaradas.** La taxonomía de guías no es exhaustiva y se limita sobre todo a publicaciones académicas (p. 7). La selección de casos «representativos» es subjetiva (p. 10). El checklist no es exhaustivo; usarlo no exime de examinar ni documentar más el proyecto (p. 20).
- **Código y datos.** No aplica.

## Aporte a la tesis

1. **Preguntas aplicables a un corpus de museo para aprendizaje automático: RESPALDA (pp. 21–25).** Aplican directamente:
   - *Procedencia y curaduría:* quién curó la colección y para qué institución; qué proceso de colección se usó y cuándo; cuáles fueron los procesos de decisión detrás de la curaduría; qué se desconoce de ese proceso (1.2, pp. 21–22); cuál es la procedencia desde la colección hasta la digitalización y si una parte es desconocida (1.4, p. 22).
   - *Digitalización:* quién eligió qué digitalizar, con qué criterios y pasos, y qué metadatos se produjeron por algoritmo (1.3, p. 22).
   - *Modificaciones propias:* si se quitaron elementos o se añadieron metadatos para formar el conjunto (1.6, p. 22). Cubre los descartes y la anotación estructural de la tesis.
   - *Licencias:* si los derechos de autor afectan al conjunto (1.1.g, p. 21) y al modelo, el código y los entregables, y qué licencias se eligieron (sección 4.1, p. 25).
   - *Historia difícil y comunidades:* si el conjunto se relaciona con una historia difícil y qué precauciones se toman (1.1.h, p. 21); si se notificó y consultó a los grupos representados en el conjunto y si estos tienen una vía de contacto y reparación (3.1.d–e, p. 24). Es la base para tratar el contexto funerario y las comunidades de origen.
   - *Modelo preentrenado:* si se usó un modelo preentrenado y dónde está su información; si los metadatos generados por el modelo, como los embeddings, son entregables; impacto ambiental (2.2, 2.4, 2.6, pp. 23–24). Aplica a M2 (OpenCLIP).
   - *Necesidad del aprendizaje automático:* si era necesario y qué críticas caben (3.2, p. 24).
   - *Reproducibilidad y mantenimiento:* si un investigador externo puede reproducir el proyecto con la documentación disponible, y quién lo mantendrá (4.3.c y 4.5, p. 25).
2. **Sesgos de colección: MATIZA (pp. 14, 23).** El checklist no tiene una pregunta titulada «sesgo de colección». El tema entra por las razones de curaduría: entender esas decisiones es esencial para contextualizar «las abundancias y las lagunas» de representación del corpus (p. 14), y por la cadena de digitalización, que puede distorsionar lo que el modelo ve (p. 14). La auditoría de equidad y sesgo se pide solo «si el modelo involucra datos de personas» (3.c, p. 23). La tesis debe formular por su cuenta el sesgo de colección (qué culturas, épocas y tipos de pieza llegaron a cada museo y cuáles fotografió).
3. **Publicar el checklist con los entregables: RESPALDA (pp. 2, 3–4, 5, 19, 20).** El autor propone que el checklist completo «puede publicarse» con los entregables para dar al público y a los auditores una descripción estructurada de las consideraciones y limitaciones del proyecto (pp. 2, 3–4, 20), y recomienda llenarlo en el diseño, antes y después del lanzamiento (p. 20). Matiz: lo plantea como posibilidad recomendada («can be published»), no como obligación.
4. **Relación con la ficha tipo Datasheets (F25).** El checklist declara inspirarse en Datasheets (pp. 8, 14) y añade lo que una ficha de conjunto de datos genérica no pregunta: curaduría, digitalización, procedencia y trabajo voluntario (p. 15). Sirve para revisar si la ficha del corpus cubre esos puntos.

## Citas útiles

- Hay pocas guías pensadas para el practicante que inicia un proyecto de aprendizaje automático con patrimonio cultural; el checklist se propone cubrir ese vacío (p. 2).
- Aun con buenas intenciones, estos proyectos arriesgan explotar a las personas representadas, pasar por alto sutilezas de la digitalización que afectan al modelo y empezar sin planes de sostenibilidad (p. 3).
- Entender las decisiones de curaduría es esencial para contextualizar las abundancias y las lagunas de representación de un corpus (p. 14).
- La cadena de digitalización puede afectar profundamente las predicciones de un modelo; documentarla es crucial (p. 14).
- La procedencia compleja de una colección debe considerarse al evaluar su contorno digital (p. 15).
- Pregunta: ¿era necesario usar aprendizaje automático en este proyecto y qué críticas caben? (p. 24).
- El checklist completado puede publicarse con los entregables para aumentar la transparencia y comunicar decisiones y limitaciones (p. 20).

## Cautela al citar

- Citar como preprint de 2022 (arXiv v1). La versión de JASIST 2025 puede diferir en preguntas y numeración; no se leyó.
- Es una propuesta conceptual validada con cinco casos y comentarios de colegas, sin evaluación empírica de su efecto.
- La numeración del apéndice tiene inconsistencias: en la sección 4, «Privacidad» figura como 4 y «Mantenimiento» como 5, al revés que en el esquema de la p. 12; y 4.1.a remite a la pregunta 1.1.c sobre derechos de autor, que en realidad es la 1.1.g (p. 25). Al citar una pregunta, indicar su texto y su página.
- Los casos tratan sobre todo bibliotecas y archivos (prensa, audio, documentos, televisión); ninguno es una colección de textiles ni de museo de arte.

---
Leído el 20 de noviembre de 2026 con asistencia computacional, sobre el texto completo extraído del PDF.
