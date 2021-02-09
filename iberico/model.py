#/usr/bin/python3

class Entity():
    
    def __init__(self, proxy):
        for key in proxy.iterkeys():
            setattr(self, key, proxy[key])

class PlusAlbaran(Entity):

    def __init__(self, proxy):
        self.Id = None
        self.site = None
        self.cliente = None
        self.flujo = None
        self.discovery = None
        self.albaran = None
        self.fecha_albaran = None
        self.slb = None
        self.truck = None
        self.trailer = None
        self.bordero1 = None
        self.bordero2 = None
        self.fecha_recogida_solicitada = None
        self.fecha_recogida = None
        self.anno_recogida = None
        self.mes_recogida = None
        self.semana_recogida = None
        self.conso_fecha_recogida = None
        self.alias_origen = None
        self.nombre_origen = None
        self.puerta_origen = None
        self.zt_origen = None
        self.fecha_entrega_solicitada = None
        self.fecha_entrega = None
        self.anno_entrega = None
        self.mes_entrega = None
        self.semana_entrega = None
        self.conso_fecha_entrega = None
        self.alias_destino = None
        self.nombre_destino = None
        self.puerta_destino = None
        self.zt_destino = None
        self.hoja_ruta = None
        self.expedicion = None
        self.peso_plus = None
        self.volumen_plus = None
        self.peso_discovery = None
        self.volumen_discovery = None
        self.peso_asn = None
        self.volumen_asn = None
        self.centro_coste = None
        self.fecha_facturacion = None
        self.clave_facturacion = None
        self.clave_tarificacion = None
        self.peso = None
        self.volumen = None
        self.peso_facturable = None
        self.importe = None
        self.pedido_wo = None
        self.importe_wo = None
        super().__init__(proxy)