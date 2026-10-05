# Esquema del corpus consolidado MET+CMA v1.0

Archivo: `data/processed/corpus_textiles_andinos_met_cma_v1_consolidado.csv` (UTF-8 sin BOM, separador coma, fin de linea LF).

Documento generado desde `src/consolidado/esquema.py`; no editar a mano. Los campos con vocabulario controlado guardan codigos de `config/vocabulario.toml`; sus etiquetas estan en `docs/corpus/taxonomia_atributos_met_cma_v1.md`.

| # | Campo | Grupo | Descripcion | Vocabulario |
|---:|---|---|---|---|
| 1 | `id_global` | identificacion | Identificador unico del corpus: <FUENTE>:<id_fuente>. **(obligatorio)** |  |
| 2 | `fuente` | identificacion | Codigo de la fuente museografica: MET o CMA. **(obligatorio)** |  |
| 3 | `id_fuente` | identificacion | Identificador institucional del objeto en la fuente. **(obligatorio)** |  |
| 4 | `numero_acceso` | identificacion | Numero de acceso del museo, cuando la fuente lo entrega. |  |
| 5 | `institucion` | identificacion | Institucion responsable del registro. **(obligatorio)** |  |
| 6 | `url_objeto` | visual | Enlace oficial al registro curatorial. **(obligatorio)** |  |
| 7 | `url_imagen` | visual | Enlace a la imagen institucional de referencia. **(obligatorio)** |  |
| 8 | `url_imagen_miniatura` | visual | Enlace a una imagen de menor resolucion, cuando existe. |  |
| 9 | `ruta_imagen_local` | visual | Ruta relativa de la copia local descargada (data/images, fuera de git). |  |
| 10 | `titulo_original` | textual | Titulo original del registro curatorial. **(obligatorio)** |  |
| 11 | `titulo_es_sugerido` | textual | Titulo sugerido en espanol, cuando existe. |  |
| 12 | `descripcion` | textual | Descripcion curatorial de la fuente, cuando existe. |  |
| 13 | `cultura` | contextual | Cultura o atribucion cultural registrada por la fuente. |  |
| 14 | `periodo` | contextual | Periodo historico o arqueologico, solo si la fuente lo entrega separado de la fecha. |  |
| 15 | `fecha_objeto` | contextual | Fecha estimada o descripcion cronologica del objeto. |  |
| 16 | `procedencia` | contextual | Pais, region o localidad registrados por la fuente. |  |
| 17 | `departamento` | contextual | Departamento del museo que custodia el objeto. |  |
| 18 | `clasificacion_original` | estructural | Clasificacion curatorial original de la fuente. |  |
| 19 | `nombre_objeto_original` | estructural | Nombre o tipo de objeto tal como lo registra la fuente. |  |
| 20 | `tipo_objeto` | estructural | Tipo de pieza normalizado (codigo del vocabulario). | Cuadro 6.5 |
| 21 | `origen_tipo_objeto` | estructural | Origen de tipo_objeto: curacion, regla o anotacion. |  |
| 22 | `tipo_superficie` | estructural | Utilidad morfologica para analisis visual (codigo del vocabulario). | Cuadro 6.5 |
| 23 | `material` | estructural | Material tal como lo registra la fuente. |  |
| 24 | `material_normalizado` | estructural | Codigos de material separados por '; '. | Cuadro 6.5, multiple |
| 25 | `origen_material_normalizado` | estructural | Origen de material_normalizado: curacion, regla o anotacion. |  |
| 26 | `tecnica` | estructural | Tecnica tal como la describe la fuente (MET no la entrega como campo). |  |
| 27 | `tecnica_normalizada` | estructural | Codigos de tecnica separados por '; '. | Cuadro 6.5, multiple |
| 28 | `origen_tecnica_normalizada` | estructural | Origen de tecnica_normalizada: curacion, regla o anotacion. |  |
| 29 | `dimensiones` | estructural | Dimensiones registradas por la fuente. |  |
| 30 | `color_dominante` | visual | Color visualmente predominante (anotacion, Cuadro 6.3). | Cuadro 6.3 |
| 31 | `colores` | visual | Colores visibles separados por '; ' (anotacion, Cuadro 6.3). | Cuadro 6.3, multiple |
| 32 | `contraste` | visual | Diferencia visual entre zonas cromaticas (anotacion, Cuadro 6.3). | Cuadro 6.3 |
| 33 | `densidad_visual` | visual | Saturacion de elementos visuales (anotacion, Cuadro 6.3). | Cuadro 6.3 |
| 34 | `composicion` | composicional | Organizacion general del diseno (anotacion, Cuadro 6.4). | Cuadro 6.4 |
| 35 | `simetria` | composicional | Organizacion simetrica o repetitiva (anotacion, Cuadro 6.4). | Cuadro 6.4 |
| 36 | `repeticion` | composicional | Presencia de patrones repetidos (anotacion, Cuadro 6.4). | Cuadro 6.4 |
| 37 | `borde` | composicional | Presencia de borde decorado (anotacion, Cuadro 6.4). | Cuadro 6.4 |
| 38 | `centro` | composicional | Presencia de campo central diferenciado (anotacion, Cuadro 6.4). | Cuadro 6.4 |
| 39 | `motivos` | iconografico | Motivos observables separados por '; ' (anotacion, Cuadro 6.6). | Cuadro 6.6, multiple |
| 40 | `familia_iconografica` | iconografico | Familia iconografica dominante (anotacion, Cuadro 6.6). | Cuadro 6.6 |
| 41 | `motivo_principal` | iconografico | Motivo mas visible o relevante (anotacion, Cuadro 6.6). | Cuadro 6.6 |
| 42 | `decision_curacion_final` | curatorial | Subconjunto final: principal o complementario. **(obligatorio)** | Cuadro 6.1 |
| 43 | `motivo_curacion_final` | curatorial | Justificacion breve de la decision de curacion. |  |
| 44 | `decision_auditoria` | curatorial | Decision registrada en la revision manual. |  |
| 45 | `motivo_auditoria` | curatorial | Motivo asociado a la decision de revision. |  |
| 46 | `observacion_auditoria` | curatorial | Comentario del revisor. |  |
| 47 | `categoria_revision` | curatorial | Categoria de revision automatica previa a la revision manual. |  |
| 48 | `origen_curacion` | curatorial | Etapa del flujo en la que el registro entro al corpus. |  |
| 49 | `estado_licencia` | contextual | Condicion de uso armonizada: dominio_publico o cc0. **(obligatorio)** | Cuadro 6.7 |
| 50 | `licencia_fuente` | contextual | Campo de licencia tal como lo entrega la fuente. |  |
| 51 | `derechos_reproduccion` | contextual | Aviso de derechos de reproduccion de la fuente, cuando existe. |  |
| 52 | `estado_metadatos` | control | Suficiencia de metadatos: completo, parcial o insuficiente. **(obligatorio)** | Cuadro 6.8 |
| 53 | `estado_anotacion` | control | Estado de anotacion manual: sin_anotar, anotado_manual, revisar, corregido o descartado. **(obligatorio)** | Cuadro 6.8 |
| 54 | `estado_imagen` | control | Estado de la imagen: util, baja_resolucion, no_disponible o requiere_revision. **(obligatorio)** | Cuadro 6.8 |
| 55 | `observaciones` | control | Comentarios metodologicos generados por el flujo (por ejemplo, imagen compartida). |  |
| 56 | `anotador` | control | Persona que registro la anotacion manual. |  |
| 57 | `fecha_anotacion` | control | Fecha de la anotacion manual (AAAA-MM-DD). |  |
| 58 | `observaciones_anotacion` | control | Comentarios del anotador: dudas, ambiguedades o criterios aplicados. |  |
| 59 | `grupo_imagen_duplicada` | imagen | Grupo de registros que comparten la misma imagen; vacio si es unica. |  |
| 60 | `imagen_sha256` | imagen | SHA-256 del archivo de imagen descargado. |  |
| 61 | `imagen_dhash` | imagen | Hash perceptual (dHash de 64 bits) de la imagen descargada. |  |
| 62 | `imagen_ancho` | imagen | Ancho en pixeles de la imagen descargada. |  |
| 63 | `imagen_alto` | imagen | Alto en pixeles de la imagen descargada. |  |
| 64 | `terminos_andinos` | auxiliar_fuente | Terminos que evidenciaron la relacion andina (CMA). |  |
| 65 | `terminos_textiles` | auxiliar_fuente | Terminos que evidenciaron la condicion textil (CMA). |  |
| 66 | `consulta_origen` | auxiliar_fuente | Consulta de busqueda con la que se recupero el registro. |  |
| 67 | `archivo_origen` | trazabilidad | CSV revisado del que proviene el registro. **(obligatorio)** |  |
| 68 | `fecha_descarga_metadatos` | trazabilidad | Fecha de descarga de los metadatos de la fuente, cuando se registro. |  |
