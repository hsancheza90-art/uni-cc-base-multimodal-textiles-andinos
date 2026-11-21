# F20 · Urbano (2019)

**Statistical Significance Testing in Information Retrieval: An Empirical Analysis of Type I, Type II and Type III Errors**

| Campo | Valor |
|---|---|
| Autores | Urbano, J.; Lima, H.; Hanjalic, A. |
| Año y sede | 2019. Proceedings of the 42nd International ACM SIGIR Conference (SIGIR '19), 21-25 de julio de 2019, París; 10 páginas (p. 1) |
| Identificador | arXiv:1905.11096 (v2, 5 de junio de 2019) · doi:10.1145/3331184.3331259 |
| PDF | `pdfs/F20_urbano_2019_pruebas_significacion.pdf` · https://arxiv.org/pdf/1905.11096 |
| Eje | G. Evaluación de recuperación |
| Origen del registro | búsqueda dirigida |
| Nivel de lectura | completo (texto extraído del PDF, 10 páginas; revisado el 20-11-2026). Las curvas de las figuras 2-6 no son legibles en el texto extraído; sí sus leyendas y el texto que las comenta |

## Qué hace

- **Datos.** Datos simulados (paquete simIReff 1.0, márgenes y cópulas) ajustados a 326 ejecuciones de TREC 5–8 Ad hoc y 193 de TREC 2010–13 Web (90 % superior); tamaños de 25, 50 y 100 temas; más de 500 millones de valores p (pp. 4-5). Medidas: AP, P@10 y RR (Ad hoc); nDCG@20 y ERR@20 (Web) (p. 5). No estudian nDCG@10 ni menos de 25 temas.
- **Tarea y protocolo.** Qué prueba pareada mantiene el error de tipo I en el nivel nominal y tiene más potencia con datos de recuperación; también error de tipo III (p. 2).
- **Método.** Simulación con hipótesis nula conocida. Comparan t de Student, Wilcoxon, signos, bootstrap con desplazamiento y permutación (sec. 3.1, pp. 3-4). La permutación es exactamente la del diseño de la tesis: Monte Carlo con cambio de signo de cada diferencia con probabilidad 0,5; el valor p bilateral es la fracción de réplicas con |media| ≥ |media observada| (ec. 8, p. 4). Usan 1 millón de réplicas y dan la fórmula del error de estimación del valor p (ec. 9, p. 4).
- **Comparadores.** Las cinco pruebas entre sí.
- **Resultados.** Tipo I (p. 6-7): con 50 temas y α = 0,05, t y permutación dan 0,05; el bootstrap 0,059 bilateral y 0,054 unilateral; con α = 0,01, el bootstrap sube a 0,014. Con pocos temas (25), Wilcoxon y signos cometen más errores de los esperados, sobre todo con α bajo, y empeoran al crecer la muestra; el bootstrap es demasiado optimista y mejora con más temas; la permutación «se comporta bastante mejor» y se acerca a la diagonal al crecer la muestra; la t es «notablemente cercana al ideal incluso con muestras pequeñas», salvo que es conservadora con α bajos y muestras pequeñas en ERR@20 y RR (p. 6). Potencia (pp. 7-8): bootstrap y Wilcoxon son algo más potentes, sobre todo con muestras pequeñas, pero a costa de más errores de tipo I; t y permutación casi idénticas. Tipo III: no despreciable, hasta 2 % con P@10, RR o pocos temas (p. 2); con AP, 50 temas y δ = 0,01, el 7,3 % de los resultados significativos podría tener el signo equivocado (p. 9). Recomiendan la t pareada para medias y la permutación para otros estadísticos; proponen abandonar el bootstrap con desplazamiento, salvo con colecciones muy grandes, y Wilcoxon y signos (pp. 2 y 9).
- **Limitaciones declaradas.** No figura una sección de limitaciones. Advierten que el modelo simulado representa sistemas hipotéticos que se comportan como los de TREC, no los sistemas reales (p. 5).
- **Código y datos.** github.com/julian-urbano/sigir2019-statistical (p. 2, nota 3).

## Aporte a la tesis

Afecta a una decisión del protocolo que aún está abierta. El protocolo prevé bootstrap pareado para el intervalo y permutación como sensibilidad. Este estudio indica que, como prueba de hipótesis, el bootstrap tiende a valores p pequeños con pocos temas, y que t pareada y permutación se comportan casi igual y bien. Conviene dejar escrito antes del test que el contraste de H1 y H2 se decide con permutación o t pareada y que el bootstrap se usa solo para el intervalo.

## Cautela al citar

Confirmado en la sección 4 completa: la crítica es al bootstrap con desplazamiento como prueba de hipótesis; el artículo no evalúa intervalos de confianza por bootstrap. El menor tamaño estudiado es 25 temas y la medida más cercana es nDCG@20: extrapolar a 10 consultas de desarrollo o a nDCG@10 no está respaldado por el texto.

## Actualización del 20 de noviembre de 2026

- Verificado con página: permutación por cambio de signo (ec. 7-8, p. 4); error de tipo I de t, permutación y bootstrap con 50 temas (p. 7); comportamiento de Wilcoxon, signos, bootstrap, permutación y t con 25 temas (p. 6); potencia (pp. 7-8) y tipo III (pp. 2 y 9), antes en el tramo no literal.
- Corregido: la «robustez con muestras pequeñas» se atribuye a la t (p. 2 y p. 9); para la permutación el texto dice que se acerca a la diagonal al crecer la muestra, sin dar la cifra con 25 temas. Se añadieron sede completa y DOI.
- Afecta al diseño: decidir H1 y H2 con permutación por cambio de signo y usar la t pareada como comprobación es coherente con la recomendación (ambas casi idénticas en tipo I y potencia); el bootstrap pareado debe quedar solo para el intervalo, nunca como prueba. Con 10 000 réplicas, aplicando la ec. 9 del artículo (cálculo propio), el error típico del valor p en torno a 0,05 es ≈ 0,0022 (≈ 4,4 % relativo): conviene informarlo o aumentar réplicas si un valor p queda cerca del umbral. Con 30 consultas (entre 25 y 50 del estudio) el respaldo es razonable; con 10 consultas de desarrollo no hay evidencia en el artículo.
- Sin pendientes de verificación en el texto; las curvas exactas por tamaño solo están en las figuras y el material suplementario.

---
Leído el 11 de noviembre de 2026 y completado el 20 de noviembre de 2026 con asistencia computacional, sobre el texto completo extraído del PDF. «NV» marca lo que no se pudo comprobar.
