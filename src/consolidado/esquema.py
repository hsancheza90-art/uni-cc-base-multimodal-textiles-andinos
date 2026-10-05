"""Esquema armonizado del corpus consolidado MET+CMA v1.0.

Sigue los Cuadros 6.1 (campos principales) y 6.8 (estados de control) del
avance de tesis, y agrega campos auxiliares de fuente, imagen y trazabilidad.
"""

from __future__ import annotations

# (campo, grupo, descripcion)
ESQUEMA: list[tuple[str, str, str]] = [
    ("id_global", "identificacion", "Identificador unico del corpus: <FUENTE>:<id_fuente>."),
    ("fuente", "identificacion", "Codigo de la fuente museografica: MET o CMA."),
    ("id_fuente", "identificacion", "Identificador institucional del objeto en la fuente."),
    ("numero_acceso", "identificacion", "Numero de acceso del museo, cuando la fuente lo entrega."),
    ("institucion", "identificacion", "Institucion responsable del registro."),
    ("url_objeto", "visual", "Enlace oficial al registro curatorial."),
    ("url_imagen", "visual", "Enlace a la imagen institucional de referencia."),
    ("url_imagen_miniatura", "visual", "Enlace a una imagen de menor resolucion, cuando existe."),
    ("ruta_imagen_local", "visual", "Ruta relativa de la copia local descargada (data/images, fuera de git)."),
    ("titulo_original", "textual", "Titulo original del registro curatorial."),
    ("titulo_es_sugerido", "textual", "Titulo sugerido en espanol, cuando existe."),
    ("descripcion", "textual", "Descripcion curatorial de la fuente, cuando existe."),
    ("cultura", "contextual", "Cultura o atribucion cultural registrada por la fuente."),
    ("periodo", "contextual", "Periodo historico o arqueologico, solo si la fuente lo entrega separado de la fecha."),
    ("fecha_objeto", "contextual", "Fecha estimada o descripcion cronologica del objeto."),
    ("procedencia", "contextual", "Pais, region o localidad registrados por la fuente."),
    ("departamento", "contextual", "Departamento del museo que custodia el objeto."),
    ("clasificacion_original", "estructural", "Clasificacion curatorial original de la fuente."),
    ("nombre_objeto_original", "estructural", "Nombre o tipo de objeto tal como lo registra la fuente."),
    ("tipo_objeto", "estructural", "Tipo de pieza normalizado (manto, tunica, bolso_textil, panel_textil, fragmento_textil...)."),
    ("origen_tipo_objeto", "estructural", "Origen de tipo_objeto: curacion (revision MET v2 o CMA) o regla (src/preprocessing)."),
    ("tipo_superficie", "estructural", "Utilidad morfologica para analisis visual, cuando se evaluo."),
    ("material", "estructural", "Material tal como lo registra la fuente."),
    ("material_normalizado", "estructural", "Materiales normalizados en espanol, separados por '; '."),
    ("origen_material_normalizado", "estructural", "Origen de material_normalizado: curacion o regla."),
    ("tecnica", "estructural", "Tecnica tal como la describe la fuente (MET no la entrega como campo)."),
    ("tecnica_normalizada", "estructural", "Tecnicas normalizadas en espanol (tejido, tapiz, bordado...), separadas por '; '."),
    ("origen_tecnica_normalizada", "estructural", "Origen de tecnica_normalizada: curacion o regla."),
    ("dimensiones", "estructural", "Dimensiones registradas por la fuente."),
    ("motivos", "iconografico", "Motivos observables (pendiente de anotacion)."),
    ("familia_iconografica", "iconografico", "Familia iconografica dominante (pendiente de anotacion)."),
    ("motivo_principal", "iconografico", "Motivo mas visible o relevante (pendiente de anotacion)."),
    ("decision_curacion_final", "curatorial", "Subconjunto final: principal o complementario."),
    ("motivo_curacion_final", "curatorial", "Justificacion breve de la decision de curacion."),
    ("decision_auditoria", "curatorial", "Decision registrada en la revision manual."),
    ("motivo_auditoria", "curatorial", "Motivo asociado a la decision de revision."),
    ("observacion_auditoria", "curatorial", "Comentario del revisor."),
    ("categoria_revision", "curatorial", "Categoria de revision automatica previa a la revision manual."),
    ("origen_curacion", "curatorial", "Etapa del flujo en la que el registro entro al corpus."),
    ("estado_licencia", "contextual", "Condicion de uso armonizada: dominio_publico o cc0."),
    ("licencia_fuente", "contextual", "Campo de licencia tal como lo entrega la fuente."),
    ("derechos_reproduccion", "contextual", "Aviso de derechos de reproduccion de la fuente, cuando existe."),
    ("estado_metadatos", "control", "Suficiencia de metadatos: completo, parcial o insuficiente."),
    ("estado_anotacion", "control", "Estado de anotacion manual: sin_anotar, anotado_manual, revisar, corregido o descartado."),
    ("estado_imagen", "control", "Estado de la imagen: util, baja_resolucion, no_disponible o requiere_revision."),
    ("observaciones", "control", "Comentarios metodologicos generados por el flujo (por ejemplo, imagen compartida)."),
    ("grupo_imagen_duplicada", "imagen", "Grupo de registros que comparten la misma imagen; vacio si es unica."),
    ("imagen_sha256", "imagen", "SHA-256 del archivo de imagen descargado."),
    ("imagen_dhash", "imagen", "Hash perceptual (dHash de 64 bits) de la imagen descargada."),
    ("imagen_ancho", "imagen", "Ancho en pixeles de la imagen descargada."),
    ("imagen_alto", "imagen", "Alto en pixeles de la imagen descargada."),
    ("terminos_andinos", "auxiliar_fuente", "Terminos que evidenciaron la relacion andina (CMA)."),
    ("terminos_textiles", "auxiliar_fuente", "Terminos que evidenciaron la condicion textil (CMA)."),
    ("consulta_origen", "auxiliar_fuente", "Consulta de busqueda con la que se recupero el registro."),
    ("archivo_origen", "trazabilidad", "CSV revisado del que proviene el registro."),
    ("fecha_descarga_metadatos", "trazabilidad", "Fecha de descarga de los metadatos de la fuente, cuando se registro."),
]

COLUMNAS: list[str] = [campo for campo, _, _ in ESQUEMA]

DECISIONES_VALIDAS = {"principal", "complementario"}
ESTADOS_LICENCIA_VALIDOS = {"dominio_publico", "cc0"}
ESTADOS_METADATOS_VALIDOS = {"completo", "parcial", "insuficiente"}
ESTADOS_IMAGEN_VALIDOS = {"util", "baja_resolucion", "no_disponible", "requiere_revision"}

# Campos que no pueden quedar vacios en ningun registro.
OBLIGATORIOS = [
    "id_global",
    "fuente",
    "id_fuente",
    "institucion",
    "url_objeto",
    "url_imagen",
    "titulo_original",
    "decision_curacion_final",
    "estado_licencia",
    "estado_metadatos",
    "estado_anotacion",
    "estado_imagen",
    "archivo_origen",
]
