import configparser
import logging
import os
import requests
import sys
import time
import traceback

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

def obtener_zonas(context):
    zonas = {}
    for zona in context.session.query(gt.Zona).all():
        zonas[zona.nombre_zona] = zona.id_zona
    return zonas

def obtener_poblaciones(context):
    return context.session.query(gt.Poblacione) \
            .join(gt.Zona) \
            .filter(gt.Poblacione.pais == 'US') \
            .filter(gt.Poblacione.id > 401916) \
            .order_by(gt.Poblacione.id) \
            .limit(2000) \
            .all()
            
def procesar_poblacion(context, poblacion):
    if poblacion.poblacion.endswith(":OK"):
        return

    p = {
            'https':'36.80.182.4:53281',
#            'https':'76.76.76.154:53281',  
#                'https':'182.253.1.82:8080',  
#                'https':'119.42.70.154:41496',  
#    'https':'89.145.184.226:53281',
            }

    url = 'https://maps.googleapis.com/maps/api/timezone/json?' \
            + 'location=%f,%f&timestamp=%d' \
            % (poblacion.latitud, poblacion.longitud, int(time.time()))
    
#    log.info(url)
#    r = requests.get(url, proxies=p)
    r = requests.get(url)
    if not r.ok:
        log.error('poblacion %d no encontrada' % poblacion.id)
        return
    
    tzId = r.json()["timeZoneId"]
    if not tzId in context.zonas:
        log.error('Zona %s no encontrada en la tabla' % tzId)
        return
    
    if poblacion.zona.nombre_zona != tzId:
        log.info('(%d) %s, %s, %s' % (poblacion.id,
                                  poblacion.poblacion,
                                  poblacion.zona.nombre_zona,
                                  tzId))
        poblacion.zona_horaria = context.zonas[tzId]
        context.session.commit()

if __name__ == "__main__":
    """
    Main module
    """
    log.info("=====> Inicio (%s)" % os.getpid())
    retval = 0

    context = Context()
    try:
        cp = configparser.ConfigParser()
        cp.read(YAETL_CONFIG)
        
        os.environ["NLS_LANG"] = cp.get("GT","nls_lang")

        engine = create_engine(cp.get("GT","uri"), echo=False)
        Session = sessionmaker(bind=engine)
        context.session = Session()
        
        context.zonas = obtener_zonas(context)

        last_id = 0
        for poblacion in obtener_poblaciones(context):
            procesar_poblacion(context, poblacion)
            last_id = poblacion.id
#            break
            
        log.info('(last_id): %d' % last_id)
            
        context.session.commit()

    except Exception as e:
        log.error(traceback.format_tb(sys.exc_info()[2]))
        log.error(e)
        retval = 1
        context.session.rollback()
    finally:
        context.session.close()

    log.info("<===== Fin (%s)" % os.getpid())
    sys.exit(retval)