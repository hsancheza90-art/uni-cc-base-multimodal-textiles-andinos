# M2: candidatos a duplicado (principal v2)

Generado por `python -m src.modelos.candidatos_duplicado` (`src/modelos/candidatos_duplicado.py`), paso del flujo, desde los embeddings versionados de M2 (`data/metadata/m2_openclip_embeddings_v2.npy`). Umbral en `config/modelos.toml` ([m2.duplicados]): coseno >= 0.95.

Son candidatos para la decision humana del workbook de grupos (S1.7), nunca uniones automaticas. El informe da solo conteos, sin pares ni vecinos, porque la galeria del protocolo experimental se juzga a ciegas; los pares estan en `data/metadata/m2_candidatos_duplicado_v2.csv`.

- Piezas del principal v2 con embedding: 462.
- Pares candidatos: 25; con la misma copia de evaluacion (mismo archivo): 11.

## Pares por tramo de coseno y por museo

| Coseno | Pares |
|---|---|
| 0,99 o mas | 12 |
| 0,97 a 0,99 | 2 |
| umbral a 0,97 | 11 |

| Museos | Pares |
|---|---|
| mismo museo | 25 |
| entre museos | 0 |

## Comprobacion con las imagenes compartidas conocidas

`grupo_imagen_duplicada` marca piezas del principal v2 que comparten imagen (misma URL, archivo o pixeles). Si M2 es coherente, cada una tiene a una pieza de su grupo como vecina mas cercana.

- Piezas en grupos conocidos: 16; con una pieza de su grupo como vecina mas cercana: 16.
- Pares dentro de grupos conocidos: 12; con coseno sobre el umbral: 12.
