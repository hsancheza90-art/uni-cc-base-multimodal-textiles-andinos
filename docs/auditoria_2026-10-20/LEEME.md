### Auditoría de textiles andinos, 20 de octubre de 2026

#### Cómo leer la entrega
Comenzar por 12_DICTAMEN_FINAL.md, después 09_BACKLOG_MEJORAS_PRIORIZADAS.md y 10_PLAN_SEIS_SEMANAS.md. Los informes 01–08 justifican el diagnóstico. El 11 propone la estructura académica. El 04 es una matriz CSV, no un resultado experimental.

Los doce entregables solicitados están en este directorio. evidencias contiene registros de ejecución, inspección de datos, reproducciones de defectos y el ensayo LOMO. revision contiene protocolo previo, resultados bibliográficos, cribado individual, BibTeX y conteos del mapeo parcial.

No se incluye una copia de las imágenes museales, ni del repositorio completo, ni se afirma haberlas descargado otra vez. No se modificaron datos curatoriales ni fuentes originales. Los informes distinguen verificación actual, resultados archivados y experimentos pendientes.

#### Reproducir la auditoría
Descomprimir conservando la carpeta auditoria. Desde su carpeta padre:
    
    git clone https://github.com/hsancheza90-art/uni-cc-base-multimodal-textiles-andinos.git repo
    git -C repo checkout c38996e3af4b1874498e7e3e24ed4fc5c3e59471
    python -m venv .venv
    . .venv/bin/activate
    python -m pip install -r repo/requirements-dev.txt
    python auditoria/evidencias/audit_data.py
    python auditoria/evidencias/reproduce_defects.py
    python auditoria/evidencias/evaluate_transfer.py

Los scripts vuelven a escribir SUS evidencias dentro de auditoria. Preservar una copia del paquete entregado si se desean comparar resultados. No escriben decisiones curatoriales originales. Para regenerar el flujo, copiar repo a repo_ejecucion y ejecutar desde esa copia:

    python -m src.flujo
    python -m pytest
    git status --porcelain
    git diff --exit-code

El log original de pytest corresponde a la copia repo y el flujo a repo_ejecucion. Las pruebas trabajan con directorios temporales. Las dependencias exactas y plataforma observada están en evidencias/entorno_final.json. Cambios de Python/BLAS pueden afectar resultados numéricos, registrar diferencias en lugar de forzar igualdad.

Para regenerar matriz, cribado y conteos de revisión desde la extracción conservada:
    
    python auditoria/revision/build_review.py

Esto no vuelve a buscar en Internet ni completa textos pendientes. Las consultas nativas Crossref y metadatos de las respuestas originales se conservan. El universo PRISMA tiene 64 registros importados, no todos los enlaces web encontrados. Véase informe03 antes de reutilizar el diagrama.

#### Estados
VERIFICADO, PARCIAL, NO_IMPLEMENTADO, INCONSISTENTE y NO_VERIFICABLE describen requisitos científicos.
PASS, FAIL, NOT_RUN, BLOCKED y NOT_APPLICABLE describen ejecuciones/contratos.
Un FAIL en una reproducción de defecto significa que el contrato esperado no se cumple, aunque el script de auditoría termine correctamente.

La revisión bibliográfica es parcial. La estimación 32% es orientativa y ponderada, no una nota oficial. El LOMO es diagnóstico retrospectivo; sus intervalos por registros no resuelven dependencia ni incertidumbre de entrenamiento. No hay resultados M0–M4 fabricados.

