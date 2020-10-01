

import logging

from flask import jsonify
from flask_restful import Resource

import cargo.bl.inf.usu
import db

log = logging.getLogger(__name__)

class List(Resource):

    def get(self):
        log.info("-----> Inicio")
        dbi = db.get_db()
        usuBL = cargo.bl.inf.usu.UsuBL(dbi.metadata)
        usu = usuBL.read(dbi.conn, 1)
        dbi.conn.close()
        log.info("<----- Fin")
        return jsonify(ususeq=usu.ususeq, usunom=usu.usunom) 

class Edit(Resource):

    def get(self, ususeq):
        return ususeq