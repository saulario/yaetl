#!/usr/bin/python3
import argparse
import configparser
import logging
import os
import pathlib
import sys

import openpyxl
import sqlalchemy

from sqlalchemy import and_

import iberico.context

log = logging.getLogger(__name__)


def main(s, wb):
    cp = configparser.ConfigParser()
    cp.read(os.path.expanduser("~") + "/etc/config.ini")
    ctx = iberico.context.Context(cp)

    dnp_t = sqlalchemy.Table("deliverynotepackages", ctx.ibsite_metadata,
            schema=f"PRE_SITE{s}", autoload=True)

    ws = wb.worksheets[0]
    for row in list(ws.rows)[1:ws.max_row]:
        site = int(row[1].value)
        if site != s:
            continue
        slb = row[8].value
        if not slb:
            continue
        slb = str(slb)

        dnid = int(row[5].value)
        albaran = row[6].value

        log.info(f"\tProcesando dnid ({dnid}), albaran ({albaran}), slb nuevo ({slb})")
        stmt = dnp_t.select().where(and_(
            dnp_t.c.dnid == dnid,
            dnp_t.c.deliverynoteorigin == str(albaran)
        ))
        dnps = ctx.ib_engine.execute(stmt).fetchall()
        for dnp in dnps:
            if dnp.slborigin == slb:
                continue
            log.info(f"\t\tdnpid ({dnp.id}), slb actual ({dnp.slborigin})")
            stmt = dnp_t.update(None).values(slborigin=slb).where(dnp_t.c.id == dnp.id)
            ctx.ib_engine.execute(stmt)




if __name__ == "__main__":
    filename = os.path.expanduser("~") + "/log/actualizar_slb.log"
    logging.basicConfig(level=logging.DEBUG, filename=filename,
            format="%(asctime)s %(levelname)s %(thread)d %(processName)s %(module)s %(funcName)s %(message)s" )
    log.info("-----> Inicio")

    parser = argparse.ArgumentParser(description="Actualiza SLB en albaranes Porsche")
    parser.add_argument("-f", "--filename", dest="filename", help="Archivo XLSX a cargar",
            default="c:/temp/porsche/actualizar_slb.xlsx")
    parser.parse_args()

    filename = "c:/temp/porsche/actualizar_slb.xlsx"    
    try:
        wb = openpyxl.load_workbook(filename)
        main(1, wb)
        main(3, wb)
    except openpyxl.utils.exceptions.InvalidFileException as e:
        log.error(e)

    log.info("<----- Fin")