# Archivo de auditoría de los juicios de desarrollo asistidos

Responde a la observación B8 del dictamen del asesor del 21 de noviembre de 2026 (decisión R39 de `docs/registro_decisiones.md`). Describe el archivo que documenta la revisión de los juicios de desarrollo con la segunda opinión de un modelo (decisión R25) y registra su huella. El archivo es privado: queda bajo custodia del investigador, fuera del repositorio, porque contiene los grados iniciales del evaluador y las respuestas del modelo. Este documento no los reproduce.

## Huella

| Elemento | Valor |
|---|---|
| Ubicación (local, no versionada) | `investigacion_local/auditoria_juicios_asistidos_2026-11-19/` |
| Manifiesto | `SHA256SUMS.txt`, con la suma SHA-256 de cada uno de los 429 archivos del archivo |
| SHA-256 del manifiesto | `c473375f6cc9c3127906704a5e03e587d7db7b6585a1123fe5a794ea1d0099f2` |
| Fecha de armado | 23 de noviembre de 2026, con el material del 19 de noviembre sin modificarlo |

Para verificarlo: calcular la suma SHA-256 de `SHA256SUMS.txt` y compararla con la de este cuadro, y después comprobar cada archivo contra el manifiesto (`sha256sum -c SHA256SUMS.txt`). Cualquier cambio posterior en el archivo se detecta así. El investigador puede entregar el archivo al asesor si este lo solicita.

## Procedimiento documentado

| Aspecto | Contenido |
|---|---|
| Fecha | 19 de noviembre de 2026 |
| Modelo | `claude-opus-5-5` (Claude Opus 5.5, de Anthropic), un modelo de visión y lenguaje de uso general que no es CLIP ni ninguno de los sistemas evaluados |
| Forma | Cinco instancias del modelo, una por cada par de consultas de desarrollo, con las mismas instrucciones salvo los pares asignados y el archivo de salida |
| Entradas autorizadas | Solo una imagen compuesta por par, con la consulta a la izquierda y el candidato a la derecha, y la rúbrica. Las instrucciones prohíben abrir cualquier otro archivo, leer código o tablas y usar la red |
| Sin acceso a | Los grados del evaluador, los rankings, los sistemas que propusieron cada par y la anotación |
| Rúbrica | La escala 0–3 y el estado `no_evaluable` del protocolo (sección 6), con cuatro ejemplos hipotéticos de organización; el color no cuenta. Se pidió una justificación de hasta 15 palabras y una confianza (alta, media o baja) por par |
| Revisión humana | El evaluador vio, par por par, su grado inicial y la opinión del modelo, y firmó un grado final, una justificación, su nombre y la fecha |

## Contenido del archivo

| Archivo | Contenido | Registros |
|---|---|---|
| `00_modelo_y_procedimiento.json` | Modelo, forma, entradas autorizadas, accesos excluidos y conteos | — |
| `01_juicios_antes_de_la_revision.xlsx` | Libro de juicios de desarrollo tal como estaba antes de la revisión | 411 pares |
| `02_clave_de_pares.csv` | Correspondencia entre cada imagen compuesta y su consulta y candidato, con el grado y la justificación iniciales | 411 |
| `entradas_pares/` | Las imágenes compuestas que vio el modelo | 411 |
| `instrucciones/` | Las instrucciones completas de cada una de las cinco instancias | 5 |
| `respuestas_modelo/` | Las respuestas del modelo: par, grado, confianza y justificación | 411 en 5 archivos |
| `03_rastro_antes_opinion_decision.csv` | Por par: grado y justificación iniciales, opinión del modelo y decisión (mantener o cambiar) | 411 |
| `04_revision_firmada_por_el_evaluador.xlsx` | Libro de la revisión con el grado y la justificación finales, el revisor y la fecha | 411 |
| `05_cruce_evaluador_modelo.csv` | Cruce del grado inicial con el del modelo y su diferencia | 411 |
| `06_informe_de_la_comparacion.md` | Acuerdo antes y después de la revisión y matriz de cambios | — |
| `07_uso_de_cada_juicio.csv` | Por par de los 419 juicios vigentes: si se usó para elegir los pesos de M4 o solo para la potencia, y si tuvo asistencia | 419 |
| `SHA256SUMS.txt` | Manifiesto de sumas | 429 líneas |

## Uso de los juicios

- **411 juicios** se revisaron con la segunda opinión y son los que se usaron, el 21 de noviembre, para elegir los pesos de M4 (1/7, 4/7 y 2/7; decisión R28) y para estimar la potencia.
- **8 juicios** corresponden a los pares que la fusión añadió después al pool. El evaluador los juzgó sin asistencia; se usaron para estimar la potencia y no para reajustar los pesos.

## Cifras que el manuscrito declara

Del informe de la comparación (`06_informe_de_la_comparacion.md`): de los 411 grados, el evaluador mantuvo 165 y cambió 246; el acuerdo entre el grado inicial y la opinión del modelo fue de κ = 0,161 (kappa ponderado lineal, 408 pares comparables), el único independiente; después de la revisión subió a 0,925, y la justificación final coincide con la del modelo en 406 de 411 pares. El capítulo 7 (sección 7.6.4) declara con estas cifras el riesgo de anclaje del evaluador en la propuesta del modelo.

## Alcance

La asistencia se limitó a los juicios de desarrollo. Los juicios de relevancia de prueba se emitirán sin asistencia de modelos (decisión R27). El archivo permite reconstruir cómo cambió cada juicio asistido y distinguir el grado del evaluador de la propuesta del modelo; no permite saber cuántos grados finales habría elegido el evaluador sin ver esa propuesta.
