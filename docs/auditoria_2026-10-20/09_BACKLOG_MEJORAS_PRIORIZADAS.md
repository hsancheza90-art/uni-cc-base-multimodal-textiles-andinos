### Backlog priorizado

#### Orden de ejecución
P0 bloquea la validez del resultado que se pretende afirmar. P1 debe cerrarse antes del experimento confirmatorio. P2 mejora fiabilidad y reporte. P3 es expansión opcional. Las estimaciones son días de trabajo efectivo, no promesas de calendario.

| ID | Prioridad/horizonte | Trabajo | Dependencia | Aceptación verificable | Esfuerzo | Riesgo |
|---|---|---|---|---|---:|---|
| MET01 | P0/H1 | Congelar preguntas, métricas, comparadores y criterios de éxito | Asesor y alcance | Protocolo fechado, test intacto | 1 | Bajo |
| DAT01 | P1/H1 | Snapshot v2 con objetos, registros, fotos y grupos | DAT02 | IDs, grupos y hashes sin conflictos | 2 | Medio |
| DAT02 | P1/H1 | Revisar duplicados, vistas y disponibilidad real | Manifiestos | Cero grupo dividido entre particiones, fotos verificadas | 2-3 | Medio |
| ANN01 | P0/H1 | Piloto de anotación estructural y guía operacional | Descriptor mínimo | 30-40 objetos doble anotados, acuerdo/desacuerdo documentado | 3-5 | Alto, disponibilidad experta |
| ANN02 | P0/H1 | Qrels independientes y consultas | ANN01, protocolo | Juicios ciegos, autoría, cobertura y acuerdo, sin etiquetas derivadas del modelo | 5-10 | Alto |
| SW01-03 | P1/H1 | Contratos de decisión, unicidad y caché | Informe06 | Reproducciones fallidas pasan tras corrección, v1 intacta | 2 | Medio |
| SW06-07 | P1/H1 | Validación agrupada y tuning separado de aptitud | DAT02, etiquetas explícitas | Ningún preprocesamiento ajustado con outer-test; matriz independiente | 2-3 | Medio |
| APT01 | P1/H1 | Rotular resultados de aptitud como desarrollo | Ninguna | No se llama independiente a los40 casos históricos | 0,5 | Bajo |
| APT02 | P2/H2 | Test externo nuevo y calibración probabilística | Sistema congelado, expertos | IC agrupados, cobertura y error por fuente | 3-5 más muestreo | Alto |
| MAT01 | P1/H1 | Definir palabras, máscaras, distancias e invariancia | ANN01 | Especificación completa y pruebas de propiedades | 2 | Bajo |
| MOD01 | P1/H1 | M0/M1/M2 con configuración congelada | DAT01 | Embeddings/rankings reproducibles y modalidades bien rotuladas | 2-3 | Medio |
| MOD02 | P1/H1 | M3, control sin orden y M4 | MAT01, MOD01 | Descomposición exacta del score y pesos solo de desarrollo | 3-4 | Medio |
| EXP01 | P0/H1 | Evaluación pareada, ablaciones y robustez | ANN02, MOD02 | Métrica primaria, IC, errores y todos los modelos predeclarados | 2-3 | Medio |
| REP01 | P1/H1 | InformeII y paquete reproducible | EXP01 | Cada conclusión enlaza a resultado real; reproducción externa | 3 | Bajo |
| BIB01 | P1/H1 | Completar búsqueda/lectura de antecedentes cruciales | Acceso documental | Cribado trazable, versiones y límites claros | 3-5 | Medio |
| SW04-05/08-12 | P2/H1-H2 | Errores de descarga, fechas, docs, retry, texto, escritura, CI | Hallazgos06 | Contratos de regresión, sin refactorización amplia | 2-3 | Bajo/medio |
| EXT01 | P3/H2 | SigLIP/DINO y WL | H1 cerrado | Ganancia/costo evaluados con mismo protocolo | 3-5 | Medio |
| PUB01 | P3/H3 | Extensión multicolección y validación externa | H2 y gobernanza | Evidencia independiente y contribución editorial específica | No estimable aún | Alto |

#### Qué es obligatorio antes de qué
Antes del piloto técnico: preservar snapshot, corregir contratos críticos y declarar claramente que el piloto no es test final. Se puede desarrollar BM25/CLIP sin esperar un estudio externo de aptitud.

Antes de cualquier afirmación confirmatoria: grupos, ground truth, protocolo, anotación y separación de ajuste/test. Si la selección del corpus se mantiene por decisiones humanas verificadas, no hace falta convertir aptitud en un subproyecto grande para evaluar recuperación. El sistema de aptitud puede quedar como apoyo exploratorio y sus límites declararse.

Antes de automatizar descarte en una fuente nueva: APT02 y política de abstención con costos de error. La AUC interna no autoriza descarte automático generalizado.

#### Qué no priorizar
No enumerar el espacio de patrones, entrenar un VLM desde cero, construir una GNN compleja ni producir una interfaz elaborada antes de validar M0-M4. No aumentar el número de museos únicamente para elevar el conteo si faltan anotaciones y grupos confiables. No corregir las pruebas cambiando datos curatoriales o hashes congelados.

Cada defecto técnico SW01-SW12 tiene archivo, causa, corrección, aceptación, riesgo y esfuerzo en informe06. Este backlog no declara que los parches hayan sido implementados.

