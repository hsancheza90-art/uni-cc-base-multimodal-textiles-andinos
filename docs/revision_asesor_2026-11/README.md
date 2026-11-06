# Revisión para el asesor: avance de la segunda parte de la tesis

| | |
|---|---|
| Para | César Lara Ávila, asesor |
| De | Henry Sánchez Alvarado |
| Tesis | «Estructuras combinatorias y representación multimodal en textiles andinos», Maestría en Ciencias de la Computación, UNI |
| Fecha | 6 de noviembre de 2026 |
| Repositorio | https://github.com/hsancheza90-art/uni-cc-base-multimodal-textiles-andinos (rama `main`) |
| Corpus de referencia | Etiqueta `corpus-met-cma-aic-v2.0` |
| Responde a | Auditoría del 20 de octubre de 2026 (informes 01 a 12) |

Profesor:

Le envío el avance de la segunda parte desde su auditoría. El trabajo siguió el plan de cierre al 22 de noviembre (`docs/plan_cierre_tesis.md`), que organiza sus observaciones en cuatro semanas. El estado de cada observación está en la matriz de respuesta. El corpus v2 quedó cerrado, con sus grupos de piezas relacionadas, y el experimento está preparado hasta el punto en que hacen falta los juicios de relevancia. Ningún sistema se ha ejecutado sobre consultas de prueba.

## Lo que le pido

1. **Aprobar el protocolo experimental**, o devolverlo con observaciones. Es la versión 0.4, en estado de propuesta (`docs/protocolo_experimental_v2.md`). Al aprobarse se congela, y cualquier cambio posterior queda en su «Historial» antes de abrir el test.
2. **Ratificar las decisiones del plan que siguen como propuestas** (sección 1 del protocolo):
   - D2: la aptitud es apoyo exploratorio de la curación, rotulado como validación de desarrollo.
   - D4: la galería es el núcleo de 150 piezas, agrupado.
   - D5: ΔnDCG@10 = 0,03, con bootstrap pareado de 10 000 réplicas.
   - D7: versionar la auditoría en el repositorio y dejar la integración continua para después del 22 de noviembre.
3. **Aceptar o declinar el doble juicio parcial.** Consiste en juzgar a ciegas los pools de 5 consultas de prueba, unos 200 pares (alrededor de 1,7 h), entre el 16 y el 17 de noviembre. Es la única medida de acuerdo entre personas que admite el estudio piloto (sección 6 del protocolo). Si acepta, le pido que no abra los rankings ni los pools del repositorio, para que su juicio también sea ciego.
4. **Revisar las decisiones de diseño que tomé desde la auditoría.** Están listadas en la sección 11 del informe de avance; las que más pesan en los resultados son:
   - M3 no usa el color ni `motivo_principal`.
   - M0 excluye la descripción de MET, que es una plantilla de metadatos.
   - Los grupos se forman con la regla «unir ante la duda».
   - M2 corre en CPU.
5. **Orientarme sobre la rúbrica de Seminario II.** La estructura del informe sigue su propuesta del informe 11, pero no tengo una rúbrica vigente.

## Orden de lectura

| # | Documento | Contenido | Tiempo |
|---:|---|---|---:|
| 1 | [`informe_avance.md`](informe_avance.md) | Estado del corpus, la anotación, el protocolo y los sistemas; calendario, riesgos y decisiones | 20 min |
| 2 | [`matriz_respuesta_auditoria.md`](matriz_respuesta_auditoria.md) | Cada observación de la auditoría con su acción, evidencia y estado | 15 min |
| 3 | [`../protocolo_experimental_v2.md`](../protocolo_experimental_v2.md) | Protocolo para aprobar: hipótesis, galería, tareas, sistemas, particiones, juicios, métricas y criterios de suspensión | 30 min |
| 4 | [`../especificacion_m3.md`](../especificacion_m3.md) | Descriptor estructural M3: definiciones, propiedades y pruebas | 15 min |
| 5 | [`../protocolo_anotacion_v2.md`](../protocolo_anotacion_v2.md) | Anotación estructural v2: capas, bandas, estados y acuerdo intra-anotador | 10 min |
| 6 | [`../plan_cierre_tesis.md`](../plan_cierre_tesis.md) | Plan de cierre y su seguimiento | 10 min |

Los informes que genera el flujo, en `outputs/reports/`, sirven de evidencia y están enlazados desde la matriz.

## Cómo reproducirlo

```bash
git clone https://github.com/hsancheza90-art/uni-cc-base-multimodal-textiles-andinos
cd uni-cc-base-multimodal-textiles-andinos
python -m venv .venv && .venv/Scripts/activate      # en Linux/macOS: source .venv/bin/activate
pip install -r requirements-dev.txt
python -m src.flujo     # 23 pasos, sin red: regenera las salidas y verifica los conteos
pytest                  # 350 pruebas: cada salida regenerada coincide con la versionada
```

Cada commit desde la auditoría se verificó así en un clon limpio, sin torch. Los embeddings de M2 son un insumo versionado: recalcularlos exige `requirements-modelos.txt` y las copias de evaluación locales.

Quedo atento a sus observaciones.

Henry Sánchez Alvarado
