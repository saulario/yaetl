import configparser
import csv
import logging
import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from gt import model

YAETL_HOME = ("%s/yaetl" % os.path.expanduser("~"))
YAETL_CONFIG = ("%s/etc/yaetl.config" % YAETL_HOME)
YAETL_LOG = ("%s/log/%s.log" %
             (YAETL_HOME, os.path.basename(__file__).split(".")[0]))
logging.basicConfig(level=logging.INFO, filename=YAETL_LOG,
                    format="%(asctime)s %(levelname)s %(module)s.%(funcName)s %(message)s")
log = logging.getLogger(__name__)

def obtener_plantas(row):
    plantas = row[0].split(';')
    return list(map(lambda x: x.rsplit(), plantas))

if __name__ == "__main__":
    """
    Main module
    """
    log.info("=====> Inicio (%s)" % os.getpid())
    retval = 0

    session = None

    try:
        cp = configparser.ConfigParser()
        cp.read(YAETL_CONFIG)
        
        os.environ["NLS_LANG"] = cp.get("GT","nls_lang")

        engine = create_engine(cp.get("GT","uri"), echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        with open('/temp/distancias.csv') as f:
            reader = csv.reader(f)
            l = 0
            plantas = None
            for row in reader:
                l = l + 1
                if l < 3 or l == 4:
                    continue
                elif l == 3:
                    print(type(row))
                    plantas = obtener_plantas(row)
                    print(plantas)
                else:
                    valores = row[0].split(';')
                    proveedor = valores[1].split()
                    for idx, distancia in enumerate(valores):
                        if idx < 4:
                            continue
                        planta = plantas[idx]
                        print(proveedor, planta, distancia)
                        
                        ed = model.EmpresasDistancia()
                        ed.ide = 3
                        ed.empresa = 34340
                        ed.codigo_destino = planta[0]
                        ed.codigo_origen = proveedor[0]
                        ed.distancia = distancia
                        session.add(ed)
                        
                        ed = model.EmpresasDistancia()
                        ed.ide = 1
                        ed.empresa = 34340
                        ed.codigo_destino = planta[0]
                        ed.codigo_origen = proveedor[0]
                        ed.distancia = distancia
                        session.add(ed)
                        
                        session.commit()
                    
                    

    except Exception as e:
        log.error(e)
        retval = 1
    finally:
        session.rollback()
        session.close()

    log.info("<===== Fin (%s)" % os.getpid())
    sys.exit(retval)