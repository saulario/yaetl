import configparser
import datetime
import logging
import os
import random
import sys
import traceback

from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity

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

def generar_isa(context, f):
    buffer = "ISA*00*" + "{:10}".format("") + "*00*" + "{:10}".format("") \
            + "*ZZ*" + "{:15}".format(context.ot.emp_idp) \
            + "*ZZ*" + "{:15}".format("SG10") \
            + "*" + context.fecha.strftime("%y%m%d") \
            + "*" + context.fecha.strftime("%H%M") \
            + "*U*00401" \
            + "*" + "{:0>9}".format(context.numero) \
            + "*1*P*:\n"
    f.write(buffer)
    
    buffer = "GS*" + context.gs01 + "*" + context.ot.emp_idp + "*SG10" \
            + "*" + context.fecha.strftime("%Y%m%d") \
            + "*" + context.fecha.strftime("%H%M") \
            + "*" + str(context.numero) \
            + "*X*004010" \
            + "\n"     
    f.write(buffer)

    context.lineas += 1
    buffer = "ST*" + context.st01 + "*1" \
            + "\n"     
    f.write(buffer)  
    

def generar_214_comun(context, f):
    
    context.lineas += 1    
    buffer = "B10" \
            + "*PRO-123456"  \
            + "*" + str(context.ot.ide) + "-" + str(context.ot.id) \
            + "\n"
    f.write(buffer)
    
    context.lineas += 1    
    buffer = "K1" \
            + "*" + context.ot.veh_mat_remolque  \
            + "*" + context.ot.veh_mat_tractora \
            + "\n"
    f.write(buffer)
    
def generar_se(context, f):    
    
    context.lineas += 1    
    buffer = "SE*" \
            + str(context.lineas) \
            + "*1" \
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

def test_990_to_does_not_exist(context):
    fn = context.path + "/X12_990_{}_{}-{}_does_not_exist.EDI" \
            .format(context.ot.emp_idp, context.ot.ide, context.ot.id)
    context.lineas = 0
    with open(fn, "w") as f:
        generar_isa(context, f)
        
        context.lineas += 1
        buffer = "B1" \
                + "*"  \
                + "*" + str(context.ot.ide) + "-" + str(context.ot.id * 1000) \
                + "*" \
                + "*A" \
                + "\n"     
        f.write(buffer)         
        
        generar_se(context, f)

def test_990_to_incorrect_carrier(context):
    fn = context.path + "/X12_990_{}_{}-{}_incorrect_carrier.EDI" \
            .format(context.ot.emp_idp, context.ot.ide, context.ot.id)
    context.lineas = 0    
    with open(fn, "w") as f:
        generar_isa(context, f)
        
        context.lineas += 1
        buffer = "B1" \
                + "*"  \
                + "*" + str(context.ot.ide) + "-" + str(2570) \
                + "*" \
                + "*A" \
                + "\n"     
        f.write(buffer)          
        
        generar_se(context, f)

def test_990_invalid_function(context):
    fn = context.path + "/X12_990_{}_{}-{}_invalid_function.EDI" \
            .format(context.ot.emp_idp, context.ot.ide, context.ot.id)
    context.lineas = 0    
    with open(fn, "w") as f:
        generar_isa(context, f)

        context.lineas += 1
        buffer = "B1" \
                + "*"  \
                + "*" + str(context.ot.ide) + "-" + str(context.ot.id) \
                + "*" \
                + "*X" \
                + "\n"     
        f.write(buffer)          
        
        generar_se(context, f)

def test_990_function_omitted(context):
    fn = context.path + "/X12_990_{}_{}-{}_function_omitted.EDI" \
            .format(context.ot.emp_idp, context.ot.ide, context.ot.id)
    context.lineas = 0    
    with open(fn, "w") as f:
        generar_isa(context, f)
        
        
        generar_se(context, f)

def test_990_accepted(context):
    fn = context.path + "/X12_990_{}_{}-{}_accepted.EDI" \
            .format(context.ot.emp_idp, context.ot.ide, context.ot.id)
    context.lineas = 0    
    with open(fn, "w") as f:
        generar_isa(context, f)
        
        context.lineas += 1
        buffer = "B1" \
                + "*"  \
                + "*" + str(context.ot.ide) + "-" + str(context.ot.id) \
                + "*" \
                + "*A" \
                + "\n"     
        f.write(buffer)
        
        context.lineas += 1
        buffer = "N9" \
                + "*CN"  \
                + "*PRO-123456" \
                + "\n"     
        f.write(buffer) 
        
        generar_se(context, f)

def test_990_declined(context):
    fn = context.path + "/X12_990_{}_{}-{}_declined.EDI" \
            .format(context.ot.emp_idp, context.ot.ide, context.ot.id)
    context.lineas = 0    
    with open(fn, "w") as f:
        generar_isa(context, f)
        
        
        context.lineas += 1
        buffer = "B1" \
                + "*"  \
                + "*" + str(context.ot.ide) + "-" + str(context.ot.id) \
                + "*" \
                + "*D" \
                + "\n"     
        f.write(buffer)
        
        generar_se(context, f)
        

def test_214_to_does_not_exist(context):
    fn = context.path + "/X12_214_{}_{}-{}_does_not_exist.EDI" \
            .format(context.ot.emp_idp, context.ot.ide, context.ot.id)
    context.lineas = 0    
    with open(fn, "w") as f:
        generar_isa(context, f)
        
        context.lineas += 1
        buffer = "B10" \
                + "*PRO-123456"  \
                + "*" + str(context.ot.ide) + "-" + str(context.ot.id * 100) \
                + "\n"
        f.write(buffer)
        
        generar_se(context, f)        
        
def test_214_to_incorrect_carrier(context):
    fn = context.path + "/X12_214_{}_{}-{}_incorrect_carrier.EDI" \
            .format(context.ot.emp_idp, context.ot.ide, context.ot.id)
    context.lineas = 0    
    with open(fn, "w") as f:
        generar_isa(context, f)
   
        context.lineas += 1
        buffer = "B10" \
                + "*PRO-123456"  \
                + "*" + str(context.ot.ide) + "-" + str(2570) \
                + "\n"
        f.write(buffer)      
        
        generar_se(context, f)             
        
def test_214_stop_does_not_exist(context):
    fn = context.path + "/X12_214_{}_{}-{}_stop_does_not_exist.EDI" \
            .format(context.ot.emp_idp, context.ot.ide, context.ot.id)
    context.lineas = 0    
    with open(fn, "w") as f:
        generar_isa(context, f)
        generar_214_comun(context, f)
        
        context.lineas += 1
        buffer = "LX" \
                + "*1"  \
                + "\n"
        f.write(buffer)            
        
        for otl in context.otls:
            code = "X3"
            if otl.tipo == "E":
                code = "X1" 
                
            context.lineas += 1
            buffer = "AT7" \
                    + "*" + code \
                    + "*NS" \
                    + "*" \
                    + "*" \
                    + "*" + otl.fecha.strftime("%Y%m%d") \
                    + "*" + otl.hora.replace(":", "") \
                    + "*LT" \
                    + "\n"
            f.write(buffer)   

            context.lineas += 1
            buffer = "L11" \
                    + "*" + str(otl.id_linea * 333) \
                    + "*X9" \
                    + "\n"
            f.write(buffer)              
        
        generar_se(context, f)    

def test_214_stop_incorrect_to(context):
    fn = context.path + "/X12_214_{}_{}-{}_stop_incorrect_to.EDI" \
            .format(context.ot.emp_idp, context.ot.ide, context.ot.id)
    context.lineas = 0    
    with open(fn, "w") as f:
        generar_isa(context, f)
        generar_214_comun(context, f)
        
        context.lineas += 1
        buffer = "LX" \
                + "*1"  \
                + "\n"
        f.write(buffer)            
        
        for otl in context.otls:
            code = "X3"
            if otl.tipo == "E":
                code = "X1"         
        
            context.lineas += 1
            buffer = "AT7" \
                    + "*" + code \
                    + "*NS" \
                    + "*" \
                    + "*" \
                    + "*" + otl.fecha.strftime("%Y%m%d") \
                    + "*" + otl.hora.replace(":", "") \
                    + "*LT" \
                    + "\n"
            f.write(buffer)   

            context.lineas += 1
            buffer = "L11" \
                    + "*" + str(otl.id_linea - 5555) \
                    + "*X9" \
                    + "\n"
            f.write(buffer)               
        
        generar_se(context, f)   

def test_214_events_placed_incorrect(context):
    fn = context.path + "/X12_214_{}_{}-{}_events_placed_incorrect.EDI" \
            .format(context.ot.emp_idp, context.ot.ide, context.ot.id)
    context.lineas = 0    
    with open(fn, "w") as f:
        generar_isa(context, f)
        generar_214_comun(context, f)        
        
        context.lineas += 1
        buffer = "LX" \
                + "*2"  \
                + "\n"
        f.write(buffer)            
        
        for otl in context.otls:
            code = "X3"
            if otl.tipo == "E":
                code = "X1"         
        
            context.lineas += 1
            buffer = "AT7" \
                    + "*" + code \
                    + "*NS" \
                    + "*" \
                    + "*" \
                    + "*" + otl.fecha.strftime("%Y%m%d") \
                    + "*" + otl.hora.replace(":", "") \
                    + "*LT" \
                    + "\n"
            f.write(buffer)   

            context.lineas += 1
            buffer = "L11" \
                    + "*" + str(otl.id_linea) \
                    + "*X9" \
                    + "\n"
            f.write(buffer)          
        
        generar_se(context, f)   
        
def wgs84toddms(wgs84, code):
    
    if wgs84 < 0:
        if code == "N":
            code = "S"
        elif code == "E":
            code = "W"
            
    wgsabs = abs(wgs84)            
            
    grados = int(wgsabs)
    wgsabs -= grados
    minutos = int(wgsabs * 60)
    wgsabs -= minutos / 60
    segundos = int(round(wgsabs * 3600, 0))            
    coord = '{:03d}{:02d}{:02d}'.format(grados, minutos, segundos)        
    
    return coord, code

def test_214_positions_placed_incorrect(context):
    fn = context.path + "/X12_214_{}_{}-{}_positions_placed_incorrect.EDI" \
            .format(context.ot.emp_idp, context.ot.ide, context.ot.id)
    context.lineas = 0    
    with open(fn, "w") as f:
        generar_isa(context, f)
        generar_214_comun(context, f)        
        
        context.lineas += 1
        buffer = "LX" \
                + "*1"  \
                + "\n"
        f.write(buffer)        
        for posicion in context.posiciones:

            print(posicion.RowKey)
            
            context.lineas += 1
            buffer = "AT7" \
                    + "*X6" \
                    + "*NS" \
                    + "*" \
                    + "*" \
                    + "*" + posicion.DateTimeGps.strftime("%Y%m%d") \
                    + "*" + posicion.DateTimeGps.strftime("%H%M") \
                    + "*UT" \
                    + "\n"
            f.write(buffer)   
            
            lat, latcod = wgs84toddms(posicion.Latitude, "N")
            lon, loncod = wgs84toddms(posicion.Longitude, "E")
            
            context.lineas += 1
            buffer = "MS1" \
                    + "***" \
                    + "*" + lon \
                    + "*" + lat \
                    + "*" + loncod \
                    + "*" + latcod \
                    + "\n"
            f.write(buffer)           
        
        generar_se(context, f)   

def test_214_ok(context):
    fn = context.path + "/X12_214_{}_{}-{}_ok.EDI" \
            .format(context.ot.emp_idp, context.ot.ide, context.ot.id)
    context.lineas = 0    
    with open(fn, "w") as f:
        generar_isa(context, f)
        generar_214_comun(context, f)    
        
        
        context.lineas += 1
        buffer = "LX" \
                + "*1"  \
                + "\n"
        f.write(buffer)            
        
        for otl in context.otls:
            code = "X3"
            if otl.tipo == "E":
                code = "X1"         
        
            context.lineas += 1
            buffer = "AT7" \
                    + "*" + code \
                    + "*NS" \
                    + "*" \
                    + "*" \
                    + "*" + otl.fecha.strftime("%Y%m%d") \
                    + "*" + otl.hora.replace(":", "") \
                    + "*LT" \
                    + "\n"
            f.write(buffer)   

            context.lineas += 1
            buffer = "L11" \
                    + "*" + str(otl.id_linea) \
                    + "*X9" \
                    + "\n"
            f.write(buffer)           
        
        context.lineas += 1
        buffer = "LX" \
                + "*2"  \
                + "\n"
        f.write(buffer)        
        for posicion in context.posiciones:

            print(posicion.RowKey)
            
            context.lineas += 1
            buffer = "AT7" \
                    + "*X6" \
                    + "*NS" \
                    + "*" \
                    + "*" \
                    + "*" + posicion.DateTimeGps.strftime("%Y%m%d") \
                    + "*" + posicion.DateTimeGps.strftime("%H%M") \
                    + "*UT" \
                    + "\n"
            f.write(buffer)   
            
            lat, latcod = wgs84toddms(posicion.Latitude, "N")
            lon, loncod = wgs84toddms(posicion.Longitude, "E")
            
            context.lineas += 1
            buffer = "MS1" \
                    + "***" \
                    + "*" + lon \
                    + "*" + lat \
                    + "*" + loncod \
                    + "*" + latcod \
                    + "\n"
            f.write(buffer)   
                
        generar_se(context, f) 
        

if __name__ == "__main__":
    """
    Main module
    """
    log.info("=====> Inicio (%s)" % os.getpid())
    retval = 0

    context = Context()
    context.session = None
    context.path = "//prodmzservices/FTPSite/x12-99999/outbox"
    context.fecha = datetime.datetime.utcnow()
    context.numero = random.randint(1000, 50000)    
    
    ot = "3-10581"

    try:
        cp = configparser.ConfigParser()
        cp.read(YAETL_CONFIG)
        
        os.environ["NLS_LANG"] = cp.get("GT","nls_lang")

        engine = create_engine(cp.get("GT","uri"), echo=False)
        Session = sessionmaker(bind=engine)
        context.session = Session()
        
        context.table_service = TableService(account_name = cp.get("AZURE","account_name")
                                             , account_key= cp.get("AZURE","account_key"))
        fromDate = datetime.datetime(2018, 1, 1)
        toDate = datetime.datetime(2018, 1, 3)
        ff = "PartitionKey eq '4' and DateTimeCreated ge datetime'%s' and " \
                " DateTimeCreated lt datetime'%s'" % (fromDate.isoformat(), toDate.isoformat())
        print(ff)
        context.posiciones = context.table_service.query_entities("apkposition", 
                                                                  filter = ff,
                                                                  num_results = 10)
        
        ide, id = ot.split("-")
        context.ot = context.session.query(gt.OrdenesTransporte) \
                .filter(gt.OrdenesTransporte.ide == ide) \
                .filter(gt.OrdenesTransporte.id == id) \
                .one_or_none()
                
        context.otls = context.session.query(gt.OrdenesTransporteLinea) \
                .filter(gt.OrdenesTransporteLinea.ide == ide) \
                .filter(gt.OrdenesTransporteLinea.ot == id) \
                .order_by(gt.OrdenesTransporteLinea.etapa_t) \
                .all()
                


        if not context.ot is None:
            
            context.gs01 = "GF"
            context.st01 = "990"
            
            test_990_to_does_not_exist(context)        
            test_990_to_incorrect_carrier(context)        
            test_990_invalid_function(context)        
            test_990_function_omitted(context)        
            test_990_accepted(context)        
            test_990_declined(context)        
            
            context.gs01 = "QM"
            context.st01 = "214"
            
            test_214_to_does_not_exist(context)
            test_214_to_incorrect_carrier(context)
            test_214_stop_does_not_exist(context)
            test_214_stop_incorrect_to(context)
            test_214_events_placed_incorrect(context)
            test_214_positions_placed_incorrect(context)
            test_214_ok(context)       

    except Exception as e:
        log.error(traceback.format_tb(sys.exc_info()[2]))
        log.error(e)
        retval = 1
        context.session.rollback()
    finally:
        context.session.close()

    log.info("<===== Fin (%s)" % os.getpid())
    sys.exit(retval)