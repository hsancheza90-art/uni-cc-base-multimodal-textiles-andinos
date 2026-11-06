# M1: caracteristicas de color y textura (v2)

Generado por `python -m src.modelos.m1_vision` (`src/modelos/m1_vision.py`), fuera del flujo: lee las copias de evaluacion locales. Parametros en `config/modelos.toml` ([m1]); segmentacion del textil en `config/aptitud.toml` ([segmentacion]).

- `data/metadata/m1_caracteristicas_v2.npy`: 873 imagenes x 266 valores (256 de color Lab y 10 de textura LBP riu2), float32 redondeado a 6 decimales. SHA-256 `39d09f1a8c8be1a0f96a455c66b6718cae8774a870bc9e73addf3ee592dacfb1`.
- `data/metadata/m1_indice_v2.csv`: id_global, fuente, SHA-256 de la copia y fraccion de la imagen que ocupa el textil.
- Fraccion del textil: mediana 0.634, minima 0.030.

Sin rankings ni vecinos: la galeria del protocolo se juzga a ciegas.
