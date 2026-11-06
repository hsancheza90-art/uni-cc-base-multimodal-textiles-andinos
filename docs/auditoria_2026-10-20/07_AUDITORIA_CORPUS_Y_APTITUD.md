### Auditoría del corpus y de la aptitud

#### Unidad experimental e integridad
id_global identifica un registro de una institución, no garantiza un objeto físico independiente. Para experimentar deben distinguirse object_group_id, record_id, image_id y duplicate_group_id. Agrupar fotografías del mismo objeto, imágenes compartidas y equivalencias confirmadas entre registros. La unidad de bootstrap de recuperación será la consulta/familia de consulta; la unidad de partición del corpus será el grupo de objeto.

Los 874 IDs compuestos son únicos en los tres workbooks. Hay 462 principales, 153 secundarios y 259 descartados. Estas decisiones no son etiquetas de relevancia ni anotaciones de motivos. El corpus está preparado para preparar un piloto técnico; no está listo como benchmark estructural.

#### Duplicación y disponibilidad
Según hashes archivados, v2 contiene 9 grupos de SHA-256 original repetido y 11 grupos de hash de copia repetido. No se observan grupos exactos cruzando museos en esos hashes; no se demuestra ausencia de duplicados perceptuales ni de objetos equivalentes entre fuentes. El manifiesto v1 tiene cuatro grupos con igualdad de píxeles; el consolidado ya incluye grupo_imagen_duplicada. Debe reutilizarse ese trabajo.

El análisis exploratorio dHash≤5 encuentra 19 pares candidatos v1. Un dHash cercano es indicio, no identidad; la selección del umbral5 en esta auditoría no redefine las decisiones curatoriales. Revisar visualmente los pares, asociar varias vistas y almacenar la justificación de cada unión. Las fotografías originales no se descargaron en esta auditoría: la inspección visual completa está pendiente.

Cuatro grupos exactos de copias v2 cruzan folds actuales de calibración:
- AIC:85028 y AIC:195555.
- AIC:2097, AIC:223218, AIC:223219 y AIC:223220.
- AIC:85397 y AIC:90831.
- MET:308106 y MET:308036.

No es preciso que las etiquetas sean contradictorias para que exista dependencia. Estas coincidencias violan la independencia por imagen si se presentan como predicción de imágenes nuevas.

#### Procedencia de decisiones
MET: 109 revisores vacíos, 46 auto, 65 Henry Sánchez. CMA:95 vacíos,13 auto,38 Henry Sánchez. AIC:340 vacíos,168 auto. En total:544 sin nombre,227 auto,103 con nombre. Los orígenes históricos proporcionan más información que la columna revisor; ambos deben preservarse. No completar autoría retrospectivamente por inferencia.

Los criterios v2 excluyen plumaria y fechas de inicio posteriores a1532, y admiten fragmentos interpretables. Es una delimitación operacional del estudio, no un juicio sobre autenticidad o valor cultural. La selección por calidad, superficie amplia y fotografía en color cambia las distribuciones de conservación, técnica y museo. Conservar secundarios para robustez y reportar cobertura de selección por cada variable.

#### Qué implementa realmente el modelo
Las etiquetas se extraen de motivos libres del revisor (src/imagenes/motivos.py). Se usan 402 registros: AIC316, MET51 y CMA35. Clases:85 descarte_imagen,43 secundarios,85 principales y189 referencia. Para el contraste útil/resto son 274 positivos y128 negativos.

Hay regresiones logísticas L2 por atributo, estimadas mediante Newton; 21 variables incluyen titulo_fragmento, una señal textual. Por tanto, "estimado solo desde la imagen" es inexacto. La regresión ordinal ajusta pesos no negativos a probabilidades producidas por los componentes sobre sus propios datos de entrenamiento. Después se impone peso mínimo0,3 a referencia, se normalizan los pesos y se usa score0–100; los cortes ordinales aprendidos no se usan como probabilidades finales de clase.

Esto es un sistema supervisado de priorización con reglas y restricciones, no una probabilidad calibrada de aptitud universal. El ajuste L2 es razonable para una muestra pequeña, pero falta comprobar convergencia/estabilidad, ablación de variables, incertidumbre y efecto del apilamiento entrenado con predicciones in-sample.

#### Resultados reproducidos y límites

| Resultado del repositorio | Valor reproducido | Interpretación correcta |
|---|---:|---|
| AUC OOF útil/resto conjunta | 0,850 | Discriminación retrospectiva en mezcla de fuentes |
| AUC OOF AIC / MET / CMA | 0,907 / 0,759 / 0,829 | Folds contienen ejemplos de los tres museos |
| Colores / formas / completitud / referencia | 0,908 / 0,861 / 0,874 / 0,813 | Poblaciones etiquetadas distintas; no promediar como una tarea |
| Cortes descarte / principal / referencia | 34,9 / 69,7 / 84,6 | Ajustados en las mismas predicciones OOF usadas para el informe |
| Precisión de principal+referencia | 189/210=0,900 | Desarrollo, no validación independiente del umbral |
| Recall útil de principal+referencia | 189/274=0,690 | El 90% de precisión no significa recuperar 90% de útiles |
| Abstención en banda revisar | 149/402=37,1% | Debe informarse junto al desempeño |
| Útiles bajo descarte | 8/274=2,9% | Restricción ajustada sobre estos datos; no garantía poblacional |

La estandarización utiliza las 873 imágenes antes de dividir folds; también hay anclas de calidad calculadas globalmente. Es información de distribución de test incorporada a entrenamiento. Sería una elección transductiva declarada para catalogar un lote fijo, pero no respalda generalización inductiva a nuevos museos.

La configuración documenta decisiones de variables, pesos y umbrales tomadas tras observar CV. La selección de modelo no queda protegida por usar OOF una sola vez. Se necesita validación anidada o un test nuevo. No hay Brier/log-loss ni curvas de fiabilidad que permitan llamar "calibradas" a las probabilidades; "calibración" aquí incluye ajuste del sistema.

#### Evaluación auxiliar leave-one-museum-out ejecutada
Se reutilizó Ajuste, con hiperparámetros existentes fijos y estandarización calculada solo en registros etiquetados de los museos de entrenamiento. Se entrenaron tres modelos nuevos. No se modificó config/aptitud_modelo.json. Script y predicciones: evidencias/evaluate_transfer.py y predicciones_lomo.csv.

| Museo reservado | Train | Test | Pos./neg. | AUC LOMO | IC95% descriptivo |
|---|---:|---:|---|---:|---|
| AIC | 86 | 316 | 225/91 | 0,563 | 0,490–0,630 |
| MET | 351 | 51 | 33/18 | 0,556 | 0,362–0,727 |
| CMA | 367 | 35 | 16/19 | 0,931 | 0,836–0,993 |

IC:2000 bootstrap estratificados por clase, semilla20261020, remuestreo de registros sobre predicciones fijas. No agrupa duplicados, no reajusta modelos y no incluye incertidumbre de selección/entrenamiento; puede ser demasiado estrecho. No usarlo como intervalo confirmatorio.

El ensayo muestra sensibilidad importante a fuente y tamaño de entrenamiento. No demuestra que CMA sea universalmente fácil ni permite atribuir causalmente la diferencia a museo: cambian distribución de clases, criterio de revisión y volumen de train. Los hiperparámetros y anclas heredados se eligieron previamente con acceso a datos de las tres fuentes; por eso este LOMO es diagnóstico retrospectivo, NO evaluación externa prospectiva. El alto valor de CMA con 35 casos no compensa la incertidumbre de los otros resultados.

#### Validación ciega histórica
40 casos MET/CMA; el resultado histórico de exactitud≈0,83 y kappa≈0,56 se refiere a30 decisiones no abstinentes, cobertura75%. Quince de esos40 IDs aparecen ahora en calibración. Debe conservarse como etapa histórica del desarrollo, sin reutilizar la etiqueta "test independiente" para el modelo actual. docs/notas_para_tesis.md ya reconoce límites y reutilización: la corrección consiste en hacer consistentes todas las tablas y afirmaciones, no en ocultar esa autocrítica.

#### Evaluación requerida
Congelar versión de criterio y convertir motivos en etiquetas explícitas por atributo; conservar texto original y enlace de trazabilidad. Dos anotadores independientes revisan un piloto equilibrado; la adjudicación sucede después de medir acuerdo. Medir también cobertura de abstención y desacuerdos del parser de motivos.

Para evaluación interna: grupos de objeto, outer CV agrupada; scaler, anclas, selección de variables, componentes y umbrales dentro del train externo. Si se aprende fusión/apilamiento, producir predicciones internas fuera de fold para entrenar esa capa. Mostrar baseline de regla simple y regresión útil/resto directa, así como ablación sin titulo_fragmento y sin señales de tamaño/estilo institucional.

Para evaluación externa: nueva muestra decidida después de congelar sistema, preferentemente una fuente no usada y con casos difíciles, sin reutilizar revisión asistida por score. Si solo hay museos actuales, reservar objetos nuevos y describirlo como generalización temporal/institucional limitada. Calcular IC agrupados, precisión-recall, ROC-AUC, balanced accuracy, confusión, cobertura y sensibilidad del corte. Brier/log-loss solo sobre salidas probabilísticas interpretables; no sobre score ordinal como si fuese probabilidad.

#### Anotación estructural y patrimonio
La guía y vocabulario constituyen un buen punto de partida, pero no se observan anotaciones estructurales completadas. Incorporar regiones, secuencias y observabilidad; no bastan categorías globales para probar relaciones. Para atributos nominales usar acuerdo bruto y kappa/alpha con prevalencias; para ordinales kappa ponderada; multietiqueta, Jaccard/F1 por conjunto y acuerdo binario por etiqueta; conteos, error absoluto y medida de concordancia adecuada. Reportar número de casos y IC, no adjetivos fijos de kappa como certificación.

Un piloto de 30–40 objetos doblemente anotados puede depurar instrucciones; no garantiza precisión final ni representatividad. Criterio orientativo:≥0,80 acuerdo bruto en atributos críticos y revisión de etiquetas con acuerdo débil; fijar criterio final según consecuencias y prevalencia.

FAIR: IDs persistentes, diccionario, procedencia, versiones, formatos abiertos y licencia por recurso. CARE: documentar beneficios, autoridad y contexto indígena; consulta especializada cuando interpretación cultural lo requiera; registrar términos sensibles y límites de reutilización. No se ha obtenido consentimiento comunitario ni debe presumirse por CC0. Mantener incertidumbres curatoriales; no borrar "atribuido", "posiblemente" o intervalos para facilitar el modelo.

