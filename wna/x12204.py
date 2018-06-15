
import configparser
import logging
import os
import sys

import cx_Oracle


YAETL_HOME = ("%s/yaetl" % os.path.expanduser("~"))
YAETL_CONFIG = ("%s/etc/yaetl.config" % YAETL_HOME)
YAETL_LOG = ("%s/log/%s.log" %
             (YAETL_HOME, os.path.basename(__file__).split(".")[0]))
logging.basicConfig(level=logging.INFO, filename=YAETL_LOG,
                    format="%(asctime)s %(levelname)s %(module)s.%(funcName)s %(message)s")
log = logging.getLogger(__name__)

#
#
#
if __name__ == "__main__":
    """
    Main module
    """
    log.info("=====> Inicio (%s)" % os.getpid())
    retval = 0
    con = None

    try:
        cp = configparser.ConfigParser()
        cp.read(YAETL_CONFIG)
        
        uri = cp.get("GT", "uri")
        con = cx_Oracle.connect(uri)



    except Exception as e:
        log.error(e)
        retval = 1
    finally:
        if not con is None:
            con.close()

    log.info("<===== Fin (%s)" % os.getpid())
    sys.exit(retval)