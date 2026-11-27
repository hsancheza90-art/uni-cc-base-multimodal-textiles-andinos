# Registro de decisiones

Decisiones del investigador sobre el diseño, la evaluación y la redacción de la tesis, a partir del 12 de noviembre de 2026. Las anteriores están en `docs/plan_cierre_tesis.md` (D1 a D7 y «Seguimiento») y en el «Historial» de `docs/protocolo_experimental_v2.md`. Cada entrada indica qué se decidió, por qué, con qué respaldo, qué archivos cambia y qué queda por hacer. Una decisión no se edita: si cambia, se añade una entrada nueva que la sustituye y se anota en la anterior.

Estados: **Decidida** (vigente); **Por ratificar** (decidida por el investigador, espera al asesor porque cambia el protocolo); **Sustituida por Rnn**. Cuando una decisión posterior resuelve un pendiente o modifica una entrada, se añade al final de esa entrada una nota en cursiva con la fecha y la decisión que la resuelve.

**Códigos de la auditoría interna.** R11 a R13 y R16 citan hallazgos de la auditoría interna del 12 de noviembre (documento fuera del repositorio) con sus códigos originales: H1 a H7 (hallazgos sobre la anotación), T1 a T7 (hallazgos sobre la tesis) y D1 a D8 (observaciones de forma). No deben confundirse con las hipótesis H1 a H3 del protocolo ni con las decisiones D1 a D7 del plan de cierre. Cada entrada describe el hallazgo en su propio texto, de modo que puede leerse sin el documento de la auditoría.

## Resumen

| ID | Fecha | Decisión | Estado |
|---|---|---|---|
| R01 | 2026-11-12 | H1 y H2 se deciden con permutación pareada; el bootstrap queda para el intervalo | Decidida; ratificada en el dictamen del 21 de noviembre; precisada por R34 y R35 |
| R02 | 2026-11-12 | Kappa ≥ 0,6 se usa como señal de revisión, no como aprobado | Por ratificar |
| R03 | 2026-11-12 | Se añade la ablación de M4 por posiciones recíprocas | Por ratificar |
| R04 | 2026-11-12 | El efecto mínimo detectable se calcula antes del test | Por ratificar |
| R05 | 2026-11-12 | No se esperan los textos sin acceso; la brecha se redacta con lo leído | Decidida |
| R06 | 2026-11-12 | La cifra de CLIP en relaciones se cita de la página 4 de Yuksekgonul et al. | Decidida |
| R07 | 2026-11-12 | El ajuste de pesos se describe como «pocas consultas etiquetadas», sin número | Decidida |
| R08 | 2026-11-12 | Las referencias se completan en el `.bib` y el estilo se fija al final | Decidida |
| R09 | 2026-11-12 | Este registro es el lugar único de las decisiones nuevas | Decidida |
| R10 | 2026-11-12 | En la fusión por posiciones, los pares sin evidencia estructural van al final del ranking de M3 | Por ratificar |
| R11 | 2026-11-12 | Se atienden las observaciones de forma de la auditoría interna del 12 de noviembre y se agrega la observabilidad al informe de acuerdo | Decidida |
| R12 | 2026-11-12 | Definición operativa de banda: franja completa, sin cenefas, retículas ni paneles | Decidida |
| R13 | 2026-11-12 | Fusión de `repeticion_modular` en `traslacional` | Descartada; sustituida por R16 |
| R14 | 2026-11-12 | En el lote re-anotado prevalece la re-anotación | Decidida |
| R15 | 2026-11-12 | Regla de los treinta segundos: el `desconocido` del atributo basta | Decidida |
| R16 | 2026-11-12 | Simetría: se mantienen `traslacional` y `repeticion_modular`, separadas por la dimensión de la repetición | Decidida |
| R17 | 2026-11-13 | Los juicios de desarrollo se conservan como se emitieron; la reserva sobre la rúbrica se declara y se somete al asesor | Por ratificar; modificada por R25 |
| R18 | 2026-11-16 | Los lotes 2 a 5 se revisan con R12 y R16 en un workbook aparte; las correcciones prevalecen al exportar | Decidida |
| R19 | 2026-11-16 | `centro` se mantiene en la anotación y en M3 pese a su estabilidad baja | Decidida |
| R20 | 2026-11-16 | La revisión de R18 parte de propuestas automáticas que el anotador verifica una por una | Decidida |
| R21 | 2026-11-17 | Cierre de la revisión de criterios: 108 piezas verificadas, aclaraciones de R12 y del eje, C1 a C4 vigentes | Decidida |
| R22 | 2026-11-17 | Reubicación de las ocho anotaciones desplazadas, observaciones en prosa y selección de la revisión congelada | Decidida |
| R23 | 2026-11-17 | La anotación estructural v2.1 queda congelada; los sistemas leen la copia congelada | Decidida |
| R24 | 2026-11-17 | Rankings de desarrollo de M3 y M3-sin-orden; el pool crece con sus candidatos y la muestra al azar queda fija | Decidida |
| R25 | 2026-11-19 | Los juicios de desarrollo se revisan con la segunda opinión ciega de un modelo de visión general; el evaluador firma cada grado | Decidida |
| R26 | 2026-11-19 | Se mide la sensibilidad de M3 a la revisión asistida de la anotación, solo en desarrollo | Decidida |
| R27 | 2026-11-21 | H2 sobre 30 consultas con análisis secundario en las 9 con bandas; juicios de prueba sin asistencia; 30 consultas; evaluador único | Decidida; contexto modificado por R30 |
| R28 | 2026-11-21 | Pesos de M4 elegidos una sola vez (1/7, 4/7, 2/7); M4 y M4-RRF en los rankings de desarrollo | Decidida |
| R29 | 2026-11-21 | Efecto mínimo detectable fijado antes del test: H1 0,087; H2 0,026 | Decidida |
| R30 | 2026-11-21 | El test espera la aprobación del asesor; se corrigen las cifras de R21; M0, M1 y M3 quedan con sus parámetros de partida | Decidida |
| R31 | 2026-11-21 | Las condiciones B3 a B7 pasan a ser reglas de la congelación y del flujo; la proposición 5.6 se fija en una prueba automática | Decidida |
| R32 | 2026-11-21 | Definición de la ablación de M3 por bloques, de la robustez por completitud y de la ejecución de T1; el test queda listo para un solo comando | Decidida; ejecución modificada por R37 |
| R33 | 2026-11-23 | H1 y H2 se contrastan en secuencia fija: H2 es confirmatoria solo si H1 se sostiene; H1 no aísla la estructura | Decidida; ratificada el 23 de noviembre (R40) |
| R34 | 2026-11-23 | H1 con 100 000 réplicas fijas, error de Monte Carlo y tres afirmaciones separadas; el efecto mínimo detectable es una estimación de planificación | Decidida; ratificada el 23 de noviembre (R40) |
| R35 | 2026-11-23 | H2 con p exacta por enumeración de los cambios de signo y tolerancia de empates de 1e-12; sin efecto mínimo detectable por aproximación normal | Decidida; ratificada el 23 de noviembre (R40) |
| R36 | 2026-11-23 | H3 pasa a ser la fidelidad computacional de M4; la revisión humana de las explicaciones es descriptiva | Decidida; ratificada el 23 de noviembre (R40) |
| R37 | 2026-11-23 | Estados de la corrida, manifiesto antes de los rankings, gestión de fallos y custodia sin firma personal | Decidida; ratificada el 23 de noviembre (R40) |
| R38 | 2026-11-23 | No se rejuzga una muestra de prueba; la estabilidad intraevaluador no se mide y se declara | Decidida; ratificada el 23 de noviembre (R40) |
| R39 | 2026-11-23 | Archivo de auditoría de los juicios asistidos, privado, con su huella y su descripción en el repositorio | Decidida; ratificada el 23 de noviembre (R40) |
| R40 | 2026-11-23 | El asesor autoriza la apertura del test sobre el commit 2b01f0e; se registra la autorización y se abre la corrida | Decidida |
| R41 | 2026-11-24 | Criterio de lectura de la revisión de H3 (tercios), doble juicio parcial no realizado y entrega del informe de Seminario II | Decidida |
| R42 | 2026-11-26 | Levantamiento del informe del asesor del 25-11 (C01–C03); referencias en IEEE con una lista única; error de anotación de AIC:85278 declarado sin corregir la copia congelada | Decidida |

## R01. Prueba inferencial de H1 y H2

- **Decisión.** H1 y H2 se deciden con una prueba de permutación pareada por cambio de signo, bilateral, con 10 000 réplicas, semilla fija y nivel 0,05. Se informa la t de Student pareada como comprobación. El bootstrap pareado se conserva solo para el IC 95 %.
- **Antes.** La regla de H1 dependía de que el límite inferior del IC 95 % por bootstrap fuese mayor que cero, y la permutación era un análisis de sensibilidad.
- **Motivo.** Con pocos temas, la t pareada y la permutación mantienen el error de tipo I nominal, y el bootstrap usado como prueba tiende a valores p pequeños. El estudio citado trata pruebas de hipótesis y no cuestiona los intervalos.
- **Fuente.** Urbano, Lima y Hanjalic (2019), p. 2 y 7. Ficha F20.
- **Archivos.** `docs/protocolo_experimental_v2.md`, secciones 1 y 7 (versión 0.6).
- **Pendiente.** Añadir `alfa` y la prueba elegida a `[metricas]` de `config/experimento.toml` y a la prueba de coherencia, al implementar la evaluación. *(21 de noviembre: `alfa`, `replicas_permutacion` y `semilla_permutacion` añadidos a `[metricas]` en R32.)* *(23 de noviembre: el asesor dio su conformidad en el dictamen del 21 de noviembre. R34 eleva las réplicas de H1 a 100 000 y R35 sustituye la permutación por muestreo en H2 por la enumeración exacta.)*

## R02. Uso del umbral de acuerdo

- **Decisión.** Se mantiene kappa ≥ 0,6 como señal de revisión por atributo, no como criterio de aprobación. Se declara como criterio operativo de estudio piloto. Un atributo por debajo se revisa en la guía antes de congelar la anotación v2.1. Si es `composicion`, se mantiene y se declara como limitación de H2. `secuencia_bandas` se informa con coincidencia exacta y similitud de edición, sin umbral.
- **Motivo.** No hay un umbral aceptado. La referencia consultada propone 0,8 si hay que fijar uno y desaconseja que un umbral sea requisito; pide informar el método, el coeficiente y la tabla de acuerdos. La regla se fija antes de calcular el acuerdo, para no decidir sobre los atributos a la vista de los resultados.
- **Fuente.** Artstein y Poesio (2008), pp. 576 y 591 de la revista (pp. 22 y 37 del PDF; ficha F07); Landis y Koch (1977) para la escala.
- **Archivos.** `docs/protocolo_anotacion_v2.md` (medición del acuerdo); `docs/protocolo_experimental_v2.md`, sección 10.
- **Pendiente.** El informe generado `outputs/reports/anotacion_acuerdo_v2.md` todavía dice «umbral de acuerdo aceptable». Cambiar el texto en `src/anotacion/acuerdo.py` y el comentario de `[acuerdo]` en `config/anotacion.toml`, y regenerar con el flujo. Añadir la tabla de acuerdos por atributo si el informe no la da.

## R03. Ablación de M4 por posiciones recíprocas

- **Decisión.** Se añade como ablación exploratoria una variante de M4 que suma 1 / (60 + posición) sobre los rankings de M0, M2 y M3. Sus 10 primeros candidatos entran al pool de desarrollo y de prueba.
- **Motivo.** No tiene pesos, así que muestra cuánto del resultado de M4 depende del ajuste con 10 consultas de desarrollo.
- **Fuente.** Cormack, Clarke y Büttcher (2009), ficha F22; Bruch, Gai e Ingber (2023), ficha F04.
- **Archivos.** `docs/protocolo_experimental_v2.md`, secciones 6, 7 y 10.
- **Abierto.** El trato de los pares sin evidencia estructural (últimas posiciones del ranking de M3, por `id_global`) figura en el protocolo como propuesta: confirmarlo antes de implementar. No interviene en H3. *Resuelto en R10.*
- **Pendiente.** Constante k = 60 en `config/modelos.toml`; implementación junto con M4; inclusión en el pool. Si sus candidatos añaden demasiados pares para el calendario, se descarta antes de cerrar el pool de prueba y se registra aquí. *(21 de noviembre: implementada e incluida en el pool de desarrollo en R28.)*

## R04. Efecto mínimo detectable

- **Decisión.** Antes de abrir el test se calcula el efecto mínimo detectable con 30 consultas y potencia de 80 %: (z₀,₉₇₅ + z₀,₈) · DE(Δ) / √30 ≈ 0,51 · DE(Δ), con DE(Δ) estimada en desarrollo y su rango de imprecisión. Si supera 0,03, el estudio se declara sin potencia para ese umbral y se informa el intervalo. No se calcula potencia a posteriori.
- **Motivo.** La potencia se planifica antes del experimento; calcularla después con el efecto observado no se recomienda.
- **Fuente.** Card et al. (2020), sección 3 y nota 2. Ficha F21.
- **Archivos.** `docs/protocolo_experimental_v2.md`, sección 7.
- **Pendiente.** El cálculo, cuando existan los juicios de desarrollo. *(21 de noviembre: calculado en R29.)*

## R05. Textos sin acceso

- **Decisión.** No se espera a Brownlow et al. (2015) ni a Phillips (2018), que no tienen copia de acceso abierto. La brecha y el estado del arte se redactan con los 30 documentos leídos.
- **Motivo.** Calendario de cierre.
- **Consecuencia que se declara.** El informe integrado del asesor (8 de noviembre, punto 10.c) pide priorizar a Brownlow et al. El manuscrito debe decir que ese texto se localizó y no se pudo leer, y formular la brecha como «en la búsqueda realizada». No se afirma que no existan antecedentes andinos equivalentes.
- **Archivos.** Ninguno. `docs/revision_bibliografica_2026-11/05_pendientes_texto_completo.md` se conserva como registro de lo que no se leyó.

## R06. Cifra de CLIP en pruebas de relaciones

- **Decisión.** Se cita el dato de la página 4 de Yuksekgonul et al. (2023): 56 % en relaciones espaciales, con el azar en 50 %.
- **Motivo.** El artículo da además 63 % en el cuerpo y 0,59 en una tabla del apéndice, que son agregaciones distintas. El dato elegido no admite dos lecturas.
- **Fuente.** Ficha F01.

## R07. Número de consultas para ajustar pesos

- **Decisión.** Al citar a Bruch, Gai e Ingber (2023) se escribe «pocas consultas etiquetadas», sin dar un número. La defensa de las 10 consultas de desarrollo se apoya en la ablación de R03.
- **Fuente.** Ficha F04, p. 1 y 2.

## R08. Referencias y estilo

- **Decisión.** Las referencias se mantienen en `docs/revision_bibliografica_2026-11/referencias.bib`. El año o la sede que falten se completan desde la página editorial de cada artículo. El estilo de cita se fija cuando el asesor lo confirme.

## R09. Registro de decisiones

- **Decisión.** Toda decisión nueva se anota aquí antes de tocar el protocolo, la configuración o el código, y el commit que la aplica la cita por su identificador.

## R10. Pares sin evidencia estructural en la fusión por posiciones

- **Decisión.** En la variante de M4 por posiciones recíprocas, los candidatos sin evidencia estructural ocupan las últimas posiciones del ranking de M3, ordenados por `id_global`, como ya establece la especificación de M3 para su propio ranking. Confirma lo que R03 dejó abierto.
- **Motivo.** Es la misma regla que usa M3: un par sin evidencia no recibe similitud máxima. No añade un criterio nuevo.
- **Archivos.** `src/modelos/m4_fusion.py` (funciones de fusión y sus pruebas de propiedades en `tests/test_m4.py`). El protocolo 0.6 ya lo describe en la sección 7.
- **Pendiente.** Conectar M4 a los rankings y al pool cuando exista la anotación v2.1; constante k = 60 y rejilla de pesos en `config/modelos.toml`. *(21 de noviembre: hecho en R28.)*

## R11. Observaciones de forma de la auditoría interna del 12 de noviembre

- **Decisión.** Se aplican las correcciones de forma y de registro de la auditoría interna del 12 de noviembre, sin cambiar el diseño del experimento ni ningún valor de la anotación:
  - D1 y D2: el calendario del protocolo pasa al 12 de noviembre y D7 sale de las decisiones por ratificar (ya estaba decidida).
  - D3: el informe de acuerdo y `config/anotacion.toml` presentan kappa < 0,6 como señal de revisión, no como criterio de aprobación (aplica el pendiente de R02).
  - D4: la especificación de M3 aclara que el reparto de M4 solo usa si hay evidencia estructural, no el valor de la cobertura (coincide con `src/modelos/m4_fusion.py`).
  - D5 y D6: la ficha F07 registra la propuesta de 0,8 de Artstein y Poesio, y el archivo de pendientes bibliográficos registra R05.
  - H4: el informe de acuerdo agrega, por atributo, si el atributo se pudo observar en cada pasada, con su acuerdo y su kappa.
  - H7, T5 y T6: el protocolo de anotación declara que el tiempo por pieza no se midió, que `lana` no implica oveja y que el vocabulario de técnica es incompleto.
  - T2, T3 y T7: la especificación de M3 declara que el eje es fotográfico, que la reversión descarta la orientación de la prenda y que la estructura no es independiente de la técnica ni de la tradición.
- **Fuente.** Auditoría interna del 12 de noviembre (`investigacion_local/auditorias/auditoria_2026-11-12.md`, fuera del repositorio).
- **Archivos.** `src/anotacion/acuerdo.py`, `tests/test_anotacion_v2.py`, `config/anotacion.toml`, `docs/protocolo_experimental_v2.md`, `docs/protocolo_anotacion_v2.md`, `docs/especificacion_m3.md` y dos archivos de `docs/revision_bibliografica_2026-11/`.
- **Pendiente.** Las observaciones que exigen una decisión curatorial (H1, H3, H5, H6, T1, T4, la adjudicación del lote 1 y el análisis por cultura de T7) y la comunicación al asesor de R05 (D8) quedan para el investigador.

## R12. Qué cuenta como banda

- **Decisión.** Una banda es una franja que atraviesa toda la superficie visible en sentido perpendicular al eje de lectura y está delimitada por un cambio de color o de diseño. No son bandas las cenefas perimetrales (se registran en `borde`), las filas o columnas de una retícula ni los paneles (se registran en `composicion`).
- **Motivo.** En la re-anotación del lote 1, la decisión más inestable fue si una pieza tiene bandas: cuatro piezas pasaron de `ausente` a una secuencia de dos a seis bandas. La guía definía los tipos de banda, pero no qué cuenta como banda. Es la variable sobre la que descansa H2.
- **Fuente.** Auditoría interna del 12 de noviembre, hallazgos H3 y T1.
- **Archivos.** `docs/protocolo_anotacion_v2.md` («Bandas») y la guía de los workbooks (`src/anotacion/workbook.py`).
- **Pendiente.** Revisar con esta definición `eje_bandas` y `secuencia_bandas` en las piezas de los lotes 2 a 5 cuya palabra incluya cenefas, filas de retícula o paneles, antes de congelar la anotación v2.1. El lote 1 se rige por R14.

## R13. Simetría: `repeticion_modular` y `traslacional`

- **Propuesta.** Recodificar `repeticion_modular` como `traslacional`, porque las dos describen la traslación de un módulo y la repetición ya tiene su propio atributo.
- **Por qué no se aplicó.** Se presentó con un alcance de tres piezas (las confundidas entre pasadas), pero `repeticion_modular` es el valor más usado: 65 de las 150 piezas de la primera anotación y 6 de las 30 de la re-anotación. Además, es una categoría de la tesis (Cuadro 6.4). Con la fusión, `traslacional` reuniría 98 de 150 piezas y el atributo apenas distinguiría piezas en M3. Queda pendiente de confirmación del investigador.
- **Fuente.** Auditoría interna del 12 de noviembre, hallazgos H5 y T4.

## R14. Adjudicación del lote re-anotado

- **Decisión.** Cuando la primera anotación y la re-anotación del lote 1 difieren, prevalece la re-anotación, hecha con más experiencia. La primera anotación solo sirve para medir la estabilidad.
- **Implementación.** `[reanotacion] prevalece = true` en `config/anotacion.toml`. Al exportar `data/metadata/anotaciones_v2.csv`, los valores de cada pieza re-anotada reemplazan a los de la primera pasada; la pieza conserva su lote y su orden. Ninguno de los dos workbooks se modifica y el informe de acuerdo sigue comparando las dos pasadas.
- **Consecuencia que se declara.** El lote 1 de la versión v2.1 refleja la segunda lectura y los lotes 2 a 5 la primera, con las aclaraciones de R12 aplicadas a los atributos afectados.
- **Archivos.** `src/anotacion/aplicar_anotaciones_v2.py`, `config/anotacion.toml`, `tests/test_anotacion_v2.py`.

## R15. Regla de los treinta segundos

- **Decisión.** El estado `desconocido` en el atributo basta para registrar una duda; `revisar` queda para las piezas que piden una segunda mirada completa.
- **Motivo.** La regla anterior exigía marcar `revisar` y no se aplicó así en ninguna de las dos pasadas (38 y 12 piezas). Cambiar la regla no edita ninguna pieza.
- **Archivos.** `docs/protocolo_anotacion_v2.md`, la guía de los workbooks y `src/anotacion/aplicar_anotaciones_v2.py`, que deja de emitir ese aviso.

## R16. Simetría: traslación frente a repetición modular

- **Decisión.** Se mantienen las dos categorías de la tesis (Cuadro 6.4) y se separan por la dimensión de la repetición. `traslacional`: un motivo se desplaza a lo largo de una sola dirección y forma una franja o friso continuo. `repeticion_modular`: un módulo con contorno propio (celda, cuadro o panel) se repite como unidad, en dos dimensiones o como piezas separadas (retícula, damero, tablero). Si una pieza tiene las dos, se anota la que organiza la mayor parte de la superficie visible.
- **Sustituye a.** R13, que proponía fusionarlas y se descartó porque `repeticion_modular` reúne 71 valores entre las dos pasadas y la fusión dejaría el atributo casi sin capacidad de distinguir piezas.
- **Motivo.** La auditoría interna (H5, T4) encontró tres piezas confundidas entre las dos categorías: la guía no las separaba. La distinción entre repetición en una dimensión (friso) y en dos (teselado) es la que usa el análisis de simetría de patrones.
- **Archivos.** `docs/protocolo_anotacion_v2.md` («Simetría: traslación y repetición modular») y la guía de los workbooks.
- **Pendiente.** Revisar `simetria` con esta definición en los lotes 2 a 5, en las piezas marcadas `traslacional` o `repeticion_modular`, antes de congelar la anotación v2.1. El lote 1 se rige por R14.

## R17. Juicios de desarrollo y aplicación de la rúbrica

- **Decisión.** Los 345 juicios de desarrollo se conservan tal como se emitieron el 12 de noviembre. El trabajo continúa con ellos y la reserva sobre la aplicación de la rúbrica se declara y se somete al asesor. No se corrige ningún juicio a la vista de la anotación o de un ranking.
- **Hallazgo que la motiva.** Los juicios no se alinean con la composición registrada en la anotación: entre los 85 pares con la misma composición, el 14 % recibió grado 2 o 3; entre los 253 de composición distinta, el 11 %. En las tres consultas de bandas, ninguno de los 39 candidatos con bandas alcanzó el grado 2. De los 40 juicios de grado 2 o 3, solo 5 llevan justificación.
- **Alternativa no adoptada.** Repetir el juicio de desarrollo con la rúbrica aclarada y ejemplos de cada grado. Queda abierta: si el asesor la indica, debe hacerse antes de ajustar los pesos de M4 y de construir el pool de prueba.
- **Consecuencia que se declara.** Mientras no se resuelva, no puede afirmarse que los juicios de desarrollo midan similitud estructural, y los pesos que se elijan con ellos heredan esa reserva.
- **Archivos.** `docs/revision_asesor_2026-11/amenazas_validez.md` (A2) y `matriz_respuesta_informe_integrado.md` (punto 6.a). Ningún dato cambia.
- *(19 de noviembre: modificada por R25. Los juicios no se conservaron como se emitieron: se revisaron con una segunda opinión ciega y el evaluador firmó cada grado. Los grados iniciales se conservan fuera del repositorio.)*

## R18. Revisión de criterios en los lotes 2 a 5

- **Decisión.** Antes de congelar la anotación v2.1, el anotador vuelve a mirar las piezas de los lotes 2 a 5 afectadas por los criterios escritos después de anotarlas, y confirma o corrige cada una. Entran a la revisión, por reglas automáticas:
  - las 52 piezas con palabra de bandas, todas y no solo las de composición distinta de bandas (R12);
  - las 85 con simetría `traslacional` o `repeticion_modular` (R16);
  - las 32 cuyas observaciones marcan una duda o un criterio sobre un atributo que usa M3;
  - las 22 cuyas observaciones piden verificar que la imagen corresponde al registro.
  En total, 108 de las 120 piezas.
- **Qué queda fuera.** Las dudas que solo tocan atributos que M3 no usa (`motivo_principal`, color, técnica, tipo de objeto o de superficie; 46 piezas) y los huecos de vocabulario (16 piezas). No se resuelven en la versión 2.1 y se declaran como limitación.
- **Procedimiento.** Las decisiones se registran en `data/metadata/anotacion_v2_revision_criterios.xlsx`, con revisor, fecha y, si hay corrección, su motivo. El workbook de la primera anotación no se modifica. Al exportar `data/metadata/anotaciones_v2.csv`, los valores corregidos reemplazan a los anteriores, y `outputs/reports/anotacion_v2_revision_criterios.md` conserva el registro de adjudicaciones (pieza, atributo, valor anterior, valor nuevo y motivo). La revisión se hace solo sobre las imágenes, sin consultar rankings ni juicios.
- **Motivo.** El informe integrado del asesor (punto 4, incisos c y d) pide resolver las ambigüedades con criterios escritos, conservar un registro de adjudicaciones y no retocar etiquetas según un ranking. Los rankings de M3 no existen todavía.
- **Consecuencia que se declara.** La versión 2.1 combina tres lecturas: la re-anotación en el lote 1 (R14), la primera anotación en los lotes 2 a 5 y, sobre esta, las correcciones de esta revisión.
- **Archivos.** `src/anotacion/revision_criterios.py`, `src/anotacion/aplicar_anotaciones_v2.py`, `config/anotacion.toml` (`[revision_criterios]`), `tests/test_revision_criterios.py`, `docs/protocolo_anotacion_v2.md`.
- **Pendiente.** La revisión de las 108 piezas. Una pieza cuya imagen no corresponda al registro debe re-anotarse antes de congelar. *(17 de noviembre: la revisión se cerró en R21; quedan las ocho anotaciones desplazadas.)*

## R19. El atributo `centro`

- **Decisión.** `centro` se mantiene en la anotación y en el descriptor M3, aunque su acuerdo intra-anotador en el lote 1 fue κ = 0,49. Su peso se fija, como los demás, solo con datos de desarrollo.
- **Motivo.** Retirar un bloque del descriptor a la vista de un único lote de 30 piezas sería una decisión tomada con poca evidencia. La estabilidad baja se declara entre las amenazas a la validez.
- **Archivos.** Ninguno: confirma el estado vigente. `centro` no es corregible en la revisión de R18.

## R20. Propuestas automáticas en la revisión de criterios

- **Decisión.** La revisión de R18 es asistida. Para cada una de las 108 piezas se generó una propuesta (confirmar o corregir, con los valores, el motivo, el criterio aplicado y un grado de confianza) a partir de la imagen, la anotación vigente y los criterios escritos. El anotador verifica cada propuesta frente a la imagen, la corrige si hace falta y la firma.
- **Cómo se generaron.** Con un modelo de visión y lenguaje, en nueve lotes de doce piezas, el 16 de noviembre. Cada lote recibió solo las imágenes, la anotación vigente, las observaciones del anotador y el texto de los criterios. No recibió rankings, juicios de relevancia ni resultados de ningún sistema. Las propuestas se validaron contra el vocabulario antes de versionarse.
- **Garantías.** Las propuestas se guardan en `data/metadata/anotacion_v2_revision_criterios_propuestas.csv` y se precargan en el workbook firmadas `revisor = auto`. Una fila firmada así no se aplica a la anotación ni cuenta como decidida: la versión 2.1 no puede congelarse mientras quede alguna. El workbook conserva la propuesta en columnas de contexto, y el informe cuenta cuántas decisiones verificadas coinciden con ella y cuántas la modifican.
- **Criterios provisionales usados en las propuestas.** Además de R12 y R16, cuatro criterios que el investigador debe aprobar o cambiar al verificar: C1, las esquinas y fragmentos con decoración perimetral son `borde`, y `composicion_libre` solo si no se distingue organización; C2, una tira con recuadros sucesivos de contorno propio es `paneles`, sin palabra de bandas; C3, una figura única es `campo_central` si un fondo la enmarca y `composicion_libre` si la pieza es la propia figura; C4, varias piezas sin relación en una foto llevan sus atributos estructurales como `no_observable`.
- **Consecuencia que se declara.** La versión 2.1 incluirá correcciones propuestas por un procedimiento automático y verificadas por el anotador. El manuscrito debe describirlo así, con el número de propuestas aceptadas y modificadas.
- **Hallazgo durante la revisión.** En ocho piezas, la anotación guardada describe la imagen de otro registro. Seis forman un ciclo (AIC:85282, AIC:85310, CMA:155505, AIC:223218, AIC:85388 y MET:307933) y dos están intercambiadas entre sí (MET:316978 y MET:316341). Se comprobó con las imágenes y con los números de inventario: las imágenes corresponden a sus registros y son las anotaciones las que están desplazadas. Sus propuestas van como `no_coincide` y sin correcciones. La reasignación es una decisión del investigador y está pendiente.
- **Archivos.** `src/anotacion/revision_criterios.py`, `config/anotacion.toml` (`[revision_criterios] propuestas`), `tests/test_revision_criterios.py`.

## R21. Cierre de la revisión de criterios

- **Decisión.** El anotador verificó y firmó las 108 piezas de R18 el 16 de noviembre: confirmó 66 y corrigió 42. Las 66 confirmaciones coinciden con la propuesta automática. Las 42 correcciones la modifican: el anotador revisó los siete atributos de cada pieza, no solo los que la propuesta tocaba. Al exportar se aplican 173 valores corregidos.
- **Aclaraciones de criterio (17 de noviembre).** Al revisar la coherencia del workbook aparecieron tres lecturas distintas de la guía. El investigador las resolvió así:
  - *Alcance de R12.* Una franja que cruza toda la pieza es banda aunque la composición dominante sea campo, paneles o retícula. El eje se registra siempre que haya palabra de bandas. Siete piezas tenían secuencia y eje `ausente`; recuperan el eje `horizontal`.
  - *Convención del eje.* El eje es el de la fotografía: `horizontal` si las franjas cruzan la foto de lado a lado. Tres piezas marcadas `vertical` con franjas horizontales pasan a `horizontal`, y en AIC:6114 vuelven eje y secuencia `ausente`.
  - *Tiras únicas.* Una tira que el anotador lee como paneles o retícula, sin franjas aparte, no tiene palabra de bandas: eje y secuencia `ausente` (ocho piezas).
- **Correcciones de forma (17 de noviembre).** Las hizo el investigador al cerrar la revisión, sin cambiar ninguna decisión. Se normalizaron los códigos mal escritos (`geometrica` en motivos, `antropoformo`, separadores) y se restauró el motivo vigente en tres piezas en que la columna se había arrastrado en Excel (MET:308024, AIC:3016 y MET:316973). Cinco secuencias escritas en la columna equivocada se leyeron de nuevo sobre la foto (AIC:85520, MET:307941, CMA:163708, MET:308068 y AIC:152928). En MET:312669, el investigador sustituyó su secuencia por la que se lee en la foto: `geometrica > figurativa > figurativa > geometrica`. Los textos de `motivo` se redactaron de nuevo, con la misma asistencia de R20, para que describan el valor final firmado: en las 42 correcciones repetían el texto de la propuesta, y varios contradecían la decisión.
- **C1 a C4.** Los criterios provisionales de R20 quedan vigentes: el investigador firmó las decisiones que los aplican.
- **Efectos que se declaran.** En el núcleo, la composición `bandas` pasa de 48 a 35 piezas y `paneles` de 24 a 40, y la palabra de bandas queda en 53 piezas (antes 66). `borde` pasa de `no` a `si` en 21 piezas. De las 40 consultas T3, cuatro cambian de estrato: `bandas` 13 → 10, `campo_central` 7 → 6, `paneles` 7 → 11. Todas siguen teniendo composición observable, así que la regla de reemplazo del protocolo no se aplica y el sorteo no se repite.
- **Prueba.** `tests/test_flujo.py` incluye ahora el workbook de revisión entre los insumos y compara su informe. Hasta este cierre, todas las filas estaban firmadas `auto` y la omisión no tenía efecto.
- **Identidad de las piezas no revisadas.** Las 12 piezas de los lotes 2 a 5 que no entraron a la revisión se compararon con sus imágenes el 17 de noviembre: en las doce, la observación del anotador describe la imagen del registro, y en las dos que muestran etiqueta de inventario (MET:307852 y MET:307679) el número coincide.
- **Pendiente antes de congelar la v2.1.** Las ocho anotaciones desplazadas (R20) se re-anotan en el workbook de anotación, decisión del investigador del 17 de noviembre. Hasta entonces, sus filas quedan `confirmar` con `identidad_imagen = no_coincide`, y la anotación exportada sigue describiendo la imagen de otro registro. *(Atendido en R22: se trasladaron y revisaron.)*
- **Archivos.** `data/metadata/anotacion_v2_revision_criterios.xlsx`, `data/metadata/anotaciones_v2.csv`, `outputs/reports/anotacion_v2_revision_criterios.md`, `outputs/reports/experimento_v2_snapshot.md`, `tests/test_flujo.py`, `docs/protocolo_anotacion_v2.md`.
- *(21 de noviembre: las cifras de coincidencia con la propuesta se corrigen en R30. De las 108 decisiones, 58 coinciden con la propuesta y 50 la modifican; de las 66 confirmaciones, 8 son las anotaciones desplazadas, cuya propuesta no confirmaba la imagen.)*

## R22. Anotaciones desplazadas, observaciones en prosa y selección congelada

- **Anotaciones desplazadas.** Las ocho anotaciones de R20 no se descartan: cada una describía bien la imagen de otro registro. Se trasladaron a la fila del registro cuya imagen describen y se revisaron sobre esa imagen con los criterios vigentes (R12, R16, C1 a C4). Quedan con `estado_anotacion = corregido` y fecha 17 de noviembre. Cambios respecto de la anotación trasladada:
  - MET:307933, esquina de un paño con greca escalonada: `composicion` pasa de `composicion_libre` a `borde` (C1), sin palabra de bandas, y los motivos quedan geométricos con motivo principal `escalonados`, como había corregido el investigador sobre la imagen.
  - AIC:85282, banda con dos hileras de personajes separadas por una línea: simetría `traslacional`, porque cada hilera es un friso (R16).
  - AIC:223218, cuatro fragmentos sin relación en una foto: `composicion` pasa a `no_observable` (C4) y se añade `antropomorfo` a los motivos por la figura con tocado.
  - MET:316978, gorro en cuadrantes: `composicion` pasa de `reticula` a `paneles`, como lo había leído el investigador.
  - AIC:85310, CMA:155505, AIC:85388 y MET:316341: la anotación trasladada se conserva.
  En el workbook de revisión, las ocho filas quedan `confirmar` con `identidad_imagen = coincide`, firmadas `revisor = auto` hasta que el investigador las verifique (R20).
- **Consulta T3-P06.** La consulta de prueba T3-P06 se había sorteado sobre AIC:223218 con la anotación desplazada, que era la del medallón (`campo_central`). Con la anotación correcta, su composición no es observable, y se aplicó la regla de reemplazo del protocolo: la sustituye AIC:5371, siguiente pieza elegible del estrato `AIC | campo_central` en el orden de la semilla. Ninguna consulta de prueba tiene rankings ni juicios.
- **Observaciones en prosa.** A pedido del investigador, las 142 observaciones restantes de la primera anotación se reescribieron el 17 de noviembre, con asistencia, para que describan solo lo que se ve en la imagen. Las dudas se expresan como posibilidad («posiblemente…»). Se retiraron las etiquetas (`OBS`, `DUDA`, `CRITERIO`, `VOCAB`, `REC`), las referencias a otras piezas, las propuestas sobre metadatos y las explicaciones de cómo se llenó cada campo. No cambia ningún valor anotado. El texto anterior queda en el historial del repositorio (commit `f40dd6e`). Las 30 observaciones de la re-anotación, escritas por el investigador en prosa, se revisaron después (ver «Segunda pasada de textos»).
- **Selección congelada.** La selección de R18 se calculaba con las etiquetas de las observaciones. Para que reescribirlas no cambie una revisión cerrada, la selección se congeló en `data/metadata/anotacion_v2_revision_criterios_seleccion.csv` (`python -m src.anotacion.revision_criterios --congelar`), calculada sobre el commit `f40dd6e`: 108 de 120 piezas, con sus motivos y las marcas de duda que no tocan a M3. Con la selección congelada, el flujo regenera las mismas salidas que antes.
- **Efectos que se declaran.** El informe de validación ya no cuenta etiquetas `DUDA`, `CRITERIO` o `VOCAB` en los lotes 2 a 5, porque las observaciones ya no las usan; los huecos de vocabulario y las dudas ajenas a M3 siguen contados en el informe de la revisión, desde la selección congelada.
- **Segunda pasada de textos.** También se pasaron a prosa, con el mismo criterio, las 30 observaciones de la re-anotación (correcciones de redacción y de erratas; se retiró la nota sobre la técnica corregida) y los 42 motivos de las correcciones del workbook de revisión, que ya no citan los códigos de las reglas. La regla aplicada a cada pieza sigue en `motivos_revision` de la selección congelada. Las columnas `propuesta*` no se modifican: registran lo que dijo la propuesta automática (R20).
- **Firma.** El investigador verificó y firmó las ocho filas el 17 de noviembre. La revisión queda sin pendientes y la anotación v2.1 puede congelarse.
- **Archivos.** `data/metadata/anotacion_v2.xlsx`, `data/metadata/anotacion_v2_revision_criterios.xlsx`, `data/metadata/anotacion_v2_revision_criterios_seleccion.csv`, `data/metadata/consultas_t3_v2.csv`, `config/anotacion.toml`, `src/anotacion/revision_criterios.py`, `src/anotacion/aplicar_anotaciones_v2.py`, `tests/test_revision_criterios.py`, `tests/test_flujo.py`.

## R23. Congelación de la anotación estructural v2.1

- **Decisión.** La anotación del núcleo (150 piezas) queda congelada como versión 2.1 el 17 de noviembre. Reúne la primera anotación, la re-anotación del lote 1 (R14), las correcciones de la revisión de criterios de los lotes 2 a 5 (R18 a R21) y las ocho anotaciones trasladadas (R22).
- **Condiciones verificadas.** La revisión de criterios no tiene pendientes, imágenes que no coinciden ni errores; el comando de congelación se niega en caso contrario. Los workbooks validan sin errores y el flujo termina sin hallazgos.
- **Cómo queda.** La copia está en `data/metadata/v2_1_congelado/anotaciones_v2_1.csv`, con su suma SHA-256 y las de sus insumos (los tres workbooks, la selección congelada y la configuración) en `sha256.txt`. Se escribió con `python -m src.anotacion.congelacion_v21 --congelar`, que no sobrescribe una copia existente.
- **Garantía.** Un paso del flujo compara en cada ejecución la anotación exportada con la copia congelada y comprueba la suma de la copia. Si un workbook cambia después de congelar, el flujo termina con código 1. Una nueva versión de la anotación requiere una decisión registrada y una carpeta nueva.
- **Uso.** M3, su control sin orden y la fusión M4 se calculan sobre la copia congelada. Su composición en el núcleo: 35 piezas de bandas, 41 de paneles, 31 de retícula, 22 de campo central, 10 de composición libre, 6 de borde, 4 desconocidas y 1 no observable (`outputs/reports/anotacion_v2_1_congelada.md`).
- **Archivos.** `src/anotacion/congelacion_v21.py`, `src/flujo.py`, `config/anotacion.toml` (`[congelacion]`), `config/corpus.toml`, `tests/test_congelacion_v21.py`, `tests/test_flujo.py`.
- **Siguiente.** Rankings de desarrollo de M3 y de M3 sin orden, ampliación del pool de juicios de desarrollo y conexión de M4.

## R24. Rankings de desarrollo de M3 y ampliación del pool

- **Decisión.** M3 y M3-sin-orden se ejecutan sobre las diez consultas T3 de desarrollo, con la anotación v2.1 congelada y los pesos iniciales de `[m3.pesos]` (todos iguales a 1; no se ajustan antes de la respuesta del asesor sobre R17). El score es 1 − D; un candidato sin ningún bloque observable en común con la consulta no tiene score y va al final, por identificador (especificación de M3, sección 3). Las consultas de prueba no se ejecutan.
- **Pool.** Los diez primeros de M3 y de M3-sin-orden entran al pool de juicios de desarrollo, que pasa de 345 a 411 pares (66 nuevos, de 4 a 8 por consulta). Los 345 pares juzgados se conservan, y 36 de ellos ganan como origen M3 o M3-sin-orden sin volver a juzgarse.
- **Muestra al azar fija.** Hasta ahora, los diez candidatos al azar de cada consulta se elegían entre los que ningún sistema proponía, de modo que agregar un sistema podía cambiar la muestra. Desde esta decisión se eligen entre los que no proponen M0, M1 y M2 (`sistemas_muestra_azar` en `config/experimento.toml`), los sistemas del pool inicial. La muestra resultante es la misma de antes: los mismos 100 pares.
- **Hallazgo para H2.** En desarrollo, M3 y M3-sin-orden producen el mismo ranking completo en 8 de las 10 consultas y el mismo top 10 en 9 (intersección media de 9,8 de 10). Solo 53 de las 150 piezas tienen palabra de bandas, y el orden solo puede pesar cuando la consulta y el candidato la tienen. Si la proporción se repite en prueba, la diferencia pareada de H2 será cero en la mayoría de las consultas y la prueba tendrá poca potencia: el veredicto más probable sería «evidencia insuficiente» por construcción.
- **Decisión pendiente, del investigador y del asesor, antes del test.** Mantener H2 sobre las 30 consultas de prueba, declarando esta limitación, o definirla sobre el subconjunto de consultas con palabra de bandas, lo que cambia el protocolo. No se toma a la vista de ningún resultado de prueba; los rankings de desarrollo no se han mostrado al evaluador. *(21 de noviembre: resuelta en R27.)*
- **Pendiente del evaluador.** Juzgar los 66 pares nuevos en `data/metadata/juicios_desarrollo_v2.xlsx`, con la misma rúbrica y sin abrir rankings ni el pool.
- **Archivos.** `src/experimento/rankings.py`, `src/experimento/juicios.py`, `config/experimento.toml`, `config/corpus.toml`, `data/processed/experimento_v2_rankings_desarrollo.csv`, `data/processed/experimento_v2_pool_desarrollo.csv`, `data/metadata/juicios_desarrollo_v2.xlsx`, `data/metadata/juicios_desarrollo_v2.csv`, `tests/test_experimento.py`.

## R25. Revisión de los juicios de desarrollo con una segunda opinión ciega

- **Método.** El 2026-11-19 se revisaron los 411 juicios de desarrollo con la segunda opinión de un modelo de visión general (Claude, de Anthropic; no es CLIP ni ninguno de los sistemas evaluados). El modelo solo vio las dos imágenes de cada par y la rúbrica: no tuvo acceso a los grados del evaluador, los rankings, los sistemas ni la anotación. El evaluador revisó cada par con esa opinión a la vista y firmó el grado y la justificación finales. Los juicios vigentes de desarrollo son, por tanto, juicios humanos asistidos por un modelo, y casi siempre coinciden con la segunda opinión. Antes de la revisión, el acuerdo entre el evaluador y la segunda opinión era bajo: kappa ponderado lineal de 0,16.
- **Alcance.** La revisión se aplica solo a los juicios de desarrollo, que se usan para ajustar pesos y estimar la potencia. Los grados iniciales se conservan fuera del repositorio. Antes de los juicios de prueba, el investigador y el asesor decidirán si se repite la asistencia.
- **Archivos.** `data/metadata/juicios_desarrollo_v2.xlsx` y `data/metadata/juicios_desarrollo_v2.csv`.
- *(21 de noviembre: R27 decide que los juicios de prueba se hacen sin asistencia. 23 de noviembre: el dictamen del asesor acepta los juicios de desarrollo con reserva y pide un archivo de auditoría, que fija R39.)*

## R26. Sensibilidad de M3 a la revisión asistida de la anotación

- **Decisión.** Se mide, solo en desarrollo, cuánto cambian los rankings de M3 y de M3-sin-orden si se usa la anotación anterior a la revisión de criterios en lugar de la v2.1. Es un análisis exploratorio que sostiene la declaración de la asistencia (R20) en el capítulo 4. No decide ninguna hipótesis ni modifica la anotación congelada.
- **Anotación previa.** Es la exportación de `data/metadata/anotaciones_v2.csv` en el commit `d0bce67`, que ya incluye la re-anotación del lote 1 (R14) y todavía no la revisión. Las ocho anotaciones desplazadas (R20) se trasladan a la fila de la imagen que describen, sin corregirlas, para que la comparación mida la revisión y no ese error. El traslado se comprobó atributo por atributo: las cuatro anotaciones que R22 conservó coinciden en los nueve atributos con su origen.
- **Resultado.** La revisión cambió al menos un atributo de M3 en 46 de 150 piezas. En las diez consultas de desarrollo, el top 10 de M3 comparte entre 4 y 9 piezas entre versiones, y la correlación de Spearman va de 0,56 a 0,91. La revisión no es neutra para el descriptor.
- **Lo que no se concluye.** El nDCG no se usa como evidencia de qué versión es mejor: el pool se construyó con la v2.1, y la revisión de la anotación (R20) y la de los juicios (R25) usaron asistencia de la misma familia de modelos.
- **Archivos.** `src/experimento/sensibilidad_anotacion.py` (con `--crear` lee el historial de git, fuera del flujo), `data/metadata/anotacion_v2_previa_revision.csv`, `outputs/reports/experimento_v2_sensibilidad_anotacion.md`, `src/flujo.py`, `tests/test_sensibilidad_anotacion.py`, `tests/test_flujo.py`, `docs/manuscrito/capitulo_4_datos_y_anotacion.md` (sección 4.10.1).

## R27. Condiciones del test: alcance de H2, juicios de prueba y evaluador único

- **Contexto.** El investigador decidió ejecutar el test antes de entregar el informe al asesor, de modo que las decisiones que se iban a someter a este (solicitudes 6 y 7 de la matriz) las toma el investigador y se registran aquí antes de ejecutar ninguna consulta de prueba.
- **Alcance de H2.** Se mantiene sobre las 30 consultas de prueba, como fija el protocolo. Se añade un análisis secundario, fijado ahora, sobre las consultas de prueba cuya pieza tiene palabra de bandas (9 de 30). Motivo matemático: si la palabra de la consulta es vacía (`ausente`) o no observable, la distancia entre palabras y la del control coinciden para todo candidato (ambas valen 0 si el candidato tampoco tiene bandas y 1 si las tiene, o el bloque se enmascara) y el bloque de adyacencias no es observable; M3 y su control dan, por tanto, el mismo score a todos los candidatos y la diferencia de H2 es cero en esas 21 consultas. En desarrollo ocurrió en 8 de las 10 consultas, las dos restantes son las únicas con palabra. El análisis secundario no sustituye a la regla de H2: se informa junto a ella.
- **Alternativas descartadas.** Completar la anotación congelada (añadir palabras a piezas marcadas `ausente` o sin observar) o redactar con un modelo el texto de las fichas para fortalecer H2: se harían a la vista del resultado de desarrollo y alterarían datos observados o la entrada de M0. Ampliar el núcleo con piezas nuevas con bandas sería legítimo con una regla previa, pero no cambia que esas 21 consultas den diferencia cero y queda como trabajo futuro.
- **Juicios de prueba.** Sin asistencia: el evaluador juzga solo y a ciegas, y su grado es el único que se usa. Responde a la pregunta de investigación (juicios humanos independientes de los modelos) y al argumento de Soboroff (2025).
- **Número de consultas.** Se mantienen las 30 consultas de prueba (unos 1600 pares, unas 13 horas de juicio).
- **Evaluador único.** No hay segundo evaluador disponible. El doble juicio parcial se prepara para cuando lo haya; mientras tanto, el evaluador único se declara como limitación principal.
- **Archivos.** `docs/protocolo_experimental_v2.md` (versión 0.6.3).
- *(21 de noviembre: el contexto cambia en R30. El investigador decidió esperar la aprobación del protocolo antes de abrir el test. Las decisiones de fondo de esta entrada se mantienen.)*
- *(23 de noviembre: el asesor dio su conformidad. Por R33, H2 es confirmatoria solo si H1 se sostiene, y el análisis de las consultas con bandas es descriptivo y no puede confirmar H2.)*

## R28. Pesos de M4 y conexión de M4 a los rankings de desarrollo

- **Decisión.** Los pesos de M4 se eligen una sola vez con la regla del protocolo (rejilla {0; 0,25; 0,5; 0,75; 1} normalizada, 91 combinaciones; mayor nDCG@10 medio en desarrollo; en empate, la más cercana a pesos iguales y luego la primera en orden lexicográfico descendente) y con los 411 juicios de desarrollo vigentes el 21 de noviembre. La regla eligió M0 = 1/7, M2 = 4/7 y M3 = 2/7, que quedan fijos en `[m4.pesos]` de `config/modelos.toml`.
- **Por qué una sola vez.** Los candidatos de M4 dependen de los pesos, y los nuevos candidatos todavía no estaban juzgados. Volver a elegir tras juzgarlos convertiría la selección en un ciclo. Los juicios de los candidatos nuevos sirven para estimar el efecto mínimo detectable de M4 frente a M2, no para cambiar los pesos. El paso del flujo `pesos_m4` informa si la regla, con los juicios vigentes, sigue eligiendo los mismos pesos, sin modificarlos.
- **Conexión.** M4 y su variante por posiciones recíprocas (M4-RRF, k = 60, decisión R03) se calculan en los rankings de desarrollo sobre los scores de M0, M2 y M3 redondeados como se versionan, de modo que M4 se reproduce desde el CSV; una prueba lo comprueba. Las consultas de prueba no se ejecutan.
- **Pool.** Los 10 primeros de M4 y de M4-RRF agregan 8 pares al pool de desarrollo (411 → 419). La muestra al azar no cambia (R24). Los 8 pares nuevos los juzga el evaluador sin asistencia (R27).
- **Ceguera.** El informe de la selección contiene el rendimiento de los sistemas en desarrollo y el evaluador no lo abre.
- **Archivos.** `src/experimento/pesos_m4.py`, `src/experimento/rankings.py`, `src/flujo.py`, `config/modelos.toml`, `config/corpus.toml`, `data/processed/experimento_v2_rankings_desarrollo.csv`, `data/processed/experimento_v2_pool_desarrollo.csv`, `data/metadata/juicios_desarrollo_v2.xlsx` y `.csv`, `outputs/reports/experimento_v2_pesos_m4.md`, `tests/test_pesos_m4.py`, `tests/test_sistemas.py`, `tests/test_flujo.py`.

## R29. Efecto mínimo detectable antes del test

- **Decisión.** El efecto mínimo detectable (EMD) se fija con los 419 juicios de desarrollo y los pesos de R28, antes de ejecutar ninguna consulta de prueba, con la fórmula del protocolo: EMD = (z_0,975 + z_0,8) · DE / raíz(30). No se calcula potencia a posteriori.
- **H1 (M4 frente a M2).** DE de las diferencias en desarrollo: 0,169. EMD con 30 consultas: 0,087 (rango 0,060 a 0,159 por la incertidumbre de estimar la DE con 10 consultas). Detectar el umbral práctico de 0,03 exigiría unas 250 consultas. El estudio no tiene potencia para ese umbral, y un resultado no significativo se informará como «no se detectó una mejora de la magnitud detectable», no como ausencia de efecto.
- **H2 (M3 frente a M3-sin-orden).** DE: 0,051; EMD: 0,026 (0,018 a 0,048). La DE es pequeña porque 8 de las 10 diferencias de desarrollo son cero (R27), y el efecto medio se diluye en la misma proporción: si el orden solo actúa en las 9 consultas de prueba con bandas, en ellas el efecto tendría que ser unas 30/9 veces mayor, del orden de 0,09, para detectarse en la media de las 30.
- **Análisis secundario de H2.** Con solo 2 consultas de desarrollo con palabra de bandas, su desviación no es estimable; se informará de forma descriptiva junto a su intervalo.
- **Ceguera.** El informe no muestra el nDCG medio de ningún sistema ni el signo de las diferencias.
- **Archivos.** `src/experimento/potencia.py`, `src/flujo.py`, `outputs/reports/experimento_v2_potencia.md`, `tests/test_potencia.py`, `tests/test_flujo.py`.
- *(23 de noviembre: el asesor aceptó el EMD de H1 como estimación incierta, no como frontera (R34). La cifra de H2 (0,026, y las consultas necesarias para 0,03) usa una aproximación normal que no vale con a lo sumo nueve diferencias distintas de cero; R35 la sustituye por la p mínima alcanzable.)*

## R30. Apertura del test, corrección de R21 y parámetros de M0, M1 y M3

- **Apertura del test.** El 21 de noviembre el investigador decidió esperar la aprobación del protocolo por el asesor antes de abrir el test. Cambia el contexto de R27, que partía de ejecutar el test antes de entregar el informe al asesor; las decisiones de fondo de R27 (alcance de H2, juicios de prueba sin asistencia, 30 consultas y evaluador único) se mantienen. Mientras tanto se prepara, con datos de desarrollo, el código que ejecutará el test.
- **Corrección de R21.** R21 dice que «las 66 confirmaciones coinciden con la propuesta automática» y que «las 42 correcciones la modifican». El informe generado `outputs/reports/anotacion_v2_revision_criterios.md` da otra cifra: 58 de las 108 decisiones coinciden con la propuesta y 50 la modifican. La diferencia está en las ocho anotaciones desplazadas (R20 y R22): se confirmaron, pero su propuesta indicaba que la imagen no correspondía al registro. Valen las cifras del informe, que son las que usan los capítulos 4 y 5 del manuscrito.
- **Parámetros de M0, M1 y M3.** Quedan fijos en sus valores de partida: k₁ = 1,2 y b = 0,75 en M0, pesos iguales de color y textura en M1 y pesos de bloque iguales a 1 en M3. No se ajustaron mientras el asesor no se pronunciara sobre R17 (R24). Después de R28, ajustar M3 cambiaría los candidatos de M4 y obligaría a repetir la selección de pesos, que se hizo una sola vez para evitar un ciclo. El único ajuste con datos de desarrollo es el de los pesos de M4.
- **Archivos.** `docs/protocolo_experimental_v2.md` (versión 0.6.4, secciones 4 y 9), `docs/manuscrito/capitulo_7_diseno_experimental.md` (secciones 7.4 y 7.12). Ningún dato cambia.

## R31. Condiciones de buena formación y cota del control en pruebas automáticas

- **Decisión.** Las condiciones de buena formación B3 a B7 de la anotación (capítulo 5, sección 5.4.1) dejan de ser una verificación manual hecha al congelar y pasan a ser reglas: la congelación se niega a escribir una copia que las incumpla, y el paso del flujo que comprueba la copia congelada termina con código 1 si la copia las incumple. La proposición 5.6 (la distancia del control sin orden no supera a la distancia entre palabras) queda fijada en una prueba automática por enumeración exhaustiva (132 496 pares).
- **Por qué sobre la anotación final y no sobre los libros.** La primera anotación de los lotes 2 a 5 podía incumplirlas antes de las correcciones de la revisión de criterios. Convertirlas en errores de los libros detendría el flujo por filas ya corregidas.
- **Resultado.** La anotación congelada v2.1 cumple las cinco condiciones (0 piezas las incumplen) y la proposición 5.6 no tiene violaciones. Ningún valor de la anotación cambia.
- **Archivos.** `src/anotacion/buena_formacion.py`, `src/anotacion/congelacion_v21.py`, `outputs/reports/anotacion_v2_1_congelada.md`, `tests/test_buena_formacion.py`, `tests/test_sistemas.py`, `docs/manuscrito/capitulo_5_metodo_formal.md`, `docs/manuscrito/capitulo_6_implementacion.md`, `docs/especificacion_m3.md`.

## R32. Precisiones del análisis de prueba y test listo para un solo comando

- **Contexto.** El protocolo nombra tres análisis sin definirlos del todo. El investigador los fijó el 21 de noviembre, antes de ejecutar ninguna consulta de prueba.
- **Ablación de M3 por bloques.** «M3 solo con bandas» usa los bloques de la palabra de bandas y de las adyacencias (`bandas`, `adyacencias`), con los demás pesos en 0. «M3 sin bandas» usa todos los demás bloques del descriptor (composición, borde, centro, simetría, repetición, motivos y familia iconográfica). Los dos lados cubren el descriptor sin solaparse. Es exploratoria.
- **Robustez por estado de la pieza.** Se usa la completitud que el revisor escribió en el motivo de su decisión de curación, interpretada por `src/imagenes/motivos.py`: completo, incompleto o sin dato. Al comprobarla en la galería se vio que 61 de las 150 piezas (41 %) no la mencionan; por eso se informan tres grupos y no dos, en lugar de clasificar como fragmento toda pieza que no sea imagen de referencia. En la prueba: 44 completas, 17 incompletas y 45 sin dato (piezas de la galería de prueba). Es descriptiva.
- **Tarea T1.** Se ejecuta con las 6 consultas redactadas (protocolo, sección 3). M2 codifica la descripción tal como la escribió el evaluador, sin plantilla, porque T1 no tiene consultas de desarrollo con que elegirla. M3 solo participa si la consulta trae especificación estructural, y compara solo los bloques especificados. M4 fusiona los componentes disponibles con los pesos de R28. La muestra al azar del pool se elige entre los candidatos que no proponen M0 ni M2, los sistemas que no dependen de la anotación. Es exploratoria y descriptiva.
- **Implementación.** `python -m src.experimento.ejecucion_prueba` reúne la comprobación previa (`--comprobar`), la ejecución única de los rankings con su manifiesto (`--rankings`), los libros ciegos de juicios de prueba de T3 y T1 (`--crear-juicios`) y el cálculo final (`--evaluar`). `--rankings` se niega a ejecutar mientras `[ejecucion] aprobacion_protocolo` esté vacío o la suma del protocolo no coincida con la registrada al aprobarlo. Los vectores de texto de T1 se calculan con `python -m src.modelos.m2_openclip --textos-t1`, con la misma condición. El cálculo se probó con la partición de desarrollo y con consultas T1 hipotéticas; ningún sistema se ejecutó sobre las consultas de prueba.
- **Al aprobarse el protocolo.** Se escriben en `[ejecucion]` la fecha y el commit de la aprobación y la suma SHA-256 del protocolo aprobado, y se registra en el historial del protocolo.
- **Archivos.** `src/experimento/ejecucion_prueba.py`, `src/experimento/rankings.py`, `src/experimento/juicios.py`, `src/modelos/m2_openclip.py`, `config/experimento.toml` (`[metricas]` y `[ejecucion]`), `tests/test_ejecucion_prueba.py`, `docs/protocolo_experimental_v2.md` (versión 0.6.5).
- *(23 de noviembre: R37 cambia el orden de la ejecución: el manifiesto se escribe antes de los rankings y la corrida avanza por estados.)*

## R33. Multiplicidad: secuencia fija de H1 y H2

- **Contexto.** El dictamen del asesor del 21 de noviembre, sobre el commit `6c121a3` y el protocolo 0.6.5, es favorable al diseño piloto y condiciona la apertura del test a que sus observaciones se acrediten en un nuevo commit con pruebas automáticas. No pide ampliar el corpus, cambiar las 30 consultas, volver a elegir los pesos de M4 ni repetir los juicios de desarrollo. Las decisiones R33 a R39 responden a sus observaciones B1 a B8 y se toman sin haber ejecutado ningún sistema sobre las consultas de prueba.
- **Observación (B1).** El protocolo decía que H2, «al ser una sola», no requería corrección por comparaciones múltiples, pero H1 y H2 son dos comparaciones confirmatorias.
- **Decisión.** Secuencia fija. H1 se contrasta primero con α = 0,05. H2 recibe una conclusión confirmatoria solo si H1 cumple su regla completa (p < 0,05 y diferencia media ≥ 0,03); si no, H2 se informa como exploratoria, con su estimación, su intervalo y su p, sin veredicto.
- **Motivo.** El procedimiento de secuencia fija controla la tasa de error por familia en α sin dividir el nivel, porque la segunda hipótesis solo se contrasta si se rechaza la primera. La exigencia adicional de Δ ≥ 0,03 hace la compuerta más conservadora. Se elige el orden H1 → H2 porque H1 es la hipótesis primaria de la tesis.
- **Consecuencia declarada.** Con la potencia disponible (R29 y R35), la compuerta hace improbable una conclusión confirmatoria sobre H2.
- **Alcance de H1 (B6).** H1 compara la fusión enriquecida M4 (M0, M2 y M3) con M2. Un resultado favorable no aísla el aporte de la estructura, porque M4 también añade el texto; ese aporte se examina en las ablaciones, que son exploratorias. El manuscrito deja de decir que la comparación «aísla» la estructura.
- **Archivos.** `docs/protocolo_experimental_v2.md` (versión 0.6.6, sección 1), `src/experimento/evaluacion.py` (`compuerta`), `src/experimento/ejecucion_prueba.py`, `tests/test_evaluacion.py` (prueba T1). Pendiente: el capítulo 2, el capítulo 7 y el resumen del manuscrito.

## R34. Inferencia de H1

- **Observación (B2).** Con 10 000 réplicas no se informaba el error de Monte Carlo, y la función que decide el veredicto mezclaba la p y el umbral: una diferencia positiva y significativa menor que 0,03 salía como «no se sostiene» sin distinguirla de una diferencia nula.
- **Decisión.** Prueba de permutación pareada por cambio de signo con B = 100 000 réplicas fijas, semilla declarada, p = (b + 1)/(B + 1) y error de Monte Carlo √[p(1 − p)/B]. El cálculo termina solo al completar las B réplicas. El resultado se informa en tres afirmaciones separadas: frente a cero (p < 0,05), estimación (media e IC 95 %) y relevancia práctica (Δ ≥ 0,03). H1 se sostiene solo con la primera y la tercera; cada una de las demás combinaciones tiene su propia redacción (protocolo, sección 7). Una diferencia negativa significativa se informa como «M4 inferior a M2», y una p no significativa no se presenta como ausencia de mejora.
- **Efecto mínimo detectable.** El de H1 (0,087, con un rango de 0,060 a 0,159) se presenta como estimación aproximada de planificación con diez consultas, no como frontera; así lo aceptó el asesor.
- **Archivos.** `docs/protocolo_experimental_v2.md` (sección 7), `config/experimento.toml` (`replicas_permutacion = 100000`), `src/experimento/evaluacion.py` (`decidir`, `permutacion_pareada`, `error_monte_carlo`), `src/experimento/potencia.py`, `outputs/reports/experimento_v2_potencia.md`, `tests/test_evaluacion.py` (prueba T3).

## R35. Inferencia exacta de H2 y empates

- **Observación (B3).** H2 usaba la misma permutación por muestreo que H1, aunque solo pueden ser distintas de cero las diferencias de las consultas con palabra de bandas (a lo sumo 9). Con tan pocas, la distribución nula se puede enumerar completa, y con m ≤ 5 no se alcanza p < 0,05.
- **Decisión.** p exacta por enumeración de los 2^m vectores de signos de las m diferencias distintas de cero, bilateral. Se definen n (consultas evaluables), b (consultas evaluables con palabra de bandas) y m (diferencias distintas de cero, m ≤ b), y se informa la p mínima alcanzable, 2^(1−m). Si m = 0, p = 1. En el subgrupo de bandas, el umbral práctico equivale a 0,03 · n/b (0,10 con 30 y 9); si b = 0, el subgrupo no es estimable. Se declaran el supuesto de intercambiabilidad de las etiquetas dentro de cada consulta, la independencia entre consultas y el carácter conservador de una prueba discreta.
- **Empates.** Una diferencia con |Δ_q| ≤ 1e-12 cuenta como cero, en H1 y en H2. Sin esa tolerancia, un redondeo de coma flotante podría convertir en distinta de cero una diferencia nula por construcción (R27) y cambiar m.
- **Corrección de R29 (hallazgo propio).** El EMD de H2 (0,026) y las consultas necesarias para 0,03 se calcularon con una aproximación normal que no vale con a lo sumo nueve diferencias distintas de cero. Se retiran del protocolo; el informe de potencia se corregirá para informar la p mínima alcanzable.
- **Archivos.** `docs/protocolo_experimental_v2.md` (sección 7), `config/experimento.toml` (`tolerancia_empates`), `src/experimento/evaluacion.py` (`permutacion_exacta`, `p_minima`, `sin_empates`), `src/experimento/potencia.py`, `outputs/reports/experimento_v2_potencia.md`, `tests/test_evaluacion.py` y `tests/test_potencia.py` (prueba T2).

## R36. H3 como fidelidad computacional

- **Observación (B4).** H3 incluía en su veredicto una revisión humana de diez explicaciones que no existía en el código y que no puede probar lo mismo que la reconstrucción y la intervención.
- **Decisión.** H3 afirma la fidelidad computacional de la descomposición de M4 y se sostiene con dos comprobaciones: reconstrucción e intervención, con error máximo de 1e-9. La revisión humana pasa a ser un análisis descriptivo aparte. Un acierto es un resultado del top 10 de M4 juzgado con grado ≥ 2, y un error, uno juzgado con grado 0 o 1; los `no_evaluable` no entran en ninguna clase. Se sortean 5 y 5 con semilla fija; si una clase tiene menos de 5, se usan todos y se informa. La ficha es ciega a la clase, al grado y a la posición. El evaluador marca cada explicación como correcta, incorrecta, especulativa o no evaluable. Se declara que la revisión no es independiente, porque el revisor anotó la estructura que usa M3.
- **Archivos.** `docs/protocolo_experimental_v2.md` (secciones 1 y 8), `config/experimento.toml`, `src/experimento/ejecucion_prueba.py` (`--crear-revision-h3`, `muestra_revision_h3`, `validar_revision_h3`), `tests/test_ejecucion_prueba.py` (prueba T6).
- *(23 de noviembre, al contrastar con el texto completo del dictamen: la ficha añade el código de desacuerdo (componente cuya contribución no corresponde: ninguno, M0, M2, M3 o varios) y una justificación obligatoria con las valoraciones incorrecta o especulativa; el denominador son las fichas sorteadas.)*

## R37. Estados de la corrida, gestión de fallos y custodia

- **Observación (B5).** El código escribía los rankings antes que el manifiesto, el manifiesto omitía en silencio los archivos ausentes y la evaluación solo comprobaba que existiera el archivo de rankings.
- **Decisión.** La corrida tiene un identificador y avanza por cinco estados (`autorizada`, `insumos_sellados`, `rankings_sellados`, `juicios_cerrados`, `evaluada`), cada uno registrado en el manifiesto. El manifiesto se escribe antes de los rankings, y un insumo obligatorio ausente detiene la corrida. Cada paso escribe en archivos temporales y publica sus salidas de una vez. `--evaluar` recalcula todas las sumas y suspende la corrida si alguna no coincide, si hay archivos de otra corrida o si falta un estado. La ausencia del manifiesto es una condición de suspensión.
- **Custodia.** Sin firma criptográfica personal: etiqueta Git anotada en cada cambio de estado, registro `docs/registro_custodia.md` (fecha, responsable, identificador de corrida, commit y sumas SHA-256) y envío de las sumas al asesor por correo al sellarlas.
- **Archivos.** `docs/protocolo_experimental_v2.md` (secciones 9 y 12), `src/experimento/ejecucion_prueba.py` (`verificar`, `publicar`, `suspender`, `--cerrar-juicios`), `docs/registro_custodia.md`, `tests/test_ejecucion_prueba.py` (pruebas T4 y T5) y `tests/test_experimento.py` (prueba T8, coherencia del protocolo con la configuración y el código).
- *(23 de noviembre, al contrastar con el texto completo del dictamen: se añaden las pruebas de `--evaluar` con un byte alterado en un insumo, un ranking o los juicios, que se detiene sin escribir métricas; de un archivo sellado faltante, y del rechazo de una reejecución después del sellado (`reejecucion`). La reanudación solo procede desde un estado sellado y sin resultados interpretables. El investigador adjunta una declaración escrita de no haber ejecutado sistemas sobre las consultas de prueba.)*

## R38. Estabilidad del evaluador en prueba

- **Observación (B7).** El asesor pide probar el cegamiento de extremo a extremo y, o bien rejuzgar una muestra, o bien declarar que no se mide la estabilidad del evaluador.
- **Decisión.** No se rejuzga una muestra de prueba. El protocolo (secciones 6 y 10) y el capítulo 11 declaran que no se estimó la estabilidad intraevaluador de los juicios de prueba. El cegamiento se comprueba con un validador automático del libro de juicios: no contiene el sistema, la puntuación ni la posición, y conserva el orden de presentación sorteado.
- **Alcance.** La estabilidad del lote 1 que ya se informa es la de la anotación, no la de los juicios, y no la sustituye.
- **Archivos.** `docs/protocolo_experimental_v2.md` (secciones 6 y 10), `src/experimento/ejecucion_prueba.py` (`validar_cegamiento`), `tests/test_ejecucion_prueba.py` (prueba T7), `docs/manuscrito/capitulo_11_limitaciones_trabajo_futuro.md` (sección 11.3).
- *(23 de noviembre, al contrastar con el texto completo del dictamen: el manifiesto sella también la huella de la rúbrica, las instrucciones y los parámetros de pooling (`reglas_juicio`), y el validador comprueba que la guía de cada libro coincide con ellas antes de entregarlo y al cerrarlo. El informe añade la cobertura del pool por consulta y la sensibilidad de cada sistema a retirar sus aportes exclusivos (regla P1).)*

## R39. Archivo de auditoría de los juicios de desarrollo asistidos

- **Observación (B8).** R25 decía que los grados iniciales se conservaban fuera del repositorio, sin un archivo formal ni una huella que permitiera verificarlo.
- **Decisión.** Se arma un archivo de auditoría con el material de la segunda opinión del 19 de noviembre: los grados del evaluador antes de la revisión, la segunda opinión del modelo, la revisión firmada por el evaluador y el informe de la comparación. Debe añadir la versión exacta del modelo y las instrucciones que recibió, y separar los 411 juicios que se usaron para elegir los pesos de M4 de los 8 juzgados después sin asistencia (R28). El archivo queda privado en `investigacion_local/`, fuera de git. En el repositorio se registran su suma SHA-256 y una descripción de su contenido (archivos, campos y número de juicios, versión del modelo e instrucciones), sin los grados iniciales ni las respuestas del modelo.
- **Riesgo de anclaje.** El capítulo 7 declarará, con los datos del informe de la segunda opinión, el riesgo de que el evaluador se anclara en la opinión del modelo.
- **Archivos.** `docs/auditoria_juicios_desarrollo.md` (descripción y huella), `docs/manuscrito/capitulo_7_diseno_experimental.md` (sección 7.6.4).
- *(23 de noviembre: archivo armado en `investigacion_local/auditoria_juicios_asistidos_2026-11-19/`, con 429 archivos y su manifiesto `SHA256SUMS.txt`, de suma `c473375f6cc9c3127906704a5e03e587d7db7b6585a1123fe5a794ea1d0099f2`. Incluye el modelo usado (`claude-opus-5-5`, cinco instancias), sus instrucciones, las 411 imágenes que vio, sus respuestas y la separación de los 411 juicios usados para los pesos de los 8 posteriores.)*

## R40. Autorización del test y apertura de la corrida

- **Autorización.** El 23 de noviembre de 2026, en reunión con el investigador, el asesor autorizó la apertura del test sobre el commit `2b01f0e` (protocolo 0.6.6), sin cambios, y ratificó las decisiones R33 a R39. Atiende la condición C12 del dictamen del 21 de noviembre.
- **Registro.** La fecha, el commit autorizado y la suma SHA-256 del protocolo se escriben en `[ejecucion]` de `config/experimento.toml`; el protocolo añade la fila de la autorización en su historial, y `docs/registro_custodia.md`, el estado `autorizada`. El protocolo queda congelado desde ese momento: si cambia, la comprobación previa y la ejecución se niegan a continuar.
- **Declaración.** El investigador declaró por escrito al asesor, el 23 de noviembre, que no había ejecutado ningún sistema sobre las consultas de prueba.
- **Vectores de T1.** Se calcularon el 23 de noviembre con `--textos-t1`, en CPU, con los pesos de M2 cuya suma coincide con la del manifiesto (`a5412f19…f378`) y las mismas versiones de bibliotecas. El tokenizador del codificador de texto se descargó en esa ejecución y no tiene suma en el manifiesto de M2; queda registrado aquí.
- **Siguiente.** Sellado de los insumos y rankings de prueba (`--rankings`), libros ciegos de juicio y juicios sin asistencia. El evaluador no abre los rankings, el pool ni el manifiesto de ejecución.
- **Archivos.** `config/experimento.toml`, `docs/protocolo_experimental_v2.md`, `docs/registro_custodia.md`.

## R41. Criterio de la revisión de H3, doble juicio y entrega

- **Criterio de lectura de la revisión de H3.** La guía del libro de revisión (sellada) no fijaba cuándo una contribución es «alta» o «baja». El investigador aplicó el mismo criterio a los tres componentes (M0, M2 y M3), sobre la puntuación normalizada por mínimo y máximo de cada consulta: alta si es ≥ 0,67, baja si es ≤ 0,33. En la zona intermedia, la contribución no se toma como una afirmación sobre las imágenes. El criterio se fijó después de crear el libro de revisión, sin conocer la clase (acierto o error) de ninguna ficha, y el investigador lo declaró el 24 de noviembre, después de completar la revisión. Como la revisión es descriptiva (R36), el criterio no cambia el veredicto de H3. Se informa como limitación que no quedó registrado antes de valorar la primera ficha.
- **Doble juicio parcial.** No se realiza. No hubo segundo evaluador disponible antes de la entrega, y el protocolo (sección 6) lo condicionaba a que lo hubiera (R27). No es una desviación: los resultados se informan con un solo evaluador y la falta de acuerdo entre evaluadores se declara en las limitaciones.
- **Entrega.** El informe de Seminario de Tesis II (MCC702, semestre 2026-2) se entrega el 27 de noviembre de 2026. Se redacta sobre `docs/manuscrito/`; el primer entregable (`docs/manuscrito/entregable_1_MCC701/`) sirve solo como referencia de formato y de figuras.
- **Archivos.** `docs/registro_decisiones.md`.

## R42. Levantamiento del informe del asesor y fe de erratas de AIC:85278

- **Informe del asesor (25 de noviembre de 2026).** Dictamen favorable con correcciones documentales: C01 (descripción única de la desviación de custodia, sin afirmar que las etiquetas Git sustituyen la constancia externa), C02 (separar la comparación confirmatoria M4 frente a M2 de las atribuciones exploratorias a sus componentes; no atribuir la ganancia a atributos no medidos) y C03 (índice generado, campos actualizados y PDF comprobado). Se atienden en el manuscrito sin tocar rankings, juicios, pesos ni archivos sellados. Se añade una aclaración fechada al registro de custodia, sin modificar sus filas.
- **Formato.** Las referencias pasan al formato IEEE numérico con una sola lista final, como exige la guía de la UNI (`docs/manuscrito/referencias.bib` y citeproc). Se mantiene «Cuadro». El curso figura como «MCC702 – Seminario de Tesis II». La plantilla, el filtro de ecuaciones y el script de generación se versionan en `docs/manuscrito/plantilla/`.
- **AIC:85278.** Al preparar las figuras se comprobó que su anotación congelada (v2.1) no corresponde a su fotografía: describe un campo central con una figura y sin repetición, y la imagen muestra una retícula de seis módulos con figuras frontales. Las anotaciones vecinas de su lote corresponden a sus imágenes, de modo que no es un desplazamiento en cadena. La pieza había entrado en la revisión de criterios del 16 de noviembre con petición de verificar su identidad, y la propuesta y la firma la dieron por coincidente; la copia de evaluación sellada es la descargada el 13 de octubre y su suma coincide con el manifiesto, de modo que el error está en la anotación y en esa verificación, no en la imagen. La copia congelada es un insumo sellado de la evaluación final y no se corrige. En los rankings sellados, la pieza entró entre los diez primeros de M3 en tres consultas (T3-P06, T3-P11, T3-P18) y de M4 en una (T3-P11), y en todas se juzgó con grado 0; el error pudo perjudicar ligeramente a M3 y a M4, no favorecerlos. Se declara en el capítulo 11. La corrección de la anotación, en el libro de anotación, queda para una versión posterior (v2.2), porque el flujo comprueba que la exportación coincide con la copia congelada.
- **Archivos.** `docs/manuscrito/`, `docs/registro_custodia.md`.

## R43. Levantamiento del informe final del asesor (B1-01 y B1-02)

- **Informe del asesor (27 de noviembre de 2026),** sobre el *commit* `4ddab6d`: pendiente de conformidad por dos precisiones científicas. Las cifras de H1, H2 y H3 se reprodujeron y no cambian; no se repite ningún experimento ni se modifica ningún insumo o resultado sellado.
- **B1-01, alcance de la proposición 5.6.** La cota $d_t \le d_w$ vale para el bloque de bandas y no se extiende a la disimilitud agregada ni al ordenamiento de los candidatos: el control omite el bloque de adyacencias y renormaliza los demás, y el orden relativo de dos candidatos puede invertirse aunque sus histogramas difieran del de la consulta. Se retira «M3 refina a su control»; el título de la proposición precisa «en el bloque de bandas» y la demostración no cambia. Los conteos de la sección 5.13 (53 piezas, 1378 pares, 41, 25 y 3) se conservan como descripción de las coincidencias que el control no distingue, no como cota de las inversiones de posición. Los contraejemplos del asesor se comprobaron con la implementación, sin modificarla: 1/4 frente a 1/3 en la disimilitud agregada, e inversión con la consulta `aab` y los candidatos `a` y `aacc`.
- **B1-02, nDCG con juicios parciales.** El nDCG@10 con los no juzgados en 0 no es una cota inferior del valor con juicios completos, porque cambian la ganancia observada y la ideal (contraejemplo del asesor: de 1 a 0,33735, comprobado). Las métricas de las variantes que no aportaron al *pool* se presentan como estimaciones bajo los juicios disponibles; el análisis de aportes exclusivos mide la sensibilidad a ese conjunto de juicios, no el signo del sesgo (M4 pasa de 0,604 a 0,602; M2, de 0,492 a 0,443). La cobertura completa del top 10 de los siete *rankings* del *pool* no equivale a un conjunto de relevancias exhaustivo: la ganancia ideal de H1 y H2 puede depender de juicios faltantes.
- **Portada.** Se incluyen la nota del asesor (20), el código UNI del tesista y las líneas de firma del asesor y del tesista.
- **Archivos.** `docs/manuscrito/`, `docs/revision_asesor_2026-11/relacion_cambios_informe_2026-11-27.md`.
