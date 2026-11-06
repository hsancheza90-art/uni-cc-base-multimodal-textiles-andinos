import sys,json,tempfile,shutil,copy,contextlib,io
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]; R=ROOT/'repo';sys.path.insert(0,str(R))
from src.metadata import apply_met_review_v2 as met,apply_cma_review_v2 as cma
from src.utils.fuentes import FUENTES
from src.utils.libros import leer_hoja
from src.imagenes import medidas,descargar_evaluacion
from src.utils.config import leer_config_aptitud
from src.anotacion.aplicar_anotaciones import normalizar_fila
from src.utils.vocabulario import leer_vocabulario
out={}
with tempfile.TemporaryDirectory() as td:
 root=Path(td)
 row=leer_hoja(R/FUENTES['MET'].workbook,FUENTES['MET'].hoja,clave='id_fuente')[0];row['corpus_final']='valor_invalido'
 with patch.object(met,'leer_hoja',return_value=[row]),contextlib.redirect_stdout(io.StringIO()):code=met.aplicar_revision(root,FUENTES['MET'])
 out['decision_invalida_met']={'esperado':'retorno 1 conforme docstring','obtenido':code,'pendiente_exportado': (root/FUENTES['MET'].pendientes).exists()}
 row=leer_hoja(R/FUENTES['CMA'].workbook,FUENTES['CMA'].hoja,clave='id_fuente')[0]
 try:cma.validar([row,row]);out['cma_duplicado']='aceptado sin excepcion'
 except Exception as e:out['cma_duplicado']=repr(e)
 with patch.object(descargar_evaluacion,'candidatos_evaluacion',return_value=[{'fuente':'AIC','id_fuente':'x','id_global':'AIC:x','urls':[]}]),patch.object(descargar_evaluacion,'descargar',return_value={'fuente':'AIC','id_fuente':'x','id_global':'AIC:x','estado_descarga':'error','error':'fallo controlado'}),patch.object(descargar_evaluacion.time,'sleep'),contextlib.redirect_stdout(io.StringIO()):
  out['descarga_error_retorno']=descargar_evaluacion.ejecutar(root,['AIC'],None)
 sample={'id_global':'MET:test','fecha_anotacion':'2026-99-99','anotador':'auditoria'}
 out['fecha_invalida_errores']=normalizar_fila(sample,leer_vocabulario(R))[1]
 # No se necesitan imagenes: cache reutilizada antes de medir.
 testroot=root/'cache';shutil.copytree(R/'data',testroot/'data');shutil.copytree(R/'config',testroot/'config')
 cfg=leer_config_aptitud(R);cfg['segmentacion']['nitidez_lado_textil']=123
 with patch.object(medidas,'medir_imagen',side_effect=AssertionError('medida recalculada')) as measuring_mock,contextlib.redirect_stdout(io.StringIO()):
  code=medidas.medir(testroot,cfg,False)
 out['cache_config_alterada']={'retorno':code,'filas_identicas':medidas.leer_csv(testroot/medidas.MEDIDAS)==medidas.leer_csv(R/medidas.MEDIDAS), 'llamadas_medicion':measuring_mock.call_count,'parametro_cambiado':'nitidez_lado_textil: 600 -> 123'}
(ROOT/'auditoria/evidencias/defectos_reproducidos.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
