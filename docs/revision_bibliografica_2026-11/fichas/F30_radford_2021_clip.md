# F30 · Radford (2021)

**Learning Transferable Visual Models From Natural Language Supervision**

| Campo | Valor |
|---|---|
| Autores | Radford, A.; Kim, J. W. (contribución igual); Hallacy, C.; Ramesh, A.; Goh, G.; Agarwal, S.; Sastry, G.; Askell, A.; Mishkin, P.; Clark, J.; Krueger, G.; Sutskever, I. (OpenAI) (p. 1) |
| Año y sede | 2021. arXiv v1 del 26-02-2021 (p. 1). La sede ICML 2021 no figura en el texto del preprint; F01 (Yuksekgonul et al., 2023, p. 13) lo cita como ICML 2021, PMLR, pp. 8748–8763 |
| Identificador | arXiv:2103.00020 |
| PDF | `pdfs/F30_radford_2021_clip.pdf` · https://arxiv.org/pdf/2103.00020 |
| Eje | C. Recuperación multimodal en patrimonio |
| Origen del registro | auditoría (S01), ahora leído completo |
| Nivel de lectura | completo (texto extraído del PDF, 48 páginas; revisado el 20-11-2026). Las figuras 2, 4, 6, 9–10, 12–16, 20 y 22 (gráficos) y los ejemplos de la figura 21 salen como números sueltos; se usaron solo las cifras que el texto o los cuadros repiten. De las p. 41–42 (datos de las figuras 20 y 21) solo se revisaron fragmentos y leyendas. Las referencias se recorrieron sin cotejarlas |

## Qué hace

- **Datos.** WIT (WebImageText): 400 millones de pares imagen-texto de internet, buscados con 500 000 consultas y hasta 20 000 pares por consulta (p. 3–4); evaluación en más de 30 conjuntos (p. 1), 27 en la sonda lineal (p. 11, 37).
- **Tarea y protocolo.** Transferencia sin ejemplos: el codificador de texto genera un clasificador a partir de los nombres de clase con indicaciones («A photo of a {label}.») y conjuntos de 80 indicaciones en ImageNet (p. 6–8). También sonda lineal (regresión logística L2) sobre las representaciones (p. 11, 38).
- **Método.** Entrenamiento contrastivo que empareja imágenes y textos dentro de cada lote (N × N pares, pérdida de entropía cruzada simétrica, temperatura aprendida) desde cero (p. 4–5). Codificadores de imagen ResNet y ViT (B/32, B/16, L/14); codificador de texto Transformer de 63M parámetros, 76 tokens como máximo; lote de 32 768; 32 épocas (p. 5, 48). El modelo que el texto llama «CLIP» es ViT-L/14@336px (p. 5).
- **Comparadores.** Visual N-Grams (cuadro 1, p. 7); regresión logística sobre rasgos de ResNet-50 (fig. 5, p. 8); sondas lineales sobre 66 modelos (EfficientNet, BiT, SimCLRv2, MoCo, etc.) (p. 11–12, 37–40); humanos en Oxford-IIIT Pets (p. 16–17).
- **Resultados.** ImageNet sin ejemplos: 76,2 % con el mejor modelo, frente a 11,5 % de Visual N-Grams (cuadro 1, p. 7; confirmado); con ViT-B/32 es 63,2 % (cuadro 11, p. 43). Frente a la sonda lineal sobre ResNet-50 (fig. 5, p. 8; confirmado): EuroSAT −37,1; CLEVRCounts −18,2; DTD (texturas) −16,6; FGVCAircraft −11,3; gana en 16 de 27 conjuntos. Recuperación sin ejemplos en Flickr30k: R@1 texto 88,0 e imagen 68,7 (cuadro 13, p. 46). El solapamiento con los datos de evaluación es bajo (mediana 2,2 %, media 3,2 %) y rara vez cambia la exactitud más de 0,1 puntos (p. 18). Frase de los autores confirmada (p. 19): «CLIP also struggles with more abstract and systematic tasks such as counting the number of objects in an image».
- **Limitaciones declaradas** (sec. 6, p. 18–20, y sec. 7, p. 20–25). Haría falta unas 1000 veces más cómputo para llegar al estado del arte (p. 19); flojo en clasificación fina (coches, flores, aviones), en conteo y en tareas nuevas (p. 19); generaliza mal fuera de distribución (MNIST 88 %, p. 19); limitado a los conceptos del clasificador (p. 19); poca eficiencia de datos (p. 20); se consultaron conjuntos de validación completos y la batería de 27 conjuntos está coadaptada al desarrollo (p. 20); sesgos sociales por datos sin curar (p. 20–23). El solapamiento con la evaluación se analiza en la sec. 5 (p. 17–18) más que como limitación.
- **Código y datos.** github.com/OpenAI/CLIP (p. 1): código y pesos; un enlace al conjunto WIT no figura en el texto.

## Aporte a la tesis

Referencia primaria de M2. Los propios autores muestran que el modelo flaquea en conteo, texturas y categorías finas, que son tres ingredientes de la similitud estructural entre textiles. Junto con F01 y F02 completa el argumento de por qué se espera que la estructura anotada añada algo. El apéndice C (p. 44) es pertinente para S1.7: los autores descartaron el espacio de CLIP como detector de duplicados porque pondera mucho la semejanza semántica y da baja similitud a copias de una misma imagen con texturas de alta frecuencia («fur or stripe patterns») reescaladas de forma distinta.

## Cautela al citar

M2 usa un checkpoint de OpenCLIP multilingüe, no este modelo: citar ambos y no atribuir estas cifras a M2. Las cifras de 76,2 % y de la fig. 5 son del modelo mayor (ViT-L/14@336px), no del ViT-B/32 que usan M2 y la mayoría de los trabajos derivados. La sede ICML 2021 no consta en el preprint.

## Actualización del 20 de noviembre de 2026

- Se leyó el texto completo (48 páginas, con apéndices A–F); se completaron los doce autores.
- NV resueltos: la frase sobre conteo y tareas abstractas (p. 19) y las limitaciones (cómputo, sesgos, fragilidad fuera de distribución, metodología), con sus páginas; el solapamiento se trata en la sec. 5.
- Precisiones: el comparador de la fig. 5 es una regresión logística sobre ResNet-50; las cifras corresponden a ViT-L/14@336px (ViT-B/32: 63,2 % en ImageNet). Se añadió el hallazgo del apéndice C sobre duplicados y texturas.
- Sigue sin verificar: la sede ICML 2021 (solo por cita de F01) y los valores que solo aparecen en gráficos.

---
Leído el 11 de noviembre de 2026 y completado el 20 de noviembre de 2026 con asistencia computacional, sobre el texto completo extraído del PDF. «NV» marca lo que no se pudo comprobar.
