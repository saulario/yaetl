#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import uuid

from sqlalchemy import and_, select

import cargo.bl.inf.nus
import cargo.bl.inf.sus

from cargo.bl.basedal import BaseBL, Entity


log = logging.getLogger(__name__)

class UssBL(BaseBL):

    def __init__(self, metadata):
        super().__init__(metadata, "uss", "usscod")


    def _before_insert(self, conn, uss, **kwargs):
        log.debug("-----> Inicio")
        uss.usscod = uuid.uuid4()
        log.debug("<----- Fin")        


    def _activarSuscripcion(self, conn, uss, fecha):
        log.debug("-----> Inicio")

        self.insert(conn, uss)
        cargo.bl.inf.nus.NusBL(self._metadata).registrarCambioDeEstado(conn, uss, fecha)

        log.debug("<----- Fin")


    def _getSuscripcionesActivas(self, conn, ususeq):
        log.debug("-----> Inicio")
        log.debug(f"     (ususeq): {ususeq}")

        susBL = cargo.bl.inf.sus.SusBL(self._metadata)
        j = self.t.join(susBL.t, susBL.c.susseq == self.c.usssusseq)
        stmt = select([self.t, susBL.c.susaka, susBL.c.susnom])\
            .select_from(j).\
            where(and_(
                self.c.ussususeq == ususeq,
                self.c.ussact == 1,
                susBL.c.susact == 1
            ))
        rows = conn.execute(stmt).fetchall()
        result = [ Entity.fromProxy(x) for x in rows ]
        
        log.debug(f"<----- Fin ({len(result)})")
        return result


    def _getUsuariosActivos(self, conn, susseq):

        return None
