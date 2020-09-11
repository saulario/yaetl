#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

from sqlalchemy import create_engine, MetaData, Table

import cargo.bl.inf as bli

log = logging.getLogger(__name__)

if __name__ == "__main__":
    log.info("-----> Inicio")

    engine = create_engine("mssql+pymssql://sa:mssql!123@localhost/C000000")
    metadata = MetaData(bind=engine)
    connection = engine.connect()

    usuDAL = bli.UsuDAL(metadata)
    rows = connection.execute(usuDAL.select()).fetchall()

    usu = usuDAL.read(connection, 1)
    result = usuDAL.update(connection, usu)

    susDAL = bli.SusDAL(metadata)
    rows = connection.execute(susDAL.select()).fetchall()
    for row in rows:
        print(row.susurl)

    r01DAL = bli.R01DAL(metadata)
    rows = connection.execute(r01DAL.select()).fetchall()



    connection.close()
    log.info("<----- Fin")