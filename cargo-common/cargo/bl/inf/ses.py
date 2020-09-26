#!/usr/bin/python3
# -*- coding: utf-8 -*-

import datetime as dt
import logging
import uuid

from sqlalchemy import and_, select

import cargo.bl.inf.sus

from cargo import default
from cargo.bl.basedal import BaseBL

log = logging.getLogger(__name__)

class SesBL(BaseBL):

    def __init__(self, metadata):
        super().__init__(metadata, "ses", "sescod")


    def _before_insert(self, conn, entity, **kwargs):
        log.debug("-----> Inicio")
        entity.sescod = uuid.uuid4()
        log.debug("<----- Fin")

    
    def _invalidarSesionesDeUsuario(self, conn, ususeq, fecha):
        log.debug("-----> Inicio")
        log.debug(f"     (ususeq): {ususeq}")

        stmt = self.t.update(None).values(sesact=0, sesval=fecha).where(and_(
            self.c.sesususeq == ususeq,
            self.c.sesact == 1
        ))
        conn.execute(stmt)
        
        log.debug("<----- Fin")


    def _invalidarSesionesCaducadas(self, conn, fecha):
        log.debug("-----> Inicio")
        log.debug(f"     (fecha) : {fecha}")

        stmt = self.t.update(None).values(sesact=0, sesval=fecha).where(and_(
            self.c.sesval < fecha,
            self.c.sesact == 1
        ))
        conn.execute(stmt)

        log.debug("<----- Fin")


    def crearSesion(self, conn, ususeq, susseq):
        log.info("-----> Inicio")
        log.info(f"     (ususeq): {ususeq}")
        log.info(f"     (susseq): {susseq}")

        ahora = dt.datetime.utcnow()
        self._invalidarSesionesDeUsuario(conn, ususeq, ahora)

        ses = self.getEntity()
        ses.sesususeq = ususeq
        ses.sessusseq = susseq
        ses.sesact = 1
        ses.sescre = ses.sesult = ahora
        ses.sesval = ses.sescre + default.SESSION_DURATION
        ses.seshit = 0
        self.insert(conn, ses)
        
        log.info("<----- Fin")
        return ses

    
    def comprobarSesion(self, conn, sescod, susseq):
        log.info("-----> Inicio")
        log.info(f"     (sescod): {sescod}")
        log.info(f"     (susseq): {susseq}")

        retval = False
        ahora = dt.datetime.utcnow()
        self._invalidarSesionesCaducadas(conn, ahora)

        ses = self.read(conn, sescod)
        if ses is None:
            log.info("<----- Salida, sesion no encontrada")
            return retval
        if ses.sesval < ahora:
            log.info("<----- Salida, sesion caducada")
            return retval

        suss = cargo.bl.info.sus.SusBL(self._metadata).getSuscripcionesActivas(conn, ses.sesususeq)
        sus = [ sus for sus in suss if sus.susseq == susseq ]
        if not len(sus):
            log.info("<----- Salida, suscripcion no valida")
            return retval
        
        ses.sesval = ahora + default.SESSION_DURATION
        self.update(conn, ses)
        retval = True

        log.info(f"<----- Fin ({retval})")
        return retval