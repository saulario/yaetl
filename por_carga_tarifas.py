import configparser
import datetime
import logging
import openpyxl as excel
import os
import sys
import traceback
import uuid

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model import gt


YAETL_HOME = ("%s/yaetl" % os.path.expanduser("~"))
YAETL_CONFIG = ("%s/etc/yaetl.config" % YAETL_HOME)
YAETL_LOG = ("%s/log/%s.log" %
             (YAETL_HOME, os.path.basename(__file__).split(".")[0]))
logging.basicConfig(level=logging.INFO, filename=YAETL_LOG,
                    format="%(asctime)s %(levelname)s %(module)s.%(funcName)s %(message)s")
log = logging.getLogger(__name__)

class Context():
    pass


def procesar_linea(context, limits, row):
    imp_maximo = 0
    for i in range(18, 4, -1):
        if i == 18:
            imp_maximo = row[i].value
            continue
        udesde = limits[i].value
        uhasta = limits[i+1].value - 0.01
        
        tc = gt.TarifasCliente()
        tc.ide = 1
        tc.cliente = 37084
        tc.fecha_aplicacion = datetime.datetime(2019, 1, 1, 0, 0, 0)
        tc.tipo = "T" if i < 8 else "U"
        tc.precio = row[i].value
        tc.remontable = "N"
        tc.req_vehiculo = "N"
        tc.moneda = "EUR"
        tc.maximo = 0 if tc.tipo == "T" else imp_maximo
        tc.desde = udesde
        tc.hasta = uhasta
        tc.posicion = context.referencia
        tc.referencia_cliente = row[0].value + ":" + row[1].value + ":" + row[4].value
        
        context.session.add(tc)
        context.session.commit()
        
        te1 = gt.TarifasClienteEtapa()
        te1.etapa = 1
        te1.tipo = "R"
        te1.direccion = 19210
        te1.tarifa = tc.id
        te1.provincia = "50"
        te1.pais = "ES"
        te1.poblacion = 22660
        context.session.add(te1)

        te99 = gt.TarifasClienteEtapa()
        te99.etapa = 99
        te99.tipo = "E"
        te99.direccion = 19210
        te99.tarifa = tc.id
        te99.provincia = "50"
        te99.pais = "ES"
        te99.poblacion = 22660
        context.session.add(te99)
        
        context.session.commit()
        
        imp_maximo = round(udesde * row[i].value / 100, 2)

def borrar_carga_previa(context, row):
    log.info("=====> Inicio (%s)" % row[0].value)
    context.referencia = row[0].value
    
    tces = context.session.query(gt.TarifasClienteEtapa) \
            .join(gt.TarifasClienteEtapa.tarifas_cliente) \
            .filter(gt.TarifasCliente.posicion == context.referencia) \
            .filter(gt.TarifasCliente.cliente == "37084")
    for tce in tces:
        log.info("       tarifa (%s)" % tce.tarifa)
        context.session.delete(tce)
    context.session.commit()
    
    tcs = context.session.query(gt.TarifasCliente) \
            .filter(gt.TarifasCliente.posicion == context.referencia) \
            .filter(gt.TarifasCliente.cliente == "37084") 
    for tc in tcs:
        log.info("       tarifa (%s)" % tc.id)
        tc.cliente = "25523"
        tc.fecha_aplicacion = datetime.datetime(2001, 1, 1, 0, 0, 0)
        tc.fecha_finalizacion = datetime.datetime(2001, 1, 2, 0, 0, 0)
        context.session.commit()
    
    log.info("<===== Fin")

def procesar_workbook(context, f):
    log.info("=====> Inicio (%s)" % f)
    
    wb = excel.load_workbook(filename = f, read_only = True)
    if (wb == None):
        log.info("<===== Saliendo sin datos")
        return
    
    ws = wb["TARIFA"]
    line = 0
    limits = None
    for row in ws.rows:
        line += 1
        if line == 1:
            borrar_carga_previa(context, row)
        if line == 2:
            limits = row
        if line < 4:
            continue
        procesar_linea(context, limits, row)
        
    wb.close()
    
    log.info("<===== Fin")

if __name__ == "__main__":
    """
    Main module
    """
    log.info("=====> Inicio (%s)" % os.getpid())
    retval = 0
    
    logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)

    context = Context()
    context.session = None

    try:
        cp = configparser.ConfigParser()
        cp.read(YAETL_CONFIG)
        
        os.environ["NLS_LANG"] = cp.get("GT","nls_lang")
        engine = create_engine(cp.get("GT","uri"), echo=False)

        Session = sessionmaker(bind=engine)
        context.session = Session()
               
        procesar_workbook(context, "/temp/pib/tarifas_4_5.xlsx")
        context.session.commit()

    except Exception as e:
        log.error(e)
        log.error(traceback.format_tb(sys.exc_info()[2]))
        retval = 1
        context.session.rollback()
    finally:
        context.session.close()

    log.info("<===== Fin (%s)" % os.getpid())
    sys.exit(retval)


