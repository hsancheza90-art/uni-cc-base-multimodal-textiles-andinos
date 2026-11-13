# F05 · Ypsilantis (2021)

**The Met Dataset: Instance-level Recognition for Artworks**

| Campo | Valor |
|---|---|
| Autores | Ypsilantis, N.-A.; Garcia, N.; Han, G.; et al. |
| Año y sede | 2021. arXiv (sede no vista en el texto leído) |
| Identificador | arXiv:2202.01747 |
| PDF | `pdfs/F05_ypsilantis_2021_met.pdf` · https://arxiv.org/pdf/2202.01747 |
| Eje | C. Recuperación multimodal en patrimonio |
| Origen del registro | búsqueda dirigida |
| Nivel de lectura | parcial: primeros ~40 000 caracteres literales; el resto, resumen automático |

## Qué hace

- **Datos.** Unas 397 000 imágenes de 224 408 piezas de la colección abierta del MET; 1 003 consultas de prueba tomadas por visitantes y dos grupos de distractores (10 352 de otras obras, 7 964 que no son obras).
- **Tarea y protocolo.** Reconocimiento de instancia: la consulta debe asignarse a su pieza; los distractores cuentan como incorrectos. Particiones agrupadas por usuario; validación para ajustar hiperparámetros.
- **Método.** ResNet con agrupación GeM y blanqueo PCA; clasificación kNN con confianza para rechazar lo que está fuera de distribución.
- **Comparadores.** Redes preentrenadas (ImageNet, SwAV, SWSL, SemArt) y variantes entrenadas con pérdidas contrastivas.
- **Resultados.** Mejor preentrenado: R50-SWSL con GAP 30,4 y exactitud 56,3 (tabla 5). Mejor entrenado: GAP 36,1 y exactitud 55,0 (tabla 6).
- **Limitaciones declaradas.** Alta similitud entre clases y cambios de punto de vista. Sección de limitaciones no vista.
- **Código y datos.** cmp.felk.cvut.cz/met

## Aporte a la tesis

Es la misma fuente MET, usada con otra noción de relevancia: identidad de la pieza, no parecido estructural. Aporta tres prácticas trasladables: agrupar particiones para evitar fugas, verificar consultas con dos anotadores y usar distractores. Sirve para explicar por qué los grupos de piezas relacionadas (DAT02) son necesarios: en T3 la misma pieza no debe contar como acierto.

## Cautela al citar

No es un benchmark de similitud; no usar sus cifras como referencia de dificultad de T3.

---
Leído el 11 de noviembre de 2026 con asistencia computacional. «NV» marca lo que no se vio en el texto literal del documento y debe comprobarse en el PDF antes de citarlo.
