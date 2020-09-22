#!/usr/bin/python3
# -*- coding: utf-8 -*-

import cargo.default as defaults

from cargo.bl.basedal import BaseBL

class R01BL(BaseBL):

    def __init__(self, metadata):
        super().__init__(metadata, "r01")


    def _before_insert(self, conn, r01, upi=None):
        self._validarFormato(r01)


    def _before_update(self, conn, r01, upi=None):
        self._validarFormato(r01)

    
    def _validarFormato(self, r01):
        r01.r01mod &= defaults.MODULOS_MAXVALUE


