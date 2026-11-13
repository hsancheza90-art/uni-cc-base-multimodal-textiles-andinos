# Síntesis crítica y brecha de investigación

11 de noviembre de 2026. Se apoya en las 30 fichas de `fichas/` y en el mapeo de la auditoría del 20 de octubre. Es una revisión de alcance con cobertura parcial (ver `01_protocolo_busqueda.md`). Las afirmaciones sobre ausencia de antecedentes valen para lo recuperado, no para todo el campo.

## 1. Lo que cambia respecto de la auditoría

La auditoría dejó cuatro estudios leídos a fondo y 21 de contexto. Esta pasada añade 22 documentos nuevos y vuelve sobre ocho de los ya localizados: tres de los leídos a fondo y cinco de contexto. Tres resultados alteran lo que la tesis puede decir:

1. **Hay antecedentes de recuperación por estructura textil, y vienen del entorno andino.** Helmer y Ngo (F10) y Ngo et al. (F11) recuperan textiles por la estructura de sus cruces de hilos con hipergrafos, y el primero procede del mismo grupo que la base de conocimiento de tejido andino. La tesis no puede presentarse como la primera en recuperar textiles por estructura. Sí puede delimitar con exactitud en qué se diferencia.
2. **H2 tiene respaldo externo que el primer avance no citaba.** Dos benchmarks independientes (F01, F02) muestran que los modelos tipo CLIP tratan el contenido casi como una bolsa de elementos y no distinguen el orden ni las relaciones.
3. **Una decisión estadística del protocolo merece revisarse antes de aprobarlo.** Urbano et al. (F20) recomiendan la t pareada o la permutación como prueba y desaconsejan el bootstrap con desplazamiento, que es demasiado optimista con pocos temas.

## 2. Síntesis por eje

### A y D. Artefactos andinos, simetría y estructura

La literatura computacional sobre textiles andinos que se pudo localizar es escasa y casi toda de pago: la ontología de tejido andino (Brownlow et al., 2015), su antecedente de 2009 y el archivo digital de estructuras de 2013 siguen sin leerse. De lo leído, el aporte más importante es de una especialista: Frame (F13) sostiene que la clasificación cristalográfica de siete grupos de banda y diecisiete de campo no es apropiada para todos los patrones andinos, y propone movimientos derivados de la tecnología de fibras, como la rotación helicoidal, que esa clasificación no admite.

Para la tesis esto es una ventaja y una advertencia. La ventaja: el descriptor M3 no clasifica por grupo de simetría. Usa una palabra de bandas y la única equivalencia que impone es la reversión, que corresponde a mirar la pieza girada. La advertencia: el capítulo 5 debe presentar Burnside y Pólya como herramientas de conteo bajo un grupo elegido por el investigador, y no como descripción de cómo se concibe el diseño andino. Coincide con el punto 9.d del asesor.

En khipus, la prepublicación de Contreras (F14) encuentra que añadir el orden de los tipos de nudo no mejora la clasificación de procedencia frente a rasgos agregados. Es evidencia débil y sin arbitraje, pero es el único caso andino hallado en el que se pone a prueba el orden frente al agregado, y el resultado es negativo.

### B. Representación y recuperación de textiles

Los trabajos leídos se ordenan según de dónde sacan la noción de parecido:

| Trabajo | Escala de la estructura | Cómo se obtiene | Qué cuenta como relevante | Comparación con modelo visual |
|---|---|---|---|---|
| Helmer y Ngo (F10), Ngo et al. (F11) | Cruces de hilos | Modelado manual de cada pieza | Misma categoría de tejido | No |
| Dorozynski y Rottensteiner (F12) | Ninguna explícita | Aprendida de la imagen | Coincidencia de metadatos | Solo variantes propias |
| Rei et al. (F06) | Ninguna explícita | Imagen, texto y tabla | Clasificación de propiedades | Modalidades por separado |
| Deschaintre et al. (F29) | Apariencia descrita en texto | Descripciones libres | Emparejar imagen y descripción | CLIP y BLIP |
| **Esta tesis** | **Bandas y regiones visibles** | **Anotación sobre fotografías** | **Juicio humano graduado y ciego** | **OpenCLIP congelado** |

Ninguno de los trabajos leídos combina las cuatro propiedades de la última fila.

### C. Recuperación multimodal en patrimonio

CLIP congelado es una línea base fuerte en obras de arte (F18) y muy débil en atributos finos de museo si no se adapta (F03). Cuando hay un vocabulario controlado, una búsqueda léxica puede empatar con CLIP (F17). El patrón común es que la relevancia casi nunca se juzga: se toma de la identidad de la pieza (F05, F18), de los metadatos (F03, F12) o se sustituye por una encuesta de preferencia (F17) o por indicadores indirectos (F09). Baldrati et al. añaden una amenaza que la tesis debe declarar: las fotografías de los museos son públicas y pudieron formar parte del preentrenamiento del modelo.

### E. Orden y composición

Yuksekgonul et al. (F01) muestran que CLIP acierta poco más que el azar en relaciones entre objetos y que barajar las palabras apenas cambia su recuperación; lo explican porque el entrenamiento contrastivo se puede resolver sin representar el orden. Winoground (F02) lo confirma con otro diseño: CLIP queda por debajo del azar al emparejar imágenes que solo difieren en la disposición. Los propios autores de CLIP muestran su debilidad en conteo y texturas (F30).

El límite de este respaldo debe quedar escrito: toda esta evidencia es sobre correspondencia entre texto e imagen en fotografías naturales. T3 compara imagen con imagen en textiles. La literatura motiva H2; no la anticipa.

### F. Fusión

La combinación convexa de scores normalizados rinde mejor que la fusión por posiciones y necesita pocas consultas etiquetadas para ajustarse (F04, con cifras por verificar). La fusión por posiciones recíprocas (F22) no necesita ajuste alguno y es estable frente a su único parámetro.

### G. Evaluación

- El pooling infravalora a los sistemas cuyos resultados no entraron al pool (F15).
- Un juez que comparte información con un sistema evaluado deja de ser un árbitro independiente (F16).
- Con pocos temas, la t pareada y la permutación mantienen el error nominal; el bootstrap con desplazamiento no (F20).
- La potencia se planifica antes del experimento; calcularla después con el efecto observado no se recomienda (F21).

### H. Anotación

El acuerdo intra-anotador casi no se informa en la literatura (F08), y cuando se mide, una de cada cuatro etiquetas cambia a las dos semanas. En anotación experta de imágenes la estabilidad varía mucho según la categoría (F24). Un mismo acuerdo observado da coeficientes distintos según el modelo de azar, y en etiquetas de conjunto depende de la distancia elegida (F07).

### I. Interpretabilidad

Fidelidad y plausibilidad son propiedades distintas, y que un modelo se declare interpretable es una afirmación que hay que comprobar (F27). Un modelo aditivo que produce su propia explicación evita el problema de explicar a posteriori (F28). Los modelos con cuello de botella de conceptos (F26) son el marco más cercano a M3 y M4, con la diferencia de que allí los conceptos se predicen y aquí se anotan.

### J. Gobernanza

El permiso legal de uso (CC0) no responde a las preguntas de los principios CARE sobre objetos de origen indígena (F23). Las fichas de conjunto de datos (F25) dan la estructura para documentar el corpus v2.0 y la anotación v2.1.

## 3. La brecha, formulada como comparación que la tesis sí pone a prueba

> En los trabajos recuperados, la estructura textil se modela a escala de hilos con datos construidos a mano y se evalúa contra categorías, o bien la recuperación patrimonial se evalúa contra metadatos o identidad de pieza. No se encontró un estudio que evalúe, con juicios humanos graduados y ciegos, si la secuencia de bandas visible en fotografías de museo añade utilidad de recuperación a un codificador visión-lenguaje congelado, aislando el efecto del orden con un control sin orden.

Tres precisiones para redactarla sin excederse:

- Decir «no se encontró en una búsqueda de alcance parcial», no «no existe». Quedan sin leer Brownlow et al. (2015) y Phillips (2018), que son los dos textos con más probabilidad de acercarse.
- La novedad no está en usar estructura ni en fusionar modalidades, que tienen precedentes (F03, F06, F10, F11). Está en la escala (macroestructura visible), en el diseño de evaluación (qrels humanos independientes del descriptor) y en el control que aísla el orden.
- La contribución es compatible con un resultado negativo. Contreras (F14) ofrece un precedente andino de orden que no añade señal.

## 4. Propuestas para el protocolo, antes de su aprobación

Ninguna reabre el corpus ni añade modelos. Todas tendrían que registrarse en el protocolo con fecha antes de abrir el test. Las decide el investigador con el asesor.

| # | Propuesta | Fundamento | Costo |
|---|---|---|---|
| P1 | Decidir H1 y H2 con una prueba de permutación pareada (o t pareada) y usar el bootstrap solo para el intervalo de confianza | F20 | Un párrafo en la sección 7; el código de permutación ya está previsto como sensibilidad |
| P2 | Añadir como ablación una variante de M4 por posiciones recíprocas, sin pesos | F22, F04 | Pocas líneas; sin juicios adicionales si sus candidatos ya están en el pool |
| P3 | Informar por sistema la proporción del top 10 juzgada y repetir las métricas retirando los pares que solo aportó cada sistema | F15 | Solo análisis; los datos de procedencia ya se guardan aparte |
| P4 | Fijar antes del test el efecto mínimo detectable con 30 consultas, a partir de la varianza de las diferencias en desarrollo; no informar potencia a posteriori | F21 | Un cálculo con los datos de desarrollo |
| P5 | Informar el acuerdo intra-anotador por atributo, con el acuerdo bruto junto al coeficiente, y sin umbral único | F07, F08, F24 | Ya lo calcula `src.anotacion.acuerdo`; es cuestión de redacción |
| P6 | Nombrar entre las amenazas que el anotador de M3 y el evaluador son la misma persona, y que el doble juicio parcial es la única mitigación externa | F16 | Un párrafo en la sección 10 |
| P7 | Añadir la posible presencia de las fotografías en el preentrenamiento de OpenCLIP como amenaza a la validez | F18 | Una frase |

P2 tiene una condición: si los candidatos de la variante no están en el pool, hay que juzgarlos. Conviene generarla antes de cerrar el pool de prueba o descartarla.

## 5. Ideas para después del experimento

Se anotan para no perderlas. El asesor pidió diferir toda extensión.

- **Una prueba de orden para M2.** Adaptar la idea de ARO (F01) al dominio: tomar pares de piezas con el mismo histograma de bandas y distinta secuencia y medir si M2 las distingue. Sería una explicación directa de un resultado de H2, en cualquier sentido.
- **Reutilizar los datos públicos de Ngo et al. (F11).** Si se define una proyección de sus estructuras a bandas, M3 podría probarse fuera del corpus de museos.
- **Extracción automática de bandas.** La recuperación por regiones de Sheng et al. (F19) y la detección de grupos de friso de Liu et al. (pendiente) son los puntos de partida para sustituir la anotación manual.
- **Vocabulario para consultas de texto.** Deschaintre et al. (F29) muestran qué atributos menciona la gente al describir telas; serviría para redactar consultas T1 con más de una persona.

## 6. Dónde entra cada documento en el manuscrito

| Capítulo | Fichas |
|---|---|
| 2. Problema, hipótesis y alcance | F01, F02, F27, F28 |
| 3. Estado del arte | F03, F05, F06, F10, F11, F12, F17, F18, F19, F29, F30 |
| 4. Marco teórico del textil andino | F13, F14 |
| 5. Modelo matemático | F13, F26 |
| Datos, anotación y ética | F07, F08, F23, F24, F25 |
| Método y evaluación | F04, F15, F16, F20, F21, F22 |
| Discusión y amenazas a la validez | F09, F14, F16, F18, F21 |

## 7. Lo que falta para que esta revisión sea defendible

1. Leer en PDF las secciones de resultados de los documentos con lectura parcial que vayan a citarse con cifras. Todo lo marcado «NV» está sin verificar.
2. Conseguir los cinco pendientes de prioridad alta, empezando por Brownlow et al. (2015) y Phillips (2018).
3. Ejecutar las cadenas en Scopus y Web of Science con acceso UNI y registrar exportaciones.
4. Buscar la bibliografía en español sobre estructura textil andina.
5. Completar las referencias: en varios documentos el año o la sede se tomaron de OpenAlex o de la auditoría porque no aparecen en el PDF leído.
