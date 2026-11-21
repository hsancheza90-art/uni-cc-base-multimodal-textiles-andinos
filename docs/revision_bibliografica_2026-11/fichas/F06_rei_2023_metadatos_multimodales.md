# F06 · Rei (2023)

**Multimodal Metadata Assignment for Cultural Heritage Artifacts**

| Campo | Valor |
|---|---|
| Autores | Rei, L.; Mladenić, D.; Dorozynski, M.; Rottensteiner, F.; Schleider, T.; Troncy, R.; Sebastián Lozano, J.; Gaitán Salvatella, M. (p. 1) |
| Año y sede | 2023. Multimedia Systems 29, 847–869 (confirmado en p. 2); se leyó la «versión mejorada» de arXiv (1 de junio de 2024), que según el autor no se publicó en la revista y añade la comparación de estrategias contra el desbalance (secciones 4.5, 5 y 8) y las matrices de confusión (sección 6) (p. 2) |
| Identificador | doi:10.1007/s00530-022-01025-2; arXiv:2406.00423 |
| PDF | `pdfs/F06_rei_2023_metadatos_multimodales.pdf` · https://arxiv.org/pdf/2406.00423 |
| Eje | B. Representación y recuperación de textiles |
| Origen del registro | auditoría (S04/S05), releído |
| Nivel de lectura | completo (texto extraído del PDF, 34 páginas; revisado el 20-11-2026) |

## Qué hace

- **Datos.** Registros de tejidos de seda europeos (siglos XV a XX) del grafo de conocimiento SILKNOW; la exportación tiene 38 873 objetos y 74 527 imágenes (p. 8). El conjunto final tiene 28 077 registros: 96,6 % con imagen, 39,3 % con texto, 38,0 % con ambos (p. 11, tabla 5, p. 13), de 12 museos (tabla 4, p. 12; el MET aporta 6 524 y el AIC 8). Textos en inglés, castellano, francés y catalán (tabla 7, p. 13). Nota: la p. 8 habla de 16 fuentes y la p. 5 y la tabla 4 de 12 colecciones.
- **Tarea y protocolo.** Asignar propiedades (material, técnica, lugar por país, época por siglo) como clasificación multitarea; clases agrupadas por expertos y descartadas las de frecuencia menor que 150 (pp. 10–11). Partición aleatoria por registro 60/20/20 (p. 11). Métricas: F1 macro y exactitud global (p. 18).
- **Método.** Fusión tardía a nivel de decisión de tres clasificadores: imagen (ResNet-152 multitarea, p. 13), texto (XLM-R base multitarea, p. 20) y tabular (XGBoost, p. 15); pérdida focal en imagen y texto para el desbalance. El clasificador de fusión (XGBoost, uno por tarea) recibe las etiquetas predichas por cada modalidad y se entrena sobre el conjunto de validación con validación cruzada de cinco pliegues (pp. 17 y 22).
- **Comparadores.** Modelos de una sola modalidad; pérdida softmax, reponderación de pesos y muestreo uniforme frente a pérdida focal (tablas 10 y 13, pp. 19 y 21); ablación de pares de modalidades (tabla 21, p. 23).
- **Resultados.** Confirmado: F1 macro multimodal 74,2 frente a 55,6 de la mejor modalidad sola (tabular) en el conjunto de prueba completo, contando como error el registro al que le falta la modalidad (tabla 20, p. 23). Exactitud multimodal 82,6 (tabla 19). Sobre los registros con texto, el clasificador de texto alcanza F1 86,1 (tabla 14, p. 21). Cualquier par de modalidades supera a cada una sola; texto + tabular 71,6 (tabla 21). El museo es el atributo más informativo del clasificador tabular en las cuatro tareas (tabla 17, p. 22).
- **Limitaciones declaradas.** Confirmadas: desbalance de clases, ruido en etiquetas de material y técnica (9 de 20 errores revisados en material eran etiquetas incorrectas, p. 25), texto disponible en el 39,3 % de los registros (tabla 5, p. 13); textos engañosos (tabla 22, p. 25); pocos datos de entrenamiento (p. 29).
- **Código y datos.** Confirmado: datos en zenodo.org/record/6590957, grafo en zenodo.org/record/5743090, código en github.com/silknow/multimodal_cultural_heritage (p. 31).

## Aporte a la tesis

Precedente textil de fusión tardía de imagen, texto y atributos, que es la arquitectura de M4. La diferencia es de objetivo: clasifican metadatos con decenas de miles de registros; la tesis recupera por estructura con 150 piezas. También ilustra un problema compartido: el texto falta en buena parte de las fichas, lo que afecta a M0.

## Cautela al citar

La ganancia 74,2 frente a 55,6 depende de contar como error la modalidad ausente; sobre registros con texto, el texto solo (86,1) supera a la fusión (p. 23). Citar el número de la revista, pero las tablas de estrategias de desbalance y las matrices de confusión solo están en la versión de arXiv (p. 2).

## Actualización del 20 de noviembre de 2026

- Se resolvieron todos los «NV»: partición 60/20/20, cifras 74,2 frente a 55,6, limitaciones y repositorios quedaron confirmados con página.
- Se precisó la condición de la comparación de la tabla 20 (modalidad ausente cuenta como error) y se añadió que el texto solo supera a la fusión sobre los registros con texto.
- Se completaron los ocho autores y se aclaró que la versión leída de arXiv difiere de la publicada en Multimedia Systems.
- Queda sin resolver la discrepancia interna entre 16 fuentes (p. 8) y 12 museos (p. 5, tabla 4).

---
Leído el 11 de noviembre de 2026 y completado el 20 de noviembre de 2026 con asistencia computacional, sobre el texto completo extraído del PDF. «NV» marca lo que no se pudo comprobar.
