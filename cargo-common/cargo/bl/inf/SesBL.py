#!/usr/bin/python3
# -*- coding: utf-8 -*-

import datetime as dt
import logging
import uuid

from sqlalchemy import and_, select


from cargo import default
from cargo.bl.basedal import BaseBL
from cargo.bl.inf.R01BL import R01BL
from cargo.bl.inf.SusBL import SusBL

log = logging.getLogger(__name__)

class SesBL(BaseBL):

    def __init__(self, metadata):
        super().__init__(metadata, "ses", "sescod")


    def _before_insert(self, conn, entity, upi):
        log.debug("-----> Inicio")
        entity.sescod = uuid.uuid4()
        entity.sescre = entity.sesult = dt.datetime.utcnow()
        entity.sesval = entity.sescre + default.SESSION_DURATION
        entity.seshit = 0
        log.debug("<----- Fin")
        

    def _borrarSesionesCaducadas(self, conn):
        log.debug("-----> Inicio")
        stmt = self.t.delete(None).where(self.c.sesval <= dt.datetime.utcnow())
        conn.execute(stmt)
        log.debug("-----> Inicio")


    def crearSesion(self, conn, ususeq):
        log.info("-----> Inicio")
        log.info(f"     (ususeq): {ususeq}")
        self._borrarSesionesCaducadas(conn)
        entity = self.getEntity()
        entity.sesususeq = ususeq
        self.insert(conn, entity)
        log.info("<----- Fin")
        return entity

    
    def comprobarSesion(self, conn, sescod, susseq):
        log.info("-----> Inicio")
        log.info(f"     (sescod): {sescod}")
        log.info(f"     (susseq): {susseq}")

        retval = False
        ahora = dt.datetime.utcnow()

        ses = self.read(conn, sescod)
        if ses is None:
            log.info("<----- Salida, sesion no encontrada")
            return retval
        if ses.sesval < ahora:
            log.info("<----- Salida, sesion caducada")
            return retval

        suss = SusBL(self._metadata).getSuscripcionesActivas(conn, ses.sesususeq)
        sus = [ sus for sus in suss if sus.susseq == susseq ]
        if not len(sus):
            log.info("<----- Salida, suscripcion no valida")
            return retval
        
        ses.sesval = ahora + default.SESSION_DURATION
        self.update(conn, ses)
        retval = True

        log.info(f"<----- Fin ({retval})")
        return retval