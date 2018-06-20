import configparser
import datetime
import logging
import os
import random
import sys

from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

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

# Esta parte es un poco complicada porque hay que hacer el salto de empresa
#
def obtener_remolque(context, pedido, pedido_etapa):
    
    if pedido_etapa.id_ot_linea is None:
        return ""
    
    # paso 1, llegar a la OT asociada a la etapa
    otl = context.session.query(gt.OrdenesTransporteLinea) \
            .filter(gt.OrdenesTransporteLinea.id_linea == pedido_etapa.id_ot_linea) \
            .one_or_none()
    if otl is None:
        return ""
    
    # paso 2, comprobar si está volcada a fleet. El problema es que la tabla
    # de volcado de empresas no tiene ningún tipo de clave ni de índice
    # y no se mapea en el ORM, así que hay que hacerlo a pelo    
    sql = """
        select * from gt.volcado_empresas where ide = :ide and ot = :ot
    """
    volcados = context.engine.execute(text(sql), 
                                      ide = otl.ordenes_transporte.ide,
                                      ot = otl.ordenes_transporte.id)
    volcado = None
    ide = None
    id = None
    for volcado in volcados:
        ide = volcado[4]
        id = volcado[6]
        break
    
    if volcado is None:
        return otl.ordenes_transporte.veh_mat_remolque
    
    # Hay volcado, así que hay que repetir la operación en la empresa
    # de destino. Si no encontramos podemos mantener el criterio de 
    # lo que haya puesto logistics
    
    #En la etapa de pedido que tenga la misma dirección
    ped = context.session.query(gt.PedidosEtapa) \
            .filter(gt.PedidosEtapa.ide == ide) \
            .filter(gt.PedidosEtapa.pedido == id) \
            .filter(gt.PedidosEtapa.tipo == otl.tipo) \
            .filter(gt.PedidosEtapa.direccion == otl.direccion) \
            .first()
            
    if ped is None:
        return otl.ordenes_transporte.veh_mat_remolque
    
    if ped.id_ot_linea is None:
        return otl.ordenes_transporte.veh_mat_remolque

    # hasta aquí se ha llegado porque se ha encontrado toda la correlación,
    # así que ya podemos leer ordenes_transporte_lineas en destino y 
    # devolver el resultado
    otld = context.session.query(gt.OrdenesTransporteLinea)   \
            .filter(gt.OrdenesTransporteLinea.id_linea == ped.id_ot_linea) \
            .first()
            
    if otld is None:
        return otl.ordenes_transporte.veh_mat_remolque    
    
    return otld.ordenes_transporte.veh_mat_remolque

def nombre_fichero(pedido):
    cdn = 'SEGO_214_' + pedido + "_" \
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
    buffer = "GS*QM*" + context.scac + "*CWNA" \
            + "*" + context.fecha.strftime("%Y%m%d") \
            + "*" + context.fecha.strftime("%H%M") \
            + "*" + str(context.numero) \
            + "*X*004010" \
            + "\n"     
    f.write(buffer)

    buffer = "ST*214*1" \
            + "\n"     
    f.write(buffer)        
    
def generar_b10(context, pedido, etapa, f):
    buffer = "B10" \
            + "*" + pedido.dim_cliente_1 \
            + "*" + pedido.pedido_cliente \
            + "*" + context.scac \
            + "\n"     
    f.write(buffer)    
    
def generar_l11_lx(context, pedido, etapa, f):
    buffer = "L11" \
            + "*" + pedido.referencia_cliente \
            + "*BM" \
            + "\n"     
    f.write(buffer)     
    
    buffer = "L11" \
            + "*" + pedido.dim_cliente_1 \
            + "*CN" \
            + "\n"     
    f.write(buffer)
    
    buffer = "LX*1" \
            + "\n"     
    f.write(buffer)

def generar_ms1_ms2(context, pedido, etapa, f):
    buffer = "MS1" \
            + "*" + etapa.dir_poblacion \
            + "*" + etapa.direccione.provincia1.cpa \
            + "*" + etapa.dir_pais \
            + "\n"     
    f.write(buffer)     
    
    buffer = "MS2" \
            + "*" + context.scac \
            + "*" + obtener_remolque(context, pedido, etapa) \
            + "\n"     
    f.write(buffer)
    
def generar_at7_llegada(context, pedido, etapa, f):
    cod1 = "X3"
    if etapa.tipo == "E":
        cod1 = "X1"
        
    buffer = "AT7" \
            + "*" + cod1 \
            + "*NS**" \
            + "*" + etapa.fecha_inicio_carga.strftime("%y%m%d") \
            + "*" + etapa.fecha_inicio_carga.strftime("%H%M") \
            + "\n"
    f.write(buffer)

def generar_at7_salida(context, pedido, etapa, f):
    cod1 = "AF"
    if etapa.tipo == "E":
        cod1 = "CD"
        
    buffer = "AT7" \
            + "*" + cod1 \
            + "*NS**" \
            + "*" + etapa.fecha_fin_carga.strftime("%y%m%d") \
            + "*" + etapa.fecha_fin_carga.strftime("%H%M") \
            + "\n"
    f.write(buffer)

def generar_l11_at8(context, pedido, etapa, f):
    buffer = "L11" \
            + "*" + etapa.codigo_externo \
            + "*LU" \
            + "\n"     
    f.write(buffer)     
    
    buffer = "AT8" \
            + "*G" \
            + "*L" \
            + "*" + str(etapa.cantidad_carga) \
            + "\n"     
    f.write(buffer)

def generar_se(context, pedido, f):    
    buffer = "SE*10*1" \
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

def generar_214_llegada(context, pedido, pedido_etapa):
    
    fn = context.path + "/" + nombre_fichero("%s-%s" % (pedido.ide, pedido.id))
    with open(fn, "w") as f:
        generar_isa(context, pedido, f)
        generar_gs(context, pedido, f)
        generar_b10(context, pedido, pedido_etapa, f)
        generar_l11_lx(context, pedido, pedido_etapa, f)
        generar_at7_llegada(context, pedido, pedido_etapa, f)
        generar_ms1_ms2(context, pedido, pedido_etapa, f)
        generar_l11_at8(context, pedido, pedido_etapa, f)
        generar_se(context, pedido, f)
    
def generar_214_salida(context, pedido, pedido_etapa):
    
    fn = context.path + "/" + nombre_fichero("%s-%s" % (pedido.ide, pedido.id))
    with open(fn, "w") as f:
        generar_isa(context, pedido, f)
        generar_gs(context, pedido, f)
        generar_b10(context, pedido, pedido_etapa, f)
        generar_l11_lx(context, pedido, pedido_etapa, f)
        generar_at7_salida(context, pedido, pedido_etapa, f)
        generar_ms1_ms2(context, pedido, pedido_etapa, f)
        generar_l11_at8(context, pedido, pedido_etapa, f)
        generar_se(context, pedido, f)
    
def generar_214(context, pedido, pedido_etapa):
    generar_214_llegada(context, pedido, pedido_etapa)
    generar_214_salida(context, pedido, pedido_etapa) 

if __name__ == "__main__":
    """
    Main module
    """
    log.info("=====> Inicio (%s)" % os.getpid())
    retval = 0

    context = Context()
    context.session = None
    context.path = "/FTPSite/WNA/output"
    context.scac = "SEGO"
    context.fecha = datetime.datetime.utcnow()
    context.numero = random.randint(1000, 50000)

    try:
        cp = configparser.ConfigParser()
        cp.read(YAETL_CONFIG)
        
        os.environ["NLS_LANG"] = cp.get("GT","nls_lang")

        engine = create_engine(cp.get("GT","uri"), echo=False)
        context.engine = engine
        
        Session = sessionmaker(bind=engine)
        context.session = Session()
        
        codigo = "10-31586"
        
        ide, id = codigo.split("-")
        pedido = context.session.query(gt.Pedido) \
                .filter(gt.Pedido.ide == int(ide)) \
                .filter(gt.Pedido.id == int(id)) \
                .one_or_none()
        
        if not pedido is None:
            
            pedidos_etapas = context.session.query(gt.PedidosEtapa) \
                    .join(gt.PedidosEtapa.direccione) \
                    .join(gt.Direccione.poblacione) \
                    .join(gt.Direccione.provincia1) \
                    .filter(gt.PedidosEtapa.ide == pedido.ide) \
                    .filter(gt.PedidosEtapa.pedido == pedido.id) \
                    .order_by(gt.PedidosEtapa.etapa) \
                    .all()
            
            for pedido_etapa in pedidos_etapas:
                generar_214(context, pedido, pedido_etapa)

        context.session.commit()

    except Exception as e:
        log.error(e)
        retval = 1
        context.session.rollback()
    finally:
        context.session.close()

    log.info("<===== Fin (%s)" % os.getpid())
    sys.exit(retval)