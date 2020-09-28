

import sqlalchemy as sa

from flask import current_app, g

class DbInfo():

    def __init__(self):
        self.engine = None
        self.metadata = None
        self.conn = None


def init_app(app):
    app.teardown_appcontext(close_db)
    

def get_db():
    pass
    if "db" not in g:
        dbInfo = DbInfo()
        dbInfo.engine = sa.create_engine("mssql+pymssql://sa:mssql!123@localhost/C000000")
        dbInfo.metadata = sa.MetaData(dbInfo.engine)
        dbInfo.conn = dbInfo.engine.connect()
        g.db = dbInfo
    return g.db


def close_db():
    print("parando la aplicacion")
    db = g.pop("db", None)
    if db is not None:
        db.conn.close()
