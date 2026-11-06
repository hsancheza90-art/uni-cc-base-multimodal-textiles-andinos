### Auditoría matemática del capítulo 5

#### Diagnóstico por formulación
Se revisan todas las ecuaciones por grupos contiguos. "Correcta" se refiere a la identidad matemática bajo sus hipótesis, no a que exista una implementación o evidencia empírica.

| Ecuaciones | Juicio | Condiciones y corrección |
|---|---|---|
| 5.1–5.3 | PARCIAL | Imagen RGB y matriz simbólica son objetos distintos; falta definir I→P, resolución, recorte, segmentación y error |
| 5.4–5.7 | PARCIAL | Alfabeto finito válido. Color, forma, orientación, rol y técnica no tienen siempre misma escala ni observabilidad; técnica no debe asignarse a cada celda sin sustento |
| 5.8–5.17 | VERIFICADO algebraicamente | Producto cartesiano y 8×10×4×5×6=9600 correctos; muchas combinaciones pueden ser no realizables, no son datos observados |
| 5.18–5.20 | VERIFICADO condicional | card(Σ)^(mn) para tamaños fijos e independencia combinatoria formal; 20^100 es ejemplo, no diversidad cultural estimada |
| 5.21–5.23 | PARCIAL | Ωobs⊆Ωplaus exige que las restricciones no excluyan observaciones válidas; inclusión estricta no prueba regularidad cultural |
| 5.24–5.30 | INCONSISTENTE en tipos | Las restricciones sobre pieza/imagen/metadatos no son funciones solo de P. Separar elegibilidad E(o,I,D) de restricciones estructurales R(P). No exigir bandas y simetría a todos los textiles |
| 5.31–5.34 | PARCIAL | Definir posiciones, coincidencia exacta/aproximada, solapamiento, transformaciones y diccionario común. Un diccionario distinto por pieza impide comparar coordenadas |
| 5.35–5.39 | PARCIAL | Fijar eje de lectura, 1≤p≤l y ∀j≤l−p. p=l existe por vacuidad, pero no evidencia repetición |
| 5.40–5.43 | PARCIAL | 1ᵀA^(n−1)1 cuenta palabras de longitud n≥1 con adyacencias admitidas y extremos libres. No incorpora restricciones globales. "No observado" no equivale a "prohibido" |
| 5.44–5.46 | PARCIAL | Definir G y su acción sobre posiciones Y símbolos; demostrar cierre y preservación de restricciones |
| 5.47–5.48 | VERIFICADO condicional | Burnside válido para conjunto y grupo finitos con acción bien definida; falta instancia útil |
| 5.49 | VERIFICADO condicional | Promedio de k^(ciclos) cuenta coloraciones libres bajo permutación de posiciones, no cualquier sistema restringido ni símbolos que cambian orientación |
| 5.50–5.52 | PARCIAL | Usar grafo atribuido con relaciones tipadas; contención dirigida, adyacencia usualmente simétrica. Una sola E no explica todas las semánticas |
| 5.53–5.54 | PARCIAL | Faltan dimensiones, unidades, escalas, valores ausentes y procedimientos de cálculo |
| 5.55 | NO_VERIFICABLE como complejidad | Es un índice propuesto; diversidad, simetría y repetición no definen una complejidad universal. Puede aumentar al añadir regularidad; justificar interpretación |
| 5.56–5.57 | VERIFICADO condicional | Entropía de histogramas con probabilidades normalizadas, base log fijada y 0 log 0=0; no mide orden espacial |
| 5.58–5.60 | PARCIAL | Coseno requiere vectores numéricos comparables y norma no nula; establecer pesos, escalas y máscaras. Mezcla de similitudes no implica distancia métrica |
| 5.61–5.64 | PARCIAL | Codificadores y F son interfaces conceptuales, no algoritmos especificados |
| 5.65 | VERIFICADO como construcción | Concatenación permite dimensiones distintas, pero exige normalización de bloques y control de pesos |
| 5.66 | INCONSISTENTE sin alineación | Suma requiere misma dimensión Y espacio compatible. Igualar tamaño mediante padding no alinea semántica |
| 5.67–5.68 | PARCIAL | Fusión de scores viable; fijar normalización, contexto disponible y ajuste solo en desarrollo |
| 5.69 | PARCIAL | Inclusión estricta de muestra finita es débil/tautológica; sustituir por hipótesis predictiva de restricciones |
| 5.70 | NO_IMPLEMENTADO | ≈ necesita transformación y tolerancia; separar invariancia de estabilidad frente a daño |
| 5.71 | NO_IMPLEMENTADO | Beneficio empírico, no teorema derivado de escribir una suma |
| 5.72–5.73 | PARCIAL | Flujo conceptual requiere registro de errores en cada interfaz |
| 5.74–5.77 | VERIFICADO como ejemplo | Vectores ilustrativos, no resultados; un cero en "periodo" necesita semántica distinta de dato desconocido |
| 5.78 | PARCIAL | Ωobs es una colección, no una transformación de una pieza aislada; corregir diagrama |

#### Descriptor mínimo implementable
Unidad o: objeto/grupo experimental; una o varias fotografías I; anotación visible A con procedencia y máscara m. No se propone inferir la trama de hilos desde fotografías generales.

A comprende regiones poligonales normalizadas, rol de región, familia geométrica visible, orientación, bandas ordenadas y relaciones espaciales. Separar valor, estado {observado, ausente, no_observable, desconocido}, anotador y confianza. "Ausente" solo se usa si la superficie pertinente es visible. Etiquetas de cultura/técnica proceden del museo y van al bloque contextual.

Para el primer experimento:
1. h: histograma normalizado de familias de motivos y roles; sirve como control sin orden.
2. w: palabra de bandas en un eje documentado, con símbolos de vocabulario fijo; conservar longitud y anchos relativos.
3. a: histograma normalizado de pares de bandas adyacentes; si se permite reflexión, canonizar primero w o usar pares no dirigidos.
4. s: discrepancia bilateral sobre regiones visibles, cobertura de comparación y eje; no asumir equivalencia de orientaciones culturales.
5. r: periodo observado y soporte; opcional para bandas discretas.
6. m: máscara de observabilidad, independiente de ceros verdaderos.

Motivos detectados manualmente convierten M3 en un sistema asistido por anotación; debe declararse. M2 usa píxeles y M3 usa información humana adicional: la comparación mide utilidad del sistema, no superioridad de extracción automática. Un extractor automático posterior se evalúa por separado.

#### Palabras, reflexión y demostración
Si el sentido de lectura es irrelevante para la tarea, usar el grupo C2={identidad, reversión}, con rev(rev(w))=w. Definir c(w)=mínimo lexicográfico de {w,rev(w)}, con orden del alfabeto fijado. Entonces c(rev(w))=c(w), pues ambos conjuntos contienen los mismos dos elementos. El histograma de adyacencias de c(w) también es invariante. Si el sentido de lectura importa, usar solo identidad.

La canonización cuesta O(l). Contar bigramas cuesta O(l); comparar vectores dispersos O(k) en el número de entradas presentes. Ejemplo matemático: aabb y abab tienen idéntico histograma y entropía, pero diferentes adyacencias. Por eso el control "sin orden" es indispensable. Este ejemplo no reemplaza datos de textiles reales.

Periodo exacto:
p*(w)=min{p∈{1,…,l}: para todo j∈{1,…,l−p}, wj=w(j+p)}.
Reportar l/p* y número de pares comparados; p*=l no se llama repetición. Para ruido, e(p)=discordancias/comparaciones observables. Exigir soporte mínimo y al menos dos repeticiones; umbral ajustado en desarrollo. Una laguna se enmascara, no se convierte en símbolo repetido.

#### Distancia mixta y fusión
Para bloques observables en ambos objetos, definir d_b en [0,1]: Jaccard para conjuntos, L1/2 para histogramas normalizados, edición normalizada para palabras, diferencias absolutas para escalares normalizados con rangos fijados en desarrollo.

D(i,j)=Σ_b λ_b m_ib m_jb d_b(i,j) / Σ_b λ_b m_ib m_jb, λ_b≥0.
Si denominador=0: resultado "sin evidencia estructural", no similitud máxima. Reportar cobertura junto a D. Con máscaras variables D es una disimilitud; no garantizar desigualdad triangular ni kernel PSD. Evitar índices que requieran propiedades métricas no probadas.

Una distancia por órbitas, min_g d(w,g·v), es métrica en clases si d es métrica y el grupo actúa por isometrías. Para edición de palabras con reflexión y costo simétrico por símbolo, la reversión preserva d. La normalización por longitud variable puede perder propiedades métricas: conservar distancia sin normalizar si se necesita la garantía.

M4 usa fusión tardía de scores/rangos, no suma arbitraria de embeddings. Un score aditivo permite explicar la contribución exacta de cada bloque. Si falta estructura, renormalizar pesos disponibles según regla predeclarada y reportar cobertura. No aprender pesos en test.

#### Burnside y Pólya: uso legítimo y alcance
Ejemplo verificable, no experimental: cuatro posiciones lineales, dos colores, G=C2 con reversión. Hay 2^4 configuraciones; la reversión fija 2^2. Número de órbitas=(16+4)/2=10. Puede enumerarse como prueba unitaria.

Con adyacencias restringidas, Burnside sigue siendo válido solo si G preserva el conjunto admisible; hay que contar fijados dentro de ese conjunto. Sustituir automáticamente por 2^(ciclos) sería incorrecto. En una matriz rectangular, rotación de 90° no conserva el dominio salvo que sea cuadrada o se amplíe explícitamente el espacio. Traslación con recorte no es acción de grupo invertible; un toro discreto sí, pero introduce vecindades artificiales que deben justificarse.

No se requiere enumerar Ω0 para recuperar 462 objetos. Mantener estos resultados como fundamento formal o apéndice si no cambian el algoritmo. Un kernel promediado sobre acciones de un grupo finito puede construirse desde una aplicación de características: ΨG(x)=|G|⁻¹Σ_g Ψ(gx); K=⟨ΨG(x),ΨG(y)⟩ es PSD por construcción. Su costo crece con |G| y no es necesario para H1.

#### Jerarquías, grafos y costo
Jerarquía pieza→región→motivo/banda es útil si los anotadores pueden identificarla consistentemente. Un kernel Weisfeiler–Lehman sobre grafos discretamente etiquetados es una ampliación H2 razonable antes que una GNN entrenada con pocos ejemplos. Hipergrafos a nivel de cruces de hilos, como Ngo et al., exigen datos que estas fotos no garantizan. Gramáticas visuales y GNN quedan en H3 salvo que un piloto demuestre utilidad y anotaciones suficientes.

Invariancia a escala se aproxima con coordenadas y anchos relativos; no garantiza invariancia del muestreo fotográfico. Degradación y pérdida de fragmentos son perturbaciones no invertibles: evaluar estabilidad/abstención, no llamarlas simetrías. Probar límites explícitos de rotación, reflexión, recorte y cambios de color; no confundir robustez de una característica con validez cultural.

