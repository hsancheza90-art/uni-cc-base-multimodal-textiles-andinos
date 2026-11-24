# Resultados del test (T3 y T1)

Generado por `python -m src.experimento.ejecucion_prueba --evaluar`, una sola vez, con los sistemas congelados y los juicios de prueba hechos sin asistencia (decisiones R27, R30 y R37). Reglas de decision: protocolo, secciones 1 y 7 (R33 a R35). El intervalo es descriptivo.

## 1. Integridad de la corrida

| Elemento | Valor |
|---|---|
| Corrida | corrida-1d7165cf4dab |
| Estados | autorizada > insumos_sellados > rankings_sellados > juicios_cerrados > evaluada |
| Commit sellado | cc501aef53628bcaabff9b02bc3ada7e892d223e |
| Huellas comprobadas | 25 (todas coinciden) |
| Comprobacion de fugas | sin problemas (comprobacion previa) |
| Cegamiento de los libros | T1: sin problemas, T3: sin problemas |

## 2. Pool y juicios

- Consultas sin ningun relevante, excluidas de la media: 0 (ninguna).

| Sistema | no_evaluable en el top 10 | Consultas con no_evaluable | Proporcion juzgada del top 10 |
|---|---|---|---|
| M0 | 0 | ninguna | 1.000 |
| M1 | 0 | ninguna | 1.000 |
| M2 | 0 | ninguna | 1.000 |
| M3 | 0 | ninguna | 1.000 |
| M3-sin-orden | 0 | ninguna | 1.000 |
| M4 | 0 | ninguna | 1.000 |
| M4-RRF | 0 | ninguna | 1.000 |

Cobertura del pool por consulta. Un candidato no juzgado cuenta como 0 (supuesto del pooling, protocolo seccion 6):

| Consulta | Pares del pool | Juzgados | Relevantes (>= 1) | Relevantes (>= 2) | no_evaluable |
|---|---|---|---|---|---|
| T3-P01 | 45 | 45 | 9 | 6 | 0 |
| T3-P02 | 50 | 50 | 18 | 11 | 0 |
| T3-P03 | 40 | 40 | 23 | 15 | 0 |
| T3-P04 | 40 | 40 | 23 | 10 | 0 |
| T3-P05 | 43 | 43 | 12 | 3 | 0 |
| T3-P06 | 39 | 39 | 16 | 13 | 0 |
| T3-P07 | 48 | 48 | 19 | 14 | 0 |
| T3-P08 | 40 | 40 | 8 | 5 | 0 |
| T3-P09 | 45 | 45 | 7 | 4 | 0 |
| T3-P10 | 44 | 44 | 12 | 6 | 0 |
| T3-P11 | 40 | 40 | 14 | 13 | 0 |
| T3-P12 | 46 | 46 | 20 | 11 | 0 |
| T3-P13 | 46 | 46 | 11 | 6 | 0 |
| T3-P14 | 42 | 42 | 14 | 10 | 0 |
| T3-P15 | 46 | 46 | 23 | 14 | 0 |
| T3-P16 | 45 | 45 | 12 | 7 | 0 |
| T3-P17 | 49 | 49 | 4 | 3 | 0 |
| T3-P18 | 35 | 35 | 17 | 17 | 0 |
| T3-P19 | 42 | 42 | 1 | 0 | 0 |
| T3-P20 | 42 | 42 | 13 | 10 | 0 |
| T3-P21 | 47 | 47 | 14 | 10 | 0 |
| T3-P22 | 48 | 48 | 17 | 15 | 0 |
| T3-P23 | 38 | 38 | 13 | 11 | 0 |
| T3-P24 | 48 | 48 | 18 | 11 | 0 |
| T3-P25 | 39 | 39 | 18 | 10 | 0 |
| T3-P26 | 44 | 44 | 11 | 4 | 0 |
| T3-P27 | 41 | 41 | 15 | 13 | 0 |
| T3-P28 | 51 | 51 | 19 | 11 | 0 |
| T3-P29 | 31 | 31 | 12 | 9 | 0 |
| T3-P30 | 29 | 29 | 12 | 8 | 0 |

Sensibilidad a los aportes exclusivos: cada sistema recalculado con los pares que solo el aporto tratados como no juzgados (Buckley et al., 2007):

| Sistema | nDCG@10 medio | Sin sus aportes exclusivos | Aportes exclusivos |
|---|---|---|---|
| M0 | 0.349 | 0.300 | 147 |
| M1 | 0.302 | 0.198 | 184 |
| M2 | 0.492 | 0.443 | 96 |
| M3 | 0.338 | 0.336 | 12 |
| M3-sin-orden | 0.353 | 0.351 | 9 |
| M4 | 0.604 | 0.602 | 4 |
| M4-RRF | 0.544 | 0.540 | 14 |

## 3. H1: M4 frente a M2

| Elemento | Valor |
|---|---|
| Consultas (n) | 30 |
| Diferencia media | 0.112 |
| IC 95 % (bootstrap) | 0.062 a 0.164 |
| p (permutacion, B = 100000) | 0.00015 |
| Error de Monte Carlo de la p | 0.00004 |
| t pareada (p) | 4.259 (0.0002) |
| (a) Frente a cero: p < 0.05 | si |
| (c) Relevancia practica: diferencia >= 0.03 | si |
| Lectura y veredicto | se sostiene |

La p contrasta la diferencia frente a cero; la relevancia practica se refiere a la diferencia observada y no prueba que el efecto poblacional alcance 0.03, umbral que no se contrasto. Si la p y el intervalo parecen discrepar, se informan ambos y decide la permutacion. Con potencia limitada, un efecto seleccionado por significacion puede estar sobrestimado. Una p no significativa no demuestra que no haya mejora (protocolo, seccion 7).

## 4. H2: M3 frente a M3-sin-orden

| Elemento | Valor |
|---|---|
| Consultas (n) | 30 |
| b: consultas evaluables con palabra de bandas | 9 |
| m: diferencias distintas de cero | 9 |
| p exacta (2^m vectores) | 0.22266 |
| p minima alcanzable | 0.00391 |
| Diferencia media | -0.015 |
| IC 95 % (bootstrap) | -0.040 a 0.006 |
| Compuerta de H1 (secuencia fija) | abierta |
| Lectura y veredicto | no se detectó una mejora |

Subgrupo de bandas (descriptivo; no puede confirmar H2):

| Elemento | Valor |
|---|---|
| Consultas | 9 |
| Diferencia media | -0.050 |
| IC 95 % (bootstrap) | -0.121 a 0.020 |
| p exacta | 0.22266 |
| Umbral equivalente (0.03 · n / b) | 0.100 |

## 5. H3: fidelidad computacional de M4

| Elemento | Valor |
|---|---|
| Resultados comprobados (top 10 de M4) | 300 |
| Error maximo de reconstruccion | 0.00e+00 |
| Error maximo de intervencion | 0.00e+00 |
| Diferencia maxima con la puntuacion versionada (6 decimales) | 0.00e+00 |
| Veredicto (tolerancia 1e-09) | se sostiene |

Revision humana de las explicaciones (descriptiva, no independiente, no interviene en H3): completa.

| Clase | correcta | incorrecta | especulativa | no_evaluable |
|---|---|---|---|---|
| acierto | 5 | 0 | 0 | 0 |
| error | 4 | 1 | 0 | 0 |

Componente en desacuerdo: ninguno: 9, M0: 0, M2: 1, M3: 0, varios: 0. Denominador: las fichas sorteadas; las `no_evaluable` se informan y no se reemplazan.

## 6. Metricas de todos los sistemas (media sobre las consultas; por consulta en `data/processed/experimento_v2_metricas_por_consulta.csv`)

| Sistema o variante | nDCG@10 medio |
|---|---|
| Control negativo | 0.418 |
| M0 | 0.349 |
| M1 | 0.302 |
| M2 | 0.492 |
| M3 | 0.338 |
| M3 sin bandas | 0.347 |
| M3 solo bandas | 0.105 |
| M3-sin-orden | 0.353 |
| M4 | 0.604 |
| M4 con M3-sin-orden | 0.608 |
| M4 sin M0 | 0.570 |
| M4 sin M3 | 0.523 |
| M4-RRF | 0.544 |

## 7. Ablaciones, control negativo y M4-RRF (exploratorias)

Diferencias pareadas con su intervalo; su p no se interpreta como confirmacion. El control negativo usa una sola permutacion y es descriptivo.

| Comparacion | Consultas | Diferencia media | IC 95 % | p permutacion | Lectura |
|---|---|---|---|---|---|
| M4 frente a M0 | 30 | 0.256 | 0.171 a 0.349 | 0.0000 | se sostiene |
| M4 frente a M1 | 30 | 0.302 | 0.186 a 0.415 | 0.0001 | se sostiene |
| M4 frente a M3 | 30 | 0.266 | 0.191 a 0.350 | 0.0000 | se sostiene |
| M4 frente a M4-RRF | 30 | 0.061 | 0.016 a 0.111 | 0.0104 | se sostiene |
| M4 frente a M4 sin M3 | 30 | 0.081 | 0.039 a 0.124 | 0.0007 | se sostiene |
| M4 frente a M4 sin M0 | 30 | 0.035 | 0.005 a 0.065 | 0.0310 | se sostiene |
| M4 frente a M4 con M3-sin-orden | 30 | -0.003 | -0.009 a 0.001 | 0.3293 | no se detectó una mejora |
| M4 frente a Control negativo | 30 | 0.187 | 0.127 a 0.253 | 0.0000 | se sostiene |
| M3 solo bandas frente a M3 sin bandas | 30 | -0.241 | -0.337 a -0.148 | 0.0000 | inferior al sistema de referencia |

## 8. Robustez por museo y por estado de la pieza (descriptiva)

| Criterio | Grupo | Consultas | M2 | M3 | M3-sin-orden | M4 |
|---|---|---|---|---|---|---|
| museo | AIC | 15 | 0.513 | 0.399 | 0.420 | 0.616 |
| museo | CMA | 7 | 0.573 | 0.210 | 0.228 | 0.624 |
| museo | MET | 8 | 0.384 | 0.336 | 0.336 | 0.566 |
| completitud | completo | 14 | 0.540 | 0.317 | 0.350 | 0.650 |
| completitud | incompleto | 5 | 0.496 | 0.469 | 0.442 | 0.561 |
| completitud | sin dato | 11 | 0.431 | 0.305 | 0.317 | 0.566 |

## 9. T1: texto a imagen (exploratoria, descriptiva)

| Sistema | Consultas | nDCG@10 medio |
|---|---|---|
| M0 | 6 | 0.295 |
| M2 | 6 | 0.414 |
| M3 | 3 | 0.183 |
| M4 | 6 | 0.499 |

## 10. Desviaciones del protocolo

Se registran, con su motivo, en `docs/registro_custodia.md`. Este informe no las infiere.
