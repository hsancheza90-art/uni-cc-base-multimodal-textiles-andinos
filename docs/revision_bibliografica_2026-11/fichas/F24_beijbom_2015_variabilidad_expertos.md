# F24 · Beijbom (2015)

**Towards Automated Annotation of Benthic Survey Images: Variability of Human Experts and Operational Modes of Automation**

| Campo | Valor |
|---|---|
| Autores | Beijbom, O.; Edmunds, P. J.; Roelfsema, C.; Smith, J.; Kline, D. I.; Neal, B. P.; Dunlap, M. J.; Moriarty, V.; Fan, T.-Y.; Tan, C.-J.; Chan, S.; Treibitz, T.; Gamst, A.; Mitchell, B. G.; Kriegman, D. (15 autores, p. 1) |
| Año y sede | 2015. PLoS ONE 10(7), e0130312 (publicado el 8 de julio de 2015; CC0) |
| Identificador | doi:10.1371/journal.pone.0130312 |
| PDF | `pdfs/F24_beijbom_2015_variabilidad_expertos.pdf` · https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0130312&type=printable |
| Eje | H. Fiabilidad de la anotación |
| Origen del registro | OpenAlex (I1) |
| Nivel de lectura | completo (texto extraído del PDF, 22 páginas; revisado el 20-11-2026). Las figuras y el material suplementario (S1 Appendix, S1 Table) no están en el texto |

## Qué hace

- **Datos.** Fotocuadrantes de cuatro arrecifes del Pacífico (Moorea, islas de la Línea, Nanwan Bay y Heron Reef). El resumen habla de 17 categorías dominantes (p. 1); el conjunto de etiquetas de consenso de la tabla 2 tiene 20 (p. 6). En cada sitio, 200 imágenes de evaluación con 10 puntos por imagen, anotadas por seis expertos: 48 000 anotaciones de punto (pp. 3, 6).
- **Tarea y protocolo.** Cuánto varían los expertos entre sí y consigo mismos, y cómo equilibrar exactitud y eficiencia al automatizar (p. 3).
- **Método.** Solo los cuatro expertos locales («Hosts») reanotan los mismos puntos de las mismas imágenes que habían anotado entre uno y seis años antes, sin ver sus anotaciones previas («Archived»); eso mide el acuerdo intra-anotador. Los otros cinco expertos de cada sitio («Visitors») miden el acuerdo entre anotadores (pp. 3, 6). La medida es kappa de Cohen frente a las anotaciones archivadas, global y binaria por grupo (p. 8). Clasificador: codificación de Fisher y SVM lineal (p. 7).
- **Comparadores.** Dos modos de operación (pp. 8–9, 12): ALLEVIATE, semiautomático, en el que el clasificador anota el punto solo si su puntuación máxima supera un umbral y, si no, la decisión queda en manos del experto, que la toma por su cuenta (en el experimento se toma la anotación del Host); y ABUNDANCE, totalmente automático, que corrige las coberturas con la matriz de confusión. Un tercer modo, REFINE, propone cinco etiquetas sugeridas por punto (p. 10), pero solo se describe en el S1 Appendix, que no está en el texto: NV.
- **Resultados.** Kappa de los Hosts (intra-anotador, media ± EE, n = 4 sitios, p. 10): coral 89,7 ± 1,2 %, macroalgas 71,0 ± 4,0 %, algas coralinas costrosas (CCA) 51,0 ± 9,3 %, algas de césped 61,6 ± 6,1 % (la discusión de la p. 15 escribe 61,1 %); géneros de coral comunes 79,4 ± 4,2 %. Visitors (entre anotadores, n = 20, p. 10): 84,0; 58,7; 35,5 y 43,3 %; géneros 58,6 %. Clasificador solo: 63,5; 48,5; 28,3 y 43,8 % (p. 11). Con ALLEVIATE al 50 % de decisiones automáticas, el error de cobertura es comparable al de los Hosts (pp. 12–13, 17). La discusión recuerda que kappa no tiene una escala absoluta y cita las escalas de Landis y Koch y de Fleiss (p. 15).
- **Limitaciones declaradas.** Definiciones de algas difíciles de aplicar en fotos planas (p. 15); la referencia archivada puede estar equivocada (Pocillopora, p. 17); el posible aumento de exactitud humana con ALLEVIATE requiere un estudio de usuarios (p. 17); ABUNDANCE solo es insesgado si se conoce la matriz de confusión de los datos muestreados (p. 18).
- **Código y datos.** Imágenes y datos en Dryad (doi:10.5061/dryad.m5pr3); modos implementados en CoralNet (pp. 1, 3, 10).

## Aporte a la tesis

Es el análogo más cercano encontrado de la reanotación del lote 1: especialistas que vuelven a anotar a ciegas las mismas imágenes, uno a seis años después, y cuya estabilidad cambia mucho de una categoría a otra (de 51 % a 90 % de kappa). Apoya informar el acuerdo por atributo y no un número global, y usar la variabilidad humana como referencia: los autores la presentan como línea base para valorar la anotación automática y advierten que, donde el acuerdo humano es bajo, cabe esperar una exactitud automática igual de baja (pp. 3, 15). No respalda, en cambio, el sentido en que la tesis llama «modo semiautomático» a su revisión asistida (ver la actualización).

## Cautela al citar

Dominio ecológico. Su «semiautomático» no es una persona que confirma o corrige propuestas: la máquina decide sola los puntos de alta confianza y deja al experto, sin propuesta, los inciertos.

## Actualización del 20 de noviembre de 2026

- Se leyó el texto completo (22 páginas). Se completó la lista de 15 autores y se corrigió el método: solo los cuatro Hosts reanotan sus propias imágenes; los Visitors miden el acuerdo entre anotadores.
- Las cifras marcadas NV se confirmaron (p. 10): kappa intra-anotador de 89,7 % en coral, 51,0 % en CCA y 61,6 % en algas de césped (61,1 % en la p. 15, errata del artículo), más 71,0 % en macroalgas.
- **Contradicción con el uso en la tesis.** El modo semiautomático ALLEVIATE (pp. 8–9, 12) asigna sin revisión humana los puntos en que el clasificador confía y deja los demás al experto, que anota sin propuesta. La revisión de la tesis es lo contrario: el anotador verifica y firma todas las propuestas del modelo. Puede citarse para «modo semiautomático» solo aclarando la diferencia; el modo más parecido, REFINE (etiquetas sugeridas que el humano elige), está solo en el S1 Appendix y sigue NV.
- Siguen NV el S1 Appendix (REFINE, efecto del tamaño de entrenamiento) y la S1 Table por sitio.

---
Leído el 11 de noviembre de 2026 y completado el 20 de noviembre de 2026 con asistencia computacional, sobre el texto completo extraído del PDF. «NV» marca lo que no se pudo comprobar.
