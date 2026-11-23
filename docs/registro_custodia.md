# Registro de custodia del test

Registro de la ejecución única del test (protocolo experimental v2, sección 9; decisión R37). No se usa una firma criptográfica personal: la custodia se acredita con tres elementos.

1. Una etiqueta Git anotada en cada cambio de estado de la corrida.
2. Este registro, con una fila por estado.
3. El envío de las huellas de cada estado al asesor por correo, en el momento de sellarlas.

Las huellas las imprime `python -m src.experimento.ejecucion_prueba` al terminar cada paso, y quedan también en el manifiesto de ejecución (`data/processed/experimento_v2_manifiesto_ejecucion.json`). Este registro lo completa el responsable a mano; el código no lo escribe.

## Estados de la corrida

| Fecha | Estado | Responsable | Corrida | Commit | Etiqueta | Huellas enviadas al asesor |
|---|---|---|---|---|---|---|
| 2026-11-23 | `autorizada` | Henry Sánchez Alvarado; autorización del asesor César Lara Ávila en reunión | `corrida-1d7165cf4dab` | `2b01f0e` autorizado; la autorización se registra en el commit de la etiqueta | `test-v2-autorizado` | Pendiente: suma del protocolo `fd43ebaecde64c3505dedf3660fa1084a12ddaee0e7c3f2789c086758d3fc22d` |
| 2026-11-23 | `insumos_sellados` | Henry Sánchez Alvarado | `corrida-1d7165cf4dab` | `cc501ae` (árbol limpio) | `test-v2-rankings-sellados` | Pendiente: 17 sumas de insumos del manifiesto de ejecución |
| 2026-11-23 | `rankings_sellados` | Henry Sánchez Alvarado | `corrida-1d7165cf4dab` | `cc501ae` | `test-v2-rankings-sellados` | Pendiente: rankings T3 `0a8d8176…2e3d`, rankings T1 `4b331212…767c`, pool T3 `5eb38c2e…f651`, pool T1 `fbf719eb…e3c1` |
| | `juicios_cerrados` | | | | | |
| | `evaluada` | | | | | |

## Fallos, suspensiones y desviaciones del protocolo

Cada fallo de un paso, cada suspensión de la corrida y cada desviación del protocolo se anotan aquí con su fecha, lo ocurrido, su motivo y lo que se hizo. Después de una suspensión no se repite ningún paso sin la conformidad del asesor.

| Fecha | Estado | Hecho | Motivo | Acción |
|---|---|---|---|---|
