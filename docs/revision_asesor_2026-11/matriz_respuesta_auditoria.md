# Matriz de respuesta a la auditoría del 20 de octubre de 2026

Estado al 6 de noviembre de 2026. Los identificadores corresponden al informe 09 de la auditoría, que se encuentra versionada en `docs/auditoria_2026-10-20/`. La columna de evidencia remite a los archivos del repositorio y al commit que los introdujo. Los estados se interpretan así:

- **Hecho:** la observación fue atendida y verificada.
- **En curso:** hay avance parcial, con fecha prevista de término.
- **Propuesto:** la acción está lista y espera la decisión del asesor.
- **Diferido:** queda fuera del alcance de las cuatro semanas, como prevé el plan de cierre.
- **Sin avance:** no se ha trabajado todavía.

## Observaciones científicas y de datos

| ID | Observación | Acción | Evidencia | Estado |
|---|---|---|---|---|
| MET01 | Congelar preguntas, métricas, comparadores y criterios de éxito | Protocolo con H1–H3, reglas de decisión, tareas, M0–M4, particiones, juicios, métricas, ablaciones y criterios de suspensión; valores en configuración, comprobados contra el documento | `docs/protocolo_experimental_v2.md` v0.5; `config/experimento.toml` (`077f89c`, `0143686`, `75a281e`) | Propuesto: falta su aprobación |
| DAT01 | Snapshot v2 con objetos, registros, fotos y grupos | Complementario v2, consolidado v2 con grupo, licencias, manifiesto y SHA-256; particiones congeladas | `corpus-met-cma-aic-v2.0`; `outputs/reports/corpus_textiles_andinos_met_cma_aic_v2_resumen.md` (`f3b0caf`, `0143686`) | Hecho |
| DAT02 | Duplicados, vistas y disponibilidad real | Cinco señales de candidatos, 100 pares decididos por el investigador, 577 grupos; ningún grupo partido entre particiones (comprobación automática); imágenes verificadas por SHA-256 antes de cada cálculo | `outputs/reports/grupos_v2.md`; `outputs/reports/experimento_v2_snapshot.md` (`f3b0caf`) | Hecho |
| ANN01 | Piloto de anotación estructural y guía operacional | Esquema con bandas y estados; núcleo de 150 anotado y validado; re-anotación ciega del lote 1 para el acuerdo intra-anotador (no hay segundo anotador) | `docs/protocolo_anotacion_v2.md`; `outputs/reports/anotacion_v2_validacion.md` (`94e61c7`, `4ee20d3`) | En curso: re-anotación desde el 12 de noviembre |
| ANN02 | Qrels independientes y consultas | Consultas T3 sorteadas y congeladas; 6 consultas T1 redactadas antes de ejecutar sistemas; pool de desarrollo ciego con ejemplos de la escala; doble juicio parcial propuesto | `data/metadata/consultas_t1_v2.xlsx`, `data/metadata/juicios_desarrollo_v2.xlsx` (`1eeb9c4`, `8a826f8`) | En curso: juicios del 6 al 17 de noviembre |
| MAT01 | Palabras, máscaras, distancias e invariancia | Especificación de M3 con definiciones, propiedades y costo; pruebas de invariancia, del ejemplo de Burnside, de la cota, de la simetría, del caso sin evidencia y de la reconstrucción | `docs/especificacion_m3.md`; `tests/test_sistemas.py` (`75a281e`) | Hecho |
| MOD01 | M0, M1 y M2 con configuración congelada | M0 BM25, M1 Lab+LBP sobre el textil y M2 OpenCLIP con checkpoint y hash de pesos; rankings de desarrollo | `config/modelos.toml`; `data/metadata/m2_openclip_manifiesto_v2.json`; `outputs/reports/experimento_v2_rankings_desarrollo.md` (`c3d186a`, `75a281e`) | Hecho en desarrollo; se congela en S3.3 |
| MOD02 | M3, control sin orden y M4 | M3 y M3-sin-orden implementados y probados; M4 pendiente | `src/modelos/m3_estructura.py` (`75a281e`) | En curso: M4 del 13 al 15 de noviembre |
| EXP01 | Evaluación pareada, ablaciones y robustez | Diseñadas en el protocolo (secciones 7 y 8); no se ha ejecutado ninguna consulta de prueba | Protocolo, secciones 7 a 9 | Pendiente: 18 y 19 de noviembre |
| REP01 | Informe II y paquete reproducible | Flujo de 23 pasos sin red y 350 pruebas; cada commit verificado en un clon limpio; etiqueta del corpus | README; `corpus-met-cma-aic-v2.0` | En curso: reproducción por el asesor al cierre |
| BIB01 | Búsqueda y lectura de antecedentes cruciales | Sin avance desde la auditoría | Plan de cierre, S1.9 | Sin avance: capítulos 3 y 4 |
| APT01 | Rotular la aptitud como desarrollo | Cifras rotuladas como validación de desarrollo en el protocolo de aptitud, las notas para la tesis y el README | `docs/protocolo_aptitud_v2.md`; `docs/notas_para_tesis.md` (`6c9ae72`) | Hecho |
| APT02 | Test externo y calibración probabilística | Fuera de H1; la aptitud queda como apoyo exploratorio (D2) | Plan de cierre | Diferido (H2) |
| EXT01 | SigLIP, DINO y WL | Fuera de H1 | Plan de cierre | Diferido (H2) |
| PUB01 | Extensión multicolección y validación externa | Fuera de H1 | Plan de cierre | Diferido (H3) |

## Contratos de código (informe 06)

| ID | Observación | Acción | Evidencia | Estado |
|---|---|---|---|---|
| SW01 | Una decisión inválida en el workbook se exportaba como pendiente | La revisión se detiene ante decisiones inválidas, sin reemplazar salidas, con su prueba | `5b67439` | Hecho |
| SW02 | Se aceptaban filas sin ID o con IDs repetidos | Unicidad y presencia del ID antes de escribir, con su prueba | `5b67439` | Hecho |
| SW03 | La caché de medidas no depende de la configuración | Sin cambio: no se vuelve a medir. M1 calcula sus propias características y verifica cada copia por SHA-256 | Plan de cierre | Diferido |
| SW04 | Una descarga fallida devolvía 0 | Código de salida distinto de 0 si alguna imagen falla, con su prueba | `62d6191` | Hecho |
| SW05 | Fechas imposibles aceptadas | Validación de calendario; la anotación v2 exige además anotador, fecha y estado | `41dd0d0`, `4ee20d3` | Hecho |
| SW06 | Escalado global y pliegues por registro en la aptitud | Cifras rotuladas como desarrollo (APT01); la corrección queda condicionada a D2 | `6c9ae72` | Diferido |
| SW07 | Umbrales elegidos con las mismas predicciones fuera de pliegue | Igual que SW06 | `6c9ae72` | Diferido |
| SW08 | «Byte a byte» no describía la comparación | La documentación dice «igualdad textual con LF» | README (`6c9ae72`) | Hecho |
| SW09 | Reintentos HTTP y POST del colector AIC | Sin cambio: no se recolecta de nuevo | Plan de cierre | Diferido |
| SW10 | El crédito de MET contaminaba la descripción | M0 no usa la descripción de MET, que además es una plantilla armada con los metadatos; la columna de crédito separada en el colector queda diferida | `config/modelos.toml` [m0] (`75a281e`) | Mitigado |
| SW11 | Escritura no atómica de los derivados | Sin cambio: todo derivado se regenera con el flujo | Plan de cierre | Diferido |
| SW12 | Sin integración continua | Verificación manual en un clon limpio en cada commit; la integración continua se pospone hasta después del 22 de noviembre (D7) | Plan de cierre | Diferido |

## Decisiones del plan de cierre

| ID | Decisión | Estado |
|---|---|---|
| D1 | Segundo anotador y evaluadores | Decidida (3 nov): no hay; estudio piloto |
| D2 | Papel del puntaje de aptitud | Propuesta: apoyo exploratorio, rotulado como desarrollo |
| D3 | Esquema de anotación ampliado | Decidida (3 nov) |
| D4 | Galería del benchmark | Propuesta: núcleo de 150, agrupado (146 grupos) |
| D5 | Umbral práctico y métrica primaria | Propuesta: ΔnDCG@10 = 0,03; bootstrap pareado de 10 000 réplicas |
| D6 | Dependencias de M2 | Decidida (5 nov): torch 2.15.0 CPU, open_clip 3.3.0, checkpoint con licencia MIT |
| D7 | Versionar la auditoría e integración continua | Decidida (6 nov): auditoría versionada en `docs/auditoria_2026-10-20/`; la integración continua se propone para después del 22 de noviembre |
