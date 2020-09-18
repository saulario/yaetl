#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

from sqlalchemy import and_, join, select

from cargo.bl.basedal import BaseBL, Entity
from cargo.bl.inf.R01BL import R01BL


log = logging.getLogger(__name__)

class SusBL(BaseBL):

    def __init__(self, metadata):
        super().__init__(metadata, "sus")


    def getSuscripcionesActivas(self, conn, ususeq):
        log.info("-----> Inicio")
        log.info(f"     (ususeq): {ususeq}")

        r01BL = R01BL(self._metadata)
        join = r01BL.t.join(self.t, r01BL.c.r01susseq == self.c.susseq)
        stmt = select([self.t]).select_from(join).where(and_(
                r01BL.c.r01susseq == ususeq,
                r01BL.c.r01act == 1,
                self.c.susact == 1
            ))
        result = [ Entity.fromProxy(x) for x in conn.execute(stmt).fetchall() ]

        log.info(f"<----- Fin ({len(result)})")
        return result