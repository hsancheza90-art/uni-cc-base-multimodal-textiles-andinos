# Seleccion de los pesos de M4 (desarrollo)

Generado por `python -m src.experimento.pesos_m4`, paso del flujo. **El evaluador no abre este informe**: contiene el rendimiento de los sistemas en desarrollo. Solo consultas y juicios de desarrollo; los candidatos sin juicio cuentan como 0. Regla de eleccion fijada antes de ver resultados (`elegir`): mayor nDCG@10 medio; en empate, la combinacion mas cercana a pesos iguales y luego la primera en orden lexicografico descendente.

- Combinaciones de la rejilla [0.0, 0.25, 0.5, 0.75, 1.0]: 91 (normalizadas a suma 1, sin repetir).
- Pesos que elige la regla con los juicios vigentes: M0 = 0.1429, M2 = 0.5714, M3 = 0.2857.
- Pesos fijados en `[m4] pesos`: M0 = 0.1429, M2 = 0.5714, M3 = 0.2857. Coinciden con la eleccion vigente.

## Las diez mejores combinaciones

| Pesos (M0, M2, M3) | nDCG@10 medio | Top 10 juzgado |
|---|---|---|
| 0.14, 0.57, 0.29 | 0.617 | 1.00 |
| 0.22, 0.44, 0.33 | 0.605 | 0.99 |
| 0.17, 0.33, 0.50 | 0.602 | 0.96 |
| 0.17, 0.50, 0.33 | 0.601 | 0.99 |
| 0.25, 0.50, 0.25 | 0.598 | 0.97 |
| 0.22, 0.33, 0.44 | 0.597 | 0.97 |
| 0.20, 0.40, 0.40 | 0.596 | 0.97 |
| 0.17, 0.67, 0.17 | 0.592 | 0.95 |
| 0.33, 0.44, 0.22 | 0.590 | 0.95 |
| 0.25, 0.38, 0.38 | 0.586 | 0.97 |
