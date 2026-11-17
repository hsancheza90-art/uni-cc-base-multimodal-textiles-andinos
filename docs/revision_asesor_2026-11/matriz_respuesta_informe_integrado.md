# Matriz de respuesta al informe integrado del 8 de noviembre de 2026

Estado al 13 de noviembre de 2026; el punto 4 se actualizó el 17 de noviembre. Los puntos y los incisos siguen la numeración del informe integrado del asesor, versionado en [`docs/informe_integrado_2026-11-08/`](../informe_integrado_2026-11-08/). El informe tomó como referencia el commit `c313224` (6 de noviembre); esta matriz registra lo ocurrido desde entonces. La columna de evidencia remite a archivos del repositorio y, entre paréntesis, al commit que los introdujo.

Los estados se interpretan así:

- **Atendido:** el inciso se cumplió y puede verificarse en el repositorio.
- **Parcial:** hay avance verificable y se indica lo que falta.
- **Por ratificar:** la acción está hecha o decidida por el investigador y requiere la conformidad del asesor.
- **Pendiente:** no se ha iniciado; se indica de qué depende.

Una advertencia general, en el sentido del punto 1 del informe: los estados «Atendido» describen procedimientos ejecutados y verificados por pruebas de software. Ninguno equivale a un resultado científico. A la fecha no se ha ejecutado ningún sistema sobre las consultas de prueba y ninguna hipótesis ha sido contrastada.

## Resumen

| Punto | Tema | Estado | Lo que falta |
|---|---|---|---|
| 1 | Estado real e inventario | Atendido | Mantenerlo al día en cada entrega |
| 2 | Pregunta, contribución y alcance | Por ratificar | Conformidad con la redacción propuesta y conciliación con los objetivos del primer avance |
| 3 | Protocolo experimental | Por ratificar | Aprobación de la versión 0.6.1 y de las decisiones R01 a R04 y R10 |
| 4 | Estabilidad de la anotación y v2.1 | Atendido | Anotación v2.1 congelada el 17 de noviembre (R21 a R23) |
| 5 | Modelos y ajuste de desarrollo | Parcial | Rankings de M3 y de su control, M4 conectado, selección de pesos |
| 6 | Juicios de relevancia | Parcial, con una reserva de validez | Decisión sobre la rúbrica; ampliación del pool; juicios de prueba |
| 7 | Congelación y ejecución confirmatoria | Pendiente | Depende de los puntos 3 a 6 |
| 8 | Resultados, ablaciones e interpretación | Pendiente | Depende del punto 7; el código de métricas e inferencia está implementado y probado |
| 9 | Formalización matemática | Parcial | Trasladar la formalización propuesta al capítulo 5 |
| 10 | Revisión bibliográfica | Parcial | Búsquedas en Scopus y Web of Science; lectura de Brownlow et al. (2015) |
| 11 | Redacción del manuscrito | Parcial | Solo están redactados los apartados que no dependen de resultados |
| 12 | Reproducibilidad y entrega | Atendido en lo verificable hoy | Manifiesto de ejecución y etiqueta final |
| 13 | Orden de trabajo | En la tercera etapa | Etapas tercera a sexta |

## 1. Estado real del proyecto

| Inciso | Acción | Evidencia | Estado |
|---|---|---|---|
| Inventario de versiones, grupos, modelos, consultas y pendientes | Se redactó un inventario referido a archivos y commits, que separa lo verificado por software de lo que constituye evidencia científica | [`inventario_estado.md`](inventario_estado.md) | Atendido |
| No reabrir la recolección ni alterar corpus congelados | Desde el 6 de noviembre no se modificó ningún archivo de recolección ni de la serie v1; el consolidado v2.0 conserva su etiqueta | `corpus-met-cma-aic-v2.0` (`0143686`); `git log c313224.. -- src/collectors data/metadata/v1_congelado` no devuelve commits | Atendido |

## 2. Pregunta científica, contribución y alcance

| Inciso | Acción | Evidencia | Estado |
|---|---|---|---|
| a) Pregunta contrastable | Pregunta redactada en términos de sistemas, tarea, métrica y juicio | [`problema_hipotesis_alcance.md`](problema_hipotesis_alcance.md), sección 2; protocolo, sección 1 | Por ratificar |
| b) Tres hipótesis ligadas a resultados observables | H1, H2 y H3 con su variable, su comparador, su regla de decisión y los tres veredictos posibles. H3 se declara como fidelidad algorítmica | Mismo documento, secciones 4 y 5 | Por ratificar |
| c) Contribución de método y evidencia | Tres contribuciones: formalización de la macroestructura observable, descriptor con secuencias, adyacencias y máscaras, y evaluación controlada | Mismo documento, sección 6 | Por ratificar |
| d) Población y comparabilidad | Población: colección digital elegible de tres museos. M3 y M4 se declaran asistidos por anotación; una mejora no respalda extracción automática ni generalización | Mismo documento, sección 7; protocolo, secciones 1 y 4 | Atendido |
| e) Coherencia entre pregunta, objetivos, hipótesis, variables, código y capítulos | Tabla de correspondencia hipótesis–prueba–artefacto. Los objetivos se redactaron conforme al protocolo y quedan por conciliar con los del primer avance, que no se modifica | Mismo documento, secciones 3 y 5 | Parcial |

## 3. Protocolo experimental

| Inciso | Acción | Evidencia | Estado |
|---|---|---|---|
| a) Completar, aprobar y registrar el protocolo | El protocolo está en la versión 0.6.1, propuesta. Su historial registra cada cambio con fecha y motivo. No tiene todavía fecha ni commit de aprobación | `docs/protocolo_experimental_v2.md` («Historial»); `docs/registro_decisiones.md` (`14c0887`, `ba18dc3`) | Por ratificar |
| a) Decisiones propuestas: aptitud, galería, umbral y verificación | D2, D4 y D5 siguen como propuestas; D7 quedó decidida | `docs/plan_cierre_tesis.md` («Decisiones del 12 de noviembre») | Por ratificar |
| b) T3 primaria, T1 exploratoria, seis sistemas | Sin cambios. M1 no participa en T1 y M3 se declara asistido por anotación | Protocolo, secciones 3 y 4 | Atendido |
| c) Métrica primaria, umbral, intervalo y reglas para casos límite | nDCG@10, Δ = 0,03, IC 95 % por bootstrap pareado de 10 000 réplicas, regla para consultas sin relevantes y para pares `no_evaluable` | Protocolo, secciones 6 y 7; `src/experimento/evaluacion.py` (`4dff235`) | Atendido |
| c) Decisión de H1 por bootstrap y permutación como sensibilidad | **Difiere de lo indicado.** La decisión R01 invierte los papeles: H1 y H2 se deciden por permutación pareada y el bootstrap se reserva para el intervalo. El motivo es que, con pocos temas, el bootstrap usado como prueba no mantiene el error de tipo I nominal (Urbano, Lima y Hanjalic, 2019). Si el asesor prefiere la regla original, se restituye antes del test: el código calcula ambas | `docs/registro_decisiones.md`, R01 | Por ratificar |
| d) Partición por grupos, consultas fijadas y diseño transductivo | 44 grupos de desarrollo y 102 de prueba; 10 y 30 consultas T3 sorteadas con semilla antes de calcular rankings. La regla de reemplazo se aplicó dos veces, a T3-P27 y a T3-P06 (R22), por correcciones de la anotación y sin consultar ningún ranking | `data/metadata/particiones_v2.csv`, `consultas_t3_v2.csv`; `outputs/reports/experimento_v2_snapshot.md` (`0143686`, `d0bce67`) | Atendido |
| e) Registrar toda modificación antes del test | Las modificaciones posteriores al 6 de noviembre están en el registro de decisiones (R01 a R17), con motivo, fuente y archivos afectados | `docs/registro_decisiones.md` | Atendido |
| f) Condiciones que detienen la prueba | El protocolo enumera cinco condiciones y una comprobación automática de fugas (grupos cruzados y autocandidatos). Falta añadir, de forma expresa, la ausencia de manifiesto de ejecución como condición de suspensión | Protocolo, sección 9 | Parcial |

## 4. Estabilidad de la anotación y versión estructural v2.1

| Inciso | Acción | Evidencia | Estado |
|---|---|---|---|
| a) Re-anotación ciega del lote 1 | Completada el 12 de noviembre: 30 de 30 piezas, en otro orden, con el intervalo mínimo de siete días cumplido en todas | `data/metadata/anotacion_v2_reanotacion.xlsx` (`d0bce67`) | Atendido |
| b) Informe de estabilidad | Kappa por atributo cuando es estimable, Jaccard y kappa por etiqueta en los campos múltiples, similitud de edición de la palabra de bandas, n y exclusiones por atributo. Se añadió una tabla de observabilidad. Se denomina acuerdo intra-anotador | `outputs/reports/anotacion_acuerdo_v2.md` (`ba18dc3`, `d0bce67`) | Atendido |
| b) Atributos con estabilidad baja | `centro` (κ = 0,49) y las etiquetas `amarillo`, `ocre` y `abstracto`. La observabilidad es inestable: en `composicion` y `simetria`, seis de las treinta piezas cambiaron entre «se observa» y «no se observa» | Mismo informe, tablas «Acuerdo por atributo» y «Observabilidad por atributo» | Atendido (hallazgo informado) |
| c) Avisos por `desconocido` sin marca de revisión | Se cambió la regla en lugar de editar las piezas: el estado `desconocido` del atributo basta para registrar la duda (R15) | `docs/protocolo_anotacion_v2.md` («Regla de los treinta segundos») | Atendido |
| c) Observaciones de duda, criterio o vocabulario y registro de adjudicaciones | Criterios escritos: qué cuenta como banda (R12, con la aclaración de R21), la frontera entre simetría traslacional y repetición modular (R16) y los criterios C1 a C4. Las observaciones se clasificaron: 108 piezas de los lotes 2 a 5 entraron a revisión y quedan fuera 46 dudas sobre atributos que M3 no usa y 16 huecos de vocabulario, que se declaran. Las 108 se verificaron (66 confirmadas, 42 corregidas) y el registro de adjudicaciones lista 173 valores corregidos con su motivo. La revisión partió de propuestas automáticas verificadas por el anotador (R20) | `outputs/reports/anotacion_v2_revision_criterios.md`; `docs/registro_decisiones.md`, R18 a R21 | Atendido |
| d) Atributos demasiado ambiguos para sostener la hipótesis | `composicion` (κ = 0,84) y `secuencia_bandas` (17 de 24 palabras idénticas; similitud media 0,80) sostienen H2 en el lote medido. La reserva es la observabilidad: el bloque que M3 compara depende de una frontera que no fue estable. `centro` se mantiene y su estabilidad baja se declara (R19) | Informe de acuerdo; `docs/especificacion_m3.md`, sección 5; R19 | Atendido, con la reserva declarada |
| d) No retocar etiquetas según un ranking | En el lote 1 prevalece la re-anotación completa, por regla general y sin selección por pieza (R14). Ninguna etiqueta se modificó tras calcular un ranking de M3: esos rankings no existen todavía | `config/anotacion.toml`, `[reanotacion]`; `src/anotacion/aplicar_anotaciones_v2.py` | Atendido |
| e) Congelar las 150 anotaciones como v2.1 | Congelada el 17 de noviembre, con la revisión de criterios sin pendientes y las ocho anotaciones desplazadas trasladadas. Copia con sumas SHA-256 de ella y de sus insumos; el flujo falla si la anotación cambia después | `data/metadata/v2_1_congelado/`; `outputs/reports/anotacion_v2_1_congelada.md`; R20 a R23 | Atendido |

## 5. Modelos, control sin orden y ajuste de desarrollo

| Inciso | Acción | Evidencia | Estado |
|---|---|---|---|
| a) Baselines y condiciones de ejecución | M0, M1 y M2 sin cambios desde el 6 de noviembre. Parámetros en configuración; checkpoint, suma de los pesos y versiones en el manifiesto de M2; los empates se resuelven por `id_global` | `config/modelos.toml`; `data/metadata/m2_openclip_manifiesto_v2.json` (`c3d186a`, `75a281e`) | Atendido |
| b) Rankings de M3 sobre la anotación v2.1 | Rankings de desarrollo de las diez consultas sobre la anotación congelada, con los pesos iniciales. Un par sin evidencia estructural va al final, sin score | `data/processed/experimento_v2_rankings_desarrollo.csv`; R24 | Atendido en desarrollo |
| c) M3-sin-orden | Rankings de desarrollo con los mismos pesos. Coincide con M3 en el ranking completo de 8 de 10 consultas, porque solo 53 de 150 piezas tienen palabra de bandas: H2 tendrá poca potencia si se evalúa sobre todas las consultas. Se pide al asesor decidir antes del test si H2 se restringe a las consultas con bandas | R24 | Atendido en desarrollo; decisión pendiente |
| d) M4 como fusión tardía | Funciones de normalización por consulta, reparto de pesos sin evidencia estructural, contribuciones, rejilla y regla de selección, con pruebas de propiedades. Falta conectarlas a los rankings y al pool | `src/modelos/m4_fusion.py`; `tests/test_m4.py` (`9f520f5`) | Parcial |
| e) Ajuste de pesos solo en desarrollo | Los juicios de desarrollo iniciales están completos. La rejilla y la regla de selección están fijadas en el código; los pesos no se han elegido | Protocolo, sección 4; `rejilla` y `elegir` en `m4_fusion.py` | Pendiente |
| f) Pruebas de propiedades | Invariancia a la reversión, simetría y cota, coherencia de máscaras, `aabb` frente a `abab`, reconstrucción numérica, intervención y determinismo | `tests/test_sistemas.py`, `tests/test_m4.py`, `tests/test_evaluacion.py` | Atendido |

## 6. Juicios humanos de relevancia

| Inciso | Acción | Evidencia | Estado |
|---|---|---|---|
| a) Los 345 pares de desarrollo | Juzgados los 345 el 12 de noviembre, con evaluador y fecha. Ninguno `no_evaluable`. Distribución: 131 de grado 0, 174 de grado 1, 28 de grado 2 y 12 de grado 3 | `data/metadata/juicios_desarrollo_v2.csv`; `outputs/reports/experimento_v2_juicios_desarrollo.md` (`408362c`) | Atendido, con la reserva que sigue |
| a) Justificación visible en los grados 2 y 3 | **Incumplido en parte:** de los 40 juicios de grado 2 o 3, solo 5 llevan justificación | Workbook de juicios | Parcial |
| a) Juicios basados en criterios estructurales | **Reserva de validez.** Los juicios no se alinean con la composición registrada en la anotación: entre los 85 pares cuya consulta y candidato tienen la misma composición, el 14 % recibió grado 2 o 3; entre los 253 de composición distinta, el 11 %. En las tres consultas de bandas, ninguno de los 39 candidatos con bandas alcanzó el grado 2. Caben dos lecturas, no excluyentes: que la rúbrica se aplicó con un criterio más global que el estructural, o que la composición anotada no capta lo que el ojo reconoce como «misma organización». El investigador decidió conservar estos juicios y someter la cuestión al asesor (R17). Se detalla en [`amenazas_validez.md`](amenazas_validez.md), sección 2 | Cálculo exploratorio con `src/experimento/evaluacion.py` sobre los archivos versionados | Por ratificar |
| b) Ampliar el pool con M3, su control y M4 | Ampliado con M3 y M3-sin-orden: 66 pares nuevos (411 en total), con los 345 juzgados y la muestra al azar intactos. Falta juzgar los 66 y, después, sumar M4 | `src/experimento/juicios.py`; R24 | Parcial |
| b) Origen de los candidatos fuera de la vista de quien juzga | El origen está en un archivo aparte, que el evaluador no abre; el workbook no lo contiene | `data/processed/experimento_v2_pool_desarrollo.csv` | Atendido |
| c) Juicio ciego | Orden aleatorio con semilla; sin sistema, posición, score ni anotación en el workbook. Ningún juicio se deriva de un modelo | Protocolo, sección 6; `src/experimento/juicios.py` (`1eeb9c4`) | Atendido |
| d) Pool ciego de prueba | No iniciado | — | Pendiente (depende del punto 7.a) |
| e) Segundo juicio parcial | Propuesto al asesor en la carta del 6 de noviembre (5 consultas de prueba). Si no se dispone de otra persona, el manuscrito declarará evaluador único | [`README.md`](README.md), solicitud 3 | Por ratificar |
| f) Cobertura, no evaluables y consultas sin relevantes | En desarrollo, el top 10 de M0, M1 y M2 está juzgado por completo; no hay pares no evaluables ni consultas sin candidatos de grado 1. En cinco de las diez consultas ningún candidato alcanzó el grado 2, lo que afecta a las métricas binarizadas. La convención para no juzgados y la sensibilidad sin aportes únicos están implementadas | `proporcion_juzgada` y `sin_aportes_unicos` en `src/experimento/evaluacion.py` | Atendido en desarrollo |

## 7. Congelación del experimento y ejecución confirmatoria

| Inciso | Acción | Evidencia | Estado |
|---|---|---|---|
| a) Manifiesto de ejecución | No iniciado. Existen sus insumos: manifiesto de imágenes con SHA-256, manifiesto de M2, particiones y consultas versionadas | `data/metadata/m2_openclip_manifiesto_v2.json` | Pendiente |
| b) Comprobaciones automáticas previas | El flujo ya verifica identificadores únicos, grupos sin cruzar, consultas que no son sus propios candidatos y coincidencia entre protocolo y configuración. Falta reunirlas en una comprobación previa al test | `tests/test_experimento.py`; `outputs/reports/experimento_v2_snapshot.md` | Parcial |
| c) Sellado de modelos y qrels | No iniciado | — | Pendiente |
| d) Evaluación confirmatoria única | No ejecutada. Ningún sistema se ha ejecutado sobre las consultas de prueba | — | Pendiente |

## 8. Resultados estadísticos, ablaciones e interpretación

No hay resultados de prueba. Lo que existe es el instrumento y una estimación previa de la precisión alcanzable.

| Inciso | Acción | Evidencia | Estado |
|---|---|---|---|
| a) y b) Inferencia para H1 y H2 | Diferencias pareadas, permutación, t pareada, intervalo por bootstrap y regla de decisión con tres veredictos, verificados con datos sintéticos | `src/experimento/evaluacion.py`; `tests/test_evaluacion.py` (`4dff235`) | Instrumento listo |
| c) H3 | Reconstrucción e intervención verificadas por pruebas de propiedades en M3 y en la fusión | `tests/test_sistemas.py`, `tests/test_m4.py` | Instrumento listo |
| d) Ablaciones y control negativo | Definidos en el protocolo; la variante por posiciones recíprocas está implementada | Protocolo, sección 7; `posiciones_reciprocas` | Pendiente |
| e) Potencia | Estimación previa con las diez consultas de desarrollo y los tres sistemas disponibles: la desviación estándar de las diferencias pareadas de nDCG@10 está entre 0,20 y 0,28, de modo que, con 30 consultas y potencia de 80 %, el efecto mínimo detectable se sitúa entre 0,10 y 0,14. Es entre tres y cinco veces el umbral práctico de 0,03. El cálculo definitivo, para M4 frente a M2, se hará antes del test (R04) | [`amenazas_validez.md`](amenazas_validez.md), sección 5 | Parcial |
| f) Análisis de errores y esfuerzo humano | No iniciado. El tiempo de anotación por pieza no se midió y así se declara | `docs/protocolo_anotacion_v2.md` («Limitaciones que se declaran») | Pendiente |

## 9. Formalización matemática

| Inciso | Acción | Evidencia | Estado |
|---|---|---|---|
| a) Definiciones inequívocas con correspondencia a datos | Objeto, registro, fotografía, grupo, galería, anotación, alfabeto, palabra, laguna, tramo, adyacencia, equivalencia por reversión y máscara, cada uno con el archivo y la columna que lo materializa | [`formalizacion_matematica.md`](formalizacion_matematica.md), secciones 1 a 4 | Por ratificar |
| b) Separar elegibilidad de estructura | La aptitud fotográfica define la población; la estructura se define sobre ella con estados explícitos de no observación. Cada sistema opera en su propio espacio y la fusión solo combina scores normalizados | Mismo documento, secciones 1 y 7 | Por ratificar |
| c) Propiedades realmente usadas | Canonización, rango, simetría, identidad, tratamiento de faltantes y costo, con su demostración o su prueba. Se muestra con un contraejemplo que la desigualdad triangular no se cumple con máscaras variables | Mismo documento, secciones 5 y 6 | Por ratificar |
| d) Burnside y Pólya como antecedentes | Se usan para contar clases de palabras y para cuantificar qué distingue el orden más allá del histograma. Se separan teoremas conocidos, decisiones de diseño, propiedades verificadas y resultados empíricos | Mismo documento, secciones 4 y 8 | Por ratificar |
| Capítulo matemático corregido | El capítulo del manuscrito no se ha reescrito; la formalización propuesta es su base | — | Pendiente |

## 10. Revisión bibliográfica y brecha

| Inciso | Acción | Evidencia | Estado |
|---|---|---|---|
| a) Presentarla como mapeo parcial | Se declara revisión de alcance con cobertura parcial; no se presenta como revisión sistemática | `docs/revision_bibliografica_2026-11/01_protocolo_busqueda.md` (`b8a80b9`) | Atendido |
| b) Búsquedas documentadas en bases indexadas | Se conservaron cadenas, fechas y criterios de la búsqueda realizada. Scopus y Web of Science no se han consultado; no se simula su cobertura | Mismo directorio; `04_sintesis_y_brecha.md`, sección 7 | Parcial |
| c) Lectura crítica de los antecedentes cercanos | 30 fichas de lectura. Ngo et al. (2021) y Helmer y Ngo (2015) se leyeron y obligan a no presentar la tesis como la primera en recuperar textiles por estructura. Brownlow et al. (2015) se localizó y no se pudo leer por falta de acceso (R05); se informa aquí al asesor | `fichas/`; `05_pendientes_texto_completo.md` | Parcial |
| d) Matriz de antecedentes | Matriz por estudio y cuadro que distingue estructura a escala de hilos, estructura visible anotada y clasificación | `03_matriz_antecedentes.csv`; `04_sintesis_y_brecha.md`, sección 2 | Atendido |
| e) Brecha formulada como comparación | La brecha se enuncia como «no se encontró, en una búsqueda de alcance parcial» y como la comparación que la tesis pone a prueba. Falta verificar las cifras marcadas como no verificadas y completar las referencias | `04_sintesis_y_brecha.md`, sección 3; `referencias.bib` | Parcial |

## 11. Redacción del manuscrito

| Inciso | Acción | Evidencia | Estado |
|---|---|---|---|
| a) Problema, objetivos, hipótesis y contribución | Redactados conforme al protocolo vigente | [`problema_hipotesis_alcance.md`](problema_hipotesis_alcance.md) | Por ratificar |
| b) Unidades del corpus | El inventario distingue decisiones curatoriales, registros utilizables, grupos y piezas del núcleo, e indica qué cuenta cada cifra | [`inventario_estado.md`](inventario_estado.md), sección 1 | Atendido |
| c) Decisiones para reproducir el método | Documentadas en los protocolos, la especificación y el registro de decisiones. Faltan los pesos y el manifiesto | `docs/` | Parcial |
| d) Resultados | No hay resultados que redactar. Ninguna tabla se ha completado con valores simulados | — | Pendiente |
| e) Amenazas a la validez | Redactadas por tipo de validez, con la mitigación aplicada y la limitación que subsiste | [`amenazas_validez.md`](amenazas_validez.md) | Por ratificar |
| f) Conclusiones por objetivo | Depende de los resultados. La regla de decisión ya prevé los veredictos «sostenida», «no sostenida» y «evidencia insuficiente» | `decidir` en `src/experimento/evaluacion.py` | Pendiente |

## 12. Reproducibilidad, entrega y mejoras diferidas

| Inciso | Acción | Evidencia | Estado |
|---|---|---|---|
| a) Verificación en un entorno limpio | Cada commit publicado se verificó en un clon limpio: el flujo de 23 pasos termina sin hallazgos, las pruebas pasan (429 en el commit de esta matriz) y el árbol queda sin cambios | `README.md` («Regenerar y verificar») | Atendido |
| b) Artefactos de evaluación | Versionados: código, consultas, particiones, juicios y rankings de desarrollo, configuración y sumas. Faltan las métricas por consulta, los intervalos y el manifiesto, que dependen del test. Las imágenes no versionadas se obtienen con los comandos de descarga documentados | `data/`, `config/`, `README.md` | Parcial |
| c) Correspondencia entre tablas y archivos | Cada sistema tiene su módulo y cada informe su generador. La correspondencia con las tablas de la tesis se hará al redactar los resultados | `docs/protocolo_experimental_v2.md`, sección 12 | Parcial |
| d) Diferir mejoras | Se mantienen diferidos SW03, SW06, SW07, SW09, SW11 y SW12, la validación externa de la aptitud, el cuarto museo y los modelos adicionales | [`matriz_respuesta_auditoria.md`](matriz_respuesta_auditoria.md) | Atendido |
| e) Prioridad del objetivo académico | Desde el 6 de noviembre, el trabajo de software se limitó a lo que el experimento exige: métricas, fusión y acuerdo | `git log c313224..` | Atendido |

## 13. Orden de trabajo

| Etapa | Situación al 13 de noviembre |
|---|---|
| Primera: protocolo y juicios de desarrollo | Juicios completos, con la reserva del punto 6. Protocolo documentado y sin aprobar |
| Segunda: re-anotación y v2.1 | Re-anotación y estabilidad completas. Criterios R12 y R16 escritos. Falta revisar los lotes 2 a 5 y congelar |
| Tercera: M3, M4, ampliación del pool y pesos | Funciones implementadas y probadas; sin rankings |
| Cuarta a sexta | No iniciadas |

Las condiciones mínimas que el informe fija antes del test no se cumplen todavía: falta la aprobación del protocolo, la congelación de la anotación, la selección de pesos y el pool de prueba. En consecuencia, el test no se abrirá por cumplir la fecha del 22 de noviembre, tal como indica el propio informe.

## Lo que se solicita al asesor

1. La aprobación del protocolo 0.6.1 o sus observaciones, y en particular su conformidad con R01 (permutación para decidir, bootstrap para el intervalo).
2. Su criterio sobre la reserva de validez de los juicios de desarrollo (punto 6.a): aceptarlos como están, declarando la limitación, o repetir el juicio con la rúbrica aclarada antes de ajustar los pesos.
3. Su conformidad con la redacción de la pregunta, las hipótesis y el alcance (punto 2) y con la formalización propuesta (punto 9).
4. Su indicación sobre Brownlow et al. (2015): si dispone del texto o si acepta que la brecha se formule con la salvedad declarada.
5. Su decisión sobre el segundo juicio parcial (punto 6.e).
6. Su decisión sobre el alcance de H2 (punto 5.c): mantenerla sobre las 30 consultas de prueba, declarando su baja potencia, o restringirla a las consultas con palabra de bandas (R24).
