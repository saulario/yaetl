import argparse
import configparser
import datetime as dt
import logging
import os
import re

import openpyxl
from sqlalchemy import Table, and_, between

import iberico.context

log = logging.getLogger(__name__)


albaran_re = re.compile(r"^LS: (?P<albaran>\d+)$")


def procesar_vollgut(ctx, wb):
    log.info("-----> Procesando llenos")

    wo_pedidos_t = Table("wo_pedidos", ctx.cf_metadata, autoload=True)

    ws = wb.worksheets[0]
    llenos = [ x for x in ws.rows if x[1].value is not None ][1:]

    wsd = wb.worksheets[1]
    detalles = [ x for x in wsd.rows if x[1].value is not None ][1:]

    for fila in llenos:
        fecha = fila[0].value
        prov = fila[1].value
        pais = fila[2].value
        plz = fila[3].value

        documentos = [ x[8].value for x in detalles if x[1].value == fecha 
                and x[29].value == prov 
                and x[46].value == pais 
                and x[45].value == plz]
        documentos = list(dict.fromkeys(documentos))
        print(documentos)

    log.info("<----- Fin")


def procesar_leergut(ctx, wb):
    log.info("-----> Procesar vacíos")

    wo_pedidos_t = Table("wo_pedidos", ctx.cf_metadata, autoload=True)

    ws = wb.worksheets[2]
    vacios = [ x for x in ws.rows if x[1].value is not None ][1:]

    wsd = wb.worksheets[3]
    albaranes = [ x for x in wsd.rows if x[1].value is not None ][1:]

    for vacio in vacios:
        log.info(f"\tProcesando {vacio[0].value}-{vacio[1].value}")
        detalles = [ x for x in albaranes if x[0].value == vacio[0].value and x[3].value == vacio[1].value ]
        if not len(detalles): continue

        albaran = f"%{int(detalles[0][1].value)}%"
        fecha = detalles[0][0].value
        dias = dt.timedelta(days=5)
        fd = fecha - dias
        td = fecha + dias

        stmt = wo_pedidos_t.select().where(and_(
            wo_pedidos_t.c.albaranes.like(albaran),
            between(wo_pedidos_t.c.fecha_recogida, fd, td),
            wo_pedidos_t.c.cliente == 37084
        ))

        rows = ctx.cf_engine.execute(stmt).fetchall()
        if not len(rows):
            log.info(f"\t\tNo se ha encontrado pedido asociado....")
            continue
        if len(rows) > 1:
            log.info(f"\t\tSe han encontrado varios pedidos {[ x.pedido for x in rows ]}")
            continue

        pedido = rows[0]
        importe = vacio[14].value + vacio[17].value
        pf = vacio[11].value
        campos = { 
            'importe_cliente' : round(importe, 2),
            'peso_facturable_cliente' : round(pf, 2),
        }

        stmt = wo_pedidos_t.update(None).values(campos).where(wo_pedidos_t.c.Id == pedido.Id)
        ctx.cf_engine.execute(stmt)

    log.info("<----- Fin")


def main(ctx, wb):
    procesar_vollgut(ctx, wb)
    #procesar_leergut(ctx, wb)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    log.info("-----> Inicio")

    parser = argparse.ArgumentParser(description="Actualiza SLB en albaranes Porsche")
    parser.add_argument("-f", "--filename", dest="filename", help="Archivo XLSX a cargar")

    site = 1
    filename = "c:/temp/porsche/FABI.xlsx"
    parser.parse_args()

    cp = configparser.ConfigParser()
    cp.read(os.path.expanduser("~") + "/etc/config.ini")
    ctx = iberico.context.Context(cp)
    ctx.fromDate = dt.date(2021, 1, 1)

    try:
        wb = openpyxl.load_workbook(filename)
        main(ctx, wb)
    except openpyxl.utils.exceptions.InvalidFileException as e:
        log.error(e)

    log.info("<----- Fin")