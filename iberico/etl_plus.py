import logging

import sqlalchemy

import context

log = logging.getLogger(__name__)

def borrar_albaranes(ctx):
    log.info("\tBorrando anteriores...")
    cf_plus_albaranes = sqlalchemy.Table("plus_albaranes", ctx.cf_metadata, autoload=True)
    stmt = cf_plus_albaranes.delete(None).where(cf_plus_albaranes.c.fecha_albaran >= ctx.fromDate)
    ctx.cf_engine.execute(stmt)

def procesar_site(ctx, id):
    log.info(f"\tTraspasando nuevos... {id}")
    cf_conn = ctx.cf_engine.connect()

    cf_plus_albaranes = sqlalchemy.Table("plus_albaranes", ctx.cf_metadata, autoload=True)

    stmt =  sqlalchemy.sql.text(f"""select S.ID AS SITE, dn.id as dnid
    , dnp.deliverynoteorigin as albaran, pua.consignmentreferencenumber AS discovery, dnp.slborigin as slb
    , dn.truck, dn.trailer, dnp.bordero as bordero1, dnp.bordero2
    , cast(dn.receptiondate AS DATE) as FECHA_RECOGIDA
    , CAST(DNP.deliverydate as date) AS FECHA_ENTREGA
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
    S.ID, dn.id
    , dnp.deliverynoteorigin, pua.consignmentreferencenumber, dnp.slborigin
    , dn.truck, dn.trailer, dnp.bordero, dnp.bordero2
    , cast(dn.receptiondate AS DATE), (extract(year from dn.receptiondate) * 100 + extract(month from dn.receptiondate))
    , CAST(DNP.deliverydate as date), (extract(year from dnp.deliverydate) * 100 + extract(month from dnp.deliverydate))
    , CAST(DNP.deliverynotedateorigin as date)
    , ACO.ALIAS, ACO.NAME, NVL(LYO.NAME , ' '), NVL(lyo.farezoneid, 0)
    , ACD.ALIAS, ACD.NAME, NVL(LYD.NAME, ' '), NVL(LYD.FAREZONEID, 0)
    , dnp.loadlistid""")

    rows = ctx.ib_engine.execute(stmt, fromDate=ctx.fromDate).fetchall()
    for row in rows:
        stmt = cf_plus_albaranes.insert(None).values(row)
        cf_conn.execute(stmt)

    cf_conn.close()

def run(ctx):
    log.info("-----> Procesando datos de PLUS")
    borrar_albaranes(ctx)
    procesar_site(ctx, 1)
    procesar_site(ctx, 3)
    log.info("<----- Fin")
