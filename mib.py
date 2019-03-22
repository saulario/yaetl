import configparser
import datetime
import logging
import openpyxl as excel
import os
import sys
import traceback

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model import gt
from model import mtb


YAETL_HOME = ("%s/yaetl" % os.path.expanduser("~"))
YAETL_CONFIG = ("%s/etc/yaetl.config" % YAETL_HOME)
YAETL_LOG = ("%s/log/%s.log" %
             (YAETL_HOME, os.path.basename(__file__).split(".")[0]))
logging.basicConfig(level=logging.INFO, filename=YAETL_LOG,
                    format="%(asctime)s %(levelname)s %(module)s.%(funcName)s %(message)s")
log = logging.getLogger(__name__)

class Context():
    pass


def obtener_pedidos(context):
    return context.gt_ses.query(gt.Pedido) \
            .filter(gt.Pedido.ide == 1) \
            .filter(gt.Pedido.pet_org_fecha >= context.from_date) \
            .filter(gt.Pedido.pet_org_fecha <= context.to_date) \
            .filter(gt.Pedido.estado != 8) \
            .filter(gt.Pedido.tipo == 4) \
            .filter(gt.Pedido.emisor == "IbericoMan") \
            .filter(gt.Pedido.dim_cliente_1 == "37323") \
            .order_by(gt.Pedido.id)
            
def obtener_vdas(context, bordero, proveedor, posicion):
    return context.mtb_ses.query(mtb.Vda4921TransportIdentific, mtb.Vda4921FwdAgentDatum) \
            .join(mtb.Vda4921FwdAgentDatum) \
            .filter(mtb.Vda4921TransportIdentific.bordero.like(bordero + "%")) \
            .filter(mtb.Vda4921FwdAgentDatum.supplierid.like(proveedor + "%")) \
            .filter(mtb.Vda4921FwdAgentDatum.positionnumber == int(posicion)) \
            .all()

def obtener_vdas_alternativas(context, bordero, proveedor):
    return context.mtb_ses.query(mtb.Vda4921TransportIdentific, mtb.Vda4921FwdAgentDatum) \
            .join(mtb.Vda4921FwdAgentDatum) \
            .filter(mtb.Vda4921TransportIdentific.bordero.like(bordero + "%")) \
            .filter(mtb.Vda4921FwdAgentDatum.supplierid.like(proveedor + "%")) \
            .all()


def verificar_vda(context, pedido):

    ped = context.gt_ses.query(gt.PedidosEtapasDetalle) \
            .filter(gt.PedidosEtapasDetalle.ide == pedido.ide) \
            .filter(gt.PedidosEtapasDetalle.pedido == pedido.id) \
            .filter(gt.PedidosEtapasDetalle.etapa == 1) \
            .first()
    if ped is None:
        log.warn("     <===== No tiene detalle, saliendo")
        return False

    vdas = obtener_vdas(context, pedido.referencia_cliente, ped.planta_carga, 
                        ped.bastidor)
    if (len(vdas) == 0):
        vdas = obtener_vdas_alternativas(context, pedido.referencia_cliente, 
                                         ped.planta_carga)
        if len(vdas) != 1:
            log.warn("     (%s) (%s) <===== No tiene VDA ni se encuentra otra, saliendo" %
                     (ped.planta_carga, ped.bastidor))
            return False

        log.warning("     Corrigiendo desde VDA ...")
        ad = vdas[0][1]
        ped.albaran = ped.matricula = ad.freightforwarderorderid.strip()
        ped.bastidor = "{:03d}".format(ad.positionnumber)
        ped.referencia1 = pedido.referencia_cliente + ped.bastidor
        log.warning("     Corregida")

    if (len(vdas) > 1):
        log.warning("     <===== VDA duplicada")
        for vda in vdas:
            ti = vda[0]
            ad = vda[1]
            log.warning("          (%d) (%s) (%s) (%s)" % (ti.messageid, 
                        ti.bordero, ad.supplierid, ad.positionnumber))
        return False
    
    ti = vdas[0][0]
    ad = vdas[0][1]
    
    to = ad.freightforwarderorderid.strip()   
    if ped.albaran.strip() != to:
        log.warning("     Corrigiendo orden de transporte ... (%s) (%s) "
                    % (ped.albaran, to))
        ped.albaran = ped.matricula = to
        log.warning("     Corregido")
        
    if ped.fecha_ref_cliente is None or \
            ped.fecha_ref_cliente != ti.borderodate:
        log.warning("     Corrigiendo fecha de bordero ... (%s) (%s) "
                    % (ped.fecha_ref_cliente, ti.borderodate))
        ped.fecha_ref_cliente = ti.borderodate
        log.warning("     Corregido")
            
    
    context.gt_ses.commit()
    return True
    
def verificar_fechas(context, pedido):
    
    ped = context.gt_ses.query(gt.PedidosEtapasDetalle) \
            .filter(gt.PedidosEtapasDetalle.ide == pedido.ide) \
            .filter(gt.PedidosEtapasDetalle.pedido == pedido.id) \
            .filter(gt.PedidosEtapasDetalle.etapa == 1) \
            .first()
    vda = obtener_vdas(context, pedido.referencia_cliente, ped.planta_carga, 
                        ped.bastidor)[0]
    ti = vda[0]
    ad = vda[1]

    pe01 = context.gt_ses.query(gt.PedidosEtapa) \
            .filter(gt.PedidosEtapa.ide == pedido.ide) \
            .filter(gt.PedidosEtapa.pedido == pedido.id) \
            .filter(gt.PedidosEtapa.etapa == 1) \
            .one()
            
    pe99 = context.gt_ses.query(gt.PedidosEtapa) \
            .filter(gt.PedidosEtapa.ide == pedido.ide) \
            .filter(gt.PedidosEtapa.pedido == pedido.id) \
            .filter(gt.PedidosEtapa.etapa == 99) \
            .one()
    
    if pe01.fecha != ad.freightfrwrdrregistrationdate:
        log.warning("     Corrigiendo fecha de recogida")
        pe01.fecha = ad.freightfrwrdrregistrationdate
    
    if pe99.fecha != ti.estimatedtimeofarrival:
        log.warning("     Corrigiendo fecha de entrega")
        pe99.fecha = ti.estimatedtimeofarrival
        
    context.gt_ses.commit()

def procesar_pedido(context, pedido):
    log.info("     (%s %s)" % (pedido.id, pedido.referencia_cliente))
    if not verificar_vda(context, pedido):
        return
    verificar_fechas(context, pedido)

def procesar_pedidos(context):
    log.info("=====> Inicio")
    
    i = 0
    pedidos = obtener_pedidos(context)    
    for pedido in pedidos:
        i += 1
        procesar_pedido(context, pedido)
    
    log.info("<===== Fin (%d)" % i)
    
    
    
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

    try:
        cp = configparser.ConfigParser()
        cp.read(YAETL_CONFIG)
        
        os.environ["NLS_LANG"] = cp.get("GT","nls_lang")
        
        e1 = create_engine(cp.get("GT","uri"), echo=False)
        S1 = sessionmaker(bind=e1)
        context.gt_ses = S1()
               
        e2 = create_engine(cp.get("MTB","uri"), echo=False)
        S2 = sessionmaker(bind=e2)
        context.mtb_ses = S2()

        procesar_pedidos(context)

    except Exception as e:
        log.error(e)
        log.error(traceback.format_tb(sys.exc_info()[2]))
        retval = 1
    finally:
        context.gt_ses.close()
        context.mtb_ses.close()

    log.info("<===== Fin (%s)" % os.getpid())
    sys.exit(retval)


