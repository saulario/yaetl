import configparser
import datetime as dt
import logging
import os

import sqlalchemy
from sqlalchemy import and_

import wo.context
import wo.model


log = logging.getLogger(__name__)

if __name__ == "__main__":
    logging.basicConfig(filename="c:/temp/asignar_expedicion.log", level=logging.DEBUG)
    log.info("-----> Info")

    cp = configparser.ConfigParser()
    cp.read(os.path.expanduser("~") + "/etc/config.ini")
    ctx = wo.context.Context(cp)

    fromDate = dt.date(2021, 1, 1)

    expediciones_lineas = sqlalchemy.Table("expediciones_lineas", ctx.wo_metadata, autoload=True)
    expediciones_pe_ot = sqlalchemy.Table("expediciones_pe_ot", ctx.wo_metadata, autoload=True)

    pedidos_map = {}
    pedidos = sqlalchemy.Table("pedidos", ctx.wo_metadata, autoload="True")
    stmt = pedidos.select().where(and_(
        pedidos.c.ide == 1,
        pedidos.c.fecha_pedido >= fromDate,
        pedidos.c.fuente.like('PLUS_%'),
        pedidos.c.estado != '8'
    ))
    results = ctx.wo_engine.execute(stmt).fetchall()
    for pedido in results:
        if not pedido.fuente in pedidos_map:
            pedidos_map[pedido.fuente] = []
        pedidos_map[pedido.fuente].append(pedido)

    update = False
    for key in pedidos_map.keys():
        for row in pedidos_map[key]:
            pedido = wo.model.Pedidos(row)
            if pedido.exp_id:
                continue

            # solo procesamos Man y Porsche
            if not pedido.dim_cliente_1:
                continue

            a = None
            for a in (x for x in pedidos_map[key] if x.exp_id): break
            if not a:
                continue
            
            log.info(f"\t({pedido.ide}-{pedido.id}) ({pedido.fuente}) ({pedido.fecha_pedido.isoformat()})"
                    f" ({pedido.emp_razon_social})"
                    f"\tExpedicion ({a.exp_id if a.exp_id else ''})")

            if not update:
                continue

            with ctx.wo_engine.connect() as conn:
                with conn.begin() as tx:

                    el = wo.model.ExpedicionesLineas()
                    el.ide = pedido.ide
                    el.expedicion = a.exp_id
                    el.tipo = "P"
                    el.codigo = pedido.id
                    conn.execute(expediciones_lineas.insert(None).values(el.__dict__))

                    epos = conn.execute(expediciones_pe_ot.select().where(and_(
                        expediciones_pe_ot.c.ide == a.ide,
                        expediciones_pe_ot.c.expedicion == a.exp_id,
                        expediciones_pe_ot.c.ot != 0
                    ))).fetchall()

                    ots = dict.fromkeys([ epo.ot for epo in epos ]).keys()
                    if not ots:
                        ots.append(0)
                    for ot in ots:
                        epo = wo.model.ExpedidionesPeOt()
                        epo.ide = pedido.ide
                        epo.expedicion = a.exp_id
                        epo.pedido = pedido.id
                        epo.ot = ot
                        conn.execute(expediciones_pe_ot.insert(None).values(epo.__dict__))

                    d = {}
                    d["exp_id"] = a.exp_id
                    stmt = pedidos.update(None).where(and_(
                        pedidos.c.ide == pedido.ide,
                        pedidos.c.id == pedido.id
                    )).values(d)
                    conn.execute(stmt)

                    tx.commit()


    print("Fin")


