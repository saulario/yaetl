import sqlalchemy

import logging

log = logging.getLogger(__file__)

def borrar_pedidos(ctx):
    log.info("\tBorrando anteriores...")
    cf_wo_pedidos = sqlalchemy.Table("wo_pedidos", ctx.cf_metadata, autoload=True)
    stmt = cf_wo_pedidos.delete(None).where(cf_wo_pedidos.c.fecha_recogida >= ctx.fromDate)
    ctx.cf_engine.execute(stmt)

def procesar_pedidos(ctx):
    log.info("\tTraspasando nuevos...")
    wo_conn = ctx.wo_engine.connect()
    cf_conn = ctx.cf_engine.connect()

    cf_wo_pedidos = sqlalchemy.Table("wo_pedidos", ctx.cf_metadata, autoload=True)
    stmt =  sqlalchemy.sql.text(f"""select p.ide, p.id as pedido, p.exp_id as expedicion, p.cliente, p.estado, p.factura as facturaid, p.fac_num_oficial as factura
    , p.importe importe_tarifa, p.pco_importe_extra importe_conceptos, (p.importe + nvl(p.pco_importe_extra, 0)) as importe_total
    , p.fuente
    , case
        when p.subtipo = 1 then 'VG'
        else 'LG'
      end as flujo
    , cast(p.pet_org_fecha as date) fecha_recogida, p.dir_org_alias alias_origen
    , cast(p.pet_des_fecha as date) fecha_entrega, p.dir_des_alias alias_destino
    , ped.albaran as slb
    , ped.detalle_cliente as puerta
    , ped.peso_bruto as peso, ped.volumen as volumen, peso_neto as peso_facturable
    , p.observaciones as albaranes
    , p.dim_cliente_7 as tarifa
from pedidos p
    join pedidos_etapas_detalle ped on ped.ide=p.ide and ped.pedido=p.id
where
p.ide = 1
and cast(p.fecha_pedido as DATE) >= :fromDate
and p.emisor = 'SB_IBERIAN'
AND P.CLIENTE = '37084'
and p.estado <> '8'
""")

    stmt =  sqlalchemy.sql.text(f"""
select p.ide, p.id as pedido, p.exp_id as expedicion, p.cliente, p.estado, p.factura as facturaid, p.fac_num_oficial as factura
    , p.importe importe_tarifa, p.pco_importe_extra importe_conceptos, (p.importe + nvl(p.pco_importe_extra, 0)) as importe_total
    , p.fuente
    , case
        when p.subtipo = 1 then 'VG'
        else 'LG'
      end as flujo
    , cast(p.pet_org_fecha as date) fecha_recogida
    , case
        when p.subtipo = 1 then (select min(proveedor) from pedidos_etapas_detalle where ide=p.ide and pedido=p.id)
        else (select min(cliente) from pedidos_etapas_detalle where ide=p.ide and pedido=p.id)
        end as alias_origen
    , cast(p.pet_des_fecha as date) fecha_entrega
    , case
        when p.subtipo = 1 then (select min(cliente) from pedidos_etapas_detalle where ide=p.ide and pedido=p.id)
        else (select min(proveedor) from pedidos_etapas_detalle where ide=p.ide and pedido=p.id)
        end as alias_destino
    , '' slb
    , '' as puerta
    , (select sum(peso_bruto) from pedidos_etapas_detalle where ide=p.ide and pedido=p.id) as peso
    , (select sum(volumen) from pedidos_etapas_detalle where ide=p.ide and pedido=p.id) as volumen
    , (select sum(peso_neto) from pedidos_etapas_detalle where ide=p.ide and pedido=p.id) as peso_facturable
    , p.observaciones as albaranes
    , p.dim_cliente_7 as tarifa
from pedidos p
where
p.ide = 1
and cast(p.fecha_pedido as DATE) >= :fromDate
and p.emisor = 'SB_IBERIAN'
AND P.CLIENTE = '37084'
and p.estado <> '8'
""")

    fila = 0
    rows = wo_conn.execute(stmt, fromDate=ctx.fromDate).fetchall()
    for row in rows:
        fila += 1
        if not (fila % 100):
            log.info(f"\tprocesando ... {fila}")        
        stmt = cf_wo_pedidos.insert(None).values(row)
        cf_conn.execute(stmt)

    cf_conn.close()
    wo_conn.close()

def run(ctx):
    log.info("-----> Procesando datos de WO")
    borrar_pedidos(ctx)
    procesar_pedidos(ctx)
    log.info("<----- Fin")
