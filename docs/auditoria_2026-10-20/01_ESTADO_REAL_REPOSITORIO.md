### Estado real del repositorio
Fecha de corte: 20-10-2026. Auditoría independiente de una instantánea; no certificación institucional. Dictamen principal: REQUIRES_METHODOLOGICAL_CORRECTIONS.

#### Alcance y preservación
Repositorio auditado: [commit c38996e3](https://github.com/hsancheza90-art/uni-cc-base-multimodal-textiles-andinos/blob/c38996e3af4b1874498e7e3e24ed4fc5c3e59471/). Rama main; ramas remotas observadas origin/main. Etiquetas y hashes completos en evidencias/entorno_final.json. Se inventariaron los archivos versionados y se inspeccionaron arquitectura, módulos críticos, configuraciones, workbooks, datos derivados, pruebas y documentación. La revisión detallada se concentró en rutas que afectan selección, anotación y estimación del desempeño; no equivale a verificación formal de cada instrucción.

El PDF adjunto es idéntico al de docs/MCC701_05-07-2026.pdf: SHA-256 1fe84982a17b2680e67016cafdf1a694c502b91f9fc4b1c081dab71f802f7fed. Se analizó su texto completo por capítulos, incluidas las formulaciones del capítulo 5. El documento pertenece a Seminario I: las tareas futuras que anuncia no son resultados incumplidos de ese documento, pero sí pendientes de Seminario II.

Se clonó el repositorio y se ejecutó el flujo en una copia separada. No se editaron fuentes, decisiones curatoriales ni workbooks originales; no hubo commit, push, merge ni PR. Estado Git final limpio en ambas copias. Las pruebas crean archivos temporales; el intérprete puede crear cachés no versionadas.

#### Verificación de avances declarados

| Afirmación | Evidencia observada | Estado |
|---|---|---|
| v1.2 contiene 288 registros | Consolidado 181 MET + 107 CMA; 214 principales + 74 complementarios | VERIFICADO |
| v1 está preservada | Cuatro CSV de entrada congelados idénticos al tag corpus-met-cma-v1.2 | VERIFICADO |
| Esquema y vocabulario armonizados | src/consolidado/esquema.py, config/vocabulario.toml; generador documental y pruebas | VERIFICADO |
| Flujo reproducible | 13 etapas, retorno 0; sin diferencias Git tras regenerar | VERIFICADO, para insumos archivados |
| 508 candidatos AIC y 228 principales | Workbook AIC: 508 IDs distintos, 228/124/156 | VERIFICADO |
| 874 registros con decisión | Workbooks: 874 IDs compuestos distintos; 462/153/259; sin pendientes | VERIFICADO |
| 874 revisados manualmente individualmente | Orígenes mixtos; 227 filas con revisor auto y 544 sin nombre de revisor | NO_VERIFICABLE |
| Aptitud v2 implementada | Medidas, modelos logísticos, puntaje, bandas, informes y pruebas | VERIFICADO |
| Aptitud validada para museo nuevo | CV mezclando fuentes; LOMO auxiliar heterogéneo | NO_VERIFICABLE como afirmación general |
| Validación ciega independiente actual | 15 de 40 casos entraron a calibración | INCONSISTENTE si se presenta como prueba independiente |
| Protocolo de anotación preparado | Guía, workbook, vocabulario y exportador | VERIFICADO |
| Corpus estructural anotado | 288 filas sin_anotar; CSV de anotaciones sin registros | NO_IMPLEMENTADO |
| M0–M4 y evaluación de recuperación | No se identifican implementaciones/runs/qrels en la instantánea | NO_IMPLEMENTADO |

La ausencia del nombre del revisor no demuestra ausencia de revisión humana. La formulación defendible es “874 decisiones registradas, de procedencia manual y automática”.

#### Versiones y divergencias históricas
v1.0 MET+CMA: 288, con MET 127/54 y CMA 88/19. v1.1: MET 126/55, CMA 88/19. v1.2 mantiene los 288 y consolida la trazabilidad. El PDF conserva una fotografía histórica de 289 registros; no corresponde actualizar retrospectivamente el archivo de Seminario I. El informe II debe incluir una tabla de cambios con fecha, criterio, ID afectado y versión.

La serie v2 reúne 874 candidatos decididos, no 874 ejemplos elegibles ni 462 objetos independientes garantizados. No hay una etiqueta de lanzamiento experimental v2 congelada equivalente a v1.2. No mezclar los 214 principales v1 con los 462 principales v2 al describir resultados.

#### Conteos comprobados

| Fuente | Principal v2 | Secundario | Descartado | Total |
|---|---:|---:|---:|---:|
| MET | 130 | 25 | 65 | 220 |
| CMA | 104 | 4 | 38 | 146 |
| AIC | 228 | 124 | 156 | 508 |
| Total | 462 | 153 | 259 | 874 |

Manifiesto v2: 873 descargas marcadas ok y una error. Manifiesto v1: 287 ok y una error. Son estados históricos archivados: no se descargaron nuevamente las 874 fotografías. Disponibilidad actual y correspondencia de píxeles: NOT_RUN. Los hashes almacenados permiten detectar duplicados declarados, pero no sustituyen una verificación de los archivos originales.

#### Arquitectura y límites de reproducción
Colectores → candidatos archivados → filtros → workbook de decisiones → subconjuntos; en paralelo, imágenes → medidas → aptitud; finalmente, anotaciones → consolidado. src/flujo.py ejecuta únicamente el tramo sin red. La obtención de metadatos, descarga y medición desde píxeles quedan fuera. Un flujo verde no prueba la exactitud de esos insumos ni la calidad científica de las etiquetas.

Evidencia: [flujo, líneas 1–87](https://github.com/hsancheza90-art/uni-cc-base-multimodal-textiles-andinos/blob/c38996e3af4b1874498e7e3e24ed4fc5c3e59471/src/flujo.py#L1-L87); [prueba de regeneración, 62–92](https://github.com/hsancheza90-art/uni-cc-base-multimodal-textiles-andinos/blob/c38996e3af4b1874498e7e3e24ed4fc5c3e59471/tests/test_flujo.py#L62-L92). La prueba compara texto UTF-8 normalizando CRLF a LF: es igualdad textual normalizada, más estricta que igualdad semántica, menos que identidad binaria general. En ESTA ejecución, adicionalmente, Git no detectó diferencias de bytes en archivos versionados. Debe corregirse la descripción general “byte a byte” del README.

#### Registro ejecutado

| Comando/actividad | Estado | Alcance |
|---|---|---|
| python -m src.flujo antes de instalar dependencias | BLOCKED | requests ausente; no fallo científico |
| python -m pip install -r requirements-dev.txt | PASS | Dependencias exactas instaladas |
| python -m src.flujo en copia | PASS | 13 etapas y conteos |
| python -m pytest | PASS | 207 pruebas |
| Comparación Git posterior | PASS | Sin diferencias versionadas |
| Auditoría independiente de CSV/XLSX | PASS | Conteos e integridad observada |
| Reproducciones de cinco contratos defectuosos | FAIL del contrato esperado | Scripts y JSON adjuntos |
| Descarga total y recolección APIs actuales | NOT_RUN | No atribuir PASS a estas etapas |
| GPU, modelos de recuperación, evaluación experta | NOT_RUN | No hay ejecución central |
| CI remota | NOT_RUN | No se observó workflow de CI |

Las evidencias contienen entorno, inventario SHA-256, logs, scripts y resultados. Las rutas de esos scripts esperan un directorio repo junto a auditoria; véase LEEME.md para reproducir.

