# F12 · Dorozynski (2022)

**Deep Descriptor Learning with Auxiliary Classification Loss for Retrieving Images of Silk Fabrics in the Context of Preserving European Silk Heritage**

| Campo | Valor |
|---|---|
| Autores | Dorozynski, M.; Rottensteiner, F. |
| Año y sede | 2022. ISPRS International Journal of Geo-Information 11, 82 (p. 1; el número 2 no figura en el texto). Recibido el 01-12-2021, aceptado el 15-01-2022, publicado el 21-01-2022; CC BY (p. 1) |
| Identificador | doi:10.3390/ijgi11020082 |
| PDF | `pdfs/F12_dorozynski_2022_descriptores_seda.pdf` · https://www.mdpi.com/2220-9964/11/2/82/pdf |
| Eje | B. Representación y recuperación de textiles |
| Origen del registro | OpenAlex (B1) |
| Nivel de lectura | completo (texto extraído del PDF, 29 páginas; revisado el 20-11-2026). Solo salieron como códigos «/gid000..» las dos primeras líneas de la p. 1 (el distintivo gráfico de la editorial); el resto del texto y las tablas 1–6 son legibles. Las ecuaciones salieron partidas en líneas pero se reconstruyen; las imágenes de las figuras no se pueden ver |

## Qué hace

- **Datos.** 48 830 imágenes de tejidos planos de seda exportadas del grafo SILKNOW, cada una con al menos una de cuatro variables: material (3 clases), lugar (17), época (6) y técnica (6); solo etiquetas con 150 o más apariciones (pp. 14–15, tabla 1). Cobertura de anotación entre 32,2 % (técnica) y 72,4 % (material); 6 143 imágenes tienen las cuatro (p. 15). Partición aleatoria 60/20/20 (p. 14). Para transferencia, 80 880 imágenes de WikiArt (pp. 16–17).
- **Tarea y protocolo.** Recuperación imagen a imagen; la evaluación se hace por clasificación kNN (k = 10, voto mayoritario de los recuperados del conjunto de entrenamiento) de las variables anotadas, con exactitud global y F1 medio por variable; cada experimento se repite cinco veces (pp. 18–19).
- **Método.** ResNet152 preentrenada (sin ajuste fino: no mejoraba, p. 18) y una capa común de 256 nodos. Pérdida de recuperación con tres términos: similitud semántica (tripletas con margen gradual), similitud de color (correlación de histogramas HSV) y autosimilitud (otra imagen del mismo objeto o una transformación), más una pérdida auxiliar de clasificación multitarea con pérdida focal (pp. 7–13). Confirmado: la similitud semántica es la fracción de variables anotadas que coinciden, y las etiquetas ausentes entran como incertidumbre que reduce el margen (ecs. 6–10, pp. 10–11).
- **Comparadores.** **Corrección:** solo un estudio de ablación de nueve combinaciones de pérdidas (tabla 2, p. 19); el trabajo previo de los autores no se compara numéricamente. Los autores declaran que no encontraron ningún estudio con el que compararse de forma justa (p. 19).
- **Resultados.** Confirmado: la variante semántica + clasificación alcanza exactitud 63,9 y F1 42,9 frente a 61,2 y 37,3 sin la pérdida auxiliar (+2,7 y +5,6; tabla 3, p. 21). Mayor ganancia de F1 en técnica (+8,4, p. 22). Color y autosimilitud no ayudan; la autosimilitud empeora (p. 20). WikiArt: exactitud 55,8 y F1 51,1 (tabla 6, p. 23). Confirmado que no hay métrica de ranking: la evaluación evita a propósito una referencia de recuperación óptima (p. 25). En los ejemplos cualitativos, una consulta recupera «tejidos de color vivo con un patrón de franjas» (fig. 5a, p. 24), sin medirlo.
- **Limitaciones declaradas.** No hay sección propia. El texto reconoce problemas persistentes con clases poco representadas (brecha entre exactitud y F1, pp. 21–22) y que la similitud visual percibida no se evalúa, porque exigiría una evaluación manual por expertos que consideran «muy subjetiva» y fuera de alcance (p. 23); el etiquetado manual se descarta por «altamente subjetivo» (p. 2).
- **Código y datos.** Datos: grafo SILKNOW en doi:10.5281/zenodo.5743090 (p. 26 y ref. 71). Código: no figura en el texto.

## Aporte a la tesis

Muestra la alternativa que la tesis evita: derivar la relevancia de los metadatos. Aquí dos sedas son parecidas si comparten lugar o época, no porque alguien las juzgue parecidas. Es el argumento para sostener qrels humanos e independientes (ANN02) y para explicar por qué las fichas de museo no bastan como verdad de referencia estructural. Aporta además la idea de similitud gradual, compatible con la escala 0–3.

## Cautela al citar

Evaluación indirecta por clasificación: no es comparable con nDCG. Su rechazo explícito del juicio humano por subjetivo (pp. 2 y 23) es la postura contraria a la de la tesis y puede citarse como tal.

## Actualización del 20 de noviembre de 2026

- El texto extraído es legible salvo el distintivo gráfico de la p. 1; se verificaron datos, protocolo, método, cifras y limitaciones con página.
- Se completó el tamaño (48 830 imágenes, cuatro variables) y se confirmaron las mejoras de 2,7 y 5,6 puntos (tabla 3).
- Se corrigió «Comparadores»: no hay comparación numérica con el trabajo previo, solo ablación.
- Se añadieron dos datos útiles: los autores descartan el juicio humano por subjetivo (pp. 2 y 23) y un ejemplo cualitativo recupera telas con franjas (p. 24). Sin código publicado; el número 2 del volumen no figura en el texto.

---
Leído el 11 de noviembre de 2026 y completado el 20 de noviembre de 2026 con asistencia computacional, sobre el texto completo extraído del PDF. «NV» marca lo que no se pudo comprobar.
