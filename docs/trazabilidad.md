# Protocolo de trazabilidad del corpus piloto

## Propósito

Este documento define los criterios mínimos de trazabilidad para cada registro incluido en la base multimodal de textiles andinos.

La trazabilidad permite verificar el origen, estado, licencia, decisión de filtrado y nivel de anotación de cada objeto incorporado al corpus.

---

## 1. Identificación del registro

Cada objeto debe conservar un identificador interno y un identificador oficial de la fuente.

Campos:

- `id_registro`
- `id_objeto`
- `fuente`
- `institucion`

Ejemplo:

```text
id_registro: MET-319523
fuente: met
institucion: The Metropolitan Museum of Art

## Criterio morfologico

Se conserva como excepción metodológica el caso de sombreros o gorros Wari/Huari cuando presentan potencial iconográfico visible, aun cuando no correspondan estrictamente a una superficie plana. Esta excepción se justifica porque algunos objetos tridimensionales textiles pueden contener patrones visuales relevantes para la primera etapa exploratoria.