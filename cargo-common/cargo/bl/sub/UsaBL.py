#!/usr/bin/python3
# -*- coding: utf-8 -*-

from cargo.bl.basedal import BaseBL

class UsaBL(BaseBL):

    def __init__(self, metadata):
        super().__init__(metadata, "usa", "usacod")