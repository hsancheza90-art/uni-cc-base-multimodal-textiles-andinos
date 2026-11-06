# Especificación de M3: descriptor estructural y disimilitud mixta

| | |
|---|---|
| Versión | 0.1, 6 de noviembre de 2026 (S2.5 del plan de cierre) |
| Implementación | `src/modelos/m3_estructura.py`; pruebas de propiedades en `tests/test_sistemas.py` |
| Parámetros | `config/modelos.toml`, `[m3.pesos]` |
| Referencias | Protocolo experimental v2, sección 4; auditoría del asesor, informe 05 («Descriptor mínimo implementable») |

M3 compara dos piezas por su organización visible, a partir de la anotación estructural v2 (`data/metadata/anotaciones_v2.csv`). Es un sistema **asistido por anotación**: usa información humana que M2 no tiene, así que la comparación con M2 mide la utilidad del sistema y no la superioridad de una extracción automática. No interpreta el significado de los motivos ni atribuye cultura.

## 1. Bloques del descriptor

Cada pieza *i* tiene un valor por bloque, o ninguno si el bloque no se observó (máscara *m_ib* = 0). Los estados `no_observable` y `desconocido`, y `no_visible` en borde y centro, apagan el bloque. `ausente` es una observación: el rasgo se ve y no está.

| Bloque *b* | Atributo de la anotación | Distancia *d_b* en [0, 1] |
|---|---|---|
| Composición | `composicion` | 0 si son iguales, 1 si no |
| Bandas | `secuencia_bandas` (palabra *w*) | Edición normalizada en la órbita de la reversión (sección 2) |
| Adyacencias | pares de bandas contiguas de *w* | Mitad de la distancia L1 entre histogramas (sección 2) |
| Borde, centro | `borde`, `centro` | 0 si son iguales, 1 si no |
| Simetría | `simetria` | 0 si son iguales, 1 si no |
| Repetición | `repeticion` (no < parcial < sí) | \|rango_i − rango_j\| / 2 |
| Motivos | `motivos` (conjunto) | 1 − Jaccard; dos conjuntos vacíos (ausentes) están a 0 |
| Familia iconográfica | `familia_iconografica` | 0 si son iguales, 1 si no |

**Fuera del descriptor:**
- **El color** (capa cromática). Así, una ganancia de M3 no es cromática; el color lo cubren M1 y M2.
- **`motivo_principal`**. Es la categoría más incierta de la primera anotación (36 de 150 piezas en `desconocido`) y se solapa con `motivos` y `familia_iconografica`. Puede incorporarse solo con datos de desarrollo, antes de congelar los sistemas.
- **Las correcciones de metadatos.**

## 2. Palabra de bandas

- **Alfabeto:** los tipos de banda de `config/vocabulario.toml`: `lisa`, `geometrica`, `figurativa`, `mixta` y `no_determinada`, en ese orden. `laguna` no es un símbolo, sino un tramo no observado.
- **Eje:** el de la fotografía (`eje_bandas`). El sentido de lectura es una convención, de modo que se trabaja con el grupo C₂ = {identidad, reversión}.
- **Forma canónica:** *c(w)* = mín_lex {*w*, rev(*w*)}. Como {*w*, rev(*w*)} = {rev(*w*), rev(rev(*w*))}, se cumple *c*(rev(*w*)) = *c*(*w*). El costo es O(*l*).
- **Distancia de palabras:** *d*(*w*, *v*) = mín{lev(*w*, *v*), lev(*w*, rev *v*)} / máx(\|*w*\|, \|*v*\|), con lev la distancia de Levenshtein y las lagunas quitadas antes de comparar. La reversión preserva lev, así que *d*(*w*, *v*) = *d*(rev *w*, *v*) = *d*(*w*, rev *v*). Dos palabras vacías (piezas sin bandas) están a 0, y una vacía frente a una no vacía, a 1. El costo es O(*l*·*l*′).
- **Adyacencias:** el histograma normalizado de pares **no dirigidos** de bandas contiguas dentro de cada tramo observado. Una laguna corta el tramo y no forma par. Al no ser dirigidos, el histograma es invariante a la reversión sin elegir sentido. Si alguna de las dos piezas no tiene ningún par (una sola banda o ninguna), el bloque no es observable para ese par de piezas.
- **Periodo (informativo):** *p*(*w*) = mín{*p* ∈ 1..*l* : *w_j* = *w_(j+p)* para todo *j* ≤ *l* − *p*}. *p* = *l* no se llama repetición. No entra en *D*.

**Ejemplo de por qué hace falta el control sin orden:** `aabb` y `abab` tienen el mismo histograma de tipos y distintas adyacencias.

**Ejemplo verificable (Burnside):** con cuatro posiciones, dos símbolos y C₂ hay 2⁴ palabras, y la reversión fija 2²; el número de formas canónicas es (16 + 4) / 2 = 10. Es una prueba unitaria y no un resultado experimental.

## 3. Disimilitud mixta

D(*i*, *j*) = Σ_b λ_b *m_ib* *m_jb* *d_b*(*i*, *j*) / Σ_b λ_b *m_ib* *m_jb*, con λ_b ≥ 0 los pesos de `[m3.pesos]`.

- **Sin evidencia estructural:** si el denominador es 0, D no existe y el par no recibe similitud máxima. En el ranking de M3 esos candidatos van al final, por `id_global`.
- **Cobertura:** Σ_b λ_b *m_ib* *m_jb* / Σ_b λ_b. Se informa junto a D y la usa la regla de reparto de pesos de M4.
- **Similitud para el ranking:** *s* = 1 − D.
- **Propiedades:**
  - D(*i*, *i*) = 0.
  - D es simétrica y está en [0, 1].
  - Con máscaras variables, D es una **disimilitud**: no se garantiza la desigualdad triangular ni que defina un núcleo semidefinido positivo, y no se usa nada que lo requiera.
- **Contribuciones:** *c_b* = λ_b *d_b* / Σ λ m m. Su suma reconstruye D de forma exacta, que es la comprobación 1 de H3 en el protocolo. Retirar un bloque (λ_b = 0) recalcula D con los demás renormalizados, que es la comprobación 2.

## 4. M3-sin-orden (control del mecanismo, H2)

Es igual que M3, con dos diferencias:
- La palabra de bandas se reemplaza por el **histograma de sus tipos**, sin las lagunas, con *d* igual a la mitad de la distancia L1.
- El bloque de adyacencias no existe.

Usa los mismos pesos, sin reajustar. Si M3 supera a M3-sin-orden, la diferencia se debe al orden de las bandas y no a su composición por tipos.

## 5. Ajuste y congelación

Los pesos parten iguales (1,0) y solo se ajustan con las consultas de desarrollo. El descriptor se calcula sobre la anotación congelada después de la re-anotación del lote 1 y de las decisiones de criterio (v2.1). Los rankings de M3 se generan desde entonces, primero en desarrollo y después, una sola vez, en prueba.

## 6. Pruebas de propiedades (`tests/test_sistemas.py`)

- Invariancia de la forma canónica a la reversión.
- Ejemplo de Burnside: 10 órbitas.
- `aabb` frente a `abab`: mismo histograma de tipos, adyacencias distintas.
- Adyacencias invariantes a la reversión.
- Distancia de palabras simétrica e invariante a la reversión, con las lagunas enmascaradas.
- Periodo exacto.
- D simétrica, nula consigo misma, en [0, 1] y sin evidencia cuando no hay bloques comunes.
- La suma de contribuciones reconstruye D, y la intervención sobre un bloque coincide con la fórmula.
- M3-sin-orden no distingue el orden de las bandas y M3 sí.
