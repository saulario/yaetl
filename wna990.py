import configparser
import datetime
import logging
import os
import random
import sys

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

def nombre_fichero(pedido):
    cdn = 'SEGO_990_' + pedido + "_" \
            + datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S%f') \
            + ".edi"
    return cdn

def generar_isa(context, pedido, f):
    buffer = "ISA*00*" + "{:10}".format("") + "*00*" + "{:10}".format("") \
            + "*02*" + "{:15}".format("SEGO") \
            + "*01*" + "{:15}".format("067888030") \
            + "*" + context.fecha.strftime("%y%m%d") \
            + "*" + context.fecha.strftime("%H%M") \
            + "*U*00401" \
            + "*" + "{:0>9}".format(context.numero) \
            + "*0*P*:\n"
    f.write(buffer)
    
def generar_gs(context, pedido, f):
    buffer = "GS*GF*SEGO*CWNA" \
            + "*" + context.fecha.strftime("%Y%m%d") \
            + "*" + context.fecha.strftime("%H%M") \
            + "*" + str(context.numero) \
            + "*X*004010" \
            + "\n"     
    f.write(buffer)
    
    buffer = "ST*990*0001" \
            + "\n"     
    f.write(buffer)    
    
def generar_b1(context, pedido, f):
    buffer = "B1*SEGO" \
            + "*" + pedido.pedido_cliente \
            + "*" + context.fecha.strftime("%Y%m%d") \
            + "*A" \
            + "\n"     
    f.write(buffer)
    
def generar_n9(context, pedido, f):
    buffer = "N9*TN" \
            + "*" + pedido.fuente \
            + "\n"     
    f.write(buffer)
    
def generar_g62(context, pedido, f):
    buffer = "G62*69" \
            + "*" + context.fecha.strftime("%Y%m%d") \
            + "*U" \
            + "*" + context.fecha.strftime("%H%M") \
            + "*ET" \
            + "\n"     
    f.write(buffer)    
    
    buffer = "SE*5*0001" \
            + "\n"     
    f.write(buffer)    
    
    buffer = "GE*1" \
            + "*" + str(context.numero) \
            + "\n"     
    f.write(buffer)      

    buffer = "IEA*1" \
            + "*" + "{:0>9}".format(context.numero) \
            + "\n"     
    f.write(buffer)      


def generar_990(context, pedido, f):
    generar_isa(context, pedido, f)
    generar_gs(context, pedido, f)
    generar_b1(context, pedido, f)
    generar_n9(context, pedido, f)
    generar_g62(context, pedido, f)
    

if __name__ == "__main__":
    """
    Main module
    """
    log.info("=====> Inicio (%s)" % os.getpid())
    retval = 0

    context = Context()
    context.session = None
    context.path = "/FTPSite/WNA/output"
    context.fecha = datetime.datetime.utcnow()
    context.numero = random.randint(1000, 50000)

    try:
        cp = configparser.ConfigParser()
        cp.read(YAETL_CONFIG)
        
        os.environ["NLS_LANG"] = cp.get("GT","nls_lang")

        engine = create_engine(cp.get("GT","uri"), echo=False)
        Session = sessionmaker(bind=engine)
        context.session = Session()
        
        codigo = "10-31584"
        
        ide, id = codigo.split("-")
        pedido = context.session.query(gt.Pedido) \
                .filter(gt.Pedido.ide == int(ide)) \
                .filter(gt.Pedido.id == int(id)) \
                .one_or_none()
        
        if not pedido is None:
            fn = context.path + "/" + nombre_fichero(codigo)
            with open(fn, "w") as f:
                generar_990(context, pedido, f)
            
        context.session.commit()

    except Exception as e:
        log.error(e)
        retval = 1
        context.session.rollback()
    finally:
        context.session.close()

    log.info("<===== Fin (%s)" % os.getpid())
    sys.exit(retval)