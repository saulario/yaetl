import configparser
import logging
import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


YAETL_HOME = ("%s/yaetl" % os.path.expanduser("~"))
YAETL_CONFIG = ("%s/etc/yaetl.config" % YAETL_HOME)
YAETL_LOG = ("%s/log/%s.log" %
             (YAETL_HOME, os.path.basename(__file__).split(".")[0]))
logging.basicConfig(level=logging.INFO, filename=YAETL_LOG,
                    format="%(asctime)s %(levelname)s %(module)s.%(funcName)s %(message)s")
log = logging.getLogger(__name__)

from model import gt

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
        
        qry = session.query(gt.Pedido).filter(gt.Pedido.ide == 10).filter(gt.Pedido.id == 31517).all()
        for p in qry:
            print("%s %s" % (p.ide, p.id))


    except Exception as e:
        log.error(e)
        retval = 1
    finally:
        session.rollback()
        session.close()

    log.info("<===== Fin (%s)" % os.getpid())
    sys.exit(retval)