#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

from sqlalchemy import and_, join, select

import cargo.bl.inf.nsu
import cargo.bl.inf.usu
import cargo.default as defaults

from cargo.bl.basedal import BaseBL, Entity

log = logging.getLogger(__name__)


class SusBL(BaseBL):

    def __init__(self, metadata):
        super().__init__(metadata, "sus")


    def _before_insert(self, conn, sus, **kwargs):
        self._validarFormato(sus)


    def _before_update(self, conn, sus, **kwargs):
        self._validarFormato(sus)

    
    def _validarFormato(self, sus):
        sus.susmod &= defaults.MODULOS_MAXVALUE


    def crearSuscripcion(self, conn, sus, usu, fecha):
        """
        Crear una suscripción tiene las siguientes implicaciones
            · El usuario necesariamente debe existir
            · Insertar la suscripción como tal
            · Registrar un cambio de estado para que permita facturar 
            · Activa la suscripción para el usuario con el máximo de permisos
        """
        log.info("-----> Inicio")
        log.info(f"     (susaka): {sus.susaka}")
        log.info(f"     (ususeq): {usu.ususeq}")
        log.info(f"     (fecha) : {fecha}")


        result = self.insert(conn, sus)
        cargo.bl.inf.nsu.NsuBL(self._metadata).registrarCambioDeEstado(conn, sus, usu, fecha)
        cargo.bl.inf.usu.UsuBL(self._metadata).activarSuscripcion(conn, usu, sus, fecha)

        log.info(f"<----- Fin ({sus.susseq})")
        return result
