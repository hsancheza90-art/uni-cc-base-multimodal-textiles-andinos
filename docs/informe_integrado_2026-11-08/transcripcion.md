# Revisión de avance proyecto de tesis: informe integrado (transcripción)

Transcripción literal de `Revision_de_avance_proyecto_de_tesis_Informe_integrado.docx` (SHA-256 `28ed3894c0bbf3ffcd65aad13f6b40b4635bb136a1c25b2272efbe0bc186ee53`), informe del asesor fechado el 8 de noviembre de 2026. Se ofrece para leer el informe en el repositorio; el documento de referencia es el `.docx`, versionado sin cambios. Solo se añadió el formato Markdown: títulos, negritas en las etiquetas «Resultado que debe entregar», «Condición…», «Dictamen…» y en el nombre de cada etapa, y saltos de párrafo.

Referencia: tesis «Estructuras combinatorias y representación multimodal en textiles andinos», auditoría del 20 de octubre de 2026, documento «Revisión de avance proyecto de tesis» y «Plan de cierre de Seminario de Tesis II». Estado de referencia: repositorio main, commit c313224 del 6 de noviembre de 2026. Informe integrado al 8 de noviembre de 2026.

Este informe consolida las indicaciones de ambos documentos y se dirige exclusivamente al estudiante de posgrado. No constituye una nueva auditoría. Indica lo que debe completar para cerrar el experimento y presentar un trabajo de maestría metodológicamente defendible. Los estados proceden de los informes y archivos citados en los documentos de origen; las pruebas informadas por el investigador no se han vuelto a ejecutar para preparar este texto.

## 1. Estado real del proyecto y trabajo que no debe repetirse

El corpus v2.0 reúne 615 registros utilizables de MET, CMA y AIC: 462 en el conjunto principal y 153 complementarios. Hay 259 descartados, por lo que existen 874 decisiones curatoriales registradas. Los registros utilizables están organizados en 577 grupos de piezas relacionadas. La galería experimental procede de un núcleo de 150 piezas anotadas, pertenecientes a 146 grupos. El corpus v2.0 se encuentra etiquetado como corpus-met-cma-aic-v2.0; el corpus histórico MET+CMA v1.2 permanece congelado.

El estudiante dispone de M0 (BM25), M1 (color CIELAB y textura LBP), M2 (OpenCLIP), M3 (descriptor estructural) y un control M3-sin-orden. M0, M1 y M2 ya producen rankings de desarrollo. M3 y su control están especificados, implementados y probados, pero aún deben producir sus rankings sobre la anotación definitiva. M4, la fusión de texto, visión y estructura, está pendiente. Las particiones por grupos, las diez consultas T3 de desarrollo, las treinta de prueba y seis consultas exploratorias de texto a imagen ya están preparadas.

El flujo reproducible cuenta con 23 etapas y 350 pruebas automáticas reportadas. La matriz de respuesta declara atendidos DAT01, DAT02, MAT01, SW01, SW02, SW04, SW05, SW08 y APT01. Esto representa un avance de ingeniería verificable en el repositorio, pero no equivale a haber probado la hipótesis científica. Al último corte documentado, los 345 pares del pool de desarrollo tenían cero juicios, la reanotación ciega registraba cero de treinta piezas y no había métricas finales de recuperación.

El estudiante no debe reabrir la recolección de imágenes, alterar corpus ya congelados ni introducir otro museo solo para aumentar volumen. Tampoco debe repetir la auditoría general. La prioridad inmediata es completar la evidencia de evaluación sobre los materiales existentes.

**Resultado que debe entregar:** Un inventario breve de versiones, grupos, modelos implementados, consultas y pendientes, referenciado a archivos y commits. No debe describir como "validado científicamente" lo que solo cuenta con pruebas de software.

## 2. Pregunta científica, contribución y alcance de las conclusiones

a) Redactar una pregunta contrastable: determinar si incorporar el orden visible de las bandas y relaciones entre regiones, mediante un descriptor estructural, aporta utilidad a la recuperación de textiles andinos frente a señales textuales y visuales generales.

b) Conservar tres hipótesis vinculadas a resultados observables. H1: M4 obtiene mejor nDCG@10 que M2 (OpenCLIP) en T3. H2: M3 con orden mejora a M3-sin-orden. H3: el score final se reconstruye exactamente a partir de sus componentes y responde a intervenciones de acuerdo con la fórmula implementada. No confundir fidelidad matemática con interpretación cultural o causal.

c) Definir la contribución en términos de método y evidencia, no de cantidad de tecnologías: formalización de una macroestructura observable, descriptor que considera secuencias, adyacencias y ausencias de observabilidad, y evaluación controlada de su utilidad en un corpus museográfico.

d) Delimitar población y comparabilidad. M3 utiliza etiquetas asignadas por una persona, mientras M2 opera sobre fotografías. Una eventual mejora de M4 respaldaría la utilidad de conocimiento estructural asistido por anotación, no una extracción automática superior ni una generalización a todos los textiles andinos.

e) Revisar la coherencia entre pregunta, objetivos, hipótesis, variables, comparadores, código y capítulos de tesis. Si la evidencia es negativa o inconclusa, conservar la pregunta y comunicar el resultado sin reformular retrospectivamente el objetivo.

**Resultado que debe entregar:** Apartado definitivo de problema, objetivos, hipótesis y alcance, con una relación explícita entre cada hipótesis y su prueba.

## 3. Protocolo experimental que debe cerrar antes de la prueba (prioridad indispensable)

a) Completar docs/protocolo_experimental_v2.md, actualmente versión 0.5 propuesta. Presentarlo para aprobación metodológica y registrar fecha, versión, decisión y commit. Las decisiones todavía propuestas, relativas al uso exploratorio de aptitud, galería, umbral práctico y reglas de verificación, deben quedar resueltas por escrito antes del test.

b) Mantener T3, recuperación por ejemplar estructural, como tarea primaria. T1, texto a imagen, permanece exploratoria. Mantener M0, M1, M2, M3, M3-sin-orden y M4 como sistemas comparables según el protocolo, sin atribuir capacidad textual a M1 ni extracción automática de estructura a M3.

c) Fijar nDCG@10 como métrica primaria, umbral práctico de Δ = 0,03, intervalo de confianza del 95 % por bootstrap pareado de consultas, análisis de sensibilidad por permutación y reglas claras para consultas sin relevantes o para pares no evaluables. Las restantes comparaciones deben marcarse exploratorias cuando corresponda.

d) Preservar la partición por grupos y las consultas fijadas antes de examinar resultados: 10 de desarrollo y 30 de prueba en T3, si la carga humana permite mantenerlas. La galería es compartida, por lo que debe describirse el diseño como recuperación transductiva. Nunca ajustar pesos ni elegir variantes con relevancias de prueba.

e) Registrar antes del test cualquier modificación imprescindible al protocolo, con motivo, fecha y efecto sobre la comparabilidad. Una reducción de consultas o del pool, si fuera necesaria por tiempo, debe definirse prospectivamente y no tras observar si el sistema gana.

f) Incluir condiciones expresas que detengan la prueba: grupos relacionados cruzados entre particiones, autocandidatos, fotografías con hash no verificado, qrels derivados de modelos o anotaciones, parámetros ajustados en prueba y ausencia de un manifiesto de ejecución reproducible.

**Resultado que debe entregar:** Protocolo definitivo y aprobado, configuración config/experimento.toml coherente, registro de decisiones y prohibiciones previas al test.

## 4. Estabilidad de la anotación y congelación estructural v2.1 (prioridad indispensable)

a) Reanotar a ciegas el primer lote de 30 piezas en data/metadata/anotacion_v2_reanotacion.xlsx, con un orden distinto y sin consultar las primeras respuestas. Respetar el intervalo mínimo de siete días desde la anotación original del 5 de noviembre, es decir, a partir del 12 de noviembre de 2026. Registrar fechas y conservar la guía vigente durante ambas pasadas.

b) Ejecutar src.anotacion.acuerdo y registrar kappa por atributo cuando sea estimable, medidas multietiqueta, similitud de edición de la palabra de bandas, tamaño efectivo y exclusiones. Informar los atributos con estabilidad baja o no estimable. Llamarlo acuerdo intra-anotador, no acuerdo entre expertos.

c) Revisar los 38 avisos por valores "desconocido" no marcados para revisión, las tres correcciones que repiten valores y las observaciones de dudas, criterios o vocabulario indicadas en más de cien piezas. Clasificar los hallazgos y resolver las ambigüedades con criterios escritos; conservar un registro de adjudicaciones.

d) Una vez cerrada la comparación ciega, decidir si hay atributos demasiado ambiguos para sostener la hipótesis. Documentar cualquier cambio y su consecuencia para M3 antes de congelar la anotación. No retocar a mano las etiquetas según la conveniencia de un ranking.

e) Congelar las 150 anotaciones efectivas con la guía y el vocabulario finales como versión estructural v2.1; guardar manifiesto, checksums y trazabilidad. No confundir esta versión con el corpus consolidado v2.0, que no contiene la anotación estructural.

**Resultado que debe entregar:** Reanotación completa, informe de estabilidad con n y métricas, decisión sobre avisos y criterios, y versión v2.1 inmutable para el experimento.

## 5. Modelos M0-M4, control sin orden y ajuste de desarrollo (prioridad indispensable)

a) Conservar los baselines existentes y sus condiciones de ejecución. M0 utiliza texto de fichas sin la descripción plantilla de MET; M1 emplea histogramas de color y textura sobre la superficie textil; M2 emplea OpenCLIP congelado con un checkpoint y hash identificables. Registrar normalización, encuadre, parámetros, versiones y manejo de empates.

b) Generar los rankings de M3 sobre la anotación v2.1. Implementar fielmente la composición, palabra de bandas canónica por reversión, adyacencias, atributos estructurales, máscaras de observabilidad y disimilitud mixta ya especificadas. Cuando no exista evidencia estructural comparable, el sistema no debe asignar similitud perfecta.

c) Generar M3-sin-orden en las mismas consultas y sobre los mismos candidatos. Sustituir la secuencia por un histograma de tipos de banda y excluir adyacencias, manteniendo la regla prevista de pesos. Esta comparación debe aislar el aporte del orden y no introducir simultáneamente otra modificación.

d) Implementar M4 como fusión tardía de M0, M2 y M3 con scores normalizados por consulta, pesos no negativos elegidos solo en desarrollo y regla fijada para redistribuir peso cuando M3 no tiene evidencia. Registrar componentes y contribuciones para reconstruir cada score.

e) Terminar primero los juicios de desarrollo necesarios y usarlos para ajustar los pesos de M4 y los parámetros autorizados. Guardar la rejilla probada, la regla de selección y el valor definitivo. No abrir resultados de prueba para corregir un peso o sustituir el checkpoint.

f) Ampliar las pruebas de tests/test_sistemas.py y tests/test_modelos.py: invariancia a reversión, simetría y cota cuando corresponda, coherencia de máscaras, diferencia entre palabras con el mismo histograma y distinto orden, reconstrucción numérica y determinismo de rankings.

**Resultado que debe entregar:** Implementaciones finales de M3, M3-sin-orden y M4, rankings completos de desarrollo, tests de propiedades, configuración y parámetros definitivamente seleccionados.

## 6. Juicios humanos de relevancia y control de sesgos (prioridad indispensable)

a) Completar los 345 pares iniciales de desarrollo en data/metadata/juicios_desarrollo_v2.xlsx, que proceden de M0, M1, M2 y candidatos aleatorios. Aplicar la escala 0-3, indicar "no_evaluable" cuando corresponda, y registrar evaluador, fecha y justificación visible para relevancias 2 o 3. Los juicios se basan en las imágenes y criterios estructurales, no en las puntuaciones de los modelos.

b) Cuando se generen rankings de desarrollo de M3, M3-sin-orden y M4, incorporar a la unión de pools sus candidatos nuevos sin duplicar pares ni sobrescribir juicios anteriores. Conservar el origen de los candidatos en un archivo separado, fuera de la vista de quien juzga.

c) Mantener el juicio ciego: consulta y candidato en orden aleatorizado, sin revelar sistema que propuso el par, posición, score ni anotación estructural utilizada por M3. No producir etiquetas automáticamente desde CLIP, desde la fórmula de M3 o desde el propio protocolo.

d) Después de congelar los modelos, construir el pool ciego de las 30 consultas de prueba. Sus rankings se pueden calcular exclusivamente para componer el pool sin evaluar ni inspeccionar métricas; la evaluación confirmatoria de desempeño solo se realizará cuando los juicios hayan quedado fijados. Conservar originales, fecha y procedencia humana.

e) Si se obtiene un segundo juicio ciego parcial, organizar y registrar los pares de esa muestra, las dos respuestas y el acuerdo antes de adjudicar. Si no se dispone de otra persona, declarar explícitamente el uso de un evaluador único y no presentar los qrels como una verdad independiente de toda subjetividad.

f) Medir cobertura del top 10 juzgado por cada sistema, número de pares no evaluables y consultas sin candidatos relevantes. Explicar la convención para candidatos no juzgados, que no constituye evidencia de irrelevancia, y reportar una comprobación de sensibilidad cuando proceda.

**Resultado que debe entregar:** Qrels de desarrollo y prueba validados, procedencia humana, cobertura por sistema, distribución de grados, casos no evaluables y registro de cegamiento.

## 7. Congelación del experimento y ejecución confirmatoria (prioridad indispensable)

a) Preparar un manifiesto de ejecución con commit, etiqueta del corpus v2.0, anotación v2.1, grupos, particiones, consultas, hashes de fotografías, dependencia OpenCLIP y checkpoint, pesos finales, semillas, entorno Python y hardware. La información debe permitir reconstruir el experimento exacto.

b) Antes de revelar los resultados, comprobar automáticamente IDs únicos, unicidad y exclusión de grupos, ausencia de consultas autocandidatas, hashes correctos y coincidencia entre protocolo y configuración. Detener el procedimiento si se incumple una condición de integridad o congelación.

c) Sellar los modelos y los qrels después de completar el juicio ciego. No modificar a partir de ese punto el código de puntuación, las relevancias, el diseño, el vocabulario, los pesos o las plantillas por el signo de los resultados.

d) Ejecutar la evaluación confirmatoria una sola vez conforme al protocolo y calcular métricas por consulta y por sistema. Guardar rankings, qrels y todos los parámetros. Una detección posterior de error genuino exige registro transparente, análisis de impacto y nueva versión si fuera necesario, nunca selección interesada del resultado.

**Resultado que debe entregar:** Manifiesto de congelación, comprobaciones previas aprobadas y resultados de prueba por consulta sin reajustes posteriores.

## 8. Resultados estadísticos, ablaciones e interpretación (prioridad indispensable)

a) Para H1, informar nDCG@10 de M4 y de M2 por cada consulta T3, diferencia pareada media, intervalo de confianza al 95 % por bootstrap pareado de 10 000 réplicas y análisis de sensibilidad por permutación. Distinguir dirección favorable, magnitud práctica igual o superior a 0,03 y evidencia compatible o no con una diferencia positiva.

b) Para H2, comparar M3 y M3-sin-orden en las mismas consultas y qrels. Aislar el efecto del orden, ilustrar ejemplos donde adyacencias y secuencias cambian el ranking y reconocer una hipótesis no sostenida si el efecto es ausente o incierto.

c) Para H3, registrar las contribuciones de M0, M2 y M3 al score de M4; verificar la reconstrucción dentro de la tolerancia declarada, y evaluar intervenciones o supresión de componentes siguiendo exactamente la fórmula y su redistribución de pesos. Aclarar que esto prueba fidelidad de la explicación algorítmica.

d) Presentar las ablaciones predefinidas: M4 sin estructura, sin texto y con M3-sin-orden; separar bandas frente a motivos y relaciones dentro de M3 cuando el diseño lo permita. Añadir el control negativo con descriptores estructurales permutados por museo para comprobar si desaparece el efecto de la señal estructural.

e) Reportar métricas secundarias autorizadas (por ejemplo, P@10 y MRR), número efectivo de consultas, amplitud de intervalos, cobertura de juicios, análisis descriptivo por museo y por fragmento o pieza completa. Con solo 30 consultas de prueba no atribuir significación concluyente a mejoras pequeñas o inestables.

f) Analizar aciertos y errores con criterios de selección explícitos; incluir casos que favorecen a M2, que favorecen a M4 y que muestran fallos de ambos. Estimar o medir el esfuerzo humano de la anotación estructural para que la comparación de recursos sea transparente.

**Resultado que debe entregar:** Tablas H1-H3, intervalos, análisis de potencia y sensibilidad, ablaciones, control negativo, ejemplos de error y conclusiones compatibles con la incertidumbre observada.

## 9. Formalización matemática y relación con la implementación (prioridad académica)

a) Corregir el capítulo matemático para que la pieza, registro, fotografía, grupo, anotación, palabra de bandas, alfabeto, adyacencias, equivalencia por reversión y máscara tengan una definición inequívoca y una correspondencia con datos concretos.

b) Separar restricciones de elegibilidad o calidad de fotografía de las propiedades estructurales. No presuponer que toda pieza presenta bandas, motivos o simetría observables, ni mezclar espacios de embeddings sin una alineación definida.

c) Presentar y verificar las propiedades realmente utilizadas: canonización bajo reversión, comparabilidad mediante máscara, rango y simetría de la disimilitud, tratamiento de datos faltantes y costo computacional. No afirmar desigualdad triangular si no se ha demostrado bajo máscaras variables.

d) Usar Burnside y Pólya como antecedentes matemáticos pertinentes, no como prueba automática de originalidad o rendimiento. Distinguir teoremas conocidos, decisiones de diseño del descriptor, propiedades verificadas por tests y resultados empíricos de recuperación.

**Resultado que debe entregar:** Capítulo matemático corregido, notación consistente y correspondencia explícita entre fórmulas, código y atributos observables.

## 10. Revisión bibliográfica y brecha de investigación (prioridad académica)

a) Tomar la revisión preparada en octubre como mapeo parcial, no como PRISMA exhaustivo. Esa auditoría documentó 64 registros importados, 63 cribados y cuatro estudios examinados sustantivamente en métodos y resultados. Los datos no deben presentarse como una revisión sistemática completa.

b) Extender, con el acceso realmente disponible, búsquedas documentadas en Scopus, Web of Science, IEEE Xplore, ACM Digital Library y fuentes pertinentes. Conservar cadenas, fecha, filtros, exportaciones, eliminación de duplicados y razones de inclusión o exclusión. Si alguna base no se puede consultar, anotarlo y no simular cobertura.

c) Leer y comparar críticamente los antecedentes cercanos: recuperación multimodal patrimonial, trabajos sobre textiles andinos, estructuras combinatorias, secuencias y grafos, codificadores visuales, explicabilidad y validación de etiquetas humanas. Priorizar los textos cruciales que la auditoría dejó pendientes, incluidos Brownlow et al. y Ngo et al.

d) Construir una matriz que explicite para cada estudio sus datos, tarea, método, comparadores, métrica, acceso a código, hallazgos y límites. Identificar con precisión la diferencia entre macroestructura visual anotada, estructura a nivel de hilos y clasificación cultural.

e) Integrar la bibliografía a la discusión de resultados, verificando DOI, versiones, referencias y citas textuales. Evitar afirmar que no existen antecedentes a partir de una búsqueda incompleta; formular la brecha como hipótesis y comparación específica que la tesis sí pone a prueba.

**Resultado que debe entregar:** Estado del arte crítico y trazable, protocolo y exportaciones de búsqueda, matriz de antecedentes y referencias bibliográficas comprobadas.

## 11. Redacción del informe de maestría a partir de evidencia real (prioridad académica)

a) Revisar introducción, problema, objetivos, hipótesis y contribución conforme al protocolo finalmente ejecutado. Aclarar el ámbito de investigación en imágenes museográficas y la diferencia entre artefacto técnico y demostración científica.

b) Describir corpus y unidades sin confundir 874 decisiones curatoriales, 615 registros utilizables, 577 grupos y 150 piezas del núcleo experimental. Aclarar en las tablas si se cuentan registros, imágenes, piezas u objetos y explicar sesgos de selección por museo.

c) Documentar todas las decisiones necesarias para reproducir el método: fuentes, licencias, curación, anotación, estabilidad, agrupación, particiones, consultas, criterio de relevancia, M0-M4, M3-sin-orden, pesos, hashes y evaluación única.

d) Ordenar resultados: cobertura del corpus, estabilidad, baselines, H1 y H2, fidelidad de H3, ablaciones, robustez y errores. Toda cifra debe proceder de una tabla, script o artefacto rastreable. No completar tablas con resultados simulados.

e) Discutir las amenazas a la validez: mismo investigador como anotador y evaluador principal, pool incompleto, número de consultas, potencia limitada, diferencias fotográficas entre museos, costo humano y dependencia de M3 respecto de etiquetas manuales.

f) Cerrar cada objetivo con una respuesta verificable. Para cada hipótesis distinguir "sostenida", "no sostenida" o "evidencia insuficiente", indicando magnitud del efecto y alcance. No es requisito que M4 supere a OpenCLIP para obtener una contribución defendible.

**Resultado que debe entregar:** Documento de Seminario de Tesis II o manuscrito de maestría coherente, con resultados y discusión sustentados en datos reales, conclusiones por objetivo y anexos metodológicos útiles.

## 12. Reproducibilidad, paquete de entrega y mejoras que deben diferirse

a) Verificar el repositorio en un clon o entorno limpio: instalar dependencias, ejecutar python -m src.flujo y pytest, comparar salidas con las versionadas y conservar logs y estado del árbol. La cifra previa de 350 tests no reemplaza la ejecución final sobre el commit de entrega.

b) Guardar y entregar código de evaluación, consultas, qrels, rankings, métricas por consulta, intervalos, semillas, configuración, hashes y manifiesto. Documentar las imágenes que no están versionadas y el procedimiento lícito para obtenerlas o las limitaciones de acceso.

c) Vincular cada tabla de la tesis con un archivo generado y cada sistema reportado con su implementación. Documentar entorno, dependencias opcionales, licencia, uso ético y tiempos/costos medidos cuando se disponga de ellos. Una reproducción independiente es deseable cuando resulte posible.

d) Conservar sin reabrir los contratos de software ya atendidos y el corpus v1.2. Diferir al periodo posterior al experimento los trabajos SW03, SW06, SW07, SW09, SW11 y SW12, además de validación externa de aptitud, cuarto museo, SigLIP, DINO, GNN, ajuste fino e interfaz web, salvo que aparezca un defecto reproducible que invalide el test.

e) Evitar que la mejora continua del software desplace el objetivo académico. Un proyecto de maestría concluye al contestar su pregunta con pruebas suficientes, incertidumbre explícita, límites reconocidos y una entrega recuperable.

**Resultado que debe entregar:** Etiqueta o commit final, instrucciones de reproducción paso a paso, resultados verificables, informe de ejecución y correspondencia íntegra entre manuscrito y repositorio.

## 13. Orden de trabajo, condiciones de avance y criterio de finalización

**Primera etapa.** Cerrar y versionar el protocolo, documentar sus decisiones y completar ahora los 345 juicios de desarrollo disponibles. La revisión bibliográfica puede avanzar en paralelo, sin retrasar los juicios. No consultar resultados de prueba.

**Segunda etapa.** Desde el 12 de noviembre, completar la reanotación ciega de 30 piezas, calcular estabilidad, resolver los criterios pendientes y congelar la anotación v2.1. Si aparecen desacuerdos importantes, documentarlos y resolver su tratamiento antes de producir rankings estructurales definitivos.

**Tercera etapa.** Generar rankings de M3 y M3-sin-orden, implementar M4, ampliar el pool de desarrollo con los candidatos nuevos, terminar los juicios añadidos y seleccionar pesos solo con desarrollo. Registrar la potencia estimada y congelar sistemas, modelos y manifiesto.

**Cuarta etapa.** Preparar el pool de prueba sin revelar resultados, completar los juicios ciegos, comprobar cobertura y realizar las verificaciones de integridad. Si faltan qrels, anotación estable, parámetros sellados o controles de fuga, no ejecutar la evaluación confirmatoria por cumplir una fecha.

**Quinta etapa.** Ejecutar una sola evaluación de prueba, contrastar H1-H3, calcular intervalos, ablaciones y control negativo, estudiar errores y cerrar el capítulo de resultados. Completar la bibliografía, corregir el capítulo matemático y redactar discusión y conclusiones sin afirmar más de lo que sustentan los datos.

**Sexta etapa.** Verificar un clon limpio, conservar archivos de entrada y salida identificables, cerrar la entrega del repositorio y preparar el manuscrito final. El calendario del plan previo proponía completar este proceso hasta el 22 de noviembre de 2026, pero esas fechas son objetivos condicionados a los juicios y a la estabilidad de las anotaciones, no plazos que justifiquen debilitar el diseño.

**Condición mínima antes del test:** protocolo aprobado y fechado, 150 anotaciones congeladas con su informe de estabilidad, qrels de desarrollo usados solo para ajuste, M0-M4 y control sin orden fijados, grupos e imágenes verificados por hash y pool ciego de prueba completo.

**Condición de término académico:** resultados por consulta y por hipótesis con incertidumbre, comparadores y ablaciones reproducibles, explicación fiel de las contribuciones de score, límites sobre una sola persona anotadora/evaluadora y sobre la galería de 150 piezas, bibliografía contrastada y manuscrito cuyos resultados pueden comprobarse en el repositorio.

**Dictamen de seguimiento:** el estudiante debe continuar y finalizar el proyecto existente; no es necesaria otra auditoría integral ni abrir un proyecto nuevo. El pendiente central no es producir más infraestructura, sino obtener, analizar y comunicar evidencia científica válida.
