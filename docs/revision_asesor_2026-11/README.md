# Revisión para el asesor: avance de la segunda parte de la tesis

| | |
|---|---|
| Para | César Lara Ávila, asesor |
| De | Henry Sánchez Alvarado |
| Tesis | «Estructuras combinatorias y representación multimodal en textiles andinos», Maestría en Ciencias de la Computación, UNI |
| Fecha | 6 de noviembre de 2026 |
| Repositorio | https://github.com/hsancheza90-art/uni-cc-base-multimodal-textiles-andinos, rama `main` |
| Corpus de referencia | Etiqueta `corpus-met-cma-aic-v2.0` |
| Responde a | Auditoría del 20 de octubre de 2026, versionada en [`docs/auditoria_2026-10-20/`](../auditoria_2026-10-20/) |

Estimado profesor:

Le hago llegar el avance de la segunda parte de la tesis, desarrollado a partir de su auditoría del 20 de octubre. El trabajo se ha organizado según el plan de cierre al 22 de noviembre (`docs/plan_cierre_tesis.md`), que ordena sus observaciones en cuatro semanas. El estado de cada observación figura en la matriz de respuesta adjunta.

En síntesis, el corpus v2 quedó cerrado y consolidado, con sus grupos de piezas relacionadas, y el experimento está preparado hasta la etapa de los juicios de relevancia. Hasta la fecha no se ha ejecutado ningún sistema sobre las consultas de prueba, de modo que el diseño puede aprobarse o corregirse sin que ningún resultado lo condicione.

## Actualización al 13 de noviembre de 2026

Esta carta se redactó el 6 de noviembre y se conserva como se envió. Desde entonces se recibió el informe integrado del 8 de noviembre, versionado en [`docs/informe_integrado_2026-11-08/`](../informe_integrado_2026-11-08/), y el trabajo avanzó en cuatro frentes: la re-anotación ciega del lote 1 y su informe de estabilidad, los 345 juicios de desarrollo, la revisión bibliográfica de alcance y el código de evaluación y de fusión. El protocolo está ahora en la versión 0.6.1 y sigue pendiente de aprobación.

La respuesta al informe integrado se organiza en cinco documentos:

| # | Documento | Contenido | Punto del informe |
|---:|---|---|---|
| 1 | [Matriz de respuesta al informe integrado](matriz_respuesta_informe_integrado.md) | Cada inciso con su acción, su evidencia, su estado y lo que falta. Termina con lo que se solicita al asesor | 1 a 13 |
| 2 | [Inventario del estado del proyecto](inventario_estado.md) | Versiones, unidades, sistemas, datos humanos y pendientes, con archivos y commits | 1 |
| 3 | [Problema, objetivos, hipótesis y alcance](problema_hipotesis_alcance.md) | Propuesta de redacción, con la correspondencia entre cada hipótesis y su prueba | 2 |
| 4 | [Formalización matemática](formalizacion_matematica.md) | Definiciones, propiedades demostradas o verificadas y correspondencia entre fórmula, código y atributo | 9 |
| 5 | [Amenazas a la validez](amenazas_validez.md) | Por tipo de validez, con la mitigación y la limitación que subsiste | 11.e |

La [matriz de respuesta a la auditoría](matriz_respuesta_auditoria.md) se actualizó a la misma fecha.

Dos asuntos requieren su atención antes de continuar. El primero es una reserva sobre los juicios de desarrollo: comparados con la anotación, no puede afirmarse que midan similitud estructural (sección 2 de las amenazas a la validez). El segundo es la regla de decisión de H1: el protocolo propone decidir por permutación pareada y reservar el bootstrap para el intervalo, a diferencia de lo que indica su informe (decisión R01).

## Lo que le solicito

1. **La aprobación del protocolo experimental** (`docs/protocolo_experimental_v2.md`, versión 0.5), o sus observaciones para corregirlo. Una vez aprobado, el protocolo se congela y cualquier cambio posterior queda registrado en su historial antes de abrir el test.
2. **La ratificación de las decisiones del plan que figuran como propuestas:**
   - D2: el puntaje de aptitud se presenta como apoyo exploratorio de la curación y se rotula como validación de desarrollo.
   - D4: la galería del experimento es el núcleo de 150 piezas, agrupadas.
   - D5: el umbral práctico es ΔnDCG@10 = 0,03, con bootstrap pareado de 10 000 réplicas.
   - D7: la integración continua se pospone hasta después del 22 de noviembre. La auditoría ya está versionada en el repositorio.
3. **Su participación en el doble juicio parcial**, si le es posible. Consistiría en juzgar a ciegas los candidatos de 5 consultas de prueba, unos 200 pares (alrededor de una hora y tres cuartos), entre el 16 y el 17 de noviembre. Es la única medida de acuerdo entre dos personas que admite este estudio piloto (sección 6 del protocolo). Si acepta, le pediría no abrir los rankings ni los archivos de candidatos del repositorio, para que su juicio sea también ciego.
4. **Su opinión sobre las decisiones de diseño tomadas desde la auditoría.** Las enumera la sección 11 del informe de avance. Las que más inciden en los resultados son cuatro:
   - M3 no utiliza el color ni el motivo principal.
   - M0 excluye la descripción de MET, que es una plantilla generada a partir de los metadatos.
   - Los grupos siguen la regla de unir los pares dudosos.
   - M2 se ejecuta en CPU.
5. **La confirmación de la versión vigente de su auditoría.** Al versionarla comprobé que nueve de sus informes no coinciden con las sumas de su `SHA256SUMS.txt`. La copia que recibí está intacta, así que es probable que esos informes se editaran después de calcular las sumas ([`NOTA_VERSIONADO.md`](../auditoria_2026-10-20/NOTA_VERSIONADO.md)).
6. **Su orientación sobre la rúbrica de Seminario II.** El informe seguirá la estructura que usted propuso en el informe 11, pero no dispongo de una rúbrica vigente.

## Orden de lectura sugerido

| # | Documento | Contenido | Tiempo aproximado |
|---:|---|---|---:|
| 1 | [Informe de avance](informe_avance.md) | Estado del corpus, la anotación, el protocolo y los sistemas; calendario, riesgos y decisiones | 20 min |
| 2 | [Matriz de respuesta a la auditoría](matriz_respuesta_auditoria.md) | Cada observación con su acción, su evidencia y su estado | 15 min |
| 3 | [Protocolo experimental v2](../protocolo_experimental_v2.md) | Documento que se somete a aprobación | 30 min |
| 4 | [Especificación de M3](../especificacion_m3.md) | Descriptor estructural: definiciones, propiedades y pruebas | 15 min |
| 5 | [Protocolo de anotación v2](../protocolo_anotacion_v2.md) | Capas, bandas, estados y acuerdo intra-anotador | 10 min |
| 6 | [Plan de cierre](../plan_cierre_tesis.md) | Plan de las cuatro semanas y su seguimiento | 10 min |

Los informes que genera el flujo, en `outputs/reports/`, sirven de evidencia y están enlazados desde la matriz.

## Reproducción

El estado del repositorio puede reproducirse con estos comandos:

```bash
git clone https://github.com/hsancheza90-art/uni-cc-base-multimodal-textiles-andinos
cd uni-cc-base-multimodal-textiles-andinos
python -m venv .venv && .venv/Scripts/activate      # en Linux o macOS: source .venv/bin/activate
pip install -r requirements-dev.txt
python -m src.flujo     # 23 pasos, sin acceso a red: regenera las salidas y verifica los conteos
pytest                  # 429 pruebas: cada salida regenerada coincide con la versionada
```

Cada commit posterior a la auditoría se verificó de este modo en un clon limpio y sin las dependencias de M2. Los embeddings de M2 se guardan como insumo versionado. Recalcularlos requiere `requirements-modelos.txt` y las copias de evaluación de las imágenes, que no se versionan por su tamaño.

Quedo atento a sus observaciones.

Atentamente,

Henry Sánchez Alvarado
