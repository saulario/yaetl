import argparse
import configparser
import datetime as dt
import itertools
import logging
import os
import re

import sqlalchemy
from sqlalchemy import Table, and_, between

import iberico.context

log = logging.getLogger(__name__)



def obtener_borderos(ctx):
    stmt = sqlalchemy.sql.text("""
        select 
            ti.messageid, ti.transportvehicleid, ti.bordero, ti.borderodate, ti.borderocorrectionkey
            , trunc(fad.freightfrwrdrregistrationdate) as recogida
            , trunc(ti.estimatedtimeofarrival) as entrega
            , trunc(p.pet_org_fecha) as e01_fecha
            , trunc(p.pet_des_fecha) as e99_fecha
            , p.id as pedido
            , p.exp_id as expedicion
            , p.factura as idfactura
        from vda_4921_transport_identific ti 
            join vda_4921_fwd_agent_data fad on fad.messageid=ti.messageid and fad.transportvehicleid=ti.transportvehicleid
            left join gt.pedidos p on p.ide = 1 and p.emisor = 'SB_IBERIAN' and p.dim_cliente_1 = '37323'
                and p.referencia_cliente = ti.bordero and p.estado <> '8'

        where 
        ti.borderodate >= :fromDate
        order by ti.bordero, ti.borderocorrectionkey
""")
    rows = ctx.mtbm_engine.execute(stmt, fromDate=ctx.fromDate).fetchall()
    vdas = {}
    for bordero in rows:
        vdas[bordero.bordero] = bordero

    for k in vdas:
        vda = vdas[k]
        recogida = "" if not vda.recogida else vda.recogida.date().isoformat()
        entrega = "" if not vda.entrega else vda.entrega.date().isoformat()
        fech01 = "" if not vda.e01_fecha else vda.e01_fecha.date().isoformat()
        fech99 = "" if not vda.e99_fecha else vda.e99_fecha.date().isoformat()
        log.info(f"\t{vda.bordero}\t{vda.borderodate.date().isoformat()}\t{vda.borderocorrectionkey}"
                f"\t{recogida}\t{entrega}"
                f"\t{fech01}\t{fech99}"
                f"\t{vda.pedido or ''}\t{vda.expedicion or ''}\t{vda.idfactura or ''}"
                )
        pass
    





def main(ctx):
    obtener_borderos(ctx)


if __name__ == "__main__":
    filename = os.path.expanduser("~") + "/log/comprobar_man.log"
    logging.basicConfig(level=logging.DEBUG, filename=filename,
            format="%(asctime)s %(levelname)s %(thread)d %(processName)s %(module)s %(funcName)s %(message)s" )

    cp = configparser.ConfigParser()
    cp.read(os.path.expanduser("~") + "/etc/config.ini")
    ctx = iberico.context.Context(cp)
    ctx.fromDate = dt.date(2020, 7, 1)

    log.info("-----> Inicio")
    try:
        main(ctx)
    except Exception as e:
        log.error(e, exc_info=True)
    log.info("<----- Fin")