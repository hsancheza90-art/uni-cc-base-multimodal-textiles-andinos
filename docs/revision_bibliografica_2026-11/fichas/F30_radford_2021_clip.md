# F30 · Radford (2021)

**Learning Transferable Visual Models From Natural Language Supervision**

| Campo | Valor |
|---|---|
| Autores | Radford, A.; Kim, J. W.; Hallacy, C.; et al. |
| Año y sede | 2021. arXiv v1; ICML 2021 según la auditoría (no visto en el texto leído) |
| Identificador | arXiv:2103.00020 |
| PDF | `pdfs/F30_radford_2021_clip.pdf` · https://arxiv.org/pdf/2103.00020 |
| Eje | C. Recuperación multimodal en patrimonio |
| Origen del registro | auditoría (S01), ahora leído en parte |
| Nivel de lectura | parcial: primeros ~40 000 caracteres literales; el resto, resumen automático |

## Qué hace

- **Datos.** 400 millones de pares imagen-texto de internet; evaluación en más de 30 conjuntos.
- **Tarea y protocolo.** Transferencia sin ejemplos mediante indicaciones de texto con el nombre de la clase.
- **Método.** Entrenamiento contrastivo que empareja imágenes y textos dentro de cada lote.
- **Comparadores.** Visual N-Grams y una sonda lineal sobre ResNet-50.
- **Resultados.** ImageNet sin ejemplos: 76,2 (tabla 1). La transferencia sin ejemplos queda por debajo de la sonda lineal en conjuntos especializados (figura 5): EuroSAT −37,1; conteo en CLEVR −18,2; texturas DTD −16,6; aviones −11,3. La frase de los autores sobre la debilidad en tareas abstractas y sistemáticas como contar: NV.
- **Limitaciones declaradas.** NV: costo de cómputo, sesgos sociales, fragilidad fuera de distribución y solapamiento con datos de evaluación.
- **Código y datos.** github.com/OpenAI/CLIP

## Aporte a la tesis

Referencia primaria de M2. Los propios autores muestran que el modelo flaquea en conteo, texturas y categorías finas, que son tres ingredientes de la similitud estructural entre textiles. Junto con F01 y F02 completa el argumento de por qué se espera que la estructura anotada añada algo.

## Cautela al citar

M2 usa un checkpoint de OpenCLIP multilingüe, no este modelo: citar ambos y no atribuir estas cifras a M2.

---
Leído el 11 de noviembre de 2026 con asistencia computacional. «NV» marca lo que no se vio en el texto literal del documento y debe comprobarse en el PDF antes de citarlo.
