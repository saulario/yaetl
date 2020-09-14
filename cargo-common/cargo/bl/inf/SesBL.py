#!/usr/bin/python3
# -*- coding: utf-8 -*-

import datetime as dt
import uuid

from cargo import default
from cargo.bl.basedal import BaseBL

class SesBL(BaseBL):

    def __init__(self, metadata):
        super().__init__(metadata, "ses", "sescod")


    def _before_insert(self, conn, entity, upi):
        entity.sescod = uuid.uuid4()
        entity.sescre = entity.sesult = dt.datetime.utcnow()
        entity.sesval = entity.sescre + default.SESSION_DURATION
        entity.seshit = 0

    
    def crearSesion(self, conn, ususeq):
        entity = self.getEntity()
        entity.sesususeq = ususeq
        result = self.insert(conn, entity)
        return entity

