

import logging

from flask import request
from flask_restful import Resource, marshal_with, fields

import cargo.bl.basedal
import cargo.bl.inf.usu
import db

log = logging.getLogger(__name__)

payload = {
    'action' : fields.String,
    'body' : fields.Nested
}

class BaseDispatcher(Resource):

    def __init__(self):
        super().__init__()
        self.bl = None

    def put(self):
        return self.post()

    def post(self):
        return None

    def _get(self, conn, id):
        log.debug("-----> Inicio")
        return self.bl._read(conn, id)



class Dispatcher(BaseDispatcher):

    def put(self):
        return self.post()

    def gettty(self, ususeq):
        log.info("-----> Inicio")
        log.info(f"     (ususeq): {ususeq}")
        return None

    def get(self, ususeq):
        dbi = db.get_db()
        self.bl = cargo.bl.inf.usu.UsuBL(dbi.metadata)
        retval = self._get(dbi.conn, ususeq)
        dbi.conn.close()
        return retval

    def post(self):
        log.info("-----> Inicio")
        for form in request.form:
            print(form)
        return None

    def delete(self, ususeq):
        log.info("-----> Inicio")
        log.info(f"     (ususeq): {ususeq}")
        return None

class List(Resource):

    def get(self):
        log.info("-----> Inicio")
        dbi = db.get_db()
        usuBL = cargo.bl.inf.usu.UsuBL(dbi.metadata)
        usu = usuBL.read(dbi.conn, 1)
        dbi.conn.close()
        log.info("<----- Fin")
        return jsonify(ususeq=usu.ususeq, usunom=usu.usunom) 

