### Auditoría científica de la tesis

#### Resultado
Hay una base de ingeniería y curación sustancial, un marco conceptual pertinente y una pregunta de investigación aún abierta. La contribución central —beneficio de representar estructura explícita en recuperación multimodal— no tiene todavía evidencia experimental. La aptitud es un componente auxiliar de selección; su desempeño no valida la tesis de recuperación.

#### Lectura de los siete capítulos

| Capítulo | Lo defendible | Corrección para Seminario II |
|---|---|---|
| 1. Introducción | Motivación patrimonial y delimitación computacional | Precisar población observable y usuarios de recuperación; evitar extrapolar a todo textil andino |
| 2. Problema, objetivos e hipótesis | Articulación imagen/texto/contexto/estructura | Definir mejora, interpretabilidad, comparadores y población de consultas antes del test |
| 3. Estado del arte | Reconoce CLIP, fusión y representación estructural | Incorporar ontología andina de Brownlow, hipergrafos de Ngo y actualizaciones 2025-2026; separar versiones editoriales |
| 4. Fundamentos textiles | Distingue observación, atribución curatorial e interpretación cultural | Operacionalizar atributos; no inferir técnica o significado de una fotografía sin evidencia |
| 5. Matemática | Productos cartesianos, palabras, grafos y acciones son una base adecuada | Definir extracción, máscaras de observabilidad, acciones válidas y similitudes; retirar pretensión de novedad de teoremas clásicos |
| 6. Corpus | Esquema, trazabilidad y conservación histórica | Separar versión histórica de expansión v2, objeto de fotografía y decisión de anotación |
| 7. Programa experimental | Propone baseline, descriptor y fusión | Convertirlo en protocolo con qrels independientes, particiones agrupadas, ablaciones e incertidumbre |

El capítulo 4 y la sección 5.23 ya reconocen límites interpretativos: conviene conservarlos. La analogía con quipus no demuestra que una representación visual permita reconstruir un sistema cultural de codificación.

#### Matriz de trazabilidad científica

| Objetivo/hipótesis | Implementación y evidencia | Métrica requerida | Estado |
|---|---|---|---|
| OE1 sistematizar atributos | Vocabulario TOML, esquema y guía; cero anotaciones estructurales | Cobertura y acuerdo por atributo | PARCIAL |
| OE2 modelo combinatorio restringido | Ecs. 5.1-5.78, sin extractor/descriptor operativo de recuperación | Propiedades formales y ablación orden/relaciones | PARCIAL |
| OE3 corpus curado | 288 congelados, 874 decisiones; faltan imágenes verificadas y grupos finales v2 | Integridad, duplicación, disponibilidad, sesgos | PARCIAL |
| OE4 baseline preentrenado | No embeddings ni checkpoint/runs observados | nDCG@10, tiempo, memoria | NO_IMPLEMENTADO |
| OE5 evaluar recuperación y ablaciones | Sin consultas ni juicios de relevancia | Diferencias pareadas e IC | NO_IMPLEMENTADO |
| OE6 analizar límites | Discusión conceptual y notas de limitaciones de aptitud | Errores por museo/atributo y robustez | PARCIAL |
| Hipótesis general: representación más rica e interpretable | No operacionalizada ni contrastada | Ganancia estructural y fidelidad de explicación | NO_IMPLEMENTADO |
| H matemática 1, Ωobs ⊊ Ω0 | Se sigue fácilmente de muestra finita vs espacio enorme | Restricciones predictivas fuera de muestra | PARCIAL; no evidencia cultural |
| H matemática 2, invariantes | Se declara φ(Pi)≈φ(Pj), sin transformación/tolerancia | Invariancia exacta o estabilidad medida | NO_IMPLEMENTADO |
| H matemática 3, beneficio multimodal | Ecuación de fusión; no resultados M4-M2 | ΔnDCG@10 estructural y utilidad de explicación | NO_IMPLEMENTADO |

No se identifican modelos de recuperación al recorrer src, dependencias y salidas. Las variables de simetría y regularidad en medidas.py son características de aptitud; no constituyen por sí mismas M3 ni un experimento de recuperación.

#### Reformulación mínima conservando el proyecto
Pregunta: en un conjunto congelado de objetos andinos representados por fotografías institucionales, ¿añadir orden de bandas y relaciones entre regiones a señales textuales y visuales mejora la recuperación estructural juzgada por expertos, y permite explicar fielmente el ranking?

Hipótesis primaria experimental: M4 mejora nDCG@10 respecto de M2 en consultas estructurales independientes. Fijar antes del test un umbral práctico, por ejemplo 0,03 puntos absolutos; es una decisión de diseño, no un resultado ni un umbral universal. Reportar IC de la diferencia: si incluye cero, evidencia inconclusa; si excluye cero pero la magnitud es menor al umbral práctico, mejora pequeña. No exigir un resultado positivo para que una tesis rigurosa termine.

Hipótesis de mecanismo: el modelo con secuencia/adyacencia supera una variante con los mismos atributos sin orden. Sin esta comparación, una mejora solo demuestra utilidad de atributos humanos adicionales, no de combinatoria.

Hipótesis de interpretabilidad: las contribuciones explicadas reconstruyen el score, una intervención sobre un atributo cambia el score conforme a la regla y evaluadores independientes consideran respaldadas las explicaciones por evidencia visible. No usar fluidez verbal como prueba.

#### Originalidad defendible
Candidata: una representación operacional de macroestructura visible, con equivalencias justificadas, incertidumbre explícita y fusión reproducible, evaluada con juicios expertos para textiles andinos y controles por museo. Es originalidad de diseño/aplicación y evidencia; no se ha demostrado aún originalidad matemática fundamental. La ontología andina de Brownlow et al. (2015) impide declarar que este sea el primer trabajo computacional estructurado sobre tejido andino. Ngo et al. (2021) ya estudian recuperación estructural textil, aunque con estructura de hilos y datos distintos.

Una prueba de invariancia de la representación propuesta puede ser una aportación formal propia de la tesis como desarrollo, pero no debe presentarse como nuevo lema de teoría de grupos. La búsqueda limitada no permite garantizar prioridad mundial.

#### Estimación de avance
Estimación orientativa de trabajo científico, no calificación institucional ni porcentaje de líneas de código:

| Bloque | Peso | Cumplimiento estimado | Aporte |
|---|---:|---:|---:|
| Problema y revisión crítica | 15 | 65% | 9,75 |
| Corpus, procedencia y versiones | 20 | 75% | 15,00 |
| Formalización operacional | 15 | 35% | 5,25 |
| Anotación y evaluación independiente | 20 | 5% | 1,00 |
| Modelos y experimentos centrales | 20 | 0% | 0,00 |
| Análisis de resultados y reporte II | 10 | 10% | 1,00 |
| Total | 100 | | 32,00% |

Rango razonable 25-40%, centro 32%, sensible a esos pesos. La auditoría presente no cuenta como resultados del estudiante. El componente experimental central está aproximadamente en 0-5%; la infraestructura del corpus está mucho más avanzada. No es apropiado sumar 207 pruebas de software a experimentos científicos.

