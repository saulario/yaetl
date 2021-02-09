import sqlalchemy

import logging

import context
import model

log = logging.getLogger(__name__)

def borrar_mensajes(ctx):
    log.info("\tBorrando anteriores ...")

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
    log.info("\tTraspasando nuevos ...")

    cf_conn = ctx.cf_engine.connect()
    cf_mtb_desadv = sqlalchemy.Table("mtb_desadv", ctx.cf_metadata, autoload=True)

    log.info("\t\tProcesando ASN")
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
        entity = model.Entity(row)
        if entity.albaranes != 1:
            entity.peso = None
            entity.volume = None
        d = entity.__dict__
        d.pop("albaranes")
        stmt = cf_mtb_desadv.insert(None).values(d)
        cf_conn.execute(stmt)

    """
    En el caso de LGI documento es número de discovery y shipmentid es a la vez albarán y SLB
    """
    log.info("\t\tProcesando vda4945 LGI")
    stmt =  sqlalchemy.sql.text(f"""select 
    37084 as cliente
    , ts.interchangesenderid as emisor
    , ts.interchangerecipientid as receptor
    , ST.PACKAGINGTRANSPORORDER as documento                -- DISCOVERY
    , 'VDA4945-VACIOS' as tipo_documento
    , ts.dateofpreparation as fecha_documento
    , st.shipmentid as albaran                              -- SLB
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
    , ST.PACKAGINGTRANSPORORDER
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

def run(ctx):
    log.info("-----> Procesando datos de MTB")
    borrar_mensajes(ctx)
    procesar_mensajes(ctx)
    log.info("<----- Fin")
