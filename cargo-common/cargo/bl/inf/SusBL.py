#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

from sqlalchemy import and_, join, select

import cargo.default as defaults

from cargo.bl.basedal import BaseBL, Entity, IllegalStateException
from cargo.bl.inf.NsuBL import NsuBL
from cargo.bl.inf.NusBL import NusBL
from cargo.bl.inf.UsuBL import UsuBL


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


    def getSuscripcionesActivas(self, conn, ususeq):
        log.info("-----> Inicio")
        log.info(f"     (ususeq): {ususeq}")


        result = None
        """
        r01BL = R01BL(self._metadata)
        join = r01BL.t.join(self.t, r01BL.c.r01susseq == self.c.susseq)
        stmt = select([self.t]).select_from(join).where(and_(
                r01BL.c.r01ususeq == ususeq,
                r01BL.c.r01act == 1,
                self.c.susact == 1
            ))
        result = [ Entity.fromProxy(x) for x in conn.execute(stmt).fetchall() ]
        """

        log.info(f"<----- Fin ({len(result)})")
        return result

    
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
        NsuBL(self._metadata).registrarCambioDeEstado(conn, sus, usu, fecha)
        UsuBL(self._metadata).activarSuscripcion(conn, usu, sus, fecha)

        log.info(f"<----- Fin ({sus.susseq})")
        return result
