# F11 · Ngo (2021)

**Structural textile pattern recognition and processing based on hypergraphs**

| Campo | Valor |
|---|---|
| Autores | Ngo, V. M.; Helmer, S.; Le-Khac, N.-A.; et al. |
| Año y sede | 2021. Information Retrieval Journal 24, 137–173 |
| Identificador | doi:10.1007/s10791-020-09384-y |
| PDF | `pdfs/F11_ngo_2021_hipergrafos.pdf` · https://link.springer.com/content/pdf/10.1007/s10791-020-09384-y.pdf |
| Eje | B. Representación y recuperación de textiles |
| Origen del registro | auditoría (S06), releído; texto clave pedido por el asesor |
| Nivel de lectura | parcial: primeros ~40 000 caracteres literales; el resto, resumen automático |

## Qué hace

- **Datos.** 1 600 muestras de estructuras tejidas, de punto y trenzadas; la introducción menciona textiles andinos y vietnamitas. Los patrones proceden de visitas a museos, no de la base de conocimiento andina, que fue un proyecto anterior. NV: 16 categorías de 100.
- **Tarea y protocolo.** NV: cada textil es consulta y son relevantes los de su categoría; MAP, precisión a 100 y curvas; agrupamiento frente a 16 categorías.
- **Método.** Hipergrafo por textil: los nodos son extremos de cruce, las hiperaristas de grado cuatro son cruces y las de grado dos marcan el hilo superior (definición 1). Huellas de vecindad de radio k como multiconjuntos, con varias distancias.
- **Comparadores.** NV: cinco distancias, métodos de enlace, K-means y la versión de 2015.
- **Resultados.** NV: MAP 0,91 con Jaccard y k = 4; mejor agrupamiento con índice de Rand 0,976 y F 0,819.
- **Limitaciones declaradas.** NV: conjunto pequeño y balanceado, modelado manual, índice de Rand inflado por verdaderos negativos.
- **Código y datos.** NV: datos en Harvard Dataverse (doi:10.7910/DVN/ZFNLES).

## Aporte a la tesis

Confirma lo que la auditoría anotó: es otra escala. El hipergrafo describe cómo se cruzan los hilos; la palabra de bandas describe qué se ve en la superficie. Ambos comparten una idea que conviene citar: representar el textil por rasgos locales y sus vecindades (aquí k-vecindades, en M3 adyacencias entre bandas). El conjunto de datos público puede servir como caso de prueba futuro de M3 si se define una proyección a bandas.

## Cautela al citar

Casi todos los resultados numéricos quedaron en el tramo no literal: leer las secciones de evaluación en el PDF antes de citarlos.

---
Leído el 11 de noviembre de 2026 con asistencia computacional. «NV» marca lo que no se vio en el texto literal del documento y debe comprobarse en el PDF antes de citarlo.
