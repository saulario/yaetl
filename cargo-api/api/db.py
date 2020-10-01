
import logging
import sqlalchemy as sa

from flask import current_app, g

log = logging.getLogger(__name__)

class DbInfo():

    def __init__(self):
        self.engine = None
        self.metadata = None
        self.conn = None


def init_app(app):
    app.teardown_appcontext(close_db)
    

def get_db():
    log.info("-----> Inicio")
    if "db" not in g:
        log.debug("     +-> Creando conexión con base de datos")
        dbInfo = DbInfo()
        dbInfo.engine = sa.create_engine("mssql+pymssql://sa:mssql!123@localhost/C000000")
        dbInfo.metadata = sa.MetaData(dbInfo.engine)
        dbInfo.conn = dbInfo.engine.connect()
        g.db = dbInfo
    log.info("<----- Fin")
    return g.db


def close_db():
    log.info("-----> Inicio")
    db = g.pop("db", None)
    if db is not None:
        db.conn.close()
    log.info("<----- Fin")
