# F19 · Sheng (2021)

**Fine-Grained Cross-Modal Retrieval for Cultural Items with Focal Attention and Hierarchical Encodings**

| Campo | Valor |
|---|---|
| Autores | Sheng, S.; Laenen, K.; Van Gool, L.; et al. |
| Año y sede | 2021. Computers 10(9), 105 |
| Identificador | doi:10.3390/computers10090105 |
| PDF | `pdfs/F19_sheng_2021_recuperacion_fina.pdf` · https://www.mdpi.com/2073-431X/10/9/105/pdf |
| Eje | C. Recuperación multimodal en patrimonio |
| Origen del registro | OpenAlex (C2) |
| Nivel de lectura | parcial: primeros ~40 000 caracteres literales; el resto, resumen automático |

## Qué hace

- **Datos.** Conjuntos de alineación de arte egipcio y chino, con un conjunto de referencia de correspondencias manuales entre fragmentos.
- **Tarea y protocolo.** Anotación (de fragmento de imagen a sintagma nominal) y búsqueda (de sintagma a fragmento); validación cruzada de cuatro pliegues sobre el conjunto de referencia.
- **Método.** Modelo débilmente supervisado con atención, filtro por puntos SIFT y codificación jerárquica; regiones propuestas por Faster R-CNN.
- **Comparadores.** Tres líneas base, dos de ellas métodos del estado del arte adaptados.
- **Resultados.** No vistos: quedaron en el tramo no literal y el resumen no dio cifras.
- **Limitaciones declaradas.** No vistos.
- **Código y datos.** No visto.

## Aporte a la tesis

Define recuperación fina como correspondencia entre regiones de la pieza y fragmentos de texto, frente al emparejamiento de imagen completa. Es la dirección a la que apuntaría una versión automática de M3: localizar bandas y regiones en lugar de anotarlas. Útil para trabajo futuro y para situar T1.

## Cautela al citar

Sin resultados leídos: citar solo el planteamiento.

---
Leído el 11 de noviembre de 2026 con asistencia computacional. «NV» marca lo que no se vio en el texto literal del documento y debe comprobarse en el PDF antes de citarlo.
