### Dictamen final
REQUIRES_METHODOLOGICAL_CORRECTIONS

#### Fundamento
La infraestructura del corpus funciona: flujo de 13 etapas,207 pruebas aprobadas y regeneración sin diferencias versionadas. Los874 registros y su reparto462/153/259 se verifican. La hipótesis central de recuperación permanece sin evaluar: faltan anotaciones estructurales, qrels independientes y comparación M0-M4.

La evaluación de aptitud requiere corrección por grupos duplicados entre folds, preprocesamiento global, selección sobre CV y reutilización de casos ciegos. El diagnóstico LOMO muestra AUC 0,563 AIC,0,556 MET y0,931 CMA, con muestras y condiciones diferentes. No es evaluación externa prospectiva ni demuestra transferencia general. Detalle y límites en informe07.

#### Respuestas a las diez preguntas exigidas
1. Avance científico aproximado:32%, rango orientativo25-40%, calculado con seis bloques ponderados en informe02. Experimento central aproximadamente0-5%. No es calificación oficial.
2. Corpus preparado: para piloto técnico y desarrollo de infraestructura, sí. Para evaluación central estructural, no: los 288 del consolidado siguen sin_anotar, falta congelar grupos/unidades v2, verificar imágenes y construir ground truth.
3. Aptitud: implementada y reproducible, pero su validación actual es de desarrollo. Necesita separación de ajuste/test, agrupación, incertidumbre y casos nuevos para afirmar transferencia.
4. Aportación matemática propia: una formalización operacional de macroestructura visible con observabilidad, equivalencias justificadas y similitud trazable. Aún es candidata. Burnside, Pólya, entropía y kernels existentes no son novedades propias.
5. Código obligatorio antes de experimentar: decisiones inválidas MET/AIC, unicidad CMA, caché dependiente de configuración/metadatos y contratos de grupos. Antes de afirmar validación de aptitud, corregir preprocesamiento/folds/selección de umbrales. Hallazgos y aceptación en informe06.
6. Combinación prometedora y viable: BM25 y visión simple como controles, CLIP/OpenCLIP congelado, descriptor de bandas/relaciones y fusión tardía explicable. SigLIP/DINO o WL son extensiones condicionadas.
7. Evidencia mínima de SeminarioII: benchmark real con relevancias independientes, M0-M4 en tareas aplicables, ablación de estructura y de orden, IC pareados, análisis por fuente/calidad, evaluación de fidelidad de explicación y reproducción.
8. Afirmaciones todavía no permitidas: superioridad de M4, interpretación cultural automática, invariancia al daño, transferencia universal de aptitud, originalidad mundial,462 objetos independientes o874 revisiones manuales individuales verificadas.
9. Principal amenaza: circularidad y dependencia entre selección, etiquetas, diseño y evaluación. Sin un test independiente, una mejora puede reflejar decisiones compartidas o duplicados en lugar del aporte estructural.
10. Cierre de SeminarioII: protocolo congelado, corpus/grupos/imágenes verificables, anotación y acuerdo, métodos implementados, resultados completos positivos o negativos, incertidumbre, explicaciones fieles, limitaciones y reproducción por tercero. No requiere que todas las hipótesis resulten favorables.

#### Prioridad y límites de este dictamen
La categoría principal es metodológica, porque los errores de validación y la ausencia de benchmark impiden la conclusión científica incluso con software ejecutable. También se requieren correcciones de corpus y software, detalladas como tareas subordinadas. No corresponde READY_FOR_EXPERIMENTS en sentido confirmatorio.

La revisión bibliográfica entregada es un mapeo parcial con búsquedas reales,64 registros importados y decisiones trazables, no una revisión sistemática exhaustiva cerrada. Solo cuatro documentos tienen evaluación sustantiva de método/datos/resultados en texto completo dentro de este proceso. La búsqueda y lectura pendiente se identifica expresamente en informe03. El diagnóstico no presupone rúbrica institucional no consultada.

No se modificó el repositorio, los workbooks ni v1.2. No hubo commits ni publicaciones. Las correcciones propuestas no se presentan como ya implementadas.

