# Revisión bibliográfica, noviembre de 2026

Revisión de alcance para la tesis «Estructuras combinatorias y representación multimodal en textiles andinos». Atiende la observación BIB01 de la auditoría y el punto 10 del informe integrado del asesor (8 de noviembre de 2026). Ejecutada el 11 de noviembre de 2026 con asistencia computacional.

No es una revisión sistemática. Se consultó una base de forma nativa (OpenAlex) y se leyeron 30 documentos de acceso abierto, la mayoría de forma parcial. Scopus, Web of Science, IEEE Xplore y ACM DL no se consultaron.

**Actualización del 20 de noviembre de 2026.** El investigador aportó 19 PDF: F31 a F33, y F34 a F48, localizados con una búsqueda web. Las 21 fichas parciales se completaron sobre el texto íntegro de su PDF. Las 48 fichas tienen lectura completa del cuerpo. `05_pendientes_texto_completo.md` reúne lo que falta leer, los datos por confirmar y los hallazgos que afectan la tesis. La matriz `03_matriz_antecedentes.csv` sigue describiendo los 30 documentos originales; las fichas prevalecen sobre ella.

## Contenido

| Archivo | Qué es |
|---|---|
| `04_sintesis_y_brecha.md` | Empezar aquí: síntesis por eje, brecha de investigación, siete propuestas para el protocolo y destino de cada fuente en el manuscrito |
| `01_protocolo_busqueda.md` | Fuentes usadas y no usadas, estrategia, criterios, flujo con conteos y limitaciones |
| `02_resultados_busqueda.md` | Las 17 cadenas de OpenAlex con su total y los registros retenidos |
| `03_matriz_antecedentes.csv` | Matriz de los 30 documentos: datos, tarea, método, comparadores, resultados, límites, código y aporte |
| `05_pendientes_texto_completo.md` | Afirmaciones pendientes y la fuente que las respalda, bibliografía que falta leer, datos por confirmar, hallazgos y correspondencia entre PDF y ficha |
| `fichas/` | Un informe `.md` por documento (F01 a F48) con su aporte a la tesis |
| `pdfs/` | Manifiesto de los PDF y sus enlaces de acceso abierto. Los archivos se bajan con `descargar.py` |
| `busquedas/consultas_openalex.json` | Cadenas literales y URL de cada consulta |
| `referencias.bib` | Entradas provisionales; faltan campos que no se vieron en los documentos |
| `descargar.py` | Baja los PDF del manifiesto; con `--busquedas` exporta los JSON de OpenAlex |

## Cómo leer las fichas

Cada ficha indica el nivel de lectura. «NV» marca un dato que no se vio en el texto literal del documento, porque quedó en un tramo que la herramienta de lectura resumió. Esos datos no deben citarse sin comprobarlos en el PDF. Las fichas son una ayuda para la lectura propia, no la sustituyen.

## Relación con la auditoría

El mapeo del 20 de octubre (`docs/auditoria_2026-10-20/`) no se modifica. Ocho de sus documentos se leyeron o releyeron aquí; sus identificadores (S01, S03, etc.) figuran en el campo «origen» de la matriz.
