### Plan de seis semanas
Escenario inicial desde la aprobación del alcance, sin atribuirlo a calendario oficial UNI. Supone un investigador con 20-25 horas semanales, acceso a dos personas capaces de juzgar estructura y capacidad de ejecutar inferencia congelada. El cuello de botella es la anotación, no el entrenamiento. Si esas condiciones faltan, ampliar calendario o reducir galería/consultas antes del test, conservando datos reales.

#### Programa y puertas de avance

| Semana | Trabajo y responsable funcional | Producto | Criterio de salida |
|---|---|---|---|
| 1 | Investigador: freeze v2, grupos, verificación de fotos, SW01-03; investigador+asesor: protocolo y alcance | Snapshot, grupos, protocolo y contratos | Sin fugas por grupos conocidas, datos y decisiones trazables |
| 2 | Dos anotadores: piloto30-40 y ajuste de guía; investigador: MAT01 y M0/M1 | Guía cerrada, acuerdo piloto, descriptor especificado | Atributos observables y reglas de desconocido claras; no quedan desacuerdos conceptuales críticos |
| 3 | Investigador: M2/M3/M4 y control sin orden; expertos: anotación y qrels de desarrollo | Runs de desarrollo, estimación de esfuerzo/varianza | Pesos/modelos congelados; n de test decidido; explicación reproduce score |
| 4 | Expertos: qrels test ciegos y adjudicación; investigador: validación agrupada de aptitud y congelación experimental | Benchmark y protocolo final; test sellado hasta cierre de juicios | Integridad de grupos y juicios comprobada; ningún tuning con test |
| 5 | Investigador: ejecutar test, ablaciones, IC y robustez; expertos: explicación/errores | Tablas, diferencias pareadas, casos de error | Todos los comparadores aplicables, resultados negativos incluidos |
| 6 | Investigador: informeII, trazabilidad y paquete; tercero/asesor: reproducción y revisión | Documento académico y release candidato | Reproducción, conclusiones sustentadas, limitaciones explícitas |

La actualización bibliográfica BIB01 se distribuye entre semanas1-3. Las correcciones menores de software se incorporan sin desplazar anotación. No se publicará ni modificará el repositorio desde esta auditoría.

#### Presupuesto y alternativas
La propuesta de 120 objetos y 40 consultas implica 4800 juicios por revisor si se evalúa exhaustivamente, además de anotación estructural. Medir tiempo por juicio en semana2 y recalcular recursos. Con dos revisores y30 segundos por juicio serían 80 horas de juicio total, sin contar adjudicación, una estimación condicional, no tiempo medido. El plan solo es factible con dedicación de los expertos o pooling explícito con límites metodológicos.

Si en semana2 falta capacidad, reducir galería a un subconjunto estratificado real y reformular el estudio como piloto. No sustituir el benchmark por un conjunto sintético diminuto ni afirmar equivalencia de evidencia. Si el acuerdo es bajo, reducir atributos ambiguos antes de ampliar muestra.

Si en semana3 no hay GPU, usar checkpoint compacto congelado y CPU, registrar tiempos. Si M4 no mejora, continuar el análisis y reportar cuándo estructura ayuda o no; no cambiar la hipótesis después de ver test.

#### Horizontes
H1, SeminarioII: benchmark defendible, descriptor mínimo, M0-M4, ablación de orden y evaluación reproducible.
H2, tesis completa: mayor cobertura, evaluación externa y modelo visual alternativo, grafo si se justifica.
H3, publicación: contribución delimitada y replicación con nueva fuente/usuarios; estudio de costos, incertidumbre y gobernanza más amplio. No prometer aceptación editorial ni ampliar H1 para "incluir toda la IA".

#### Condiciones de suspensión del test
No abrir test si persisten grupos duplicados divididos, qrels derivados automáticamente del descriptor, cambios de guía sin registrar, pesos ajustados con prueba o imágenes no verificadas. La suspensión protege el experimento final, no impide preparar código o anotar desarrollo.

