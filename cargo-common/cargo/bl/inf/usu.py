#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

from sqlalchemy import and_, or_

import cargo.bl.inf.ses
import cargo.bl.inf.sus
import cargo.bl.inf.uss

from cargo.bl.basedal import BaseBL, Entity

log = logging.getLogger(__name__)


class SessionInfo:
    pass

class UsuBL(BaseBL):

    def __init__(self, metadata):
        super().__init__(metadata, "usu")


    def activarSuscripcion(self, conn, usu, sus, fecha):
        """
        Activar una suscripción para un usuario tiene las siguientes implicaciones
        """
        log.info("-----> Inicio")
        log.info(f"     (ususeq): {usu.ususeq}")
        log.info(f"     (susseq): {sus.susseq}")
        log.info(f"     (fecha) : {sus.susseq}")

        ussBL = cargo.bl.inf.uss.UssBL(self._metadata)
        uss = ussBL.getEntity()
        uss.ussact = 1
        uss.ussususeq = usu.ususeq
        uss.usssusseq = sus.susseq
        uss.ussmod = sus.susmod
        uss.ussdef = 0
        ussBL._activarSuscripcion(conn, uss, fecha)

        log.info("<----- Fin")


    def getSuscripcionesActivas(self, conn, ususeq):
        """
        Recupera las suscripciones activas para el usuario. Tiene que
        estar activa la asignación y la propia suscripción
        """
        return cargo.bl.inf.uss.UssBL(self._metadata).\
                _getSuscripcionesActivas(conn, ususeq)


    def login(self, conn, user, password):
        log.info(f"-----> Inicio")
        log.info(f"     (user): {user}")

        if user is None or password is None:
            log.info("<----- Salida, usuario o password nulo")
            return None

        stmt = self.t.select().where(and_(
            or_(
                self.c.usuaka == str.upper(str.strip(user)),
                self.c.usueml == str.strip(user)
            ),
            self.c.usupwd == str.strip(password),
            self.c.usuact == 1
        ))
        usu = conn.execute(stmt).fetchone()
        if usu is None:
            log.info("<----- Salida, usuario no encontrado")            
            return None

        si = SessionInfo()
        si.usu = Entity.fromProxy(usu)
        si.usu.usupwd = "*" * 5
        si.uss = self.getSuscripcionesActivas(conn, usu.ususeq)
        si.ses = cargo.bl.inf.ses.SesBL(self._metadata).crearSesion(conn, usu.ususeq)

        log.info("<----- Fin")
        return si