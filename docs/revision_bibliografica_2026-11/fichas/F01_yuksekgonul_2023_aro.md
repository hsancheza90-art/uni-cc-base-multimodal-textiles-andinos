# F01 · Yuksekgonul (2023)

**When and Why Vision-Language Models Behave like Bags-of-Words, and What to Do About It?**

| Campo | Valor |
|---|---|
| Autores | Yuksekgonul, M.; Bianchi, F.; Kalluri, P.; et al. |
| Año y sede | 2023. ICLR 2023 |
| Identificador | arXiv:2210.01936 |
| PDF | `pdfs/F01_yuksekgonul_2023_aro.pdf` · https://arxiv.org/pdf/2210.01936 |
| Eje | E. Orden y composición en modelos visión-lenguaje |
| Origen del registro | búsqueda dirigida |
| Nivel de lectura | parcial: primeros ~40 000 caracteres literales; el resto, resumen automático |

## Qué hace

- **Datos.** Benchmark ARO sobre Visual Genome/GQA: VG-Relation (23 937 casos), VG-Attribution (28 748); COCO-Order y Flickr30k-Order sobre las particiones de Karpathy; más de 50 000 casos.
- **Tarea y protocolo.** Elegir el pie correcto frente a uno con palabras intercambiadas (azar 50 %) o frente a cuatro permutaciones (azar 20 %).
- **Método.** Diagnóstico de CLIP, BLIP, FLAVA y X-VLM; proponen NegCLIP, un CLIP ViT-B/32 afinado en COCO con negativos difíciles que alteran la composición.
- **Comparadores.** CLIP, BLIP, FLAVA, X-VLM; CLIP afinado sin negativos como ablación.
- **Resultados.** CLIP → NegCLIP: VG-Relation 63 % → 81 %; VG-Attribution 62 % → 71 %; COCO-Order 46 % → 86 %; Flickr30k-Order 59 % → 91 % (sec. 4). CLIP obtiene 56 % en relaciones espaciales (sec. 2.3). Barajar las palabras del pie apenas reduce la recuperación (sec. 3.1). Una tabla del tramo no literal da 0,59 para VG-Relation: NV.
- **Limitaciones declaradas.** No vistos en el texto literal. NV: sin entrenamiento desde cero, lote de 1024, una sola semilla.
- **Código y datos.** github.com/mertyg/vision-language-models-are-bows

## Aporte a la tesis

Es el mejor respaldo externo de H2. Muestra que un codificador contrastivo puede resolver su tarea sin representar orden ni relaciones (lo llaman un atajo válido). Justifica preguntar si un descriptor que sí codifica el orden de las bandas añade señal a M2.

## Cautela al citar

La evidencia es sobre texto e imagen en fotos naturales, no sobre similitud imagen-imagen en textiles. Sirve como motivación de H2, no como prueba anticipada.

---
Leído el 11 de noviembre de 2026 con asistencia computacional. «NV» marca lo que no se vio en el texto literal del documento y debe comprobarse en el PDF antes de citarlo.
