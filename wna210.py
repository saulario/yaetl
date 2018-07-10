import configparser
import datetime
import logging
import os
import random
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

def nombre_fichero(pedido):
    cdn = 'SEGO_210_' + pedido + "_" \
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
            + "*1*P*:\n"
    f.write(buffer)
    
def generar_gs(context, pedido, f):
    buffer = "GS*IM*" + context.scac + "*CWNA" \
            + "*" + context.fecha.strftime("%Y%m%d") \
            + "*" + context.fecha.strftime("%H%M") \
            + "*" + str(context.numero) \
            + "*X*004010" \
            + "\n"     
    f.write(buffer)

    buffer = "ST*210*1" \
            + "\n"     
    f.write(buffer)        
    
# B3**102297679501*1056355*CC*L*20180124*162280**20180118*035*SCAC~    
def generar_b3_c3(context, pedido, factura, f):
        
    buffer = "B3*" \
            + "*" + pedido.fac_num_oficial \
            + "*" + pedido.pedido_cliente \
            + "*CC*L" \
            + "*" + factura.fecha_emision.strftime("%Y%m%d") \
            + "*" + str(int(context.importe_total * 100)) \
            + "*" \
            + "*" + pedido.pet_des_fecha.strftime("%Y%m%d") + "*035" \
            + "*" + context.scac \
            + "\n"     
    f.write(buffer)

    buffer = "C3" \
            + "*" + pedido.moneda \
            + "\n"     
    f.write(buffer)
    
    context.segmentos += 2

def generar_n9(context, pedido, f):    
    buffer = "N9*BM*" \
            + "*%s" % pedido.referencia_cliente \
            + "\n"     
    f.write(buffer)    
    
    buffer = "N9*CN*" \
            + "*%s" % pedido.dim_cliente_1 \
            + "\n"     
    f.write(buffer)    
    
    context.segmentos += 2

def generar_g62(context, pedido, factura, f):    
    buffer = "G62" \
            + "*85*" + factura.fecha_emision.strftime("%Y%m%d") \
            + "\n"     
    f.write(buffer)  
    
    context.segmentos += 1
    
def generar_n1(context, pedido, f):
    
    e1 = context.session.query(gt.PedidosEtapa) \
            .join(gt.Direccione) \
            .filter(gt.PedidosEtapa.ide == pedido.ide) \
            .filter(gt.PedidosEtapa.pedido == pedido.id) \
            .filter(gt.PedidosEtapa.etapa == 1) \
            .first()
            
    buffer = "N1" \
            + "*SH*" + e1.direccione.nombre \
            + "\n"     
    f.write(buffer)  
    
    buffer = "N3" \
            + "*" + e1.direccione.direccion \
            + "\n"     
    f.write(buffer)  

    buffer = "N4" \
            + "*" + e1.direccione.poblacion \
            + "*" + e1.direccione.pais \
            + "*" + e1.direccione.cp \
            + "\n"     
    f.write(buffer)  
            
    e1 = context.session.query(gt.PedidosEtapa) \
            .join(gt.Direccione) \
            .filter(gt.PedidosEtapa.ide == pedido.ide) \
            .filter(gt.PedidosEtapa.pedido == pedido.id) \
            .filter(gt.PedidosEtapa.etapa == 99) \
            .first()   

    buffer = "N1" \
            + "*CN*" + e1.direccione.nombre \
            + "\n"     
    f.write(buffer)  
    
    buffer = "N3" \
            + "*" + e1.direccione.direccion \
            + "\n"     
    f.write(buffer)  

    buffer = "N4" \
            + "*" + e1.direccione.poblacion \
            + "*" + e1.direccione.pais \
            + "*" + e1.direccione.cp \
            + "\n"     
    f.write(buffer)  
    
    context.segmentos += 6
    
def generar_lx(context, pedido, concepto, f)    :
   
    buffer = "LX" \
            + "*" + str(concepto["linea"]) \
            + "\n"     
    f.write(buffer)  

    buffer = "L5" \
            + "*" + str(concepto["linea"]) \
            + "*" + concepto["descripcion"] \
            + "\n"     
    f.write(buffer)     
       
    tipo = "NU"
    
    buffer = "L0" \
            + "*" + str(concepto["linea"]) \
            + "*" + str(concepto["cantidad"]) \
            + "*" + tipo \
            + "\n"     
    f.write(buffer)  
    
    tipo = "FC"
    if concepto["cantidad"] != 1:
        tipo= "PU"
    
    buffer = "L1" \
            + "*" + str(concepto["linea"]) \
            + "*" + str(concepto["precioUnit"]) \
            + "*" + tipo \
            + "*" + str(concepto["precio"]) \
            + "*" \
            + "*" \
            + "*" \
            + "*" + concepto["codigo"] \
            + "\n"     
    f.write(buffer)       
    
    context.segmentos += 4
    
def generar_l3(context, pedido, f):    
    
    buffer = "L3" \
            + "*" \
            + "*" \
            + "*" \
            + "*" \
            + "*" + str(int(context.importe_total * 100)) \
            + "\n"     
    f.write(buffer)  
    
    context.segmentos += 1

def generar_se(context, pedido, f):    
    
    buffer = "SE" \
            + "*" + str(context.segmentos) \
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

def traduce_concepto(cod):
    lista = {
            1: "105",
            7: "UNL",
            24: "370",
            40: "370",
            27: "405",
            39: "APT",
            38: "BLC",
            }
    return lista.get(cod, "MSG")

def generar_210(context, pedido, factura):
    
    context.numero = random.randint(1000, 50000)
    context.segmentos = 2
    context.importe_total = pedido.importe + pedido.pco_importe_extra
    
    fn = context.path + "/" + nombre_fichero("%s-%s" % (pedido.ide, pedido.id))
    with open(fn, "w") as f:
        generar_isa(context, pedido, f)
        generar_gs(context, pedido, f)
        generar_b3_c3(context, pedido, factura, f)
        generar_n9(context, pedido, f)
        generar_g62(context, pedido, factura, f)
#        generar_n1(context, pedido, f)
    
        # L0*1***4345*N***346~
        # L1*1*2.02*FC*143460****
        linea = 1
        c = {}
        c["linea"] = linea
        c["codigo"] = ""
        c["descripcion"] = "Line haul"
        c["cantidad"] = 1
        c["precioUnit"] = pedido.importe
        c["precio"] = int(pedido.importe * 100)
        
        generar_lx(context, pedido, c, f)
        
        conceptos = context.session.query(gt.PedidosConcepto) \
                .filter(gt.PedidosConcepto.ide == pedido.ide) \
                .filter(gt.PedidosConcepto.pedido == pedido.id) \
                .all()
        for concepto in conceptos:
            linea += 1
            c["linea"] = linea
            c["codigo"] = traduce_concepto(concepto.concepto)
            c["descripcion"] = concepto.observaciones
            c["cantidad"] = concepto.cantidad
            c["precioUnit"] = concepto.importe_unidad
            c["precio"] = int(concepto.importe * 100)
            generar_lx(context, pedido, c, f)
            
        generar_l3(context, pedido, f)
        generar_se(context, pedido, f)
    

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

    try:
        cp = configparser.ConfigParser()
        cp.read(YAETL_CONFIG)
        
        os.environ["NLS_LANG"] = cp.get("GT","nls_lang")

        engine = create_engine(cp.get("GT","uri"), echo=False)
        context.engine = engine
        
        Session = sessionmaker(bind=engine)
        context.session = Session()
        
#        codigos = ["10-33555", "10-29613", "10-29584", "10-29755", "10-29614"] 
        codigos = ["10-33555", "10-31607", "10-31609",]
        
        for codigo in codigos:
            
            ide, id = codigo.split("-")
            pedido = context.session.query(gt.Pedido) \
                    .filter(gt.Pedido.ide == int(ide)) \
                    .filter(gt.Pedido.id == int(id)) \
                    .one_or_none()
            
            factura = None
            if not pedido is None:
                factura = context.session.query(gt.FaFactura) \
                        .filter(gt.FaFactura.ide == pedido.ide_factura) \
                        .filter(gt.FaFactura.id == pedido.factura) \
                        .one_or_none()
            
            if pedido and factura:
                generar_210(context, pedido, factura)

        context.session.commit()

    except Exception as e:
        log.error(e)
        retval = 1
        context.session.rollback()
    finally:
        context.session.close()

    log.info("<===== Fin (%s)" % os.getpid())
    sys.exit(retval)