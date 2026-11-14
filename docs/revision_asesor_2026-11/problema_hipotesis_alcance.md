# Problema, objetivos, hipótesis y alcance

Propuesta de redacción al 13 de noviembre de 2026, en respuesta al punto 2 del informe integrado del asesor. Es coherente con la sección 1 del protocolo experimental (versión 0.6.1) y no la modifica. Los objetivos se redactaron a partir del protocolo; deben conciliarse con los del primer avance de tesis, que no se corrige, y las diferencias se anotarán en `docs/notas_para_tesis.md`. Las referencias remiten a las fichas de `docs/revision_bibliografica_2026-11/fichas/`.

## 1. Problema

Buena parte del diseño textil andino prehispánico se organiza en unidades que se repiten y se ordenan sobre la superficie: listas y franjas, paneles, retículas, cenefas y campos centrales. Esa organización es visible en una fotografía de museo y es, para quien estudia las piezas, un criterio habitual de comparación: dos tejidos pueden parecerse por la disposición de sus bandas aunque difieran en color, en iconografía o en estado de conservación.

Las colecciones digitales de los museos ofrecen dos vías de acceso a estas piezas, y ninguna recoge esa organización. Las fichas describen material, técnica, cultura atribuida y fecha, con un vocabulario heterogéneo entre instituciones. Los codificadores visión-lenguaje preentrenados producen representaciones generales de la imagen, pero la evidencia disponible indica que tratan el contenido de forma cercana a una bolsa de elementos: en pruebas diseñadas para ello, CLIP acierta el 56 % de las relaciones espaciales entre objetos, con el azar en 50 % (Yuksekgonul et al., 2023; F01), y queda por debajo del azar cuando dos imágenes solo difieren en la disposición de los mismos elementos (Thrush et al., 2022; F02). Esa evidencia procede de la correspondencia entre texto e imagen en fotografías naturales. No demuestra que ocurra lo mismo al comparar un textil con otro; motiva la pregunta, y esta tesis la pone a prueba.

Por otra parte, la recuperación por estructura textil tiene antecedentes, pero a otra escala. Helmer y Ngo (2015; F10) y Ngo et al. (2021; F11) recuperan tejidos por la estructura de sus cruces de hilos, modelada a mano para cada pieza, y los evalúan contra categorías de tejido. En los trabajos de recuperación patrimonial revisados, la relevancia se toma de la identidad de la pieza o de sus metadatos, y rara vez de un juicio humano (F03, F05, F12, F18). En la búsqueda realizada, de alcance parcial, no se encontró un estudio que evalúe con juicios humanos graduados y ciegos si la organización visible de un textil añade utilidad de recuperación a un codificador visión-lenguaje congelado. Queda sin leer, por falta de acceso, el trabajo de Brownlow et al. (2015), que es uno de los que con más probabilidad se aproximan; por ello la ausencia de antecedentes se afirma solo respecto de lo recuperado.

El problema es, entonces, de representación y de evidencia: cómo formalizar la organización visible de un textil de modo que pueda compararse entre piezas, y cómo comprobar, con un diseño que no favorezca al método propuesto, si esa representación aporta algo que las señales textuales y visuales generales no aportan ya.

## 2. Pregunta de investigación

> En un conjunto congelado de textiles andinos fotografiados por museos, ¿añadir el orden de las bandas y las relaciones entre regiones, mediante un descriptor estructural derivado de anotación humana, mejora la recuperación por similitud estructural respecto de las señales textuales y visuales generales, según juicios humanos independientes de los sistemas? ¿Permite, además, explicar el ranking de forma fiel?

La pregunta es contrastable porque fija los términos de la comparación: los sistemas (M4 frente a M2; M3 frente a su control sin orden), la tarea (recuperación por ejemplar, T3), la medida (nDCG@10 por consulta) y el árbitro (juicios humanos ciegos en una escala de cuatro grados).

## 3. Objetivos

**Objetivo general.** Determinar si un descriptor de la macroestructura visible de los textiles andinos, que considera el orden de las bandas y las relaciones entre regiones, aporta utilidad a la recuperación por similitud estructural frente a representaciones textuales y visuales generales, y si su aporte puede explicarse de forma fiel.

**Objetivos específicos.**

| | Objetivo | Producto verificable | Estado |
|---|---|---|---|
| OE1 | Construir y documentar un corpus multimodal de textiles andinos de colecciones abiertas, con criterios de selección explícitos y agrupación de las piezas relacionadas | Corpus v2.0 con grupos, licencias y sumas de verificación | Cumplido |
| OE2 | Formalizar la macroestructura observable y anotarla con un protocolo que registre lo que no puede observarse, midiendo la estabilidad de la anotación | Esquema de anotación, anotación v2.1 e informe de estabilidad | En curso |
| OE3 | Definir un descriptor estructural y una disimilitud entre piezas, con sus propiedades demostradas o verificadas, y un control que aísle el efecto del orden | Especificación de M3, M3-sin-orden y pruebas de propiedades | Cumplido en el diseño; rankings pendientes |
| OE4 | Evaluar, con un protocolo fijado de antemano y juicios humanos ciegos, la utilidad del descriptor solo y en fusión con texto e imagen, frente a un codificador visión-lenguaje congelado | Resultados por consulta, con intervalos, ablaciones y control negativo | Pendiente |
| OE5 | Comprobar que la puntuación del sistema combinado se descompone exactamente en las contribuciones de sus componentes | Reconstrucción e intervención sobre los resultados de prueba | Pendiente |

## 4. Hipótesis

Las tres hipótesis se formulan sobre resultados observables. Para cada una se indica qué resultado la sostendría y cuál no.

**H1 (primaria).** La fusión que incorpora la estructura recupera mejor que el codificador visión-lenguaje congelado: la diferencia media por consulta de nDCG@10 entre M4 y M2 en T3 es positiva e igual o superior a 0,03.

**H2 (mecanismo).** El orden importa: el descriptor con secuencia de bandas y adyacencias (M3) obtiene mejor nDCG@10 que el mismo descriptor reducido al histograma de tipos de banda (M3-sin-orden).

**H3 (fidelidad de la explicación).** La puntuación de M4 para cada par es exactamente la suma de las contribuciones de sus componentes, y retirar un componente la modifica como predice la fórmula.

H3 es una afirmación sobre el algoritmo. En los términos de Jacovi y Goldberg (2020; F27), se refiere a la fidelidad de la explicación (que describa lo que el sistema calcula) y no a su plausibilidad (que resulte convincente para una persona). M4 es un modelo aditivo que produce su propia explicación, en el sentido que defiende Rudin (2019; F28). Que la contribución estructural a un ranking sea exacta no dice nada sobre el significado cultural de las bandas ni sobre las razones por las que un tejedor las dispuso así. Esa interpretación queda fuera de la tesis.

## 5. Correspondencia entre hipótesis y prueba

| | Variable de resultado | Comparación | Unidad de análisis | Prueba y regla de decisión | Artefacto | Veredictos posibles |
|---|---|---|---|---|---|---|
| H1 | nDCG@10 en T3 | M4 − M2, pareada por consulta | 30 consultas de prueba | Permutación pareada bilateral, 10 000 réplicas, α = 0,05; IC 95 % por bootstrap pareado. Sostenida si Δ ≥ 0,03 y p < 0,05 | `comparar` y `decidir` en `src/experimento/evaluacion.py` | Sostenida; dirección favorable sin evidencia suficiente; no sostenida |
| H2 | nDCG@10 en T3 | M3 − M3-sin-orden, mismas consultas y candidatos | 30 consultas de prueba | La misma regla | El mismo; `comparar(..., sin_orden=True)` en `src/modelos/m3_estructura.py` | Los mismos |
| H3 | Error de reconstrucción y efecto de retirar un componente | Puntuación frente a la suma de contribuciones | Cada resultado del top 10 de M4 en prueba | Error ≤ 1e-9 en todos los resultados; intervención conforme a la fórmula; revisión humana de 10 resultados | `fusionar` en `src/modelos/m4_fusion.py`; `tests/test_m4.py` | Sostenida; no sostenida |

La regla de decisión de H1 y H2 figura en el protocolo como propuesta (decisión R01) y requiere la conformidad del asesor, cuyo informe indicaba decidir por el intervalo de bootstrap. Las dos pruebas están implementadas.

H1 es la única comparación confirmatoria primaria y H2 la única secundaria. Las demás (frente a M0 y M1, ablaciones, análisis por museo, T1) son exploratorias y se presentarán como tales.

## 6. Contribución

La contribución se define por el método y por la evidencia, no por el número de técnicas empleadas.

1. **Una formalización de la macroestructura observable** de un textil a partir de su fotografía: una palabra de bandas sobre un alfabeto finito, considerada salvo reversión, sus adyacencias, un conjunto de atributos de región y una máscara que distingue lo ausente de lo que no pudo observarse. Se sitúa en una escala distinta de la estructura de hilos de Helmer y Ngo (F10, F11) y no adopta la clasificación por grupos de simetría, que Frame (2006; F13) considera inadecuada para parte de los patrones andinos.
2. **Un descriptor y una disimilitud** definidos sobre esa formalización, con propiedades demostradas o verificadas por pruebas, y un control sin orden que permite atribuir una eventual diferencia a la secuencia y no a la composición por tipos.
3. **Una evaluación controlada** de su utilidad en un corpus museográfico: partición por grupos de piezas relacionadas, consultas fijadas antes de ejecutar los sistemas, juicios humanos graduados y ciegos, una sola ejecución de prueba y un control negativo.

Estas contribuciones no dependen del signo del resultado. Si H1 o H2 no se sostienen, la tesis aporta una medición controlada de que, en este corpus y con este descriptor, la estructura anotada no añade utilidad apreciable a un codificador general. Existe un precedente andino en ese sentido: en khipus, Contreras (2026; F14, prepublicación sin arbitraje) no halló que el orden de los tipos de nudo mejorase la clasificación frente a rasgos agregados.

## 7. Alcance de las conclusiones

**Población.** La colección digital elegible del corpus principal v2: piezas de tres museos estadounidenses (MET, CMA y AIC), con imagen de dominio público, seleccionadas con el criterio de aptitud v2. El experimento se realiza sobre un núcleo de 150 piezas. La población no es «los textiles andinos»: está determinada por lo que esos museos adquirieron, fotografiaron y publicaron, y por un criterio que privilegia piezas cuyos colores y figuras se distinguen a primera vista.

**Comparabilidad de los sistemas.** M3 y M4 son sistemas asistidos por anotación: disponen de etiquetas asignadas por una persona. M2 opera solo sobre los píxeles. Una mejora de M4 respaldaría la utilidad del conocimiento estructural aportado por anotación humana. No respaldaría que ese conocimiento pueda extraerse automáticamente, ni que un método de extracción sea superior a otro.

**Lo que la tesis no afirma.**

- No interpreta el significado de los motivos ni atribuye cultura, función o cronología.
- No sostiene que la palabra de bandas describa cómo se concibió el diseño. Es una codificación elegida por el investigador a partir de lo visible en una fotografía.
- No mide la estructura técnica del tejido (ligamento, dirección de la urdimbre, número de hilos).
- No generaliza a piezas de otras colecciones, a otras condiciones fotográficas ni a tradiciones textiles distintas.
- No presenta la fidelidad de H3 como explicación causal o cultural.

**Resultado negativo o inconcluso.** La pregunta y los objetivos se mantienen cualquiera que sea el resultado. Con 30 consultas de prueba, el estudio tiene alcance de piloto: la estimación previa con los datos de desarrollo indica que solo podrá detectar con fiabilidad diferencias de nDCG@10 del orden de 0,10 o mayores. Un efecto positivo menor se informará como «dirección favorable sin evidencia suficiente», con su intervalo, y no como confirmación ni como refutación.

## 8. Gobernanza del corpus

Las imágenes se usan bajo licencia CC0 o dominio público. Ese permiso legal no responde por sí solo a las preguntas de los principios CARE sobre datos de origen indígena (Carroll et al., 2020; F23): buena parte de los textiles andinos conservados en museos procede de contextos funerarios, y ninguna comunidad de origen participó en su descripción. La tesis lo declara como límite y documenta el corpus con la estructura de las fichas de conjunto de datos (Gebru et al., 2021; F25).

## Referencias citadas

Las entradas completas están en `docs/revision_bibliografica_2026-11/referencias.bib`: `yuksekgonul_2023_aro` (F01), `thrush_2022_winoground` (F02), `helmer_ngo_2015_similitud_tejidos` (F10), `ngo_2021_hipergrafos` (F11), `frame_2006_pathways` (F13), `contreras_2026_khipus` (F14), `carroll_2020_care` (F23), `gebru_2021_datasheets` (F25), `jacovi_goldberg_2020_fidelidad` (F27), `rudin_2019_modelos_interpretables` (F28).
