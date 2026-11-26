# Relación de cambios: informe de revisión del 25 de noviembre de 2026

Respuesta al «Informe de revisión Proyecto de Tesis 2» (dictamen favorable con correcciones documentales C01, C02 y C03), sobre el commit `d5d6a82`. Versión corregida: commit `9aaa8bc`, archivos `MCC702_informe_seminario_II_2026-11-27.docx` y `.pdf`.

No se modificaron rankings, juicios, pesos, resultados ni archivos sellados. `python -m src.experimento.ejecucion_prueba --comprobar` y la verificación de las sumas del manifiesto siguen coincidiendo, y `git diff --stat d5d6a82..9aaa8bc` solo muestra cambios en `docs/`.

## C01. Coherencia de la declaración de custodia

| Ubicación | Antes | Ahora |
|---|---|---|
| Sección 7.12, párrafos 2 y 3 | «La corrida no tuvo fallos, suspensiones ni desviaciones del protocolo»; las etiquetas acreditan cada estado | No se registraron fallos ni suspensiones; se declara la desviación: las huellas se enviaron juntas el 24 de noviembre, después de la evaluación. La verificación no detectó discrepancias, pero el envío tardío limita la constancia externa contemporánea de la secuencia |
| Sección 8.1 | «La única desviación afectó a la custodia y no a los datos» | Misma redacción que 7.12, con remisión al anexo B |
| Anexo B, B.2 y B.3 | Envío pendiente; «sin efecto sobre los datos»; la secuencia «quedó fijada» por las etiquetas | Envío conjunto del 24 de noviembre, declarado como desviación; la coincidencia de sumas acredita la integridad actual, no toda la historia temporal; las etiquetas son una constancia interna y no sustituyen el envío por etapas |
| Sección 10.3, contribución 4 | «custodia verificable» | «custodia documentada y una desviación declarada en el envío de las huellas» |
| Sección 11.2 | — | Nuevo párrafo «Custodia de la evaluación final» con el alcance de la verificación y de la independencia del juicio |
| `docs/registro_custodia.md` | Fila de desviación del 24 de noviembre | Se conserva la fila y se añade al final una aclaración fechada (26 de noviembre) con el mismo alcance |

## C02. Correspondencia entre evidencia y conclusiones

| Ubicación | Antes | Ahora |
|---|---|---|
| Resumen y sección 1.5 | Retirar la estructura redujo el resultado; el orden no mejoró al inventario | La retirada de la estructura se presenta como análisis exploratorio; «no se detectó una mejora atribuible al orden de las bandas» |
| Sección 8.5 | «La estructura aporta dentro de la fusión»; «el orden no aporta»; el control negativo «confirma» | Retirar M3 es, entre las ablaciones realizadas, la que más reduce el resultado (no se evaluó retirar M2); no se detectó una mejora atribuible al orden (IC 95 %: −0,009 a 0,001); el control negativo aporta evidencia exploratoria compatible, con una sola permutación |
| Secciones 8.7 y 8.10 | «Indicio»; la estructura «es la parte que más pesa» | «Compatible con»; síntesis que separa la comparación confirmatoria de las exploratorias |
| Capítulo 9 (introducción, 9.1, 9.3, 9.6) | «Confirma», «descarta», «la ganancia depende», «cuatro factores explican», «el orden no añadió utilidad» | «Compatible con», «evidencia exploratoria contra», «sugiere», «pueden contribuir a explicarlo», «no se detectó una mejora atribuible al orden»; el aporte de cada bloque por separado no se midió |
| Sección 9.7 | Composición, borde, simetría, repetición y motivos como los atributos que más aportaron y los más fáciles de registrar | Se retira esa clasificación: el aporte individual de cada atributo y el esfuerzo de anotarlo no se midieron y pasan a trabajo futuro |
| Sección 10.1, OE4 | La estructura es el componente cuya retirada más reduce; el control «confirma» | Retirar la estructura redujo más que retirar el texto, entre las ablaciones realizadas; no se evaluó retirar M2; control exploratorio de una sola permutación |
| Sección 10.2 | La mejora procede de los cinco atributos; el orden no aportó | Redacción orientativa del asesor: en este corpus y bajo los juicios del evaluador, M4 superó a M2; las ablaciones exploratorias sugieren una contribución de la estructura; no se detectó una mejora adicional atribuible al orden; la descomposición fue fiel en el nivel de sus componentes |
| Secciones 10.3 y 10.4 | Contribución 5 y recomendación por aporte y facilidad de los atributos | Evidencia de alcance piloto con ablaciones exploratorias; la recomendación ya no prioriza atributos; medir su aporte y costo pasa a las prioridades de investigación |
| Capítulos 2, 5, 7 y 11 (formulaciones equivalentes) | «Permite afirmar que la estructura no aporta»; «aísla»; «descarta» | Se distingue un resultado no significativo de la ausencia de efecto; «separa»; control negativo descriptivo |

## C03. Presentación de la versión definitiva

| Aspecto | Antes | Ahora |
|---|---|---|
| Índice | Instrucción «clic derecho… Actualizar campo» | Índice generado hasta el nivel 3, con paginación real, actualizado con Word antes de exportar a PDF |
| Ecuaciones | Las ecuaciones numeradas perdían su número en el Word | Las 25 ecuaciones numeradas (5.1–5.21, 7.1, C.1–C.3) conservan su número |
| Paginación | Arábiga desde la portada | Romanos en los preliminares (portada sin número) y arábigos desde el capítulo 1, como pide la guía |
| Referencias | Una lista APA por capítulo | Formato IEEE numérico con una sola lista final de 49 referencias, como pide la guía de la UNI |
| Tablas | Sin bordes | Formato de tres líneas |
| Portada | Sin el nombre del director | Bloque del jurado y nombre del director de la Unidad de Posgrado, según la plantilla del curso |
| Figuras y cuadros | Figuras 4.1 y 4.2 en orden inverso; varios cuadros sin cita en el texto | Numeración en orden de aparición; todos los cuadros y figuras citados |
| Reproducibilidad | Plantilla en una carpeta temporal | Plantilla, filtro de ecuaciones y script de generación versionados en `docs/manuscrito/plantilla/` |

## Otras correcciones de coherencia

- Una sola versión de la estabilidad de la anotación en los capítulos 4, 9 y 10; significado de «juicios independientes de los sistemas» precisado en 2.3; principio 3 del capítulo 7 corregido (los juicios de desarrollo se revisaron con asistencia); amenaza A4 sin prometer una cobertura que no se informa; tolerancias de H3 precisadas en el Cuadro 8.8; explicación del Cuadro 8.4; porcentaje 39,7 % uniforme; 504 pruebas, de las que 503 se ejecutan y una se omite por diseño; términos de otros idiomas en cursiva.
- **Fe de erratas.** La anotación congelada de la pieza AIC:85278 no corresponde a su fotografía. No se corrigió, porque es un insumo sellado; se declara en la sección 11.2 con su alcance en los rankings sellados (entre los diez primeros de M3 en tres consultas y de M4 en una, siempre con grado 0) y en la decisión R42.
