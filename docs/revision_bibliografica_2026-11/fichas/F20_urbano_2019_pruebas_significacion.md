# F20 · Urbano (2019)

**Statistical Significance Testing in Information Retrieval: An Empirical Analysis of Type I, Type II and Type III Errors**

| Campo | Valor |
|---|---|
| Autores | Urbano, J.; Lima, H.; Hanjalic, A. |
| Año y sede | 2019. SIGIR 2019 |
| Identificador | arXiv:1905.11096 |
| PDF | `pdfs/F20_urbano_2019_pruebas_significacion.pdf` · https://arxiv.org/pdf/1905.11096 |
| Eje | G. Evaluación de recuperación |
| Origen del registro | búsqueda dirigida |
| Nivel de lectura | parcial: primeros ~40 000 caracteres literales; el resto, resumen automático |

## Qué hace

- **Datos.** Datos simulados ajustados a TREC 5–8 Ad hoc y TREC 2010–13 Web; tamaños de 25, 50 y 100 temas; más de 500 millones de valores p.
- **Tarea y protocolo.** Qué prueba pareada mantiene el error de tipo I en el nivel nominal y tiene más potencia con datos de recuperación.
- **Método.** Simulación con hipótesis nula conocida. Comparan t de Student, Wilcoxon, signos, bootstrap con desplazamiento y permutación.
- **Comparadores.** Las cinco pruebas entre sí.
- **Resultados.** Con 50 temas y α = 0,05, t y permutación dan 0,05 y el bootstrap 0,059 (sec. 4.1). Wilcoxon y signos son demasiado optimistas. Recomiendan la t pareada, que es robusta incluso con muestras pequeñas, y la permutación para estadísticos que no son medias; proponen abandonar el bootstrap con desplazamiento. Los resultados de potencia quedaron en el tramo no literal.
- **Limitaciones declaradas.** Sin sección de limitaciones en el texto literal.
- **Código y datos.** github.com/julian-urbano/sigir2019-statistical

## Aporte a la tesis

Afecta a una decisión del protocolo que aún está abierta. El protocolo prevé bootstrap pareado para el intervalo y permutación como sensibilidad. Este estudio indica que, como prueba de hipótesis, el bootstrap tiende a valores p pequeños con pocos temas, y que t pareada y permutación se comportan casi igual y bien. Conviene dejar escrito antes del test que el contraste de H1 y H2 se decide con permutación o t pareada y que el bootstrap se usa solo para el intervalo.

## Cautela al citar

La crítica es al bootstrap como prueba, no al intervalo percentil. Leer la sección 4 completa para confirmar el alcance antes de cambiar el protocolo.

---
Leído el 11 de noviembre de 2026 con asistencia computacional. «NV» marca lo que no se vio en el texto literal del documento y debe comprobarse en el PDF antes de citarlo.
