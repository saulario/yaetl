
import sqlalchemy
import sqlalchemy.sql

if __name__ == "__main__":

    site = "PRE_SITE1"

    engine = sqlalchemy.create_engine("oracle+cx_oracle://PRE_PLUSCORE:CORE@db0.sese.com:1521/?service_name=sese11g&encoding=UTF-8&nencoding=UTF-8")
    metadata = sqlalchemy.MetaData(bind=engine)

    dnp = sqlalchemy.Table("DELIVERYNOTEPACKAGES", metadata, schema=site, autoload=True)
    stmt = dnp.select().where(dnp.c.dnid == 1172594)

    conn = engine.connect()

    rows = conn.execute(stmt).fetchall()
    for row in rows:
        print(row)

    stmt = sqlalchemy.sql.text(
    """
select S.ID AS SITE, dn.id dnid, dnp.deliverynoteorigin as albaran, pua.consignmentreferencenumber AS discovery, dnp.slborigin
    , dn.truck, dn.trailer, dnp.bordero as bordero1, dnp.bordero2
    , cast(dn.receptiondate AS DATE) as FECHA_RECOGIDA, (extract(year from dn.receptiondate) * 100 + extract(month from dn.receptiondate)) as MES_RECOGIDA
    , CAST(DNP.deliverydate as date) AS FECHA_ENTREGA, (extract(year from dnp.deliverydate) * 100 + extract(month from dnp.deliverydate)) as MES_ENTREGA
    , cast(dnp.deliverynotedateorigin as date) as FECHA_ALBARAN
    , ACO.ALIAS AS ALIAS_ORIGEN, ACO.NAME AS NOMBRE_ORIGEN,  NVL(LYO.NAME , ' ') AS PUERTA_ORIGEN, NVL(lyo.farezoneid, 0) AS ZT_ORIGEN
    , ACD.ALIAS AS ALIAS_DESTINO, ACD.NAME AS NOMBRE_DESTINO, NVL(LYD.NAME, ' ') AS PUERTA_DESTINO, NVL(LYD.FAREZONEID, 0) AS ZT_DESTINO    
    , dnp.loadlistid as hoja_ruta
    , min(ed.expid) expedicion
    , sum(dnp.weight) as peso
    , sum(puap.weight) as peso_discovery
    , count(dnp.id) as dnips
from pre_site1.deliverynotes dn
    JOIN pre_site1.SITE S ON 1=1
    join pre_site1.deliverynotepackages dnp on dnp.dnid = dn.id
    LEFT JOIN PRE_PLUSCORE.ACTORS ACO ON ACO.ID = dn.actoridorigin
    LEFT JOIN PRE_PLUSCORE.layouts LYO ON LYO.ID = dn.layoutidorigin    
    LEFT JOIN PRE_PLUSCORE.ACTORS ACD ON ACD.ID = dnp.actoriddestiny
    LEFT JOIN PRE_PLUSCORE.LAYOUTS LYD ON LYD.ID = dnp.layoutiddestiny
    LEFT JOIN pre_site1.pickupadvicepackages PUAP ON PUAP.ID = dnp.puapid
    LEFT JOIN pre_site1.pickupadvices PUA ON PUA.ID = PUAP.PUAID    
    LEFT JOIN PRE_PLUSCORE.EXPEDITIONDETAILS ED ON ED.DNPID = DNP.ID and ed.siteid = s.id
where
    (lyo.farezoneid = 370 or lyd.farezoneid = 370)
group by 
    S.ID, dn.id, dnp.deliverynoteorigin, pua.consignmentreferencenumber, dnp.slborigin
    , dn.truck, dn.trailer, dnp.bordero, dnp.bordero2
    , cast(dn.receptiondate AS DATE), (extract(year from dn.receptiondate) * 100 + extract(month from dn.receptiondate))
    , CAST(DNP.deliverydate as date), (extract(year from dnp.deliverydate) * 100 + extract(month from dnp.deliverydate))
    , CAST(DNP.deliverynotedateorigin as date)
    , ACO.ALIAS, ACO.NAME, NVL(LYO.NAME , ' '), NVL(lyo.farezoneid, 0)
    , ACD.ALIAS, ACD.NAME, NVL(LYD.NAME, ' '), NVL(LYD.FAREZONEID, 0)
    , dnp.loadlistid
order by dn.id
    """)

    conn = engine.connect()
    rows = conn.execute(stmt).fetchall()
    for row in rows:
        print(row)

    conn.close()