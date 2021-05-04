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

    # precarga los albaranes con id numérico
    albaranes ={}
    plus_albaranes_t = Table("plus_albaranes", ctx.cf_metadata, autoload="True")
    stmt = plus_albaranes_t.select().where(and_(
        plus_albaranes_t.c.fecha_albaran >= ctx.fromDate,
        plus_albaranes_t.c.flujo == "VG",
        plus_albaranes_t.c.albaran != None,
    ))
    rows = ctx.cf_engine.execute(stmt).fetchall()
    for albaran in rows:
        albnum = None
        try:
            albnum = int(albaran.albaran)
        except ValueError: continue
        if albnum not in albaranes:
            albaranes[albnum] = []
        albaranes[albnum].append(albaran)

    ws = wb.worksheets[0]
    llenos = [ x for x in ws.rows if x[1].value is not None ][1:]

    wsd = wb.worksheets[1]
    detalles = [ x for x in wsd.rows if x[1].value is not None ][1:]

    log.info(f"\t\talbaran\tfecha\tproveedor\tfecha recogida\talias origen\tpedido WO")

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
        for doc in documentos:

            match = albaran_re.match(doc)
            if not match:
                continue
            try:
                numalb = int(match.group('albaran'))
            except ValueError: continue

            encontrado = None
            if numalb in albaranes:
                td = dt.timedelta(days=10)
                fd = (fecha - td).date()
                fh = (fecha + td).date()
                for alb in albaranes[numalb]:
                    if alb.fecha_albaran >= fd and alb.fecha_albaran <= fh:
                        encontrado = alb
                        break
            
            alias_origen = ""
            pedido_wo = ""
            fecha_recogida = ""
            if encontrado:
                alias_origen = encontrado.alias_origen or None
                pedido_wo = encontrado.pedido_wo or None
                fecha_recogida = encontrado.fecha_recogida.isoformat()

            log.info(f"\t\t{numalb}\t{fecha.date().isoformat()}\t{prov}\t{fecha_recogida}\t{alias_origen}\t{pedido_wo}")




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
            log.info(f"\t\tNo se ha encontrado pedido asociado para el albarán. {albaran}")
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
    filename = os.path.expanduser("~") + "/log/comprobar_fabi.log"
    logging.basicConfig(level=logging.DEBUG, filename=filename,
            format="%(asctime)s %(levelname)s %(thread)d %(processName)s %(module)s %(funcName)s %(message)s" )

    parser = argparse.ArgumentParser(description="Comprueba la composición del archivo FABI")
    parser.add_argument("-f", "--filename", dest="filename", help="Archivo XLSX a cargar")
    parser.add_argument("-s", "--site", dest="site", help="Site a verificar", default=0)

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