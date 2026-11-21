# Efecto minimo detectable antes del test (desarrollo)

Generado por `python -m src.experimento.potencia`, paso del flujo (protocolo, seccion 7; decisiones R04 y R27). Se calcula con las diferencias pareadas de nDCG@10 en las consultas de desarrollo y el numero de consultas de prueba, con nivel 0.05 y potencia 80%: EMD = (z_0,975 + z_0,8) · DE / raiz(n). El rango usa el intervalo del 95% de la DE estimada con pocas consultas. **No se informa el nDCG medio de ningun sistema ni el signo de las diferencias**: el evaluador juzga despues la prueba.

| Comparacion | Consultas de desarrollo | DE de las diferencias | EMD con n de prueba | Rango del EMD | n de prueba | Consultas para detectar 0.03 |
|---|---|---|---|---|---|---|
| H1: M4 frente a M2 | 10 | 0.169 | 0.087 | 0.060 a 0.159 | 30 | 250 |
| H2: M3 frente a M3-sin-orden (30 consultas) | 10 | 0.051 | 0.026 | 0.018 a 0.048 | 30 | 24 |
| H2 secundario: consultas con palabra de bandas | 2 | no estimable | — | — | 9 | — |

- Consultas de desarrollo excluidas por no tener relevantes: H1 0, H2 0.
- En H2, 8 de 10 diferencias de desarrollo son exactamente cero: las consultas sin palabra de bandas dan el mismo score en M3 y en su control (R27). Por eso su DE es pequena, pero el efecto medio se diluye en la misma proporcion: si solo actua en las 9 consultas de prueba con bandas, en ellas tendria que ser unas 30/9 veces el EMD de la tabla para detectarse en la media de las 30.
- El analisis secundario de H2 tiene 2 consultas de desarrollo con palabra de bandas y 9 de prueba; con tan pocas consultas de desarrollo su desviacion no es estimable con fiabilidad.

Lectura: si el EMD supera el umbral practico, el estudio no tiene potencia para detectar un efecto de esa magnitud. Un resultado no significativo se informara entonces como «no se detecto una mejora de la magnitud detectable», no como ausencia de efecto. El numero de consultas de prueba no se modifica despues de abrir el test.
