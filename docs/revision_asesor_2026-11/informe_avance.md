# Informe de avance de la segunda parte de la tesis

6 de noviembre de 2026. El informe describe el estado de la rama `main`, con el corpus de referencia en la etiqueta `corpus-met-cma-aic-v2.0`. Las cifras proceden de los informes que genera el flujo del repositorio (`outputs/reports/`); los conteos que el flujo verifica en cada ejecución se encuentran en `config/corpus.toml`.

## 1. Resumen

**Corpus.** El corpus v2, que reúne piezas del Metropolitan Museum of Art (MET), el Cleveland Museum of Art (CMA) y el Art Institute of Chicago (AIC), quedó cerrado y consolidado en 615 registros. Esos registros forman 577 grupos de piezas relacionadas, decididos por el investigador.

**Anotación.** El núcleo de anotación, de 150 piezas, está anotado con el esquema ampliado, que incorpora la secuencia de bandas y los estados de observabilidad. La anotación se validó sin errores. Su estabilidad se medirá mediante la re-anotación ciega del primer lote, prevista a partir del 12 de noviembre.

**Protocolo.** El protocolo experimental está redactado y a la espera de su aprobación. Las particiones de desarrollo y prueba y las 40 consultas de la tarea primaria quedaron congeladas, sin fugas entre particiones. Las 6 consultas de texto a imagen ya están redactadas.

**Sistemas.** M0, M1 y M2 están implementados y cuentan con rankings de desarrollo. El descriptor estructural M3 está especificado, implementado y probado; sus rankings se generarán sobre la anotación congelada. Falta implementar la fusión M4.

**Juicios.** El conjunto de pares de desarrollo está listo para el juicio ciego. Todavía no se dispone de ninguna métrica de recuperación ni se ha ejecutado ninguna consulta de prueba.

## 2. Corpus y versiones

| Versión | Contenido | Estado |
|---|---|---|
| `corpus-met-cma-v1.2` | Consolidado MET y CMA, 288 registros | Congelado como respaldo del primer avance; se regenera idéntico desde copias congeladas de sus entradas |
| Corpus v2 | 874 registros con decisión curatorial, de procedencia manual y automática: 462 en el principal, 153 en el secundario y 259 descartados | Cerrado |
| `corpus-met-cma-aic-v2.0` | Consolidado del principal y el complementario de las tres fuentes: 615 registros (MET 130 + 25, CMA 104 + 4 y AIC 228 + 124). Incluye el grupo de cada registro, las licencias por fuente, el manifiesto de imágenes y las sumas SHA-256 | Etiquetado el 6 de noviembre. No incluye la anotación estructural, que se incorporará en la versión 2.1 |

Las imágenes de las tres fuentes son de dominio público o tienen licencia CC0. Las descripciones de AIC tienen licencia CC BY 4.0 y se citan como tales. El resumen del consolidado está en `outputs/reports/corpus_textiles_andinos_met_cma_aic_v2_resumen.md` y su esquema, en `docs/esquema_consolidado_met_cma_aic_v2.md`.

## 3. Unidad experimental: grupos de piezas relacionadas (DAT01 y DAT02)

La auditoría señaló que la unidad experimental debía ser el objeto y no el registro, porque un mismo objeto puede aparecer en varias fotografías, vistas o fragmentos. Para identificar esas relaciones se proponen pares candidatos mediante cinco señales, aplicadas sobre el principal y el complementario. Un mismo par puede tener varias:

| Señal | Pares propuestos |
|---|---:|
| Imagen idéntica | 13 |
| Número de inventario con la misma base y un sufijo de parte (por ejemplo, `1922.395.a` y `1922.395.b`) | 52 |
| Descripción curatorial idéntica | 41 |
| Huella perceptual dHash de la copia de evaluación, con distancia ≤ 4 | 18 |
| Similitud de M2, con coseno ≥ 0,95 (≥ 0,93 entre museos) | 28 |
| **Pares distintos** | **100** |

El investigador decidió los 100 pares en un libro de revisión que exige revisor y fecha en cada decisión: 65 se unieron (13 de ellos, de imagen idéntica, propuestos automáticamente) y 35 se separaron. La regla según la cual los pares dudosos se unen, pensada para evitar fugas entre particiones, no llegó a aplicarse. El resultado son 577 grupos para los 615 registros: 555 grupos de una sola pieza, 15 de dos, 2 de tres, 3 de cuatro y 1 de cinco. El núcleo de anotación queda distribuido en 146 grupos.

Como comprobación de coherencia, las 18 piezas que comparten imagen con otra tienen a esa otra pieza como vecina más cercana en el espacio de M2. El detalle está en `outputs/reports/grupos_v2.md`.

## 4. Anotación estructural (ANN01)

**Esquema.** El esquema v2 (decisión D3) tiene 19 columnas. Respecto del primer avance, agrega el eje de las bandas y su secuencia: la «palabra de bandas», que registra el tipo de cada banda (lisa, geométrica, figurativa, mixta o no determinada), con lagunas para los tramos que no se ven. Se omiten deliberadamente el color y el ancho de cada banda. Los estados *ausente*, *no observable* y *desconocido* se registran en la misma celda del atributo, para distinguir lo que no existe de lo que no puede observarse. El procedimiento está en `docs/protocolo_anotacion_v2.md`.

**Núcleo.** El núcleo de anotación está formado por 150 piezas (42 de MET, 34 de CMA y 74 de AIC) en cinco lotes estratificados, que el investigador anotó el 5 de noviembre.

**Validación.** La validación (`outputs/reports/anotacion_v2_validacion.md`) no encontró errores y dejó tres tipos de avisos:
- 38 piezas registran un valor *desconocido* sin haberse marcado para revisión.
- 3 correcciones repiten el valor vigente.
- Las observaciones del anotador señalan 104 piezas con dudas, criterios por unificar o vacíos del vocabulario.

**Acuerdo.** Como no hay un segundo anotador (decisión D1), la consistencia de la anotación se estimará con un acuerdo intra-anotador. El primer lote se re-anotará a ciegas a partir del 12 de noviembre, en otro orden y al menos siete días después de la primera anotación. Se calcularán kappa por atributo y la similitud de edición entre las palabras de bandas. El resultado se informará como estabilidad de la anotación, no como acuerdo entre personas.

**Criterios pendientes.** Para que las dos pasadas usen los mismos criterios, la guía y el vocabulario no cambian hasta cerrar la re-anotación. Después se decidirán los criterios pendientes y la anotación se congelará como versión 2.1, antes de congelar los sistemas.

## 5. Protocolo experimental y partición de los datos (MET01)

El protocolo (`docs/protocolo_experimental_v2.md`, versión 0.5) formula tres hipótesis, cada una con su regla de decisión:
- **H1, primaria:** la fusión M4 supera a M2 en nDCG@10.
- **H2, sobre el mecanismo:** M3 supera a su versión sin orden.
- **H3, sobre la interpretabilidad:** el score se reconstruye y responde a la intervención como predice la fórmula.

El protocolo fija también un umbral práctico, el análisis por bootstrap pareado y los criterios que impiden abrir el test. La tarea primaria es T3, la recuperación de piezas con la misma estructura a partir de un ejemplar. La tarea de texto a imagen, T1, es secundaria y exploratoria.

Las particiones se congelaron por grupo y se estratificaron por museo: 44 grupos de desarrollo (44 piezas) y 102 de prueba (106 piezas). En cada ejecución, el flujo comprueba que ningún grupo esté presente en las dos particiones (`outputs/reports/experimento_v2_snapshot.md`).

Las consultas se fijaron así:
- **T3:** 10 consultas de desarrollo y 30 de prueba, sorteadas con semilla fija, a lo sumo una por grupo y estratificadas por museo y por tipo de composición. Se declaró de antemano una regla de reemplazo para el caso de que la corrección de la anotación deje alguna consulta sin composición observable.
- **T1:** el investigador redactó las 6 consultas el 6 de noviembre, antes de ejecutar ningún sistema sobre ellas.

Los valores numéricos del protocolo se encuentran en `config/experimento.toml`, y una prueba automática comprueba que coinciden con el documento.

## 6. Sistemas de recuperación (MOD01, MOD02 y MAT01)

| Sistema | Estado | Observaciones |
|---|---|---|
| M0: BM25 sobre el texto | Implementado, con rankings de desarrollo | Usa el texto de la ficha de cada pieza. La descripción de MET se excluye, porque en las 26 piezas que la tienen es una plantilla generada a partir de los metadatos y no un texto del museo |
| M1: color y textura | Implementado, con rankings de desarrollo | Histograma CIELAB y patrones binarios locales (LBP) sobre el textil, separado del fondo con la misma segmentación del puntaje de aptitud |
| M2: OpenCLIP | Implementado, con rankings de desarrollo | Checkpoint multilingüe `xlm-roberta-base-ViT-B-32` con pesos `laion5b_s13b_b90k` (licencia MIT), en precisión fp32 y CPU. Dos ejecuciones producen exactamente los mismos embeddings. El manifiesto registra la suma SHA-256 de los pesos |
| M3: descriptor estructural | Especificado (`docs/especificacion_m3.md`), implementado y probado | Usa la palabra de bandas en forma canónica bajo reversión, los pares de bandas contiguas, una máscara de observabilidad y una disimilitud mixta cuyas contribuciones suman exactamente el score. Excluye el color. Sus rankings se generarán sobre la versión 2.1 de la anotación |
| M3-sin-orden | Implementado | Control de H2: sustituye la palabra de bandas por el histograma de sus tipos y omite las adyacencias |
| M4: fusión | Pendiente, del 13 al 15 de noviembre | Fusión tardía y aditiva de M0, M2 y M3, con pesos ajustados en desarrollo |

Los rankings de desarrollo cubren las 10 consultas de desarrollo con 149 candidatos cada una, siempre sin el grupo de la propia consulta. Ningún sistema se ha ejecutado sobre las consultas de prueba.

## 7. Consultas y juicios de relevancia (ANN02)

El conjunto de pares de desarrollo reúne 345 pares: los diez primeros candidatos de M0, M1 y M2, sin repetir, más diez candidatos al azar por consulta. Se presentan para el juicio en un libro de revisión, en orden aleatorio y sin indicar qué sistema propuso cada candidato ni en qué posición. Lo acompañan una galería local de imágenes y una hoja de ejemplos hipotéticos de la escala 0–3. El registro de qué sistema propuso cada par se guarda en un archivo aparte, que el evaluador no consulta. Cuando existan M3 y M4 se agregarán sus candidatos, sin repetir los pares ya juzgados. Los juicios de prueba seguirán el mismo procedimiento sobre los candidatos de los sistemas congelados.

## 8. Software y reproducibilidad (REP01 y SW01 a SW12)

El flujo del repositorio consta de 23 pasos, se ejecuta sin acceso a red y está cubierto por 350 pruebas automáticas. Cada commit posterior a la auditoría se verificó en un clon limpio y sin las dependencias de M2: el flujo terminó sin hallazgos, las pruebas pasaron y el árbol de trabajo quedó sin cambios.

Las decisiones humanas se registran en libros de revisión y se validan antes de exportarlas (revisor, fecha, códigos del vocabulario y escala de juicio). Cualquier error detiene el flujo sin reemplazar las salidas anteriores.

De los defectos de código señalados por la auditoría:
- **Corregidos:** SW01, SW02, SW04, SW05 y SW08.
- **Mitigado:** SW10, en M0.
- **Diferidos según el plan:** SW03, SW06, SW07, SW09, SW11 y SW12.

La matriz de respuesta detalla cada caso. Las dependencias de M2 son opcionales y no intervienen en el flujo. La versión de torch con soporte CUDA para Python 3.15 no funciona en el equipo de referencia, por lo que M2 se ejecuta en CPU, sin consecuencias para los resultados.

## 9. Calendario hasta el cierre

| Fechas | Actividad | Responsable |
|---|---|---|
| 6 a 11 nov | Juicios de los pares de desarrollo de M0, M1 y M2 | Investigador |
| 12 y 13 nov | Re-anotación ciega del primer lote, cálculo del acuerdo intra-anotador, decisión de criterios y congelación de la anotación 2.1 | Investigador |
| 13 a 15 nov | Rankings de M3 y M3-sin-orden, implementación de M4, juicios de sus candidatos y estimación de la potencia | Investigador |
| 16 y 17 nov | Congelación de los sistemas, juicios de prueba (unas 13 horas) y doble juicio parcial | Investigador y asesor |
| 18 y 19 nov | Ejecución única del test, ablaciones, control negativo e interpretabilidad | Investigador |
| 20 a 22 nov | Redacción del informe de Seminario II y preparación del paquete reproducible | Investigador |

## 10. Riesgos y limitaciones

| Riesgo o limitación | Tratamiento previsto |
|---|---|
| Circularidad: el investigador anota, diseña y juzga | Consultas fijadas antes de ejecutar los sistemas, juicio ciego y aleatorizado, y doble juicio parcial con el asesor. Se declarará como la limitación principal |
| Un solo anotador y un solo evaluador (D1) | Estudio piloto, con acuerdo intra-anotador y doble juicio parcial |
| Potencia con 30 consultas de prueba | Se estimará con los datos de desarrollo. Si no alcanza para detectar Δ = 0,03, el estudio se declarará sin potencia suficiente y se informará el intervalo obtenido |
| Carga de juicios: 345 pares de desarrollo, unos 1600 de prueba y unos 240 de T1 | Si no cabe en el calendario, se reducirá el número de consultas de prueba antes de abrir el test, nunca después |
| Calendario ajustado entre la re-anotación (12 y 13) y la congelación (16) | Las etapas intermedias quedan reproducibles y ningún ajuste usa datos de prueba |
| M3 asistido por anotación | Se declara: la comparación mide la utilidad del sistema, no la extracción automática |
| Revisión bibliográfica (BIB01 y S1.9) | Sin avance desde la auditoría. Las búsquedas nativas en Scopus y Web of Science se harán junto con la redacción de los capítulos 3 y 4 |

## 11. Decisiones tomadas por el investigador desde la auditoría

| Fecha | Decisión | Registro |
|---|---|---|
| 3 nov | D1: sin segundo anotador; estudio piloto con acuerdo intra-anotador | Plan de cierre |
| 3 nov | D3: esquema de anotación con bandas y estados de observabilidad | Protocolo de anotación |
| 5 nov | D6: dependencias y checkpoint de M2, con ejecución en CPU | `config/modelos.toml` y protocolo experimental |
| 5 nov | La guía y el vocabulario de anotación no cambian hasta cerrar la re-anotación | `config/anotacion.toml` |
| 5 y 6 nov | Grupos sobre el principal y el complementario, con cinco señales, unión de los pares dudosos y revisor y fecha obligatorios | `config/grupos.toml` |
| 6 nov | Consolidado v2.0 sin la anotación, que se incorporará en la versión 2.1 | README y `config/corpus.toml` |
| 6 nov | Sorteo de las consultas T3 con la anotación del día, con regla de reemplazo | `config/experimento.toml` y protocolo experimental |
| 6 nov | M0 sin la descripción plantilla de MET; M1 sobre el textil segmentado | `config/modelos.toml` y protocolo experimental |
| 6 nov | M3 sin color ni motivo principal, con pesos iniciales iguales | `docs/especificacion_m3.md` |
| 6 nov | D7: auditoría versionada en `docs/auditoria_2026-10-20/`; integración continua después del 22 de noviembre | Plan de cierre |
