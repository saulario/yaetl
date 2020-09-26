#!/usr/bin/python3
# -*- coding: utf-8 -*-

import datetime as dt
import logging

from sqlalchemy import create_engine, MetaData, Table

import cargo.default as default

import cargo.bl.inf.ses
import cargo.bl.inf.sus
import cargo.bl.inf.usu

logging.basicConfig(level=logging.DEBUG, format=default.LOG_FORMAT)
log = logging.getLogger(__name__)


if __name__ == "__main__":
    log.info("-----> Inicio")

    engine = create_engine("mssql+pymssql://sa:mssql!123@localhost/C000000")
    metadata = MetaData(bind=engine)
    connection = engine.connect()

    usuBL = cargo.bl.inf.usu.UsuBL(metadata)
    row = usuBL.read(connection, 1)
    row = usuBL.read(connection, 2)

    """
    usu = usuBL.getEntity()
    usu.usuact = 1
    usu.usuaka = "12312"
    usu.usunom = "123sfsdf"
    usu.usueml = "sdjfs"
    usu.usupwd = "lsdfjlskdfj"
    usuBL.insert(connection, usu)
    usu.usunom, usu.usueml = usu.usueml, usu.usunom
    usuBL.update(connection, usu)
    usuBL.delete(connection, usu.ususeq)
    """

    sessionInfo = usuBL.login(connection, " admin01 ", "0lAmUe9MgNi3")
    sessionInfo = usuBL.login(connection, " admin02 ", "0lAmUe9MgNi3")

    """
    result = SesBL(metadata).comprobarSesion(connection, sessionInfo.ses.sescod, 1)
    result = SesBL(metadata).comprobarSesion(connection, sessionInfo.ses.sescod, 5)
    result = SesBL(metadata).comprobarSesion(connection, sessionInfo.ses.sescod, 1)
    """

    """
    tx = connection.begin()

    susBL = SusBL(metadata)
    ahora = dt.datetime.utcnow()

    usu = usuBL.read(connection, 1)
    sus = susBL.getEntity()
    sus.susact = 1
    sus.susaka = "LAMIA"
    sus.susnom = "ESTA ES LA MIA"
    sus.susmod = 64
    sus.susurl = "No tiene URL"
    susBL.crearSuscripcion(connection, sus, usu, ahora)

    tx.commit()
    """
    
    connection.close()
    log.info("<----- Fin")