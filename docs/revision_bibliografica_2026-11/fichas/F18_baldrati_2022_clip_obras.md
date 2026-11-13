# F18 · Baldrati (2022)

**Exploiting CLIP-Based Multi-modal Approach for Artwork Classification and Retrieval**

| Campo | Valor |
|---|---|
| Autores | Baldrati, A.; Bertini, M.; Uricchio, T.; et al. |
| Año y sede | 2022. Capítulo en Springer (2022) según OpenAlex; leído en arXiv |
| Identificador | doi:10.1007/978-3-031-20302-2_11; arXiv:2309.12110 |
| PDF | `pdfs/F18_baldrati_2022_clip_obras.pdf` · https://arxiv.org/pdf/2309.12110 |
| Eje | C. Recuperación multimodal en patrimonio |
| Origen del registro | OpenAlex (C1) |
| Nivel de lectura | completo |

## Qué hace

- **Datos.** NoisyArt: 89 095 imágenes de 3 120 obras reunidas de la web; 200 clases verificadas para prueba.
- **Tarea y protocolo.** Clasificación y recuperación obra a obra y descripción a obra; la relevancia queda implícita en la clase.
- **Método.** Rasgos de CLIP con ResNet-50 usados directamente; variante con clasificación previa y reordenamiento; CLIP afinado con dos capas lineales.
- **Comparadores.** ResNet-50 de ImageNet y las líneas base de NoisyArt.
- **Resultados.** mAP de recuperación (tabla 4): ResNet-50 36,32; CLIP sin ajustar 46,40; CLIP afinado 69,60.
- **Limitaciones declaradas.** Desplazamiento de dominio entre entrenamiento y prueba; los datos de entrenamiento de CLIP no son públicos, así que puede haber fuga.
- **Código y datos.** No visto.

## Aporte a la tesis

Confirma que CLIP congelado es una línea base fuerte en obras de arte y que su ventaja crece al afinar. Fija la expectativa para H1: superar a M2 no es trivial. Aporta una amenaza a la validez que la tesis debe recoger: las fotos de MET, CMA y AIC son públicas y pudieron estar en los datos de preentrenamiento de OpenCLIP.

## Cautela al citar

Relevancia por identidad de clase, no por estructura.

---
Leído el 11 de noviembre de 2026 con asistencia computacional. «NV» marca lo que no se vio en el texto literal del documento y debe comprobarse en el PDF antes de citarlo.
