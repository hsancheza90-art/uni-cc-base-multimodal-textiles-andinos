# Revision de criterios de la anotacion v2

Generado por `python -m src.anotacion.aplicar_anotaciones_v2`, paso del flujo, con las reglas de `src/anotacion/revision_criterios.py`. Workbook: `data/metadata/anotacion_v2_revision_criterios.xlsx`; parametros en `config/anotacion.toml` ([revision_criterios]).

Los lotes 2, 3, 4, 5 se anotaron antes de escribir la definicion de banda (R12) y la frontera entre simetria traslacional y repeticion modular (R16). El anotador vuelve a mirar las piezas afectadas y confirma o corrige. La primera anotacion no se modifica en su workbook: las correcciones se aplican al exportar `data/metadata/anotaciones_v2.csv` y quedan registradas abajo.

- Piezas en revision: 108.
- Confirmadas: 66; corregidas: 42; pendientes: 0.
- Valores corregidos: 173.
- Propuestas automaticas sin verificar (`revisor = auto`): 0. No se aplican: cuentan como pendientes hasta que el revisor las verifica y firma.
- Decisiones verificadas frente a la propuesta automatica: distinta de la propuesta, 42; igual a la propuesta, 66.

## Piezas por motivo de revision

| Motivo | Piezas |
|---|---|
| R12 | 52 |
| R16 | 85 |
| OBS | 32 |
| ID | 22 |

`R12`: tiene palabra de bandas. `R16`: simetria traslacional o repeticion_modular. `OBS`: sus observaciones marcan una duda o un criterio sobre un atributo que usa M3. `ID`: sus observaciones piden verificar que la imagen corresponde al registro. Una pieza puede tener varios motivos.

## Observaciones que no entran a la revision

| Tipo | Piezas |
|---|---|
| dudas sobre atributos que M3 no usa | 46 |
| huecos de vocabulario (VOCAB) | 16 |

No tocan ningun atributo de M3 (`motivo_principal`, color, tecnica, tipo de objeto o de superficie) o son huecos del vocabulario. No se resuelven en la version 2.1 y se declaran como limitacion.

## Registro de adjudicaciones

| Pieza | Atributo | Antes | Despues | Motivo |
|---|---|---|---|---|
| AIC:181388 | `composicion` | reticula | bandas | Las cuatro franjas de abajo (bloques, aves, zigzag y figuras) cruzan la tira y forman la palabra; los recuadros de arriba no entran en ella (R12). Se repiten como módulos: repetición modular. |
| AIC:181388 | `secuencia_bandas` | figurativa > figurativa > figurativa > figurativa > geometrica > figurativa > geometrica > figurativa | geometrica > figurativa > geometrica > figurativa | Las cuatro franjas de abajo (bloques, aves, zigzag y figuras) cruzan la tira y forman la palabra; los recuadros de arriba no entran en ella (R12). Se repiten como módulos: repetición modular. |
| AIC:181388 | `borde` | no | si | Las cuatro franjas de abajo (bloques, aves, zigzag y figuras) cruzan la tira y forman la palabra; los recuadros de arriba no entran en ella (R12). Se repiten como módulos: repetición modular. |
| AIC:181388 | `familia_iconografica` | figurativa | mixta | Las cuatro franjas de abajo (bloques, aves, zigzag y figuras) cruzan la tira y forman la palabra; los recuadros de arriba no entran en ella (R12). Se repiten como módulos: repetición modular. |
| MET:310511 | `composicion` | bandas | paneles | Los dos registros se leen como paneles; las franjas que los cruzan dan geométrica > figurativa. El motivo avanza en un solo sentido dentro de cada franja: traslacional (R16). |
| MET:310511 | `secuencia_bandas` | figurativa > figurativa | geometrica > figurativa | Los dos registros se leen como paneles; las franjas que los cruzan dan geométrica > figurativa. El motivo avanza en un solo sentido dentro de cada franja: traslacional (R16). |
| MET:310511 | `simetria` | repeticion_modular | traslacional | Los dos registros se leen como paneles; las franjas que los cruzan dan geométrica > figurativa. El motivo avanza en un solo sentido dentro de cada franja: traslacional (R16). |
| MET:310511 | `motivos` | geometrico; zoomorfo | geometrico | Los dos registros se leen como paneles; las franjas que los cruzan dan geométrica > figurativa. El motivo avanza en un solo sentido dentro de cada franja: traslacional (R16). |
| MET:310511 | `familia_iconografica` | mixta | abstracta | Los dos registros se leen como paneles; las franjas que los cruzan dan geométrica > figurativa. El motivo avanza en un solo sentido dentro de cada franja: traslacional (R16). |
| AIC:85245 | `eje_bandas` | horizontal | ausente | El campo de monos no es banda y las franjas de los extremos lo rodean como cenefa, ya registrada en borde (R12). Los monos avanzan en hileras en un solo sentido: traslacional. |
| AIC:85245 | `secuencia_bandas` | lisa > geometrica > lisa > figurativa > lisa > geometrica > lisa | ausente | El campo de monos no es banda y las franjas de los extremos lo rodean como cenefa, ya registrada en borde (R12). Los monos avanzan en hileras en un solo sentido: traslacional. |
| AIC:85245 | `simetria` | repeticion_modular | traslacional | El campo de monos no es banda y las franjas de los extremos lo rodean como cenefa, ya registrada en borde (R12). Los monos avanzan en hileras en un solo sentido: traslacional. |
| AIC:85245 | `motivos` | geometrico; antropomorfo; zoomorfo | antropomorfo; zoomorfo | El campo de monos no es banda y las franjas de los extremos lo rodean como cenefa, ya registrada en borde (R12). Los monos avanzan en hileras en un solo sentido: traslacional. |
| AIC:85245 | `familia_iconografica` | figurativa | abstracta | El campo de monos no es banda y las franjas de los extremos lo rodean como cenefa, ya registrada en borde (R12). Los monos avanzan en hileras en un solo sentido: traslacional. |
| CMA:165266 | `secuencia_bandas` | lisa > figurativa > lisa > figurativa | lisa > figurativa > lisa | El campo con el ave no es banda; solo cuentan las franjas de arriba que cruzan la pieza (R12). |
| CMA:165266 | `motivos` | antropomorfo; zoomorfo | zoomorfo | El campo con el ave no es banda; solo cuentan las franjas de arriba que cruzan la pieza (R12). |
| CMA:165266 | `familia_iconografica` | figurativa | abstracta | El campo con el ave no es banda; solo cuentan las franjas de arriba que cruzan la pieza (R12). |
| AIC:85006 | `secuencia_bandas` | figurativa | lisa > figurativa | La banda de aves va acompañada de una franja lisa que también cruza la pieza. Las aves avanzan en un solo sentido: friso traslacional (R16). |
| AIC:85006 | `simetria` | repeticion_modular | traslacional | La banda de aves va acompañada de una franja lisa que también cruza la pieza. Las aves avanzan en un solo sentido: friso traslacional (R16). |
| AIC:237551 | `eje_bandas` | horizontal | ausente | Las franjas de arriba, abajo y a la izquierda rodean el campo: son cenefa, ya registrada en borde, no bandas (R12). |
| AIC:237551 | `secuencia_bandas` | geometrica > figurativa > geometrica | ausente | Las franjas de arriba, abajo y a la izquierda rodean el campo: son cenefa, ya registrada en borde, no bandas (R12). |
| AIC:237551 | `motivos` | geometrico; antropomorfo; zoomorfo | zoomorfo | Las franjas de arriba, abajo y a la izquierda rodean el campo: son cenefa, ya registrada en borde, no bandas (R12). |
| AIC:237551 | `familia_iconografica` | figurativa | abstracta | Las franjas de arriba, abajo y a la izquierda rodean el campo: son cenefa, ya registrada en borde, no bandas (R12). |
| AIC:85639 | `borde` | no | si | El damero y los camélidos se repiten en filas y columnas: repetición modular, no friso (R16). |
| AIC:85639 | `simetria` | traslacional | repeticion_modular | El damero y los camélidos se repiten en filas y columnas: repetición modular, no friso (R16). |
| AIC:85639 | `familia_iconografica` | mixta | figurativa | El damero y los camélidos se repiten en filas y columnas: repetición modular, no friso (R16). |
| CMA:134604 | `composicion` | reticula | bandas | El damero de arriba es retícula y no entra en la palabra; quedan las seis franjas lisas de abajo (R12). El damero ocupa la mayor parte: repetición modular. |
| CMA:134604 | `secuencia_bandas` | geometrica > geometrica > geometrica > geometrica > geometrica > geometrica > geometrica > lisa > lisa > lisa > lisa > lisa > lisa | lisa > lisa > lisa > lisa > lisa > lisa | El damero de arriba es retícula y no entra en la palabra; quedan las seis franjas lisas de abajo (R12). El damero ocupa la mayor parte: repetición modular. |
| AIC:6114 | `simetria` | traslacional | repeticion_modular | Dos recuadros con el mismo motivo se repiten como unidad: repetición modular (R16). Las aves que los rodean son relleno, no bandas. |
| AIC:6114 | `motivos` | geometrico; antropomorfo; zoomorfo | geometrico; zoomorfo | Dos recuadros con el mismo motivo se repiten como unidad: repetición modular (R16). Las aves que los rodean son relleno, no bandas. |
| AIC:6114 | `familia_iconografica` | figurativa | geometrica | Dos recuadros con el mismo motivo se repiten como unidad: repetición modular (R16). Las aves que los rodean son relleno, no bandas. |
| MET:307959 | `composicion` | bandas | paneles | Tira con pares de figuras separados por tramos lisos: se leen como paneles que se repiten, sin bandas (R12, R16). |
| MET:307959 | `eje_bandas` | horizontal | ausente | Tira con pares de figuras separados por tramos lisos: se leen como paneles que se repiten, sin bandas (R12, R16). |
| MET:307959 | `secuencia_bandas` | figurativa | ausente | Tira con pares de figuras separados por tramos lisos: se leen como paneles que se repiten, sin bandas (R12, R16). |
| MET:307959 | `borde` | no | no_visible | Tira con pares de figuras separados por tramos lisos: se leen como paneles que se repiten, sin bandas (R12, R16). |
| MET:307959 | `motivos` | zoomorfo | geometrico | Tira con pares de figuras separados por tramos lisos: se leen como paneles que se repiten, sin bandas (R12, R16). |
| MET:307959 | `familia_iconografica` | figurativa | geometrica | Tira con pares de figuras separados por tramos lisos: se leen como paneles que se repiten, sin bandas (R12, R16). |
| CMA:163708 | `secuencia_bandas` | geometrica > figurativa > figurativa > geometrica | geometrica > geometrica | Las dos franjas a cuadros de los lados cruzan toda la altura; el campo central no es banda (R12). En él, la figura se repite en filas y columnas: repetición modular. |
| CMA:163708 | `borde` | no | si | Las dos franjas a cuadros de los lados cruzan toda la altura; el campo central no es banda (R12). En él, la figura se repite en filas y columnas: repetición modular. |
| CMA:163708 | `simetria` | traslacional | repeticion_modular | Las dos franjas a cuadros de los lados cruzan toda la altura; el campo central no es banda (R12). En él, la figura se repite en filas y columnas: repetición modular. |
| CMA:163708 | `motivos` | geometrico; zoomorfo | geometrico | Las dos franjas a cuadros de los lados cruzan toda la altura; el campo central no es banda (R12). En él, la figura se repite en filas y columnas: repetición modular. |
| CMA:163708 | `familia_iconografica` | mixta | geometrica | Las dos franjas a cuadros de los lados cruzan toda la altura; el campo central no es banda (R12). En él, la figura se repite en filas y columnas: repetición modular. |
| MET:307941 | `secuencia_bandas` | figurativa > figurativa > figurativa | figurativa | Los campos laterales repiten el camélido en filas y columnas: repetición modular (R16). Solo la banda central, con camélidos, cruza la pieza. |
| MET:307941 | `borde` | no | si | Los campos laterales repiten el camélido en filas y columnas: repetición modular (R16). Solo la banda central, con camélidos, cruza la pieza. |
| MET:307941 | `simetria` | traslacional | repeticion_modular | Los campos laterales repiten el camélido en filas y columnas: repetición modular (R16). Solo la banda central, con camélidos, cruza la pieza. |
| CMA:132125 | `composicion` | bandas | paneles | Se lee como paneles, sin bandas; dentro de ellos el motivo avanza en un solo sentido: traslacional (R16). |
| CMA:132125 | `eje_bandas` | horizontal | ausente | Se lee como paneles, sin bandas; dentro de ellos el motivo avanza en un solo sentido: traslacional (R16). |
| CMA:132125 | `secuencia_bandas` | figurativa | ausente | Se lee como paneles, sin bandas; dentro de ellos el motivo avanza en un solo sentido: traslacional (R16). |
| CMA:132125 | `borde` | no | si | Se lee como paneles, sin bandas; dentro de ellos el motivo avanza en un solo sentido: traslacional (R16). |
| CMA:132125 | `simetria` | repeticion_modular | traslacional | Se lee como paneles, sin bandas; dentro de ellos el motivo avanza en un solo sentido: traslacional (R16). |
| CMA:132125 | `motivos` | antropomorfo; zoomorfo | geometrico; antropomorfo | Se lee como paneles, sin bandas; dentro de ellos el motivo avanza en un solo sentido: traslacional (R16). |
| CMA:132125 | `familia_iconografica` | figurativa | abstracta | Se lee como paneles, sin bandas; dentro de ellos el motivo avanza en un solo sentido: traslacional (R16). |
| AIC:85467 | `composicion` | bandas | reticula | Los cuadros enmarcados forman una retícula y no son bandas (R12); solo cuentan las dos franjas de triángulos que cruzan la pieza. |
| AIC:85467 | `secuencia_bandas` | figurativa > figurativa > geometrica > figurativa > geometrica > figurativa | geometrica > geometrica | Los cuadros enmarcados forman una retícula y no son bandas (R12); solo cuentan las dos franjas de triángulos que cruzan la pieza. |
| AIC:85467 | `borde` | no | si | Los cuadros enmarcados forman una retícula y no son bandas (R12); solo cuentan las dos franjas de triángulos que cruzan la pieza. |
| AIC:85467 | `familia_iconografica` | figurativa | geometrica | Los cuadros enmarcados forman una retícula y no son bandas (R12); solo cuentan las dos franjas de triángulos que cruzan la pieza. |
| CMA:294068 | `borde` | no | no_visible | El motivo se repite en filas y columnas por todo el campo: repetición modular (R16). |
| CMA:294068 | `simetria` | traslacional | repeticion_modular | El motivo se repite en filas y columnas por todo el campo: repetición modular (R16). |
| AIC:152928 | `composicion` | reticula | paneles | Campo diagonal con el motivo repetido en dos direcciones: repetición modular (R16). A la izquierda, una franja lisa recorre toda la altura. |
| AIC:152928 | `eje_bandas` | ausente | vertical | Campo diagonal con el motivo repetido en dos direcciones: repetición modular (R16). A la izquierda, una franja lisa recorre toda la altura. |
| AIC:152928 | `secuencia_bandas` | ausente | lisa | Campo diagonal con el motivo repetido en dos direcciones: repetición modular (R16). A la izquierda, una franja lisa recorre toda la altura. |
| AIC:152928 | `borde` | no | si | Campo diagonal con el motivo repetido en dos direcciones: repetición modular (R16). A la izquierda, una franja lisa recorre toda la altura. |
| AIC:152928 | `simetria` | traslacional | repeticion_modular | Campo diagonal con el motivo repetido en dos direcciones: repetición modular (R16). A la izquierda, una franja lisa recorre toda la altura. |
| AIC:152928 | `familia_iconografica` | mixta | geometrica | Campo diagonal con el motivo repetido en dos direcciones: repetición modular (R16). A la izquierda, una franja lisa recorre toda la altura. |
| MET:313153 | `secuencia_bandas` | figurativa > figurativa > lisa | figurativa > lisa | El campo de los felinos no es banda; cruzan la prenda la banda de felinos y las listas amarillas (R12). Los dos felinos se reflejan: simetría bilateral. |
| MET:313153 | `simetria` | traslacional | bilateral | El campo de los felinos no es banda; cruzan la prenda la banda de felinos y las listas amarillas (R12). Los dos felinos se reflejan: simetría bilateral. |
| MET:313153 | `motivos` | geometrico; zoomorfo | zoomorfo | El campo de los felinos no es banda; cruzan la prenda la banda de felinos y las listas amarillas (R12). Los dos felinos se reflejan: simetría bilateral. |
| AIC:181387 | `composicion` | campo_central | paneles | Los recuadros de arriba son paneles, no bandas; cruzan la tira las franjas de aves, zigzag y figuras (R12). |
| AIC:181387 | `secuencia_bandas` | figurativa > figurativa > geometrica > figurativa | figurativa > geometrica > figurativa | Los recuadros de arriba son paneles, no bandas; cruzan la tira las franjas de aves, zigzag y figuras (R12). |
| AIC:181387 | `motivos` | geometrico; antropomorfo; zoomorfo | antropomorfo; zoomorfo | Los recuadros de arriba son paneles, no bandas; cruzan la tira las franjas de aves, zigzag y figuras (R12). |
| AIC:152929 | `composicion` | bandas | paneles | Los recuadros con figuras son paneles y salen de la palabra (R12); quedan las listas y la franja de rombos que cruzan la pieza. Cada franja avanza en un solo sentido: traslacional. |
| AIC:152929 | `secuencia_bandas` | lisa > figurativa > lisa > geometrica > lisa | lisa > lisa > geometrica > lisa | Los recuadros con figuras son paneles y salen de la palabra (R12); quedan las listas y la franja de rombos que cruzan la pieza. Cada franja avanza en un solo sentido: traslacional. |
| AIC:152929 | `borde` | no | si | Los recuadros con figuras son paneles y salen de la palabra (R12); quedan las listas y la franja de rombos que cruzan la pieza. Cada franja avanza en un solo sentido: traslacional. |
| AIC:152929 | `simetria` | repeticion_modular | traslacional | Los recuadros con figuras son paneles y salen de la palabra (R12); quedan las listas y la franja de rombos que cruzan la pieza. Cada franja avanza en un solo sentido: traslacional. |
| AIC:152929 | `familia_iconografica` | mixta | figurativa | Los recuadros con figuras son paneles y salen de la palabra (R12); quedan las listas y la franja de rombos que cruzan la pieza. Cada franja avanza en un solo sentido: traslacional. |
| MET:312669 | `composicion` | bandas | paneles | Las filas de recuadros son paneles; entre ellas corren franjas que cruzan la pieza, cada una con su friso en un solo sentido: traslacional (R16). |
| MET:312669 | `secuencia_bandas` | figurativa > geometrica > figurativa > figurativa > figurativa > geometrica | figurativa > geometrica > figurativa | Las filas de recuadros son paneles; entre ellas corren franjas que cruzan la pieza, cada una con su friso en un solo sentido: traslacional (R16). |
| MET:312669 | `borde` | no | si | Las filas de recuadros son paneles; entre ellas corren franjas que cruzan la pieza, cada una con su friso en un solo sentido: traslacional (R16). |
| MET:312669 | `simetria` | repeticion_modular | traslacional | Las filas de recuadros son paneles; entre ellas corren franjas que cruzan la pieza, cada una con su friso en un solo sentido: traslacional (R16). |
| MET:312669 | `motivos` | geometrico; antropomorfo; zoomorfo | antropomorfo; zoomorfo | Las filas de recuadros son paneles; entre ellas corren franjas que cruzan la pieza, cada una con su friso en un solo sentido: traslacional (R16). |
| AIC:85520 | `borde` | no | si | Las columnas son bandas paralelas, cada una con un friso en un solo sentido: traslacional (R16). |
| AIC:85520 | `simetria` | repeticion_modular | traslacional | Las columnas son bandas paralelas, cada una con un friso en un solo sentido: traslacional (R16). |
| AIC:181384 | `composicion` | campo_central | paneles | Los recuadros del campo son paneles, no bandas; solo las dos franjas de abajo cruzan todo el ancho, y la última combina figuras y zigzag (R12). |
| AIC:181384 | `secuencia_bandas` | figurativa > figurativa > geometrica > figurativa > geometrica | figurativa > mixta | Los recuadros del campo son paneles, no bandas; solo las dos franjas de abajo cruzan todo el ancho, y la última combina figuras y zigzag (R12). |
| AIC:181384 | `simetria` | repeticion_modular | traslacional | Los recuadros del campo son paneles, no bandas; solo las dos franjas de abajo cruzan todo el ancho, y la última combina figuras y zigzag (R12). |
| AIC:181384 | `motivos` | geometrico; antropomorfo; zoomorfo | antropomorfo; zoomorfo | Los recuadros del campo son paneles, no bandas; solo las dos franjas de abajo cruzan todo el ancho, y la última combina figuras y zigzag (R12). |
| AIC:181384 | `familia_iconografica` | figurativa | geometrica | Los recuadros del campo son paneles, no bandas; solo las dos franjas de abajo cruzan todo el ancho, y la última combina figuras y zigzag (R12). |
| MET:307953 | `composicion` | bandas | paneles | Fragmentos de una misma tira con un solo motivo repetido: se leen como paneles, sin bandas. El motivo avanza en un solo sentido: traslacional (R16). |
| MET:307953 | `eje_bandas` | horizontal | ausente | Fragmentos de una misma tira con un solo motivo repetido: se leen como paneles, sin bandas. El motivo avanza en un solo sentido: traslacional (R16). |
| MET:307953 | `secuencia_bandas` | figurativa | ausente | Fragmentos de una misma tira con un solo motivo repetido: se leen como paneles, sin bandas. El motivo avanza en un solo sentido: traslacional (R16). |
| MET:307953 | `borde` | no | si | Fragmentos de una misma tira con un solo motivo repetido: se leen como paneles, sin bandas. El motivo avanza en un solo sentido: traslacional (R16). |
| MET:307953 | `simetria` | repeticion_modular | traslacional | Fragmentos de una misma tira con un solo motivo repetido: se leen como paneles, sin bandas. El motivo avanza en un solo sentido: traslacional (R16). |
| CMA:104242 | `composicion` | bandas | reticula | Tira con triángulos en diagonal que cubren toda la superficie decorada: se lee como retícula, sin bandas. El diseño avanza en un solo sentido: traslacional (R16). |
| CMA:104242 | `eje_bandas` | horizontal | ausente | Tira con triángulos en diagonal que cubren toda la superficie decorada: se lee como retícula, sin bandas. El diseño avanza en un solo sentido: traslacional (R16). |
| CMA:104242 | `secuencia_bandas` | lisa > geometrica > lisa > lisa | ausente | Tira con triángulos en diagonal que cubren toda la superficie decorada: se lee como retícula, sin bandas. El diseño avanza en un solo sentido: traslacional (R16). |
| CMA:104242 | `borde` | no | si | Tira con triángulos en diagonal que cubren toda la superficie decorada: se lee como retícula, sin bandas. El diseño avanza en un solo sentido: traslacional (R16). |
| CMA:104242 | `simetria` | repeticion_modular | traslacional | Tira con triángulos en diagonal que cubren toda la superficie decorada: se lee como retícula, sin bandas. El diseño avanza en un solo sentido: traslacional (R16). |
| AIC:85134 | `composicion` | bandas | paneles | Tira con un motivo que se repite a lo largo de una sola dirección: se lee como paneles, sin bandas; traslacional (R16). |
| AIC:85134 | `eje_bandas` | horizontal | ausente | Tira con un motivo que se repite a lo largo de una sola dirección: se lee como paneles, sin bandas; traslacional (R16). |
| AIC:85134 | `secuencia_bandas` | lisa > geometrica > lisa | ausente | Tira con un motivo que se repite a lo largo de una sola dirección: se lee como paneles, sin bandas; traslacional (R16). |
| AIC:85134 | `borde` | no | si | Tira con un motivo que se repite a lo largo de una sola dirección: se lee como paneles, sin bandas; traslacional (R16). |
| AIC:85134 | `simetria` | repeticion_modular | traslacional | Tira con un motivo que se repite a lo largo de una sola dirección: se lee como paneles, sin bandas; traslacional (R16). |
| CMA:104246 | `composicion` | bandas | paneles | Tres tiras con el mismo diseño diagonal: se leen como paneles, sin bandas. El diseño avanza en un solo sentido dentro de cada tira: traslacional (R16). |
| CMA:104246 | `eje_bandas` | horizontal | ausente | Tres tiras con el mismo diseño diagonal: se leen como paneles, sin bandas. El diseño avanza en un solo sentido dentro de cada tira: traslacional (R16). |
| CMA:104246 | `secuencia_bandas` | lisa > geometrica > lisa > lisa | ausente | Tres tiras con el mismo diseño diagonal: se leen como paneles, sin bandas. El diseño avanza en un solo sentido dentro de cada tira: traslacional (R16). |
| CMA:104246 | `borde` | no | si | Tres tiras con el mismo diseño diagonal: se leen como paneles, sin bandas. El diseño avanza en un solo sentido dentro de cada tira: traslacional (R16). |
| CMA:104246 | `simetria` | repeticion_modular | traslacional | Tres tiras con el mismo diseño diagonal: se leen como paneles, sin bandas. El diseño avanza en un solo sentido dentro de cada tira: traslacional (R16). |
| CMA:104246 | `motivos` | geometrico | geometrico; zoomorfo | Tres tiras con el mismo diseño diagonal: se leen como paneles, sin bandas. El diseño avanza en un solo sentido dentro de cada tira: traslacional (R16). |
| CMA:104246 | `familia_iconografica` | geometrica | figurativa | Tres tiras con el mismo diseño diagonal: se leen como paneles, sin bandas. El diseño avanza en un solo sentido dentro de cada tira: traslacional (R16). |
| AIC:85269 | `composicion` | reticula | paneles | El motivo se repite en filas y columnas como unidad: paneles con repetición modular (R16). |
| AIC:85269 | `borde` | no | si | El motivo se repite en filas y columnas como unidad: paneles con repetición modular (R16). |
| AIC:85269 | `simetria` | traslacional | repeticion_modular | El motivo se repite en filas y columnas como unidad: paneles con repetición modular (R16). |
| AIC:85269 | `motivos` | zoomorfo | geometrico; zoomorfo | El motivo se repite en filas y columnas como unidad: paneles con repetición modular (R16). |
| AIC:182605 | `composicion` | bandas | reticula | Tira cubierta por un diseño continuo que se lee como retícula, sin bandas; avanza en un solo sentido: traslacional (R16). |
| AIC:182605 | `eje_bandas` | horizontal | ausente | Tira cubierta por un diseño continuo que se lee como retícula, sin bandas; avanza en un solo sentido: traslacional (R16). |
| AIC:182605 | `secuencia_bandas` | figurativa | ausente | Tira cubierta por un diseño continuo que se lee como retícula, sin bandas; avanza en un solo sentido: traslacional (R16). |
| AIC:182605 | `borde` | no | si | Tira cubierta por un diseño continuo que se lee como retícula, sin bandas; avanza en un solo sentido: traslacional (R16). |
| AIC:182605 | `simetria` | repeticion_modular | traslacional | Tira cubierta por un diseño continuo que se lee como retícula, sin bandas; avanza en un solo sentido: traslacional (R16). |
| AIC:182605 | `motivos` | geometrico; antropomorfo | geometrico | Tira cubierta por un diseño continuo que se lee como retícula, sin bandas; avanza en un solo sentido: traslacional (R16). |
| AIC:182605 | `familia_iconografica` | figurativa | abstracta | Tira cubierta por un diseño continuo que se lee como retícula, sin bandas; avanza en un solo sentido: traslacional (R16). |
| MET:308068 | `borde` | no | si | Recuadros con contorno propio apilados a lo largo de la tira: paneles que se repiten como unidad, sin bandas (C2, R16). |
| MET:308068 | `simetria` | traslacional | repeticion_modular | Recuadros con contorno propio apilados a lo largo de la tira: paneles que se repiten como unidad, sin bandas (C2, R16). |
| MET:308068 | `motivos` | geometrico; zoomorfo | zoomorfo | Recuadros con contorno propio apilados a lo largo de la tira: paneles que se repiten como unidad, sin bandas (C2, R16). |
| CMA:164421 | `composicion` | bandas | reticula | Los cuadros del damero son módulos con contorno propio repetidos en dos dimensiones: retícula sin bandas, repetición modular (R16). |
| CMA:164421 | `eje_bandas` | horizontal | ausente | Los cuadros del damero son módulos con contorno propio repetidos en dos dimensiones: retícula sin bandas, repetición modular (R16). |
| CMA:164421 | `secuencia_bandas` | lisa > geometrica > lisa > geometrica > lisa | ausente | Los cuadros del damero son módulos con contorno propio repetidos en dos dimensiones: retícula sin bandas, repetición modular (R16). |
| CMA:164421 | `borde` | no | si | Los cuadros del damero son módulos con contorno propio repetidos en dos dimensiones: retícula sin bandas, repetición modular (R16). |
| CMA:164421 | `simetria` | traslacional | repeticion_modular | Los cuadros del damero son módulos con contorno propio repetidos en dos dimensiones: retícula sin bandas, repetición modular (R16). |
| AIC:85273 | `secuencia_bandas` | geometrica > lisa > figurativa > lisa > lisa | lisa > figurativa > lisa > lisa | El campo de brocado no es banda (R12); quedan las franjas que lo cruzan por debajo. |
| AIC:85273 | `motivos` | geometrico; zoomorfo | geometrico | El campo de brocado no es banda (R12); quedan las franjas que lo cruzan por debajo. |
| AIC:85273 | `familia_iconografica` | mixta | geometrica | El campo de brocado no es banda (R12); quedan las franjas que lo cruzan por debajo. |
| AIC:85566 | `secuencia_bandas` | figurativa > lisa > figurativa > lisa > figurativa > lisa > figurativa | lisa > figurativa > lisa > figurativa > lisa | Las franjas extremas son la cenefa que rodea los campos (R12); quedan las franjas interiores entre campos lisos. Cada franja es un friso en un solo sentido: traslacional (R16). |
| AIC:85566 | `simetria` | repeticion_modular | traslacional | Las franjas extremas son la cenefa que rodea los campos (R12); quedan las franjas interiores entre campos lisos. Cada franja es un friso en un solo sentido: traslacional (R16). |
| AIC:85566 | `motivos` | geometrico; antropomorfo | geometrico | Las franjas extremas son la cenefa que rodea los campos (R12); quedan las franjas interiores entre campos lisos. Cada franja es un friso en un solo sentido: traslacional (R16). |
| AIC:85566 | `familia_iconografica` | figurativa | geometrica | Las franjas extremas son la cenefa que rodea los campos (R12); quedan las franjas interiores entre campos lisos. Cada franja es un friso en un solo sentido: traslacional (R16). |
| CMA:104245 | `composicion` | bandas | paneles | Tira con un diseño diagonal continuo: se lee como paneles, sin bandas; avanza en un solo sentido: traslacional (R16). |
| CMA:104245 | `eje_bandas` | horizontal | ausente | Tira con un diseño diagonal continuo: se lee como paneles, sin bandas; avanza en un solo sentido: traslacional (R16). |
| CMA:104245 | `secuencia_bandas` | lisa > geometrica > lisa > lisa | ausente | Tira con un diseño diagonal continuo: se lee como paneles, sin bandas; avanza en un solo sentido: traslacional (R16). |
| CMA:104245 | `borde` | no | si | Tira con un diseño diagonal continuo: se lee como paneles, sin bandas; avanza en un solo sentido: traslacional (R16). |
| CMA:104245 | `simetria` | repeticion_modular | traslacional | Tira con un diseño diagonal continuo: se lee como paneles, sin bandas; avanza en un solo sentido: traslacional (R16). |
| AIC:85333 | `composicion` | campo_central | bandas | El campo no es banda (R12): la palabra conserva solo las dos franjas laterales que cruzan toda la altura. |
| AIC:85333 | `secuencia_bandas` | lisa > geometrica > lisa | lisa > lisa | El campo no es banda (R12): la palabra conserva solo las dos franjas laterales que cruzan toda la altura. |
| AIC:85333 | `simetria` | repeticion_modular | traslacional | El campo no es banda (R12): la palabra conserva solo las dos franjas laterales que cruzan toda la altura. |
| AIC:152936 | `simetria` | traslacional | repeticion_modular | La cuadrícula y los animales en filas y columnas cubren la superficie en dos dimensiones: repetición modular (R16). |
| AIC:152936 | `motivos` | geometrico; zoomorfo | geometrico | La cuadrícula y los animales en filas y columnas cubren la superficie en dos dimensiones: repetición modular (R16). |
| AIC:152936 | `familia_iconografica` | mixta | geometrica | La cuadrícula y los animales en filas y columnas cubren la superficie en dos dimensiones: repetición modular (R16). |
| AIC:6102 | `composicion` | campo_central | paneles | El campo central no es banda (R12): quedan las dos franjas de olas que cruzan la pieza arriba y abajo. |
| AIC:6102 | `secuencia_bandas` | geometrica > figurativa > geometrica | geometrica > geometrica | El campo central no es banda (R12): quedan las dos franjas de olas que cruzan la pieza arriba y abajo. |
| MET:316973 | `composicion` | bandas | paneles | Las franjas se leen como paneles, sin bandas; cada una es un friso en un solo sentido: traslacional (R16). |
| MET:316973 | `eje_bandas` | horizontal | ausente | Las franjas se leen como paneles, sin bandas; cada una es un friso en un solo sentido: traslacional (R16). |
| MET:316973 | `secuencia_bandas` | figurativa > geometrica | ausente | Las franjas se leen como paneles, sin bandas; cada una es un friso en un solo sentido: traslacional (R16). |
| MET:316973 | `borde` | no | si | Las franjas se leen como paneles, sin bandas; cada una es un friso en un solo sentido: traslacional (R16). |
| MET:316973 | `simetria` | repeticion_modular | traslacional | Las franjas se leen como paneles, sin bandas; cada una es un friso en un solo sentido: traslacional (R16). |
| MET:316973 | `familia_iconografica` | mixta | figurativa | Las franjas se leen como paneles, sin bandas; cada una es un friso en un solo sentido: traslacional (R16). |
| AIC:3016 | `borde` | no | si | Las figuras se suceden en una sola dirección a lo largo de la tira: traslacional (R16). |
| AIC:3016 | `simetria` | repeticion_modular | traslacional | Las figuras se suceden en una sola dirección a lo largo de la tira: traslacional (R16). |
| CMA:165184 | `secuencia_bandas` | geometrica > lisa > figurativa > lisa > figurativa > lisa > figurativa > lisa > figurativa > lisa > geometrica | figurativa > lisa > figurativa > lisa > figurativa > lisa > figurativa > lisa | Bandas paralelas, cada una con un friso que avanza en un solo sentido: traslacional (R16). Las franjas de los extremos no entran en la palabra. |
| CMA:165184 | `borde` | no | no_visible | Bandas paralelas, cada una con un friso que avanza en un solo sentido: traslacional (R16). Las franjas de los extremos no entran en la palabra. |
| CMA:165184 | `simetria` | repeticion_modular | traslacional | Bandas paralelas, cada una con un friso que avanza en un solo sentido: traslacional (R16). Las franjas de los extremos no entran en la palabra. |
| CMA:165184 | `motivos` | geometrico; antropomorfo | geometrico | Bandas paralelas, cada una con un friso que avanza en un solo sentido: traslacional (R16). Las franjas de los extremos no entran en la palabra. |
| CMA:165184 | `familia_iconografica` | figurativa | geometrica | Bandas paralelas, cada una con un friso que avanza en un solo sentido: traslacional (R16). Las franjas de los extremos no entran en la palabra. |
| AIC:85552 | `composicion` | bandas | reticula | El damero ocupa la mayor parte de la superficie decorada: retícula sin bandas, repetición modular (R16). |
| AIC:85552 | `eje_bandas` | horizontal | ausente | El damero ocupa la mayor parte de la superficie decorada: retícula sin bandas, repetición modular (R16). |
| AIC:85552 | `secuencia_bandas` | geometrica > lisa > geometrica > geometrica | ausente | El damero ocupa la mayor parte de la superficie decorada: retícula sin bandas, repetición modular (R16). |
| AIC:85552 | `simetria` | traslacional | repeticion_modular | El damero ocupa la mayor parte de la superficie decorada: retícula sin bandas, repetición modular (R16). |
| AIC:85552 | `motivos` | geometrico | geometrico; zoomorfo | El damero ocupa la mayor parte de la superficie decorada: retícula sin bandas, repetición modular (R16). |
| AIC:85361 | `composicion` | borde | paneles | Las aves forman filas y columnas sobre el campo, no un friso en un solo sentido: repetición modular (R16). |
| AIC:85361 | `simetria` | traslacional | repeticion_modular | Las aves forman filas y columnas sobre el campo, no un friso en un solo sentido: repetición modular (R16). |
| AIC:85361 | `familia_iconografica` | mixta | figurativa | Las aves forman filas y columnas sobre el campo, no un friso en un solo sentido: repetición modular (R16). |
| MET:308024 | `composicion` | bandas | reticula | Las hileras de animales cubren la bolsa como una retícula, sin bandas; cada hilera avanza en un solo sentido: traslacional (R16). |
| MET:308024 | `eje_bandas` | horizontal | ausente | Las hileras de animales cubren la bolsa como una retícula, sin bandas; cada hilera avanza en un solo sentido: traslacional (R16). |
| MET:308024 | `secuencia_bandas` | lisa > figurativa > figurativa > figurativa > figurativa > figurativa > figurativa | ausente | Las hileras de animales cubren la bolsa como una retícula, sin bandas; cada hilera avanza en un solo sentido: traslacional (R16). |
| MET:308024 | `simetria` | repeticion_modular | traslacional | Las hileras de animales cubren la bolsa como una retícula, sin bandas; cada hilera avanza en un solo sentido: traslacional (R16). |

## Imagenes que no corresponden al registro

- MET:316978
- MET:316341
- MET:307933
- AIC:85310
- AIC:223218
- AIC:85282
- CMA:155505
- AIC:85388

## Errores

Ninguno.
