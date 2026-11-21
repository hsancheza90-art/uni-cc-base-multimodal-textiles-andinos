# Rankings de desarrollo T3 (M0, M1, M2, M3, M3-sin-orden, M4, M4-RRF)

Generado por `python -m src.experimento.rankings` (`src/experimento/rankings.py`), paso del flujo. Parametros en `config/modelos.toml`. Solo consultas de desarrollo: las de prueba se ejecutan una vez, con los sistemas congelados. El evaluador no abre los rankings; este informe da solo conteos.

- Consultas de desarrollo: 10; galeria: 150 piezas; candidatos por consulta: de 149 a 149 (sin el grupo de la consulta).
- Consultas sin texto de ficha para M0: 0.

| Sistema | Consultas | Pares con score 0 | Pares sin evidencia estructural |
|---|---|---|---|
| M0 | 10 | 289 | 0 |
| M1 | 10 | 0 | 0 |
| M2 | 10 | 0 | 0 |
| M3 | 10 | 9 | 0 |
| M3-sin-orden | 10 | 9 | 0 |
| M4 | 10 | 1 | 0 |
| M4-RRF | 10 | 0 | 0 |

Total: 10430 filas (70 rankings completos). En M0, un score 0 indica que el candidato no comparte ningun termino con la consulta: esos candidatos quedan al final, por id. M3 y M3-sin-orden se calculan sobre la anotacion v2.1 congelada con los pesos iniciales de `[m3.pesos]`; un par sin ningun bloque observable en las dos piezas no tiene score y va al final, por id. M4 fusiona M0, M2 y M3 con los pesos fijados en `[m4.pesos]` (decision R28); M4-RRF suma 1 / (k + posicion) sobre los rankings de M0, M2 y M3, sin pesos.
