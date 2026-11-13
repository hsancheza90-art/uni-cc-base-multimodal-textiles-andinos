# F29 · Deschaintre (2023)

**The Visual Language of Fabrics**

| Campo | Valor |
|---|---|
| Autores | Deschaintre, V.; Guerrero-Viu, J.; Gutierrez, D.; et al. |
| Año y sede | 2023. ACM Transactions on Graphics (SIGGRAPH 2023) según DOI |
| Identificador | doi:10.1145/3592391; arXiv:2307.13681 |
| PDF | `pdfs/F29_deschaintre_2023_lenguaje_telas.pdf` · https://arxiv.org/pdf/2307.13681 |
| Eje | B. Representación y recuperación de textiles |
| Origen del registro | OpenAlex (B1) |
| Nivel de lectura | parcial: primeros ~40 000 caracteres literales; el resto, resumen automático |

## Qué hace

- **Datos.** text2fabric: 3 000 materiales textiles, 45 000 imágenes sintéticas y 15 461 descripciones libres válidas de 122 personas.
- **Tarea y protocolo.** Cómo describe la gente la apariencia de una tela y si esas descripciones mejoran la recuperación.
- **Método.** Descripciones recogidas con prueba de calificación y auditoría manual; los lemas se agrupan en atributos; se afinan CLIP y BLIP.
- **Comparadores.** CLIP y BLIP sin afinar.
- **Resultados.** 84 lemas cubren el 75 % de las descripciones. Once atributos; color, patrón, tacto y tipo de tela aparecen en más del 70 %. El color suele mencionarse primero (tabla 1). Mejora por afinado NV: recuperación al primer resultado 13,81 % frente a 2,94 %.
- **Limitaciones declaradas.** Quienes describen son hablantes nativos de inglés cercanos a la moda y el diseño.
- **Código y datos.** valentin.deschaintre.fr/text2fabric

## Aporte a la tesis

Informa la tarea exploratoria T1. Muestra que el lenguaje espontáneo sobre telas privilegia color y patrón y casi no describe disposición ni secuencia, lo que explica por qué las consultas de texto con especificación estructural son las difíciles. Sirve para discutir que las seis consultas T1 las redactó una sola persona y en español.

## Cautela al citar

Telas contemporáneas en imágenes sintéticas, no piezas arqueológicas.

---
Leído el 11 de noviembre de 2026 con asistencia computacional. «NV» marca lo que no se vio en el texto literal del documento y debe comprobarse en el PDF antes de citarlo.
