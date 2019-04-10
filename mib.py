import configparser
import datetime
import decimal
import logging
import openpyxl as excel
import os
import sys
import traceback

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model import gt
from model import mtb
from model import plus_core
from model import plus_site


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
           
def localizar_albaran(context, pedido):

    expid = int(pedido.fuente[2:])
    detail = context.core_ses.query(plus_core.Expeditiondetail) \
            .filter(plus_core.Expeditiondetail.expid == expid) \
            .filter(plus_core.Expeditiondetail.bordero == pedido.referencia_cliente) \
            .one_or_none()
    if detail is None:
        return

    ses = None
    if detail.siteid == 1:
        ses = context.site1_ses
    elif detail.siteid == 3:
        ses = context.site3_ses
    else:
        return None
    
    dnps = ses.query(plus_site.Deliverynotepackage) \
            .filter(plus_site.Deliverynotepackage.id == detail.dnpid) \
            .all()
    if dnps is None:
        return
    for dnp in dnps:
        log.warning("     (%s %s) <===== Posible albarán detectado" %
                     (dnp.deliverynoteorigin, dnp.transportorder))
    


def obtener_gestor_expedicion(context, pedido):
    if pedido.exp_id is None:
        return None
    ot = context.gt_ses.query(gt.OrdenesTransporte) \
            .filter(gt.OrdenesTransporte.ide == pedido.ide) \
            .filter(gt.OrdenesTransporte.exp_id == pedido.exp_id) \
            .first()
    if ot == None:
        return None
    return ot.gestor

def round_int(valor):
    d = decimal.Decimal(valor)
    return int(d.to_integral(rounding = decimal.ROUND_HALF_UP))

def verificar_vda(context, pedido):

    ped = context.gt_ses.query(gt.PedidosEtapasDetalle) \
            .filter(gt.PedidosEtapasDetalle.ide == pedido.ide) \
            .filter(gt.PedidosEtapasDetalle.pedido == pedido.id) \
            .filter(gt.PedidosEtapasDetalle.etapa == 1) \
            .first()
    if ped is None:
        log.warning("     <===== No tiene detalle, saliendo")
        return False

    vdas = obtener_vdas(context, pedido.referencia_cliente, ped.planta_carga, 
                        ped.bastidor)
    if (len(vdas) == 0):
        vdas = obtener_vdas_alternativas(context, pedido.referencia_cliente, 
                                         ped.planta_carga)
        if len(vdas) != 1:
            log.warning("     (%s) (%s) <===== No tiene VDA ni se encuentra otra, saliendo" %
                     (pedido.fuente, ped.bastidor))
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

    if ped.elementos is None:
        ped.elementos = float(ped.ref_cliente)
        log.warning("     Corrigiendo el largo")

    if ped.ref_cliente != pedido.referencia_cliente:
        log.warning("     Corrigiendo bordero")
        ped.ref_cliente = pedido.referencia_cliente
            
    if ped.fecha_ref_cliente is None or \
            ped.fecha_ref_cliente != ti.borderodate:
        log.warning("     Corrigiendo fecha de bordero ... (%s) (%s) "
                    % (ped.fecha_ref_cliente, ti.borderodate))
        ped.fecha_ref_cliente = ti.borderodate
        log.warning("     Corregido")
            
    
    context.gt_ses.commit()
    return True
    
def verificar_fechas(context, pedido):
    
    if not pedido.factura is None:
        return
        
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
    
def verificar_otros_datos(context, pedido):
    ped = context.gt_ses.query(gt.PedidosEtapasDetalle) \
            .filter(gt.PedidosEtapasDetalle.ide == pedido.ide) \
            .filter(gt.PedidosEtapasDetalle.pedido == pedido.id) \
            .filter(gt.PedidosEtapasDetalle.etapa == 1) \
            .first()

    volumengewitch = round_int(ped.volumen * 250)
    if pedido.subtipo == 5:
        volumengewitch = round_int(ped.elementos * 1500)
    if ped.peso_neto != volumengewitch:
        ped.peso_neto = volumengewitch
        log.warning("     Corrigiendo volumengewitch")    
        
    gestor = obtener_gestor_expedicion(context, pedido)
    if not gestor is None and pedido.gestor != gestor:
        pedido.gestor = gestor
        log.warning("     Corrigiendo gestor")    
    
    pedido.alias = "OK"
    context.gt_ses.commit()

def procesar_pedido(context, pedido):
    log.info("     (%s %s)" % (pedido.id, pedido.referencia_cliente))
    if not verificar_vda(context, pedido):
#        localizar_albaran(context, pedido)
        return
    verificar_fechas(context, pedido)
    verificar_otros_datos(context, pedido)

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
        
        e3 = create_engine(cp.get("PLUS","core"), echo=False)
        S3 = sessionmaker(bind=e3)
        context.core_ses = S3()    
        
        e4 = create_engine(cp.get("PLUS","site1"), echo=False)
        S4 = sessionmaker(bind=e4)
        context.site1_ses = S4() 

        e5 = create_engine(cp.get("PLUS","site3"), echo=False)
        S5 = sessionmaker(bind=e5)
        context.site3_ses = S5()         

        procesar_pedidos(context)

    except Exception as e:
        log.error(e)
        log.error(traceback.format_tb(sys.exc_info()[2]))
        retval = 1
    finally:
        context.site3_ses.close()
        context.site1_ses.close()
        context.core_ses.close()
        context.mtb_ses.close()
        context.gt_ses.close()
        
    log.info("<===== Fin (%s)" % os.getpid())
    sys.exit(retval)


