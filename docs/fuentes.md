# Fuentes del corpus

Qué museos alimentan el corpus, cómo se extraen sus registros y qué fuentes se evaluaron y descartaron. Los conteos vigentes por fuente y etapa están en un solo lugar, `config/corpus.toml`, que el flujo verifica en cada ejecución; las licencias por objeto, en `data/processed/corpus_textiles_andinos_met_cma_v1_fuentes_licencias.csv` (v1).

## Criterio de selección

Solo se incorporan colecciones museográficas que cumplen las cuatro condiciones:

1. Imágenes en dominio público o con licencia CC0, registradas por objeto.
2. API pública que permita reconstruir la extracción (no se raspan páginas web).
3. Metadatos curatoriales suficientes para la trazabilidad: identificador, enlace oficial, cultura o procedencia, fecha y material o técnica.
4. Colección andina con volumen suficiente para aportar al estudio.

## Fuentes incluidas

| Fuente | Licencia de imagen | Extracción | Particularidades |
|---|---|---|---|
| The Metropolitan Museum of Art (MET) | Dominio público (Open Access) | `src/collectors/met_collector_v2.py`; el corpus parte de la curación MET v1 congelada en `data/processed/corpus_met_textiles_andinos_v1_*` | Las fechas vienen en texto libre («7th–9th century»); el inventario v1 las conserva. Algunas imágenes originales ya no existen en el museo (MET:312615). |
| Cleveland Museum of Art (CMA) | CC0 | `src/collectors/cma_collector.py` (consulta conservadora por cultura andina + «textile») | Una prueba con `type=Textile` recuperó 2045 registros casi todos no andinos y se descartó; la búsqueda conservadora dio 146 registros normalizados. |
| Art Institute of Chicago (AIC) | CC0 (imagen); descripción CC BY 4.0, que se cita | `src/collectors/aic_collector.py` | La API exige consultas estructuradas por POST (el parámetro `?q=` devuelve la colección completa), máximo 60 peticiones por minuto y la cabecera `AIC-User-Agent`. El IIIF sirve 1686 px de ancho y responde 403 si se pide más que el original. |

Los colectores escriben por defecto en `data/raw/<fuente>/` (fuera de git). La lista de candidatos versionada en `data/metadata/` es un insumo del corpus y solo se reemplaza con `--salida data/metadata/<archivo> --forzar`, porque sobre ella se tomaron decisiones manuales.

## Criterio de candidatura

Un registro recuperado pasa a ser candidato para la revisión cuando tiene imagen oficial y metadatos mínimos de trazabilidad, y además presenta evidencia textil (clasificación o material textil, o términos como *textile*, *woven*, *tunic*, *mantle*, *tapestry*) y evidencia andina (Perú, Inca, Paracas, Nasca, Wari, Chancay, Moche, Tiwanaku u otras). El filtro (`src/preprocessing/textile_filters.py`) busca los términos como palabra completa y descarta de forma automática las herramientas de hilado y tejido.

Ser candidato no implica entrar al corpus: la decisión es manual, con el criterio de aptitud analítica de `docs/protocolo_aptitud_v2.md`.

## Fuentes evaluadas y no incluidas

| Fuente | Motivo |
|---|---|
| British Museum, Museo de Berlín, Field Museum, Penn Museum, MFA Boston, NMAI/NMNH (Smithsonian), Brooklyn Museum, LACMA | Licencia de imagen incompatible o acceso sin API reutilizable. |
| Museos peruanos | Solo serían posibles mediante convenio institucional. |
| Yale University Art Gallery | Candidata para una cuarta fuente: cultura estructurada, resolución irregular. |
| Cooper Hewitt | Candidata para una cuarta fuente: CC0 y técnica detallada, pero sin cultura; pide clave de api.data.gov. |
