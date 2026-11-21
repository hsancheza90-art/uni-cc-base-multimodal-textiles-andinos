# 6. Implementación

> **Borrador 0.1, 21 de noviembre de 2026.** Capítulo de la segunda parte de la tesis. Describe la implementación con que se construyeron el corpus, la anotación y los sistemas, y con que se ejecutará la evaluación. Recoge las interfaces que el primer avance presentaba en su capítulo 5 (ecuaciones 5.61 a 5.65), que pasan aquí porque son implementación y no formalización. Las cifras corresponden al estado del repositorio al 21 de noviembre de 2026.

## 6.1 Propósito

Un experimento de recuperación con juicios humanos es reproducible solo si cada número que se informa puede regenerarse a partir de las decisiones que lo produjeron. En este estudio esas decisiones son de tres tipos: humanas (qué pieza entra al corpus, cómo se anota, qué grupos se unen, qué grado recibe cada par), de configuración (umbrales, semillas, pesos) y de datos externos (respuestas de los museos, imágenes, vectores del codificador visual). La implementación se organizó para que las tres queden registradas en archivos versionados y para que todo lo demás se derive de ellas por un procedimiento único, sin intervención manual y sin acceso a la red.

El capítulo describe los principios de esa organización (sección 6.2), su estructura (6.3), el flujo que regenera el corpus y los resultados de desarrollo (6.4), los pasos que quedan fuera de él (6.5), la implementación de los sistemas y de la evaluación (6.6 y 6.7), el tratamiento de las decisiones humanas y de la ceguera del evaluador (6.8), la verificación (6.9), el entorno (6.10) y lo que falta implementar antes de ejecutar la prueba (6.11).

## 6.2 Principios

La implementación responde a ocho reglas, que funcionan como restricciones de diseño y que las pruebas automáticas hacen cumplir.

1. **Las decisiones humanas viven en libros de cálculo.** Cada decisión de curación, de agrupamiento, de anotación o de relevancia se registra en un libro de Excel con su autor y su fecha. Ningún archivo derivado se edita a mano, y ningún programa escribe una decisión humana.
2. **Todo lo derivado se regenera.** Un único punto de entrada reconstruye, sin red, todos los archivos derivados a partir de los libros y de los insumos versionados.
3. **Los conteos están fijados.** Un archivo de configuración declara cuántas filas debe tener cada salida, y cada cambio lleva un comentario con su fecha y su motivo. El flujo termina con error si un conteo no coincide, de modo que un cambio curatorial no pasa inadvertido.
4. **Cada responsabilidad tiene un solo lugar.** Las rutas de cada fuente, la lectura de libros, la lectura y escritura de archivos y la lectura de la configuración se implementan una sola vez.
5. **Lo que necesita red o imágenes locales queda fuera del flujo.** Esos pasos escriben insumos versionados, que el flujo solo lee.
6. **Lo congelado no se modifica.** La serie del primer avance y la anotación v2.1 se leen de copias congeladas, verificadas por sus sumas SHA-256.
7. **Determinismo.** Todo muestreo usa una semilla fija y declarada; ningún archivo versionado contiene la fecha de ejecución; las salidas usan finales de línea LF.
8. **Cada salida tiene un informe.** Todo paso que cambia un archivo escribe un informe legible que explica qué cambió y por qué.

La regla 1 tiene una consecuencia que conviene explicitar. Las reglas automáticas (por ejemplo, descartar una pieza de plumaria o mandar al complementario una fotografía monocroma) firman como revisor «auto», y el revisor humano puede corregirlas; una regla automática nunca reemplaza una decisión que el revisor ya tomó.

## 6.3 Estructura

El código está escrito en Python, en módulos ejecutables que exponen una función `main` y se invocan como `python -m paquete.modulo`. No se usan cuadernos interactivos.

**Cuadro 6.1.** Paquetes del código y su responsabilidad.

| Paquete | Responsabilidad |
|---|---|
| `collectors` | Recolección desde las interfaces públicas de MET, CMA y AIC (con red) |
| `preprocessing` | Filtros de evidencia textil y andina, normalización y estructura común de los libros de revisión |
| `metadata` | Construcción de las salidas de MET, auditorías y aplicación de la revisión manual de cada fuente |
| `imagenes` | Descarga de copias de evaluación, medidas de imagen, calibración y aplicación del puntaje de aptitud |
| `consolidado` | Esquema armonizado y construcción de los consolidados v1 y v2 |
| `anotacion` | Corpus principal v2, núcleo de anotación, libros de anotación, validación, acuerdo intra-anotador, revisión de criterios y congelación |
| `grupos` | Candidatos a duplicado y grupos de piezas relacionadas |
| `modelos` | Sistemas M0 a M4 y lectura de los vectores del codificador visual |
| `experimento` | Particiones, consultas, rankings, pool de juicios, selección de pesos, efecto mínimo detectable, sensibilidad y métricas |
| `review` | Galerías HTML locales para la revisión visual |
| `utils` | Registro de fuentes, lectura de libros, lectura y escritura de archivos, configuración, vocabulario, métricas de acuerdo, fechas y texto |

La configuración se reparte en archivos TOML por ámbito: conteos esperados (`corpus.toml`), vocabulario controlado (`vocabulario.toml`), anotación (`anotacion.toml`), puntaje de aptitud (`aptitud.toml`), grupos (`grupos.toml`), experimento (`experimento.toml`) y sistemas (`modelos.toml`). Una prueba automática comprueba que los parámetros numéricos de `experimento.toml` coinciden con los del protocolo experimental, de modo que el documento y el código no pueden divergir sin que la prueba falle.

## 6.4 Flujo reproducible

El punto de entrada `python -m src.flujo` ejecuta 27 pasos en un orden fijo y termina con una verificación de conteos. Si un paso devuelve un código distinto de cero, el flujo se detiene. El Cuadro 6.2 agrupa los pasos por etapa.

**Cuadro 6.2.** Etapas del flujo reproducible.

| Etapa | Pasos | Insumos | Salidas principales |
|---|---|---|---|
| Curación por fuente | 1–6 | Candidatos de cada museo y libros de revisión | Subconjuntos principal, complementario y descartados de MET, CMA y AIC, con sus informes |
| Puntaje de aptitud | 7–9 | Medidas de imagen y decisiones del revisor | Modelo calibrado, puntaje por imagen e informe de calibración |
| Serie del primer avance | 10–13 | Copias congeladas y vocabulario congelado | Taxonomía, anotación v1, consolidado MET+CMA v1 y comparación de filtros |
| Corpus v2 y anotación | 14–18 | Subconjuntos revisados, dHash, libros de grupos y de anotación | Principal v2, núcleo de anotación, grupos, consolidado v2, anotación exportada |
| Congelación | 19 | Copia congelada de la anotación v2.1 y sus sumas | Comprobación de que la exportación no cambió |
| Experimento de desarrollo | 20–26 | Particiones, consultas, vectores de M1 y M2, juicios de desarrollo | Comprobación de fugas, rankings de desarrollo, pool, selección de pesos de M4, efecto mínimo detectable, sensibilidad de la anotación, consultas T1 |
| Estabilidad de la anotación | 27 | Primera anotación y re-anotación del lote 1 | Informe de acuerdo intra-anotador |

Con un equipo de escritorio, el flujo completo tarda unos segundos.

Tres propiedades del flujo son las que sostienen la reproducibilidad del estudio:

- **Idempotencia.** Ejecutar el flujo dos veces sobre los mismos insumos produce archivos idénticos byte a byte.
- **Aislamiento de lo congelado.** La serie v1 lee sus insumos de copias congeladas y se regenera idéntica aunque cambien los libros de la v2. La anotación v2.1 se compara en cada ejecución con su copia congelada: si un libro de anotación cambia después de la congelación, el flujo termina con error.
- **Ceguera por construcción.** Los pasos del experimento solo procesan las consultas de desarrollo. Ningún paso del flujo ejecuta un sistema sobre las consultas de prueba.

## 6.5 Pasos fuera del flujo

Los pasos que dependen de la red, de las imágenes locales o de una decisión humana se ejecutan por separado y escriben insumos versionados. Ninguno sobrescribe un archivo con decisiones manuales salvo con una opción explícita (`--forzar`).

**Cuadro 6.3.** Pasos fuera del flujo.

| Paso | Por qué queda fuera | Insumo versionado que escribe |
|---|---|---|
| Colectores de MET, CMA y AIC | Necesitan red | Listas de candidatos con los textos originales de la fuente |
| Descarga de copias de evaluación | Necesita red | Manifiesto de imágenes con sumas SHA-256 (las imágenes no se versionan) |
| Medidas de imagen y huella perceptual (dHash) | Necesitan las imágenes locales | Tablas de medidas y de dHash |
| Características de M1 | Necesitan las imágenes locales | Matriz de histogramas de color y textura con su índice |
| Vectores de M2 | Necesitan las imágenes y el modelo (unos 600 MB de dependencias) | Matriz de vectores, índice y manifiesto con las sumas de los pesos y las versiones |
| Generadores de libros (`--crear`) | Preparan el trabajo del revisor; conservan lo ya escrito | Libros de revisión, de anotación, de grupos, de consultas T1 y de juicios |
| Sorteo de particiones y consultas | Se ejecuta una sola vez | Particiones y consultas T3 |
| Congelación de la anotación | Se ejecuta una sola vez y se niega si hay pendientes | Copia congelada v2.1 y sus sumas |

Los vectores de M2 merecen una nota. Se calcularon en CPU, con precisión fp32, porque la compilación con GPU de la biblioteca de aprendizaje profundo no cargaba en el equipo disponible. El cálculo comprueba su propio determinismo: recalcula una muestra de 32 piezas y exige una diferencia máxima de 10⁻⁵ por componente entre pasadas. El manifiesto registra las sumas SHA-256 de los archivos de pesos y las versiones de las bibliotecas, de modo que una ejecución posterior puede verificar que usa el mismo punto de control. El flujo y las pruebas leen los vectores ya calculados y no necesitan esas dependencias.

## 6.6 Implementación de los sistemas

Los sistemas se implementaron en funciones puras, sin lectura ni escritura de archivos, que reciben datos ya cargados y devuelven puntuaciones. La construcción de los rankings, en un módulo aparte, lee los insumos, llama a cada sistema y escribe el ranking completo de cada consulta.

**M0.** BM25 de Okapi implementado directamente, sin bibliotecas de recuperación, con idf = ln((N − n + 0,5) / (n + 0,5) + 1). El documento de cada pieza es la unión de los campos configurados, normalizados a minúsculas y sin tildes; los términos son secuencias de letras y dígitos de al menos tres caracteres. La implementación propia evita depender de las decisiones de tokenización de una biblioteca externa y deja visible cada componente de la fórmula.

**M1.** Histogramas de color en CIELAB y de patrones binarios locales invariantes a la rotación, calculados con NumPy y Pillow sobre la máscara del textil que produce la segmentación del puntaje de aptitud. La disimilitud por bloque es la mitad de la distancia L1 entre histogramas normalizados, en [0, 1].

**M2.** Lectura de los vectores congelados y similitud coseno entre vectores normalizados. El encuadre con relleno cuadrado, la arquitectura y los pesos se declaran en la configuración.

**M3.** Las funciones del descriptor siguen la formalización del capítulo 5: `reverso` (la reversión), `tramos` y `sin_lagunas` (tratamiento de las lagunas), `histograma_tipos` e `histograma_adyacencias`, `distancia_edicion` y `distancia_palabras` (distancia normalizada entre palabras), `descriptor` (bloques y máscara de observabilidad), `distancias_por_bloque` y `comparar` (disimilitud mixta, cobertura y contribuciones de cada bloque). La invariancia a la reversión no se obtiene canonizando cada palabra, sino comparando una palabra con la otra y con su reverso y tomando la menor de las dos distancias, que es la distancia entre órbitas del capítulo 5; la función `canonizar`, que calcula la forma canónica, se usa en las pruebas que verifican la invariancia y el conteo de órbitas. El control sin orden es la misma función con un argumento que sustituye la palabra por el histograma de tipos y omite las adyacencias, de modo que ambos sistemas comparten todo el código salvo esa diferencia. La correspondencia completa entre fórmulas, funciones y pruebas está en el capítulo 5, sección 5.15.

**M4.** `normalizar` (mínimo y máximo por consulta), `pesos_efectivos` (reparto del peso de un componente sin evidencia), `fusionar` (puntuación y contribuciones) y `posiciones_reciprocas` (variante M4-RRF). La selección de pesos usa `rejilla`, que enumera las combinaciones normalizadas, y `elegir`, que aplica la regla del protocolo con sus criterios de desempate.

**Rankings y reproducibilidad de la fusión.** Los rankings de desarrollo se escriben con las puntuaciones redondeadas a seis decimales. M4 se calcula sobre esas mismas puntuaciones redondeadas, no sobre las de precisión completa, de modo que la fusión puede reproducirse exactamente desde el archivo versionado; una prueba lo comprueba. Los empates se resuelven por identificador.

## 6.7 Implementación de la evaluación

Las métricas y las pruebas estadísticas están en un módulo de funciones puras que no lee consultas ni juicios por su cuenta: quien las llama decide qué datos les pasa. Esta separación permite probarlas con ejemplos construidos a mano y garantiza que ninguna función de evaluación acceda por error a datos de prueba.

**Cuadro 6.4.** Funciones de evaluación.

| Función | Qué calcula |
|---|---|
| `ndcg`, `precision`, `rango_reciproco` | nDCG@k, precisión y rango recíproco; un candidato sin juicio cuenta como 0 y un par `no_evaluable` se retira del ranking y del ideal |
| `proporcion_juzgada`, `sin_aportes_unicos` | Proporción juzgada del top k y métrica sin los pares que solo aportó un sistema |
| `diferencias` | Diferencias pareadas por consulta, excluyendo las consultas sin relevantes |
| `permutacion_pareada` | Prueba de permutación por cambio de signo, bilateral, con semilla fija |
| `t_pareada` | t de Student pareada como comprobación |
| `intervalo_bootstrap` | Intervalo de percentiles por bootstrap pareado |
| `decidir`, `comparar` | Aplicación de la regla de decisión de H1 y H2 |
| `efecto_minimo_detectable`, `consultas_necesarias`, `rango_desviacion` | Planificación de la potencia (capítulo 7, sección 7.8) |

La distribución t se calcula mediante la función beta incompleta regularizada, implementada en el propio módulo, para no añadir una biblioteca de estadística a las dependencias del flujo.

## 6.8 Decisiones humanas y ceguera del evaluador

Cada tipo de decisión humana tiene su libro, con una estructura común: columnas de contexto que el revisor no edita, columnas de decisión con listas de valores válidos, y columnas de revisor y fecha obligatorias. El flujo valida cada libro antes de usarlo: un valor fuera del vocabulario, una fila sin identificador o un identificador repetido detienen la ejecución sin modificar ninguna salida.

El libro de juicios de relevancia se diseñó para sostener la ceguera del evaluador. Presenta los pares de cada consulta en orden aleatorio, sin el sistema que los propuso, su posición ni su puntuación; las imágenes se muestran en una galería local que no se versiona. El archivo que registra qué sistema aportó cada par al pool existe, pero el evaluador no lo abre, y los informes que contienen el rendimiento de los sistemas en desarrollo llevan esa advertencia. Los libros de consultas T1 y de juicios incluyen una hoja de ejemplos hipotéticos que ilustran el formato y la escala sin usar piezas de la galería.

Los generadores de libros conservan lo ya escrito: al regenerar un libro para añadir filas nuevas, por ejemplo los pares que aportó un sistema incorporado después, se mantienen los juicios existentes y solo se agregan los pendientes.

## 6.9 Verificación

La batería de pruebas reúne 460 casos en 19 archivos. Se agrupan en cinco clases.

**Cuadro 6.5.** Pruebas automáticas por clase.

| Clase | Qué comprueba | Casos |
|---|---|---:|
| Regeneración | Que cada salida versionada se regenera idéntica, con finales LF, y que los conteos coinciden con la configuración; que una revisión con errores termina con código 1 sin reemplazar salidas; que los generadores no sobrescriben decisiones | 120 |
| Curación, aptitud y consolidados | Filtros de evidencia textil y andina, reglas y calibración del puntaje, esquema y construcción de los consolidados, colectores | 144 |
| Anotación | Validación de la anotación v1 y v2, estados de observación, revisión de criterios, congelación y grupos | 78 |
| Sistemas | Propiedades del descriptor y de la fusión: invariancia de la forma canónica, conteo de órbitas, simetría y cotas de la disimilitud, contraejemplos de la desigualdad triangular, descomposición exacta, intervención, renormalización, posiciones recíprocas | 86 |
| Experimento y evaluación | Particiones y consultas sin fugas, coherencia del protocolo con la configuración, métricas con ejemplos calculados a mano, pruebas estadísticas, selección de pesos, efecto mínimo detectable y sensibilidad | 32 |

Las pruebas de propiedades de M3 y M4 cumplen una función adicional: fijan los enunciados **[P]** del capítulo 5 y los contraejemplos de la proposición 5.8, de modo que una afirmación contraria no puede introducirse en el código sin que una prueba falle. Dos enunciados no tienen prueba automática: la cota del control sin orden (proposición 5.6), comprobada por enumeración, y las condiciones de buena formación B3 a B7 de la anotación (capítulo 5, sección 5.4.1), verificadas al congelar la anotación pero no convertidas en reglas de validación.

Antes de cada entrega se ejecuta una verificación en una copia limpia del repositorio: se clona, se instalan las dependencias fijadas, se ejecutan el flujo y las pruebas, y se comprueba que el árbol de trabajo queda sin cambios. Esa verificación detectó, por ejemplo, un informe que había quedado desactualizado tras incorporar juicios nuevos.

## 6.10 Entorno y dependencias

El flujo y las pruebas requieren Python 3.11 o superior y cuatro bibliotecas: NumPy, openpyxl, Pillow y requests. Sus versiones exactas están fijadas en `requirements.txt` y los rangos compatibles en `pyproject.toml`; la verificación de referencia se hizo con Python 3.15.2. Las dependencias del codificador visual (PyTorch, OpenCLIP y sus requisitos) están en un archivo separado, `requirements-modelos.txt`, porque solo las necesita el cálculo de los vectores de M2, que queda fuera del flujo.

El número reducido de dependencias es deliberado. Cada biblioteca añadida es un punto en que la regeneración puede dejar de ser idéntica al cambiar de versión, y las operaciones que el estudio necesita (BM25, histogramas, distancias de edición, pruebas de permutación, bootstrap) son lo bastante simples para implementarlas y probarlas directamente.

## 6.11 Pendiente de implementación antes de la prueba

A la fecha de este borrador, la implementación cubre todo lo necesario hasta el final de la fase de desarrollo. Antes de abrir la prueba deben implementarse y verificarse con datos de desarrollo, sin ejecutar ninguna consulta de prueba:

1. El **manifiesto de ejecución**, que registra el commit, las sumas SHA-256 de todos los insumos, el punto de control de M2, los parámetros, el equipo y las semillas.
2. La **comprobación previa** de las condiciones de suspensión del capítulo 7 (sección 7.12).
3. La **generación del pool y del libro de juicios de prueba**, con la misma estructura ciega que los de desarrollo.
4. El **cálculo final** de H1, H2 (con su análisis secundario) y H3, de las ablaciones, del control negativo y de los análisis por museo, a partir de los juicios de prueba.
5. La **prueba automática de la proposición 5.6** y las **reglas de validación B3 a B7**.

El objetivo es que el día en que se abra la prueba no haya que escribir código nuevo: el test se ejecuta con un solo comando, sobre un código ya verificado, cuando ya no puede corregirse nada.

## 6.12 Cierre del capítulo

La implementación traduce las exigencias metodológicas de los capítulos 4, 5 y 7 a restricciones verificables: las decisiones humanas quedan en libros con autor y fecha, todo lo derivado se regenera de forma idéntica, lo congelado se comprueba en cada ejecución y las propiedades del descriptor y de la fusión están fijadas en pruebas. Su principal virtud para la tesis no es la eficiencia, que en una galería de 150 piezas es irrelevante, sino que cualquier cifra del manuscrito puede rastrearse hasta la decisión que la produjo.
