# Snapshot experimental v2: particiones y consultas T3

Generado por `python -m src.experimento.snapshot` (`src/experimento/snapshot.py`), paso del flujo. Parametros en `config/experimento.toml`; protocolo en `docs/protocolo_experimental_v2.md` (seccion 5). Los insumos congelados son `data/metadata/particiones_v2.csv` y `data/metadata/consultas_t3_v2.csv`.

Solo conteos: la galeria se juzga a ciegas y el lote 1 se re-anota a ciegas.

- Galeria: 150 piezas del nucleo en 146 grupos.
- Proporcion de desarrollo: 0.3 de los grupos, por museo.

## Piezas, grupos y consultas por museo y particion

| Museo | Piezas desarrollo | Grupos desarrollo | Consultas desarrollo | Piezas prueba | Grupos prueba | Consultas prueba |
|---|---|---|---|---|---|---|
| AIC | 22 | 22 | 6 | 52 | 51 | 15 |
| CMA | 9 | 9 | 2 | 25 | 22 | 7 |
| MET | 13 | 13 | 2 | 29 | 29 | 8 |

## Consultas por tipo de composicion (todas)

| Composicion | Consultas |
|---|---|
| `bandas` | 13 |
| `borde` | 3 |
| `campo_central` | 7 |
| `composicion_libre` | 3 |
| `paneles` | 7 |
| `reticula` | 7 |

## Comprobacion de fugas

Sin fugas: ningun grupo esta en las dos particiones, cada consulta esta en la particion de su pieza, hay a lo sumo una consulta por grupo, todas tienen composicion observable y su numero es el de la configuracion.
