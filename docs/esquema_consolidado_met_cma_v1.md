# Esquema del corpus consolidado MET+CMA v1.0

Archivo: `data/processed/corpus_textiles_andinos_met_cma_v1_consolidado.csv` (UTF-8 sin BOM, separador coma, fin de linea LF).

Documento generado desde `src/consolidado/esquema.py`; no editar a mano.

| # | Campo | Grupo | Descripcion |
|---:|---|---|---|
| 1 | `id_global` | identificacion | Identificador unico del corpus: <FUENTE>:<id_fuente>. **(obligatorio)** |
| 2 | `fuente` | identificacion | Codigo de la fuente museografica: MET o CMA. **(obligatorio)** |
| 3 | `id_fuente` | identificacion | Identificador institucional del objeto en la fuente. **(obligatorio)** |
| 4 | `numero_acceso` | identificacion | Numero de acceso del museo, cuando la fuente lo entrega. |
| 5 | `institucion` | identificacion | Institucion responsable del registro. **(obligatorio)** |
| 6 | `url_objeto` | visual | Enlace oficial al registro curatorial. **(obligatorio)** |
| 7 | `url_imagen` | visual | Enlace a la imagen institucional de referencia. **(obligatorio)** |
| 8 | `url_imagen_miniatura` | visual | Enlace a una imagen de menor resolucion, cuando existe. |
| 9 | `ruta_imagen_local` | visual | Ruta relativa de la copia local descargada (data/images, fuera de git). |
| 10 | `titulo_original` | textual | Titulo original del registro curatorial. **(obligatorio)** |
| 11 | `titulo_es_sugerido` | textual | Titulo sugerido en espanol, cuando existe. |
| 12 | `descripcion` | textual | Descripcion curatorial de la fuente, cuando existe. |
| 13 | `cultura` | contextual | Cultura o atribucion cultural registrada por la fuente. |
| 14 | `periodo` | contextual | Periodo historico o arqueologico, solo si la fuente lo entrega separado de la fecha. |
| 15 | `fecha_objeto` | contextual | Fecha estimada o descripcion cronologica del objeto. |
| 16 | `procedencia` | contextual | Pais, region o localidad registrados por la fuente. |
| 17 | `departamento` | contextual | Departamento del museo que custodia el objeto. |
| 18 | `clasificacion_original` | estructural | Clasificacion curatorial original de la fuente. |
| 19 | `nombre_objeto_original` | estructural | Nombre o tipo de objeto tal como lo registra la fuente. |
| 20 | `tipo_objeto` | estructural | Tipo de pieza normalizado (manto, tunica, bolso_textil, panel_textil, fragmento_textil...). |
| 21 | `origen_tipo_objeto` | estructural | Origen de tipo_objeto: curacion (revision MET v2 o CMA) o regla (src/preprocessing). |
| 22 | `tipo_superficie` | estructural | Utilidad morfologica para analisis visual, cuando se evaluo. |
| 23 | `material` | estructural | Material tal como lo registra la fuente. |
| 24 | `material_normalizado` | estructural | Materiales normalizados en espanol, separados por '; '. |
| 25 | `origen_material_normalizado` | estructural | Origen de material_normalizado: curacion o regla. |
| 26 | `tecnica` | estructural | Tecnica tal como la describe la fuente (MET no la entrega como campo). |
| 27 | `tecnica_normalizada` | estructural | Tecnicas normalizadas en espanol (tejido, tapiz, bordado...), separadas por '; '. |
| 28 | `origen_tecnica_normalizada` | estructural | Origen de tecnica_normalizada: curacion o regla. |
| 29 | `dimensiones` | estructural | Dimensiones registradas por la fuente. |
| 30 | `motivos` | iconografico | Motivos observables (pendiente de anotacion). |
| 31 | `familia_iconografica` | iconografico | Familia iconografica dominante (pendiente de anotacion). |
| 32 | `motivo_principal` | iconografico | Motivo mas visible o relevante (pendiente de anotacion). |
| 33 | `decision_curacion_final` | curatorial | Subconjunto final: principal o complementario. **(obligatorio)** |
| 34 | `motivo_curacion_final` | curatorial | Justificacion breve de la decision de curacion. |
| 35 | `decision_auditoria` | curatorial | Decision registrada en la revision manual. |
| 36 | `motivo_auditoria` | curatorial | Motivo asociado a la decision de revision. |
| 37 | `observacion_auditoria` | curatorial | Comentario del revisor. |
| 38 | `categoria_revision` | curatorial | Categoria de revision automatica previa a la revision manual. |
| 39 | `origen_curacion` | curatorial | Etapa del flujo en la que el registro entro al corpus. |
| 40 | `estado_licencia` | contextual | Condicion de uso armonizada: dominio_publico o cc0. **(obligatorio)** |
| 41 | `licencia_fuente` | contextual | Campo de licencia tal como lo entrega la fuente. |
| 42 | `derechos_reproduccion` | contextual | Aviso de derechos de reproduccion de la fuente, cuando existe. |
| 43 | `estado_metadatos` | control | Suficiencia de metadatos: completo, parcial o insuficiente. **(obligatorio)** |
| 44 | `estado_anotacion` | control | Estado de anotacion manual: sin_anotar, anotado_manual, revisar, corregido o descartado. **(obligatorio)** |
| 45 | `estado_imagen` | control | Estado de la imagen: util, baja_resolucion, no_disponible o requiere_revision. **(obligatorio)** |
| 46 | `observaciones` | control | Comentarios metodologicos generados por el flujo (por ejemplo, imagen compartida). |
| 47 | `grupo_imagen_duplicada` | imagen | Grupo de registros que comparten la misma imagen; vacio si es unica. |
| 48 | `imagen_sha256` | imagen | SHA-256 del archivo de imagen descargado. |
| 49 | `imagen_dhash` | imagen | Hash perceptual (dHash de 64 bits) de la imagen descargada. |
| 50 | `imagen_ancho` | imagen | Ancho en pixeles de la imagen descargada. |
| 51 | `imagen_alto` | imagen | Alto en pixeles de la imagen descargada. |
| 52 | `terminos_andinos` | auxiliar_fuente | Terminos que evidenciaron la relacion andina (CMA). |
| 53 | `terminos_textiles` | auxiliar_fuente | Terminos que evidenciaron la condicion textil (CMA). |
| 54 | `consulta_origen` | auxiliar_fuente | Consulta de busqueda con la que se recupero el registro. |
| 55 | `archivo_origen` | trazabilidad | CSV revisado del que proviene el registro. **(obligatorio)** |
| 56 | `fecha_descarga_metadatos` | trazabilidad | Fecha de descarga de los metadatos de la fuente, cuando se registro. |
