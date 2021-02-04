import configparser
import datetime as dt
import logging
import os

import context

import sqlalchemy, sqlalchemy.sql


log = logging.getLogger(__name__)


class Entity():

    def __init__(self, proxy):
        for key in proxy.iterkeys():
            setattr(self, key, proxy[key])


def borrar_albaranes(ctx):
    log.info("Borrando anteriores...")
    cf_albaranes = sqlalchemy.Table("albaranes", ctx.cf_metadata, autoload=True)
    stmt = cf_albaranes.delete(None).where(cf_albaranes.c.fecha_recogida >= ctx.fromDate)
    ctx.cf_engine.execute(stmt)

def procesar_site(ctx, id):
    ib_conn = ctx.ib_engine.connect()
    cf_conn = ctx.cf_engine.connect()

    cf_albaranes = sqlalchemy.Table("albaranes", ctx.cf_metadata, autoload=True)

    stmt =  sqlalchemy.sql.text(f"""select S.ID AS SITE, dnp.deliverynoteorigin as albaran, pua.consignmentreferencenumber AS discovery, dnp.slborigin as slb
    , dn.truck, dn.trailer, dnp.bordero as bordero1, dnp.bordero2
    , cast(dn.receptiondate AS DATE) as FECHA_RECOGIDA, (extract(year from dn.receptiondate) * 100 + extract(month from dn.receptiondate)) as MES_RECOGIDA
    , CAST(DNP.deliverydate as date) AS FECHA_ENTREGA, (extract(year from dnp.deliverydate) * 100 + extract(month from dnp.deliverydate)) as MES_ENTREGA
    , cast(dnp.deliverynotedateorigin as date) as FECHA_ALBARAN
    , ACO.ALIAS AS ALIAS_ORIGEN, ACO.NAME AS NOMBRE_ORIGEN,  NVL(LYO.NAME , ' ') AS PUERTA_ORIGEN, NVL(lyo.farezoneid, 0) AS ZT_ORIGEN
    , ACD.ALIAS AS ALIAS_DESTINO, ACD.NAME AS NOMBRE_DESTINO, NVL(LYD.NAME, ' ') AS PUERTA_DESTINO, NVL(LYD.FAREZONEID, 0) AS ZT_DESTINO    
    , dnp.loadlistid as hoja_ruta
    , min(ed.expid) expedicion
    , sum(dnp.weight) as peso_plus
    , sum(puap.weight) as peso_discovery
from PRE_SITE{id}.deliverynotes dn
    JOIN PRE_SITE{id}.SITE S ON 1=1
    join PRE_SITE{id}.deliverynotepackages dnp on dnp.dnid = dn.id
    LEFT JOIN PRE_PLUSCORE.ACTORS ACO ON ACO.ID = dn.actoridorigin
    LEFT JOIN PRE_PLUSCORE.layouts LYO ON LYO.ID = dn.layoutidorigin    
    LEFT JOIN PRE_PLUSCORE.ACTORS ACD ON ACD.ID = dnp.actoriddestiny
    LEFT JOIN PRE_PLUSCORE.LAYOUTS LYD ON LYD.ID = dnp.layoutiddestiny
    LEFT JOIN PRE_SITE{id}.pickupadvicepackages PUAP ON PUAP.ID = dnp.puapid
    LEFT JOIN PRE_SITE{id}.pickupadvices PUA ON PUA.ID = PUAP.PUAID    
    LEFT JOIN PRE_PLUSCORE.EXPEDITIONDETAILS ED ON ED.DNPID = DNP.ID and ed.siteid = s.id
where
    (lyo.farezoneid = 370 or lyd.farezoneid = 370)
    and cast(dn.receptiondate as date) >= :fromDate
group by 
    S.ID, dnp.deliverynoteorigin, pua.consignmentreferencenumber, dnp.slborigin
    , dn.truck, dn.trailer, dnp.bordero, dnp.bordero2
    , cast(dn.receptiondate AS DATE), (extract(year from dn.receptiondate) * 100 + extract(month from dn.receptiondate))
    , CAST(DNP.deliverydate as date), (extract(year from dnp.deliverydate) * 100 + extract(month from dnp.deliverydate))
    , CAST(DNP.deliverynotedateorigin as date)
    , ACO.ALIAS, ACO.NAME, NVL(LYO.NAME , ' '), NVL(lyo.farezoneid, 0)
    , ACD.ALIAS, ACD.NAME, NVL(LYD.NAME, ' '), NVL(LYD.FAREZONEID, 0)
    , dnp.loadlistid""")

    rows = ib_conn.execute(stmt, fromDate=ctx.fromDate).fetchall()
    for row in rows:
        stmt = cf_albaranes.insert(None).values(row)
        result = cf_conn.execute(stmt)

    cf_conn.close()
    ib_conn.close()

def procesar_iberico(ctx):
    borrar_albaranes(ctx)
    procesar_site(ctx, 1)
    procesar_site(ctx, 3)



def borrar_pedidos(ctx):
    log.info("Borrando pedidos...")
    cf_pedidos = sqlalchemy.Table("pedidos", ctx.cf_metadata, autoload=True)
    stmt = cf_pedidos.delete(None).where(cf_pedidos.c.fecha_recogida >= ctx.fromDate)
    ctx.cf_engine.execute(stmt)



def procesar_pedidos(ctx):
    wo_conn = ctx.wo_engine.connect()
    cf_conn = ctx.cf_engine.connect()

    cf_pedidos = sqlalchemy.Table("pedidos", ctx.cf_metadata, autoload=True)
    stmt =  sqlalchemy.sql.text(f"""select p.ide, p.id as pedido, p.exp_id as expedicion, p.cliente, p.estado, p.factura as facturaid, p.fac_num_oficial as factura
    , p.importe importe_tarifa, p.pco_importe_extra importe_conceptos, (p.importe + nvl(p.pco_importe_extra, 0)) as importe_total
    , p.fuente
    , case
        when p.subtipo = 1 then 'VG'
        else 'LG'
      end as flujo
    , cast(p.pet_org_fecha as date) fecha_recogida, p.dir_org_alias alias_origen
    , cast(p.pet_des_fecha as date) fecha_entrega, p.dir_des_alias alias_destino
    , ped.albaran as slb
    , ped.detalle_cliente as puerta
    , ped.peso_bruto as peso, ped.volumen as volumen, peso_neto as peso_facturable
    , p.observaciones as albaranes
from pedidos p
    join pedidos_etapas_detalle ped on ped.ide=p.ide and ped.pedido=p.id
where
p.ide = 1
and cast(p.fecha_pedido as DATE) >= :fromDate
and p.emisor = 'SB_IBERIAN'
AND P.CLIENTE = '37084'
and p.estado <> '8'
""")

    rows = wo_conn.execute(stmt, fromDate=ctx.fromDate).fetchall()
    for row in rows:
        stmt = cf_pedidos.insert(None).values(row)
        result = cf_conn.execute(stmt)

    cf_conn.close()
    wo_conn.close()

def procesar_wo(ctx):
    borrar_pedidos(ctx)
    procesar_pedidos(ctx)

if __name__ == "__main__":
    cp = configparser.ConfigParser()
    cp.read(os.path.expanduser("~") + "/etc/config.ini")

    ctx = context.Context(cp)
    ctx.fromDate = dt.date(2020, 1, 1)

    #procesar_iberico(ctx)
    procesar_wo(ctx)

    print("aqui")
    pass





