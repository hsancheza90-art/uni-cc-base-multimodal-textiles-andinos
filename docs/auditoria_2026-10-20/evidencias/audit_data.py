import sys,csv,json,hashlib,subprocess,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; R=ROOT/'repo'; sys.path.insert(0,str(R))
from src.utils.fuentes import FUENTES
from src.utils.libros import leer_hoja
from src.utils.archivos import leer_csv,indexar
from src.utils.config import leer_config_aptitud
from src.imagenes.calibrar_aptitud import registros_calibracion
out={}; inv=[]
for p in sorted(R.rglob('*')):
 if p.is_file() and '.git' not in p.parts and '__pycache__' not in p.parts and '.pytest_cache' not in p.parts:
  inv.append({'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
with (ROOT/'auditoria/evidencias/inventario.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=inv[0]);w.writeheader();w.writerows(inv)
for name,source in FUENTES.items():
 rows=leer_hoja(R/source.workbook,source.hoja,clave='id_fuente')
 out[name]={'filas':len(rows),'decisiones':dict(collections.Counter(x['corpus_final'] for x in rows)),'origenes':dict(collections.Counter(x.get('origen_curacion') for x in rows)),'revisores':dict(collections.Counter(x.get('revisor') for x in rows)),'ids_unicos':len(set(x['id_fuente'] for x in rows))}
for rel in ['data/metadata/imagenes_evaluacion_manifiesto_v2.csv','data/metadata/imagenes_manifiesto_met_cma_v1.csv','data/processed/corpus_textiles_andinos_met_cma_v1_consolidado.csv']:
 rows=leer_csv(R/rel); d={'n':len(rows),'columnas':list(rows[0])};
 for col in ['estado_descarga','estado_anotacion','fuente','decision_curacion_final']:
  if col in rows[0]:d[col]=dict(collections.Counter(x[col] for x in rows))
 for col in ['sha256_original','sha256_copia','imagen_sha256','imagen_sha256_pixeles','url_descargada']:
  if col in rows[0]:
   groups=collections.defaultdict(list)
   for x in rows:
    if x[col]:groups[x[col]].append(x['id_global'])
   d[col+'_duplicados']=[v for v in groups.values() if len(v)>1]
 if 'imagen_dhash' in rows[0]:
  pairs=[]
  for i,x in enumerate(rows):
   if not x['imagen_dhash']:continue
   for y in rows[i+1:]:
    if y['imagen_dhash']:
     dist=(int(x['imagen_dhash'],16)^int(y['imagen_dhash'],16)).bit_count()
     if dist<=5:pairs.append([x['id_global'],y['id_global'],dist])
  d['dhash_candidatos_hasta_5']=pairs
 out[rel]=d
frozen=[]
for p in (R/'data/metadata/v1_congelado').glob('*.csv'):
 old=subprocess.check_output(['git','-C',str(R),'show','corpus-met-cma-v1.2:data/metadata/'+p.name]);frozen.append({'file':p.name,'identico_tag':old==p.read_bytes()})
out['entradas_congeladas']=frozen
med=indexar(leer_csv(R/'data/metadata/aptitud_medidas_v2.csv'),'id_global');reg=registros_calibracion(R,med,leer_config_aptitud(R));out['calibracion_n']=len(reg)
from openpyxl import load_workbook
wb=load_workbook(R/'data/metadata/validacion_met_cma_v2.xlsx',read_only=True,data_only=True);out['validacion_hojas']=wb.sheetnames
for sheet in wb:
 rows=list(sheet.values)
 if rows and 'id_global' in rows[0]:
  k=rows[0].index('id_global');ids={str(x[k]) for x in rows[1:] if x[k]};out['validacion_solapamiento']={'n_validacion':len(ids),'n_en_calibracion':len(ids&{x['id_global'] for x in reg}),'ids':sorted(ids&{x['id_global'] for x in reg})}
wb.close()
(ROOT/'auditoria/evidencias/auditoria_datos.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print(json.dumps(out,ensure_ascii=False,indent=2))
