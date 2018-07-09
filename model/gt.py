# coding: utf-8
from sqlalchemy import CHAR, CheckConstraint, Column, DateTime, ForeignKey, ForeignKeyConstraint, Index, VARCHAR, text
from sqlalchemy.dialects.oracle.base import NUMBER
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class CfDimensione(Base):
    __tablename__ = 'cf_dimensiones'
    __table_args__ = {'schema': 'gt'}

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    descripcion = Column(VARCHAR(30))


class CfDispositivo(Base):
    __tablename__ = 'cf_dispositivos'
    __table_args__ = (
        Index('cf_dis_iddis_fab_uk', 'id_dispositivo', 'fabricante', unique=True),
        {'schema': 'gt'}
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    id_dispositivo = Column(NUMBER(asdecimal=False))
    fabricante = Column(NUMBER(6, 0, False))
    activo = Column(NUMBER(1, 0, False), server_default=text("1"))
    mensajeria = Column(NUMBER(1, 0, False), server_default=text("0"))
    tablet = Column(NUMBER(1, 0, False), server_default=text("0"))
    descripcion = Column(VARCHAR(100))
    fecha_creacion = Column(DateTime)
    fecha_actualizacion = Column(DateTime)
    registro = Column(VARCHAR(100))
    fecha_ultima_conexion = Column(DateTime)
    fecha_ultima_posicion = Column(DateTime)
    observaciones = Column(VARCHAR(200))
    idioma = Column(VARCHAR(25))
    latitud = Column(NUMBER(asdecimal=False))
    longitud = Column(NUMBER(asdecimal=False))
    ultima_posicion = Column(VARCHAR(300))


class CfTiposVehiculo(Base):
    __tablename__ = 'cf_tipos_vehiculo'
    __table_args__ = {'schema': 'gt'}

    id = Column(NUMBER(3, 0, False), primary_key=True)
    nombre = Column(VARCHAR(50))
    caracteristicas = Column(VARCHAR(200))
    arrastre = Column(VARCHAR(1))
    autonomo = Column(CHAR(1))
    nombre_us = Column(VARCHAR(50))


class CfVehiculosBaja(Base):
    __tablename__ = 'cf_vehiculos_baja'
    __table_args__ = {'schema': 'gt'}

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    descripcion = Column(VARCHAR(100))


class CmCorredore(Base):
    __tablename__ = 'cm_corredores'
    __table_args__ = {'schema': 'gt'}

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    nombre = Column(VARCHAR(20), nullable=False)
    fecha_creacion = Column(DateTime, nullable=False)
    usuario_creacion = Column(VARCHAR(20), nullable=False)
    fecha_modificacion = Column(DateTime)
    usuario_modificacion = Column(VARCHAR(20))


class CmEmpresa(Base):
    __tablename__ = 'cm_empresas'
    __table_args__ = {'schema': 'gt'}

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    nombre = Column(VARCHAR(100))
    descripcion = Column(VARCHAR(200))
    estado = Column(CHAR(1), server_default=text("'A'"))
    fecha_creacion = Column(DateTime)
    usu_creacion = Column(VARCHAR(100))
    empresa_asociada = Column(NUMBER(asdecimal=False))
    idioma = Column(VARCHAR(2))
    moneda = Column(VARCHAR(3))
    multidivisa = Column(VARCHAR(1))
    activo_axon = Column(VARCHAR(1))
    ide_trafico = Column(NUMBER(6, 0, False))
    calculo_previsiones = Column(CHAR(1), nullable=False, server_default=text("'N' "))
    cierre_matriculas = Column(VARCHAR(1), server_default=text("'N'"))
    sii_activo = Column(NUMBER(1, 0, False), server_default=text("(0)"))
    direccion_facturas = Column(VARCHAR(1000))
    sii_dias_permitidos = Column(NUMBER(2, 0, False))


class CmGruposDelegacione(Base):
    __tablename__ = 'cm_grupos_delegaciones'
    __table_args__ = {'schema': 'gt'}

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    nombre = Column(VARCHAR(50))
    observaciones = Column(VARCHAR(200))
    orden = Column(NUMBER(3, 0, False))


class ConductoresTipoDocumento(Base):
    __tablename__ = 'conductores_tipo_documento'
    __table_args__ = {'schema': 'gt'}

    id = Column(NUMBER(2, 0, False), primary_key=True)
    nombre = Column(VARCHAR(50))
    observaciones = Column(VARCHAR(200))


class ConductoresTiposNomina(Base):
    __tablename__ = 'conductores_tipos_nomina'
    __table_args__ = {'schema': 'gt'}

    id = Column(NUMBER(6, 0, False), primary_key=True)
    nombre = Column(VARCHAR(50))
    descripcion = Column(VARCHAR(100))
    activo = Column(NUMBER(1, 0, False))


class EmpresasEstado(Base):
    __tablename__ = 'empresas_estados'
    __table_args__ = {'schema': 'gt'}

    id = Column(CHAR(1), primary_key=True)
    descripcion = Column(VARCHAR(25))


class EmpresasMotivoBaja(Base):
    __tablename__ = 'empresas_motivo_baja'
    __table_args__ = {'schema': 'gt'}

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    descripcion = Column(VARCHAR(25))


class EmpresasSectore(Base):
    __tablename__ = 'empresas_sectores'
    __table_args__ = {'schema': 'gt'}

    id = Column(NUMBER(4, 0, False), primary_key=True)
    nombre = Column(VARCHAR(30))
    observaciones = Column(VARCHAR(150))
    nombre_us = Column(VARCHAR(30))


class Moneda(Base):
    __tablename__ = 'monedas'
    __table_args__ = {'schema': 'gt'}

    id = Column(CHAR(3), primary_key=True)
    nombre = Column(VARCHAR(100))
    unidades = Column(NUMBER(6, 0, False))
    cambio_fijo = Column(NUMBER(9, 3, True))


class OrdenesTransporteEstadoEnv(Base):
    __tablename__ = 'ordenes_transporte_estado_env'
    __table_args__ = {'schema': 'gt'}

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    estado = Column(VARCHAR(50))
    activo = Column(NUMBER(1, 0, False))


class OrdenesTransporteEstado(Base):
    __tablename__ = 'ordenes_transporte_estados'
    __table_args__ = {'schema': 'gt'}

    id = Column(CHAR(1), primary_key=True)
    descripcion = Column(VARCHAR(50))
    descripcion_us = Column(VARCHAR(50))


class Regione(Base):
    __tablename__ = 'regiones'
    __table_args__ = {'schema': 'gt'}

    id = Column(NUMBER(5, 0, False), primary_key=True)
    descripcion = Column(VARCHAR(100))
    nombre = Column(VARCHAR(50))


class Series(Base):
    __tablename__ = 'series'
    __table_args__ = {'schema': 'gt'}

    id = Column(CHAR(3), primary_key=True)
    nombre = Column(VARCHAR(50))
    descripcion = Column(VARCHAR(200))


class TiposConceptosTarifa(Base):
    __tablename__ = 'tipos_conceptos_tarifas'
    __table_args__ = {'schema': 'gt'}

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    descripcion = Column(VARCHAR(200))
    activo = Column(CHAR(1))
    tipo = Column(CHAR(1))
    descripcion_us = Column(VARCHAR(200))


class TiposImpuesto(Base):
    __tablename__ = 'tipos_impuesto'
    __table_args__ = {'schema': 'gt'}

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    descripcion = Column(VARCHAR(200))


class TiposPagoCobro(Base):
    __tablename__ = 'tipos_pago_cobro'
    __table_args__ = {'schema': 'gt'}

    id = Column(NUMBER(3, 0, False), primary_key=True)
    descripcion = Column(VARCHAR(100))
    idnav = Column(VARCHAR(10))
    idinvoic = Column(VARCHAR(3))
    ide = Column(NUMBER(asdecimal=False), nullable=False)


class TiposUrgencia(Base):
    __tablename__ = 'tipos_urgencia'
    __table_args__ = {'schema': 'gt'}

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    descripcion = Column(VARCHAR(200))


class Zona(Base):
    __tablename__ = 'zonas'
    __table_args__ = {'schema': 'gt'}

    id_zona = Column(NUMBER(10, 0, False), primary_key=True)
    pais = Column(CHAR(2))
    nombre_zona = Column(VARCHAR(35))


class ZonasHoraria(Base):
    __tablename__ = 'zonas_horarias'
    __table_args__ = {'schema': 'gt'}

    id_zona = Column(NUMBER(10, 0, False), primary_key=True, nullable=False)
    abreviacion = Column(VARCHAR(6))
    timestamp = Column(NUMBER(11, 0, False))
    fecha_hora = Column(DateTime, primary_key=True, nullable=False)
    gmt_variacion = Column(NUMBER(11, 0, False))
    ahorro_luz = Column(CHAR(1), primary_key=True, nullable=False)


class CfVehiculosDispositivo(Base):
    __tablename__ = 'cf_vehiculos_dispositivos'
    __table_args__ = {'schema': 'gt'}

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    id_vehiculo = Column(NUMBER(6, 0, False), nullable=False)
    fecha_alta = Column(DateTime)
    fecha_baja = Column(DateTime)
    dispositivo = Column(ForeignKey('gt.cf_dispositivos.id'))

    cf_dispositivo = relationship('CfDispositivo')


class CfVehiculosTiempoReal(Base):
    __tablename__ = 'cf_vehiculos_tiempo_real'
    __table_args__ = {'schema': 'gt'}

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    id_vehiculo = Column(NUMBER(6, 0, False))
    fecha_ultima_conexion = Column(DateTime)
    remolque = Column(VARCHAR(20))
    conductor1 = Column(VARCHAR(70))
    conductor2 = Column(VARCHAR(70))
    fecha_ultima_posicion = Column(DateTime)
    latitud = Column(VARCHAR(40))
    longitud = Column(VARCHAR(40))
    velocidad = Column(NUMBER(asdecimal=False))
    rumbo = Column(VARCHAR(10))
    posicion_ciudad = Column(VARCHAR(200))
    posicion_pueblo = Column(VARCHAR(200))
    nivel_deposito = Column(NUMBER(asdecimal=False))
    nuevo_mensaje = Column(NUMBER(1, 0, False))
    nueva_incidencia = Column(NUMBER(1, 0, False))
    motor_encendido = Column(NUMBER(1, 0, False))
    estado_frigo = Column(VARCHAR(100))
    temperatura = Column(NUMBER(asdecimal=False))
    set_point = Column(NUMBER(asdecimal=False))
    peso = Column(NUMBER(asdecimal=False))
    id_conductor1 = Column(NUMBER(6, 0, False))
    id_conductor2 = Column(NUMBER(6, 0, False))
    kms_registrados_gps = Column(NUMBER(asdecimal=False))
    kms_registrados_tacografo = Column(NUMBER(asdecimal=False))
    temperatura_sonda1 = Column(NUMBER(asdecimal=False))
    temperatura_sonda2 = Column(NUMBER(asdecimal=False))
    modo_parking = Column(VARCHAR(20))
    fecha_parking_desde = Column(DateTime)
    fecha_parking_hasta = Column(DateTime)
    ebs = Column(NUMBER(1, 0, False))
    id_dispositivo = Column(ForeignKey('gt.cf_dispositivos.id'))
    email_parking = Column(VARCHAR(50))
    gmt_fecha_parking = Column(NUMBER(2, 0, False))

    cf_dispositivo = relationship('CfDispositivo')


class CmDelegacione(Base):
    __tablename__ = 'cm_delegaciones'
    __table_args__ = {'schema': 'gt'}

    id = Column(VARCHAR(2), primary_key=True)
    descripcion = Column(VARCHAR(200))
    activo = Column(CHAR(1), server_default=text("'N'"))
    fecha_alta = Column(DateTime, server_default=text("sysdate"))
    fecha_baja = Column(DateTime)
    grupo = Column(ForeignKey('gt.cm_grupos_delegaciones.id'))
    responsable = Column(VARCHAR(10))
    responsable_operativo = Column(VARCHAR(10))
    id_corredor = Column(ForeignKey('gt.cm_corredores.id'))
    idioma_defecto = Column(VARCHAR(5))

    cm_grupos_delegacione = relationship('CmGruposDelegacione')
    cm_corredore = relationship('CmCorredore')


class Conductore(Base):
    __tablename__ = 'conductores'
    __table_args__ = (
        Index('ind_conductores_emp', 'empresa', 'id'),
        {'schema': 'gt'}
    )

    id = Column(NUMBER(6, 0, False), primary_key=True)
    nombre = Column(VARCHAR(100), nullable=False)
    alias = Column(VARCHAR(50))
    empresa = Column(NUMBER(6, 0, False))
    serie = Column(ForeignKey('gt.series.id'))
    propio = Column(CHAR(1))
    observaciones = Column(VARCHAR(200))
    nombre_solo = Column(VARCHAR(100))
    apellidos = Column(VARCHAR(100), nullable=False)
    dni = Column(VARCHAR(30))
    usu_creacion = Column(VARCHAR(100))
    fecha_creacion = Column(DateTime)
    tipo = Column(NUMBER(3, 0, False))
    documento_pais = Column(VARCHAR(30))
    permiso_tacografo = Column(VARCHAR(30))
    tipo_documento = Column(ForeignKey('gt.conductores_tipo_documento.id'))
    documento = Column(VARCHAR(30))
    activo = Column(VARCHAR(1))
    dimension = Column(NUMBER(asdecimal=False))
    usu_modificacion = Column(VARCHAR(100))
    fecha_modificacion = Column(DateTime)
    id_extra = Column(NUMBER(6, 0, False))
    fecha_nacimiento = Column(DateTime)
    tipo_nomina = Column(ForeignKey('gt.conductores_tipos_nomina.id'))
    antiguedad = Column(DateTime)
    trafico = Column(VARCHAR(200))
    residencia = Column(VARCHAR(200))
    titular_cuenta = Column(VARCHAR(100))
    cuenta_bancaria = Column(VARCHAR(50))
    telefono = Column(VARCHAR(100))

    series = relationship('Series')
    conductores_tipo_documento = relationship('ConductoresTipoDocumento')
    conductores_tipos_nomina = relationship('ConductoresTiposNomina')


class FaFactura(Base):
    __tablename__ = 'fa_facturas'
    __table_args__ = (
        Index('fa_numero_factura_uq', 'ide', 'numero_factura', unique=True),
        {'schema': 'gt'}
    )

    ide = Column(NUMBER(3, 0, False), primary_key=True, nullable=False, server_default=text("1 "))
    id = Column(NUMBER(10, 0, False), primary_key=True, nullable=False)
    numero_factura = Column(VARCHAR(20))
    fecha_emision = Column(DateTime)
    concepto = Column(VARCHAR(200))
    cliente = Column(VARCHAR(10), nullable=False)
    gf = Column(NUMBER(2, 0, False))
    forma_pago = Column(NUMBER(3, 0, False))
    dias_vencimiento = Column(NUMBER(asdecimal=False))
    fecha_vencimiento = Column(DateTime)
    importe = Column(NUMBER(asdecimal=False))
    iva = Column(NUMBER(4, 2, True))
    importe_iva = Column(NUMBER(asdecimal=False))
    descuento = Column(NUMBER(asdecimal=False))
    importe_descuento = Column(NUMBER(asdecimal=False))
    importe_total = Column(NUMBER(asdecimal=False))
    moneda = Column(ForeignKey('gt.monedas.id'))
    cobrado = Column(CHAR(1), server_default=text("'N'"))
    observaciones = Column(VARCHAR(200))
    fecha_creacion = Column(DateTime, server_default=text("SYSDATE"))
    usuario_creacion = Column(VARCHAR(100))
    fecha_modificacion = Column(DateTime, server_default=text("SYSDATE"))
    usuario_modificacion = Column(VARCHAR(100))
    ide_factura_abonada = Column(NUMBER(3, 0, False))
    factura_abonada = Column(NUMBER(10, 0, False))
    motivo_abono = Column(VARCHAR(200))
    estado = Column(NUMBER(1, 0, False))
    numero_autofactura = Column(VARCHAR(30))
    gasoil = Column(NUMBER(8, 2, True))
    precio_tarifa = Column(NUMBER(asdecimal=False))
    numero_oficina = Column(VARCHAR(20))
    numero_departamento = Column(VARCHAR(20))
    numero_albaran = Column(VARCHAR(30))
    cambio_aplicado = Column(NUMBER(asdecimal=False))
    moneda_cambio = Column(CHAR(3))
    terminos_cobro = Column(NUMBER(asdecimal=False))
    fecha_servicio = Column(DateTime)
    gr_reg_iva_neg = Column(NUMBER(asdecimal=False))
    facturador = Column(VARCHAR(20))
    numero_pedido = Column(VARCHAR(50))
    importe_sistema = Column(NUMBER(asdecimal=False))
    importe_iva_sistema = Column(NUMBER(asdecimal=False))
    importe_descuento_sistema = Column(NUMBER(asdecimal=False))
    importe_total_sistema = Column(NUMBER(asdecimal=False))
    id_cambio = Column(NUMBER(asdecimal=False))
    retencion = Column(NUMBER(asdecimal=False))
    importe_retencion = Column(NUMBER(asdecimal=False))
    importe_retencion_sistema = Column(NUMBER(asdecimal=False))
    fact_negativa = Column(NUMBER(1, 0, False))
    sii_l2_codigo = Column(VARCHAR(2))
    sii_l5_codigo = Column(VARCHAR(1))
    factura_enviada = Column(NUMBER(1, 0, False))
    fecha_envio = Column(DateTime)
    certificado = Column(VARCHAR(50))

    moneda1 = relationship('Moneda')


class Paise(Base):
    __tablename__ = 'paises'
    __table_args__ = {'schema': 'gt'}

    id = Column(CHAR(2), primary_key=True)
    codigo_ison = Column(NUMBER(3, 0, False))
    codigo_iso3 = Column(CHAR(3))
    pais_esp = Column(VARCHAR(100))
    pais_ing = Column(VARCHAR(100))
    pais_org = Column(VARCHAR(100))
    observaciones = Column(VARCHAR(200))
    activo = Column(VARCHAR(1))
    ue = Column(VARCHAR(1), server_default=text("'N'"))
    zona_horaria = Column(ForeignKey('gt.zonas.id_zona'))

    zona = relationship('Zona')


class PedidosConcepto(Base):
    __tablename__ = 'pedidos_conceptos'
    __table_args__ = (
        Index('ind_pedidos_concep_ide_ped_id', 'ide', 'pedido', 'id'),
        {'schema': 'gt'}
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    ide = Column(NUMBER(3, 0, False), nullable=False, server_default=text("1 "))
    pedido = Column(NUMBER(8, 0, False), nullable=False)
    concepto = Column(ForeignKey('gt.tipos_conceptos_tarifas.id'), nullable=False)
    importe = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))
    moneda = Column(ForeignKey('gt.monedas.id'), server_default=text("'EUR'"))
    importe_unidad = Column(NUMBER(asdecimal=False))
    cantidad = Column(NUMBER(asdecimal=False))
    observaciones = Column(VARCHAR(200))
    importe_sistema = Column(NUMBER(asdecimal=False))

    tipos_conceptos_tarifa = relationship('TiposConceptosTarifa')
    moneda1 = relationship('Moneda')


class TarifasCliente(Base):
    __tablename__ = 'tarifas_cliente'
    __table_args__ = (
        CheckConstraint("TIPO in ('T','U')"),
        CheckConstraint("remontable in ('S','N')"),
        CheckConstraint("req_vehiculo in ('S','N')"),
        CheckConstraint("unidad in ('B','H','C','G','K','D','M','P','Z','Q','T','E','V', 'X')"),
        Index('ind_tarifas_cliente_emp', 'cliente', 'id'),
        {'schema': 'gt'}
    )

    id = Column(NUMBER(6, 0, False), primary_key=True)
    cliente = Column(VARCHAR(10))
    codigo_tarifa = Column(VARCHAR(11))
    codigo_tarifa_ant = Column(VARCHAR(10))
    oferta = Column(NUMBER(6, 0, False))
    fecha_aplicacion = Column(DateTime)
    fecha_finalizacion = Column(DateTime)
    kms = Column(NUMBER(5, 0, False))
    precio = Column(NUMBER(asdecimal=False))
    tipo = Column(CHAR(1), server_default=text("'T'"))
    unidad = Column(CHAR(1), server_default=text("'M'"))
    desde = Column(NUMBER(asdecimal=False))
    hasta = Column(NUMBER(asdecimal=False))
    remontable = Column(CHAR(1), server_default=text("'N'"))
    alturas = Column(NUMBER(2, 0, False))
    tipo_mercancia = Column(CHAR(1))
    req_vehiculo = Column(CHAR(1), server_default=text("'N'"))
    fecha_creacion = Column(DateTime, server_default=text("sysdate"))
    usu_creacion = Column(VARCHAR(50))
    fecha_modificacion = Column(DateTime)
    usu_modificacion = Column(VARCHAR(50))
    iyv = Column(VARCHAR(1))
    moneda = Column(ForeignKey('gt.monedas.id'), server_default=text("'EUR'"))
    iva = Column(NUMBER(3, 0, False))
    descuento = Column(NUMBER(5, 0, False))
    tp_vehiculo = Column(ForeignKey('gt.cf_tipos_vehiculo.id'))
    observaciones = Column(VARCHAR(200))
    referencia_cliente = Column(VARCHAR(50))
    gf = Column(NUMBER(2, 0, False))
    minimo = Column(NUMBER(asdecimal=False))
    maximo = Column(NUMBER(asdecimal=False))
    obs_transporte = Column(VARCHAR(200))
    detalle_concepto = Column(VARCHAR(200))
    ide = Column(NUMBER(asdecimal=False))
    posicion = Column(VARCHAR(30))
    urgente = Column(NUMBER(1, 0, False))
    gas_margen = Column(NUMBER(asdecimal=False))
    gas_porcentaje_aplicacion = Column(NUMBER(asdecimal=False))
    gas_fecha_acuerdo = Column(DateTime)
    gas_precio_firma = Column(NUMBER(asdecimal=False))

    moneda1 = relationship('Moneda')
    cf_tipos_vehiculo = relationship('CfTiposVehiculo')


class Empresa(Base):
    __tablename__ = 'empresas'
    __table_args__ = (
        Index('empresas_cseguro_nif', 'codigo_seguro', 'cif'),
        {'schema': 'gt'}
    )

    id = Column(NUMBER(6, 0, False), primary_key=True)
    razon_social = Column(VARCHAR(100))
    alias = Column(VARCHAR(50))
    cif = Column(VARCHAR(30), index=True)
    moneda = Column(ForeignKey('gt.monedas.id'))
    sector = Column(ForeignKey('gt.empresas_sectores.id'))
    fecha_alta = Column(DateTime, server_default=text("Sysdate"))
    fecha_baja = Column(DateTime)
    iva = Column(NUMBER(4, 2, True))
    forma_pago = Column(ForeignKey('gt.tipos_pago_cobro.id'))
    forma_cobro = Column(ForeignKey('gt.tipos_pago_cobro.id'))
    vencimiento_pago = Column(NUMBER(3, 0, False))
    vencimiento_cobro = Column(NUMBER(3, 0, False))
    idc = Column(VARCHAR(10), unique=True)
    idp = Column(VARCHAR(10), unique=True)
    irpf = Column(NUMBER(4, 0, False))
    grupo = Column(VARCHAR(30))
    estado = Column(ForeignKey('gt.empresas_estados.id'), server_default=text("'A'"))
    web = Column(VARCHAR(100))
    pais = Column(ForeignKey('gt.paises.id'))
    empresa_fiscal = Column(ForeignKey('gt.empresas.id'))
    siglas = Column(VARCHAR(3))
    dias_pago = Column(VARCHAR(20))
    observaciones = Column(VARCHAR(200))
    tipo_impuesto = Column(ForeignKey('gt.tipos_impuesto.id'))
    tipo_proveedor = Column(NUMBER(asdecimal=False))
    fecha_alta_cliente = Column(DateTime)
    fecha_baja_cliente = Column(DateTime)
    bloqueo_cliente = Column(CHAR(1), server_default=text("'N'"))
    fecha_alta_proveedor = Column(DateTime)
    fecha_baja_proveedor = Column(DateTime)
    bloqueo_proveedor = Column(CHAR(1), server_default=text("'N'"))
    control_flota = Column(CHAR(1))
    tipo_cliente = Column(NUMBER(asdecimal=False))
    riesgo = Column(NUMBER(asdecimal=False))
    riesgo_medida = Column(NUMBER(asdecimal=False))
    riesgo_sese = Column(NUMBER(asdecimal=False))
    tipo_riesgo = Column(NUMBER(asdecimal=False), server_default=text("NULL"))
    codigo_seguro = Column(VARCHAR(25))
    descuento = Column(NUMBER(asdecimal=False))
    retencion = Column(NUMBER(asdecimal=False))
    numero_certificado = Column(VARCHAR(30))
    fecha_certificado = Column(DateTime)
    bloquear_facturas_proveedor = Column(CHAR(1))
    bloqueo_tarifa = Column(CHAR(1), server_default=text("'N'"))
    codigo_cuenta_cotizacion = Column(VARCHAR(12))
    fecha_cuenta_cotizacion = Column(DateTime)
    gr_contable_cli = Column(NUMBER(3, 0, False))
    gr_contable_pro = Column(NUMBER(3, 0, False))
    gr_contable_neg_cli = Column(NUMBER(3, 0, False))
    gr_contable_neg_pro = Column(NUMBER(3, 0, False))
    gr_registro_iva_neg_cli = Column(NUMBER(3, 0, False))
    gr_registro_iva_neg_pro = Column(NUMBER(3, 0, False))
    fecha_bloqueo_cliente = Column(DateTime)
    fecha_bloqueo_proveedor = Column(DateTime)
    terminos_pago = Column(NUMBER(3, 0, False))
    proponer_tarifa = Column(VARCHAR(1), server_default=text("'N'"))
    cod_presupuestario_cli = Column(VARCHAR(20))
    cod_presupuestario_pro = Column(VARCHAR(20))
    bloquear_facturas_proveedor_ss = Column(CHAR(1))
    codigo_deudor_cesce = Column(VARCHAR(20))
    refacturar = Column(VARCHAR(1), nullable=False, server_default=text("'S' "))
    liquidador = Column(VARCHAR(20), server_default=text("null"))
    fecha_creacion = Column(DateTime)
    usu_creacion = Column(VARCHAR(50))
    fecha_modificacion = Column(DateTime)
    usu_modificacion = Column(VARCHAR(50))
    permiso_tarjetas = Column(NUMBER(1, 0, False))
    sigla = Column(VARCHAR(1))
    cuenta_debe_gasoil = Column(NUMBER(asdecimal=False))
    cuenta_debe_adblue = Column(NUMBER(asdecimal=False))
    cuenta_debe_empleado = Column(NUMBER(asdecimal=False))
    cuenta_haber_gasoil = Column(NUMBER(asdecimal=False))
    cuenta_haber_adblue = Column(NUMBER(asdecimal=False))
    cuenta_haber_empleado = Column(NUMBER(asdecimal=False))
    cuenta = Column(VARCHAR(25))
    tarifa_gasoleo = Column(VARCHAR(10))
    reg_fact_prov = Column(NUMBER(1, 0, False), server_default=text("0"))
    motivo_baja = Column(ForeignKey('gt.empresas_motivo_baja.id'))
    observaciones_bloqueo = Column(VARCHAR(50))
    infcli_fecha = Column(DateTime)
    infcli_vol_mens_viajes = Column(NUMBER(asdecimal=False))
    infcli_precio_viaje = Column(NUMBER(asdecimal=False))
    infcli_importe_clasif_riesgo = Column(NUMBER(asdecimal=False))
    infcli_ide_emp_fact = Column(NUMBER(3, 0, False))
    dni_coop = Column(VARCHAR(100))
    fecha_certificado_hacienda = Column(DateTime)
    fecha_certificado_ss = Column(DateTime)
    fecha_ultimo_recibo_ss_tc2 = Column(DateTime)
    dimension_proveedor = Column(ForeignKey('gt.cf_dimensiones.id'))
    permitir_spot = Column(NUMBER(1, 0, False), nullable=False, server_default=text("0 "))
    tipo_cif = Column(VARCHAR(2))
    tiene_renting = Column(NUMBER(1, 0, False))
    cfdi_uso = Column(VARCHAR(4))
    cfdi_aduana = Column(VARCHAR(4))
    dig_codigo_docum_cliente = Column(VARCHAR(20))
    emp_basica = Column(VARCHAR(1))
    ref_externa_1 = Column(VARCHAR(20))
    ref_externa_2 = Column(VARCHAR(20))

    cf_dimensione = relationship('CfDimensione')
    parent = relationship('Empresa', remote_side=[id])
    empresas_estado = relationship('EmpresasEstado')
    tipos_pago_cobro = relationship('TiposPagoCobro', primaryjoin='Empresa.forma_cobro == TiposPagoCobro.id')
    tipos_pago_cobro1 = relationship('TiposPagoCobro', primaryjoin='Empresa.forma_pago == TiposPagoCobro.id')
    moneda1 = relationship('Moneda')
    empresas_motivo_baja = relationship('EmpresasMotivoBaja')
    paise = relationship('Paise')
    empresas_sectore = relationship('EmpresasSectore')
    tipos_impuesto = relationship('TiposImpuesto')


class Pedido(Base):
    __tablename__ = 'pedidos'
    __table_args__ = (
        ForeignKeyConstraint(['ide_pedido_asociado', 'pedido_asociado'], ['gt.pedidos.ide', 'gt.pedidos.id']),
        Index('ind_pedidos_ide_pet_org_f_prev', 'ide', 'pet_org_fecha_prevista'),
        Index('ind_pedidos_ide_emp_empresa', 'ide', 'emp_empresa'),
        Index('ind_pedidos_refcliente', 'referencia_cliente', 'ide', 'id'),
        Index('ind_pedidos_pedcliente', 'pedido_cliente', 'ide', 'id'),
        Index('ind_pedidos_tarifa', 'tarifa', 'ide', 'id'),
        Index('ind_pedidos_ide_exp_id', 'ide', 'exp_id'),
        Index('ind_pedidos_pedido_asociado', 'ide_pedido_asociado', 'pedido_asociado'),
        Index('ind_pedidos_cliente_gf', 'cliente', 'gf', 'ide', 'id'),
        Index('ind_pedidos_usu', 'gestor', 'ide', 'id'),
        {'schema': 'gt'}
    )

    ide = Column(ForeignKey('gt.cm_empresas.id'), primary_key=True, nullable=False, server_default=text("1 "))
    id = Column(NUMBER(8, 0, False), primary_key=True, nullable=False)
    cliente = Column(VARCHAR(10), nullable=False)
    pedido_cliente = Column(VARCHAR(150))
    estado = Column(CHAR(1), nullable=False)
    tipo = Column(NUMBER(asdecimal=False), server_default=text("1"))
    cantidad_carga = Column(NUMBER(10, 0, False))
    unidad_carga = Column(CHAR(1))
    fecha_solicitud = Column(DateTime)
    tiempo_estimado = Column(NUMBER(asdecimal=False))
    km_estimados = Column(NUMBER(asdecimal=False))
    observaciones = Column(VARCHAR(200))
    referencia_cliente = Column(VARCHAR(50))
    alias = Column(VARCHAR(100))
    camion_completo = Column(CHAR(1), server_default=text("'N'"))
    pedido_patron = Column(CHAR(1))
    gestor = Column(VARCHAR(15), nullable=False)
    tarifa = Column(ForeignKey('gt.tarifas_cliente.id'))
    importe = Column(NUMBER(asdecimal=False))
    moneda = Column(CHAR(3), server_default=text("'EUR'"))
    iva = Column(NUMBER(3, 0, False))
    descuento = Column(NUMBER(3, 0, False))
    delegacion = Column(CHAR(2), nullable=False)
    importe_conceptos = Column(NUMBER(asdecimal=False))
    ide_pedido_asociado = Column(NUMBER(8, 0, False), server_default=text("1"))
    pedido_asociado = Column(NUMBER(8, 0, False))
    moneda_prov = Column(CHAR(3), server_default=text("'EUR'"))
    vacio = Column(CHAR(1))
    pedido_automatico = Column(NUMBER(8, 0, False))
    urgencia = Column(CHAR(1), server_default=text("'N'"))
    tipo_urgencia = Column(ForeignKey('gt.tipos_urgencia.id'))
    gestor_asociado = Column(VARCHAR(500))
    fuente = Column(VARCHAR(200), index=True)
    gf = Column(NUMBER(2, 0, False), server_default=text("1"))
    expedicion_asociada = Column(NUMBER(8, 0, False))
    fecha_creacion = Column(DateTime)
    usu_creacion = Column(VARCHAR(50))
    fecha_modificacion = Column(DateTime)
    usu_modificacion = Column(VARCHAR(50))
    factura = Column(NUMBER(10, 0, False))
    ide_factura = Column(NUMBER(3, 0, False))
    fecha_pedido = Column(DateTime, index=True)
    conforme = Column(CHAR(1), server_default=text("'N'"))
    subtipo = Column(NUMBER(4, 0, False), server_default=text("1"))
    bloqueado = Column(VARCHAR(1))
    importe_sistema = Column(NUMBER(asdecimal=False))
    id_cambio = Column(NUMBER(asdecimal=False))
    cartera = Column(NUMBER(6, 0, False))
    frio = Column(NUMBER(1, 0, False))
    tipo_vehiculo = Column(NUMBER(3, 0, False))
    pco_importe_extra = Column(NUMBER(asdecimal=False))
    emp_empresa = Column(NUMBER(6, 0, False))
    emp_razon_social = Column(VARCHAR(100))
    emp_cif = Column(VARCHAR(30))
    emp_alias = Column(VARCHAR(50))
    exp_id = Column(NUMBER(8, 0, False))
    egf_nombre = Column(VARCHAR(100))
    tar_tipo = Column(CHAR(1))
    tar_precio_unitario = Column(NUMBER(asdecimal=False))
    fac_num_oficial = Column(VARCHAR(20))
    pet_cantidad = Column(NUMBER(asdecimal=False))
    pet_unidad = Column(CHAR(1))
    pet_kms = Column(NUMBER(5, 0, False))
    pet_org_fecha = Column(DateTime, index=True)
    pet_org_fecha_prevista = Column(DateTime)
    pet_org_fecha_real = Column(DateTime)
    pet_org_fecha_inicio = Column(DateTime)
    pet_org_fecha_fin = Column(DateTime)
    pet_org_direccion_id = Column(NUMBER(6, 0, False))
    dir_org_nombre = Column(VARCHAR(100))
    dir_org_zona = Column(VARCHAR(5))
    dir_org_poblacion = Column(VARCHAR(200))
    dir_org_direccion = Column(VARCHAR(200))
    dir_org_latitud = Column(NUMBER(asdecimal=False))
    dir_org_longitud = Column(NUMBER(asdecimal=False))
    pet_des_fecha = Column(DateTime, index=True)
    pet_des_fecha_prevista = Column(DateTime)
    pet_des_fecha_real = Column(DateTime)
    pet_des_fecha_inicio = Column(DateTime)
    pet_des_fecha_fin = Column(DateTime)
    pet_des_direccion_id = Column(NUMBER(6, 0, False))
    dir_des_nombre = Column(VARCHAR(100))
    dir_des_zona = Column(VARCHAR(5))
    dir_des_poblacion = Column(VARCHAR(200))
    dir_des_direccion = Column(VARCHAR(200))
    dir_des_latitud = Column(NUMBER(asdecimal=False))
    dir_des_longitud = Column(NUMBER(asdecimal=False))
    dim_metros = Column(NUMBER(asdecimal=False))
    dim_peso = Column(NUMBER(asdecimal=False))
    dim_fc = Column(NUMBER(asdecimal=False))
    del_nombre_delegacion = Column(VARCHAR(100))
    dir_org_alias = Column(VARCHAR(150))
    dir_des_alias = Column(VARCHAR(150))
    emisor = Column(VARCHAR(30))
    grupo_transporte = Column(NUMBER(2, 0, False))
    pet_org_gmt = Column(NUMBER(2, 0, False))
    pet_des_gmt = Column(NUMBER(2, 0, False))
    retraso = Column(NUMBER(1, 0, False))
    visor_europroveedores = Column(NUMBER(1, 0, False), nullable=False, server_default=text("1 "))
    pet_org_fecha_eta_manual = Column(DateTime)
    pet_des_fecha_borrar = Column(VARCHAR(20))
    valor_mercancia = Column(NUMBER(asdecimal=False))
    timbre_uuid = Column(VARCHAR(100))
    num_detalles = Column(NUMBER(asdecimal=False))
    precio_venta = Column(NUMBER(asdecimal=False))
    pet_des_fecha_eta_manual = Column(DateTime)
    pet_org_slot = Column(VARCHAR(40))
    pet_des_slot = Column(VARCHAR(40))
    pco_importe_extra_sistema = Column(NUMBER(asdecimal=False))
    pet_r_paises = Column(VARCHAR(25))
    pet_r_poblaciones = Column(VARCHAR(150))
    pet_r_fechas_llegada = Column(VARCHAR(150))
    pet_r_fechas_salida = Column(VARCHAR(150))
    pet_e_paises = Column(VARCHAR(25))
    pet_e_poblaciones = Column(VARCHAR(150))
    pet_e_fechas_llegada = Column(VARCHAR(150))
    pet_e_fechas_salida = Column(VARCHAR(150))
    pet_des_fecha_prev_salida = Column(DateTime)
    pet_org_fecha_prev_salida = Column(DateTime)
    pl_carga = Column(NUMBER(asdecimal=False))
    pl_ruta = Column(NUMBER(asdecimal=False))
    dim_cliente_1 = Column(VARCHAR(20))
    dim_cliente_2 = Column(VARCHAR(20))
    dim_cliente_6 = Column(VARCHAR(50))
    dim_cliente_3 = Column(VARCHAR(20))
    dim_cliente_4 = Column(VARCHAR(20))
    dim_cliente_5 = Column(VARCHAR(20))
    pet_org_fecha_inicio_ventana = Column(DateTime)
    pet_org_fecha_fin_ventana = Column(DateTime)
    pet_des_fecha_inicio_ventana = Column(DateTime)
    pet_des_fecha_fin_ventana = Column(DateTime)

    cm_empresa = relationship('CmEmpresa')
    parent = relationship('Pedido', remote_side=[ide, id])
    tarifas_cliente = relationship('TarifasCliente')
    tipos_urgencia = relationship('TiposUrgencia')


class Poblacione(Base):
    __tablename__ = 'poblaciones'
    __table_args__ = (
        Index('ind_pais_poblacion', 'pais', 'poblacion'),
        Index('poblaciones_pais_poblacion_cpa', 'pais', 'cpa', 'poblacion_consultas'),
        {'schema': 'gt'}
    )

    id = Column(NUMBER(8, 0, False), primary_key=True)
    poblacion = Column(VARCHAR(50))
    poblacion_principal = Column(VARCHAR(50))
    area = Column(VARCHAR(50))
    pais = Column(ForeignKey('gt.paises.id'))
    ruta = Column(VARCHAR(200))
    latitud = Column(NUMBER(10, 5, True))
    longitud = Column(NUMBER(10, 5, True))
    poblacion_consultas = Column(VARCHAR(50))
    ruta_consultas = Column(VARCHAR(200))
    provincia = Column(NUMBER(5, 0, False))
    cpa = Column(VARCHAR(2))
    zona_horaria = Column(ForeignKey('gt.zonas.id_zona'))

    paise = relationship('Paise')
    zona = relationship('Zona')


class Provincia(Base):
    __tablename__ = 'provincias'
    __table_args__ = (
        Index('provincias_pais_cpa_uk', 'pais', 'cpa', unique=True),
        {'schema': 'gt'}
    )

    id = Column(NUMBER(5, 0, False), primary_key=True)
    cpa = Column(CHAR(2))
    provincia_esp = Column(VARCHAR(50))
    provincia_org = Column(VARCHAR(50))
    provincia_ing = Column(VARCHAR(50))
    pais = Column(ForeignKey('gt.paises.id'))
    region = Column(ForeignKey('gt.regiones.id'))
    id_zona = Column(ForeignKey('gt.zonas.id_zona'))

    zona = relationship('Zona')
    paise = relationship('Paise')
    regione = relationship('Regione')


class Direccione(Base):
    __tablename__ = 'direcciones'
    __table_args__ = {'schema': 'gt'}

    id = Column(NUMBER(6, 0, False), primary_key=True)
    direccion = Column(VARCHAR(200))
    poblacion = Column(VARCHAR(200))
    provincia = Column(ForeignKey('gt.provincias.id'))
    pais = Column(ForeignKey('gt.paises.id'))
    cp = Column(VARCHAR(10))
    observaciones = Column(VARCHAR(200))
    alias = Column(VARCHAR(20))
    nombre = Column(VARCHAR(100))
    estado = Column(CHAR(1))
    social = Column(CHAR(1), server_default=text("'S'"))
    fiscal = Column(CHAR(1), server_default=text("'S'"))
    almacen = Column(CHAR(1), server_default=text("'S'"))
    posicion_gps = Column(ForeignKey('gt.poblaciones.id'))
    fecha_creacion = Column(DateTime, server_default=text("SYSDATE"))
    usu_creacion = Column(VARCHAR(100))
    latitud = Column(NUMBER(asdecimal=False))
    longitud = Column(NUMBER(asdecimal=False))
    tipo_direccion = Column(NUMBER(2, 0, False), nullable=False, server_default=text("0 "))

    paise = relationship('Paise')
    poblacione = relationship('Poblacione')
    provincia1 = relationship('Provincia')


class TarifasProveedor(Base):
    __tablename__ = 'tarifas_proveedor'
    __table_args__ = (
        Index('ind_tarifas_proveedor_cte', 'cliente', 'id'),
        Index('ind_tarifas_proveedor_tarcte', 'tarifa', 'id'),
        Index('ind_tarifas_proveedor_veh', 'matricula', 'id'),
        Index('ind_tarifas_proveedor_prov', 'proveedor', 'id'),
        {'schema': 'gt'}
    )

    id = Column(NUMBER(6, 0, False), primary_key=True)
    proveedor = Column(VARCHAR(10))
    matricula = Column(NUMBER(6, 0, False))
    cliente = Column(VARCHAR(10))
    tarifa = Column(ForeignKey('gt.tarifas_cliente.id'))
    precio_viaje = Column(NUMBER(asdecimal=False))
    unidades = Column(CHAR(1))
    precio_unidad = Column(NUMBER(asdecimal=False))
    precio_nac = Column(NUMBER(asdecimal=False))
    precio_vnac = Column(NUMBER(asdecimal=False))
    precio_int = Column(NUMBER(asdecimal=False))
    precio_vint = Column(NUMBER(asdecimal=False))
    moneda = Column(ForeignKey('gt.monedas.id'), server_default=text("'EUR'"))
    unidades_2 = Column(CHAR(1))
    precio_unidad_2 = Column(NUMBER(asdecimal=False))
    u1_desde = Column(NUMBER(asdecimal=False))
    u1_hasta = Column(NUMBER(asdecimal=False))
    ratio = Column(NUMBER(asdecimal=False))
    imp_exp = Column(CHAR(1))
    zona_origen = Column(VARCHAR(5))
    zona_destino = Column(VARCHAR(5))
    fecha_inicio = Column(DateTime)
    fecha_fin = Column(DateTime)
    fecha_creacion = Column(DateTime)
    usu_creacion = Column(VARCHAR(100))
    ide = Column(NUMBER(10, 0, False))
    gl = Column(NUMBER(10, 0, False))
    tipo_apl_tarifa = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))
    tipo_vehiculo = Column(NUMBER(3, 0, False))
    id_poblacion_origen = Column(ForeignKey('gt.poblaciones.id'))
    id_poblacion_destino = Column(ForeignKey('gt.poblaciones.id'))

    poblacione = relationship('Poblacione', primaryjoin='TarifasProveedor.id_poblacion_destino == Poblacione.id')
    poblacione1 = relationship('Poblacione', primaryjoin='TarifasProveedor.id_poblacion_origen == Poblacione.id')
    moneda1 = relationship('Moneda')
    tarifas_cliente = relationship('TarifasCliente')


class CfBase(Base):
    __tablename__ = 'cf_bases'
    __table_args__ = {'schema': 'gt'}

    id = Column(NUMBER(3, 0, False), primary_key=True)
    nombre = Column(VARCHAR(20))
    direccion = Column(ForeignKey('gt.direcciones.id'))
    observaciones = Column(VARCHAR(200))

    direccione = relationship('Direccione')


class EmpresasDireccione(Base):
    __tablename__ = 'empresas_direcciones'
    __table_args__ = {'schema': 'gt'}

    empresa = Column(NUMBER(6, 0, False), primary_key=True, nullable=False)
    direccion = Column(ForeignKey('gt.direcciones.id'), primary_key=True, nullable=False)
    tipo = Column(CHAR(1))
    codigo = Column(VARCHAR(200))
    descripcion = Column(VARCHAR(120))
    codigo_externo = Column(VARCHAR(200))
    mail = Column(VARCHAR(300))

    direccione = relationship('Direccione')


class OrdenesTransporte(Base):
    __tablename__ = 'ordenes_transporte'
    __table_args__ = (
        Index('ind_ordenes_transporte_fk', 'gestor', 'ide', 'id'),
        Index('ind_ordenes_transporte_exp_id', 'ide', 'exp_id'),
        Index('ind_ordenes_transporte_fecha', 'fecha_ot', 'ide', 'id'),
        Index('ind_ordenes_transporte_emp', 'empresa', 'ide', 'id'),
        {'schema': 'gt'}
    )

    ide = Column(ForeignKey('gt.cm_empresas.id'), primary_key=True, nullable=False, server_default=text("1 "))
    id = Column(NUMBER(8, 0, False), primary_key=True, nullable=False)
    semi = Column(NUMBER(6, 0, False))
    gestor = Column(VARCHAR(20))
    empresa = Column(NUMBER(6, 0, False))
    agencia = Column(CHAR(1))
    para = Column(VARCHAR(50))
    atton = Column(VARCHAR(50))
    fax = Column(VARCHAR(30))
    importe_prov = Column(NUMBER(asdecimal=False))
    moneda = Column(CHAR(3), server_default=text("'EUR'"))
    tarifa = Column(ForeignKey('gt.tarifas_proveedor.id'))
    tipo_tarifa = Column(CHAR(1))
    importe_tarifa = Column(NUMBER(asdecimal=False))
    tipo = Column(CHAR(1), server_default=text("'N'"))
    kms = Column(NUMBER(asdecimal=False))
    albaran = Column(VARCHAR(150))
    tractora = Column(NUMBER(6, 0, False))
    remolque = Column(NUMBER(6, 0, False))
    horas = Column(NUMBER(asdecimal=False))
    estado = Column(CHAR(1), server_default=text("'A'"))
    gestor_flota = Column(VARCHAR(10))
    conductor1 = Column(ForeignKey('gt.conductores.id'))
    conductor2 = Column(ForeignKey('gt.conductores.id'))
    cantidad_minima = Column(NUMBER(asdecimal=False))
    observaciones = Column(VARCHAR(400))
    usu_creacion = Column(VARCHAR(50))
    fecha_creacion = Column(DateTime, server_default=text("SYSDATE"))
    usu_modificacion = Column(VARCHAR(50))
    fecha_modificacion = Column(DateTime)
    estado_admin = Column(ForeignKey('gt.ordenes_transporte_estados.id'), server_default=text("'0'"))
    fecha_ot = Column(DateTime)
    ide_factura = Column(NUMBER(3, 0, False))
    factura = Column(NUMBER(10, 0, False))
    observaciones_admin = Column(VARCHAR(400))
    conforme = Column(CHAR(1), server_default=text("'N'"))
    gl = Column(NUMBER(2, 0, False), server_default=text("1"))
    regularizacion = Column(VARCHAR(1))
    fuente = Column(VARCHAR(100))
    peso = Column(NUMBER(asdecimal=False))
    ot_cargada = Column(NUMBER(asdecimal=False))
    importe_prov_sistema = Column(NUMBER(asdecimal=False))
    id_cambio = Column(NUMBER(asdecimal=False))
    estado_flota = Column(ForeignKey('gt.ordenes_transporte_estado_env.id'))
    color = Column(VARCHAR(10))
    km_estimado = Column(NUMBER(asdecimal=False))
    tiempo_estimado = Column(NUMBER(asdecimal=False))
    importe_estimado = Column(NUMBER(asdecimal=False))
    oco_importe_extra = Column(NUMBER(asdecimal=False))
    emp_idp = Column(VARCHAR(10))
    emp_razon_social = Column(VARCHAR(100))
    emp_cif = Column(VARCHAR(30))
    emp_alias = Column(VARCHAR(50))
    exp_id = Column(NUMBER(8, 0, False))
    egl_nombre = Column(VARCHAR(100))
    veh_mat_tractora = Column(VARCHAR(12))
    veh_mat_remolque = Column(VARCHAR(12))
    con_nombre_cond1 = Column(VARCHAR(100))
    con_nombre_cond2 = Column(VARCHAR(100))
    ot_vacio_id = Column(NUMBER(8, 0, False))
    ot_vacio_org_zona = Column(VARCHAR(5))
    ot_vacio_org_poblacion = Column(VARCHAR(200))
    ot_vacio_kms = Column(NUMBER(asdecimal=False))
    ot_vacio_importe = Column(NUMBER(asdecimal=False))
    fac_num_oficial = Column(VARCHAR(20))
    otl_cantidad = Column(NUMBER(asdecimal=False))
    otl_unidad = Column(CHAR(1))
    otl_org_fecha = Column(DateTime)
    otl_org_fecha_prevista = Column(DateTime)
    otl_org_fecha_real = Column(DateTime)
    otl_org_fecha_inicio = Column(DateTime)
    otl_org_fecha_fin = Column(DateTime)
    otl_org_direccion_id = Column(NUMBER(6, 0, False))
    dir_org_nombre = Column(VARCHAR(100))
    dir_org_zona = Column(VARCHAR(5))
    dir_org_poblacion = Column(VARCHAR(200))
    dir_org_direccion = Column(VARCHAR(200))
    dir_org_latitud = Column(NUMBER(asdecimal=False))
    dir_org_longitud = Column(NUMBER(asdecimal=False))
    otl_des_fecha = Column(DateTime)
    otl_des_fecha_prevista = Column(DateTime)
    otl_des_fecha_real = Column(DateTime)
    otl_des_fecha_inicio = Column(DateTime)
    otl_des_fecha_fin = Column(DateTime)
    otl_des_direccion_id = Column(NUMBER(6, 0, False))
    dir_des_nombre = Column(VARCHAR(100))
    dir_des_zona = Column(VARCHAR(5))
    dir_des_poblacion = Column(VARCHAR(200))
    dir_des_direccion = Column(VARCHAR(200))
    dir_des_latitud = Column(NUMBER(asdecimal=False))
    dir_des_longitud = Column(NUMBER(asdecimal=False))
    dim_metros = Column(NUMBER(asdecimal=False))
    dim_peso = Column(NUMBER(asdecimal=False))
    dim_fc = Column(NUMBER(asdecimal=False))
    remolque2 = Column(NUMBER(6, 0, False))
    remolque3 = Column(NUMBER(6, 0, False))
    veh_mat_remolque2 = Column(VARCHAR(12))
    veh_mat_remolque3 = Column(VARCHAR(12))
    kms_rutas = Column(VARCHAR(13))
    grupo_tarifa = Column(NUMBER(7, 0, False))
    id_parte = Column(NUMBER(asdecimal=False))
    kms_nacionales = Column(NUMBER(asdecimal=False))
    kms_internacionales = Column(NUMBER(asdecimal=False))
    saltar_restriccion = Column(NUMBER(1, 0, False), nullable=False, server_default=text("0 "))
    dimension = Column(ForeignKey('gt.cf_dimensiones.id'))
    telefono = Column(VARCHAR(100))
    otl_org_gmt = Column(NUMBER(2, 0, False))
    otl_des_gmt = Column(NUMBER(2, 0, False))

    conductore = relationship('Conductore', primaryjoin='OrdenesTransporte.conductor1 == Conductore.id')
    conductore1 = relationship('Conductore', primaryjoin='OrdenesTransporte.conductor2 == Conductore.id')
    cf_dimensione = relationship('CfDimensione')
    ordenes_transporte_estado = relationship('OrdenesTransporteEstado')
    ordenes_transporte_estado_env = relationship('OrdenesTransporteEstadoEnv')
    cm_empresa = relationship('CmEmpresa')
    tarifas_proveedor = relationship('TarifasProveedor')


class PedidosEtapa(Base):
    __tablename__ = 'pedidos_etapas'
    __table_args__ = (
        CheckConstraint('ETAPA BETWEEN 1 AND 99'),
        Index('ind_pedidos_etapa_dir', 'direccion', 'ide', 'pedido', 'etapa'),
        Index('ind_ped_etap_fecha', 'ide', 'pedido', 'etapa', 'fecha'),
        Index('ide_ped_etapas_fecreal', 'ide', 'pedido', 'etapa', 'fecha_real', 'fecha'),
        {'schema': 'gt'}
    )

    ide = Column(NUMBER(3, 0, False), primary_key=True, nullable=False, server_default=text("1 "))
    pedido = Column(NUMBER(8, 0, False), primary_key=True, nullable=False)
    etapa = Column(NUMBER(3, 0, False), primary_key=True, nullable=False)
    tipo = Column(CHAR(1))
    direccion = Column(ForeignKey('gt.direcciones.id'))
    fecha = Column(DateTime, nullable=False, server_default=text("SYSDATE "))
    hora = Column(VARCHAR(5), server_default=text("'00:01'"))
    fecha_real = Column(DateTime)
    hora_real = Column(VARCHAR(5), server_default=text("null"))
    fecha_fin_carga = Column(DateTime)
    hora_fin_carga = Column(VARCHAR(5), server_default=text("null"))
    fecha_flota = Column(DateTime)
    hora_flota = Column(VARCHAR(5), server_default=text("null"))
    cantidad_carga = Column(NUMBER(asdecimal=False))
    unidad_carga = Column(CHAR(1))
    cantidad_carga2 = Column(NUMBER(asdecimal=False))
    unidad_carga2 = Column(CHAR(1))
    km = Column(NUMBER(5, 0, False))
    horas = Column(NUMBER(asdecimal=False))
    importe_etapa = Column(NUMBER(asdecimal=False))
    moneda_importe_etapa = Column(CHAR(3))
    observaciones = Column(VARCHAR(200))
    importe_etapa_sistema = Column(NUMBER(asdecimal=False))
    gmt = Column(NUMBER(2, 0, False))
    fecha_inicio_ventana = Column(DateTime)
    fecha_fin_ventana = Column(DateTime)
    dir_nombre = Column(VARCHAR(100))
    dir_pais = Column(VARCHAR(2))
    dir_poblacion = Column(VARCHAR(200))
    dir_direccion = Column(VARCHAR(200))
    dir_cp = Column(VARCHAR(10))
    id_ot_linea = Column(NUMBER(9, 0, False))
    dir_zona = Column(VARCHAR(10))
    dir_latitud = Column(NUMBER(asdecimal=False))
    dir_longitud = Column(NUMBER(asdecimal=False))
    codigo_externo = Column(VARCHAR(20))
    fecha_inicio_carga = Column(DateTime)
    retraso = Column(NUMBER(1, 0, False))
    fecha_eta_manual = Column(DateTime)
    visor_europroveedores = Column(NUMBER(1, 0, False), nullable=False, server_default=text("0 "))
    slot = Column(VARCHAR(40))
    id_linea = Column(NUMBER(9, 0, False), unique=True)
    punto_control = Column(NUMBER(1, 0, False))
    ponumber = Column(VARCHAR(200))
    fecha_prev_salida = Column(DateTime)
    eta_automatica = Column(DateTime)
    muelle = Column(VARCHAR(150))

    direccione = relationship('Direccione')


class CfVehiculo(Base):
    __tablename__ = 'cf_vehiculos'
    __table_args__ = (
        Index('ind_cf_vehiculos_empresas', 'empresa', 'id'),
        {'schema': 'gt'}
    )

    id = Column(NUMBER(6, 0, False), primary_key=True)
    matricula = Column(VARCHAR(12), nullable=False, unique=True)
    tipo = Column(ForeignKey('gt.cf_tipos_vehiculo.id'))
    marca = Column(VARCHAR(30))
    modelo = Column(VARCHAR(50))
    estado = Column(CHAR(1), server_default=text("'A'"))
    empresa = Column(NUMBER(6, 0, False))
    base = Column(ForeignKey('gt.cf_bases.id'))
    gestor = Column(NUMBER(asdecimal=False))
    fecha_matriculacion = Column(DateTime)
    fecha_inicio_servicio = Column(DateTime)
    fecha_fin_servicio = Column(DateTime)
    bastidor = Column(VARCHAR(20))
    tacografo = Column(VARCHAR(20))
    ruedas = Column(VARCHAR(20))
    gps = Column(VARCHAR(20))
    telefono = Column(VARCHAR(20))
    observaciones = Column(VARCHAR(200))
    neumaticos = Column(VARCHAR(30))
    tacografo_fecha = Column(DateTime)
    ruedas_fecha = Column(DateTime)
    propio = Column(CHAR(1))
    asociado = Column(ForeignKey('gt.cf_vehiculos.id'))
    potencia = Column(NUMBER(5, 0, False))
    tipo_tacografo = Column(CHAR(1))
    extension = Column(VARCHAR(8))
    tfno_sustitucion = Column(VARCHAR(30))
    fecha_dev_tfno_sus = Column(DateTime)
    tablas = Column(NUMBER(3, 0, False))
    cable_tir = Column(CHAR(1))
    plomo = Column(CHAR(1))
    tp_elevacion = Column(CHAR(1))
    tp_tricarril = Column(CHAR(1))
    tp_tarjeta = Column(CHAR(1))
    delegacion = Column(ForeignKey('gt.cm_delegaciones.id'))
    matricula_con_separadores = Column(VARCHAR(20))
    tipo_proveedor = Column(VARCHAR(1))
    usu_creacion = Column(VARCHAR(50))
    fecha_creacion = Column(DateTime, server_default=text("sysdate"))
    usu_modificacion = Column(VARCHAR(50))
    fecha_modificacion = Column(DateTime, server_default=text("sysdate"))
    orden = Column(NUMBER(asdecimal=False))
    numero_depositos = Column(NUMBER(asdecimal=False))
    capacidad_deposito = Column(NUMBER(asdecimal=False))
    clasificacion_euro = Column(VARCHAR(30))
    fecha_ultima_itv = Column(DateTime)
    fecha_proxima_itv = Column(DateTime)
    periodo_aviso_itv = Column(NUMBER(asdecimal=False))
    periodo_bloqueo_itv = Column(NUMBER(asdecimal=False))
    fecha_ultimo_mant = Column(DateTime)
    fecha_proximo_mant = Column(DateTime)
    dias_aviso = Column(NUMBER(asdecimal=False))
    dias_bloqueo = Column(NUMBER(asdecimal=False))
    dias_entre_mant = Column(NUMBER(asdecimal=False))
    kms_ultimo_mant = Column(NUMBER(asdecimal=False))
    kms_proximo_mant = Column(NUMBER(asdecimal=False))
    kms_aviso = Column(NUMBER(asdecimal=False))
    kms_bloqueo = Column(NUMBER(asdecimal=False))
    kms_entre_mant = Column(NUMBER(asdecimal=False))
    periodo_aviso_mant_taco = Column(NUMBER(3, 0, False))
    periodo_bloqueo_mant_taco = Column(NUMBER(3, 0, False))
    fecha_ultimo_mant_taco = Column(DateTime)
    fecha_proximo_mant_taco = Column(DateTime)
    dimension = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("null "))
    subdimension = Column(NUMBER(asdecimal=False), nullable=False)
    tipos_operaciones = Column(NUMBER(asdecimal=False), server_default=text("4"))
    empresa_propietaria = Column(ForeignKey('gt.empresas.id'))
    kms_rutas = Column(VARCHAR(13))
    fecha_ultima_conexion = Column(DateTime)
    remolque = Column(VARCHAR(20))
    conductor1 = Column(VARCHAR(70))
    conductor2 = Column(VARCHAR(70))
    fecha_ultima_posicion = Column(DateTime)
    latitud = Column(VARCHAR(20))
    longitud = Column(VARCHAR(20))
    velocidad = Column(NUMBER(asdecimal=False))
    rumbo = Column(VARCHAR(10))
    posicion_ciudad = Column(VARCHAR(200))
    posicion_pueblo = Column(VARCHAR(200))
    nivel_deposito = Column(NUMBER(asdecimal=False))
    nuevo_mensaje = Column(NUMBER(1, 0, False))
    nueva_incidencia = Column(NUMBER(1, 0, False))
    motivo_baja = Column(ForeignKey('gt.cf_vehiculos_baja.id'))
    motor_encendido = Column(NUMBER(1, 0, False))
    ide_explotacion = Column(ForeignKey('gt.cm_empresas.id'))
    estado_frigo = Column(VARCHAR(100))
    temperatura = Column(NUMBER(asdecimal=False))
    set_point = Column(NUMBER(asdecimal=False))
    peso = Column(NUMBER(asdecimal=False))
    id_conductor1 = Column(NUMBER(6, 0, False))
    id_conductor2 = Column(NUMBER(6, 0, False))
    kms_teoricos = Column(NUMBER(6, 0, False))
    kms_ot = Column(NUMBER(6, 0, False))
    kms_reales = Column(NUMBER(6, 0, False))
    kms_registrados = Column(NUMBER(asdecimal=False))
    parada = Column(NUMBER(1, 0, False))
    tipo_plataforma = Column(VARCHAR(10))
    gas_centro_coste = Column(VARCHAR(30))
    gas_grupo_empresa = Column(NUMBER(6, 0, False))
    gas_tipo = Column(VARCHAR(30))
    gas_empresa_liquidadora = Column(VARCHAR(30))
    gas_empresa_facturacion = Column(ForeignKey('gt.empresas.id'))
    liquidar = Column(VARCHAR(1))
    precio_liq = Column(NUMBER(asdecimal=False))
    standby = Column(NUMBER(1, 0, False))
    ot_ide = Column(NUMBER(3, 0, False))
    ot_id = Column(NUMBER(8, 0, False))
    ot_tipo = Column(CHAR(1))
    ot_org_fecha_prevista = Column(DateTime)
    ot_org_fecha_real = Column(DateTime)
    ot_org_fecha_inicio = Column(DateTime)
    ot_org_fecha_fin = Column(DateTime)
    ot_org_direccion_id = Column(NUMBER(6, 0, False))
    ot_org_nombre_dir = Column(VARCHAR(100))
    ot_org_alias_dir = Column(VARCHAR(100))
    ot_org_zona = Column(VARCHAR(5))
    ot_org_poblacion = Column(VARCHAR(200))
    ot_org_direccion = Column(VARCHAR(200))
    ot_org_latitud = Column(NUMBER(asdecimal=False))
    ot_org_longitud = Column(NUMBER(asdecimal=False))
    ot_des_fecha_prevista = Column(DateTime)
    ot_des_fecha_real = Column(DateTime)
    ot_des_fecha_inicio = Column(DateTime)
    ot_des_fecha_fin = Column(DateTime)
    ot_des_direccion_id = Column(NUMBER(6, 0, False))
    ot_des_nombre_dir = Column(VARCHAR(100))
    ot_des_alias_dir = Column(VARCHAR(100))
    ot_des_zona = Column(VARCHAR(5))
    ot_des_poblacion = Column(VARCHAR(200))
    ot_des_direccion = Column(VARCHAR(200))
    ot_des_latitud = Column(NUMBER(asdecimal=False))
    ot_des_longitud = Column(NUMBER(asdecimal=False))
    ot_ultima_tractora = Column(VARCHAR(12))
    ot_ultimo_remolque = Column(VARCHAR(12))
    ot_dim_metros = Column(NUMBER(asdecimal=False))
    ot_dim_peso = Column(NUMBER(asdecimal=False))
    ot_dim_fc = Column(NUMBER(asdecimal=False))
    ot_fecha = Column(DateTime)
    ot_zona = Column(VARCHAR(10))
    ot_poblacion = Column(VARCHAR(200))
    ot_direccion = Column(NUMBER(asdecimal=False))
    ot_etapa = Column(NUMBER(2, 0, False))
    descripcion = Column(VARCHAR(30))
    centro_trabajo = Column(VARCHAR(500))

    parent = relationship('CfVehiculo', remote_side=[id])
    cf_base = relationship('CfBase')
    cm_delegacione = relationship('CmDelegacione')
    empresa1 = relationship('Empresa', primaryjoin='CfVehiculo.empresa_propietaria == Empresa.id')
    empresa2 = relationship('Empresa', primaryjoin='CfVehiculo.gas_empresa_facturacion == Empresa.id')
    cm_empresa = relationship('CmEmpresa')
    cf_vehiculos_baja = relationship('CfVehiculosBaja')
    cf_tipos_vehiculo = relationship('CfTiposVehiculo')


class OrdenesTransporteLinea(Base):
    __tablename__ = 'ordenes_transporte_lineas'
    __table_args__ = (
        ForeignKeyConstraint(['ide', 'ot'], ['gt.ordenes_transporte.ide', 'gt.ordenes_transporte.id']),
        Index('ind_ot_lineas_dir', 'direccion', 'ot', 'etapa_t'),
        Index('ind_ot_lineas_pedido', 'pedido', 'ot', 'etapa_t'),
        {'schema': 'gt'}
    )

    ide = Column(NUMBER(3, 0, False), primary_key=True, nullable=False, server_default=text("1 "))
    ot = Column(NUMBER(8, 0, False), primary_key=True, nullable=False)
    etapa_t = Column(NUMBER(2, 0, False), primary_key=True, nullable=False)
    etapa_p = Column(NUMBER(2, 0, False))
    ide_pedido = Column(NUMBER(3, 0, False), server_default=text("1"))
    pedido = Column(NUMBER(8, 0, False))
    tipo = Column(CHAR(1))
    direccion = Column(ForeignKey('gt.direcciones.id'))
    cantidad = Column(NUMBER(asdecimal=False))
    tractora = Column(NUMBER(6, 0, False))
    semi = Column(NUMBER(6, 0, False))
    unidad = Column(CHAR(1))
    conductor1 = Column(ForeignKey('gt.conductores.id'))
    conductor2 = Column(ForeignKey('gt.conductores.id'))
    referencia = Column(VARCHAR(30))
    fecha = Column(DateTime)
    hora = Column(VARCHAR(5), server_default=text("'00:01'"))
    fecha_real = Column(DateTime)
    hora_real = Column(VARCHAR(5), server_default=text("null"))
    observaciones = Column(VARCHAR(200))
    kms = Column(NUMBER(asdecimal=False))
    fecha_inicio = Column(DateTime)
    fecha_fin = Column(DateTime)
    pais = Column(VARCHAR(2))
    cpa = Column(VARCHAR(3))
    poblacion = Column(VARCHAR(60))
    calle = Column(VARCHAR(200))
    latitud = Column(VARCHAR(20))
    longitud = Column(VARCHAR(20))
    palets = Column(NUMBER(asdecimal=False))
    kgs = Column(NUMBER(asdecimal=False))
    metros = Column(NUMBER(asdecimal=False))
    coincide_direccion = Column(NUMBER(1, 0, False))
    presencia_conductor = Column(NUMBER(1, 0, False))
    accion_conductor = Column(NUMBER(1, 0, False))
    tipo_incidencia = Column(NUMBER(6, 0, False))
    gmt = Column(NUMBER(asdecimal=False))
    ponumber = Column(VARCHAR(200))
    km_aux = Column(NUMBER(asdecimal=False))
    id_linea = Column(NUMBER(9, 0, False))
    nombre = Column(VARCHAR(200))
    zona = Column(VARCHAR(10))
    cp = Column(VARCHAR(10))
    codigo_externo = Column(VARCHAR(20))
    eta_automatica = Column(DateTime)
    etd = Column(DateTime)

    conductore = relationship('Conductore', primaryjoin='OrdenesTransporteLinea.conductor1 == Conductore.id')
    conductore1 = relationship('Conductore', primaryjoin='OrdenesTransporteLinea.conductor2 == Conductore.id')
    direccione = relationship('Direccione')
    ordenes_transporte = relationship('OrdenesTransporte')
