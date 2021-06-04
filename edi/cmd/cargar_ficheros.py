#!/usr/bin/python3
import argparse
import configparser
import datetime as dt
import logging
import os
import pathlib

import sqlalchemy

log = logging.getLogger(__name__)

class EdiMensajes():
    
    def __init__(self):
        self.fecha = None
        self.fechaYYYY = None
        self.fechaYYYYMM = None
        self.fechaYYYYWW = None
        self.buzon = None
        self.archivo = None
        self.proceso = None
        self.tamano = None

class LocalContext():

    def __init__(self, cp, buzon):
        self.cp = cp
        self.buzon = buzon
        self.engine = None
        self.metadata = None
        self.conn = None

    def __enter__(self):
        self.engine = sqlalchemy.create_engine(cp.get("DATASOURCES", "controlfac"))
        self.metadata = sqlalchemy.MetaData(bind=self.engine)
        self.conn = self.engine.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

def procesar_fichero(lc, file):
    log.info(f"\t(file): {file.name}")
    st = file.stat()
    em = EdiMensajes()
    em.buzon = lc.buzon    
    em.archivo = file.name
    try:
        em.proceso = file.name.split(".")[-2]
    except:
        pass
    em.fecha = dt.datetime.fromtimestamp(st.st_ctime)
    em.fechaYYYY = em.fecha.year
    em.fechaYYYYMM = em.fecha.year * 100 + em.fecha.month
    em.fechaYYYYWW = em.fecha.year * 100 + em.fecha.isocalendar()[1]
    em.tamano = st.st_size

    em_t = sqlalchemy.Table("edi_mensajes", lc.metadata, autoload=True)
    stmt = em_t.insert(None).values(em.__dict__)
    lc.conn.execute(stmt)

def procesar_directorio(lc, dir):
    log.info("-----> Inicio")
    log.info(f"\t(dir): {dir}")

    path = pathlib.Path(dir)
    if not path.is_dir(): return

    try:
        pathlib.Path(path._str + "\procesados").mkdir()
    except FileExistsError:
        pass

    for file in [ f for f in path.glob("*") if f.is_file() ]:
        procesar_fichero(lc, file)

    log.info("<----- Fin")

def procesar_buzon(lc):
    log.info(f"\t(buzon): {lc.buzon}")
    buzones_t = sqlalchemy.Table("edi_buzones", lc.metadata, autoload=True)
    stmt = buzones_t.select().where(buzones_t.c.codigo == lc.buzon)
    row = lc.conn.execute(stmt).fetchone()
    if row:
        procesar_directorio(lc, row.path)

if __name__ == "__main__":
    filename = os.path.expanduser("~") + "/log/cargar_ficheros.log"
    logging.basicConfig(level=logging.DEBUG, filename=filename,
            format="%(asctime)s %(levelname)s %(thread)d %(processName)s %(module)s %(funcName)s %(message)s" )
    log.info("-----> Inicio")

    directory = None
    parser = argparse.ArgumentParser(description="Procesa archivos EDI en una carpeta")
    parser.add_argument("-b", dest="buzon", action="store", help="Buzón a procesar")
    args = parser.parse_args()
    buzon = args.buzon or "PRUEBAS"

    cp = configparser.ConfigParser()
    cp.read(os.path.expanduser("~") + "/etc/config.ini")    

    try:
        with LocalContext(cp, buzon) as lc:
            procesar_buzon(lc)
    except Exception as e:
        log.error(e, exc_info=True)

    log.info("<----- Fin")