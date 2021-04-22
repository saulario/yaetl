import configparser
import datetime as dt
import json
import logging
import os

import sqlalchemy

from sqlalchemy import and_, select

import iberico.context


log = logging.getLogger(__name__)


def esta_configurado(ctx):
    log.info("-----> Inicio")
    retval = False
    pp_t = sqlalchemy.Table("parametros", ctx.cf_metadata, autoload=True)
    stmt = pp_t.select().where(pp_t.c.id == "ACTUALIZAR_SLB_ASN")
    row = ctx.cf_engine.execute(stmt).fetchone()
    if row:
        retval = True
        parametros = json.loads(row.parametros)
        ctx.fromDate = dt.date.fromisoformat(parametros.get("fromDate"))
        log.info(f"\t(fromDate): {ctx.fromDate}")
    log.info("<----- Fin")
    return retval

def buscar_slb(ctx, albaran):

    fd = albaran.fecha_albaran - dt.timedelta(days=15)
    td = albaran.fecha_albaran + dt.timedelta(days=15)

    am = sqlalchemy.Table("asn_message", ctx.mtbm_metadata, autoload=True)
    ap = sqlalchemy.Table("asn_parts", ctx.mtbm_metadata, autoload=True)

    puerta = None
    if albaran.puerta_destino:
        puerta = albaran.puerta_destino.split(":")[0]
        planta = albaran.puerta_destino.split(":")[1]

    j1 = am.join(ap, ap.c.asnmessageid == am.c.id)
    stmt = select([am.c.despatchadvicenumber, am.c.despatchadvicedate, 
            am.c.consignmentreferencenumber,
            am.c.shipfromcode, 
            am.c.shipfromduns,
            am.c.shiptocode, 
            am.c.shiptoduns,
            am.c.shiptoplaceofdeliveryid,
            ap.c.deliverynotenumber
        ]).select_from(j1)\
        .where(and_(
            am.c.filename.like(f"%4987.TXT"),
            am.c.despatchadvicedate.between(fd, td),
            am.c.shipfromcode.like(f"%{albaran.alias_origen}%"),
            am.c.shiptocode == planta,
            #am.c.shiptoplaceofdeliveryid == puerta,
            ap.c.deliverynotenumber != None,
        ))

    log.info(f"\t(origen): {albaran.alias_origen}\t(destino): {albaran.alias_destino}"
            f"\t{albaran.puerta_destino}\t(albaran): {albaran.albaran}")

    try:
        alb = int(albaran.albaran)
    except:
        alb = None

    retval = None
    asns = ctx.mtbm_engine.execute(stmt).fetchall()
    for asn in asns:
        if not alb: continue
        try:
            dn = int(asn.deliverynotenumber)
        except:
            dn = None
        if alb == dn:
            log.info(f"\t\t\tEncontrado {asn.shipfromcode}:{asn.shiptocode}:{asn.shiptoplaceofdeliveryid}"
                    f":{asn.deliverynotenumber}")
            retval = asn.consignmentreferencenumber
            break

    return retval

def procesar_albaranes(ctx):
    
    cf_plus_albaranes = sqlalchemy.Table("plus_albaranes", ctx.cf_metadata, autoload=True)
    stmt = cf_plus_albaranes.select().where(and_(
        cf_plus_albaranes.c.cliente == 37084,
        cf_plus_albaranes.c.fecha_albaran >= ctx.fromDate,
        cf_plus_albaranes.c.alias_destino == 'LGI',
        cf_plus_albaranes.c.slb == None
    ))
    albaranes = ctx.cf_engine.execute(stmt).fetchall()
    total = len(albaranes)
    encontrados = 0
    for albaran in albaranes:
        slb = buscar_slb(ctx, albaran)
        if slb: encontrados += 1
            
    log.info(f"(total): {total}, (encontrados): {encontrados}")


def main():
    cp = configparser.ConfigParser()
    cp.read(os.path.expanduser("~") + "/etc/config.ini")
    ctx = iberico.context.Context(cp)
    if esta_configurado(ctx):
        procesar_albaranes(ctx)

if __name__ == "__main__":
    filename = os.path.expanduser("~") + "/log/asignar_slb_asn.log"
    logging.basicConfig(level=logging.DEBUG, filename=filename,
            format="%(asctime)s %(levelname)s %(thread)d %(processName)s %(module)s %(funcName)s %(message)s" )
    log.info("-----> Info")
    try:
        main()
    except:
        log.error("Se ha producido una excepción no controlada...", exc_info=True)
    log.info("<----- Fin")