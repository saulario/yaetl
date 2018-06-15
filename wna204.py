
import configparser
import datetime
import logging
import os
import pathlib
import sys
import uuid

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

def get_files(context):
    retval = []
    
    if context.path is None:
        return retval
    
    p = pathlib.Path(context.path)
    for f in p.glob("**/*"):
        if f.is_file():
            retval.append(f)
    
    return retval


def procesar_gs(linea, pedido):
    pedido["emisor"] = linea[2]
    pedido["fuente"] = linea[6] # puede venir también en L11
    return pedido

def procesar_b2(campos, pedido):
    pedido["pedido_cliente"] = campos[4]
    return pedido

def procesar_b2a(linea, pedido):
    pedido["x12_purpose"] = linea[1]
    return pedido

def procesar_l11(campos, pedido):
    if campos[2] == "BM":
        pedido["referencia_cliente"] = campos[1]
    elif campos[2] == "TN":
        pedido["fuente"] = campos[1]
    return pedido

def procesar_n7(campos, pedido):
    largo = float(campos[15]) / 100
    if campos[11] == "TV":
        pedido["observaciones"] = ("Dry van %s" % largo)
    elif campos[11] == "RT":
        pedido["observaciones"] = ("Reefer %s" % largo)
        pedido["frio"] = True
    return pedido

def procesar_l3(campos, pedido):
    pedido["peso"] = float(campos[1])
    pedido["udmPeso"] = campos[2]
    pedido["volumen"] = float(campos[9])
    pedido["udmVolumen"] = campos[10]
    return pedido

def procesar_s5(campos, etapa):
    etapa["etapa"] = campos[1]
#    etapa["tipo"] = campos[2]
    etapa["peso"] = float(campos[3])
    etapa["udmPeso"] = campos[4]
    etapa["bultos"]= campos[5]
    etapa["tipoContenedor"] = campos[6]
    etapa["volumen"] = campos[7]
    etapa["udmVolumen"] = campos[8]
    return etapa
    
def procesar_g62(campos, etapa):
    if campos[0] == "69":
        etapa["tipo"] = "R"
    else:
        etapa["tipo"] = "E"

    fecha = campos[2]
    hora = campos[4]
    etapa["fecha"] = datetime.date(int(fecha[0:4]), int(fecha[4:6]), 
         int(fecha[6:8]))
    etapa["hora"] = datetime.time(int(hora[0:2]), int(hora[2:4]))
    etapa["calificador"] = campos[3]
    
    return etapa

def procesar_n1(campos, etapa):
    etapa["nombre"] = campos[2]
    etapa["codigoExterno"] = campos[4]
    return etapa

def procesar_n3(campos, etapa):
    etapa["calle"] = campos[1]
    return etapa

def procesar_n4(campos, etapa):
    etapa["ciudad"] = campos[1]
    etapa["estado"] = campos[2]
    etapa["cp"] = campos[3]
    etapa["pais"] = campos[4]
    return etapa

def procesar_g61(campos, etapa):
    etapa["contacto"] = campos[4]
    return etapa

def procesar_l5(campos, etapa):
    bulto = {}
    bulto["uuid"] = str(uuid.uuid4())        
    bulto["linea"] = campos[1]
    bulto["descripcion"] = campos[2]
    bulto["cantidad"] = campos[3]
    etapa["detalle"].append(bulto)
    return etapa

def procesar_oid(campos, etapa):
    etapa["referencia"] = campos[1]
    etapa["ordCompra"] = campos[2]
    etapa["udm"] = campos[4]
    etapa["cantidad"] = float(campos[5])
    etapa["pesoEn"] = campos[6]
    etapa["peso"] = float(campos[7])
    return etapa

def procesar_lad(campos, etapa):
    return etapa

def procesar_poblacion(lineas, pedido):
    etapa = {}
    etapa["uuid"] = str(uuid.uuid4())
    etapa["detalle"] = []
    pedido["etapas"].append(etapa)  
    
    repite = False
    while len(lineas):
        campos = lineas[0].split("*")
        
        if campos[0] == "L3":
            return pedido
        if campos[0] == "S5" and repite:
            return pedido
        
        if campos[0] == "S5":
            etapa = procesar_s5(campos, etapa)
            repite = True
        elif campos[0] == "G62":
            etapa = procesar_g62(campos, etapa)
        elif campos[0] == "N1":
            etapa = procesar_n1(campos, etapa)
        elif campos[0] == "N3":
            etapa = procesar_n3(campos, etapa)
        elif campos[0] == "N4":
            etapa = procesar_n4(campos, etapa)      
        elif campos[0] == "G61":
            etapa = procesar_g61(campos, etapa)      
        elif campos[0] == "L5":
            etapa = procesar_l5(campos, etapa)  
        elif campos[0] == "OID":
            etapa = procesar_oid(campos, etapa)              
        elif campos[0] == "LAD":
            etapa = procesar_lad(campos, etapa)  
        
        lineas.pop(0)

def procesar_pedidos(lineas):
    pedido = {}
    pedido["uuid"] = str(uuid.uuid4())
    pedido["etapas"] = []
    
    while len(lineas):
        campos = lineas[0].split("*")
        
        if campos[0] == "S5":
            pedido = procesar_poblacion(lineas, pedido)
            continue
        
        if campos[0] == "SE":
            lineas.pop(0)
            return pedido
        
        if campos[0] == "ST":
            pass
        elif campos[0] == "B2":
            pedido = procesar_b2(campos, pedido)
        elif campos[0] == "B2A":
            pedido = procesar_b2a(campos, pedido)            
        elif campos[0] == "L11":
            pedido = procesar_l11(campos, pedido)
        elif campos[0] == "N7":
            pedido = procesar_n7(campos, pedido)
        elif campos[0] == "L3":
            pedido = procesar_l3(campos, pedido)
            
        lineas.pop(0)
        
    return pedido    

def procesar_archivo(context, file):
    log.info("-----> Inicio")
    log.info("       (file): %s" % file)
    
    emisor = None
    pedidos = []
    lineas = []
    with open(file) as f:
        lineas = f.read().split("~")

    while len(lineas):
        campos = lineas[0].split("*")
        
        if campos[0] == "ST":
            pedido = procesar_pedidos(lineas)
            pedido["emisor"] = emisor
            pedidos.append(pedido)
            continue
        
        if campos[0] == "GS":
            emisor = campos[2]
        
        lineas.pop(0)
        
    log.info("<----- Fin")
    return pedidos


def insertar_pedido(context, p):

    pedido = gt.Pedido()
    pedido.ide = 10
    pedido.id = None
    pedido.cliente = '29530'
    pedido.estado = '1'
    pedido.tipo = 1
    pedido.gestor = "SCORREAS"
    pedido.importe = 0
    pedido.moneda = "USD"
    pedido.delegacion = '61'
    pedido.ide_pedido_asociado = 1
    pedido.moneda_prov = 'USD'
    pedido.urgencia = 'N'
    pedido.gf = 1
    pedido.importe_sistema = 0
    pedido.frio = 0
    
    pedido.emisor = p["emisor"]
    pedido.fuente = p["fuente"]
    pedido.timbre_uuid = p["uuid"]

    context.session.add(pedido)
    context.session.commit()
    
    pedido = context.session.query(gt.Pedido)\
            .filter(gt.Pedido.ide == 10)\
            .filter(gt.Pedido.timbre_uuid == p["uuid"])\
            .first()

    print(pedido.id)

    
    

def insertar_pedidos(context, pedidos):    
    for pedido in pedidos:
        insertar_pedido(context, pedido)

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
    context.path = '/FTPSite/WNA/input'

    try:
        cp = configparser.ConfigParser()
        cp.read(YAETL_CONFIG)
        
        os.environ["NLS_LANG"] = cp.get("GT","nls_lang")

        engine = create_engine(cp.get("GT","uri"), echo=False)
        Session = sessionmaker(bind=engine)
        context.session = Session()
        
        for file in get_files(context):
            pedidos = procesar_archivo(context, file)
            insertar_pedidos(context, pedidos)
            break

        
        context.session.commit()

    except Exception as e:
        log.error(e)
        retval = 1
        context.session.rollback()
    finally:
        context.session.close()

    log.info("<===== Fin (%s)" % os.getpid())
    sys.exit(retval)