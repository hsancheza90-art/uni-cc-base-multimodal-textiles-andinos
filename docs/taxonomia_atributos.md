# Taxonomía de atributos para el corpus piloto

## Propósito

Este documento define una taxonomía inicial de atributos para describir textiles andinos dentro de la base multimodal del proyecto. La taxonomía separa atributos visuales, composicionales, técnicos, iconográficos y contextuales.

La información oficial del museo se conserva como metadata curatorial. Los atributos visuales e iconográficos pueden completarse mediante anotación manual controlada en una muestra piloto.

---

## 1. Familia visual

| Atributo | Descripción | Valores sugeridos |
|---|---|---|
| `color_dominante` | Color visualmente predominante | rojo, marrón, crema, negro, azul, amarillo, verde, multicolor |
| `colores` | Lista breve de colores visibles | rojo; crema; marrón |
| `contraste` | Diferencia visual entre colores o zonas | bajo, medio, alto |
| `densidad_visual` | Nivel de saturación de elementos visuales | baja, media, alta |

---

## 2. Familia composicional

| Atributo | Descripción | Valores sugeridos |
|---|---|---|
| `composicion` | Organización general del diseño | bandas, campo central, borde, paneles, retícula, composición libre |
| `simetria` | Organización simétrica o repetitiva | bilateral, radial, repetición modular, traslacional, no evidente |
| `repeticion` | Presencia de patrones repetidos | sí, no, parcial |
| `borde` | Presencia de borde decorado | sí, no, no visible |
| `centro` | Presencia de campo central diferenciado | sí, no, no visible |

---

## 3. Familia técnica

| Atributo | Descripción | Valores sugeridos |
|---|---|---|
| `material_normalizado` | Material normalizado desde metadata oficial | algodón, fibra de camélido, lana, plumas |
| `tecnica` | Técnica identificada desde metadata oficial | tejido, tapiz, bordado, trabajo con plumas |
| `tipo_objeto` | Tipo de textil | manto, túnica, bolso textil, panel textil, fragmento textil, tapiz textil |
| `tipo_superficie` | Utilidad morfológica para análisis visual | superficie_amplia, formato_estrecho, revision_morfologica |

---

## 4. Familia iconográfica

| Atributo | Descripción | Valores sugeridos |
|---|---|---|
| `motivos` | Motivos observables | geométrico, antropomorfo, zoomorfo, fitomorfo, abstracto |
| `familia_iconografica` | Familia dominante de representación | geométrica, figurativa, mixta, abstracta, no determinada |
| `motivo_principal` | Motivo más visible | rombos, aves, felinos, figuras humanas, serpientes, escalonados, no determinado |

---

## 5. Familia contextual

| Atributo | Descripción | Origen |
|---|---|---|
| `cultura` | Cultura o atribución cultural | fuente oficial |
| `periodo` | Periodo histórico o arqueológico | fuente oficial |
| `fecha_objeto` | Fecha estimada del objeto | fuente oficial |
| `procedencia` | País, región o localidad | fuente oficial normalizada |
| `fuente` | Fuente de extracción | pipeline del proyecto |
| `institucion` | Institución museográfica | fuente oficial |
| `url` | URL oficial del objeto | fuente oficial |
| `licencia` | Condición de uso o dominio público | fuente oficial |

---

## 6. Estados de control

| Campo | Descripción | Valores sugeridos |
|---|---|---|
| `estado_metadata` | Nivel de suficiencia de metadata | completo, parcial, insuficiente |
| `estado_anotacion` | Estado de revisión manual | sin_anotar, anotado_manual, revisar |
| `observaciones` | Comentarios metodológicos | texto libre breve |

---

## Nota metodológica

La taxonomía no pretende descifrar el significado cultural profundo de los textiles. Su finalidad es construir atributos computables y trazables para experimentos de aprendizaje multimodal, recuperación imagen-texto y análisis comparativo de patrones.