# Informe de avance: segunda parte de la tesis

6 de noviembre de 2026. Estado del repositorio en `main`, con el corpus de referencia en la etiqueta `corpus-met-cma-aic-v2.0`. Las cifras son las de los informes que genera el flujo (`outputs/reports/`); los conteos que el flujo verifica en cada ejecución están en `config/corpus.toml`.

## 1. Resumen

- **Corpus:** el corpus v2 (MET, CMA y AIC) quedó cerrado y consolidado, con 615 registros en 577 grupos de piezas relacionadas decididos por el investigador.
- **Anotación:** el núcleo de 150 piezas está anotado con el esquema ampliado (bandas y estados) y validado. Falta medir su estabilidad con la re-anotación ciega del lote 1, que empieza el 12 de noviembre.
- **Protocolo:** está redactado (v0.4) y pendiente de su aprobación. Las particiones de desarrollo y prueba y las 40 consultas T3 están congeladas y sin fugas. Las 6 consultas T1 están redactadas.
- **Sistemas:** M0, M1 y M2 están implementados y tienen rankings de desarrollo. M3 está especificado, implementado y probado, y sus rankings esperan la anotación congelada (v2.1). Falta implementar M4.
- **Juicios:** el pool de desarrollo (345 pares, ciego) está listo para juzgar. Todavía no hay ninguna métrica de recuperación, ni se ejecutó ninguna consulta de prueba.

## 2. Corpus y versiones

| Versión | Contenido | Estado |
|---|---|---|
| `corpus-met-cma-v1.2` | Consolidado MET+CMA, 288 registros | Congelado; respaldo del primer avance. Se regenera idéntico desde copias congeladas |
| Corpus v2, decisiones | 874 registros de MET, CMA y AIC con decisión de procedencia manual y automática: 462 principal, 153 secundario y 259 descartados | Cerrado |
| `corpus-met-cma-aic-v2.0` | Consolidado v2: principal y complementario de las tres fuentes, 615 registros (MET 130 + 25, CMA 104 + 4, AIC 228 + 124), con grupo, licencias por fuente, manifiesto de imágenes y SHA-256 | Etiquetado el 6 de noviembre. Sin anotación estructural, que entra en la v2.1 |

Documentos: resumen en `outputs/reports/corpus_textiles_andinos_met_cma_aic_v2_resumen.md`; esquema en `docs/esquema_consolidado_met_cma_aic_v2.md`. Las imágenes de las tres fuentes son CC0 o de dominio público. La descripción de AIC es CC BY 4.0 y se cita.

## 3. Unidad experimental: grupos de piezas relacionadas (DAT01, DAT02)

Los pares candidatos a «mismo objeto» se proponen con cinco señales sobre el principal y el complementario. Un par puede tener varias:

| Señal | Pares |
|---|---:|
| Imagen idéntica | 13 |
| Inventario con la misma base y sufijo de parte (`1922.395.a`, `.b`…) | 52 |
| Descripción curatorial idéntica | 41 |
| dHash de la copia de evaluación (≤ 4) | 18 |
| M2, coseno ≥ 0,95 (≥ 0,93 entre museos) | 28 |
| **Pares distintos** | **100** |

- **Decisiones:** el investigador decidió los 100 pares en `data/metadata/grupos_revision_v2.xlsx`, con revisor y fecha obligatorios: 65 unir (13 de imagen idéntica, propuestos automáticamente) y 35 separar. La regla `no_seguro` = unir existe para evitar fugas, pero no se usó.
- **Grupos:** 577 para 615 registros (555 de una pieza, 15 de dos, 2 de tres, 3 de cuatro y 1 de cinco). El núcleo queda en 146 grupos.
- **Verificación de M2:** las 18 piezas con imagen compartida conocida tienen a su par como vecino más cercano (18 de 18).
- **Detalle:** `outputs/reports/grupos_v2.md`.

## 4. Anotación estructural (ANN01)

- **Esquema v2 (decisión D3):** 19 columnas. Se agregan `eje_bandas` y `secuencia_bandas`, la palabra de bandas con tipos `lisa`, `geometrica`, `figurativa`, `mixta`, `no_determinada` y `laguna`, sin color ni anchos. Los estados `ausente`, `no_observable` y `desconocido` van en la misma celda del atributo. Protocolo: `docs/protocolo_anotacion_v2.md`.
- **Núcleo:** 150 piezas (MET 42, CMA 34 y AIC 74), estratificadas en 5 lotes. Las anotó el investigador el 5 de noviembre.
- **Validación** (`outputs/reports/anotacion_v2_validacion.md`):
  - 0 errores.
  - 38 piezas con `desconocido` que no están en `revisar` (regla de los treinta segundos).
  - 3 correcciones iguales al valor vigente.
  - Las observaciones marcan 104 piezas con dudas, criterios o huecos del vocabulario por decidir.
- **Acuerdo:** no hay segundo anotador (D1), así que el lote 1 se re-anota a ciegas a partir del 12 de noviembre, en otro orden y al menos 7 días después de la primera anotación. Se medirá el acuerdo intra-anotador (kappa por atributo y similitud de edición en la palabra de bandas). Se informará como estabilidad de la anotación, no como acuerdo entre personas.
- **Criterios:** la guía y el vocabulario no cambian hasta cerrar la re-anotación. Después se deciden los criterios pendientes y la anotación se congela como v2.1, antes de congelar los sistemas.

## 5. Protocolo experimental y snapshot (MET01)

- **Protocolo:** `docs/protocolo_experimental_v2.md`, v0.4, propuesto. Hipótesis:
  - H1, primaria: M4 frente a M2 en nDCG@10.
  - H2, mecanismo: M3 frente a M3-sin-orden.
  - H3, interpretabilidad: reconstrucción e intervención.
  - Las tres llevan regla de decisión, umbral práctico, bootstrap pareado y criterios de suspensión del test.
- **Tareas:** T3, estructura por ejemplar, es la primaria; T1, texto a imagen, es secundaria y exploratoria.
- **Particiones** (`outputs/reports/experimento_v2_snapshot.md`): congeladas por grupo y estratificadas por museo, con 44 grupos de desarrollo (44 piezas) y 102 de prueba (106 piezas). El flujo comprueba en cada ejecución que ningún grupo esté en las dos particiones.
- **Consultas T3:** 10 de desarrollo y 30 de prueba, sorteadas con semilla, a lo sumo una por grupo y estratificadas por museo y composición. Hay una regla de reemplazo declarada para el caso de que la corrección de la anotación deje alguna sin composición observable.
- **Consultas T1:** 6, redactadas por el evaluador el 6 de noviembre, antes de ejecutar cualquier sistema sobre ellas.
- **Configuración:** los valores numéricos del protocolo están en `config/experimento.toml`, y una prueba comprueba que coinciden con el documento.

## 6. Sistemas (MOD01, MOD02, MAT01)

| Sistema | Estado | Notas |
|---|---|---|
| M0, BM25 | Implementado; rankings de desarrollo | Texto de la ficha. La descripción de MET no entra: es una plantilla armada con los metadatos (las 26 MET con descripción), no un texto del museo |
| M1, color y textura | Implementado; rankings de desarrollo | Histograma CIELAB y LBP sobre el textil, separado del fondo con la segmentación de la aptitud |
| M2, OpenCLIP | Implementado; rankings de desarrollo | `xlm-roberta-base-ViT-B-32` / `laion5b_s13b_b90k` (MIT), multilingüe, fp32, en CPU. Determinista: dos pasadas dan diferencia 0. Manifiesto con el hash de los pesos |
| M3, estructura | Especificado (`docs/especificacion_m3.md`), implementado y probado | Palabra de bandas canónica bajo reversión, adyacencias no dirigidas, máscara de observabilidad y disimilitud mixta con contribuciones exactas. Sin color. Rankings tras la v2.1 |
| M3-sin-orden | Implementado (control de H2) | Histograma de tipos en lugar de la palabra; sin adyacencias |
| M4, fusión | Pendiente (13 al 15 de noviembre) | Fusión tardía aditiva de M0, M2 y M3, con pesos de desarrollo |

Los rankings de desarrollo cubren las 10 consultas de desarrollo con 149 candidatos cada una, siempre sin el grupo de la consulta. Las consultas de prueba no se han ejecutado.

## 7. Consultas y juicios (ANN02)

- **Pool de desarrollo:** 345 pares (los 10 primeros de M0, M1 y M2 sin repetir, más 10 al azar por consulta) en `data/metadata/juicios_desarrollo_v2.xlsx`.
- **Juicio ciego:** los pares se presentan barajados, sin sistema ni posición, con una galería local de imágenes y ejemplos hipotéticos de la escala 0–3. El origen de cada par queda en un archivo que el evaluador no abre.
- **Crecimiento del pool:** se agregarán los candidatos de M3 y M4 sin repetir los pares ya juzgados.
- **Juicios de prueba:** con el mismo procedimiento, sobre un pool que se arma cuando los sistemas estén congelados.

## 8. Software y reproducibilidad (REP01, SW01–SW12)

- **Verificación:** el flujo tiene 23 pasos y no usa red; la suite tiene 350 pruebas. Cada commit desde la auditoría se verificó en un clon limpio, sin torch, con el flujo en 0, las pruebas en verde y el árbol sin cambios.
- **Decisiones humanas:** se leen de workbooks y se validan antes de exportar (revisor, fecha, códigos y escala). Un error detiene el flujo y no reemplaza las salidas.
- **Contratos de la auditoría:** SW01, SW02, SW04, SW05 y SW08 están corregidos y SW10 está mitigado en M0. SW03, SW06, SW07, SW09, SW11 y SW12 quedan diferidos según el plan (detalle en la matriz).
- **Dependencias de M2:** son opcionales y están fuera del flujo (`requirements-modelos.txt`). La compilación de torch con CUDA para Python 3.15 no carga en el equipo de referencia; M2 usa la compilación CPU, sin efecto en los resultados.

## 9. Calendario restante

| Fechas | Actividad | Responsable |
|---|---|---|
| 6 a 11 nov | Juicios del pool de desarrollo, con los 10 primeros de M0, M1 y M2 | Investigador |
| 12 y 13 nov | Re-anotación ciega del lote 1; acuerdo intra-anotador; decisión de criterios; anotación v2.1 congelada | Investigador |
| 13 a 15 nov | Rankings de M3 y M3-sin-orden; M4 con pesos de desarrollo; juicios de sus candidatos; estimación de la potencia | Investigador |
| 16 y 17 nov | Congelación de los sistemas (manifiesto); pool y juicios de prueba (unas 13 h); doble juicio parcial | Investigador y asesor |
| 18 y 19 nov | Ejecución única del test; ablaciones; control negativo; interpretabilidad | Investigador |
| 20 a 22 nov | Informe de Seminario II y paquete reproducible | Investigador |

## 10. Riesgos y limitaciones

| Riesgo o limitación | Tratamiento |
|---|---|
| Circularidad: el investigador anota, diseña y juzga | Consultas fijadas antes de ejecutar sistemas, juicio ciego y barajado, y doble juicio parcial del asesor. Se declara como limitación principal |
| Un solo anotador y un solo evaluador (D1) | Estudio piloto: acuerdo intra-anotador y doble juicio parcial |
| Potencia con 30 consultas de prueba | Se estima con desarrollo; si no alcanza para Δ = 0,03, se declara sin potencia suficiente y se informa el IC |
| Carga de juicios: 345 de desarrollo, unos 1600 de prueba y unos 240 de T1 | Si no cabe, se reducen las consultas de prueba antes de abrir el test, nunca después |
| Calendario ajustado: re-anotación el 12 y 13 y congelación el 16 | Las salidas parciales quedan reproducibles; no se ajusta nada con datos de prueba |
| M3 asistido por anotación | Declarado: mide utilidad del sistema, no extracción automática |
| Revisión bibliográfica (BIB01, S1.9) | Sin avance desde la auditoría. Las búsquedas nativas en Scopus y Web of Science quedan para los capítulos 3 y 4 |

## 11. Decisiones tomadas por el investigador desde la auditoría

| Fecha | Decisión | Dónde consta |
|---|---|---|
| 3 nov | D1: no hay segundo anotador; estudio piloto con acuerdo intra-anotador | Plan de cierre |
| 3 nov | D3: esquema de anotación con bandas y estados | Protocolo de anotación |
| 5 nov | D6: dependencias y checkpoint de M2; CPU | `config/modelos.toml`, protocolo |
| 5 nov | Guía y vocabulario fijos hasta cerrar la re-anotación | `config/anotacion.toml` |
| 5 y 6 nov | Grupos sobre el principal y el complementario; cinco señales; «unir ante la duda»; revisor y fecha obligatorios | `config/grupos.toml` |
| 6 nov | Consolidado v2.0 sin anotación; la anotación entra en la v2.1 | README, `config/corpus.toml` |
| 6 nov | Consultas T3 sorteadas con la anotación del día y regla de reemplazo | `config/experimento.toml`, protocolo |
| 6 nov | M0 sin la descripción plantilla de MET; M1 sobre el textil segmentado | `config/modelos.toml`, protocolo |
| 6 nov | M3 sin color ni `motivo_principal`; pesos iniciales iguales | `docs/especificacion_m3.md` |
