# coding: utf-8
from sqlalchemy import CHAR, CheckConstraint, Column, DateTime, ForeignKey, ForeignKeyConstraint, Index, Integer, NVARCHAR, VARCHAR, text
from sqlalchemy.dialects.oracle import NUMBER
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class BloqueoAdmProvMotivo(Base):
    __tablename__ = 'bloqueo_adm_prov_motivos'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    descripcion = Column(VARCHAR(50))
    activo = Column(NUMBER(1, 0, False))


class BloqueoAdmProvTipo(Base):
    __tablename__ = 'bloqueo_adm_prov_tipos'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    descripcion = Column(VARCHAR(50))
    activo = Column(NUMBER(1, 0, False))


class CfDimensione(Base):
    __tablename__ = 'cf_dimensiones'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    descripcion = Column(VARCHAR(30))


class CfTiposVehiculo(Base):
    __tablename__ = 'cf_tipos_vehiculo'

    id = Column(NUMBER(3, 0, False), primary_key=True)
    nombre = Column(VARCHAR(50))
    caracteristicas = Column(VARCHAR(200))
    arrastre = Column(VARCHAR(1))
    autonomo = Column(CHAR(1))
    nombre_us = Column(VARCHAR(50))


class CmCentrosTrabajo(Base):
    __tablename__ = 'cm_centros_trabajo'

    id = Column(NUMBER(3, 0, False), primary_key=True)
    nombre = Column(VARCHAR(50))
    descripcion = Column(VARCHAR(200))


class CmDepartamento(Base):
    __tablename__ = 'cm_departamentos'

    id = Column(NUMBER(3, 0, False), primary_key=True)
    nombre = Column(VARCHAR(50))
    descripcion = Column(VARCHAR(200))
    mail = Column(VARCHAR(50))


class CmEmpresa(Base):
    __tablename__ = 'cm_empresas'

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
    pais = Column(VARCHAR(2))
    restriccion_conductor = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("(0) "))
    restriccion_conductor2 = Column(NUMBER(asdecimal=False), server_default=text("""\
0
"""))
    tipo_cierre = Column(NUMBER(10, 0, False), nullable=False, server_default=text("0 "))


class DigDocumentacionCliente(Base):
    __tablename__ = 'dig_documentacion_cliente'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    codigo = Column(VARCHAR(20), nullable=False)
    idioma = Column(VARCHAR(2), nullable=False)
    activo = Column(NUMBER(1, 0, False), server_default=text("0"))


class EmpresasEstado(Base):
    __tablename__ = 'empresas_estados'

    id = Column(CHAR(1), primary_key=True)
    descripcion = Column(VARCHAR(25))


class EmpresasGrCtbCli(Base):
    __tablename__ = 'empresas_gr_ctb_cli'
    __table_args__ = (
        Index('ind_emp_gr_ctb_cli_uq', 'ide', 'id', unique=True),
    )

    ide = Column(NUMBER(asdecimal=False), nullable=False)
    id = Column(NUMBER(asdecimal=False), primary_key=True)
    codigo = Column(VARCHAR(50))
    activo = Column(VARCHAR(1))
    intragrupo = Column(VARCHAR(1))


class EmpresasGrCtbNeg(Base):
    __tablename__ = 'empresas_gr_ctb_neg'
    __table_args__ = (
        Index('ind_emp_gr_ctb_neg_cli', 'ide', 'id', 'activo_cli'),
        Index('ind_emp_gr_ctb_neg_pro', 'ide', 'id', 'activo_pro')
    )

    ide = Column(NUMBER(asdecimal=False), nullable=False)
    id = Column(NUMBER(asdecimal=False), primary_key=True)
    codigo = Column(VARCHAR(11))
    descripcion = Column(VARCHAR(50))
    activo_cli = Column(VARCHAR(1))
    activo_pro = Column(VARCHAR(1))


class EmpresasGrCtbPro(Base):
    __tablename__ = 'empresas_gr_ctb_pro'
    __table_args__ = (
        Index('ind_gr_ctb_pro', 'ide', 'id', 'activo'),
        Index('ind_gr_ctb_pro_uq', 'ide', 'id', unique=True)
    )

    ide = Column(NUMBER(asdecimal=False), nullable=False)
    id = Column(NUMBER(asdecimal=False), primary_key=True)
    codigo = Column(VARCHAR(50))
    activo = Column(VARCHAR(1))
    intragrupo = Column(VARCHAR(1))


class EmpresasMotivoBaja(Base):
    __tablename__ = 'empresas_motivo_baja'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    descripcion = Column(VARCHAR(25))
    general = Column(NUMBER(1, 0, False), server_default=text("1 "))
    activo = Column(NUMBER(1, 0, False), nullable=False, server_default=text("1 "))


class EmpresasSectore(Base):
    __tablename__ = 'empresas_sectores'

    id = Column(NUMBER(4, 0, False), primary_key=True)
    nombre = Column(VARCHAR(30))
    observaciones = Column(VARCHAR(150))
    nombre_us = Column(VARCHAR(30))


class EmpresasTiposCliente(Base):
    __tablename__ = 'empresas_tipos_cliente'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    descripcion = Column(VARCHAR(50))
    nombre_us = Column(VARCHAR(50))


class EmpresasTiposProveedor(Base):
    __tablename__ = 'empresas_tipos_proveedor'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    descripcion = Column(VARCHAR(50))
    activo = Column(VARCHAR(1))
    nombre_us = Column(VARCHAR(50))
    bloqueo_matricula = Column(NUMBER(1, 0, False))
    bloqueo_tarifa = Column(NUMBER(1, 0, False))
    bloqueo_kms = Column(NUMBER(1, 0, False))
    rol_permitido = Column(VARCHAR(100))


class OrigenDatosDivisa(Base):
    __tablename__ = 'origen_datos_divisas'

    origen_datos_divisas_id = Column(NUMBER(10, 0, False), primary_key=True)
    origen_datos = Column(VARCHAR(512), nullable=False)
    tipo = Column(NUMBER(10, 0, False), nullable=False)
    origen_datos_nombre = Column(VARCHAR(100))


class Regione(Base):
    __tablename__ = 'regiones'

    id = Column(NUMBER(5, 0, False), primary_key=True)
    descripcion = Column(VARCHAR(100))
    nombre = Column(VARCHAR(50))


class TiposConceptosTarifa(Base):
    __tablename__ = 'tipos_conceptos_tarifas'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    descripcion = Column(VARCHAR(200))
    activo = Column(CHAR(1))
    tipo = Column(CHAR(1))
    descripcion_us = Column(VARCHAR(200))


class TiposImpuesto(Base):
    __tablename__ = 'tipos_impuesto'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    descripcion = Column(VARCHAR(200))


class TiposPagoCobro(Base):
    __tablename__ = 'tipos_pago_cobro'

    id = Column(NUMBER(3, 0, False), primary_key=True)
    descripcion = Column(VARCHAR(100))
    idnav = Column(VARCHAR(10))
    idinvoic = Column(VARCHAR(3))
    ide = Column(NUMBER(asdecimal=False), nullable=False)
    activo = Column(NUMBER(1, 0, False))


class TiposUrgencia(Base):
    __tablename__ = 'tipos_urgencia'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    descripcion = Column(VARCHAR(200))


class VehiculosMarca(Base):
    __tablename__ = 'vehiculos_marcas'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    marca = Column(VARCHAR(100))
    codigo = Column(VARCHAR(100))


class VehiculosTipo(Base):
    __tablename__ = 'vehiculos_tipos'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    codigo = Column(VARCHAR(50))
    nombre = Column(VARCHAR(50))
    activo = Column(NUMBER(1, 0, False))
    peso = Column(NUMBER(asdecimal=False))


class Zona(Base):
    __tablename__ = 'zonas'

    id_zona = Column(NUMBER(10, 0, False), primary_key=True)
    pais = Column(CHAR(2))
    nombre_zona = Column(VARCHAR(35))


class CmUsuario(Base):
    __tablename__ = 'cm_usuarios'

    id = Column(NUMBER(6, 0, False), primary_key=True)
    login = Column(VARCHAR(20), nullable=False, unique=True)
    pw = Column(VARCHAR(10))
    nombre = Column(VARCHAR(50))
    apellidos = Column(VARCHAR(100))
    departamento = Column(ForeignKey('cm_departamentos.id'))
    mail = Column(VARCHAR(200))
    telefono_movil = Column(VARCHAR(15))
    telefono_fijo = Column(VARCHAR(15))
    extension = Column(VARCHAR(5))
    centro_trabajo = Column(ForeignKey('cm_centros_trabajo.id'))
    fecha_alta = Column(DateTime, server_default=text("SYSDATE"))
    fecha_baja = Column(DateTime)
    observaciones = Column(VARCHAR(200))
    ide = Column(NUMBER(3, 0, False))
    ided = Column(NUMBER(3, 0, False))
    sub_departamento = Column(NUMBER(3, 0, False))
    generic = Column(NUMBER(1, 0, False), server_default=text("""\
0
"""))

    cm_centros_trabajo = relationship('CmCentrosTrabajo')
    cm_departamento = relationship('CmDepartamento')


class Moneda(Base):
    __tablename__ = 'monedas'

    id = Column(CHAR(3), primary_key=True)
    nombre = Column(VARCHAR(100))
    unidades = Column(NUMBER(6, 0, False))
    cambio_fijo = Column(NUMBER(9, 3, True))
    origen_datos_divisas_id = Column(ForeignKey('origen_datos_divisas.origen_datos_divisas_id'))
    activo = Column(NVARCHAR(1), nullable=False, server_default=text("'N' "))

    origen_datos_divisas = relationship('OrigenDatosDivisa')


class Paise(Base):
    __tablename__ = 'paises'

    id = Column(CHAR(2), primary_key=True)
    codigo_ison = Column(NUMBER(3, 0, False))
    codigo_iso3 = Column(CHAR(3))
    pais_esp = Column(VARCHAR(100))
    pais_ing = Column(VARCHAR(100))
    pais_org = Column(VARCHAR(100))
    observaciones = Column(VARCHAR(200))
    activo = Column(VARCHAR(1))
    ue = Column(VARCHAR(1), server_default=text("'N'"))
    zona_horaria = Column(ForeignKey('zonas.id_zona'))

    zona = relationship('Zona')


class VehiculosModelo(Base):
    __tablename__ = 'vehiculos_modelos'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    id_tipo = Column(ForeignKey('vehiculos_tipos.id'))
    id_marca = Column(ForeignKey('vehiculos_marcas.id'))
    modelo = Column(VARCHAR(100))
    codigo = Column(VARCHAR(25))
    peso = Column(NUMBER(asdecimal=False))
    lf = Column(NUMBER(asdecimal=False))

    vehiculos_marca = relationship('VehiculosMarca')
    vehiculos_tipo = relationship('VehiculosTipo')


class EmpresasIde(Base):
    __tablename__ = 'empresas_ide'
    __table_args__ = (
        ForeignKeyConstraint(['ide', 'gr_ctb_cli'], ['empresas_gr_ctb_cli.ide', 'empresas_gr_ctb_cli.id']),
        ForeignKeyConstraint(['ide', 'gr_ctb_pro'], ['empresas_gr_ctb_pro.ide', 'empresas_gr_ctb_pro.id'])
    )

    ide = Column(NUMBER(3, 0, False), primary_key=True, nullable=False)
    id = Column(NUMBER(6, 0, False), primary_key=True, nullable=False)
    gr_ctb_cli = Column(NUMBER(asdecimal=False))
    gr_ctb_pro = Column(NUMBER(asdecimal=False))
    gr_ctb_neg_cli = Column(ForeignKey('empresas_gr_ctb_neg.id'))
    gr_ctb_neg_pro = Column(ForeignKey('empresas_gr_ctb_neg.id'))
    gr_reg_iva_neg_cli = Column(NUMBER(asdecimal=False))
    gr_reg_iva_neg_pro = Column(NUMBER(asdecimal=False))
    gr_tax_area = Column(NUMBER(asdecimal=False))
    gr_tax_area_cli = Column(NUMBER(asdecimal=False))
    gr_tax_area_pro = Column(NUMBER(asdecimal=False))
    edi_gen_eventos = Column(NUMBER(1, 0, False), nullable=False, server_default=text("0 "))
    id_comercial = Column(ForeignKey('cm_usuarios.id'))
    fecha_modificacion = Column(DateTime)
    usu_modificacion = Column(VARCHAR(50))

    empresas_gr_ctb_neg = relationship('EmpresasGrCtbNeg', primaryjoin='EmpresasIde.gr_ctb_neg_cli == EmpresasGrCtbNeg.id')
    empresas_gr_ctb_neg1 = relationship('EmpresasGrCtbNeg', primaryjoin='EmpresasIde.gr_ctb_neg_pro == EmpresasGrCtbNeg.id')
    cm_usuario = relationship('CmUsuario')
    empresas_gr_ctb_cli = relationship('EmpresasGrCtbCli')
    empresas_gr_ctb_pro = relationship('EmpresasGrCtbPro')


class PedidosConcepto(Base):
    __tablename__ = 'pedidos_conceptos'
    __table_args__ = (
        Index('ind_pedidos_concep_ide_ped_id', 'ide', 'pedido', 'id'),
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    ide = Column(NUMBER(3, 0, False), nullable=False, server_default=text("1 "))
    pedido = Column(NUMBER(8, 0, False), nullable=False)
    concepto = Column(ForeignKey('tipos_conceptos_tarifas.id'), nullable=False)
    importe = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))
    moneda = Column(ForeignKey('monedas.id'), server_default=text("'EUR'"))
    importe_unidad = Column(NUMBER(asdecimal=False))
    cantidad = Column(NUMBER(asdecimal=False))
    observaciones = Column(VARCHAR(200))
    importe_sistema = Column(NUMBER(asdecimal=False))

    tipos_conceptos_tarifa = relationship('TiposConceptosTarifa')
    moneda1 = relationship('Moneda')


class Poblacione(Base):
    __tablename__ = 'poblaciones'
    __table_args__ = (
        Index('poblaciones_pais_poblacion_cpa', 'pais', 'cpa', 'poblacion_consultas'),
        Index('ind_pais_poblacion', 'pais', 'poblacion')
    )

    id = Column(NUMBER(8, 0, False), primary_key=True)
    poblacion = Column(VARCHAR(50))
    poblacion_principal = Column(VARCHAR(50))
    area = Column(VARCHAR(50))
    pais = Column(ForeignKey('paises.id'))
    ruta = Column(VARCHAR(200))
    latitud = Column(NUMBER(10, 5, True))
    longitud = Column(NUMBER(10, 5, True))
    poblacion_consultas = Column(VARCHAR(50))
    ruta_consultas = Column(VARCHAR(200))
    provincia = Column(NUMBER(5, 0, False))
    cpa = Column(VARCHAR(2))
    zona_horaria = Column(ForeignKey('zonas.id_zona'))

    paise = relationship('Paise')
    zona = relationship('Zona')


class Provincia(Base):
    __tablename__ = 'provincias'
    __table_args__ = (
        Index('provincias_pais_cpa_uk', 'pais', 'cpa', unique=True),
    )

    id = Column(NUMBER(5, 0, False), primary_key=True)
    cpa = Column(CHAR(2))
    provincia_esp = Column(VARCHAR(50))
    provincia_org = Column(VARCHAR(50))
    provincia_ing = Column(VARCHAR(50))
    pais = Column(ForeignKey('paises.id'))
    region = Column(ForeignKey('regiones.id'))
    id_zona = Column(ForeignKey('zonas.id_zona'))

    zona = relationship('Zona')
    paise = relationship('Paise')
    regione = relationship('Regione')


class TarifasCliente(Base):
    __tablename__ = 'tarifas_cliente'
    __table_args__ = (
        CheckConstraint("TIPO in ('T','U')"),
        CheckConstraint("remontable in ('S','N')"),
        CheckConstraint("req_vehiculo in ('S','N')"),
        CheckConstraint("unidad in ('B','H','C','G','K','D','M','P','Z','Q','T','E','V', 'X')"),
        Index('ind_tarifas_cliente_emp', 'cliente', 'id')
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
    moneda = Column(ForeignKey('monedas.id'), server_default=text("'EUR'"))
    iva = Column(NUMBER(3, 0, False))
    descuento = Column(NUMBER(5, 0, False))
    tp_vehiculo = Column(ForeignKey('cf_tipos_vehiculo.id'))
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
    unidad2 = Column(CHAR(1), server_default=text("'M'"))
    desde2 = Column(NUMBER(asdecimal=False))
    hasta2 = Column(NUMBER(asdecimal=False))
    minimo2 = Column(NUMBER(asdecimal=False))
    maximo2 = Column(NUMBER(asdecimal=False))

    moneda1 = relationship('Moneda')
    cf_tipos_vehiculo = relationship('CfTiposVehiculo')


class Direccione(Base):
    __tablename__ = 'direcciones'

    id = Column(NUMBER(6, 0, False), primary_key=True)
    direccion = Column(VARCHAR(200))
    poblacion = Column(VARCHAR(200))
    provincia = Column(ForeignKey('provincias.id'))
    pais = Column(ForeignKey('paises.id'))
    cp = Column(VARCHAR(10))
    observaciones = Column(VARCHAR(200))
    alias = Column(VARCHAR(20))
    nombre = Column(VARCHAR(100))
    estado = Column(CHAR(1))
    social = Column(CHAR(1), server_default=text("'S'"))
    fiscal = Column(CHAR(1), server_default=text("'S'"))
    almacen = Column(CHAR(1), server_default=text("'S'"))
    posicion_gps = Column(ForeignKey('poblaciones.id'))
    fecha_creacion = Column(DateTime, server_default=text("SYSDATE"))
    usu_creacion = Column(VARCHAR(100))
    latitud = Column(NUMBER(asdecimal=False))
    longitud = Column(NUMBER(asdecimal=False))
    tipo_direccion = Column(NUMBER(2, 0, False), nullable=False, server_default=text("0 "))

    paise = relationship('Paise')
    poblacione = relationship('Poblacione')
    provincia1 = relationship('Provincia')


class Empresa(Base):
    __tablename__ = 'empresas'
    __table_args__ = (
        ForeignKeyConstraint(['ide_empresas_ide', 'id_empresa_ide'], ['empresas_ide.ide', 'empresas_ide.id']),
        Index('empresas_cseguro_nif', 'codigo_seguro', 'cif')
    )

    id = Column(NUMBER(6, 0, False), primary_key=True)
    razon_social = Column(VARCHAR(100))
    alias = Column(VARCHAR(50))
    cif = Column(VARCHAR(30), index=True)
    moneda = Column(ForeignKey('monedas.id'))
    sector = Column(ForeignKey('empresas_sectores.id'))
    fecha_alta = Column(DateTime, server_default=text("Sysdate"))
    fecha_baja = Column(DateTime)
    iva = Column(NUMBER(4, 2, True))
    forma_pago = Column(ForeignKey('tipos_pago_cobro.id'))
    forma_cobro = Column(ForeignKey('tipos_pago_cobro.id'))
    vencimiento_pago = Column(NUMBER(3, 0, False))
    vencimiento_cobro = Column(NUMBER(3, 0, False))
    idc = Column(VARCHAR(10), unique=True)
    idp = Column(VARCHAR(10), unique=True)
    irpf = Column(NUMBER(4, 0, False))
    grupo = Column(VARCHAR(30))
    estado = Column(ForeignKey('empresas_estados.id'), server_default=text("'A'"))
    web = Column(VARCHAR(100))
    pais = Column(ForeignKey('paises.id'))
    empresa_fiscal = Column(ForeignKey('empresas.id'))
    siglas = Column(VARCHAR(3))
    dias_pago = Column(VARCHAR(20))
    observaciones = Column(VARCHAR(200))
    tipo_impuesto = Column(ForeignKey('tipos_impuesto.id'))
    tipo_proveedor = Column(ForeignKey('empresas_tipos_proveedor.id'))
    fecha_alta_cliente = Column(DateTime)
    fecha_baja_cliente = Column(DateTime)
    bloqueo_cliente = Column(CHAR(1), server_default=text("'N'"))
    fecha_alta_proveedor = Column(DateTime)
    fecha_baja_proveedor = Column(DateTime)
    bloqueo_proveedor = Column(CHAR(1), server_default=text("'N'"))
    control_flota = Column(CHAR(1))
    tipo_cliente = Column(ForeignKey('empresas_tipos_cliente.id'))
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
    motivo_baja = Column(ForeignKey('empresas_motivo_baja.id'))
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
    dimension_proveedor = Column(ForeignKey('cf_dimensiones.id'))
    permitir_spot = Column(NUMBER(1, 0, False), nullable=False, server_default=text("0 "))
    tipo_cif = Column(VARCHAR(2))
    tiene_renting = Column(NUMBER(1, 0, False))
    cfdi_uso = Column(VARCHAR(4))
    cfdi_aduana = Column(VARCHAR(4))
    dig_codigo_docum_cliente = Column(VARCHAR(20))
    emp_basica = Column(VARCHAR(1))
    ref_externa_1 = Column(VARCHAR(20))
    ref_externa_2 = Column(VARCHAR(20))
    id_empresa_ide = Column(NUMBER(asdecimal=False))
    ide_empresas_ide = Column(NUMBER(asdecimal=False))
    bloq_adm_prov = Column(ForeignKey('bloqueo_adm_prov_tipos.id'))
    bloq_adm_prov_motivo = Column(ForeignKey('bloqueo_adm_prov_motivos.id'))
    nalbaran_notas_pedido = Column(NVARCHAR(1), server_default=text("'N'"))

    bloqueo_adm_prov_tipo = relationship('BloqueoAdmProvTipo')
    bloqueo_adm_prov_motivo = relationship('BloqueoAdmProvMotivo')
    cf_dimensione = relationship('CfDimensione')
    parent = relationship('Empresa', remote_side=[id])
    empresas_estado = relationship('EmpresasEstado')
    tipos_pago_cobro = relationship('TiposPagoCobro', primaryjoin='Empresa.forma_cobro == TiposPagoCobro.id')
    tipos_pago_cobro1 = relationship('TiposPagoCobro', primaryjoin='Empresa.forma_pago == TiposPagoCobro.id')
    empresas_ide = relationship('EmpresasIde')
    moneda1 = relationship('Moneda')
    empresas_motivo_baja = relationship('EmpresasMotivoBaja')
    paise = relationship('Paise')
    empresas_sectore = relationship('EmpresasSectore')
    empresas_tipos_cliente = relationship('EmpresasTiposCliente')
    tipos_impuesto = relationship('TiposImpuesto')
    empresas_tipos_proveedor = relationship('EmpresasTiposProveedor')


class Pedido(Base):
    __tablename__ = 'pedidos'
    __table_args__ = (
        ForeignKeyConstraint(['ide_pedido_asociado', 'pedido_asociado'], ['pedidos.ide', 'pedidos.id']),
        Index('ind_pedidos_tarifa', 'tarifa', 'ide', 'id'),
        Index('ind_pedidos_pedcliente', 'pedido_cliente', 'ide', 'id'),
        Index('ind_pedidos_pedido_asociado', 'ide_pedido_asociado', 'pedido_asociado'),
        Index('ind_pedidos_usu', 'gestor', 'ide', 'id'),
        Index('ind_pedidos_ide_emp_empresa', 'ide', 'emp_empresa'),
        Index('ind_pedidos_cliente_gf', 'cliente', 'gf', 'ide', 'id'),
        Index('ind_pedidos_ide_exp_id', 'ide', 'exp_id'),
        Index('ind_pedidos_ide_pet_org_f_prev', 'ide', 'pet_org_fecha_prevista'),
        Index('ind_pedidos_refcliente', 'referencia_cliente', 'ide', 'id')
    )

    ide = Column(ForeignKey('cm_empresas.id'), primary_key=True, nullable=False, server_default=text("1 "))
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
    tarifa = Column(ForeignKey('tarifas_cliente.id'))
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
    tipo_urgencia = Column(ForeignKey('tipos_urgencia.id'))
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
    alerta = Column(VARCHAR(1000))
    estado_eta = Column(NUMBER(asdecimal=False))
    estado_gps = Column(NUMBER(asdecimal=False))
    dim_cliente_7 = Column(VARCHAR(30))
    dig_codigo_docum_cliente = Column(ForeignKey('dig_documentacion_cliente.id'))
    parquin_vigilado = Column(NUMBER(1, 0, False))

    dig_documentacion_cliente = relationship('DigDocumentacionCliente')
    cm_empresa = relationship('CmEmpresa')
    parent = relationship('Pedido', remote_side=[ide, id])
    tarifas_cliente = relationship('TarifasCliente')
    tipos_urgencia = relationship('TiposUrgencia')


class PedidosEtapasDetalle(Base):
    __tablename__ = 'pedidos_etapas_detalle'
    __table_args__ = (
        Index('ind_ped_et_det_prov_alb', 'proveedor', 'albaran'),
        Index('ind_ped_et_det_prov_alb_falb', 'proveedor', 'albaran', 'fecha_albaran')
    )

    ide = Column(NUMBER(3, 0, False), primary_key=True, nullable=False, server_default=text("1 "))
    pedido = Column(NUMBER(8, 0, False), primary_key=True, nullable=False)
    etapa = Column(NUMBER(8, 0, False), primary_key=True, nullable=False)
    albaran = Column(VARCHAR(100), primary_key=True, nullable=False)
    fecha_albaran = Column(DateTime)
    proveedor = Column(VARCHAR(100), index=True)
    nombre_proveedor = Column(VARCHAR(100))
    detalle_proveedor = Column(VARCHAR(100))
    cliente = Column(VARCHAR(100))
    nombre_cliente = Column(VARCHAR(100))
    detalle_cliente = Column(VARCHAR(400))
    elementos = Column(NUMBER(asdecimal=False))
    paquetes = Column(NUMBER(asdecimal=False))
    peso_neto = Column(NUMBER(asdecimal=False))
    peso_bruto = Column(NUMBER(asdecimal=False))
    volumen = Column(NUMBER(asdecimal=False))
    ref_cliente = Column(VARCHAR(50), index=True)
    fecha_ref_cliente = Column(DateTime)
    codigo_seguimiento1 = Column(VARCHAR(50))
    codigo_seguimiento2 = Column(VARCHAR(50))
    bastidor = Column(VARCHAR(30))
    modelo = Column(VARCHAR(50))
    matricula = Column(VARCHAR(20))
    unidades = Column(NUMBER(asdecimal=False))
    peso_agrupacion = Column(NUMBER(asdecimal=False))
    importe_agrupacion = Column(NUMBER(asdecimal=False))
    pais_proveedor = Column(VARCHAR(2))
    pais_cliente = Column(VARCHAR(2))
    planta_carga = Column(VARCHAR(20))
    puerta_carga = Column(VARCHAR(20))
    planta_descarga = Column(VARCHAR(20))
    puerta_descarga = Column(VARCHAR(20))
    importe_gasoil = Column(NUMBER(asdecimal=False))
    importe_agrupacion_sistema = Column(NUMBER(asdecimal=False))
    importe_detalle_sistema = Column(NUMBER(asdecimal=False))
    fuente_detalle = Column(VARCHAR(100))
    id_marca = Column(ForeignKey('vehiculos_marcas.id'))
    marca = Column(VARCHAR(50))
    id_tipo_vehiculo = Column(ForeignKey('vehiculos_tipos.id'))
    cod_tipo_vehiculo = Column(VARCHAR(20))
    tipo_vehiculo = Column(VARCHAR(50))
    id_modelo = Column(ForeignKey('vehiculos_modelos.id'))
    tarifa = Column(ForeignKey('tarifas_cliente.id'))
    importe_proveedor = Column(NUMBER(asdecimal=False))
    tarifa_proveedor = Column(NUMBER(asdecimal=False))
    comision = Column(VARCHAR(20))
    urgente = Column(NUMBER(1, 0, False))
    confrontado = Column(NUMBER(1, 0, False))
    importe1 = Column(NUMBER(12, 4, True))
    importe2 = Column(NUMBER(12, 4, True))
    importe3 = Column(NUMBER(12, 4, True))
    importe4 = Column(NUMBER(12, 4, True))
    importe5 = Column(NUMBER(12, 4, True))
    referencia1 = Column(VARCHAR(50))
    referencia2 = Column(VARCHAR(50))
    referencia3 = Column(VARCHAR(50))
    referencia4 = Column(VARCHAR(50))
    referencia5 = Column(VARCHAR(50))

    vehiculos_marca = relationship('VehiculosMarca')
    vehiculos_modelo = relationship('VehiculosModelo')
    vehiculos_tipo = relationship('VehiculosTipo')
    tarifas_cliente = relationship('TarifasCliente')


class TarifasClienteConcepto(Base):
    __tablename__ = 'tarifas_cliente_conceptos'

    tarifa = Column(ForeignKey('tarifas_cliente.id'), primary_key=True, nullable=False)
    concepto = Column(ForeignKey('tipos_conceptos_tarifas.id'), primary_key=True, nullable=False)
    importe = Column(NUMBER(asdecimal=False))
    moneda = Column(ForeignKey('monedas.id'), server_default=text("'EUR'"))
    fecha_modificacion = Column(DateTime, server_default=text("sysdate"))
    usu_modificacion = Column(VARCHAR(50))
    observaciones = Column(VARCHAR(200))

    tipos_conceptos_tarifa = relationship('TiposConceptosTarifa')
    moneda1 = relationship('Moneda')
    tarifas_cliente = relationship('TarifasCliente')


class EmpresasGruposFacturacion(Base):
    __tablename__ = 'empresas_grupos_facturacion'

    idc = Column(VARCHAR(10), primary_key=True, nullable=False)
    gf = Column(NUMBER(2, 0, False), primary_key=True, nullable=False)
    descripcion = Column(VARCHAR(100), nullable=False)
    estado = Column(CHAR(1), server_default=text("null"))
    iva = Column(NUMBER(asdecimal=False), nullable=False)
    moneda = Column(ForeignKey('monedas.id'))
    idioma = Column(VARCHAR(2))
    concepto = Column(VARCHAR(200))
    direccion_envio = Column(ForeignKey('direcciones.id'))
    direccion_facturacion = Column(ForeignKey('direcciones.id'))
    albaran_en_factura = Column(CHAR(1), server_default=text("'N'"))
    albaran_obligatorio = Column(CHAR(1), server_default=text("'N'"))
    albaran_observaciones = Column(VARCHAR(200))
    pedido_en_factura = Column(CHAR(1), server_default=text("'N'"))
    pedido_obligatorio = Column(CHAR(1), server_default=text("'N'"))
    pedido_observaciones = Column(VARCHAR(200))
    ref_cliente_en_factura = Column(CHAR(1), server_default=text("'N'"))
    ref_cliente_obligatorio = Column(CHAR(1), server_default=text("'N'"))
    ref_cliente_observaciones = Column(VARCHAR(200))
    ticket_en_factura = Column(CHAR(1), server_default=text("'N'"))
    ticket_obligatorio = Column(CHAR(1), server_default=text("'N'"))
    ticket_observaciones = Column(VARCHAR(200))
    facturador = Column(VARCHAR(15))
    observaciones = Column(VARCHAR(200))
    fecha_creacion = Column(DateTime, server_default=text("SYSDATE"))
    usu_creacion = Column(VARCHAR(50))
    vencimiento = Column(NUMBER(asdecimal=False))
    pedido_valor = Column(VARCHAR(50))
    forma_cobro = Column(NUMBER(3, 0, False))
    vencimiento_cobro = Column(NUMBER(3, 0, False))
    tipo_impuesto = Column(NUMBER(1, 0, False))
    dias_cobro = Column(VARCHAR(20))
    descuento = Column(NUMBER(asdecimal=False))
    bloqueo_tarifa = Column(CHAR(1), server_default=text("'N'"))
    gestor_cobro = Column(VARCHAR(10))
    terminos_cobro = Column(NUMBER(asdecimal=False))
    gr_registro_iva_neg_cli = Column(NUMBER(2, 0, False))
    pais = Column(VARCHAR(2))
    bloqueo_gf = Column(CHAR(1), server_default=text("'N'"))
    ide = Column(NUMBER(3, 0, False), primary_key=True, nullable=False, server_default=text("1"))
    gr_registro_iva_prod = Column(NUMBER(asdecimal=False))
    empresa = Column(NUMBER(6, 0, False), nullable=False)
    retencion = Column(NUMBER(asdecimal=False))
    notas_carga = Column(VARCHAR(1000))
    fecha_alta = Column(DateTime)
    fecha_baja = Column(DateTime)
    motivo_baja = Column(NUMBER(asdecimal=False))
    usu_modificacion = Column(VARCHAR(50))
    fecha_modificacion = Column(DateTime)
    gf_principal = Column(CHAR(1))
    dig_codigo_docum_cliente = Column(ForeignKey('dig_documentacion_cliente.id'))

    dig_documentacion_cliente = relationship('DigDocumentacionCliente')
    direccione = relationship('Direccione', primaryjoin='EmpresasGruposFacturacion.direccion_envio == Direccione.id')
    direccione1 = relationship('Direccione', primaryjoin='EmpresasGruposFacturacion.direccion_facturacion == Direccione.id')
    moneda1 = relationship('Moneda')


class PedidosEtapa(Base):
    __tablename__ = 'pedidos_etapas'
    __table_args__ = (
        CheckConstraint('ETAPA BETWEEN 1 AND 99'),
        Index('ind_pedidos_etapa_dir', 'direccion', 'ide', 'pedido', 'etapa'),
        Index('ind_ped_etap_fecha', 'ide', 'pedido', 'etapa', 'fecha'),
        Index('ide_ped_etapas_fecreal', 'ide', 'pedido', 'etapa', 'fecha_real', 'fecha')
    )

    ide = Column(NUMBER(3, 0, False), primary_key=True, nullable=False, server_default=text("1 "))
    pedido = Column(NUMBER(8, 0, False), primary_key=True, nullable=False)
    etapa = Column(NUMBER(3, 0, False), primary_key=True, nullable=False)
    tipo = Column(CHAR(1))
    direccion = Column(ForeignKey('direcciones.id'))
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


class TarifasClienteEtapa(Base):
    __tablename__ = 'tarifas_cliente_etapas'
    __table_args__ = (
        CheckConstraint("tipo in ('R','E','M','T','P')"),
    )

    etapa = Column(NUMBER(3, 0, False), primary_key=True, nullable=False)
    tipo = Column(CHAR(1))
    direccion = Column(ForeignKey('direcciones.id'), index=True)
    tarifa = Column(ForeignKey('tarifas_cliente.id'), primary_key=True, nullable=False, index=True)
    provincia = Column(NUMBER(asdecimal=False))
    poblacion = Column(NUMBER(asdecimal=False))
    pais = Column(CHAR(2))

    direccione = relationship('Direccione')
    tarifas_cliente = relationship('TarifasCliente')
