import configparser
import datetime
import json
import logging
import os
import sys
import traceback

from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pluscore import model

YAETL_HOME = ("%s/yaetl" % os.path.expanduser("~"))
YAETL_CONFIG = ("%s/etc/yaetl.config" % YAETL_HOME)
YAETL_LOG = ("%s/log/%s.log" %
             (YAETL_HOME, os.path.basename(__file__).split(".")[0]))
logging.basicConfig(level=logging.INFO, filename=YAETL_LOG,
                    format="%(asctime)s %(levelname)s %(module)s.%(funcName)s %(message)s")
log = logging.getLogger(__name__)

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
        
        os.environ["NLS_LANG"] = cp.get("PLUSCORE","nls_lang")

        engine = create_engine(cp.get("PLUSCORE","uri"), echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        from_date = datetime.date(2018, 12, 5)
        
        mm = session.query(model.ServicebusMessagesPending) \
                .filter(model.ServicebusMessagesPending.created >= from_date) \
                .filter(model.ServicebusMessagesPending.message.like('%MAN-%')) \
                .filter(model.ServicebusMessagesPending.messagetype == 2) \
                .order_by(model.ServicebusMessagesPending.created) \
                .all()
                      
        for m in mm:
            m1 = json.loads(m.message)
            fn = '{}-{}.json'.format(m.created.__format__('%Y%m%d%H%M%S')
                    , m1['Mensaje']['IdTransporteEmisor'])
            with open('/temp/MAN/1809/' + fn, 'w') as f:
                f.write(m.message)

#        with open('/temp/man.json', 'w') as f:
#            for m in mm:
#                m1 = json.loads(m.message)
#                json.dump(m1, f)
#                f.write('\n#\n')
                        
#        print(Path.home())
#        
#        base_dir = '/FTPSite/WNA/input'
#        desc = base_dir + '/descartados/'
#        proc = base_dir + '/procesados/'
#        
#        p = Path(base_dir)
#        l = p.glob('*')
#        for f in l:
#            if f.is_dir():
#                continue
#            print(f.name)
#            f.rename(proc + f.name)
        
        
                        
                        
                        
                        
                        
                        

    except Exception as e:
        log.error(traceback.format_tb(sys.exc_info()[2]))
        log.error(e)
        retval = 1
    finally:
        session.rollback()
        session.close()

    log.info("<===== Fin (%s)" % os.getpid())
    sys.exit(retval)