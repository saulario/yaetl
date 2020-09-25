#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import uuid

from sqlalchemy import and_

from cargo.bl.basedal import BaseBL, Entity

log = logging.getLogger(__name__)

class NsuBL(BaseBL):

    def __init__(self, metadata):
        super().__init__(metadata, "nsu", "nsucod")


    def _before_insert(self, conn, nsu, **kwargs):
        log.debug("-----> Inicio")
        nsu.nsucod = uuid.uuid4()
        log.debug("<----- Fin")        

    
    def _anularEstadosAnteriores(self, conn, susseq, fecha):
        log.debug("-----> Inicio")

        stmt = self.t.update(None).values(nsufecfin=fecha).where(and_(
            self.c.nsususseq == susseq,
            self.c.nsufecfin == None
        ))
        conn.execute(stmt)

        log.debug("<----- Fin")


    def registrarCambioDeEstado(self, conn, sus, usu, fecha):
        log.info("-----> Inicio")
        log.info(f"     (suscod): {sus.susseq}")

        self._anularEstadosAnteriores(conn, sus.susseq, fecha, **kwargs)

        nsu = self.getEntity()
        nsu.nsucod = None
        nsu.nsususseq = sus.susseq
        nsu.nsufecini = fecha
        nsu.nsufecfin = None
        nsu.nsumod = sus.susmod
        nsu.nsuususeq = usu.ususeq
        self.insert(conn, nsu, **kwargs)

        log.info(f"<----- Fin {nsu.nsucod}")
        return nsu