# Registro de custodia del test

Registro de la ejecución única del test (protocolo experimental v2, sección 9; decisión R37). No se usa una firma criptográfica personal: la custodia se acredita con tres elementos.

1. Una etiqueta Git anotada en cada cambio de estado de la corrida.
2. Este registro, con una fila por estado.
3. El envío de las huellas de cada estado al asesor por correo, en el momento de sellarlas.

Las huellas las imprime `python -m src.experimento.ejecucion_prueba` al terminar cada paso, y quedan también en el manifiesto de ejecución (`data/processed/experimento_v2_manifiesto_ejecucion.json`). Este registro lo completa el responsable a mano; el código no lo escribe.

## Estados de la corrida

| Fecha | Estado | Responsable | Corrida | Commit | Etiqueta | Huellas enviadas al asesor |
|---|---|---|---|---|---|---|
| | `autorizada` | | | | | |
| | `insumos_sellados` | | | | | |
| | `rankings_sellados` | | | | | |
| | `juicios_cerrados` | | | | | |
| | `evaluada` | | | | | |

## Fallos, suspensiones y desviaciones del protocolo

Cada fallo de un paso, cada suspensión de la corrida y cada desviación del protocolo se anotan aquí con su fecha, lo ocurrido, su motivo y lo que se hizo. Después de una suspensión no se repite ningún paso sin la conformidad del asesor.

| Fecha | Estado | Hecho | Motivo | Acción |
|---|---|---|---|---|
