# Metodología de curaduría textil

## Propósito

El objetivo de la curaduría es distinguir textiles andinos de otros objetos arqueológicos o artísticos recuperados desde colecciones oficiales digitalizadas.

## Problema

Las búsquedas amplias en APIs museográficas pueden recuperar no solo textiles, sino también cerámicas, objetos metálicos, placas, vasijas y otros artefactos asociados a culturas andinas.

## Estrategia

Se implementó un pipeline en dos etapas:

1. **Recuperación amplia de candidatos**  
   Se consultó la API de The Metropolitan Museum of Art mediante términos relacionados con textiles andinos.

2. **Curaduría automática basada en reglas**  
   Cada registro fue evaluado a partir de:
   - clasificación,
   - título,
   - nombre del objeto,
   - material,
   - etiquetas,
   - evidencia cultural andina.

## Reglas de inclusión

Se asignó evidencia positiva cuando el registro contenía términos como:
- textile,
- woven,
- tapestry,
- embroidery,
- cotton,
- wool,
- camelid,
- tunic,
- mantle,
- sash,
- garment.

## Reglas de exclusión

Se asignó evidencia negativa cuando el registro contenía términos asociados a objetos no textiles, como:
- ceramic,
- pottery,
- vessel,
- bottle,
- plaque,
- gold,
- silver,
- metal,
- mask,
- figurine,
- ornament.

## Resultado

Cada registro recibe:
- un puntaje textil,
- un estado de curación,
- y un motivo explicativo.

Los estados posibles son:
- `aceptado_textil`,
- `revision_manual`,
- `excluido_no_textil`,
- `excluido_sin_imagen`.

## Valor académico

Este enfoque permite construir una base más precisa, trazable y metodológicamente defendible para fines de investigación en ciencias computacionales.