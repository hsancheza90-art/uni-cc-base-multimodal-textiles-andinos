# M2: embeddings OpenCLIP (v2)

Generado por `python -m src.modelos.m2_openclip` (`src/modelos/m2_openclip.py`), fuera del flujo: necesita torch y las copias de evaluacion locales. Parametros en `config/modelos.toml` ([m2]); protocolo en `docs/protocolo_experimental_v2.md` (seccion 4). Sistema congelado: sin ajuste ni entrenamiento.

## Checkpoint

- Arquitectura: `xlm-roberta-base-ViT-B-32`; pesos: `laion5b_s13b_b90k` (`laion/CLIP-ViT-B-32-xlm-roberta-base-laion5B-s13B-b90k`, revision `506d40eb551f4801a1c27fc20a31c7b8f590deda`).
- Archivo de pesos: `open_clip_pytorch_model.bin`, SHA-256 `a5412f19cca70db8d434f68361f7254bd322a553455a63dbb709bd6a650cf378`. Licencia: MIT.
- Precision: fp32; lote: 32; encuadre: `relleno_cuadrado`; dispositivo: Intel64 Family 6 Model 197 Stepping 2, GenuineIntel.
- Versiones: python 3.15.2, torch 2.15.0, torchvision 0.29.2, open_clip_torch 3.3.0, transformers 5.22.1, huggingface_hub 2.4.0, numpy 2.5.3, Pillow 12.3.0.

## Salidas

- `data/metadata/m2_openclip_embeddings_v2.npy`: 873 imagenes x 512 dimensiones, float32, filas de norma 1 redondeadas a 6 decimales. SHA-256 `131418045b53748651594469bf8339e27a7438b8ea392c0610af741e9dcee78f`.
- `data/metadata/m2_openclip_indice_v2.csv`: id_global, fuente y SHA-256 de la copia de cada fila. SHA-256 `29bc0021ea7bf4aae710177bc303672823974355217f242b91c9ccd3ef7f3acb`.
- `data/metadata/m2_openclip_manifiesto_v2.json`: este registro en JSON.

## Comprobaciones

| Comprobacion | Resultado | Cumple |
|---|---|---|
| Normas de las filas guardadas | 0.999999 a 1.000001 | si |
| Determinismo: dos pasadas sobre 32 imagenes, diferencia maxima | 0.0e+00 (tolerancia 1e-05) | si |

El informe no muestra rankings ni vecinos: la galeria del protocolo (el nucleo) se juzga a ciegas. Los embeddings tambien proponen candidatos a duplicado para los grupos v2 (`outputs/reports/grupos_v2.md`).
