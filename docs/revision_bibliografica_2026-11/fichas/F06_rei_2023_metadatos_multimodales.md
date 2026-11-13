# F06 · Rei (2023)

**Multimodal Metadata Assignment for Cultural Heritage Artifacts**

| Campo | Valor |
|---|---|
| Autores | Rei, L.; Mladenić, D.; Dorozynski, M.; et al. |
| Año y sede | 2023. Multimedia Systems 29, 847–869; versión ampliada en arXiv (2024) |
| Identificador | doi:10.1007/s00530-022-01025-2; arXiv:2406.00423 |
| PDF | `pdfs/F06_rei_2023_metadatos_multimodales.pdf` · https://arxiv.org/pdf/2406.00423 |
| Eje | B. Representación y recuperación de textiles |
| Origen del registro | auditoría (S04/S05), releído |
| Nivel de lectura | parcial: primeros ~40 000 caracteres literales; el resto, resumen automático |

## Qué hace

- **Datos.** Registros de tejidos de seda europeos de 12 colecciones (proyecto SILKNOW); la exportación del grafo tiene 38 873 objetos y 74 527 imágenes.
- **Tarea y protocolo.** Asignar propiedades (material, técnica, lugar, época) como clasificación multitarea. NV: partición aleatoria 60/20/20.
- **Método.** Fusión tardía de tres clasificadores: imagen (ResNet), texto (XLM-R multilingüe) y tabular (árboles con gradient boosting), con pérdida focal para el desbalance.
- **Comparadores.** Modelos de una sola modalidad y variantes de pérdida (NV).
- **Resultados.** El resumen afirma que el enfoque multimodal da los mejores resultados. Cifras NV: F1 multimodal 74,2 frente a 55,6 de la mejor modalidad sola en el conjunto de prueba completo.
- **Limitaciones declaradas.** NV: desbalance de clases, ruido en etiquetas de material y técnica, texto disponible en cerca del 39 % de los registros.
- **Código y datos.** NV: datos en Zenodo y código en github.com/silknow.

## Aporte a la tesis

Precedente textil de fusión tardía de imagen, texto y atributos, que es la arquitectura de M4. La diferencia es de objetivo: clasifican metadatos con decenas de miles de registros; la tesis recupera por estructura con 150 piezas. También ilustra un problema compartido: el texto falta en buena parte de las fichas, lo que afecta a M0.

## Cautela al citar

Las cifras de ganancia no se vieron en el texto literal.

---
Leído el 11 de noviembre de 2026 con asistencia computacional. «NV» marca lo que no se vio en el texto literal del documento y debe comprobarse en el PDF antes de citarlo.
