#!/usr/bin/python3
# -*- coding: utf-8 -*-

from cargo.bl.basedal import BaseBL

class R01BL(BaseBL):

    def __init__(self, metadata):
        super().__init__(metadata, "r01")