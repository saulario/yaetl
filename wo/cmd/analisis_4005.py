import configparser
import datetime as dt
import logging
import os
import re

import sqlalchemy
from sqlalchemy import and_

import wo.context
import wo.model


pattern = re.compile(r"^(PLUS_(?P<TIPO>HR|EX)_)(?P<ID>\d+)$")

zonas_no_vw = {
    369 : "MAN",
    370 : "PORSCHE",
}

log = logging.getLogger(__name__)

def buscar_expedicion(ctx, ruta, site):

    return []

def buscar_hoja_de_ruta(ctx, ruta, site):

    dnp_t = sqlalchemy.Table("deliverynotepackages", ctx.ibsite_metadata, schema=f"pre_site{site}", autoload=True).alias("dnp")
    dn_t = sqlalchemy.Table("deliverynotes", ctx.ibsite_metadata, schema=f"pre_site{site}", autoload=True).alias("dn")
    lyo_t = sqlalchemy.Table("layouts", ctx.ibcore_metadata, autoload=True).alias("lyo")
    lyd_t = sqlalchemy.Table("layouts", ctx.ibcore_metadata, autoload=True).alias("lyd")

    stmt = sqlalchemy.select([dn_t, lyo_t, dnp_t, lyd_t]).apply_labels()\
            .select_from(dnp_t.outerjoin(lyd_t, lyd_t.c.id == dnp_t.c.layoutiddestiny))\
            .select_from(dn_t.outerjoin(lyo_t, lyo_t.c.id == dn_t.c.layoutidorigin))\
            .where(and_(
                dnp_t.c.loadlistid == ruta,
                dn_t.c.id == dnp_t.c.dnid,
            ))
    return ctx.ib_engine.execute(stmt).fetchall()

def buscar_packages(ctx, pedido, site):

    matched = pattern.match(pedido.fuente)
    if not matched:
        return []

    ruta = matched.group("ID")
    tipo = matched.group("TIPO")

    retval = []
    if tipo == "EX":
        retval = buscar_expedicion(ctx, ruta, site)
    elif tipo == "HR":
        retval = buscar_hoja_de_ruta(ctx, ruta, site)
    return retval


def analizar_packages(ctx, pedido, site):
    total = vw = man = porsche = 0

    dnps = buscar_packages(ctx, pedido, site)
    for dnp in dnps:
        total += 1
        if dnp.lyo_farezoneid == 369 or dnp.lyd_farezoneid == 369:
            man += 1
        elif dnp.lyo_farezoneid == 370 or dnp.lyd_farezoneid == 370:
            porsche += 1

    return total, vw, man, porsche


def procesar_delegacion(ctx, fromDate, delegacion):
    log.info("-----> Inicio")
    log.info(f"\t(fromDate)..: {fromDate}")
    log.info(f"\t(delegacion): {delegacion}")

    site = 1 if delegacion == 80 else 3

    pedidos_t = sqlalchemy.Table("pedidos", ctx.wo_metadata, autoload="True")
    stmt = pedidos_t.select().where(and_(
        pedidos_t.c.ide == 1,
        pedidos_t.c.fecha_pedido >= fromDate,
        pedidos_t.c.fuente.like('PLUS_%'),
        pedidos_t.c.estado != '8',
        pedidos_t.c.cliente == 4005,
        pedidos_t.c.delegacion == delegacion
    ))
    fila = 0
    pedidos = ctx.wo_engine.execute(stmt).fetchall()
    for pedido in pedidos:
        fila += 1
        if not (fila % 100):
            log.info(f"\tprocesando ... {fila}")    

        total, vw, man, porsche = analizar_packages(ctx, pedido, site)
        log.info (f"\t\tRuta\t{pedido.fuente} {pedido.fecha_pedido}\t(total)\t{total}" 
                f"\t{vw}\t{man}\t{porsche}")

    log.info("<----- Fin")

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    log.info("-----> Info")

    cp = configparser.ConfigParser()
    cp.read(os.path.expanduser("~") + "/etc/config.ini")
    ctx = wo.context.Context(cp)

    fromDate = dt.date(2021, 2, 1)

    procesar_delegacion(ctx, fromDate, 80)
    procesar_delegacion(ctx, fromDate, 81)
