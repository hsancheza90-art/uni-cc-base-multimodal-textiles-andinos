# Rankings de desarrollo T3 (M0, M1 y M2)

Generado por `python -m src.experimento.rankings` (`src/experimento/rankings.py`), paso del flujo. Parametros en `config/modelos.toml`. Solo consultas de desarrollo: las de prueba se ejecutan una vez, con los sistemas congelados. El evaluador no abre los rankings; este informe da solo conteos.

- Consultas de desarrollo: 10; galeria: 150 piezas; candidatos por consulta: de 149 a 149 (sin el grupo de la consulta).
- Consultas sin texto de ficha para M0: 0.

| Sistema | Consultas | Pares consulta-candidato con score 0 |
|---|---|---|
| M0 | 10 | 289 |
| M1 | 10 | 0 |
| M2 | 10 | 0 |

Total: 4470 filas (30 rankings completos). En M0, un score 0 indica que el candidato no comparte ningun termino con la consulta: esos candidatos quedan al final, por id.
