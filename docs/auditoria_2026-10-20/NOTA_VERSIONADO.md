# Nota sobre el versionado de la auditoría

Esta carpeta reproduce, sin cambios, la auditoría entregada por el asesor el 20 de octubre de 2026. Se incorporó al repositorio el 6 de noviembre de 2026 (decisión D7 del plan de cierre), para que la revisión pueda leerse completa desde la rama `main`. Este es el único archivo agregado; ningún archivo de la entrega fue modificado.

Los archivos se guardan byte a byte (atributo `-text` en `.gitattributes`), porque algunos CSV usan finales de línea CRLF y la normalización del repositorio alteraría sus sumas.

Al verificar `SHA256SUMS.txt`, 46 archivos coinciden y 9 no coinciden: los informes `02`, `03`, `05`, `07`, `08`, `09`, `10`, `11` y `12`. La discrepancia ya estaba en la copia recibida: la carpeta original y esta copia son idénticas. Lo más probable es que esos informes se hayan editado después de calcular las sumas. Se conservan tal como se recibieron, y se pide al asesor que confirme cuál es la versión vigente.
