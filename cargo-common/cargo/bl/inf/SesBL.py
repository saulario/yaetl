#!/usr/bin/python3
# -*- coding: utf-8 -*-

import datetime as dt
import uuid

from cargo.bl.basedal import BaseBL

class SesBL(BaseBL):

    def __init__(self, metadata):
        super().__init__(metadata, "ses", "sescod")


    def _before_insert(self, conn, entity, upi):
        entity.sescod = uuid.uuid4()
        entity.sescre = entity.sesult = dt.datetime.utcnow()
        entity.sesval = entity.sescre + dt.timedelta(hours=8)
        entity.seshit = 0

