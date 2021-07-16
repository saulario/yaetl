#!/usr/bin/python3
import argparse
import configparser
import datetime as dt
import logging
import os
import pathlib
import re

import sqlalchemy

log = logging.getLogger(__name__)

res = [
    re.compile(r"^.+(?P<proceso>(33T2VW|33T3VW|33T4VW|4984MX|4984UC|4987FL|ADIENT|ADUANAS|ANSZIP|ASNHIS|ASNMAR|ASNTXT|ASNVMEX|BASTID|BAT511|BEWEGX|BFM141|BFM143|CATCON|CHATTA|COVISI|DBZASN|DELCSL|DELFOR|DELSIL|DESACA|DFAVUS|DFLAUS|DISCOV|EDIPROD|EMPAQS|ENTALM|ENTREG|ERRDEL|FAURECIA|FLOWVN|FSTABL|GAALSE|GACAVA|GALOI3|GALSCC|GALSSC|GASALS|GDAAUD|GDFDBZ|GDSIW6|GSTAMM|GW3640|GW3642|GW3645|GW3646|GW3650|GW3X05|IDSIW6|INVOIC|LAMBORWE|LE33T1|LE33T2|LE4945|LE4987|LTSTAM|LU33T1|LU4987|LUNKOM|MAGNAPOL|MANPRO|MX6015|MX6030|OPELSS|PLASTIC|PORSCHE|PORTSCS|POSRCHELE|POSRCHELEL|POSRCHELET3|POSRCHELET4|POSRCHEZU|POSRCHEZUL|POSRCHEZUT3|proceso|PROVAE|PROVIB|PROVSE|RECAMBIO|SALALM|SCCT-KCC|SCHENE|SDSIW6|SKODA|STATRA|TEMOCO|TOALCA|TOSACA|TOTDEL|TRANSP|VALDEL|VALEOILU|VD4906|VD4984|VESTDE|VESTIB|VWL4945L|VWL4945V|WRSIMX|ZU33T1|ZU33T2|ZU4945|ZU4987))[\.TXT|\.XML|\.ZIP]*$"),
    re.compile(r"^.+(?P<proceso>FTARIS|PLAOMN)\.\d+.TXT$"),
    re.compile(r"^.+(?P<proceso>(LE|ZU)4945)$"),
]

class EdiMensajes():
    
    def __init__(self):
        self.fechaCreacion = None
        self.fecha = None
        self.fechaYYYY = None
        self.fechaYYYYMM = None
        self.fechaYYYYWW = None
        self.fechaWD = None
        self.fechaHH = None
        self.buzon = None
        self.flujo = None
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
        self.engine = sqlalchemy.create_engine(self.cp.get("DATASOURCES", "controlfac"))
        self.metadata = sqlalchemy.MetaData(bind=self.engine)
        self.conn = self.engine.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()


def obtener_proceso(nombre):
    a = [ x.match(nombre) for x in res if x.match(nombre) ]
    if not a: return None
    b = a[0].group("proceso")
    return b

def procesar_fichero(lc, flujo, file):
    log.info(f"\t(file): {file.name}")
    st = file.stat()
    em = EdiMensajes()
    em.buzon = lc.buzon    
    em.flujo = flujo
    em.archivo = file.name
    try:
        em.proceso = obtener_proceso(em.archivo)
    except:
        pass
    em.fechaCreacion = dt.datetime.fromtimestamp(st.st_ctime)
    em.fecha = em.fechaCreacion.date()
    em.fechaYYYY = em.fecha.year
    em.fechaYYYYMM = em.fecha.year * 100 + em.fecha.month
    em.fechaYYYYWW = em.fecha.year * 100 + em.fecha.isocalendar()[1]
    em.fechaWD = em.fecha.isoweekday()
    em.fechaHH = em.fechaCreacion.time().hour
    em.tamano = st.st_size

    em_t = sqlalchemy.Table("edi_mensajes", lc.metadata, autoload=True)
    stmt = em_t.insert(None).values(em.__dict__)
    lc.conn.execute(stmt)

    if flujo == "OUT":
        file.unlink()
    else:
        try:
            file.rename(f"{str(file.parent)}/procesados/{file.name}")
        except FileExistsError:
            pass

def borrar_ficheros_antiguos(p):
    ahora = dt.datetime.now()
    for file in p.glob("*"):
        st = file.stat()
        fc = dt.datetime.fromtimestamp(st.st_mtime)
        td = ahora - fc
        if td.days > 7:
            file.unlink()

def procesar_directorio(lc, flujo, dir):
    log.info("-----> Inicio")
    log.info(f"\t(flujo): {flujo}")
    log.info(f"\t(dir)  : {dir}")

    if not dir: return

    path = pathlib.Path(dir)
    if not path.is_dir(): return

    procesados = None
    try:
        procesados = pathlib.Path(path._str + "\procesados")
        procesados.mkdir()
    except FileExistsError:
        pass

    for file in [ f for f in path.glob("*") if f.is_file() ]:
        procesar_fichero(lc, flujo, file)

    borrar_ficheros_antiguos(procesados)

    log.info("<----- Fin")

def procesar_buzon(lc):
    log.info(f"\t(buzon): {lc.buzon}")
    buzones_t = sqlalchemy.Table("edi_buzones", lc.metadata, autoload=True)
    stmt = buzones_t.select().where(buzones_t.c.codigo == lc.buzon)
    row = lc.conn.execute(stmt).fetchone()
    if row:
        procesar_directorio(lc, "IN", row.pathIn)
        procesar_directorio(lc, "OUT", row.pathOut)

def retroactivo(lc):
    edi_mensajes_t = sqlalchemy.Table("edi_mensajes", lc.metadata, autoload=True)
    mensajes = lc.conn.execute(edi_mensajes_t.select()).fetchall()
    for mensaje in mensajes:
        proceso = obtener_proceso(mensaje.archivo)
        if proceso == mensaje.proceso: continue
        values = { "proceso" : proceso }
        stmt = edi_mensajes_t.update(None).values(values).where(edi_mensajes_t.c.id == mensaje.id)
        lc.conn.execute(stmt)

if __name__ == "__main__":

    filename = os.path.expanduser("~") + "/log/cargar_ficheros.log"
    logging.basicConfig(level=logging.DEBUG, filename=filename,
            format="%(asctime)s %(levelname)s %(thread)d %(processName)s %(module)s %(funcName)s %(message)s" )
    log.info("-----> Inicio")

    parser = argparse.ArgumentParser(description="Procesa archivos EDI en una carpeta")
    parser.add_argument("-b", dest="buzon", action="store", help="Buzón a procesar")
    args = parser.parse_args()
    buzon = args.buzon or "PRUEBAS"

    cp = configparser.ConfigParser()
    cp.read(os.path.expanduser("~") + "/etc/config.ini")    

    try:
        with LocalContext(cp, buzon) as lc:
            procesar_buzon(lc)
            #retroactivo(lc)
    except Exception as e:
        log.error(e, exc_info=True)

    log.info("<----- Fin")