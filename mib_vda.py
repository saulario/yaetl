import configparser
import datetime
import decimal
import logging
import os
import sys
import traceback

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model import gt
from model import mtb
from model import plus_core
from model import plus_site


YAETL_HOME = ("%s/yaetl" % os.path.expanduser("~"))
YAETL_CONFIG = ("%s/etc/yaetl.config" % YAETL_HOME)
YAETL_LOG = ("%s/log/%s.log" %
             (YAETL_HOME, os.path.basename(__file__).split(".")[0]))
logging.basicConfig(level=logging.INFO, filename=YAETL_LOG,
                    format="%(asctime)s %(levelname)s %(module)s.%(funcName)s %(message)s")
log = logging.getLogger(__name__)

class Context():
    pass




    


def round_int(valor):
    d = decimal.Decimal(valor)
    return int(d.to_integral(rounding = decimal.ROUND_HALF_UP))


def cargar_vdas(context):
    return context.mtb_ses.query(mtb.Vda4921TransportIdentific,
                                 mtb.Vda4921FwdAgentDatum) \
            .filter(mtb.Vda4921TransportIdentific.bordero.like("ES3C%")) \
            .join(mtb.Vda4921FwdAgentDatum) \
            .all()

def procesar_vda(context, vda):
    
    
    log.info("     (%s) " % vda[0].bordero.strip())
            
def procesar_vdas(context):
    context.vdas = cargar_vdas(context)
    for vda in context.vdas:
        procesar_vda(context, vda)       
            
if __name__ == "__main__":
    """
    Main module
    """
    log.info("=====> Inicio (%s)" % os.getpid())
    retval = 0
    
    logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)

    context = Context()
    context.from_date = datetime.datetime(2018, 9, 1)
    context.to_date = context.from_date + datetime.timedelta(days = 29)

    try:
        cp = configparser.ConfigParser()
        cp.read(YAETL_CONFIG)
        
        os.environ["NLS_LANG"] = cp.get("GT","nls_lang")
        
        e1 = create_engine(cp.get("GT","uri"), echo=False)
        S1 = sessionmaker(bind=e1)
        context.gt_ses = S1()
               
        e2 = create_engine(cp.get("MTB","uri"), echo=False)
        S2 = sessionmaker(bind=e2)
        context.mtb_ses = S2()
        
        e3 = create_engine(cp.get("PLUS","core"), echo=False)
        S3 = sessionmaker(bind=e3)
        context.core_ses = S3()    
        
        e4 = create_engine(cp.get("PLUS","site1"), echo=False)
        S4 = sessionmaker(bind=e4)
        context.site1_ses = S4() 

        e5 = create_engine(cp.get("PLUS","site3"), echo=False)
        S5 = sessionmaker(bind=e5)
        context.site3_ses = S5()         

        procesar_vdas(context)

    except Exception as e:
        log.error(e)
        log.error(traceback.format_tb(sys.exc_info()[2]))
        retval = 1
    finally:
        context.site3_ses.close()
        context.site1_ses.close()
        context.core_ses.close()
        context.mtb_ses.close()
        context.gt_ses.close()
        
    log.info("<===== Fin (%s)" % os.getpid())
    sys.exit(retval)


