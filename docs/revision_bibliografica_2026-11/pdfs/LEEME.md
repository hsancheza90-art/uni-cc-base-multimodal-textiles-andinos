# PDF consultados

Esta carpeta está preparada para los PDF, pero **los archivos todavía no están aquí**. El entorno en el que se hizo la revisión permite leer el texto de los artículos pero no descargar los binarios. Para bajarlos en un paso, desde la raíz del repositorio:

```
python docs/revision_bibliografica_2026-11/descargar.py
```

El script lee `MANIFIESTO.csv`, descarga cada PDF de su fuente de acceso abierto, comprueba que el archivo empiece por `%PDF` y escribe `descargas.log` con el SHA-256 de cada uno. Usa solo la biblioteca estándar de Python.

- 29 de los 30 documentos tienen enlace directo. F23 (CARE) se baja a mano desde la página de su DOI.
- Algunos sitios (MDPI, PLOS) pueden rechazar descargas automáticas; el registro indica cuáles fallaron para bajarlos desde el navegador.
- Los PDF tienen derechos de sus autores y editoriales. Conviene no versionarlos: añade `docs/revision_bibliografica_2026-11/pdfs/*.pdf` a `.gitignore`. El manifiesto y las fichas sí se versionan.
