#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import uuid

from cargo.bl.basedal import BaseBL, Entity

log = logging.getLogger(__name__)

class NusBL(BaseBL):

    def __init__(self, metadata):
        super().__init__(metadata, "nus", "nuscod")

    def _before_insert(self, conn, entity, upi):
        log.debug("-----> Inicio")
        entity.nuscod = uuid.uuid4()
        log.debug("<----- Fin")        
