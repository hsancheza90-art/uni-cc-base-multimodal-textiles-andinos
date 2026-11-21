# F29 · Deschaintre (2023)

**The Visual Language of Fabrics**

| Campo | Valor |
|---|---|
| Autores | Deschaintre, V.; Guerrero-Viu, J. (primeros autores conjuntos); Gutierrez, D.; Boubekeur, T.; Masia, B. (Adobe Research; Universidad de Zaragoza - I3A) (p. 1) |
| Año y sede | 2023. arXiv v1 del 25-07-2023 (p. 1). El texto usa la plantilla de ACM con volumen, número y DOI sin completar («XX», «https://doi.org/XXXX», fecha de publicación julio de 2023, 15 páginas) (p. 1): la sede ACM Transactions on Graphics (SIGGRAPH 2023) y el DOI 10.1145/3592391 no figuran en el texto |
| Identificador | doi:10.1145/3592391 (no figura en el texto); arXiv:2307.13681 |
| PDF | `pdfs/F29_deschaintre_2023_lenguaje_telas.pdf` · https://arxiv.org/pdf/2307.13681 |
| Eje | B. Representación y recuperación de textiles |
| Origen del registro | OpenAlex (B1) |
| Nivel de lectura | completo (texto extraído del PDF, 15 páginas; revisado el 20-11-2026). Las figuras (imágenes de telas, gráficos de las fig. 3–6) no son legibles; las estadísticas de la fig. 3b no se pudieron leer. El material suplementario citado no está en el PDF |

## Qué hace

- **Datos.** text2fabric: 3 000 materiales textiles de Substance 3D (procedurales y escaneados), 45 000 imágenes renderizadas (3 000 en la geometría base más 42 000 con otras cuatro geometrías y dos iluminaciones) y 15 461 descripciones libres válidas de 122 personas (p. 2–4). Se recogieron 19 167 descripciones y se rechazaron 3 706 (19,3 %) en auditoría manual (p. 4).
- **Tarea y protocolo.** Cómo describe la gente la apariencia de una tela y si esas descripciones mejoran la recuperación. Cada persona ve una imagen con tres ampliaciones y escribe de 20 a 100 palabras; al menos cinco descripciones válidas por imagen; nadie aporta más del 9 % (p. 4). Recuperación por texto evaluada con Recall@K sobre 3 129 descripciones de prueba y materiales no vistos (p. 8).
- **Método.** Prueba de calificación (aprox. uno de cada cuatro no la pasa) y auditoría manual con escala de 1 a 5 (p. 4); léxico por frecuencia reducida media; los 524 lemas del léxico se agrupan en atributos con propagación de afinidad sobre ConceptNet Numberbatch (p. 5–6); orden de mención por producto de rangos y prueba de Kruskal-Wallis (p. 6); se afinan CLIP ViT-B/16 (recuperación) y BLIP ViT-B (pies) (p. 7–10).
- **Comparadores.** CLIP y BLIP sin afinar; BLIP entrenado solo con text2fabric (sin preentrenamiento) (p. 8).
- **Resultados.** 84 lemas cubren el 75 % de las descripciones y 524 el 95 % (p. 5). Once atributos; color, patrón, tacto y tipo de tela aparecen en más del 70 % (p. 6). El color se menciona primero (producto de rangos 2,25; el patrón 2,86; cuadro 1, p. 7). Las descripciones de una misma tela se parecen más entre sí que las de telas distintas (ANOSIM, p = 0,001; cuadro 2, p. 7). Recuperación al primer resultado (cuadro 3, p. 8): CLIP afinado 13,81 % frente a 2,94 % de CLIP sin afinar (confirmado); Top-10 46,76 % frente a 12,59 %. En una geometría no vista: 7,38 % frente a 1,34 % (cuadro 4, p. 8). La mayor parte de la ganancia llega con las primeras 2 000 descripciones (p. 8). CLIP sin afinar se guía por la forma 3D y no por el patrón del material (p. 10).
- **Limitaciones declaradas.** Quienes describen son hablantes nativos de inglés, con visión del color normal y cercanos a la moda y el diseño, pero no expertos (p. 4, 13); los resultados valen para estos estímulos (el atributo «military» refleja el sesgo del conjunto) (p. 6, 13); las consultas negativas («no rojo») fallan; en diseños muy intrincados los pies omiten motivos salientes, como leopardos (fig. 16, p. 13); imágenes renderizadas y estáticas (p. 14).
- **Código y datos.** valentin.deschaintre.fr/text2fabric (p. 2–3): conjunto completo y modelos afinados.

## Aporte a la tesis

Informa la tarea exploratoria T1. Muestra que el lenguaje espontáneo sobre telas privilegia color y patrón y casi no describe disposición ni secuencia, lo que explica por qué las consultas de texto con especificación estructural son las difíciles. Sirve para discutir que las seis consultas T1 las redactó una sola persona y en español. La omisión de motivos en diseños intrincados (p. 13) y el sesgo de CLIP hacia la forma global (p. 10) también son pertinentes para textiles con bandas y figuras.

## Cautela al citar

Telas contemporáneas en imágenes sintéticas, no piezas arqueológicas. El texto afirma que CLIP se entrenó con LAION (p. 3 y 7), lo que no coincide con F30 (WebImageText, conjunto propio de OpenAI): no tomar ese dato de esta fuente. La sede y el DOI deben tomarse de la versión publicada.

## Actualización del 20 de noviembre de 2026

- Se leyó el texto completo (15 páginas); se completaron los cinco autores y sus afiliaciones.
- NV resuelto: la mejora por afinado (Top-1 13,81 % frente a 2,94 %) está en el cuadro 3, p. 8; se añadieron los resultados en geometría no vista y el número de descripciones rechazadas.
- Corrección: la sede ACM TOG / SIGGRAPH 2023 y el DOI no figuran en el texto (plantilla con «XXXX»); se mantienen solo como dato externo.
- Sigue sin verificar: las cifras de la fig. 3b y el material suplementario (detalles de lematización y de la agrupación en atributos).

---
Leído el 11 de noviembre de 2026 y completado el 20 de noviembre de 2026 con asistencia computacional, sobre el texto completo extraído del PDF. «NV» marca lo que no se pudo comprobar.
