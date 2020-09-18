#!/usr/bin/python3
# -*- coding: utf-8 -*-

from cargo.bl.basedal import BaseBL

class GdiBL(BaseBL):

    def __init__(self, metadata):
        super().__init__(metadata, "gdi", "gdicod")