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
    cf_plus_albaranes = sqlalchemy.Table("plus_albaranes", ctx.cf_metadata, autoload=True)
    stmt = cf_plus_albaranes.delete(None).where(cf_plus_albaranes.c.fecha_recogida >= ctx.fromDate)
    ctx.cf_engine.execute(stmt)

def procesar_site(ctx, id):
    ib_conn = ctx.ib_engine.connect()
    cf_conn = ctx.cf_engine.connect()

    cf_plus_albaranes = sqlalchemy.Table("plus_albaranes", ctx.cf_metadata, autoload=True)

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
        albaran = Entity(row)
        stmt = cf_plus_albaranes.insert(None).values(row.__dict__)
        cf_conn.execute(stmt)

    cf_conn.close()
    ib_conn.close()

def procesar_iberico(ctx):
    borrar_albaranes(ctx)
    procesar_site(ctx, 1)
    procesar_site(ctx, 3)



def borrar_pedidos(ctx):
    log.info("Borrando pedidos de wo...")
    cf_wo_pedidos = sqlalchemy.Table("wo_pedidos", ctx.cf_metadata, autoload=True)
    stmt = cf_wo_pedidos.delete(None).where(cf_wo_pedidos.c.fecha_recogida >= ctx.fromDate)
    ctx.cf_engine.execute(stmt)



def procesar_pedidos(ctx):
    log.info("Procesando pedidos de wo...")
    wo_conn = ctx.wo_engine.connect()
    cf_conn = ctx.cf_engine.connect()

    cf_wo_pedidos = sqlalchemy.Table("wo_pedidos", ctx.cf_metadata, autoload=True)
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
        stmt = cf_wo_pedidos.insert(None).values(row)
        cf_conn.execute(stmt)

    cf_conn.close()
    wo_conn.close()

def procesar_wo(ctx):
    borrar_pedidos(ctx)
    procesar_pedidos(ctx)


def borrar_mensajes(ctx):
    log.info("Borrando mensajes edi ...")

    cf_mtb_desadv = sqlalchemy.Table("mtb_desadv", ctx.cf_metadata, autoload=True)
    cf_mtb_insdes = sqlalchemy.Table("mtb_insdes", ctx.cf_metadata, autoload=True)
    cf_mtb_recadv = sqlalchemy.Table("mtb_recadv", ctx.cf_metadata, autoload=True)

    stmt = cf_mtb_desadv.delete(None).where(cf_mtb_desadv.c.fecha_documento >= ctx.fromDate)
    ctx.cf_engine.execute(stmt)
      
    stmt = cf_mtb_insdes.delete(None).where(cf_mtb_insdes.c.fecha_documento >= ctx.fromDate)
    ctx.cf_engine.execute(stmt)

    stmt = cf_mtb_recadv.delete(None).where(cf_mtb_recadv.c.fecha_documento >= ctx.fromDate)
    ctx.cf_engine.execute(stmt)

def procesar_mensajes(ctx):
    log.info("Cargando desadv...")

    cf_conn = ctx.cf_engine.connect()
    cf_mtb_desadv = sqlalchemy.Table("mtb_desadv", ctx.cf_metadata, autoload=True)

    log.info("\tProcesando asn")
    stmt =  sqlalchemy.sql.text(f"""SELECT 
    37084 as cliente
    , m.interchangerecipientid as emisor
    , m.consignmentreferencenumber as documento
    , m.messageversion as tipo_documento
    , m.filedate as fecha_documento
    , p.deliverynotenumber as albaran
    , m.dateofpreparation as fecha_recogida_solicitada
    , m.shipfromcode as alias_origen
    , m.shipfromplaceofloadingid as puerta_origen
    , m.requesteddeliverydate as fecha_entrega_solicitada
    , m.shiptocode as alias_destino
    , m.shiptoplaceofdeliveryid as puerta_destino
    , m.grossweight as peso
    , m.volume as volumen
    , count(distinct p.deliverynotenumber) albaranes
FROM asn_message m
    join asn_parts p on p.asnmessageid = m.id and p.deliverynotenumber is not null
WHERE 
    m.FILENAME LIKE '%4987.TXT'
    and m.filedate >= :fromDate
group by
    37084
    , m.interchangerecipientid
    , m.consignmentreferencenumber
    , m.messageversion
    , m.filedate
    , p.deliverynotenumber
    , m.dateofpreparation
    , m.shipfromcode
    , m.shipfromplaceofloadingid
    , m.requesteddeliverydate
    , m.shiptocode
    , m.shiptoplaceofdeliveryid
    , m.grossweight
    , m.volume

""")    
    rows = ctx.mtbm_engine.execute(stmt, fromDate=ctx.fromDate).fetchall()
    for row in rows:
        entity = Entity(row)
        if entity.albaranes != 1:
            entity.peso = None
            entity.volume = None
        d = entity.__dict__
        d.pop("albaranes")
        stmt = cf_mtb_desadv.insert(None).values(d)
        cf_conn.execute(stmt)

    log.info("\tProcesando vda4945 LGI/Schaeffer")
    stmt =  sqlalchemy.sql.text(f"""select 
    37084 as cliente
    , ts.interchangesenderid as emisor
    , ts.interchangerecipientid as receptor
    , ts.bordero as documento
    , 'VDA4945-VACIOS' as tipo_documento
    , ts.dateofpreparation as fecha_documento
    , st.shipmentid as albaran
    , ts.dateofpreparation as fecha_recogida_solicitada
    , st.shipfromcode as alias_origen
    , st.estimatedtimeofarrival fecha_entrega_solicitada
    , st.shiptocode alias_destino
    , sum(hus.volume) volumen
    , sum(hus.grossweight) peso
from vda_4945_transport_status ts
    join vda_4945_shipment_status st on st.transportstatusid = ts.id
    left join vda_4945_handling_unit_status hus on hus.transportstatusid = st.transportstatusid and hus.shipmentstatusid = st.shipmentstatusid    
where
    ts.interchangesenderid like '%LGI%'    
group by
    37084
    , ts.interchangesenderid
    , ts.interchangerecipientid
    , ts.bordero
    , 'VDA4945-VACIOS'
    , ts.dateofpreparation
    , st.shipmentid
    , ts.dateofpreparation
    , st.shipfromcode
    , st.estimatedtimeofarrival 
    , st.shiptocode
""" )

    rows = ctx.mtbm_engine.execute(stmt, fromDate=ctx.fromDate).fetchall()
    for row in rows:
        stmt = cf_mtb_desadv.insert(None).values(row)
        cf_conn.execute(stmt)


    cf_conn.close()


def procesar_mtb(ctx):
    borrar_mensajes(ctx)
    procesar_mensajes(ctx)


if __name__ == "__main__":
    cp = configparser.ConfigParser()
    cp.read(os.path.expanduser("~") + "/etc/config.ini")

    ctx = context.Context(cp)
    ctx.fromDate = dt.date(2021, 1, 25)

    #procesar_wo(ctx)
    procesar_mtb(ctx)
    #procesar_iberico(ctx)
    

    print("aqui")
    pass




"""
SELECT 
    37084 as cliente
    , m.interchangerecipientid as emisor
    , m.consignmentreferencenumber as documento
    , m.messageversion as tipo_documento
    , m.filedate as fecha_documento
    , p.deliverynotenumber as albaran
    , m.dateofpreparation as fecha_recogida_solicitada
    , m.shipfromcode as alias_origen
    , m.shipfromplaceofloadingid as puerta_origen
    , m.requesteddeliverydate as fecha_entrega_solicitada
    , m.shiptocode as alias_destino
    , m.shiptoplaceofdeliveryid as puerta_destino
    , m.grossweight as peso
    , m.volume as volumen
    , count(distinct p.deliverynotenumber) albaranes
FROM asn_message m
    join asn_parts p on p.asnmessageid = m.id and p.deliverynotenumber is not null
WHERE 
    m.FILENAME LIKE '%4987.TXT'
group by
    37084
    , m.interchangerecipientid
    , m.consignmentreferencenumber
    , m.messageversion
    , m.filedate
    , p.deliverynotenumber
    , m.dateofpreparation
    , m.shipfromcode
    , m.shipfromplaceofloadingid
    , m.requesteddeliverydate
    , m.shiptocode
    , m.shiptoplaceofdeliveryid
    , m.grossweight
    , m.volume
"""
