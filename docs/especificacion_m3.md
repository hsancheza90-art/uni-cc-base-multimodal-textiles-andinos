# Especificación de M3: descriptor estructural y disimilitud mixta

| | |
|---|---|
| Versión | 0.1, 6 de noviembre de 2026 (actividad S2.5 del plan de cierre) |
| Implementación | `src/modelos/m3_estructura.py`; pruebas de propiedades en `tests/test_sistemas.py` |
| Parámetros | `config/modelos.toml`, sección `[m3.pesos]` |
| Referencias | Protocolo experimental v2, sección 4; auditoría del asesor, informe 05 («Descriptor mínimo implementable») |

M3 compara dos piezas a partir de su organización visible, tal como la registra la anotación estructural v2. Es un sistema **asistido por anotación**: dispone de información humana a la que M2 no tiene acceso. Por eso, la comparación entre ambos mide la utilidad de cada sistema para la recuperación y no la superioridad de un método de extracción automática. M3 no interpreta el significado de los motivos ni atribuye una cultura de origen.

## 1. Bloques del descriptor

El descriptor de una pieza *i* asigna un valor a cada bloque *b*, salvo que el bloque no se haya podido observar. En ese caso, la máscara *m_ib* vale 0. Los estados *no observable* y *desconocido*, y *no visible* en el borde y en el centro, desactivan el bloque. El estado *ausente*, en cambio, es una observación: indica que el rasgo es visible y no está presente, y se compara como cualquier otro valor.

| Bloque *b* | Atributo de la anotación | Distancia *d_b*, en [0, 1] |
|---|---|---|
| Composición | `composicion` | 0 si los valores coinciden; 1 en caso contrario |
| Bandas | `secuencia_bandas` (la palabra *w*) | Distancia de edición normalizada en la órbita de la reversión (sección 2) |
| Adyacencias | Pares de bandas contiguas de *w* | Mitad de la distancia L1 entre histogramas (sección 2) |
| Borde y centro | `borde`, `centro` | 0 si coinciden; 1 en caso contrario |
| Simetría | `simetria` | 0 si coinciden; 1 en caso contrario |
| Repetición | `repeticion`, ordenada como no < parcial < sí | Diferencia de rangos dividida por 2 |
| Motivos | `motivos`, como conjunto | 1 menos el índice de Jaccard; dos conjuntos vacíos (motivos ausentes) están a distancia 0 |
| Familia iconográfica | `familia_iconografica` | 0 si coinciden; 1 en caso contrario |

Tres elementos quedan fuera del descriptor de forma deliberada:
- **El color.** Así, una eventual ganancia de M3 no puede deberse al color, que ya está representado en M1 y M2.
- **El motivo principal.** Es la categoría más incierta de la primera anotación (36 de las 150 piezas la registran como *desconocida*) y se solapa con los motivos y la familia iconográfica. Podría incorporarse solo con datos de desarrollo y antes de congelar los sistemas.
- **Las correcciones de metadatos.**

## 2. La palabra de bandas

**Alfabeto y eje.** El alfabeto está formado por los tipos de banda del vocabulario controlado, en este orden: lisa, geométrica, figurativa, mixta y no determinada. La laguna no es un símbolo, sino la marca de un tramo que no puede observarse. El eje de lectura es el de la fotografía (`eje_bandas`). Como el sentido de lectura es una convención, el descriptor trabaja con el grupo C₂ = {identidad, reversión}.

**Forma canónica.** Se define *c(w)* = mín_lex {*w*, rev(*w*)}. Puesto que {*w*, rev(*w*)} = {rev(*w*), rev(rev(*w*))}, se cumple *c*(rev(*w*)) = *c*(*w*); es decir, leer la pieza en el sentido opuesto no cambia su forma canónica. El cálculo tiene un costo O(*l*) en la longitud de la palabra.

**Distancia entre palabras.** La distancia es *d*(*w*, *v*) = mín{lev(*w*, *v*), lev(*w*, rev *v*)} / máx(\|*w*\|, \|*v*\|), donde lev es la distancia de Levenshtein y las lagunas se eliminan antes de comparar. Como la reversión preserva la distancia de Levenshtein, se cumple *d*(*w*, *v*) = *d*(rev *w*, *v*) = *d*(*w*, rev *v*). Dos piezas sin bandas (dos palabras vacías) están a distancia 0, y una palabra vacía frente a una no vacía está a distancia 1. El costo es O(*l* · *l*′).

**Adyacencias.** Se construye el histograma normalizado de los pares **no dirigidos** de bandas contiguas dentro de cada tramo observado. Una laguna interrumpe el tramo y no forma pares. Al no considerar la dirección, el histograma es invariante a la reversión sin necesidad de elegir un sentido de lectura. Si alguna de las dos piezas no tiene ningún par (porque tiene una sola banda o ninguna), el bloque se considera no observable para ese par de piezas.

**Periodo, solo informativo.** El periodo es *p*(*w*) = mín{*p* ∈ 1..*l* : *w_j* = *w_(j+p)* para todo *j* ≤ *l* − *p*}. Un periodo igual a la longitud de la palabra no indica repetición. El periodo se calcula, pero no interviene en la disimilitud.

Dos ejemplos ilustran estas definiciones:
- Las palabras `aabb` y `abab` tienen el mismo histograma de tipos y distintas adyacencias. Por eso es indispensable un control sin orden para atribuir una ganancia al orden de las bandas.
- Con cuatro posiciones, dos símbolos y el grupo C₂ hay 2⁴ palabras, de las cuales la reversión deja fijas 2². Por el lema de Burnside, el número de formas canónicas es (16 + 4) / 2 = 10. El ejemplo forma parte de las pruebas unitarias; no es un resultado experimental.

## 3. Disimilitud mixta

La disimilitud entre dos piezas es

D(*i*, *j*) = Σ_b λ_b *m_ib* *m_jb* *d_b*(*i*, *j*) / Σ_b λ_b *m_ib* *m_jb*,

con pesos λ_b ≥ 0 definidos en `[m3.pesos]`.

**Ausencia de evidencia.** Si el denominador es 0, ningún bloque es observable en ambas piezas y la disimilitud no está definida. El par queda «sin evidencia estructural»: no recibe la similitud máxima y, en el ranking de M3, esos candidatos se ubican al final, ordenados por identificador.

**Cobertura.** Se define como Σ_b λ_b *m_ib* *m_jb* / Σ_b λ_b. Se informa junto con D, y la regla de reparto de pesos de M4 la utiliza.

**Similitud para el ranking.** *s* = 1 − D.

**Propiedades.**
- D(*i*, *i*) = 0, D es simétrica y toma valores en [0, 1].
- Con máscaras variables, D es una **disimilitud**, no una métrica: no se garantiza la desigualdad triangular ni que defina un núcleo semidefinido positivo, y ningún paso del método depende de esas propiedades.

**Contribuciones.** La contribución de cada bloque es *c_b* = λ_b *d_b* / Σ λ m m. Su suma reconstruye D de forma exacta, que es la primera comprobación de H3 en el protocolo. Retirar un bloque (λ_b = 0) recalcula D con los bloques restantes renormalizados, que es la segunda comprobación.

## 4. M3-sin-orden, control del mecanismo (H2)

M3-sin-orden coincide con M3 salvo en dos aspectos:
- la palabra de bandas se sustituye por el histograma de sus tipos, sin lagunas, comparado con la mitad de la distancia L1;
- se omite el bloque de adyacencias.

Usa los mismos pesos, sin reajustarlos. Si M3 supera a M3-sin-orden, la diferencia puede atribuirse al orden de las bandas y no a su composición por tipos.

## 5. Ajuste y congelación

Los pesos parten de valores iguales (1,0) y solo se ajustan con las consultas de desarrollo. El descriptor se calcula sobre la anotación congelada después de la re-anotación del primer lote y de las decisiones de criterio (versión 2.1). A partir de ese momento se generan los rankings de M3: primero en desarrollo y después, una sola vez, en prueba.

## 6. Pruebas de propiedades

Las pruebas de `tests/test_sistemas.py` verifican:
- la invariancia de la forma canónica a la reversión;
- el ejemplo de Burnside, con 10 órbitas;
- que `aabb` y `abab` tienen el mismo histograma de tipos y distintas adyacencias;
- la invariancia del histograma de adyacencias a la reversión;
- la simetría y la invariancia a la reversión de la distancia entre palabras, con las lagunas enmascaradas;
- el cálculo exacto del periodo;
- que D es simétrica, nula consigo misma, acotada en [0, 1] y no definida cuando no hay bloques comunes;
- que la suma de las contribuciones reconstruye D y que la intervención sobre un bloque coincide con la fórmula;
- que M3-sin-orden no distingue el orden de las bandas y M3 sí.
