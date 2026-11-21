# F38 · Landis y Koch (1977)

**The Measurement of Observer Agreement for Categorical Data**

| Campo | Valor |
|---|---|
| Autores | Landis, J. R. (University of Michigan); Koch, G. G. (University of North Carolina) |
| Año y sede | 1977. Biometrics, 33(1), 159-174 (marzo de 1977). International Biometric Society. Recibido en abril de 1975, revisado en noviembre de 1975 (p. 174) |
| Identificador | JSTOR: https://www.jstor.org/stable/2529310 (portada del PDF). El DOI no figura en el texto |
| PDF | `pdfs/landis_1977_kappa.pdf` |
| Eje | Fiabilidad de la anotación |
| Origen del registro | aportado por el investigador (20-11-2026) |
| Nivel de lectura | completo (texto extraído del PDF, 17 páginas: portada de JSTOR y pp. 159-174 de la revista). Las matrices de las ecuaciones (4.2)-(4.5) y algunos pesos del cuadro 8 no son legibles en el texto extraído |

En esta ficha, las páginas citadas son las de la revista. La p. 165 corresponde a la p. 8 del PDF.

## Qué hace

- **Datos.** Ejemplo clínico de Westlund y Kurland (1953): dos neurólogos (Winnipeg y Nueva Orleans) clasifican pacientes de esclerosis múltiple en cuatro categorías ordenadas (cierta, probable, posible, dudosa); 149 pacientes de Winnipeg y 69 de Nueva Orleans. Solo coinciden en el 43 % y el 48 % (pp. 160-161, cuadro 1).
- **Tarea y protocolo.** Metodología general para datos categóricos de estudios de fiabilidad de observadores: sesgo entre observadores (homogeneidad marginal) y acuerdo sujeto a sujeto (pp. 159-162).
- **Método.** Medidas de acuerdo del tipo kappa = (π0 − πe)/(1 − πe), generalizadas con conjuntos de pesos (ec. 3.2-3.8, pp. 163-164); pruebas con el enfoque de mínimos cuadrados ponderados GSK (p. 165). Kappas jerárquicos que van sumando categorías vecinas (cuadros 2-3, pp. 166-167) y kappa ponderado con crédito parcial (cuadro 8 y p. 172). Señalan que kappa es análogo al coeficiente de correlación intraclase y sirve como medida de fiabilidad de determinaciones repetidas sobre los mismos sujetos (p. 163).
- **Comparadores.** No compara métodos; ilustra la metodología.
- **Resultados.** Kappa de acuerdo perfecto: 0,208 (Winnipeg) y 0,297 (Nueva Orleans); con los pesos más permisivos, 0,596 y 0,789 (ec. 4.6, p. 167). Kappa ponderado con crédito parcial: 0,315 y 0,407 (ec. 5.1, p. 172). Hay sesgo significativo entre los neurólogos en el uso de la escala (p. 166). Solo con el criterio más relajado el acuerdo llega a «moderado» o «sustancial» (p. 171).
- **Limitaciones declaradas.** Las pruebas de significación se usan de forma descriptiva y se ignoran las comparaciones múltiples (p. 165). El método se ilustra con dos observadores; con muchos observadores o categorías, las tablas crecen demasiado y hacen falta procedimientos especiales (p. 172).
- **Código y datos.** Programa GENCAT (Landis et al., 1976), citado como informe técnico (pp. 172 y 174). Datos tomados de Westlund y Kurland (1953).

## Aporte a la tesis

- **Escala exacta (p. 165).** «Para mantener una nomenclatura coherente» al describir la fuerza del acuerdo (p. 164), los autores asignan estas etiquetas:

  | Kappa | Fuerza del acuerdo |
  |---|---|
  | < 0,00 | Pobre (*Poor*) |
  | 0,00-0,20 | Leve (*Slight*) |
  | 0,21-0,40 | Aceptable (*Fair*) |
  | 0,41-0,60 | Moderado (*Moderate*) |
  | 0,61-0,80 | Sustancial (*Substantial*) |
  | 0,81-1,00 | Casi perfecto (*Almost Perfect*) |

  **Respalda** los tramos que usa la tesis (0,41-0,60 moderado; 0,61-0,80 sustancial; > 0,80 casi perfecto). Los límites exactos son 0,61 y 0,81.
- **¿Arbitraria o «benchmark»?** **Ambas cosas.** Los autores dicen que las divisiones son «claramente arbitrarias», aunque ofrecen «benchmarks» útiles para discutir el ejemplo del cuadro 1 (p. 165). La escala se propone como nomenclatura para su ejemplo, no como criterio validado. La tesis debe presentarla así.
- **Umbral 0,6 como señal de revisión.** **No lo respalda el texto**: el artículo no fija ningún umbral de aceptación ni de revisión. Además, 0,60 es el extremo superior de «moderado» y «sustancial» empieza en 0,61. Si la tesis usa 0,6, conviene presentarlo como decisión propia («por debajo de 0,61, es decir, sin llegar a sustancial»), no como un umbral de Landis y Koch.
- **Kappa ponderado y acuerdo intra-anotador.** El artículo trata el kappa ponderado con crédito parcial (p. 172; remite a Cohen, 1968). Lo presenta como análogo a la correlación intraclase para determinaciones repetidas (p. 163). El ejemplo, sin embargo, es de acuerdo **entre** dos observadores, no intra-observador. Que la escala sirva para el acuerdo intra-anotador de la tesis es una extensión de uso que el texto no discute. Las cifras del ejemplo muestran además que un kappa sin ponderar y uno ponderado pueden caer en tramos distintos (0,208 frente a 0,315; p. 172).

## Citas útiles

- Las etiquetas de fuerza del acuerdo (pobre, leve, aceptable, moderado, sustancial, casi perfecto) se asignan para mantener una nomenclatura coherente (pp. 164-165).
- Las divisiones son claramente arbitrarias, pero sirven como puntos de referencia («benchmarks») para la discusión (p. 165).
- Kappa mide cuánto excede la probabilidad observada de acuerdo a la esperada bajo una línea base; va de −πe/(1 − πe) a +1 (p. 163).
- Kappa es análogo al coeficiente de correlación intraclase y puede usarse como medida de fiabilidad de determinaciones múltiples sobre los mismos sujetos (p. 163).
- Si se da crédito parcial a ciertos desacuerdos, la proporción ponderada de acuerdo incluye celdas fuera de la diagonal (p. 162).
- Los observadores pueden mostrar sesgo en el uso global de la escala (homogeneidad marginal) además de desacuerdo caso a caso (pp. 166 y 171).

## Cautela al citar

Citar la escala con la advertencia de los propios autores: «claramente arbitraria» (p. 165). No atribuirle un umbral de aceptación de 0,6 ni de ningún otro valor. Los tramos son cerrados y en dos decimales (0,41-0,60; 0,61-0,80; 0,81-1,00); un kappa de 0,605 queda entre tramos y conviene decir cómo se redondea. El artículo trata el acuerdo entre observadores; su uso intra-anotador es una extensión de la tesis.

---
Leído el 20 de noviembre de 2026 con asistencia computacional, sobre el texto completo extraído del PDF.
