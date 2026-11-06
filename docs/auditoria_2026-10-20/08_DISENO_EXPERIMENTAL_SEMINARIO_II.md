### Diseño experimental ejecutable de Seminario II
Estado: protocolo propuesto; modelos, qrels y métricas centrales todavía NOT_RUN. H1/H2/H3 en este informe significan horizontes de trabajo, distintos de las hipótesis numeradas del capítulo5.

#### Alcance mínimo y decisiones previas
H1: recuperar objetos similares por macroestructura visible mediante M0-M4 congelados, con juicios independientes. Empezar por un benchmark manejable de 120-180 grupos de objetos seleccionados de manera estratificada entre fuentes, conservación y estructura, sin elegir por éxito del modelo. Si capacidad de anotación permite cubrir los462 principales, ampliar antes de cerrar test; no después de ver resultados.

Población de inferencia: colección digital elegible, no todos los textiles andinos. Índice de texto y fotografías preservan fuente y licencia. Objetos secundarios pueden formar una extensión de robustez separada. No incorporar descartados por falta de pertinencia como negativos fáciles de la evaluación primaria.

#### Modelos comparables

| Modelo | Entrada y score | Ajuste permitido | Papel y costo |
|---|---|---|---|
| M0 | BM25 sobre título, descripción real, material/técnica; contexto en variante separada | k1/b fijados o seleccionados en desarrollo | Baseline textual CPU; documentar idioma/tokenización |
| M1 | Histogramas HSV o Lab, LBP/HOG y proporciones de regiones; distancia normalizada por bloque | Resolución y pesos en desarrollo | Visión convencional CPU; sin etiquetas expertas |
| M2 | CLIP/OpenCLIP congelado, checkpoint exacto, embeddings L2 y coseno | Plantillas/recorte solo en desarrollo | Baseline visual y texto-imagen; inferencia por lotes |
| M3 | Descriptor de bandas, relaciones y motivos de informe05 | Vocabulario/pesos en desarrollo | Asistido por anotaciones; comparar además atributos sin orden |
| M4 | Fusión tardía M0/M2/M3, contexto opcional | Pesos en rejilla pequeña sobre desarrollo | Aporte marginal estructura; explicar score por componentes |

Primero M4=visión/texto+estructura con pocos pesos. Evitar entrenar desde cero o fine-tuning de un VLM con esta muestra. Elegir checkpoint con licencia y disponibilidad verificadas al implementar; no hay hardware del usuario verificado. La extracción de cientos de embeddings es viable por lotes incluso en CPU con mayor tiempo; no se promete duración sin medir. Registrar latencia, memoria pico y costo de anotación.

SigLIP2 congelado es alternativa H2 pertinente si consultas españolas perjudican CLIP. DINOv2/DINOv3 ofrecen control visual adicional, no sustituyen el encoder textual. Fusión aprendida y re-ranking solo si desarrollo permite estimar parámetros sin sobreajuste. Grafo WL antes que GNN; LLM generativo no es necesario para explicar una suma de scores.

#### Tareas y modalidades

| Tarea | Consulta | Relevancia | Comparación |
|---|---|---|---|
| T1 texto→imagen | Descripción nueva redactada por experto, sin copiar ficha | Coincidencia semántica/visual graduada | M0 vs M2 vs M4; M3 si consulta tiene estructura explícita |
| T2 imagen→imagen | Foto de consulta de objeto reservado | Similitud con OTROS objetos | M1/M2/M3/M4; excluir mismo grupo |
| T3 estructura | Ejemplar o especificación de bandas/motivos/relaciones | Juicio estructural independiente | Principal: M4 vs M2; control atributos sin orden |
| T4 restricciones composicionales | Ej. bandas alternantes y campo central | Cumplimiento visible y cobertura | Filtro simbólico+ranking vs ranking sin filtro |
| T5 robustez | Consultas de museo reservado o secundarios | Mismo protocolo | Δdesempeño por fuente, calidad, fragmentación |
| T6 agrupamiento exploratorio | Colección completa | Clases externas solo si existen | ARI/NMI con referencia; sin referencia, análisis descriptivo |

M0 no tiene entrada de imagen; M1 no procesa texto. No completar una tabla con números ficticios de modalidades inexistentes. Un M0 basado en metadatos del objeto consultado es una condición multimodal distinta y debe etiquetarse así. No comparar rankings de tareas diferentes como si compartieran la misma dificultad.

#### Particiones y prevención de fugas
Construir componentes conexas de relaciones confirmadas: mismo objeto, foto exacta, vistas vinculadas y duplicado perceptual adjudicado. Detectar textos curatoriales idénticos o casi idénticos que puedan revelar equivalencias, sin agrupar automáticamente frases genéricas. Congelar el mapa de grupos y documentar decisiones.

Separar grupos para desarrollo y evaluación. En una colección pequeña puede usarse ~30% desarrollo y70% test como punto de partida, estratificado por fuente; los números definitivos dependen de grupos reales, no de filas. Las consultas de test proceden de grupos que no participaron en ajuste ni desarrollo de consultas. La galería de evaluación puede ser fija e incluir objetos elegibles de test; no aprender con sus etiquetas. Para T2 excluir el grupo de consulta de candidatos. Si se permite galería compartida de desarrollo/test, declararlo como evaluación transductiva de recuperación y evitar aprendizaje a partir de sus relevancias.

Fijar normalización, diccionario, pesos, plantillas y reglas con desarrollo. Test se ejecuta una sola vez por protocolo congelado. Para LOMO central, reservar museo también en ajuste de fusión y umbrales; reportar cambios de tamaño y clases. La colección de aptitud y el benchmark de recuperación tienen propósitos distintos.

#### Consultas y ground truth reales
Plan inicial:12-15 consultas de desarrollo y 40-60 consultas de prueba, distribuidas en familias estructurales y generales. Son tamaños de planificación, no cálculo de potencia ni garantía de significación. El piloto estima varianza y tiempo; ajustar número antes del cierre de test. Variantes de una misma consulta se agrupan para bootstrap y no se cuentan como independientes.

Dos expertos redactan/validan necesidades informativas y juzgan sin conocer modelo/ranking. Qrels graduados:0 no pertinente,1 parcial,2 pertinente,3 muy pertinente; "no evaluable" es estado separado. Una justificación debe señalar evidencia visible y distinguir atribución cultural. No derivar qrels por coincidencia exacta del descriptor ni por similitud CLIP.

Para galería120 y 40 consultas, juicio exhaustivo son 4800 pares por revisor: presupuestar ese trabajo. Si no es viable, usar pooling ciego de top20 de todos los sistemas predeclarados más muestra aleatoria y positivos propuestos por experto; deduplicar pares. El pool reduce esfuerzo, pero sesga a los sistemas que contribuyeron. Publicar proporción juzgada y no equiparar no juzgado a irrelevante sin análisis de sensibilidad. Recall y mAP solo tienen denominador fiable con evaluación suficientemente completa; con pool incompleto reportarlos como relativos al pool. Consultas sin relevantes: reportar frecuencia, reglas predeclaradas y no eliminarlas silenciosamente.

Al menos una muestra relevante de juicios debe ser doble y no solo ejemplos sencillos. Para inferencia fuerte se prefieren todos los juicios primarios doblemente evaluados. Reportar acuerdo antes de adjudicación; conservar ambas versiones y resolución.

#### Métricas e inferencia
Primaria: nDCG@10 por consulta estructural con ganancias2^rel-1 y descuento log2(r+1). Secundarias: P@5/10, Recall@10 cuando ground truth completo, MRR si existe objetivo de primer relevante, mAP con relevancia binarizada predefinida. Contexto, idioma y consultas generales son análisis secundarios.

Comparar M4-M2 por consulta; bootstrap pareado por familia de consulta con10000 réplicas y semilla fijada, e IC95%. Una permutación pareada puede acompañar como sensibilidad. Repeticiones de semilla de un encoder congelado no crean nuevos sujetos. Si se ajusta M4 en varios splits, separar variabilidad del ajuste y de las consultas. Holm para familia de comparaciones secundarias confirmatorias o etiquetarlas exploratorias; no seleccionar solo métricas favorables.

Umbral práctico propuesto ΔnDCG@10=0,03, ratificado antes del test. Análisis de potencia aproximado tras piloto de desarrollo: n≈[(z(0,975)+z(0,8))·SD(d)/δ]^2, reconociendo dependencia y distribución acotada; no sustituye simulación/estimación específica. Si el tiempo no permite n suficiente, reportar IC amplio y alcance piloto.

#### Ablaciones y controles mínimos
Ablaciones: M4 sin estructura; M4 sin texto; M4 sin contexto; M3 atributos sin orden frente a M3 completo; solo bandas vs solo motivos/relaciones; sin color para determinar si una ganancia es principalmente cromática. Mantener mismo conjunto de consultas y candidatos.

Controles negativos: permutar descriptores entre grupos dentro de museo en desarrollo y evaluar la condición congelada; esto debe degradar el aporte de estructura si el mecanismo es real. Control fuente/tamaño simple detecta atajos institucionales. Emparejar o estratificar por calidad y reportar desempeño de fragmentos. Los controles no generan ground truth sintético.

Robustez mediante recorte, escala, compresión o cambios moderados de iluminación puede complementar fotos reales, con transformaciones registradas y sin reemplazar la evaluación principal. Algunas transformaciones alteran relevancia; revisarlas antes de llamar "invariante" al sistema.

#### Interpretabilidad evaluable
Para cada resultado, mostrar contribuciones del score con valores observados, máscara y procedencia. Fidelidad algebraica: suma de contribuciones coincide con score a tolerancia numérica. Intervención: retirar/cambiar un atributo altera score/ranking como especifica la fórmula. Validación humana: explicación correcta, útil y no especulativa en muestra de éxitos y errores, revisada ciegamente. Reportar desacuerdos y cobertura.

Medir costo de anotación por objeto y tiempo de juicio; la utilidad marginal puede no justificar ese costo. Una explicación de ranking no es interpretación del significado ritual ni prueba de la cultura de origen.

#### Archivos y criterios de cierre
Crear en nueva versión: objects.csv, images.csv, groups.csv, annotations.jsonl, queries.csv, qrels.csv, splits.csv, models.toml, run_manifest.json, rankings.csv, metrics_by_query.csv, tablas e IC. Cada run registra commit, hashes de insumos, checkpoint, normalización, parámetros, hardware y semilla. Usar nombres nuevos; preservar v1.2.

Termina H1 cuando hay corpus/grupos verificables, anotación pertinente, M0-M4 para las modalidades aplicables, evaluación independiente, ablación de estructura/orden, análisis de incertidumbre/errores y reproducción por tercero. Una hipótesis no confirmada con diseño válido también es un resultado de maestría.

