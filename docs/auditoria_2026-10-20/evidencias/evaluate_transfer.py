import sys,json,csv,collections
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2]; R=ROOT/'repo';sys.path.insert(0,str(R))
from src.imagenes.calibrar_aptitud import Ajuste,estandarizacion,registros_calibracion,medidas_atributo,pliegues
from src.utils.archivos import leer_csv,indexar
from src.utils.config import leer_config_aptitud
from src.utils.metricas import auc
config=leer_config_aptitud(R);measures=indexar(leer_csv(R/'data/metadata/aptitud_medidas_v2.csv'),'id_global');records=registros_calibracion(R,measures,config)
names={m for a in config['atributos'] for m in medidas_atributo(config,a)}
manifest=indexar(leer_csv(R/'data/metadata/imagenes_evaluacion_manifiesto_v2.csv'),'id_global')
folds=pliegues([r['fuente']+r['clase'] for r in records]);groups=collections.defaultdict(list)
for r,f in zip(records,folds):groups[manifest[r['id_global']]['sha256_copia']].append((r['id_global'],int(f),r['clase']))
leaks=[g for k,g in groups.items() if k and len({v[1] for v in g})>1]
results=[]; predictions=[]
for museum in ['AIC','MET','CMA']:
 train=[r for r in records if r['fuente']!=museum];test=[r for r in records if r['fuente']==museum]
 std=estandarizacion([measures[r['id_global']] for r in train],names); fit=Ajuste(config,measures,train,std)
 scores=np.array([fit.puntaje(r['id_global']) for r in test]);y=np.array([r['clase'] in ('principal','referencia') for r in test]);pos=scores[y];neg=scores[~y]
 rng=np.random.default_rng(20261020);boots=[]
 # IC descriptivo condicional: remuestreo estratificado de registros, no cubre incertidumbre del entrenamiento.
 for _ in range(2000):boots.append(auc(rng.choice(pos,len(pos)).tolist(),rng.choice(neg,len(neg)).tolist()))
 results.append({'museo_prueba':museum,'n_train':len(train),'n_test':len(test),'positivos':int(y.sum()),'negativos':int((~y).sum()),'auc':auc(pos.tolist(),neg.tolist()),'ci95_registros':np.quantile(boots,[.025,.975]).tolist()})
 for r,s in zip(test,scores):predictions.append({'id_global':r['id_global'],'fuente':museum,'clase':r['clase'],'score':float(s)})
 print(results[-1],flush=True)
(ROOT/'auditoria/evidencias/transferencia.json').write_text(json.dumps({'metodo':'LOMO; estandarizacion entrenada solo en museos de entrenamiento; parametros originales fijos; no es validacion externa prospectiva','fugas_duplicados_cv_original':leaks,'resultados':results},indent=2))
with (ROOT/'auditoria/evidencias/predicciones_lomo.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=predictions[0]);w.writeheader();w.writerows(predictions)
