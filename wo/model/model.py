#!/usr/bin/python3


class Entity():
    
    def __init__(self, proxy):
        if not proxy:
            return
        for key in proxy.iterkeys():
            setattr(self, key, proxy[key])

class ExpedicionesLineas(Entity):
    
    def __init__(self, proxy=None, **kwargs):
        self.ide = None
        self.expedicion = None
        self.tipo = None
        self.codigo = None
        super().__init__(proxy)

class ExpedidionesPeOt(Entity):

    def __init__(self, proxy=None, **kwargs):
        self.ide = None
        self.expedicion = None
        self.pedido = None
        self.ot = None
        super().__init__(proxy)

class Pedidos(Entity):

    def __init__(self, proxy=None, **kwargs):
        self.ide = None
        self.id = None
        self.exp_id = None
        self.fuente = None
        self.fecha_pedido = None
        self.emp_razon_social = None
        self.dim_cliente_1 = None
        super().__init__(proxy)