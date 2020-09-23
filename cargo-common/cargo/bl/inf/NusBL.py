#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import uuid

from cargo.bl.basedal import BaseBL, Entity, and_

log = logging.getLogger(__name__)

class NusBL(BaseBL):

    def __init__(self, metadata):
        super().__init__(metadata, "nus", "nuscod")

    def _before_insert(self, conn, entity, upi):
        log.debug("-----> Inicio")
        entity.nuscod = uuid.uuid4()
        log.debug("<----- Fin")   


    def _anularEstadosAnteriores(self, conn, uss, fecha, upi=None):
        log.debug("-----> Inicio")

        stmt = self.t.update(None).values(nusfecfin=fecha).where(and_(
            self.c.nusususeq == uss.ussususeq,
            self.c.nussusseq == uss.usssusseq,
            self.c.nusfecfin == None
        ))
        conn.execute(stmt)

        log.debug("<----- Fin")


    def registrarCambioDeEstado(self, conn, uss, fecha, upi=None):
        log.info("-----> Inicio")

        self._anularEstadosAnteriores(conn, uss, fecha, upi)
        nus = self.getEntity()
        nus.nusususeq = uss.ussususeq
        nus.nussusseq = uss.usssusseq
        nus.nusfecini = fecha
        nus.nusmod = uss.ussmod
        self.insert(conn, nus, upi)

        log.info("<----- Fin")
