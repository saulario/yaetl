#!/usr/bin/python3
# -*- coding: utf-8 -*-

from cargo.bl.basedal import BaseDAL

class UsuDAL(BaseDAL):

    def __init__(self, metadata):
        super().__init__(metadata, "usu")



