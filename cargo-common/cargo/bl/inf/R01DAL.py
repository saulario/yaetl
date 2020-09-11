#!/usr/bin/python3
# -*- coding: utf-8 -*-

from cargo.bl.basedal import BaseDAL

class R01DAL(BaseDAL):

    def __init__(self, metadata):
        super().__init__(metadata, "r01")



