# Matriz de respuesta al dictamen del 21 de noviembre de 2026

Estado al 23 de noviembre de 2026. Responde al «Informe técnico-científico de revisión. Dictamen de observaciones previo a la apertura del test» del asesor, emitido sobre el commit `6c121a3` y el protocolo 0.6.5. La numeración (B1 a B8, P1 a P5, C1 a C12, T1 a T8 y sección 10) es la del dictamen. La evidencia remite a archivos del repositorio; las pruebas se citan por archivo y nombre.

Estados:

- **Atendido:** la exigencia se cumplió y puede verificarse en el repositorio con la evidencia indicada.
- **Por verificar:** la acción está hecha y requiere la revisión del asesor del nuevo commit.
- **Pendiente:** depende de un paso posterior, que se indica.

Ningún estado describe un resultado científico. A la fecha no se ha ejecutado ningún sistema sobre las consultas de prueba.

## Resumen

| Observación | Condición | Estado | Evidencia principal |
|---|---|---|---|
| B1. Multiplicidad | C1 | Atendido | Protocolo 0.6.6, sección 1; R33; `evaluacion.compuerta` |
| B2. Inferencia de H1 | C2 | Atendido | Protocolo, sección 7; R34; `config/experimento.toml` (`replicas_permutacion = 100000`) |
| B3. Inferencia exacta de H2 | C3 | Atendido | Protocolo, sección 7; R35; `evaluacion.permutacion_exacta` |
| B4. H3 y revisión humana | C4 | Atendido | Protocolo, sección 8; R36; `--crear-revision-h3` |
| B5. Congelación, custodia y fallos | C5 | Atendido; la declaración del tesista se adjunta a la solicitud de autorización | Protocolo, sección 9; R37; `docs/registro_custodia.md` |
| B6. Alcance de H1 | C6 | Atendido | Capítulos 1, 2 y 7 y resumen |
| B7. Cegamiento y estabilidad | C7 | Atendido | Protocolo, secciones 6 y 10; R38; `validar_cegamiento`; capítulo 11 |
| B8. Juicios asistidos | C8 | Atendido | `docs/auditoria_juicios_desarrollo.md`; R39; capítulo 7, sección 7.6.4 |
| P1 a P5 | C9 | Atendido | Protocolo, secciones 6, 7 y 10; plantilla del informe |
| Concordancia protocolo, configuración y código | C10 | Atendido | `tests/test_experimento.py::test_t8_protocolo_configuracion_y_codigo_dicen_lo_mismo` |
| Desarrollo cerrado | C11 | Atendido | Diff desde `6c121a3` (más abajo) |
| Nuevo commit revisado y autorizado | C12 | Por verificar | Este commit; la autorización es del asesor |

## B1 a B8

| Obs. | Exigencia del dictamen | Acción | Evidencia | Estado |
|---|---|---|---|---|
| B1 | Secuencia fija o Holm; control formal por p de H1; Δ ≥ 0,03 como filtro adicional; frase sobre la potencia; corregir «al ser una sola» | Secuencia fija H1 → H2, elegida porque H1 es la hipótesis primaria. El texto separa el control formal (rechazo de H1) del filtro de magnitud y reconoce que la compuerta hace improbable confirmar H2. La frase se retiró. El informe rotula H2 «exploratoria» si H1 no se sostiene | Protocolo, sección 1; R33; `src/experimento/evaluacion.py` (`compuerta`); pruebas `test_t1_secuencia_fija_h2_solo_es_confirmatoria_si_h1_se_sostiene`, `test_t1_h1_confirmada_conserva_la_lectura_de_h2_favorable_o_no`, `test_t1_la_compuerta_mantiene_la_tasa_de_error_por_familia_bajo_la_nula` | Atendido |
| B2 | B = 100 000 fijo, semilla, p = (b + 1)/(B + 1), error de Monte Carlo, parada al completar B; tres afirmaciones; Δ negativa significativa; p no significativa; sobrestimación | Las 100 000 réplicas se calculan por bloques sin parada anticipada; se informa el error de Monte Carlo. La regla separa frente a cero, estimación y relevancia práctica, y cada combinación tiene su lectura («inferior al sistema de referencia» para Δ negativa significativa). El protocolo y el informe dicen que «se sostiene» no afirma un efecto poblacional de 0,03, que la p y el intervalo se informan aunque parezcan discrepar y que un efecto significativo puede estar sobrestimado | Protocolo, sección 7; R34; `evaluacion.decidir`, `permutacion_pareada`, `error_monte_carlo`; pruebas `test_t3_la_regla_separa_las_tres_afirmaciones_de_h1`, `test_t3_la_permutacion_usa_exactamente_b_replicas_y_su_error_de_monte_carlo` | Atendido |
| B3 | Enumeración exacta de 2^m; empates con tolerancia; n, b y m; p mínima; ambas medias; umbral 0,03 · n/b; b = 0 no estimable; intercambiabilidad | p exacta por enumeración; \|d\| ≤ 1e-12 cuenta como cero; el informe da n, b, m, la p exacta, la p mínima, la media global y la del subgrupo con su umbral equivalente (0,10 con 30 y 9). Se declaran el supuesto y sus límites. El informe de potencia retira el EMD de H2 por aproximación normal | Protocolo, sección 7; R35; `evaluacion.permutacion_exacta`, `p_minima`, `sin_empates`; `outputs/reports/experimento_v2_potencia.md`; pruebas `test_t2_la_p_exacta_de_h2_coincide_con_la_enumeracion_completa` (m = 0, 1, 5, 6 y 9), `test_t2_p_minima_y_tolerancia_de_empates`, `test_t2_exclusiones_ceros_y_b_mayor_que_m` | Atendido |
| B4 | H3 como fidelidad computacional; revisión humana descriptiva; acierto, error, semilla, clases cortas, no evaluable; ficha ciega con rúbrica, código de desacuerdo y justificación; no independencia | H3 se sostiene con reconstrucción e intervención. La revisión es descriptiva: acierto con grado ≥ 2, error con grado 0 o 1, sorteo con semilla, todos los casos si una clase es corta, `no_evaluable` fuera de las clases. La ficha no muestra clase, grado ni posición y registra valoración, componente en desacuerdo y justificación, con validador | Protocolo, secciones 1 y 8; R36; `ejecucion_prueba.py` (`--crear-revision-h3`, `muestra_revision_h3`, `validar_revision_h3`); pruebas `test_t6_la_muestra_de_h3_usa_todos_los_casos_si_una_clase_es_corta`, `test_t6_la_ficha_de_h3_es_ciega_y_se_valida` | Atendido |
| B5 | Secuencia obligatoria; insumos obligatorios; árbol limpio; identificador y estados; escritura atómica; huellas por fase; comparar todas al evaluar; rechazar mezclas; custodia verificable; gestión de fallos; declaración del tesista | Cinco estados (`autorizada`, `insumos_sellados`, `rankings_sellados`, `juicios_cerrados`, `evaluada`). El manifiesto se escribe antes de los rankings; falta de un insumo o cambios sin commit detienen la corrida. Escritura en temporales y publicación al final. `--evaluar` recalcula todas las huellas y suspende ante discrepancias, archivos faltantes o artefactos de otra corrida. Custodia: etiqueta Git anotada por estado, registro de custodia versionado y envío de huellas por correo. Reanudación solo desde un estado sellado; segunda corrida rechazada | Protocolo, sección 9; R37; `ejecucion_prueba.py` (`verificar`, `publicar`, `suspender`, `reejecucion`); `docs/registro_custodia.md`; pruebas `test_t4_alterar_un_byte_de_un_archivo_sellado_suspende_la_corrida`, `test_t4_evaluar_se_detiene_antes_de_producir_metricas_si_cambia_un_byte` (insumo, ranking y juicios), `test_t4_un_archivo_sellado_faltante_suspende`, `test_t4_un_manifiesto_de_otra_corrida_no_se_acepta`, `test_t5_una_caida_parcial_no_deja_salidas_ni_avanza_el_estado`, `test_t5_el_paso_de_rankings_exige_todos_los_insumos`, `test_t5_se_rechaza_la_reejecucion_accidental` | Atendido; la declaración escrita se adjunta a la solicitud |
| B6 | H1 como mejora de la fusión enriquecida frente a M2; el aporte de la estructura en ablaciones exploratorias; utilidad, costo de anotación y generalización por separado | Reescritos la hipótesis, la pregunta específica PE3, el alcance y el cierre del capítulo 2; el principio 4, los estimandos y las implicaciones del capítulo 7; el enfoque y la contribución del capítulo 1 y el resumen. El costo de anotación no medido se declara | `docs/manuscrito/capitulo_2_problema_objetivos_hipotesis.md` (secciones 2.2, 2.3, 2.5, 2.7 y 2.8), `capitulo_7_diseno_experimental.md` (7.1, 7.7 y 7.13), `capitulo_1_introduccion.md`, `00_resumen.md` | Atendido |
| B7 | Probar el cegamiento de extremo a extremo; distinguir «orden» de la posición; registrar rúbrica, instrucciones y pooling y comprobarlos contra los libros; rejuicio o declaración; reporte de `no_evaluable` | Validador del libro: sin sistema, puntuación ni posición, orden sorteado y guía igual a la rúbrica sellada; se aplica al entregar y al cerrar los juicios. El manifiesto sella la huella de la rúbrica, las instrucciones y el pooling. Sin rejuicio: se declara en el protocolo y en el capítulo 11 que no se estimó la estabilidad intraevaluador. `no_evaluable` por consulta y sistema, sin umbral | Protocolo, secciones 6, 9 y 10; R38; `ejecucion_prueba.py` (`validar_cegamiento`, `cegamiento_del_libro`, `reglas_juicio`); pruebas `test_t7_el_libro_de_juicios_es_ciego_de_extremo_a_extremo`, `test_t7_las_reglas_de_juicio_se_sellan_y_su_cambio_se_detecta`; capítulo 11, secciones 11.1 y 11.3 | Atendido |
| B8 | Archivo de auditoría con versión del modelo, instrucciones, entradas, respuestas, juicios anteriores y posteriores, firmas; separar 411 y 8; riesgo de anclaje en el capítulo 7 | Archivo privado de 429 archivos con manifiesto de sumas: modelo `claude-opus-5-5` en cinco instancias, instrucciones completas, las 411 imágenes que vio, sus respuestas, grados antes y después, revisión firmada y uso de cada juicio (411 para los pesos, 8 posteriores sin asistencia). Huella del manifiesto: `c473375f6cc9c3127906704a5e03e587d7db7b6585a1123fe5a794ea1d0099f2`. El capítulo 7 declara el anclaje con las cifras: 246 de 411 grados cambiados, κ de 0,161 antes y 0,925 después, justificación igual a la del modelo en 406 | `docs/auditoria_juicios_desarrollo.md`; R39; capítulo 7, sección 7.6.4 | Atendido |

## P1 a P5

| Regla | Exigencia | Dónde queda escrita | Estado |
|---|---|---|---|
| P1. Pooling y qrels | No juzgado frente a irrelevante; regla de pooling e IDCG; cobertura, tamaño del pool, relevantes, no evaluables y exclusiones; sensibilidad con retirada de aportes exclusivos | Protocolo, sección 6 («Supuesto del pooling») y tabla 2 del informe; `ejecucion_prueba.pooling` | Atendido |
| P2. Validez y generalización | Estimandos de M4 frente a M2, M4 sin M3 y M3 frente a M3-sin-orden; evaluación transductiva; confusores; heterogeneidad descriptiva | Protocolo, sección 7 («Estimandos»); capítulo 7, sección 7.7 | Atendido |
| P3. Control negativo | Exploratorio; semillas y número fijados | Protocolo, sección 7: una sola permutación dentro de cada museo, semilla en la configuración, sin permutaciones adicionales | Atendido |
| P4. Informe completo | Plantilla con todas las tablas; todos los análisis, cualquiera sea el signo | Protocolo, sección 7 («Informe de resultados», tablas 1 a 10); `ejecucion_prueba.informe`; prueba `test_el_informe_sigue_la_plantilla_de_diez_tablas` | Atendido |
| P5. Limitaciones | Anotación humana, evaluador único, pool parcial, potencia, pesos con diez consultas, generalización, estabilidad no estimada | Protocolo, sección 10; capítulo 11, sección 11.1 («Limitaciones fijadas antes del test») | Atendido |

## C10 a C12

- **C10.** La prueba `test_t8_protocolo_configuracion_y_codigo_dicen_lo_mismo` compara el protocolo con `config/experimento.toml`, `config/modelos.toml` y el código: B = 100 000, α, la tolerancia de empates, la de H3, la muestra de la revisión, las clases de H3, las lecturas de la regla, los estados de la corrida, las órdenes, el umbral del subgrupo, la p mínima, los pesos 1/7, 4/7 y 2/7, el k = 60 de M4-RRF, las 30 consultas y los siete sistemas del pool. La prueba anterior de coherencia (particiones, consultas, pool, nDCG@10, umbral, bootstrap e IC) se mantiene.
- **C11.** Desde `6c121a3` no cambia ningún archivo de `data/` ni `config/modelos.toml`: siguen las 30 consultas de prueba y las 10 de desarrollo, los pesos 1/7, 4/7 y 2/7 y los juicios de desarrollo. En `config/experimento.toml` solo cambian `replicas_permutacion` (10 000 → 100 000) y se añade `tolerancia_empates`. El único informe regenerado es el de potencia, por la corrección de H2.
- **C12.** El commit correctivo pasa la suite completa (504 pruebas), el flujo termina sin hallazgos y `--comprobar` solo falla por la falta de autorización. Se verifica en un clon limpio antes de la entrega. La autorización es del asesor.

## Pruebas de aceptación T1 a T8

Todas en `tests/`, sin ejecutar ningún sistema sobre las consultas de prueba: con datos hipotéticos, con la partición de desarrollo o en directorios temporales.

| Prueba | Caso del dictamen | Pruebas |
|---|---|---|
| T1 | H1 no confirmada con H2 p < 0,05: H2 exploratoria; condición formal y filtro de magnitud separados | `test_evaluacion.py`: `test_t1_secuencia_fija_h2_solo_es_confirmatoria_si_h1_se_sostiene`, `test_t1_h1_confirmada_conserva_la_lectura_de_h2_favorable_o_no`, `test_t1_la_compuerta_mantiene_la_tasa_de_error_por_familia_bajo_la_nula` |
| T2 | Enumeración independiente para m = 0, 1, 5, 6 y 9; ceros, empates, exclusiones, b > m; n, b, m y p mínima | `test_evaluacion.py`: `test_t2_la_p_exacta_de_h2_coincide_con_la_enumeracion_completa`, `test_t2_p_minima_y_tolerancia_de_empates`, `test_t2_exclusiones_ceros_y_b_mayor_que_m` |
| T3 | Umbral de H1; Δ negativa significativa; B = 100 000, semilla, error de Monte Carlo, parada no adaptativa | `test_evaluacion.py`: `test_t3_la_regla_separa_las_tres_afirmaciones_de_h1`, `test_t3_la_permutacion_usa_exactamente_b_replicas_y_su_error_de_monte_carlo`; `test_ejecucion_prueba.py`: `test_el_ensayo_produce_todas_las_comparaciones_y_variantes` |
| T4 | Un byte alterado en un insumo, ranking o libro de juicios detiene el paso antes de las métricas | `test_ejecucion_prueba.py`: `test_t4_*` (cuatro pruebas) |
| T5 | Caída parcial; archivos incompletos; segunda corrida | `test_ejecucion_prueba.py`: `test_t5_*` (tres pruebas) |
| T6 | H3 sin errores, sin aciertos y con `no_evaluable`; sin completar cuotas | `test_ejecucion_prueba.py`: `test_t6_*` |
| T7 | Libro sin sistema ni posición, con el orden sorteado; el validador rechaza campos que revelen el origen | `test_ejecucion_prueba.py`: `test_t7_*` |
| T8 | Coherencia de métricas, semillas, pesos, tamaños, umbrales y método | `test_experimento.py`: `test_t8_protocolo_configuracion_y_codigo_dicen_lo_mismo`, `test_la_configuracion_coincide_con_el_protocolo` |

## Sección 10: ajustes al manuscrito

| Ajuste | Texto nuevo | Lugar |
|---|---|---|
| Resumen | «La evaluación se realizará conforme a un protocolo previamente definido», con el desarrollo ejecutado separado de la prueba pendiente | `00_resumen.md` |
| Juicios | «Los juicios de relevancia de prueba se emitirán sin asistencia de modelos; M3 y M4 utilizarán, no obstante, la anotación congelada cuya revisión incluyó asistencia» | Capítulo 7, secciones 7.6.5 y 7.14; capítulo 11, sección 11.6 |
| Interpretación | H1 como utilidad del sistema combinado; ablaciones exploratorias; H3 solo fidelidad a la fórmula, con valoración humana descriptiva | Capítulos 1, 2 y 7 |
| Potencia | 0,087 como estimación aproximada de planificación con diez consultas, no frontera | Capítulo 2, sección 2.5; capítulo 7, sección 7.8; capítulo 11, sección 11.4 |
| Limitaciones | Lista de P5 y declaración de que no se estimó la estabilidad intraevaluador de los juicios de prueba | Capítulo 11, secciones 11.1 y 11.3 |

## Estados que la matriz anterior sobrestimaba

La matriz de respuesta al informe integrado (21 de noviembre) daba por atendidos dos incisos que no lo estaban del todo:

- **7.a, manifiesto de ejecución.** El manifiesto existía, pero se escribía después de los rankings y omitía en silencio los archivos ausentes. Lo corrige R37.
- **8.c, instrumento de H3.** La revisión humana se mencionaba, pero el código no la generaba ni la validaba. Lo corrige R36.

## Lo que se solicita al asesor

1. La revisión del commit correctivo y, si la considera suficiente, la autorización expresa de la apertura del test (C12). Al recibirla se registran la fecha, el commit y la suma del protocolo en `[ejecucion]`, se crea la etiqueta de la autorización, se anota en el registro de custodia y se le envían las huellas.
2. La ratificación de R33 a R39.
3. Las respuestas pendientes de la entrega anterior, sobre las que el dictamen no se pronuncia: la conformidad con la pregunta, las hipótesis y la formalización; la reserva R17 sobre los juicios de desarrollo, y las decisiones D2, D4 y D5 del plan de cierre.
