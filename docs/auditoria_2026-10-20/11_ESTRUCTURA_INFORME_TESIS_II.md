### Estructura propuesta del informe de Seminario de Tesis II

#### Título y formulación
Conservar el título actual mientras se desarrolla el protocolo. Alternativa solo si refleja el trabajo finalmente ejecutado: "Representación combinatoria interpretable para la recuperación multimodal de textiles andinos en colecciones museográficas digitales". Es más preciso sobre tarea y población, no una decisión editorial impuesta.

Objetivo general propuesto: diseñar y evaluar una representación explícita de la macroestructura visible de textiles andinos, integrada con señales visuales y textuales, para determinar su aporte a la recuperación y a la explicación fiel de resultados.

Objetivos específicos:
1. Consolidar un corpus trazable con unidades experimentales y observabilidad verificadas.
2. Definir y anotar atributos y relaciones con acuerdo documentado.
3. Formalizar e implementar un descriptor de bandas, motivos y relaciones.
4. Implementar líneas base textual, visual y visión-lenguaje, y una fusión interpretable.
5. Evaluar con consultas y juicios independientes, ablaciones e incertidumbre.
6. Analizar robustez, costos, errores y límites culturales y computacionales.

No se cambia el núcleo del proyecto, se vuelve contrastable. Las métricas y variables están en informe08 y la correspondencia con objetivos originales en informe02.

#### Organización del documento

| Sección | Contenido indispensable | Evidencia/figuras propuestas |
|---|---|---|
| Resumen | Problema, tarea, muestra efectiva, método, resultado principal real y límite | No rellenar cifras centrales antes del experimento |
| 1. Introducción | Motivación, usuarios, alcance y contribuciones | Diagrama de preguntas y aportes |
| 2. Problema y objetivos | Hipótesis falsables, unidades y criterios de éxito | Matriz de consistencia |
| 3. Estado del arte | Mapeo actualizado, antecedentes andinos/textiles, familias y brecha | PRISMA bibliográfico separado del flujo del corpus |
| 4. Datos y anotación | Versiones, procedencia, licencias, selección, grupos y acuerdo | Conteos por fuente, faltantes y sesgos, acuerdo por atributo |
| 5. Método formal | Dominio, observabilidad, secuencias/grafo, equivalencias, distancia, fusión | Definiciones y demostración de invariancia, costo |
| 6. Implementación | Etapas, dependencias, checkpoints, determinismo y contratos | Arquitectura y manifiesto del run |
| 7. Diseño experimental | Tareas, consultas, qrels, particiones, métricas y análisis | Tabla de modelos/ablaciones y esquema sin fugas |
| 8. Resultados | Corpus, aptitud, descriptor, recuperación, híbrido y explicación, separados | Tablas T1–T8 indicadas abajo |
| 9. Discusión | Magnitud práctica, mecanismo, casos de fallo, costos y amenazas | Análisis estratificado y ejemplos seleccionados sistemáticamente |
| 10. Conclusiones | Respuesta por objetivo e hipótesis, incluso no confirmación | Sin inferencias más amplias que población evaluada |
| 11. Limitaciones y trabajo futuro | Cobertura, expertos, fuente, observabilidad y prioridades H2/H3 | Lista concreta de límites |
| Referencias y anexos | BibTeX corregido, protocolo, guía, scripts, hashes y pruebas | Paquete reproducible |

#### Tablas y figuras que deben producirse con datos reales
T1 versión/fuente/subconjunto y número de grupos independientes.
T2 cobertura y faltantes por atributo, foto y museo.
T3 acuerdo entre anotadores antes de adjudicación.
T4 aptitud interna agrupada y evaluación externa si se hace, con abstención e IC.
T5 M0–M4 por tarea/modalidad, nDCG primaria y métricas secundarias.
T6 ablaciones, especialmente estructura ordenada vs atributos sin orden.
T7 robustez por museo/calidad/fragmentación, con tamaños por celda.
T8 fidelidad/utilidad de explicación y costo de anotación/inferencia.

Figuras: flujo del corpus, ejemplo de objeto→regiones→palabra/grafo, distribución de diferencias pareadas por consulta, curvas precisión-recall cuando proceda, intervalos por fuente y panel de errores. Un mapa UMAP puede ser exploratorio, nunca prueba suficiente de separación cultural o recuperación.

No convertir los números LOMO de esta auditoría en la validación final de aptitud sin sus limitaciones. No utilizar resultados del corpus como sustituto de resultados de la hipótesis central.

#### Matriz de consistencia actualizada
| Pregunta | Variable manipulada | Resultado observado | Control |
|---|---|---|---|
| ¿Aporta estructura? | Inclusión del bloque estructural en M4 | ΔnDCG@10 pareada | M4 sin estructura y mismo desarrollo |
| ¿Aporta orden/relaciones? | Secuencias/adyacencias vs bolsas | ΔnDCG estructural | Mismos atributos y anotadores |
| ¿Es fiel la explicación? | Intervención/retirada de atributo | Cambio de score/ranking previsto | Reconstrucción algebraica y juicio ciego |
| ¿Es robusto por fuente? | Museo/calidad/conservación | Desempeño y cobertura estratificados | Grupos y tamaños reportados |
| ¿Aptitud generaliza? | Fuente reservada/nuevos objetos | AUC, PR, confusión, calibración y abstención | Sistema congelado y etiquetas nuevas |

#### Requisitos institucionales
Se consultó la página pública del programa indicada por el usuario. No se verificó una rúbrica vigente específica de SeminarioII, extensión mínima, estilo bibliográfico obligatorio, formato de defensa, número de experimentos ni criterio formal de aprobación. Esta estructura es una recomendación científica, no un reglamento atribuido a UNI. Contrastar con sílabo y asesor antes del formato final, sin detener el trabajo ya autorizado.

