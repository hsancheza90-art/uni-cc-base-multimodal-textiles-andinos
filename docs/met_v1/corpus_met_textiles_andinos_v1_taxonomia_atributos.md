# TaxonomÃ­a de atributos para el Corpus MET de Textiles Andinos v1.0

## PropÃ³sito

Este documento define una taxonomÃ­a inicial de atributos para describir textiles andinos dentro de la base multimodal del proyecto. La taxonomÃ­a separa atributos visuales, composicionales, tÃ©cnicos, iconogrÃ¡ficos y contextuales.

La informaciÃ³n oficial del museo se conserva como metadata curatorial. Los atributos visuales e iconogrÃ¡ficos pueden completarse mediante anotaciÃ³n manual controlada en una muestra de anotacion.

---

## 1. Familia visual

| Atributo | DescripciÃ³n | Valores sugeridos |
|---|---|---|
| `color_dominante` | Color visualmente predominante | rojo, marrÃ³n, crema, negro, azul, amarillo, verde, multicolor |
| `colores` | Lista breve de colores visibles | rojo; crema; marrÃ³n |
| `contraste` | Diferencia visual entre colores o zonas | bajo, medio, alto |
| `densidad_visual` | Nivel de saturaciÃ³n de elementos visuales | baja, media, alta |

---

## 2. Familia composicional

| Atributo | DescripciÃ³n | Valores sugeridos |
|---|---|---|
| `composicion` | OrganizaciÃ³n general del diseÃ±o | bandas, campo central, borde, paneles, retÃ­cula, composiciÃ³n libre |
| `simetria` | OrganizaciÃ³n simÃ©trica o repetitiva | bilateral, radial, repeticiÃ³n modular, traslacional, no evidente |
| `repeticion` | Presencia de patrones repetidos | sÃ­, no, parcial |
| `borde` | Presencia de borde decorado | sÃ­, no, no visible |
| `centro` | Presencia de campo central diferenciado | sÃ­, no, no visible |

---

## 3. Familia tÃ©cnica

| Atributo | DescripciÃ³n | Valores sugeridos |
|---|---|---|
| `material_normalizado` | Material normalizado desde metadata oficial | algodÃ³n, fibra de camÃ©lido, lana, plumas |
| `tecnica` | TÃ©cnica identificada desde metadata oficial | tejido, tapiz, bordado, trabajo con plumas |
| `tipo_objeto` | Tipo de textil | manto, tÃºnica, bolso textil, panel textil, fragmento textil, tapiz textil |
| `tipo_superficie` | Utilidad morfolÃ³gica para anÃ¡lisis visual | superficie_amplia, objeto_tridimensional_iconografico, formato_estrecho, borde_o_fragmento_lineal, objeto_tridimensional_no_prioritario, revision_morfologica |

---

## 4. Familia iconogrÃ¡fica

| Atributo | DescripciÃ³n | Valores sugeridos |
|---|---|---|
| `motivos` | Motivos observables | geomÃ©trico, antropomorfo, zoomorfo, fitomorfo, abstracto |
| `familia_iconografica` | Familia dominante de representaciÃ³n | geomÃ©trica, figurativa, mixta, abstracta, no determinada |
| `motivo_principal` | Motivo mÃ¡s visible | rombos, aves, felinos, figuras humanas, serpientes, escalonados, no determinado |

---

## 5. Familia contextual

| Atributo | DescripciÃ³n | Origen |
|---|---|---|
| `cultura` | Cultura o atribuciÃ³n cultural | fuente oficial |
| `periodo` | Periodo histÃ³rico o arqueolÃ³gico | fuente oficial |
| `fecha_objeto` | Fecha estimada del objeto | fuente oficial |
| `procedencia` | PaÃ­s, regiÃ³n o localidad | fuente oficial normalizada |
| `fuente` | Fuente de extracciÃ³n | flujo de trabajo del proyecto |
| `institucion` | InstituciÃ³n museogrÃ¡fica | fuente oficial |
| `url` | URL oficial del objeto | fuente oficial |
| `licencia` | CondiciÃ³n de uso o dominio pÃºblico | fuente oficial |

---

## 6. Estados de control

| Campo | DescripciÃ³n | Valores sugeridos |
|---|---|---|
| `estado_metadata` | Nivel de suficiencia de metadata | completo, parcial, insuficiente |
| `estado_anotacion` | Estado de revisiÃ³n manual | sin_anotar, anotado_manual, revisar |
| `observaciones` | Comentarios metodolÃ³gicos | texto libre breve |

---

## Nota metodolÃ³gica

La taxonomÃ­a no pretende descifrar el significado cultural profundo de los textiles. Su finalidad es construir atributos computables y trazables para experimentos de aprendizaje multimodal, recuperaciÃ³n imagen-texto y anÃ¡lisis comparativo de patrones.
