# Especificación de M3: descriptor estructural y disimilitud mixta

| | |
|---|---|
| Versión | 0.2, 21 de noviembre de 2026. La 0.1 es del 6 de noviembre (actividad S2.5 del plan de cierre); la sección 5 y la regla de reparto de la sección 3 se añadieron el 12 de noviembre (R11); la 0.2 retira el periodo, precisa el papel de la forma canónica y fija los pesos (R30) |
| Implementación | `src/modelos/m3_estructura.py`; pruebas de propiedades en `tests/test_sistemas.py` |
| Parámetros | `config/modelos.toml`, sección `[m3.pesos]` |
| Referencias | Protocolo experimental v2, sección 4; auditoría del asesor, informe 05 («Descriptor mínimo implementable») |

M3 compara dos piezas a partir de su organización visible, tal como la registra la anotación estructural congelada v2.1 (`data/metadata/v2_1_congelado/`). La formalización completa, con las demostraciones, está en el capítulo 5 del manuscrito (`docs/manuscrito/capitulo_5_metodo_formal.md`). Es un sistema **asistido por anotación**: dispone de información humana a la que M2 no tiene acceso. Por eso, la comparación entre ambos mide la utilidad de cada sistema para la recuperación y no la superioridad de un método de extracción automática. M3 no interpreta el significado de los motivos ni atribuye una cultura de origen.

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

**Forma canónica.** Se define *c(w)* = mín_lex {*w*, rev(*w*)}. Puesto que {*w*, rev(*w*)} = {rev(*w*), rev(rev(*w*))}, se cumple *c*(rev(*w*)) = *c*(*w*); es decir, leer la pieza en el sentido opuesto no cambia su forma canónica. El cálculo tiene un costo O(*l*) en la longitud de la palabra. La forma canónica sirve para contar las órbitas y para decidir si dos palabras son equivalentes; la disimilitud no la necesita, porque la distancia entre palabras ya toma el mínimo sobre la órbita.

**Distancia entre palabras.** La distancia es *d*(*w*, *v*) = mín{lev(*w*, *v*), lev(*w*, rev *v*)} / máx(\|*w*\|, \|*v*\|), donde lev es la distancia de Levenshtein y las lagunas se eliminan antes de comparar. Como la reversión preserva la distancia de Levenshtein, se cumple *d*(*w*, *v*) = *d*(rev *w*, *v*) = *d*(*w*, rev *v*). Dos piezas sin bandas (dos palabras vacías) están a distancia 0, y una palabra vacía frente a una no vacía está a distancia 1. El costo es O(*l* · *l*′).

**Adyacencias.** Se construye el histograma normalizado de los pares **no dirigidos** de bandas contiguas dentro de cada tramo observado. Una laguna interrumpe el tramo y no forma pares. Al no considerar la dirección, el histograma es invariante a la reversión sin necesidad de elegir un sentido de lectura. Si alguna de las dos piezas no tiene ningún par (porque tiene una sola banda o ninguna), el bloque se considera no observable para ese par de piezas.

**Periodo, retirado.** La versión 0.1 calculaba el periodo de la palabra como dato informativo, sin intervenir en la disimilitud. Se retiró en la 0.2: la repetición entra en el descriptor como atributo anotado, y el capítulo 5 del manuscrito no usa el periodo (sección 5.16).

Dos ejemplos ilustran estas definiciones:
- Las palabras `aabb` y `abab` tienen el mismo histograma de tipos y distintas adyacencias. Por eso es indispensable un control sin orden para atribuir una ganancia al orden de las bandas.
- Con cuatro posiciones, dos símbolos y el grupo C₂ hay 2⁴ palabras, de las cuales la reversión deja fijas 2². Por el lema de Burnside, el número de formas canónicas es (16 + 4) / 2 = 10. El ejemplo forma parte de las pruebas unitarias; no es un resultado experimental.

## 3. Disimilitud mixta

La disimilitud entre dos piezas es

D(*i*, *j*) = Σ_b λ_b *m_ib* *m_jb* *d_b*(*i*, *j*) / Σ_b λ_b *m_ib* *m_jb*,

con pesos λ_b ≥ 0 definidos en `[m3.pesos]`.

**Ausencia de evidencia.** Si el denominador es 0, ningún bloque es observable en ambas piezas y la disimilitud no está definida. El par queda «sin evidencia estructural»: no recibe la similitud máxima y, en el ranking de M3, esos candidatos se ubican al final, ordenados por identificador.

**Cobertura.** Se define como Σ_b λ_b *m_ib* *m_jb* / Σ_b λ_b y se informa junto con D. La regla de reparto de pesos de M4 no usa su valor: solo distingue si hay evidencia estructural (cobertura mayor que cero) o no.

**Puntuación para el ranking.** *s* = 1 − D.

**Propiedades.**
- D(*i*, *i*) = 0, D es simétrica y toma valores en [0, 1].
- Con máscaras variables, D es una **disimilitud**, no una métrica: no se garantiza la desigualdad triangular ni que defina un núcleo semidefinido positivo, y ningún paso del método depende de esas propiedades.

**Contribuciones.** La contribución de cada bloque es *c_b* = λ_b *d_b* / Σ λ m m. Su suma reconstruye D de forma exacta, que es la primera comprobación de H3 en el protocolo. Retirar un bloque (λ_b = 0) recalcula D con los bloques restantes renormalizados, que es la segunda comprobación.

## 4. M3-sin-orden, control del mecanismo (H2)

M3-sin-orden coincide con M3 salvo en dos aspectos:
- la palabra de bandas se sustituye por el histograma de sus tipos, sin lagunas, comparado con la mitad de la distancia L1;
- se omite el bloque de adyacencias.

Usa los mismos pesos, sin reajustarlos. Si M3 supera a M3-sin-orden, la diferencia puede atribuirse al orden de las bandas y no a su composición por tipos.

## 5. Límites del descriptor

- **El eje es fotográfico, no estructural.** `eje_bandas` registra la orientación de las bandas en la fotografía del museo, no la dirección de la urdimbre. En las túnicas de tapiz wari e inca la urdimbre corre en horizontal cuando la prenda está en posición de uso, de modo que una misma organización puede aparecer como horizontal o vertical según cómo se fotografió la pieza. La forma canónica es invariante a la reversión, no a una rotación de 90°: la comparación de palabras no depende del eje, pero el bloque de composición y el propio eje sí reflejan la toma.
- **La reversión descarta la orientación de la prenda.** Para un fragmento, el sentido de lectura es convencional. Para una túnica con abertura de cuello o un manto con cenefa en un solo extremo, no lo es. Tratar w y rev(w) como equivalentes es una simplificación que se declara entre las limitaciones.
- **La estructura no es independiente de la técnica ni de la tradición.** Los paños de cara de urdimbre tienden a las listas, la tapicería admite campos figurativos y retículas, y el bordado paracas ordena figuras en cenefas y damero. Una similitud estructural alta puede reflejar en parte la pertenencia a una misma tradición, que un codificador visual también capta. Una ganancia de M3 no se leerá, por sí sola, como evidencia de una gramática estructural independiente del estilo.

## 6. Ajuste y congelación

Los pesos parten de valores iguales (1,0) y el protocolo solo permite ajustarlos con las consultas de desarrollo. No se ajustaron: primero, a la espera de la respuesta del asesor sobre los juicios de desarrollo (R24); después, porque los pesos de M4 se eligieron con M3 en sus valores de partida y ajustar M3 obligaría a repetir esa selección (R28). Quedan fijos en 1,0 (R30). El descriptor se calcula sobre la anotación congelada v2.1. Los rankings de M3 se generaron en desarrollo el 17 de noviembre; en prueba se generarán una sola vez, con los sistemas congelados.

## 7. Pruebas de propiedades

Las pruebas de `tests/test_sistemas.py` verifican:
- la invariancia de la forma canónica a la reversión;
- el ejemplo de Burnside, con 10 órbitas;
- que `aabb` y `abab` tienen el mismo histograma de tipos y distintas adyacencias;
- la invariancia del histograma de adyacencias a la reversión;
- la simetría y la invariancia a la reversión de la distancia entre palabras, con las lagunas enmascaradas;
- que D es simétrica, nula consigo misma, acotada en [0, 1] y no definida cuando no hay bloques comunes;
- que la suma de las contribuciones reconstruye D y que la intervención sobre un bloque coincide con la fórmula;
- que la distancia del control sin orden nunca supera a la distancia entre palabras (proposición 5.6 del capítulo 5), por enumeración exhaustiva;
- que M3-sin-orden no distingue el orden de las bandas y M3 sí.
