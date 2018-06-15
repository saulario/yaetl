
import configparser
import logging
import os
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

#
#
#
if __name__ == "__main__":
    """
    Main module
    """
    log.info("=====> Inicio (%s)" % os.getpid())
    retval = 0

    context = Context()
    context.session = None

    try:
        cp = configparser.ConfigParser()
        cp.read(YAETL_CONFIG)
        
        os.environ["NLS_LANG"] = cp.get("GT","nls_lang")

        engine = create_engine(cp.get("GT","uri"), echo=False)
        Session = sessionmaker(bind=engine)
        context.session = Session()
        
        q = context.session.query(gt.Pedido).filter(gt.Pedido.ide == 10)\
            .filter(gt.Pedido.pet_org_fecha >= '01/06/2018')\
            .all()[1:5]
        for r in q:
            log.info("%s %s" % (r.id, r.pet_org_fecha))

    except Exception as e:
        log.error(e)
        retval = 1
    finally:
        context.session.rollback()
        context.session.close()

    log.info("<===== Fin (%s)" % os.getpid())
    sys.exit(retval)