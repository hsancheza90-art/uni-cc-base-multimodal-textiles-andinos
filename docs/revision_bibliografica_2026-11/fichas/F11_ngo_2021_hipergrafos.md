# F11 · Ngo (2021)

**Structural textile pattern recognition and processing based on hypergraphs**

| Campo | Valor |
|---|---|
| Autores | Ngo, V. M.; Helmer, S.; Le-Khac, N.-A.; Kechadi, M.-T. (p. 137) |
| Año y sede | 2021. Information Retrieval Journal 24, 137–173 (confirmado, p. 137). Recibido el 16-03-2020, aceptado el 12-11-2020, publicado en línea el 23-01-2021; acceso abierto CC BY 4.0 (pp. 137 y 171) |
| Identificador | doi:10.1007/s10791-020-09384-y |
| PDF | `pdfs/F11_ngo_2021_hipergrafos.pdf` · https://link.springer.com/content/pdf/10.1007/s10791-020-09384-y.pdf |
| Eje | B. Representación y recuperación de textiles |
| Origen del registro | auditoría (S06), releído; texto clave pedido por el asesor |
| Nivel de lectura | completo (texto extraído del PDF, 37 páginas, numeradas 137–173; revisado el 20-11-2026). Las fórmulas salieron con códigos de glifo («/u1D6EF…») pero el texto es legible; las figuras 13 y 15–23 no son legibles como cifras salvo lo que repite el texto |

## Qué hace

- **Datos.** 1 600 muestras en 16 categorías de 100 elegidas con expertos (p. 160): tafetán, cinco sargas, raso, tejido andino, tejido vietnamita, triaxial, punto por trama, punto por urdimbre, cota de malla, trenza, «warp above weave» y tejidos mixtos vietnamitas (pp. 160–161). Cada muestra se construyó a mano con el editor SAWU del proyecto anterior; en promedio 20 916 vértices y 5 229 cruces (p. 160). Se alteró el 1 % de los cruces, se rotó el 85 % y se reflejó el 35 % de los patrones (p. 161). **Corrección:** el texto no dice que los patrones procedan de visitas a museos; esas visitas (proyecto anterior) solo motivaron el enfoque al revelar patrones sin terminología (p. 138). Los andinos y vietnamitas son dos de las 16 categorías, «tomados de una colección de tejidos» de esas regiones (p. 160). No se usan fotografías.
- **Tarea y protocolo.** Confirmado: cada uno de los 1 600 textiles es consulta y son relevantes los 100 de su categoría; MAP, MeanP@100 y curvas PR y FR de 11 puntos (pp. 157–158). Agrupamiento frente a las 16 categorías con pureza, NMI, índice de Rand, precisión, exhaustividad y F (pp. 158–160).
- **Método.** Hipergrafo por textil: los nodos son extremos de cruce, las hiperaristas de grado cuatro son cruces y las aristas de grado dos marcan el hilo superior (definición 1, p. 145). Cada cruce recibe una k-vecindad (tramos alternos, no alternos o terminados al seguir los cuatro hilos; definiciones 2–5, pp. 147–149); la huella es su multiconjunto, invariante a rotación y reflejo (p. 148); cálculo en O(nk) (p. 151). **Escala:** estructura de hilos; el resumen sitúa la búsqueda «al nivel de la estructura de hilos» (p. 137) y el texto aparta los métodos por imagen porque «dependen del color y no de la estructura» (p. 140). No menciona bandas, franjas ni su orden; la única aparición de «bands» es el título de una referencia (Chan et al. 2017, p. 172).
- **Comparadores.** **Corrección:** siete distancias, no cinco (euclidiana, coseno de frecuencias, coseno TF-IDF, Hamming booleana, Hamming de frecuencias, Jaccard y solapamiento; p. 161); agrupamiento jerárquico con enlace simple, completo, promedio y Ward, y K-means (pp. 154–156); comparación con los resultados de 2015 (pp. 164 y 166). Ninguna línea base externa ni modelo visual.
- **Resultados.** Confirmado: con k = 4, MAP 0,91 (Jaccard), 0,897 (coseno de frecuencias), 0,889 (TF-IDF), 0,887 (solapamiento), 0,814 (euclidiana), 0,805 y 0,661 (Hamming); MeanP@100 0,881 con Jaccard (p. 163). k > 4 no mejora (p. 163). Mejor agrupamiento: enlace completo con coseno TF-IDF (k = 2), pureza 0,842, NMI 0,912, índice de Rand 0,976, precisión 0,755 y F 0,819 (pp. 165–166). Frente a 2015: Rand 0,938 → 0,976, precisión 0,577 → 0,755, exhaustividad 0,922 → 0,894, F 0,71 → 0,819 (p. 166); en recuperación los resultados son «más o menos comparables» a los de 2015 (p. 164).
- **Limitaciones declaradas.** Confirmadas: conjunto relativamente pequeño y balanceado (p. 166), modelado mayormente manual (p. 167), índice de Rand fácil de inflar por los verdaderos negativos (pp. 159 y 166); piden conjuntos grandes y diversos y su generación (semi)automática (p. 167).
- **Código y datos.** Confirmado: datos en Harvard Dataverse, doi:10.7910/DVN/ZFNLES (pp. 160 y 173). Código: no figura en el texto.

## Aporte a la tesis

Confirma lo que la auditoría anotó: es otra escala. El hipergrafo describe cómo se cruzan los hilos; la palabra de bandas describe qué se ve en la superficie. Ambos comparten una idea que conviene citar: representar el textil por rasgos locales y sus vecindades (aquí k-vecindades, en M3 adyacencias entre bandas). El conjunto de datos público puede servir como caso de prueba futuro de M3 si se define una proyección a bandas.

## Cautela al citar

Las cifras ya están verificadas con página. Al citar el vínculo andino, decir que es una de 16 categorías modeladas a mano a escala de hilos, no un corpus de piezas andinas fotografiadas.

## Actualización del 20 de noviembre de 2026

- Se resolvieron todos los «NV» (16 categorías, protocolo, cifras de recuperación y agrupamiento, limitaciones y Dataverse) con página.
- Se corrigió el número de distancias (siete, no cinco) y la afirmación de que los patrones proceden de visitas a museos, que el texto no sostiene.
- Se confirmó la escala: cruces de hilos (ligamento); el andino es una categoría entre 16 y no hay mención de bandas, franjas ni su orden.
- El artículo cita la versión previa como «Helmer & Ngo (2015), Proceedings of the 38th SIGIR, pp. 163–172» (p. 172) y se declara su extensión (p. 171); dato útil para F10. Sin código publicado.

---
Leído el 11 de noviembre de 2026 y completado el 20 de noviembre de 2026 con asistencia computacional, sobre el texto completo extraído del PDF. «NV» marca lo que no se pudo comprobar.
