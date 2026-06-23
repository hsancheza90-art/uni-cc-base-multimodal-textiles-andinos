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
```

---

## Criterio morfologico

Se conserva como excepción metodológica el caso de sombreros o gorros Wari/Huari cuando presentan potencial iconográfico visible, aun cuando no correspondan estrictamente a una superficie plana. Esta excepción se justifica porque algunos objetos tridimensionales textiles pueden contener patrones visuales relevantes para la primera etapa exploratoria.

## Criterio sobre featherwork y plumas

En la primera etapa experimental se separan los objetos de featherwork o con presencia dominante de plumas hacia un corpus secundario. Esta decisión no implica descartar su valor cultural o visual, sino controlar la variabilidad material del corpus principal. 

El corpus principal prioriza textiles tejidos, bordados o con superficie visual amplia comparable. Los objetos con plumas se conservan como registros secundarios para una posible fase posterior de análisis material o iconográfico diferenciado.