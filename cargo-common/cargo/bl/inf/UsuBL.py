#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

from sqlalchemy import and_, or_

from cargo.bl.basedal import BaseBL, Entity
from cargo.bl.inf.SesBL import SesBL
from cargo.bl.inf.SusBL import SusBL


log = logging.getLogger(__name__)


class SessionInfo:
    pass

class UsuBL(BaseBL):

    def __init__(self, metadata):
        super().__init__(metadata, "usu")


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
        si.suss = SusBL(self._metadata).getSuscripcionesActivas(conn, usu.ususeq)
        si.ses = SesBL(self._metadata).crearSesion(conn, usu.ususeq)

        log.info("<----- Fin")
        return si