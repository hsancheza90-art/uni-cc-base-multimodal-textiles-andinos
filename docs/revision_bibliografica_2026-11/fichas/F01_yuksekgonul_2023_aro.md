# F01 · Yuksekgonul (2023)

**When and Why Vision-Language Models Behave like Bags-of-Words, and What to Do About It?**

| Campo | Valor |
|---|---|
| Autores | Yuksekgonul, M.; Bianchi, F.; Kalluri, P.; Jurafsky, D.; Zou, J. (Stanford University) (p. 1) |
| Año y sede | 2023. ICLR 2023, artículo de conferencia («Published as a conference paper at ICLR 2023», p. 1); arXiv v3 del 23-03-2023 |
| Identificador | arXiv:2210.01936 |
| PDF | `pdfs/F01_yuksekgonul_2023_aro.pdf` · https://arxiv.org/pdf/2210.01936 |
| Eje | E. Orden y composición en modelos visión-lenguaje |
| Origen del registro | búsqueda dirigida |
| Nivel de lectura | completo (texto extraído del PDF, 20 páginas; revisado el 20-11-2026). La figura 1 (con las cifras por tarea) y el radar de la figura 3 salen ilegibles en la extracción; sus valores se tomaron del texto y de los cuadros 2, 5 y 6 del apéndice |

## Qué hace

- **Datos.** Benchmark ARO sobre Visual Genome con anotaciones de GQA: VG-Relation (48 relaciones, 23 937 casos), VG-Attribution (117 pares de atributos, 28 748 casos) (p. 3 y apéndice A, p. 16); COCO-Order y Flickr30k-Order sobre las particiones de Karpathy (p. 4–5); más de 50 000 casos en total (p. 1).
- **Tarea y protocolo.** Elegir el pie correcto frente a uno con los constituyentes intercambiados (azar 50 %, p. 4) o frente a cuatro permutaciones sistemáticas del cuadro 1 (azar 20 %, p. 4). Las imágenes se recortan a la caja mínima que contiene ambos objetos y se eliminan relaciones simétricas como «near» (p. 16).
- **Método.** Diagnóstico de CLIP (ViT-B/32), BLIP, FLAVA y X-VLM (p. 4, 17–19); proponen NegCLIP, un CLIP ViT-B/32 afinado en COCO con pies negativos (intercambio de sustantivos, adjetivos, adverbios, frases verbales y nominales) e imágenes alternativas entre los 3 vecinos más cercanos (p. 7, 20).
- **Comparadores.** CLIP, BLIP, FLAVA, X-VLM; CLIP afinado en COCO sin negativos (CLIP-FT) como ablación (p. 7, cuadro 6, p. 20).
- **Resultados.** Según el texto (p. 7): VG-Relation 63 % → 81 %; VG-Attribution 62 % → 71 %; COCO-Order 46 % → 86 %; Flickr30k-Order 59 % → 91 %. El cuadro 6 (p. 20) da para VG-Relation CLIP 0,59, CLIP-FT 0,63 y NegCLIP 0,81: el 63 % del texto coincide con CLIP-FT, no con CLIP (el cuadro 2, p. 17, también da 0,59 para CLIP). CLIP obtiene 56 % en relaciones espaciales y 61 % en verbos; FLAVA 25 % en relaciones (p. 4). Barajar las palabras del pie o los parches de la imagen apenas reduce la recuperación (sec. 3.1, p. 6; cuadros 3–4, p. 18–19): p. ej., CLIP en Flickr30k, R@1 texto 0,784 → 0,587 al barajar todas las palabras. NegCLIP no pierde mucho en tareas generales (ImageNet 0,75 → 0,72, p. 20).
- **Limitaciones declaradas.** Sin entrenamiento desde cero por coste (p. 7 y p. 20); lote de 1024 en una sola GPU RTX 2080 Ti frente a 32 000 en CLIP (p. 20); los experimentos con CLIP y NegCLIP no se repitieron con varias semillas, aunque se usó semilla fija (p. 11). Las perturbaciones de pies se repiten con 3 semillas (p. 6, 10); el texto de la p. 4 dice 5 semillas para la tarea de orden, pero el cuadro 5 (p. 19) dice 3.
- **Código y datos.** github.com/mertyg/vision-language-models-are-bows (p. 2, 10); NegCLIP como bifurcación de open_clip (p. 11).

## Aporte a la tesis

Es el mejor respaldo externo de H2. Muestra que un codificador contrastivo puede resolver su tarea sin representar orden ni relaciones (lo llaman un atajo válido, p. 2 y 7). Justifica preguntar si un descriptor que sí codifica el orden de las bandas añade señal a M2. El experimento de barajar filas, columnas o parches de la imagen (p. 6, cuadro 4) es la analogía más cercana a una permutación de bandas.

## Cautela al citar

La evidencia es sobre texto e imagen en fotos naturales, no sobre similitud imagen-imagen en textiles. Sirve como motivación de H2, no como prueba anticipada. Al citar la mejora en VG-Relation, precisar que el punto de partida de CLIP sin afinar es 0,59 (cuadros 2 y 6), no 63 %.

## Actualización del 20 de noviembre de 2026

- Se leyó el texto completo (20 páginas, incluido el apéndice); se completaron los autores y la sede (ICLR 2023, p. 1).
- Se resolvió el NV de la cifra 0,59: es la de CLIP en VG-Relation (cuadros 2 y 6); el 63 % del texto principal corresponde a CLIP-FT. Se dejó constancia de la discrepancia.
- Se confirmaron las limitaciones antes marcadas NV (sin entrenamiento desde cero, lote de 1024, una sola corrida con semilla fija) con sus páginas.
- Sigue sin verificar: los valores que solo aparecen en las figuras 1 y 3 (ilegibles en la extracción) y la discrepancia entre 5 y 3 semillas en la tarea de orden.

---
Leído el 11 de noviembre de 2026 y completado el 20 de noviembre de 2026 con asistencia computacional, sobre el texto completo extraído del PDF. «NV» marca lo que no se pudo comprobar.
