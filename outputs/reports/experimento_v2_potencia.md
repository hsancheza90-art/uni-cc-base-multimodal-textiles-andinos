# Planificacion de la potencia antes del test (desarrollo)

Generado por `python -m src.experimento.potencia`, paso del flujo (protocolo, seccion 7; decisiones R04, R27, R29, R34 y R35). **No se informa el nDCG medio de ningun sistema ni el signo de las diferencias**: el evaluador juzga despues la prueba.

## H1: efecto minimo detectable

Con las diferencias pareadas de nDCG@10 en las consultas de desarrollo y el numero de consultas de prueba, con nivel 0.05 y potencia 80%: EMD = (z_0,975 + z_0,8) · DE / raiz(n). El rango usa el intervalo del 95% de la DE estimada con pocas consultas. Es una estimacion aproximada de planificacion, no una frontera: no garantiza que un efecto mayor se detecte ni que uno menor no se detecte (R34).

| Comparacion | Consultas de desarrollo | DE de las diferencias | EMD con n de prueba | Rango del EMD | n de prueba | Consultas para detectar 0.03 |
|---|---|---|---|---|---|---|
| H1: M4 frente a M2 | 10 | 0.169 | 0.087 | 0.060 a 0.159 | 30 | 250 |

## H2: prueba exacta

H2 se contrasta con la enumeracion exacta de los 2^m cambios de signo, con m el numero de diferencias distintas de cero (R35). Solo pueden ser distintas de cero las de las consultas con palabra de bandas (R27), de modo que m <= b. La distribucion es discreta y la aproximacion normal no vale: en lugar de un efecto minimo detectable se informa la p minima alcanzable, 2^(1 - m), y el umbral practico equivalente en el subgrupo, 0,03 · n / b. La version anterior de este informe (R29) daba para H2 un EMD de 0,026 con la aproximacion normal; esa cifra se retira.

| Comparacion | Consultas de desarrollo | Diferencias distintas de cero en desarrollo | b: consultas de prueba con bandas | p minima con m = b | m minimo para p < 0.05 | Umbral equivalente en el subgrupo (n = 30) |
|---|---|---|---|---|---|---|
| H2: M3 frente a M3-sin-orden | 10 | 2 | 9 | 0.0039 | 6 | 0.100 |

- Consultas de desarrollo excluidas por no tener relevantes: H1 0, H2 0.
- Con m de 5 o menos, la prueba exacta no puede dar p < 0.05 cualquiera sea el resultado.
- El analisis del subgrupo tiene 2 consultas de desarrollo con palabra de bandas y 9 de prueba; es descriptivo y no puede confirmar H2 (R33).
- H2 solo recibe una conclusion confirmatoria si H1 se sostiene (secuencia fija, R33): con esta potencia, una conclusion confirmatoria sobre H2 es improbable.

Lectura: un resultado no significativo se informara como «no se detecto una mejora», no como ausencia de efecto. El numero de consultas de prueba no se modifica despues de abrir el test.
