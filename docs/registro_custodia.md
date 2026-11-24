# Registro de custodia del test

Registro de la ejecución única del test (protocolo experimental v2, sección 9; decisión R37). No se usa una firma criptográfica personal: la custodia se acredita con tres elementos.

1. Una etiqueta Git anotada en cada cambio de estado de la corrida.
2. Este registro, con una fila por estado.
3. El envío de las huellas de cada estado al asesor por correo, en el momento de sellarlas.

Las huellas las imprime `python -m src.experimento.ejecucion_prueba` al terminar cada paso, y quedan también en el manifiesto de ejecución (`data/processed/experimento_v2_manifiesto_ejecucion.json`). Este registro lo completa el responsable a mano; el código no lo escribe.

## Estados de la corrida

| Fecha | Estado | Responsable | Corrida | Commit | Etiqueta | Huellas enviadas al asesor |
|---|---|---|---|---|---|---|
| 2026-11-23 | `autorizada` | Henry Sánchez Alvarado; autorización del asesor César Lara Ávila en reunión | `corrida-1d7165cf4dab` | `2b01f0e` autorizado; la autorización se registra en el commit de la etiqueta | `test-v2-autorizado` | Enviadas por correo el 2026-11-24, todas juntas tras la evaluación: suma del protocolo `fd43ebaecde64c3505dedf3660fa1084a12ddaee0e7c3f2789c086758d3fc22d` |
| 2026-11-23 | `insumos_sellados` | Henry Sánchez Alvarado | `corrida-1d7165cf4dab` | `cc501ae` (árbol limpio) | `test-v2-rankings-sellados` | Enviadas por correo el 2026-11-24, todas juntas tras la evaluación: 17 sumas de insumos del manifiesto de ejecución |
| 2026-11-23 | `rankings_sellados` | Henry Sánchez Alvarado | `corrida-1d7165cf4dab` | `cc501ae` | `test-v2-rankings-sellados` | Enviadas por correo el 2026-11-24, todas juntas tras la evaluación: rankings T3 `0a8d8176…2e3d`, rankings T1 `4b331212…767c`, pool T3 `5eb38c2e…f651`, pool T1 `fbf719eb…e3c1` |
| 2026-11-24 | `juicios_cerrados` | Henry Sánchez Alvarado; juicios de T3 (1283 pares) y T1 (212 pares) emitidos sin asistencia | `corrida-1d7165cf4dab` | el de la etiqueta | `test-v2-juicios-cerrados` | Enviadas por correo el 2026-11-24, todas juntas tras la evaluación: juicios T3 `ee52f855…f3e2` (libro `a480dfe3…c447`), juicios T1 `d1aa209e…13fd` (libro `6cc822c7…8473`) |
| 2026-11-24 | `evaluada` | Henry Sánchez Alvarado; revisión descriptiva de H3 (10 fichas) hecha sin asistencia | `corrida-1d7165cf4dab` | el de la etiqueta | `test-v2-evaluada` | Enviadas por correo el 2026-11-24, todas juntas tras la evaluación: informe `046cf990…d4a7`, métricas por consulta `9aa7145c…2b0f`, revisión H3 `be9a71cb…a1a9` (libro `f080efbe…d48a`), muestra H3 `f9b7fb4f…c48a` |

## Fallos, suspensiones y desviaciones del protocolo

Cada fallo de un paso, cada suspensión de la corrida y cada desviación del protocolo se anotan aquí con su fecha, lo ocurrido, su motivo y lo que se hizo. Después de una suspensión no se repite ningún paso sin la conformidad del asesor.

| Fecha | Estado | Hecho | Motivo | Acción |
|---|---|---|---|---|
| 2026-11-24 | `autorizada` a `evaluada` | Las sumas de los cinco estados se enviaron al asesor juntas, por correo, el 24 de noviembre después de la evaluación, y no en el momento de sellar cada estado (protocolo, sección 9). | El envío se dejó para el final de la corrida. | Se registra como desviación del procedimiento de custodia, sin efecto sobre los datos ni las métricas. Entre el sellado y el envío, la secuencia la fijan las etiquetas Git anotadas (23-11 12:21 y 12:23; 24-11 12:36 y 14:10, hora de Lima), y la evaluación comprobó las 25 sumas. Se declara en el anexo B del informe y en el capítulo 8. |
