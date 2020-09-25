#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import uuid

from sqlalchemy import and_

from cargo.bl.basedal import BaseBL, Entity
from cargo.bl.inf.NusBL import NusBL

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
        NusBL(self._metadata).registrarCambioDeEstado(conn, uss, fecha)

        log.debug("<----- Fin")