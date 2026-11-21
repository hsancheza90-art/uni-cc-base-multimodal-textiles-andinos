# F05 · Ypsilantis (2021)

**The Met Dataset: Instance-level Recognition for Artworks**

| Campo | Valor |
|---|---|
| Autores | Ypsilantis, N.-A.; Garcia, N.; Han, G.; Ibrahimi, S.; van Noord, N.; Tolias, G. (p. 1) |
| Año y sede | 2021. 35th Conference on Neural Information Processing Systems (NeurIPS 2021), Track on Datasets and Benchmarks (p. 1); arXiv v1 del 3 de febrero de 2022 |
| Identificador | arXiv:2202.01747 |
| PDF | `pdfs/F05_ypsilantis_2021_met.pdf` · https://arxiv.org/pdf/2202.01747 |
| Eje | C. Recuperación multimodal en patrimonio |
| Origen del registro | búsqueda dirigida |
| Nivel de lectura | completo (texto extraído del PDF, 29 páginas; revisado el 20-11-2026) |

## Qué hace

- **Datos.** 397 121 imágenes de estudio de 224 408 piezas de acceso abierto del MET (máximo 10 por pieza, sin duplicados); prueba: 1 003 consultas tomadas por visitantes y dos grupos de distractores de Wikimedia Commons (10 352 de otras obras, 7 964 que no son obras); validación: 129 + 1 168 + 868 (tabla 1, p. 4). Consultas de 39 visitantes; imágenes reducidas a 500 × 500 como máximo (p. 5). El departamento «Africa, Oceania, the Americas» figura en la distribución (fig. 4, p. 4).
- **Tarea y protocolo.** Reconocimiento de instancia: la consulta debe asignarse a su pieza; los distractores cuentan siempre como incorrectos. Métricas: exactitud media (solo consultas MET) y GAP (todas las consultas) y GAP⁻ (solo MET) (p. 5). Particiones agrupadas por usuario y sin clases compartidas entre validación y prueba; validación para ajustar hiperparámetros (p. 5). Etiquetas verificadas por dos anotadores (p. 4).
- **Método.** ResNet18/50 con agrupación GeM, representación multiescala y blanqueo PCA (512 D); clasificación kNN con confianza normalizada por softmax para relegar lo que está fuera de distribución (pp. 6–8).
- **Comparadores.** Redes preentrenadas (ImageNet, SfM, SemArt, Stylized-ImageNet, SwAV, SWSL), clasificadores paramétricos (CE, ArcFace), SimSiam y variantes contrastivas (tablas 5 y 6, pp. 8–9); en el apéndice, descriptores locales HOW + ASMK (p. 14).
- **Resultados.** Mejor preentrenado: R50-SWSL con GAP 30,4 y exactitud 56,3 (tabla 5, p. 8). Mejor entrenado: R18-SWSL Con-Syn+Real-closest con GAP 36,1 y exactitud 55,0 (tabla 6, p. 9). Las redes de atributos artísticos (SemArt) rinden peor que ImageNet (p. 9). kNN supera al clasificador paramétrico, sobre todo en clases con pocas imágenes (fig. 8, p. 10).
- **Limitaciones declaradas.** Alta similitud entre clases y cambios de punto de vista (p. 10). No hay sección de limitaciones; la ficha de datos indica que el conjunto se construyó para reconocimiento de instancia y que las imágenes reducidas pueden impedir usos que requieren alta resolución (p. 28); sin revisión ética institucional (p. 26).
- **Código y datos.** cmp.felk.cvut.cz/met y github.com/nikosips/met; anotaciones CC BY 4.0 (p. 13).

## Aporte a la tesis

Es la misma fuente MET, usada con otra noción de relevancia: identidad de la pieza, no parecido estructural. Aporta tres prácticas trasladables: agrupar particiones para evitar fugas, verificar consultas con dos anotadores y usar distractores. Sirve para explicar por qué los grupos de piezas relacionadas (DAT02) son necesarios: en T3 la misma pieza no debe contar como acierto.

## Cautela al citar

No es un benchmark de similitud; no usar sus cifras como referencia de dificultad de T3.

## Actualización del 20 de noviembre de 2026

- Se verificó la sede en el PDF: NeurIPS 2021, Track on Datasets and Benchmarks (p. 1); la ficha decía «sede no vista».
- Se completaron los seis autores y se confirmaron las cifras de las tablas 1, 5 y 6 sin cambios.
- Se añadió que no hay sección de limitaciones propiamente dicha; las limitaciones de uso están en la ficha de datos (p. 28).
- Se agregaron el repositorio de código y la licencia de las anotaciones (p. 13).

---
Leído el 11 de noviembre de 2026 y completado el 20 de noviembre de 2026 con asistencia computacional, sobre el texto completo extraído del PDF. «NV» marca lo que no se pudo comprobar.
