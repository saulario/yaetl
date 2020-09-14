#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

from sqlalchemy import and_, or_

from cargo.bl.basedal import BaseBL, Entity
from cargo.bl.inf.SesBL import SesBL
from cargo.bl.inf.SusBL import SusBL


log = logging.getLogger(__name__)


class UserProfileInfo:
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

        stmt = self.getTable().select().where(and_(
            or_(
                self.c().usuaka == str.upper(str.strip(user)),
                self.c().usueml == str.strip(user)
            ),
            self.c().usupwd == str.strip(password),
            self.c().usuact == 1
        ))
        row = conn.execute(stmt).fetchone()
        if row is None:
            log.info("<----- Salida, usuario no encontrado")            
            return

        upi = UserProfileInfo()
        upi.usu = Entity.fromProxy(row)
        upi.usu.usupwd = "*" * 5

        upi.suss = SusBL(self._metadata).getSuscripciones(conn, row.ususeq)

        ses = SesBL(self._metadata).crearSesion(conn, upi.usu.ususeq)
        upi.sescod = ses.sescod

        log.info("<----- Fin")
        return upi