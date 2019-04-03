import configparser
import datetime
import logging
import os
import pyodbc
import sys
import traceback


YAETL_HOME = ("%s/yaetl" % os.path.expanduser("~"))
YAETL_CONFIG = ("%s/etc/yaetl.config" % YAETL_HOME)
YAETL_LOG = ("%s/log/%s.log" %
             (YAETL_HOME, os.path.basename(__file__).split(".")[0]))
logging.basicConfig(level=logging.INFO, filename=YAETL_LOG,
                    format="%(asctime)s %(levelname)s %(module)s.%(funcName)s %(message)s")
log = logging.getLogger(__name__)

class Context():
    pass

    
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
    
    conn = None

    try:
        cp = configparser.ConfigParser()
        cp.read(YAETL_CONFIG)
        
#        os.environ["NLS_LANG"] = cp.get("GT","nls_lang")
#        e1 = create_engine(cp.get("GT","uri"), echo=False)
        
        driver = cp.get("EPSILON","driver")
        server = cp.get("EPSILON","server")
        database = cp.get("EPSILON","database")
        username = cp.get("EPSILON","username")
        password = cp.get("EPSILON","password")
#        uri = "DRIVER=" + driver + ";SERVER=" + server + ";DATABASE=" \
#                + database + ";UID=" + username + ";PWD=" + password
        uri = "DRIVER={ODBC Driver 13 for SQL Server};SERVER=localhost;UID=saul.correas;PWD=Perroflauta17;DATABASE=bd_epsilon"
        conn = pyodbc.connect(uri)
               
        cursor = conn.cursor()
        cursor.execute("select @@version")
        row = cursor.fetchone()
        while row:
            log.info(row[0])
            row = cursor.fetchone()

    except Exception as e:
        log.error(e)
        log.error(traceback.format_tb(sys.exc_info()[2]))
        retval = 1
    finally:
        cursor.close()

    log.info("<===== Fin (%s)" % os.getpid())
    sys.exit(retval)


