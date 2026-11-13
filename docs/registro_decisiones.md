# Registro de decisiones

Decisiones del investigador sobre el diseño, la evaluación y la redacción de la tesis, a partir del 12 de noviembre de 2026. Las anteriores están en `docs/plan_cierre_tesis.md` (D1 a D7 y «Seguimiento») y en el «Historial» de `docs/protocolo_experimental_v2.md`. Cada entrada indica qué se decidió, por qué, con qué respaldo, qué archivos cambia y qué queda por hacer. Una decisión no se edita: si cambia, se añade una entrada nueva que la sustituye y se anota en la anterior.

Estados: **Decidida** (vigente); **Por ratificar** (decidida por el investigador, espera al asesor porque cambia el protocolo); **Sustituida por Rnn**.

## Resumen

| ID | Fecha | Decisión | Estado |
|---|---|---|---|
| R01 | 2026-11-12 | H1 y H2 se deciden con permutación pareada; el bootstrap queda para el intervalo | Por ratificar |
| R02 | 2026-11-12 | Kappa ≥ 0,6 se usa como señal de revisión, no como aprobado | Por ratificar |
| R03 | 2026-11-12 | Se añade la ablación de M4 por posiciones recíprocas | Por ratificar |
| R04 | 2026-11-12 | El efecto mínimo detectable se calcula antes del test | Por ratificar |
| R05 | 2026-11-12 | No se esperan los textos sin acceso; la brecha se redacta con lo leído | Decidida |
| R06 | 2026-11-12 | La cifra de CLIP en relaciones se cita de la página 4 de Yuksekgonul et al. | Decidida |
| R07 | 2026-11-12 | El ajuste de pesos se describe como «pocas consultas etiquetadas», sin número | Decidida |
| R08 | 2026-11-12 | Las referencias se completan en el `.bib` y el estilo se fija al final | Decidida |
| R09 | 2026-11-12 | Este registro es el lugar único de las decisiones nuevas | Decidida |
| R10 | 2026-11-12 | En la fusión por posiciones, los pares sin evidencia estructural van al final del ranking de M3 | Por ratificar |

## R01. Prueba inferencial de H1 y H2

- **Decisión.** H1 y H2 se deciden con una prueba de permutación pareada por cambio de signo, bilateral, con 10 000 réplicas, semilla fija y nivel 0,05. Se informa la t de Student pareada como comprobación. El bootstrap pareado se conserva solo para el IC 95 %.
- **Antes.** La regla de H1 dependía de que el límite inferior del IC 95 % por bootstrap fuese mayor que cero, y la permutación era un análisis de sensibilidad.
- **Motivo.** Con pocos temas, la t pareada y la permutación mantienen el error de tipo I nominal, y el bootstrap usado como prueba tiende a valores p pequeños. El estudio citado trata pruebas de hipótesis y no cuestiona los intervalos.
- **Fuente.** Urbano, Lima y Hanjalic (2019), p. 2 y 7. Ficha F20.
- **Archivos.** `docs/protocolo_experimental_v2.md`, secciones 1 y 7 (versión 0.6).
- **Pendiente.** Añadir `alfa` y la prueba elegida a `[metricas]` de `config/experimento.toml` y a la prueba de coherencia, al implementar la evaluación.

## R02. Uso del umbral de acuerdo

- **Decisión.** Se mantiene kappa ≥ 0,6 como señal de revisión por atributo, no como criterio de aprobación. Se declara como criterio operativo de estudio piloto. Un atributo por debajo se revisa en la guía antes de congelar la anotación v2.1. Si es `composicion`, se mantiene y se declara como limitación de H2. `secuencia_bandas` se informa con coincidencia exacta y similitud de edición, sin umbral.
- **Motivo.** No hay un umbral aceptado. La referencia consultada propone 0,8 si hay que fijar uno y desaconseja que un umbral sea requisito; pide informar el método, el coeficiente y la tabla de acuerdos. La regla se fija antes de calcular el acuerdo, para no decidir sobre los atributos a la vista de los resultados.
- **Fuente.** Artstein y Poesio (2008), p. 22 y 37 (ficha F07); Landis y Koch (1977) para la escala.
- **Archivos.** `docs/protocolo_anotacion_v2.md` (medición del acuerdo); `docs/protocolo_experimental_v2.md`, sección 10.
- **Pendiente.** El informe generado `outputs/reports/anotacion_acuerdo_v2.md` todavía dice «umbral de acuerdo aceptable». Cambiar el texto en `src/anotacion/acuerdo.py` y el comentario de `[acuerdo]` en `config/anotacion.toml`, y regenerar con el flujo. Añadir la tabla de acuerdos por atributo si el informe no la da.

## R03. Ablación de M4 por posiciones recíprocas

- **Decisión.** Se añade como ablación exploratoria una variante de M4 que suma 1 / (60 + posición) sobre los rankings de M0, M2 y M3. Sus 10 primeros candidatos entran al pool de desarrollo y de prueba.
- **Motivo.** No tiene pesos, así que muestra cuánto del resultado de M4 depende del ajuste con 10 consultas de desarrollo.
- **Fuente.** Cormack, Clarke y Büttcher (2009), ficha F22; Bruch, Gai e Ingber (2023), ficha F04.
- **Archivos.** `docs/protocolo_experimental_v2.md`, secciones 6, 7 y 10.
- **Abierto.** El trato de los pares sin evidencia estructural (últimas posiciones del ranking de M3, por `id_global`) figura en el protocolo como propuesta: confirmarlo antes de implementar. No interviene en H3. *Resuelto en R10.*
- **Pendiente.** Constante k = 60 en `config/modelos.toml`; implementación junto con M4; inclusión en el pool. Si sus candidatos añaden demasiados pares para el calendario, se descarta antes de cerrar el pool de prueba y se registra aquí.

## R04. Efecto mínimo detectable

- **Decisión.** Antes de abrir el test se calcula el efecto mínimo detectable con 30 consultas y potencia de 80 %: (z₀,₉₇₅ + z₀,₈) · DE(Δ) / √30 ≈ 0,51 · DE(Δ), con DE(Δ) estimada en desarrollo y su rango de imprecisión. Si supera 0,03, el estudio se declara sin potencia para ese umbral y se informa el intervalo. No se calcula potencia a posteriori.
- **Motivo.** La potencia se planifica antes del experimento; calcularla después con el efecto observado no se recomienda.
- **Fuente.** Card et al. (2020), sección 3 y nota 2. Ficha F21.
- **Archivos.** `docs/protocolo_experimental_v2.md`, sección 7.
- **Pendiente.** El cálculo, cuando existan los juicios de desarrollo.

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
- **Pendiente.** Conectar M4 a los rankings y al pool cuando exista la anotación v2.1; constante k = 60 y rejilla de pesos en `config/modelos.toml`.
