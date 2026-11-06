# Grupos de piezas relacionadas (principal y complementario v2)

Generado por `python -m src.grupos.grupos` (`src/grupos/grupos.py`), paso del flujo. Parametros en `config/grupos.toml`; decisiones del revisor en `data/metadata/grupos_revision_v2.xlsx` (lo crea `python -m src.grupos.workbook`).

Un grupo reune los registros que muestran el mismo objeto o partes de el; es la unidad de particion del protocolo experimental. El informe da solo conteos: los pares incluyen piezas de la galeria, que se juzga a ciegas. Los pares estan en `data/metadata/grupos_candidatos_v2.csv`.

## Pares candidatos por senal

Un par puede tener varias senales. Umbrales: dHash <= 4; coseno M2 >= 0.95 (>= 0.93 entre museos); descripcion identica de 40 caracteres o mas; inventario con la misma base y sufijo de parte.

| Senal | Pares |
|---|---|
| `imagen_identica` | 13 |
| `inventario` | 52 |
| `descripcion` | 41 |
| `dhash` | 18 |
| `m2` | 28 |
| Pares distintos | 100 |

- Entre museos: 3. Con alguna pieza del nucleo: 55.

- Comprobacion de M2: de 18 piezas con imagen compartida conocida (`grupo_imagen_duplicada`), 18 tienen a una pieza de su grupo como vecina mas cercana.

## Decisiones

| Decision | Pares |
|---|---|
| unir | 65 |
| no_seguro | 0 |
| separar | 35 |
| pendiente | 0 |

`unir` incluye 13 pares de imagen identica propuestos con `revisor = auto`. `no_seguro` cuenta como unir (regla de [decisiones]).

## Grupos

| Piezas por grupo | Grupos |
|---|---|
| 1 | 555 |
| 2 | 15 |
| 3 | 2 |
| 4 | 3 |
| 5 | 1 |
| 7 | 1 |

- Grupos: 577 para 615 piezas del principal y del complementario.
- Nucleo de anotacion: 150 piezas en 146 grupos; 13 grupos del nucleo incluyen piezas de fuera del nucleo.

Todos los pares tienen decision: los grupos pueden congelarse.

## Avisos

Ninguno.

## Errores

Ninguno.
