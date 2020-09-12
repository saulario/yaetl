#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

from sqlalchemy import create_engine, MetaData, Table

from cargo.bl.inf.SesBL import SesBL
from cargo.bl.inf.UsuBL import UsuBL

log = logging.getLogger(__name__)

if __name__ == "__main__":
    log.info("-----> Inicio")

    engine = create_engine("mssql+pymssql://sa:mssql!123@localhost/C000000")
    metadata = MetaData(bind=engine)
    connection = engine.connect()

    tx = connection.begin()

    usuBL = UsuBL(metadata)
    row = usuBL.read(connection, 1)
    row = usuBL.read(connection, 2)

    usu = usuBL.getEntity()
    usu.active = 1
    usu.usuaka = "12312"
    usu.usunom = "123sfsdf"
    usu.usueml = "sdjfs"
    usu.usupwd = "lsdfjlskdfj"
    usuBL.insert(connection, usu)
    usuBL.update(connection, usu)
    usuBL.delete(connection, usu.id)

    stmt = usuBL.select().where(usuBL.getTable().columns["id"] >= 0)
    rows = connection.execute(stmt)
    for row in rows:
        print(row.id)

    sesBL = SesBL(metadata)
    ses = sesBL.getEntity()
    ses.sesusu_id = 1
    sesBL.insert(connection, ses)

    tx.commit()
    connection.close()
    log.info("<----- Fin")