import configparser
import datetime as dt
import json
import logging
import os

import sqlalchemy, sqlalchemy.sql

import iberico.context
import iberico.etl_mtb
import iberico.etl_plus
import iberico.etl_wo
import iberico.model

from sqlalchemy import and_

log = logging.getLogger(__name__)

def cargar_maps(ctx):

    cf_centros_coste = sqlalchemy.Table("centros_coste", ctx.cf_metadata, autoload=True)
    rows = ctx.cf_engine.execute(cf_centros_coste.select()).fetchall()
    ctx.cc_map = { x.id:x for x in rows }

    cf_plus_albaranes = sqlalchemy.Table("plus_albaranes", ctx.cf_metadata, autoload=True)
    stmt = cf_plus_albaranes.select().where(cf_plus_albaranes.c.fecha_albaran >= ctx.fromDate)
    rows = ctx.cf_engine.execute(stmt).fetchall()
    ctx.alb_map = {}
    for row in rows:
        if row.albaran not in ctx.alb_map:
            ctx.alb_map[row.albaran]  = []
        ctx.alb_map[row.albaran].append(row)

    # hay que hacer 2 maps porque hay pedidos en los que no caben toda la lista de
    # albaranes y hay que asumir que están en la ruta
    ctx.ped_map = {}
    ctx.ped_fuente = {}
    fd = ctx.fromDate - dt.timedelta(days=15)
    cf_wo_pedidos = sqlalchemy.Table("wo_pedidos", ctx.cf_metadata, autoload=True)
    stmt = cf_wo_pedidos.select().where(and_(
        cf_wo_pedidos.c.fecha_recogida >= fd,
        cf_wo_pedidos.c.cliente == 37084))
    pedidos = ctx.cf_engine.execute(stmt).fetchall()
    for pedido in pedidos:
        for albaran in [ x.strip() for x in (pedido.albaranes or "").split(",") ]:
            if albaran not in ctx.ped_map:
                ctx.ped_map[albaran] = []
            ctx.ped_map[albaran].append(pedido)
            if pedido.fuente not in ctx.ped_fuente:
                ctx.ped_fuente[pedido.fuente] = []
            ctx.ped_fuente[pedido.fuente].append(pedido)

    # albaranes recibidos en desadv pero eliminando ceros iniciales
    ctx.desadv_map = {}
    cf_mtb_desadv = sqlalchemy.Table("mtb_desadv", ctx.cf_metadata, autoload=True)
    stmt = cf_mtb_desadv.select().where(cf_mtb_desadv.c.fecha_documento >= fd)
    mensajes = ctx.cf_engine.execute(stmt).fetchall()
    for mensaje in mensajes:
        albaran = None
        try:
            albaran = int(mensaje.albaran)
        except:
            continue
        if albaran not in ctx.desadv_map:
            ctx.desadv_map[albaran] = []
        ctx.desadv_map[albaran].append(mensaje)


def asignar_centro_coste(ctx, albaran):
    """
    Centros de coste y claves de recogida
    """
    puerta = albaran.puerta_destino if albaran.flujo == "VG" else albaran.puerta_origen
    clave = f"PORSCHE:{albaran.fecha_recogida.year}:{puerta}"
    cc = ctx.cc_map.get(clave, None)
    albaran.centro_coste = None
    albaran.conso_fecha_entrega = None
    albaran.conso_fecha_entrega = None
    if not cc:
        return
    albaran.centro_coste = cc.id
    if albaran.flujo == "VG":
        albaran.conso_fecha_recogida = f"{albaran.fecha_recogida.isoformat()}:{albaran.alias_origen}:{cc.cc1}"
        albaran.conso_fecha_entrega = f"{albaran.fecha_recogida.isoformat()}:{albaran.alias_origen}:{cc.cc1}"        
    else:
        albaran.conso_fecha_recogida = f"{albaran.fecha_recogida.isoformat()}:{cc.cc2}:{albaran.alias_destino}"
        albaran.conso_fecha_entrega = f"{albaran.fecha_recogida.isoformat()}:{cc.cc2}:{albaran.alias_destino}"            


def asignar_desadv_llenos(ctx, albaran):

    numalb = None
    try:
        numalb = int(albaran.albaran)
    except Exception:
        numalb = None
    if not numalb: return

    if albaran.slb:
        albaran.slb = albaran.slb.split(":")[0]

    mensajes = ctx.desadv_map.get(numalb)
    if not mensajes: 
        albaran.slb = f"{albaran.slb or ''}:NO ENCONTRADO:"
        return

    o1 = (albaran.alias_origen + "0"*5)[:5]

    encontrado = False
    for mensaje in mensajes:
        o2 = (mensaje.emisor + "0"*5)[:5]
        o3 = (mensaje.alias_origen + "0"*5)[:5]
        if (o1 == o2 or o1 == o3):
            albaran.fecha_recogida_solicitada = mensaje.fecha_recogida
            albaran.fecha_entrega_solicitada = mensaje.fecha_entrega
            try:
                slb1 = int(albaran.slb)
            except:
                slb1 = None
            try:
                slb2 = int(mensaje.documento)
            except:
                slb2 = None
            if slb1 != slb2:
                albaran.slb = f"{albaran.slb or ''}:CORREGIR:{mensaje.documento}"
            encontrado = True
            break

    if not encontrado: 
        albaran.slb = f"{albaran.slb or ''}:NO ENCONTRADO:"
        return


def asignar_desadv_vacios(ctx, albaran):
    """
    Esta búsqueda es para LGI, con la entrada de schaeffer hay que ampliarla dependiendo
    también de cómo entren sus datos.
    """
    if albaran.slb:
        albaran.slb = albaran.slb.split(":")[0]
    else:
        albaran.slb = ":NO INFORMADO:"
    albaran.peso_asn = None
    albaran.volumen_asn = None
    albaran.fecha_recogida_solicitada = None
    albaran.fecha_entrega_solicitada = None

    cf_mtb_desadv = sqlalchemy.Table("mtb_desadv", ctx.cf_metadata, autoload=True)
    c = cf_mtb_desadv.c
    stmt = cf_mtb_desadv.select().where(and_(
        c.cliente == albaran.cliente,
        c.emisor == 'O0013003102LGI',
        c.documento == albaran.discovery
    ))

    asn = ctx.cf_engine.execute(stmt).fetchone()
    if not asn:
        albaran.slb = f"{albaran.slb}:NO ENCONTRADO"
        return


    albaran.peso_asn = asn.peso
    albaran.volumen_asn = asn.volumen
    albaran.fecha_recogida_solicitada = asn.fecha_recogida_solicitada
    albaran.fecha_entrega_solicitada = asn.fecha_entrega_solicitada
    if albaran.slb != asn.albaran:
        albaran.slb = f"{albaran.albaran}:CORREGIR({asn.documento})"









def asignar_desadv(ctx, albaran):
    if albaran.flujo == "VG":
        asignar_desadv_llenos(ctx, albaran)
    else:
        #asignar_desadv_vacios(ctx, albaran)
        pass

def asignar_pedido(ctx, albaran):

    if albaran.pedido_wo:
        return

    albaran.pedido_wo = None
    albaran.expedicion_wo = None
    albaran.importe_wo = None
    albaran.peso = None
    albaran.volumen = None
    albaran.peso_facturable = None
    albaran.directo = 1 if albaran.bordero1 == albaran.bordero2 else 0

    for pedido in ctx.ped_map.get(albaran.albaran) or []:
        if pedido.flujo != albaran.flujo:
            continue
        if (pedido.alias_origen != albaran.alias_origen and
            pedido.alias_destino != albaran.alias_destino):
            continue
        albaran.pedido_wo = pedido.pedido
        albaran.expedicion_wo = pedido.expedicion
        albaran.importe_wo = pedido.importe_total
        albaran.facturaid_wo = pedido.facturaid
        # esto no se puede porque no tenemos los datos a nivel de albaran
        break
    if albaran.pedido_wo:
        return

    # si no se han encontrado por albarán hay que buscar en la HR/EX más probable
    if albaran.flujo == "VG":
        fuente = f"PLUS_EX_{albaran.expedicion}" if not albaran.directo else f"PLUS_HR_{albaran.hoja_ruta}"
    else:
        fuente = f"PLUS_HR_{albaran.hoja_ruta}" if not albaran.directo else f"PLUS_EX_{albaran.expedicion}"

    pedidos = ctx.ped_fuente.get(fuente) or []
    for pedido in pedidos:
        if pedido.flujo != albaran.flujo:
            continue
        if (pedido.alias_origen != albaran.alias_origen and
            pedido.alias_destino != albaran.alias_destino):
            continue
        albaran.pedido_wo = pedido.pedido
        albaran.expedicion_wo = pedido.expedicion
        albaran.importe_wo = pedido.importe_total
        albaran.facturaid_wo = pedido.facturaid
        break


def aplicar_cambios(ctx):
    cf_conn = ctx.cf_engine.connect()
    cf_plus_albaranes = sqlalchemy.Table("plus_albaranes", ctx.cf_metadata, autoload=True)

    fila = 0
    stmt = cf_plus_albaranes.select().where(cf_plus_albaranes.c.fecha_recogida >= ctx.fromDate)\
                .order_by(cf_plus_albaranes.c.fecha_albaran)
    result = cf_conn.execute(stmt).fetchall()
    for row in result:

        fila += 1
        if not (fila % 100):
            log.info(f"\tprocesando ... {fila}")

        albaran = iberico.model.PlusAlbaran(row)
        albaran.cliente = 37084
        albaran.flujo = "VG" if albaran.zt_destino == 370 else "LG"
        asignar_centro_coste(ctx, albaran)

        if not albaran.fecha_albaran: albaran.fecha_albaran = albaran.fecha_recogida        

        if albaran.fecha_recogida:
            albaran.anno_recogida = albaran.fecha_recogida.year
            albaran.mes_recogida = albaran.fecha_recogida.month + albaran.anno_recogida * 100
            albaran.semana_recogida = albaran.fecha_recogida.isocalendar()[1] + albaran.anno_recogida * 100
            
        if albaran.fecha_entrega:
            albaran.anno_entrega = albaran.fecha_entrega.year
            albaran.mes_entrega = albaran.fecha_entrega.month + albaran.anno_entrega * 100
            albaran.semana_entrega = albaran.fecha_entrega.isocalendar()[1] + albaran.anno_entrega * 100

        asignar_desadv(ctx, albaran)
        asignar_pedido(ctx, albaran)

        stmt = cf_plus_albaranes.update(None).where(cf_plus_albaranes.c.Id == albaran.Id) \
                .values(albaran.__dict__)
        cf_conn.execute(stmt)


    cf_conn.close()


def cruzar_datos(ctx):
    log.info("-----> Inicio")
    cargar_maps(ctx)
    aplicar_cambios(ctx)
    log.info("<----- Fin")


def esta_configurado(ctx):
    log.info("-----> Inicio")
    retval = False
    pp_t = sqlalchemy.Table("parametros", ctx.cf_metadata, autoload=True)
    stmt = pp_t.select().where(pp_t.c.id == "ETL_IBERICO")
    row = ctx.cf_engine.execute(stmt).fetchone()
    if row:
        retval = True
        parametros = json.loads(row.parametros)
        ctx.fromDate = dt.date.fromisoformat(parametros.get("fromDate"))
        log.info(f"\t(fromDate): {ctx.fromDate}")
    log.info("<----- Fin")
    return retval


def main():
    cp = configparser.ConfigParser()
    cp.read(os.path.expanduser("~") + "/etc/config.ini")
    ctx = iberico.context.Context(cp)
    if esta_configurado(ctx):
        #iberico.etl_wo.run(ctx)
        #iberico.etl_mtb.run(ctx)
        #iberico.etl_plus.run(ctx)
        cruzar_datos(ctx)

if __name__ == "__main__":
    filename = os.path.expanduser("~") + "/log/etl_iberico.log"
    logging.basicConfig(level=logging.DEBUG, filename=filename,
            format="%(asctime)s %(levelname)s %(thread)d %(processName)s %(module)s %(funcName)s %(message)s" )
    log.info("-----> Info")
    try:
        main()
    except:
        log.error("Se ha producido una excepción no controlada...", exc_info=True)
    log.info("<----- Fin")