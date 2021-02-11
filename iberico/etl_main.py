import configparser
import datetime as dt
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

    ctx.ped_map = {}
    cf_wo_pedidos = sqlalchemy.Table("wo_pedidos", ctx.cf_metadata, autoload=True)
    stmt = cf_wo_pedidos.select().where(and_(
        cf_wo_pedidos.c.fecha_recogida >= ctx.fromDate,
        cf_wo_pedidos.c.cliente == 37084))
    rows = ctx.cf_engine.execute(stmt).fetchall()
    for pedido in rows:
        if not pedido.slb:
            continue
        slb = None
        try:
            slb = int(pedido.slb)
        except ValueError:
            continue
        if slb not in ctx.ped_map:
            ctx.ped_map[slb] = []
        ctx.ped_map[slb].append(pedido)


def asignar_centro_coste(ctx, albaran):
    """
    Centros de coste y claves de recogida
    """
    puerta = albaran.puerta_destino if albaran.flujo == "VG" else albaran.puerta_origen
    clave = f"PORSCHE:{albaran.fecha_albaran.year}:{puerta}"
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
    cf_mtb_desadv = sqlalchemy.Table("mtb_desadv", ctx.cf_metadata, autoload=True)
    c = cf_mtb_desadv.c

    alias = None
    puerta = None
    if ":" in albaran.puerta_destino:
        alias = albaran.puerta_destino.split(":")[1]
        puerta = albaran.puerta_destino.split(":")[0]

    stmt = cf_mtb_desadv.select().where(and_(
        c.cliente == albaran.cliente,
        c.albaran == albaran.albaran,
        c.alias_origen == albaran.alias_origen,
        c.alias_destino == alias,
        c.puerta_destino == puerta
    ))

    if albaran.slb:
        albaran.slb = albaran.slb.split(":")[0]
    albaran.peso_asn = None
    albaran.volumen_asn = None
    albaran.fecha_recogida_solicitada = None
    albaran.fecha_entrega_solicitada = None
    asn = ctx.cf_engine.execute(stmt).fetchone()
    if not asn:
        if albaran.slb:
            albaran.slb = f"{albaran.slb}:NO ENCONTRADO"
        else:
            albaran.slb = ":NO INFORMADO"
        return

    albaran.peso_asn = asn.peso
    albaran.volumen_asn = asn.volumen
    albaran.fecha_recogida_solicitada = asn.fecha_recogida_solicitada
    albaran.fecha_entrega_solicitada = asn.fecha_entrega_solicitada
    if albaran.slb != asn.documento:
        albaran.slb = f"{albaran.slb}:CORREGIR({asn.documento})"



def asignar_desadv_vacios(ctx, albaran):
    """
    Esta búsqueda es para LGI, con la entrada de schaeffer hay que ampliarla dependiendo
    también de cómo entren sus datos.
    """
    if albaran.slb:
        albaran.slb = albaran.slb.split(":")[0]
    else:
        albaran.slb = ":NO INFORMADO"
    albaran.peso_asn = None
    albaran.volumen_asn = None
    albaran.fecha_recogida_solicitada = None
    albaran.fecha_entrega_solicitada = None

    if not albaran.discovery:
        return

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
        asignar_desadv_vacios(ctx, albaran)

def asignar_pedido(ctx, albaran):
    slb = None
    try:
        slb = int(albaran.slb)
    except ValueError:
        return
    if slb not in ctx.ped_map:
        return

    albaran.pedido_wo = None
    albaran.expedicion_wo = None
    albaran.importe_wo = None
    albaran.peso = None
    albaran.volumen = None
    albaran.peso_facturable = None
    for pedido in ctx.ped_map[slb]:
        if pedido.flujo != albaran.flujo:
            continue
        if pedido.alias_origen != albaran.alias_origen:
            continue
        if pedido.alias_destino != albaran.alias_destino:
            continue
        puerta = albaran.puerta_destino if albaran.flujo == "VG" else albaran.puerta_origen
        if pedido.puerta != puerta:
            continue
        albaran.pedido_wo = pedido.pedido
        albaran.expedicion_wo = pedido.expedicion
        albaran.importe_wo = pedido.importe_total
        # esto hay que cogerlo con pinzas
        if pedido.tarifa:
            albaran.peso = pedido.peso
            albaran.volumen = pedido.volumen
            albaran.peso_facturable = pedido.peso_facturable


def aplicar_cambios(ctx):
    cf_conn = ctx.cf_engine.connect()
    cf_plus_albaranes = sqlalchemy.Table("plus_albaranes", ctx.cf_metadata, autoload=True)

    fila = 0
    stmt = cf_plus_albaranes.select().where(cf_plus_albaranes.c.fecha_albaran >= ctx.fromDate)\
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
        asignar_desadv(ctx, albaran)
        asignar_pedido(ctx, albaran)

        if albaran.fecha_recogida:
            albaran.anno_recogida = albaran.fecha_recogida.year
            albaran.mes_recogida = albaran.fecha_recogida.month + albaran.anno_recogida * 100
            albaran.semana_recogida = albaran.fecha_recogida.isocalendar()[1] + albaran.anno_recogida * 100

        if albaran.fecha_entrega:
            albaran.anno_entrega = albaran.fecha_entrega.year
            albaran.mes_entrega = albaran.fecha_entrega.month + albaran.anno_entrega * 100
            albaran.semana_entrega = albaran.fecha_entrega.isocalendar()[1] + albaran.anno_entrega * 100


        stmt = cf_plus_albaranes.update(None).where(cf_plus_albaranes.c.Id == albaran.Id) \
                .values(albaran.__dict__)
        cf_conn.execute(stmt)


    cf_conn.close()


def cruzar_datos(ctx):
    log.info("-----> Inicio")
    cargar_maps(ctx)
    aplicar_cambios(ctx)
    log.info("<----- Fin")


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)
    log.info("-----> Info")

    cp = configparser.ConfigParser()
    cp.read(os.path.expanduser("~") + "/etc/config.ini")

    ctx = iberico.context.Context(cp)
    ctx.fromDate = dt.date(2020, 11, 1)

    actualizar = False
    if actualizar:
        iberico.etl_wo.run(ctx)
        etl_mtb.run(ctx)
        iberico.etl_plus.run(ctx)

    cruzar_datos(ctx)

    log.info("<----- Fin")