import sqlalchemy

import logging

import context
import model

log = logging.getLogger(__name__)

def datos_fecha(f):
    if f is None: return None, None, None
    aa = f.year
    mm = f.month + aa * 100
    ss = f.isocalendar()[1] + aa * 100
    return aa, mm, ss

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
    stmt =  sqlalchemy.sql.text(f"""select
    37084 as cliente
    , am.interchangesenderid as emisor
    , am.interchangerecipientid as receptor
    , am.despatchadvicenumber as documento    
    , am.messageversion as tipo_documento
    , am.despatchadvicedate as fecha_documento
    , ap.deliverynotenumber as albaran
    , am.despatchadvicedate as fecha_recogida    
    , am.shipfromcode as alias_origen
    , am.shipfromduns as alias_origen_duns
    , am.shipfromplaceofloadingid as puerta_origen
    , aco.name as nombre_origen
    , am.requesteddeliverydate as fecha_entrega
    , am.shiptocode as alias_destino
    , am.shiptoduns as alias_destino_duns
    , am.shiptoplaceofdeliveryid as puerta_destino
    , acd.name as nombre_destino
from asn_message am
    join asn_parts ap on ap.asnmessageid = am.id
    left join pre_pluscore.actors aco on substr(aco.alias, 1, 5) = substr(am.shipfromcode, 1, 5)
    left join pre_pluscore.actors acd on substr(acd.alias, 1, 5) = substr(am.shiptocode, 1, 5)
where
    am.filename like '%4987.TXT'
    and ap.deliverynotenumber is not null
    and am.filedate >= :fromDate
group by
    37084
    , am.interchangesenderid
    , am.interchangerecipientid 
    , am.despatchadvicenumber 
    , am.messageversion 
    , am.despatchadvicedate 
    , ap.deliverynotenumber 
    , am.despatchadvicedate 
    , am.shipfromcode 
    , am.shipfromduns 
    , am.shipfromplaceofloadingid 
    , aco.name
    , am.requesteddeliverydate 
    , am.shiptocode 
    , am.shiptoduns 
    , am.shiptoplaceofdeliveryid 
    , acd.name
""")    
    fila = 0
    rows = ctx.mtbm_engine.execute(stmt, fromDate=ctx.fromDate).fetchall()
    for row in rows:
        fila += 1
        if not (fila % 100): log.info(f"\tprocesando ... {fila}")
        d = dict(zip(row.keys(), row.values()))
        d["anno_recogida"], d["mes_recogida"], d["semana_recogida"] = datos_fecha(row.fecha_recogida)
        d["anno_entrega"], d["mes_entrega"], d["semana_entrega"] = datos_fecha(row.fecha_entrega)
        stmt = cf_mtb_desadv.insert(None).values(d)
        cf_conn.execute(stmt)

    return

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
