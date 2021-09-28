import configparser
import datetime as dt
import logging
import os
from sys import exc_info

import requests
import sqlalchemy

from sqlalchemy import and_

import wo.context
import wo.model


log = logging.getLogger(__name__)

url_api = r"http://riesgos.gruposese.com:9536/Riesgo/Cifs/%s/%s"
POLIZA  = 539293

def comprobar_activo(poliza, cif):
    """
    Basta con que un único GF esté activo
    """
    if cif is None:
        return
    activos = [ x for x in cif if x.fecha_baja is None ]
    if not len(activos):
        log.info("\t%s\tno tiene GF activos, bloquear", poliza.cif)

def comprobar_bloqueado(poliza, cif):
    """
    Todos los GF deben esar bloqueados
    """
    if cif is None:
        return
    activos = [ x for x in cif if x.fecha_baja is None ]
    if len(activos):
        log.info("\t%s\ttiene %d GF activos, desbloquear", poliza.cif, len(activos))
        url = url_api % (poliza.cif, "Reactivar")
        params = { 
            "Origen": "PLUS", 
            "Usuario": "CORRECTOR",
        }
        data =  { 
            "Cif" : poliza.cif,
            "Ide" : activos[0].ide,
            "Moneda" : None,
            "Bloqueado" : None,
            "MotivoBloqueo" : None,
            "FechaBloqueo" : None
        }
        response = requests.post(url, params=params, data=data)
        print("Estoy aquí")


def comprobar(poliza, cif):
    if poliza.bloqueado == "S":
        comprobar_bloqueado(poliza, cif)
    else:
        comprobar_activo(poliza, cif)

def main(ctx):
    
    emp = sqlalchemy.Table("EMPRESAS", ctx.wo_metadata, autoload=True)
    egf = sqlalchemy.Table("EMPRESAS_GRUPOS_FACTURACION", ctx.wo_metadata, autoload=True)
    pe = sqlalchemy.Table("POLIZAS_EMPRESAS", ctx.wo_metadata, schema="RIESGO", autoload=True)
    pide = sqlalchemy.Table("POLIZAS_IDE", ctx.wo_metadata, schema="RIESGO", autoload=True)

    log.info("\tCargando datos...")

    stmt = pide.select().with_only_columns([ pide.c.ide ]).where(pide.c.poliza == POLIZA).order_by(pide.c.ide)
    ides = [ x.ide for x in ctx.wo_engine.execute(stmt).fetchall() ]


    cifs = {}
    polizas = {}

    stmt = sqlalchemy.select([emp.c.id, emp.c.cif, emp.c.razon_social, emp.c.idc,
            egf.c.ide, egf.c.idc, egf.c.fecha_alta, egf.c.fecha_baja, egf.c.motivo_baja  ])\
            .where(and_(
                emp.c.idc == egf.c.idc,
                egf.c.ide.in_(ides)
            ))\
            .order_by(emp.c.cif)
    rows = ctx.wo_engine.execute(stmt).fetchall()
    for row in rows:
        if row.cif is None or len(row.cif) < 6: continue
        if not row.cif in cifs:
            cifs[row.cif] = []
        cifs[row.cif].append(row)

    rows = ctx.wo_engine.execute(pe.select().where(pe.c.poliza == POLIZA)).fetchall()
    polizas =  { x.cif:x for x in rows if len(x.cif) >= 6 }

    for poliza in polizas:
        comprobar(polizas.get(poliza), cifs.get(poliza))

    log.info("\tCruzando datos...")


if __name__ == "__main__":
    filename = os.path.expanduser("~") + "/log/comprobar_riesgos.log"
    logging.basicConfig(level=logging.DEBUG, filename=filename,
            format="%(asctime)s %(levelname)s %(thread)d %(processName)s %(module)s %(funcName)s %(message)s" )
    log.info("-----> Inicio")

    cp = configparser.ConfigParser()
    cp.read(os.path.expanduser("~") + "/etc/config.ini")
    ctx = wo.context.Context(cp)

    try:
        main(ctx)
    except Exception as e:
        log.error(e, exc_info=True)

    log.info("<----- Fin")
