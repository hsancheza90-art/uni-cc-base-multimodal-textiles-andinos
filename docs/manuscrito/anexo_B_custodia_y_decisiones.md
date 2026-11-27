# Anexo B. Custodia de la evaluación final y trazabilidad de las decisiones

Este anexo reúne los datos de procedencia que el cuerpo de la tesis omite: los estados de la ejecución única de la evaluación final y su custodia (capítulo 7, sección 7.12), el archivo de auditoría de los juicios de desarrollo asistidos (sección 7.6.4) y el índice de las decisiones registradas durante la segunda parte del trabajo. Las huellas SHA-256 se abrevian con sus primeros y últimos caracteres; las completas están en el manifiesto de ejecución (`data/processed/experimento_v2_manifiesto_ejecucion.json`) y en el registro de custodia (`docs/registro_custodia.md`).

## B.1 Estados de la corrida

La evaluación final se ejecutó en una sola corrida, `corrida-1d7165cf4dab`, entre el 23 y el 24 de noviembre de 2026. Cada estado se registró en el manifiesto de ejecución antes de pasar al siguiente, y ningún paso podía ejecutarse sin el estado anterior.

**Cuadro B.1.** Estados de la corrida.

| Fecha | Estado | Qué se hizo y qué quedó sellado | *Commit* | Etiqueta |
|---|---|---|---|---|
| 2026-11-23 | `autorizada` | El asesor autorizó el protocolo 0.6.6 en reunión, sobre el *commit* `2b01f0e`, sin cambios. Se registraron en la configuración la fecha, el *commit* y la suma del protocolo (`fd43ebae…c22d`), y se calcularon los vectores de texto de las consultas T1 | `cc501ae` | `test-v2-autorizado` |
| 2026-11-23 | `insumos_sellados` | Antes de calcular ningún *ranking*, con el árbol de trabajo limpio, se escribió el manifiesto con 17 sumas de insumos (particiones, consultas, anotación congelada, vectores de M2, índices de M1, configuración y protocolo), la huella de la rúbrica, las instrucciones y los parámetros de *pooling*, el punto de control de M2, las semillas, las versiones y el equipo | `cc501ae` | `test-v2-rankings-sellados` |
| 2026-11-23 | `rankings_sellados` | *Rankings* de T3 (`0a8d8176…2e3d`) y de T1 (`4b331212…767c`), *pool* de T3 (`5eb38c2e…f651`) y de T1 (`fbf719eb…e3c1`); creación de los libros ciegos de juicio | `73bfe74` | `test-v2-rankings-sellados` |
| 2026-11-24 | `juicios_cerrados` | Juicios de T3 (1283 pares; exportación `ee52f855…f3e2`, libro `a480dfe3…c447`) y de T1 (212 pares; exportación `d1aa209e…13fd`, libro `6cc822c7…8473`), emitidos sin asistencia | `3e55585` | `test-v2-juicios-cerrados` |
| 2026-11-24 | `evaluada` | Revisión descriptiva de H3 (10 fichas, sin asistencia; muestra `f9b7fb4f…c48a`, revisión `be9a71cb…a1a9`, libro `f080efbe…d48a`). La evaluación recalculó las 25 sumas del manifiesto, todas coincidentes, y produjo el informe (`046cf990…d4a7`) y las métricas por consulta (`9aa7145c…2b0f`) | `a45f6dc` | `test-v2-evaluada` |

La columna «*Commit*» indica el *commit* al que apunta la etiqueta de cada estado; en `insumos_sellados`, el *commit* registrado en el manifiesto como base de los insumos. El responsable de todos los estados es el investigador, Henry Sánchez Alvarado.

## B.2 Custodia

La custodia no depende de una firma criptográfica personal. Se documentó con tres elementos:

1. una etiqueta Git anotada por estado (Cuadro B.1), salvo `insumos_sellados` y `rankings_sellados`, que comparten etiqueta porque los produjo la misma orden;
2. el registro de custodia versionado, con la fecha, el responsable, la corrida, el *commit* y las sumas de cada estado; al estar bajo control de versiones, cualquier modificación posterior queda a la vista;
3. el envío de las sumas de cada estado al asesor por correo, que deja una constancia fuera del repositorio. Las sumas de los cinco estados se enviaron juntas por correo el 24 de noviembre de 2026, una vez evaluada la corrida, y no al sellar cada estado; es la desviación que describe la sección B.3.

El 23 de noviembre de 2026, junto con la autorización, el investigador declaró por escrito que no había ejecutado ningún sistema sobre las consultas de prueba.

## B.3 Gestión de fallos

El protocolo fijó de antemano cómo tratar un fallo:

- Cada paso escribe sus salidas en archivos temporales y las publica de una vez al terminar, de modo que un fallo no deja salidas parciales con el nombre definitivo.
- Si un paso falla antes de publicar, el estado no avanza, el fallo se anota en el registro de custodia y el paso puede repetirse desde el último estado sellado, con el mismo código y los mismos insumos, mientras no existan resultados interpretables.
- Una vez sellados los *rankings*, una segunda ejecución de esa orden se rechaza, y ningún *ranking* publicado se regenera con otro código ni con otros parámetros.
- Si la evaluación encuentra una suma que no coincide, un archivo sellado ausente, un artefacto de otra corrida o un estado que falta, la corrida queda suspendida: no se calcula ninguna métrica, se informa al asesor y no se repite ningún paso sin su conformidad.

En esta corrida no hubo fallos ni suspensiones. Se produjo una desviación del procedimiento de custodia: las sumas de los cinco estados se enviaron al asesor juntas, el 24 de noviembre de 2026, después de la evaluación, y no en el momento de sellar cada estado, como prevé el protocolo. Durante ese intervalo, la secuencia de los estados solo consta en las etiquetas Git anotadas, con fecha y hora: autorización y *rankings* sellados el 23 de noviembre (12:21 y 12:23), juicios cerrados el 24 (12:36) y evaluación el 24 (14:10), hora de Lima. La evaluación comprobó que las 25 sumas registradas en cada estado coincidían con los archivos, y la verificación de los archivos sellados no detectó discrepancias. Esa coincidencia acredita la integridad actual de los archivos, no toda su historia temporal. Las etiquetas Git son una constancia interna del repositorio y no sustituyen íntegramente la constancia externa contemporánea que debía dar el envío por etapas, de modo que el envío tardío limita la constancia externa de la secuencia de ejecución. La desviación figura en el registro de custodia. El doble juicio parcial previsto no se realizó porque no hubo un segundo evaluador; el protocolo lo condicionaba a que lo hubiera, de modo que no constituye una desviación.

## B.4 Archivo de auditoría de los juicios de desarrollo asistidos

La revisión de los juicios de desarrollo con la segunda opinión de un modelo (capítulo 7, sección 7.6.4) se documenta en un archivo de auditoría privado, bajo custodia del investigador y fuera del repositorio, porque contiene los grados iniciales del evaluador y las respuestas del modelo. En el repositorio se registran su huella y una descripción de su contenido (`docs/auditoria_juicios_desarrollo.md`), que resume el Cuadro B.2.

**Cuadro B.2.** Archivo de auditoría de los juicios asistidos.

| Elemento | Contenido |
|---|---|
| Fecha de la revisión | 19 de noviembre de 2026 |
| Fecha de armado del archivo | 23 de noviembre de 2026, con el material del 19 de noviembre sin modificarlo |
| Modelo | Claude Opus 5.5 (`claude-opus-5-5`), de Anthropic, un modelo de visión y lenguaje de uso general que no es CLIP ni ninguno de los sistemas evaluados |
| Forma | Cinco instancias del modelo, una por cada par de consultas de desarrollo, con las mismas instrucciones salvo los pares asignados |
| Entradas del modelo | Una imagen compuesta por par (consulta a la izquierda, candidato a la derecha) y la rúbrica 0–3 con `no_evaluable`; se pidió un grado, una confianza y una justificación breve por par |
| Sin acceso a | Los grados del evaluador, los *rankings*, los sistemas que propusieron cada par y la anotación |
| Contenido | Libro de juicios antes de la revisión, clave de pares, las 411 imágenes compuestas, las instrucciones de las cinco instancias, las respuestas del modelo, el rastro de cada par (grado inicial, opinión y decisión), la revisión firmada por el evaluador, el cruce entre ambos, el informe de la comparación y el uso de cada uno de los 419 juicios vigentes |
| Uso de los juicios | 411 juicios revisados con asistencia, usados para elegir los pesos de M4 y para la potencia; 8 juicios posteriores, sin asistencia, usados solo para la potencia |
| Cifras de la comparación | Grados mantenidos: 165; cambiados: 246. Kappa ponderado lineal antes de la revisión: 0,161 (408 pares comparables); después: 0,925. Justificación final coincidente con la del modelo en 406 de 411 pares |
| Archivos | 429, con un manifiesto `SHA256SUMS.txt` |
| SHA-256 del manifiesto | `c473375f6cc9c3127906704a5e03e587d7db7b6585a1123fe5a794ea1d0099f2` |

Para verificar el archivo basta calcular la suma SHA-256 de su manifiesto, compararla con la del cuadro y comprobar cada archivo contra el manifiesto. El archivo permite reconstruir cómo cambió cada juicio asistido y distinguir el grado del evaluador de la propuesta del modelo; no permite saber qué grado habría elegido el evaluador sin ver esa propuesta.

## B.5 Trazabilidad de las decisiones

Las decisiones del investigador sobre el diseño, la evaluación y la redacción tomadas desde el 12 de noviembre de 2026 se registraron con un identificador, su fecha, su motivo, su respaldo y los archivos afectados en `docs/registro_decisiones.md`, donde figura también el estado de cada una. Una decisión no se edita: si cambia, se añade una nueva que la sustituye. El Cuadro B.3 reproduce su índice.

**Cuadro B.3.** Índice de decisiones registradas.

| Id | Fecha | Decisión |
|---|---|---|
| R01 | 2026-11-12 | H1 y H2 se deciden con permutación pareada; el *bootstrap* queda para el intervalo |
| R02 | 2026-11-12 | Kappa ≥ 0,6 se usa como señal de revisión, no como aprobado |
| R03 | 2026-11-12 | Se añade la ablación de M4 por posiciones recíprocas |
| R04 | 2026-11-12 | El efecto mínimo detectable se calcula antes de la evaluación final |
| R05 | 2026-11-12 | No se esperan los textos sin acceso; la brecha se redacta con lo leído |
| R06 | 2026-11-12 | La cifra de CLIP en relaciones se cita de la página 4 de Yuksekgonul et al. [@yuksekgonul2023] |
| R07 | 2026-11-12 | El ajuste de pesos se describe como «pocas consultas etiquetadas», sin número |
| R08 | 2026-11-12 | Las referencias se completan en el archivo bibliográfico y el estilo se fija al final |
| R09 | 2026-11-12 | El registro de decisiones es el lugar único de las decisiones nuevas |
| R10 | 2026-11-12 | En la fusión por posiciones, los pares sin evidencia estructural van al final del *ranking* de M3 |
| R11 | 2026-11-12 | Se atienden las observaciones de forma de la auditoría interna y se agrega la observabilidad al informe de acuerdo |
| R12 | 2026-11-12 | Definición operativa de banda: franja completa, sin cenefas, retículas ni paneles |
| R13 | 2026-11-12 | Fusión de `repeticion_modular` en `traslacional` (descartada; sustituida por R16) |
| R14 | 2026-11-12 | En el lote re-anotado prevalece la re-anotación |
| R15 | 2026-11-12 | Regla de los treinta segundos: el estado `desconocido` del atributo basta |
| R16 | 2026-11-12 | Simetría: se mantienen `traslacional` y `repeticion_modular`, separadas por la dimensión de la repetición |
| R17 | 2026-11-13 | Los juicios de desarrollo se conservan como se emitieron y la reserva sobre la rúbrica se hace explícita |
| R18 | 2026-11-16 | Los lotes 2 a 5 se revisan con R12 y R16 en un libro aparte; las correcciones prevalecen al exportar |
| R19 | 2026-11-16 | El atributo `centro` se mantiene en la anotación y en M3 pese a su estabilidad baja |
| R20 | 2026-11-16 | La revisión de R18 parte de propuestas automáticas que el anotador verifica una por una |
| R21 | 2026-11-17 | Cierre de la revisión de criterios: 108 piezas verificadas, aclaraciones de R12 y del eje |
| R22 | 2026-11-17 | Reubicación de las ocho anotaciones desplazadas, observaciones en prosa y selección de la revisión congelada |
| R23 | 2026-11-17 | La anotación estructural v2.1 queda congelada; los sistemas leen la copia congelada |
| R24 | 2026-11-17 | *Rankings* de desarrollo de M3 y M3-sin-orden; el *pool* crece con sus candidatos y la muestra al azar queda fija |
| R25 | 2026-11-19 | Los juicios de desarrollo se revisan con la segunda opinión ciega de un modelo de visión general; el evaluador firma cada grado |
| R26 | 2026-11-19 | Se mide la sensibilidad de M3 a la revisión asistida de la anotación, solo en desarrollo |
| R27 | 2026-11-21 | H2 sobre 30 consultas, con el subgrupo de las 9 con bandas; juicios de prueba sin asistencia; 30 consultas; evaluador único |
| R28 | 2026-11-21 | Pesos de M4 elegidos una sola vez (1/7, 4/7, 2/7); M4 y M4-RRF en los *rankings* de desarrollo |
| R29 | 2026-11-21 | Efecto mínimo detectable fijado antes de la evaluación final: H1 0,087; H2 0,026 (este último retirado por R35) |
| R30 | 2026-11-21 | La evaluación final espera la autorización del asesor; se corrigen las cifras de R21; M0, M1 y M3 quedan con sus parámetros de partida |
| R31 | 2026-11-21 | Las condiciones B3 a B7 pasan a ser reglas de la congelación y del flujo; la proposición 5.6 se fija en una prueba automatizada |
| R32 | 2026-11-21 | Definición de la ablación de M3 por bloques, de la robustez por completitud y de la ejecución de T1 |
| R33 | 2026-11-23 | H1 y H2 se contrastan en secuencia fija: H2 es confirmatoria solo si H1 se sostiene; H1 no aísla la estructura |
| R34 | 2026-11-23 | H1 con 100 000 réplicas fijas, error de Monte Carlo y tres afirmaciones separadas; el efecto mínimo detectable es una estimación de planificación |
| R35 | 2026-11-23 | H2 con p exacta por enumeración de los cambios de signo y tolerancia de empates de 10⁻¹²; sin efecto mínimo detectable por aproximación normal |
| R36 | 2026-11-23 | H3 pasa a ser la fidelidad computacional de M4; la revisión humana de las explicaciones es descriptiva |
| R37 | 2026-11-23 | Estados de la corrida, manifiesto antes de los *rankings*, gestión de fallos y custodia sin firma personal |
| R38 | 2026-11-23 | No se rejuzga una muestra de prueba; la estabilidad intraevaluador no se mide |
| R39 | 2026-11-23 | Archivo de auditoría de los juicios asistidos, privado, con su huella y su descripción en el repositorio |
| R40 | 2026-11-23 | El asesor autoriza la evaluación final sobre el *commit* `2b01f0e`; se registra la autorización y se abre la corrida |
| R41 | 2026-11-24 | Criterio de lectura de la revisión de H3 (tercios), doble juicio parcial no realizado y entrega del informe de Seminario de Tesis II |
| R42 | 2026-11-26 | Levantamiento del informe del asesor del 25 de noviembre; referencias en IEEE; error de anotación de AIC:85278 declarado sin corregir la copia congelada |
| R43 | 2026-11-27 | Levantamiento del informe final del asesor: alcance de la proposición 5.6 al bloque de bandas y nDCG con juicios parciales como estimación, no como cota inferior |
