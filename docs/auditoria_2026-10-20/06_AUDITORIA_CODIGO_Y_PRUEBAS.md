### Auditoría de código y pruebas

#### Resultado reproducido
207 pruebas pasan y el flujo de 13 etapas termina con código 0 usando dependencias fijadas. Los resultados son reproducibles a partir de insumos archivados. Se han reproducido cinco fallos de contrato que la batería actual no detecta; ninguno exige rehacer la arquitectura. Scripts auxiliares no modifican el repositorio.

#### Hallazgos con evidencia y tratamiento

| ID/prioridad | Archivo/función y evidencia | Impacto y causa | Corrección y aceptación | Esfuerzo/riesgo/dependencias |
|---|---|---|---|---|
| SW01 P1 | [apply_met_review_v2, normalizar_corpus_final/aplicar_revision](https://github.com/hsancheza90-art/uni-cc-base-multimodal-textiles-andinos/blob/c38996e3af4b1874498e7e3e24ed4fc5c3e59471/src/metadata/apply_met_review_v2.py#L33-L116): valor_invalido retorna 0 y se exporta pendiente | Normalización borra evidencia del valor inválido; AIC reutiliza ruta | Validar valor crudo antes de normalizar; inválido→retorno1 y sin reemplazar salidas. Prueba parametrizada MET/AIC | 0,5 día; riesgo bajo; preservar pendientes legítimos |
| SW02 P1 | [apply_cma_review_v2.validar](https://github.com/hsancheza90-art/uni-cc-base-multimodal-textiles-andinos/blob/c38996e3af4b1874498e7e3e24ed4fc5c3e59471/src/metadata/apply_cma_review_v2.py#L78-L90): acepta dos filas de mismo ID | Doble conteo/sobrescritura aguas abajo; no es duplicación presente hoy | Unicidad por fuente antes de escribir, rechazar ID vacío y duplicado; prueba contrato entre tres fuentes | 0,5 día; bajo; ninguna |
| SW03 P1 | [medidas.medir](https://github.com/hsancheza90-art/uni-cc-base-multimodal-textiles-andinos/blob/c38996e3af4b1874498e7e3e24ed4fc5c3e59471/src/imagenes/medidas.py#L466-L502): cambio nitidez_lado_textil 600→123 no invoca medición | Caché solo por hash de imagen; configuración y metadatos pueden quedar obsoletos | Clave=(hash imagen, hash config pertinente, hash metadatos usados, versión algoritmo); test invalida solo afectados | 1 día; medio; nueva versión de medidas, jamás reescribir v1 |
| SW04 P2 | [descargar_evaluacion.ejecutar](https://github.com/hsancheza90-art/uni-cc-base-multimodal-textiles-andinos/blob/c38996e3af4b1874498e7e3e24ed4fc5c3e59471/src/imagenes/descargar_evaluacion.py): error simulado devuelve0 | Automatización puede interpretar descarga fallida como éxito | Mantener manifiesto de errores, retorno no cero o política explícita partial; test fallo total/parcial | 0,5 día; bajo; documentar reanudación |
| SW05 P2 | [anotacion.normalizar_fila](https://github.com/hsancheza90-art/uni-cc-base-multimodal-textiles-andinos/blob/c38996e3af4b1874498e7e3e24ed4fc5c3e59471/src/anotacion/aplicar_anotaciones.py#L31-L53): 2026-99-99 sin errores | Regex valida forma pero no fecha de calendario | date.fromisoformat, comprobar rango y requisito de autor para anotación; test bisiesto e inválidos | 0,25 día; bajo; conservar textos históricos aparte |
| SW06 P1 | [calibrar, líneas228–244](https://github.com/hsancheza90-art/uni-cc-base-multimodal-textiles-andinos/blob/c38996e3af4b1874498e7e3e24ed4fc5c3e59471/src/imagenes/calibrar_aptitud.py#L222-L255) | Escalado global y folds por registro contaminan estimación inductiva | Pipeline con escalado/anclas de train, folds por grupo, tuning interno; test que test no cambia parámetros de train | 2–3 días; medio; grupos de objetos y etiquetas |
| SW07 P1 | [elegir_umbrales/construir_informe](https://github.com/hsancheza90-art/uni-cc-base-multimodal-textiles-andinos/blob/c38996e3af4b1874498e7e3e24ed4fc5c3e59471/src/imagenes/calibrar_aptitud.py#L259-L397) | Mismas OOF eligen cortes y producen matriz; optimismo | Separar selección y evaluación; informe rotulado desarrollo mientras tanto | 1 día junto SW06; medio; política de descarte |
| SW08 P2 | [test_flujo, 62–92](https://github.com/hsancheza90-art/uni-cc-base-multimodal-textiles-andinos/blob/c38996e3af4b1874498e7e3e24ed4fc5c3e59471/tests/test_flujo.py#L62-L92) y README | “byte a byte” no describe comparación CRLF normalizada | Corregir documentación; si se promete bytes, añadir hash de outputs deterministas sin normalizar | 0,25 día; bajo |
| SW09 P2 | [utils/http](https://github.com/hsancheza90-art/uni-cc-base-multimodal-textiles-andinos/blob/c38996e3af4b1874498e7e3e24ed4fc5c3e59471/src/utils/http.py), collector AIC | Retry permite GET, colector consulta mediante POST | Incluir POST solo para endpoint de búsqueda idempotente o reintento explícito acotado; mock429/503 y Retry-After | 0,5 día; medio; API documentada |
| SW10 P2 | [met_collector_v2](https://github.com/hsancheza90-art/uni-cc-base-multimodal-textiles-andinos/blob/c38996e3af4b1874498e7e3e24ed4fc5c3e59471/src/collectors/met_collector_v2.py#L160-L185) | creditLine se guarda en descripcion: crédito no descripción del contenido | Columna crédito separada en nueva versión, recuperar descripción si existe o dejar faltante; evitar contaminar BM25 | 0,5 día; medio; contrato textual v2 |
| SW11 P2 | Rutas de salida y escritores CSV | Escritura directa puede dejar derivados parciales ante interrupción; no se simuló fallo de disco | Temporal+replace atómico para derivados críticos; validar antes de escribir | 1 día; bajo; no refactorizar todo |
| SW12 P2 | Sin workflow CI identificado | Suite depende de ejecución local; cobertura no medida | CI con 207 pruebas y contratos nuevos, Python de referencia fijado; lint acotado a nuevo código | 0,5–1 día; bajo; hosting autorizado en fase posterior |

P0 científico: no presentar la estimación contaminada como prueba independiente ni construir evaluación central circular. P0 no implica vulnerabilidad de seguridad ni daño demostrado al corpus. SW01–05 tienen reproducción dinámica en evidencias/defectos_reproducidos.json. SW06–10 combinan inspección estática con datos/ejecución del flujo; SW11 es riesgo de diseño, no incidente observado.

#### Arquitectura, colectores y fechas
El registro común de fuentes y los módulos utils reducen duplicación. La arquitectura por etapas es adecuada; no hace falta migrar a un framework pesado. Hay tipado parcial con dict[str, Any]; agregar contratos de filas en fronteras aporta más que tipar cada función interna.

Los filtros usan palabras completas y evitan penalizar títulos figurativos cuando material/clasificación aportan evidencia textil. Son reglas auditables, no clasificadores científicamente validados. La excepción Wari en superficies es un criterio de selección que puede sesgar la distribución; documentarla.

La normalización cronológica conserva un problema semántico inevitable: intervalos, siglos, a.C./d.C. e incertidumbre no se reducen siempre a un año. El corte por inicio>1532 no equivale a exigir que todo el intervalo sea prehispánico. Probar intervalos que cruzan1532, ausencia de fecha y siglos ambiguos; registrar estado indeterminado. No se atribuye a los tests actuales validación arqueológica.

CMA deja algunos campos vacíos en las salidas de revisión; el consolidado v1 puede recuperarlos uniendo originales. No es correcto afirmar pérdida universal de metadatos. El índice textual v2 debe comprobar ese join. Colectores y descarga dependen de servicios externos: sus pruebas con mocks son útiles, pero las APIs actuales no se recorrieron completas.

#### Protección, licencias y reproducibilidad
Las pruebas protegen la no sobrescritura habitual de workbooks con decisiones. Aun así, resolver rutas canónicas antes de comparar rutas protegidas evita alias de ruta; es una mejora preventiva, no un incidente reproducido aquí. Usar backup/versionado antes de migrar esquemas humanos.

En descarga, limitar bytes durante streaming, no solo después de cargar response.content; ajustar límite de píxeles al uso científico. Conservar URL, fecha, MIME, hash original, hash derivado, transformación y error. No tratar licencia de metadatos como licencia universal de cada imagen. El estado legal actual por objeto no se reverificó en la web.

Dependencias exactas facilitan reproducción. Python local 3.12 pasa aunque la referencia documental sea distinta; eso no prueba compatibilidad en Windows/macOS ni otras versiones. Congelar versión de Python, dependencias y hardware para embeddings. Para GPU registrar semilla, modo determinista y posibles tolerancias numéricas.

#### Pruebas necesarias, no ejecutadas todavía
Contratos: IDs únicos/no vacíos, relaciones imagen↔objeto, vocabulario, esquema por fuente, fechas válidas, licencia/procedencia y completitud de manifiesto.

Propiedades: normalización idempotente; particiones disjuntas por grupo; canonización de bandas invariante bajo el grupo permitido; similitud acotada; vacíos no equivalen a máxima similitud.

Integración: fallo HTTP parcial visible; cambio de parámetros invalida caché; corrida desde copia mínima genera exactamente outputs esperados; interrupción no reemplaza archivos aprobados.

Estadística: introducir cambios solo en test no debe cambiar scaler, anclas, diccionario, pesos ni umbrales entrenados. Verificar independencia de qrels respecto del descriptor.

207 PASS no equivalen a cobertura de líneas o ramas: no se ejecutó una medición de cobertura. CI/lint/análisis estático completo: NOT_RUN. No se añadió una batería redundante al repositorio ni se entregan parches como si estuvieran aprobados.

