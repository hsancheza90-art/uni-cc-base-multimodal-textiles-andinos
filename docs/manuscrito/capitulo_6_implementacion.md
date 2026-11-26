# 6. Implementación

## 6.1 Propósito

Un experimento de recuperación con juicios humanos es reproducible solo si cada cifra que se informa puede regenerarse a partir de las decisiones que la produjeron. En este estudio esas decisiones son de tres tipos: humanas (qué pieza entra al corpus, cómo se anota, qué grupos se unen, qué grado recibe cada par), de configuración (umbrales, semillas, pesos) y de datos externos (respuestas de los museos, imágenes, vectores del codificador visual). La implementación se organizó para que las tres queden registradas en archivos versionados y para que todo lo demás se derive de ellas por un procedimiento único, sin intervención manual y sin acceso a la red. El detalle técnico de este capítulo está en el anexo A.

## 6.2 Principios

Ocho reglas funcionan como restricciones de diseño, y las pruebas automatizadas las hacen cumplir:

1. **Las decisiones humanas viven en libros de cálculo**, con su autor y su fecha. Ningún archivo derivado se edita a mano y ningún programa escribe una decisión humana.
2. **Todo lo derivado se regenera** desde un único punto de entrada, sin red, a partir de los libros y de los insumos versionados.
3. **Los conteos están fijados** en un archivo de configuración, con la fecha y el motivo de cada cambio; si uno no coincide, el flujo termina con error y un cambio curatorial no pasa inadvertido.
4. **Cada responsabilidad tiene un solo lugar**: las rutas de cada fuente, la lectura de libros, la lectura y escritura de archivos y la configuración se implementan una sola vez.
5. **Lo que necesita red o imágenes locales queda fuera del flujo** y escribe insumos versionados, que el flujo solo lee.
6. **Lo congelado no se modifica**: la serie del primer avance y la anotación v2.1 se leen de copias verificadas por sus sumas SHA-256.
7. **Determinismo**: semillas fijas y declaradas, ninguna fecha de ejecución en un archivo versionado y finales de línea LF.
8. **Cada salida tiene un informe** legible que explica qué cambió y por qué.

Las reglas automáticas de curación (por ejemplo, descartar una pieza de plumaria o enviar al conjunto complementario una fotografía monocroma) firman como revisor «auto», y el revisor humano puede corregirlas; una regla automática nunca reemplaza una decisión que el revisor ya tomó.

## 6.3 Arquitectura

El código está escrito en Python, en módulos ejecutables que se invocan desde la línea de órdenes, sin cuadernos interactivos. Los paquetes siguen las etapas del trabajo: recolección desde las interfaces de los tres museos, filtros y normalización, revisión manual de cada fuente, medidas de imagen y puntaje de aptitud, consolidados, anotación, grupos de piezas relacionadas, sistemas M0 a M4 y experimento, más un paquete de utilidades que concentra el registro de fuentes, la lectura de libros, la escritura de archivos y la configuración (anexo A, Cuadro A.1). La configuración se reparte en archivos por ámbito, y una prueba automatizada comprueba que los parámetros numéricos del experimento coinciden con los del protocolo experimental, de modo que el documento y el código no pueden divergir sin que la prueba falle.

## 6.4 Flujo reproducible

Un único punto de entrada ejecuta 27 pasos en un orden fijo, desde la curación de cada fuente hasta los *rankings* de desarrollo, la selección de pesos, la potencia y el acuerdo intra-anotador, y termina con una verificación de conteos; si un paso falla, el flujo se detiene (anexo A, Cuadro A.2). En un equipo de escritorio tarda unos segundos. Tres propiedades sostienen la reproducibilidad del estudio:

- **Idempotencia.** Ejecutar el flujo dos veces sobre los mismos insumos produce archivos idénticos byte a byte.
- **Aislamiento de lo congelado.** La serie v1 se regenera idéntica aunque cambien los libros de la v2, y la anotación v2.1 se compara en cada ejecución con su copia congelada: si un libro de anotación cambia después de la congelación, el flujo termina con error.
- **Ceguera por construcción.** Los pasos del experimento solo procesan las consultas de desarrollo; ningún paso del flujo ejecuta un sistema sobre las consultas de prueba.

Los pasos que dependen de la red, de las imágenes locales o de una decisión humana se ejecutan por separado y escriben insumos versionados: la recolección, la descarga de las copias de evaluación con sus sumas SHA-256, las medidas de imagen, las características de M1, los vectores de M2, los generadores de libros, el sorteo de particiones y consultas y la congelación de la anotación (anexo A, Cuadro A.3). Ninguno sobrescribe decisiones manuales salvo con una opción explícita. Los vectores de M2 se calcularon una sola vez, en CPU; el cálculo comprueba su propio determinismo y registra las sumas de los pesos del modelo, de modo que el flujo y las pruebas no necesitan las dependencias de aprendizaje profundo.

## 6.5 Implementación de los sistemas

Los sistemas son funciones puras, sin lectura ni escritura de archivos, que reciben datos ya cargados y devuelven puntuaciones; un módulo aparte lee los insumos, llama a cada sistema y escribe el *ranking* completo de cada consulta. Sus entradas y parámetros se describen en el capítulo 7 (Cuadro 7.2); aquí interesan las decisiones de implementación.

**M0** implementa BM25 de Okapi directamente, sin bibliotecas de recuperación, con $\mathrm{idf} = \ln\!\left(\frac{N - n + 0{,}5}{n + 0{,}5} + 1\right)$, para no depender de las decisiones de segmentación de una biblioteca externa y dejar visible cada componente de la fórmula. **M1** calcula sus histogramas de color y textura sobre la máscara del textil que produce la segmentación del puntaje de aptitud. **M2** lee los vectores congelados y los compara por coseno.

**M3** sigue la formalización del capítulo 5 función por función. La invariancia a la reversión no se obtiene canonizando cada palabra, sino comparando una palabra con la otra y con su reverso y tomando la menor de las dos distancias, que es la distancia entre órbitas del capítulo 5; la forma canónica solo se calcula en las pruebas que verifican la invariancia y el conteo de órbitas. El control sin orden es la misma función con un argumento que sustituye la palabra por el histograma de tipos y omite las adyacencias: ambos sistemas comparten todo el código salvo esa diferencia.

**M4** normaliza cada componente por mínimo y máximo en la consulta, reparte el peso de un componente sin evidencia y devuelve la puntuación junto con sus contribuciones. Los *rankings* de desarrollo se escriben con seis decimales, y M4 se calcula sobre esas mismas puntuaciones redondeadas, de modo que la fusión se reproduce exactamente desde el archivo versionado. Los empates se resuelven por identificador. El anexo A recoge la correspondencia entre cada fórmula, la función que la implementa y la prueba que la verifica.

## 6.6 Implementación de la evaluación

Las métricas y los contrastes estadísticos están en un módulo de funciones puras que no lee consultas ni juicios por su cuenta: quien las llama decide qué datos les pasa. Esta separación permite probarlas con ejemplos calculados a mano y garantiza que ninguna función de evaluación acceda por error a datos de prueba. El módulo cubre las métricas, la sensibilidad al *pool*, las diferencias pareadas, las pruebas de permutación, la t pareada, el *bootstrap*, la regla de decisión y la planificación de la potencia (anexo A, Cuadro A.4).

Las dependencias se redujeron deliberadamente: el flujo y las pruebas requieren cuatro bibliotecas (anexo A, sección A.5). Cada biblioteca añadida es un punto en que la regeneración puede dejar de ser idéntica al cambiar de versión, y las operaciones que el estudio necesita son lo bastante simples para implementarlas y probarlas directamente; la distribución t, por ejemplo, se calcula con una función beta incompleta implementada en el propio módulo.

## 6.7 Decisiones humanas y ceguera del evaluador

Cada tipo de decisión humana tiene su libro, con una estructura común: columnas de contexto que el revisor no edita, columnas de decisión con listas de valores válidos y columnas de revisor y fecha obligatorias. El flujo valida cada libro antes de usarlo: un valor fuera del vocabulario, una fila sin identificador o un identificador repetido detienen la ejecución sin modificar ninguna salida. Al regenerar un libro para añadir filas, por ejemplo los pares que aportó un sistema incorporado después, se conservan los juicios existentes y solo se agregan los pendientes.

El libro de juicios de relevancia se diseñó para sostener la ceguera del evaluador. Presenta los pares de cada consulta en orden aleatorio, sin el sistema que los propuso, su posición ni su puntuación, y las imágenes se muestran en una galería local que no se versiona. El archivo que registra qué sistema aportó cada par existe, pero el evaluador no lo abre, y los informes con el rendimiento de los sistemas llevan esa advertencia. Los libros incluyen una hoja de ejemplos hipotéticos que ilustran el formato y la escala sin usar piezas de la galería.

## 6.8 Verificación

La batería reúne 504 pruebas automatizadas (503 se ejecutan; una se omite por diseño, porque protege la apertura de la evaluación final ya autorizada) en cinco clases (anexo A, sección A.4): regeneración idéntica de las salidas y protección de las decisiones manuales; curación, aptitud y consolidados; anotación y congelación; propiedades de los sistemas, y experimento y evaluación.

Las pruebas de propiedades de M3 y M4 fijan los enunciados **[P]** del capítulo 5 y los contraejemplos de la proposición 5.8, de modo que una afirmación contraria no puede introducirse en el código sin que una prueba falle. La cota del control sin orden (proposición 5.6) se comprueba por enumeración exhaustiva de 132 496 pares de palabras, y las condiciones de buena formación de la anotación (capítulo 5, sección 5.4.1) son reglas que la congelación y el flujo aplican sobre la anotación final. Antes de cada entrega, el repositorio se clona en una copia limpia, se instalan las dependencias fijadas, se ejecutan el flujo y las pruebas, y se comprueba que el árbol de trabajo queda sin cambios.

## 6.9 Ejecución única de la evaluación final

La ejecución se implementó y verificó por completo antes de la autorización, de modo que la evaluación final no requirió código nuevo. La corrida avanza por los cinco estados de la sección 7.12, registrados en un manifiesto de ejecución, mediante seis órdenes sucesivas (anexo A, sección A.6): una comprobación previa de las condiciones de suspensión, que exige que el protocolo no haya cambiado después de autorizarse; el sellado de los insumos y, después, el cálculo y sellado de los *rankings* y el *pool* de prueba; la creación de los libros ciegos de juicio, con un validador que comprueba que no contienen el sistema, la puntuación ni la posición; el cierre y sellado de los juicios; el sorteo de las fichas de la revisión de H3, y la evaluación, que recalcula todas las sumas del manifiesto y solo si coinciden calcula los resultados con la plantilla fijada en el protocolo. Cada orden publica sus salidas al terminar; si una suma no coincide o falta un archivo sellado, la corrida queda suspendida y no se calcula ninguna métrica.

El cálculo de la evaluación recibe la partición como parámetro. Las pruebas automatizadas lo ejecutaron sobre la partición de desarrollo, en memoria y sin mostrar ninguna métrica, para comprobar que producía el informe completo y que la reconstrucción y la intervención de H3 se cumplían; la tarea T1 se probó con consultas hipotéticas y vectores sintéticos. Ocho pruebas de aceptación (PA1–PA8) cubren la secuencia de H1 y H2, la p exacta de H2, la regla de H1 con réplicas fijas, la alteración de un byte en un archivo sellado, una interrupción parcial, la muestra de H3 con clases vacías, el cegamiento de extremo a extremo y la coherencia entre protocolo, configuración y código. Otra prueba comprueba que, sin autorización, la orden de los *rankings* termina con error y no escribe nada. Ningún sistema se ejecutó sobre las consultas de prueba antes de la autorización (23 de noviembre de 2026).
