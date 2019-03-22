# coding: utf-8
from sqlalchemy import CHAR, Column, DateTime, ForeignKey, ForeignKeyConstraint, Index, Integer, TIMESTAMP, Table, Text, VARCHAR, text
from sqlalchemy.dialects.oracle.base import NUMBER, RAW
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


t_actores_sds_kk = Table(
    'actores_sds_kk', metadata,
    Column('vnd_id', NUMBER(asdecimal=False), nullable=False),
    Column('vnd_id_vw', NUMBER(asdecimal=False), nullable=False),
    Column('vnd_code', VARCHAR(11)),
    Column('vnd_plant', VARCHAR(3)),
    Column('vnd_duns', VARCHAR(11)),
    Column('vnd_name', VARCHAR(40)),
    Column('vnd_type', NUMBER(asdecimal=False)),
    Column('vnd_client_group', NUMBER(asdecimal=False)),
    Column('vnd_country', VARCHAR(2)),
    Column('vnd_cp', VARCHAR(10)),
    Column('vnd_place', VARCHAR(40)),
    Column('vnd_district', VARCHAR(40)),
    Column('vnd_client_plant_number', VARCHAR(3)),
    Column('vnd_zwv_code', NUMBER(asdecimal=False)),
    Column('vnd_valid_from', DateTime),
    Column('vnd_valid_until', DateTime),
    Column('vnd_in_use', NUMBER(asdecimal=False)),
    Column('vnd_client_group_name', VARCHAR(10)),
    Column('vnd_source', CHAR(1)),
    Column('vnd_adress_id', NUMBER(asdecimal=False)),
    schema='pre_pluscore'
)


t_actors_sn_kk = Table(
    'actors_sn_kk', metadata,
    Column('cliente', VARCHAR(20)),
    Column('nombre', VARCHAR(50)),
    Column('poblacion', VARCHAR(50)),
    Column('cp', VARCHAR(20)),
    Column('calle', VARCHAR(60)),
    Column('pais', VARCHAR(3)),
    Column('cp_corto', VARCHAR(3)),
    Column('provincia', VARCHAR(50)),
    Column('features', NUMBER(1, 0, False)),
    schema='pre_pluscore'
)


class Adrtype(Base):
    __tablename__ = 'adrtypes'
    __table_args__ = {'schema': 'pre_pluscore'}

    id = Column(NUMBER(10, 0, False), primary_key=True)
    name = Column(VARCHAR(100), nullable=False)
    description = Column(VARCHAR(100))


class Calendar(Base):
    __tablename__ = 'calendars'
    __table_args__ = {'schema': 'pre_pluscore'}

    id = Column(NUMBER(10, 0, False), primary_key=True)
    name = Column(VARCHAR(200), nullable=False)
    description = Column(VARCHAR(1000))


class Country(Base):
    __tablename__ = 'countries'
    __table_args__ = {'schema': 'pre_pluscore'}

    id = Column(NUMBER(10, 0, False), primary_key=True)
    isocode = Column(VARCHAR(50), unique=True)
    name = Column(VARCHAR(200))


t_del_kk_plantas = Table(
    'del_kk_plantas', metadata,
    Column('id', VARCHAR(3)),
    Column('nombre', VARCHAR(100)),
    schema='pre_pluscore'
)


t_del_kk_puertas = Table(
    'del_kk_puertas', metadata,
    Column('layoutid', NUMBER(10, 0, False)),
    Column('zonaid', NUMBER(10, 0, False)),
    Column('zona', VARCHAR(10)),
    Column('almacenid', NUMBER(10, 0, False)),
    schema='pre_pluscore'
)


t_del_kk_zonas = Table(
    'del_kk_zonas', metadata,
    Column('zonaori', VARCHAR(30)),
    Column('zonades', VARCHAR(10)),
    Column('dia', VARCHAR(1)),
    Column('calendario', VARCHAR(50)),
    Column('directo', VARCHAR(2)),
    Column('cc', Integer),
    Column('recogida', VARCHAR(1)),
    Column('recepcion', VARCHAR(1)),
    Column('expedicion', VARCHAR(1)),
    schema='pre_pluscore'
)


t_devicerelationship = Table(
    'devicerelationship', metadata,
    Column('id', Integer),
    Column('deviceidorigin', Integer),
    Column('deviceiddestination', Integer),
    schema='pre_pluscore'
)


t_devices = Table(
    'devices', metadata,
    Column('id', Integer),
    Column('name', VARCHAR(50)),
    Column('type', Integer),
    Column('model', VARCHAR(50)),
    Column('ip', VARCHAR(20)),
    Column('port', VARCHAR(10)),
    Column('alias', VARCHAR(20)),
    Column('server_ip', VARCHAR(20)),
    Column('warehouseid', NUMBER(10, 0, False), nullable=False),
    Column('device_id', VARCHAR(100)),
    Column('device_name', VARCHAR(199)),
    Column('device_token', VARCHAR(100)),
    Column('device_userid', Integer),
    Column('device_siteid', Integer),
    Column('device_challenge', VARCHAR(50)),
    schema='pre_pluscore'
)


t_dtoallcontainer = Table(
    'dtoallcontainer', metadata,
    Column('Site', NUMBER(10, 0, False)),
    Column('Id', VARCHAR(73)),
    Column('ContainerId', RAW),
    Column('Name', VARCHAR(50)),
    Column('Volume', NUMBER(asdecimal=False)),
    Column('VolumeFolded', NUMBER(asdecimal=False)),
    Column('QuantityPackages', NUMBER(asdecimal=False)),
    schema='pre_pluscore'
)


t_dtoalldeliverynotepackages = Table(
    'dtoalldeliverynotepackages', metadata,
    Column('Site', NUMBER(10, 0, False)),
    Column('SiteName', VARCHAR(401)),
    Column('Id', VARCHAR(122)),
    Column('IdL', VARCHAR(81)),
    Column('idDeliveryNote', NUMBER(10, 0, False)),
    Column('StatusDeliveryNote', NUMBER(10, 0, False)),
    Column('Manual', NUMBER(1, 0, False)),
    Column('AddrOrigName', VARCHAR(200)),
    Column('AddrOrigCity', VARCHAR(200)),
    Column('AddrOrigPostCode', VARCHAR(50)),
    Column('AddrDestName', VARCHAR(200)),
    Column('AddrDestPostCode', VARCHAR(50)),
    Column('AddrDestCountryName', VARCHAR(200)),
    Column('AddrDestCity', VARCHAR(200)),
    Column('idDeliveryNotePackage', NUMBER(10, 0, False)),
    Column('StackingFactor', NUMBER(10, 0, False)),
    Column('idActorOrigin', NUMBER(10, 0, False)),
    Column('NameActorOrigin', VARCHAR(250)),
    Column('AliasActorOrigin', VARCHAR(50)),
    Column('LogisticZoneOrigin', VARCHAR(50)),
    Column('LogisticZoneOriginId', NUMBER(asdecimal=False)),
    Column('LayoutOrigin', VARCHAR(200)),
    Column('LayoutOriginId', NUMBER(10, 0, False)),
    Column('FareZoneOrigin', VARCHAR(50)),
    Column('WarehouseName', VARCHAR(200)),
    Column('DeliveryNoteDate', TIMESTAMP),
    Column('ReceptionDate', TIMESTAMP),
    Column('DeliveryReceptionDate', TIMESTAMP),
    Column('DeliveryNoteOrigin', VARCHAR(50)),
    Column('DeliveryNoteDateOrigin', TIMESTAMP),
    Column('DeliveryDate', TIMESTAMP),
    Column('idActorDestination', NUMBER(10, 0, False)),
    Column('NameActorDestination', VARCHAR(250)),
    Column('AliasActorDestination', VARCHAR(50)),
    Column('LogisticZoneDestination', VARCHAR(50)),
    Column('LogisticZoneDestinationId', NUMBER(10, 0, False)),
    Column('LayoutDestination', VARCHAR(200)),
    Column('LayoutDestinationId', NUMBER(10, 0, False)),
    Column('FareZoneDestination', VARCHAR(50)),
    Column('WrDestinationId', NUMBER(10, 0, False)),
    Column('WrDestinationName', VARCHAR(200)),
    Column('LoadListId', NUMBER(10, 0, False)),
    Column('Weight', NUMBER(18, 10, True)),
    Column('Volume', NUMBER(asdecimal=False)),
    Column('Length', NUMBER(18, 10, True)),
    Column('Height', NUMBER(18, 10, True)),
    Column('Width', NUMBER(18, 10, True)),
    Column('Quantity', NUMBER(10, 0, False)),
    Column('Features', NUMBER(asdecimal=False)),
    Column('Ordered', NUMBER(10, 0, False)),
    Column('OverTruck', NUMBER(1, 0, False)),
    Column('WareHouseGroup', VARCHAR(50)),
    Column('GroupNumber', NUMBER(10, 0, False)),
    Column('Comments', VARCHAR(50)),
    Column('adr', NUMBER(10, 0, False)),
    Column('Sofa', VARCHAR(10)),
    Column('Urgency', NUMBER(1, 0, False)),
    Column('ManufactureType', NUMBER(10, 0, False)),
    Column('BorderCustom', NUMBER(1, 0, False)),
    Column('MainPartCode', VARCHAR(200)),
    Column('PartId', NUMBER(10, 0, False)),
    Column('MainPartQuantity', NUMBER(10, 0, False)),
    Column('NumPackages', NUMBER(asdecimal=False)),
    Column('MainZoneOrigin', VARCHAR(50)),
    Column('MainZoneDestination', VARCHAR(50)),
    Column('ExpeditionDetailsId', NUMBER(10, 0, False)),
    Column('ExpeditionId', NUMBER(10, 0, False)),
    Column('ExpeditionDetailStatus', NUMBER(10, 0, False)),
    Column('ExpeditionDetailBordero', VARCHAR(50)),
    Column('ExpeditionDetailCMR', VARCHAR(10)),
    Column('ContainerName', VARCHAR(50)),
    Column('ContainerMainPart', VARCHAR(200)),
    Column('ContainerMainPartQuantity', NUMBER(10, 0, False)),
    Column('StockLocation', VARCHAR(200)),
    Column('Amount', NUMBER(18, 2, True)),
    Column('ExpeditionDate', TIMESTAMP),
    Column('ExpeditionTruck', VARCHAR(50)),
    Column('ExpeditionTrailer', VARCHAR(50)),
    Column('ExpeditionStatus', NUMBER(10, 0, False)),
    Column('ExpeditionComments', Text),
    Column('PickUpAdviceId', NUMBER(10, 0, False)),
    Column('PickUpAdvicePackageId', NUMBER(10, 0, False)),
    schema='pre_pluscore'
)


t_dtoallexpeditiondetails = Table(
    'dtoallexpeditiondetails', metadata,
    Column('Site', NUMBER(10, 0, False)),
    Column('SiteName', VARCHAR(401)),
    Column('ExpeditionId', NUMBER(10, 0, False)),
    Column('ExpeditionDetailId', NUMBER(10, 0, False)),
    Column('TypeRow', CHAR(12)),
    Column('HeaderId', NUMBER(10, 0, False)),
    Column('HeaderStatus', NUMBER(10, 0, False)),
    Column('RowId', VARCHAR(81)),
    Column('RowStatus', NUMBER(asdecimal=False)),
    Column('StackingFactor', NUMBER(10, 0, False)),
    Column('idActorOrigin', NUMBER(10, 0, False)),
    Column('NameActorOrigin', VARCHAR(250)),
    Column('AliasActorOrigin', VARCHAR(50)),
    Column('AddrOrigName', VARCHAR(200)),
    Column('AddrOrigCity', VARCHAR(200)),
    Column('AddrOrigPostCode', VARCHAR(50)),
    Column('AddrDestName', VARCHAR(200)),
    Column('LogisticZoneOrigin', VARCHAR(50)),
    Column('LayoutOrigin', VARCHAR(200)),
    Column('FareZoneOrigin', VARCHAR(50)),
    Column('WarehouseName', VARCHAR(200)),
    Column('ReceptionDate', TIMESTAMP),
    Column('DeliveryNote', VARCHAR(50)),
    Column('DeliveryNoteDate', TIMESTAMP),
    Column('DeliveryDate', TIMESTAMP),
    Column('idActorDestination', NUMBER(10, 0, False)),
    Column('NameActorDestination', VARCHAR(250)),
    Column('AliasActorDestination', VARCHAR(50)),
    Column('LogisticZoneDestination', VARCHAR(50)),
    Column('LayoutDestination', VARCHAR(200)),
    Column('FareZoneDestination', VARCHAR(50)),
    Column('MainPartCode', VARCHAR(200)),
    Column('Weight', NUMBER(18, 10, True)),
    Column('Volume', NUMBER(asdecimal=False)),
    Column('Quantity', NUMBER(10, 0, False)),
    Column('Features', NUMBER(asdecimal=False)),
    Column('OverTruck', NUMBER(asdecimal=False)),
    Column('Amount', NUMBER(18, 2, True)),
    schema='pre_pluscore'
)


t_dtoallexpeditions = Table(
    'dtoallexpeditions', metadata,
    Column('Id', NUMBER(10, 0, False)),
    Column('Site', NUMBER(10, 0, False)),
    Column('Name', VARCHAR(50)),
    Column('Status', NUMBER(10, 0, False)),
    Column('LoadListDate', TIMESTAMP),
    Column('ExpeditionDate', TIMESTAMP),
    Column('Truck', VARCHAR(50)),
    Column('Trailer', VARCHAR(50)),
    Column('Weight', NUMBER(asdecimal=False)),
    Column('Volume', NUMBER(asdecimal=False)),
    Column('Quantity', NUMBER(asdecimal=False)),
    Column('FactWeight', NUMBER(asdecimal=False)),
    Column('StatusPackages', NUMBER(asdecimal=False)),
    Column('Incidence', NUMBER(asdecimal=False)),
    Column('TravelDate', TIMESTAMP),
    schema='pre_pluscore'
)


t_dtoallpickupadvicepackages = Table(
    'dtoallpickupadvicepackages', metadata,
    Column('Site', NUMBER(10, 0, False)),
    Column('SiteName', VARCHAR(401)),
    Column('Id', VARCHAR(81)),
    Column('IdL', NUMBER(10, 0, False)),
    Column('idPickupAdvice', NUMBER(10, 0, False)),
    Column('StatusPickupAdvice', NUMBER(10, 0, False)),
    Column('InputWorkDate', TIMESTAMP),
    Column('OutputWorkDate', TIMESTAMP),
    Column('AddrOrigName', VARCHAR(200)),
    Column('idPickupAdvicePackage', NUMBER(10, 0, False)),
    Column('StatusPickupAdvicePackage', NUMBER(10, 0, False)),
    Column('idActorOrigin', NUMBER(10, 0, False)),
    Column('NameActorOrigin', VARCHAR(250)),
    Column('AliasActorOrigin', VARCHAR(50)),
    Column('AddrOrigCity', VARCHAR(200)),
    Column('AddrOrigPostCode', VARCHAR(50)),
    Column('LogisticZoneOrigin', VARCHAR(50)),
    Column('LogisticZoneOriginId', NUMBER(asdecimal=False)),
    Column('LayoutOrigin', VARCHAR(200)),
    Column('LayoutOriginId', NUMBER(10, 0, False)),
    Column('FareZoneOrigin', VARCHAR(50)),
    Column('WarehouseName', VARCHAR(200)),
    Column('PickUpDate', TIMESTAMP),
    Column('ReceptionDate', TIMESTAMP),
    Column('DeliveryNote', VARCHAR(50)),
    Column('DeliveryNoteDate', TIMESTAMP),
    Column('DeliveryDate', TIMESTAMP),
    Column('DepartureDateCC', TIMESTAMP),
    Column('idActorDestination', NUMBER(10, 0, False)),
    Column('NameActorDestination', VARCHAR(250)),
    Column('AliasActorDestination', VARCHAR(50)),
    Column('AddrDestName', VARCHAR(200)),
    Column('LogisticZoneDestination', VARCHAR(50)),
    Column('LogisticZoneDestinationId', NUMBER(asdecimal=False)),
    Column('LayoutDestination', VARCHAR(200)),
    Column('LayoutDestinationId', NUMBER(10, 0, False)),
    Column('FareZoneDestination', VARCHAR(50)),
    Column('WrDestinationId', NUMBER(10, 0, False)),
    Column('WrDestinationName', VARCHAR(200)),
    Column('MainPartCode', VARCHAR(200)),
    Column('Weight', NUMBER(18, 10, True)),
    Column('Volume', NUMBER(18, 10, True)),
    Column('Height', NUMBER(18, 10, True)),
    Column('Width', NUMBER(18, 10, True)),
    Column('Length', NUMBER(18, 10, True)),
    Column('Quantity', NUMBER(10, 0, False)),
    Column('Features', NUMBER(10, 0, False)),
    Column('StackingFactor', NUMBER(10, 0, False)),
    Column('Ordered', NUMBER(10, 0, False)),
    Column('OrderComments', VARCHAR(200)),
    Column('Adr', NUMBER(10, 0, False)),
    Column('MainZoneOrigin', VARCHAR(50)),
    Column('MainZoneDestination', VARCHAR(50)),
    Column('LoadListPickupsId', NUMBER(10, 0, False)),
    Column('LoadListId', NUMBER(10, 0, False)),
    Column('LoadListDate', TIMESTAMP),
    Column('LoadListFeatures', NUMBER(10, 0, False)),
    Column('OverTruck', NUMBER(1, 0, False)),
    Column('LoadListTruck', VARCHAR(50)),
    Column('LoadListTrailer', VARCHAR(50)),
    Column('LoadListStatus', NUMBER(10, 0, False)),
    Column('LoadListComments', VARCHAR(200)),
    Column('TravelDateLL', TIMESTAMP),
    Column('LoadListName', VARCHAR(50)),
    Column('PlannerPickupsId', NUMBER(10, 0, False)),
    Column('PlannerId', NUMBER(10, 0, False)),
    Column('Amount', NUMBER(18, 2, True)),
    Column('DeliveryNoteId', NUMBER(10, 0, False)),
    Column('DeliveryNotePackageId', NUMBER(10, 0, False)),
    Column('ExpeditionDetailId', NUMBER(10, 0, False)),
    Column('ExpeditionId', NUMBER(10, 0, False)),
    Column('ExpeditionDetailStatus', NUMBER(10, 0, False)),
    Column('ExpeditionDetailCMR', VARCHAR(10)),
    Column('AxonId', NUMBER(10, 0, False)),
    Column('Carrier', VARCHAR(250)),
    Column('ConsignmentReferenceNumber', VARCHAR(100)),
    Column('WoIdPedido', NUMBER(10, 0, False)),
    schema='pre_pluscore'
)


t_dtoallpickupadvices = Table(
    'dtoallpickupadvices', metadata,
    Column('Id', VARCHAR(81)),
    Column('Site', NUMBER(10, 0, False)),
    Column('SiteName', VARCHAR(401)),
    Column('idPickupAdvice', NUMBER(10, 0, False)),
    Column('StatusPickupAdvice', NUMBER(10, 0, False)),
    Column('InputWorkDate', TIMESTAMP),
    Column('OutputWorkDate', TIMESTAMP),
    Column('AddrOrigName', VARCHAR(200)),
    Column('AddrOrigCity', VARCHAR(200)),
    Column('AddrOrigPostCode', VARCHAR(50)),
    Column('idActorOrigin', NUMBER(10, 0, False)),
    Column('NameActorOrigin', VARCHAR(250)),
    Column('AliasActorOrigin', VARCHAR(50)),
    Column('LogisticZoneOrigin', VARCHAR(50)),
    Column('LogisticZoneOriginId', NUMBER(asdecimal=False)),
    Column('LayoutOrigin', VARCHAR(200)),
    Column('LayoutOriginId', NUMBER(10, 0, False)),
    Column('FareZoneOrigin', VARCHAR(50)),
    Column('WarehouseName', VARCHAR(200)),
    Column('PickUpDate', TIMESTAMP),
    Column('ReceptionDate', TIMESTAMP),
    Column('Weight', NUMBER(asdecimal=False)),
    Column('Volume', NUMBER(asdecimal=False)),
    Column('Quantity', NUMBER(asdecimal=False)),
    schema='pre_pluscore'
)


t_dtoallpickupstockpackages = Table(
    'dtoallpickupstockpackages', metadata,
    Column('Id', VARCHAR(83)),
    Column('Site', NUMBER(10, 0, False)),
    Column('SiteName', VARCHAR(401)),
    Column('idHeader', NUMBER(10, 0, False)),
    Column('idDetail', NUMBER(10, 0, False)),
    Column('idType', NUMBER(asdecimal=False)),
    Column('Type', VARCHAR(6)),
    Column('Features', NUMBER(asdecimal=False)),
    Column('idActorOrigin', NUMBER(10, 0, False)),
    Column('NameActorOrigin', VARCHAR(250)),
    Column('AliasActorOrigin', VARCHAR(50)),
    Column('LogisticZoneOriginId', NUMBER(asdecimal=False)),
    Column('LogisticZoneOrigin', VARCHAR(50)),
    Column('idActorDestination', NUMBER(10, 0, False)),
    Column('NameActorDestination', VARCHAR(250)),
    Column('AliasActorDestination', VARCHAR(50)),
    Column('LogisticZoneDestinationId', NUMBER(asdecimal=False)),
    Column('LogisticZoneDestination', VARCHAR(50)),
    Column('ReceptionDate', TIMESTAMP),
    Column('DeliveryDate', TIMESTAMP),
    Column('LayoutDestinationId', NUMBER(10, 0, False)),
    Column('LayoutDestination', VARCHAR(200)),
    Column('DeliveryNote', VARCHAR(50)),
    Column('Part', VARCHAR(200)),
    Column('PackageName', VARCHAR(50)),
    Column('OverTruck', NUMBER(asdecimal=False)),
    Column('Weight', NUMBER(asdecimal=False)),
    Column('Volume', NUMBER(asdecimal=False)),
    Column('Quantity', NUMBER(10, 0, False)),
    Column('ExpeditionDetailId', NUMBER(10, 0, False)),
    Column('ExpeditionId', NUMBER(10, 0, False)),
    Column('PickUpAdviceId', NUMBER(asdecimal=False)),
    schema='pre_pluscore'
)


t_dtoallstocks = Table(
    'dtoallstocks', metadata,
    Column('id', VARCHAR(81)),
    Column('idstock', NUMBER(10, 0, False)),
    Column('dnpid', NUMBER(10, 0, False)),
    Column('layoutid', NUMBER(10, 0, False)),
    Column('containerid', RAW),
    Column('site', NUMBER(10, 0, False)),
    schema='pre_pluscore'
)


t_dtoallstockspackages = Table(
    'dtoallstockspackages', metadata,
    Column('Id', VARCHAR(122)),
    Column('Site', NUMBER(10, 0, False)),
    Column('SiteName', VARCHAR(401)),
    Column('StockId', NUMBER(10, 0, False)),
    Column('ContainerId', RAW),
    Column('ContainerPartId', NUMBER(10, 0, False)),
    Column('DeliveryNoteId', NUMBER(10, 0, False)),
    Column('DeliveryNotePackageId', NUMBER(10, 0, False)),
    Column('DeliveryNoteStatus', NUMBER(10, 0, False)),
    Column('PickUpAdviceId', NUMBER(10, 0, False)),
    Column('PickUpAdvicePackageId', NUMBER(10, 0, False)),
    Column('DeliveryNotePackageFeatures', NUMBER(asdecimal=False)),
    Column('ReceptionDate', TIMESTAMP),
    Column('DeliveryNote', VARCHAR(50)),
    Column('DeliveryNoteDate', TIMESTAMP),
    Column('DeliveryDate', TIMESTAMP),
    Column('DepartureDateCC', TIMESTAMP),
    Column('AdrTypeId', NUMBER(10, 0, False)),
    Column('idActorOrigin', NUMBER(10, 0, False)),
    Column('NameActorOrigin', VARCHAR(250)),
    Column('AliasActorOrigin', VARCHAR(50)),
    Column('LogisticZoneOriginId', NUMBER(asdecimal=False)),
    Column('LogisticZoneOrigin', VARCHAR(50)),
    Column('LayoutOriginId', NUMBER(10, 0, False)),
    Column('LayoutOrigin', VARCHAR(200)),
    Column('idActorDestination', NUMBER(10, 0, False)),
    Column('NameActorDestination', VARCHAR(250)),
    Column('AliasActorDestination', VARCHAR(50)),
    Column('LogisticZoneDestinationId', NUMBER(asdecimal=False)),
    Column('LogisticZoneDestination', VARCHAR(50)),
    Column('LayoutDestinationId', NUMBER(10, 0, False)),
    Column('LayoutDestination', VARCHAR(200)),
    Column('NaveDestination', VARCHAR(200)),
    Column('Receptor', VARCHAR(250)),
    Column('ContainerName', VARCHAR(50)),
    Column('LocationId', NUMBER(10, 0, False)),
    Column('Location', VARCHAR(200)),
    Column('LocationFeatures', NUMBER(10, 0, False)),
    Column('Part', VARCHAR(200)),
    Column('Quantity', NUMBER(10, 0, False)),
    Column('Features', NUMBER(10, 0, False)),
    Column('MainPart', NUMBER(1, 0, False)),
    Column('ContainerParentId', RAW),
    Column('Weight', NUMBER(asdecimal=False)),
    Column('Volume', NUMBER(asdecimal=False)),
    Column('FactWeight_Type', VARCHAR(1)),
    Column('ExpeditionId', NUMBER(10, 0, False)),
    Column('ExpeditionStatus', NUMBER(10, 0, False)),
    Column('ExpeditionDetailId', NUMBER(10, 0, False)),
    Column('ExpeditionDetailStatus', NUMBER(10, 0, False)),
    schema='pre_pluscore'
)


t_dtoalltravelincidences = Table(
    'dtoalltravelincidences', metadata,
    Column('typetravel', NUMBER(asdecimal=False)),
    Column('travelid', NUMBER(10, 0, False)),
    Column('incidence', VARCHAR(4000)),
    Column('siteid', NUMBER(10, 0, False)),
    schema='pre_pluscore'
)


t_dtopuapconfirmed = Table(
    'dtopuapconfirmed', metadata,
    Column('Site', NUMBER(10, 0, False)),
    Column('IdPuap', NUMBER(10, 0, False)),
    schema='pre_pluscore'
)


class Entity(Base):
    __tablename__ = 'entities'
    __table_args__ = {'schema': 'pre_pluscore'}

    id = Column(NUMBER(10, 0, False), primary_key=True)
    type = Column(VARCHAR(1000), nullable=False)


class ExpeditionPlannersLog(Base):
    __tablename__ = 'expedition_planners_log'
    __table_args__ = {'schema': 'pre_pluscore'}

    id = Column(NUMBER(10, 0, False), primary_key=True)
    userid = Column(NUMBER(10, 0, False), nullable=False)
    insertdate = Column(DateTime, nullable=False)
    expid = Column(NUMBER(10, 0, False), nullable=False)
    nameroute = Column(VARCHAR(100), nullable=False)
    factweight = Column(NUMBER(18, 2, True), nullable=False)
    weight = Column(NUMBER(18, 2, True), nullable=False)
    volume = Column(NUMBER(18, 2, True), nullable=False)
    deliverydate = Column(DateTime)
    departuredatecc = Column(DateTime)
    siteid = Column(NUMBER(10, 0, False), nullable=False)
    receptiondate = Column(DateTime)
    departuredate = Column(DateTime)
    traveldate = Column(DateTime)


class ExpeditionPlannersNote(Base):
    __tablename__ = 'expedition_planners_notes'
    __table_args__ = {'schema': 'pre_pluscore'}

    logistic_zone_name = Column(VARCHAR(50), primary_key=True, nullable=False)
    reception_date = Column(DateTime, primary_key=True, nullable=False)
    delivery_date = Column(DateTime, primary_key=True, nullable=False)
    country = Column(VARCHAR(2), primary_key=True, nullable=False)
    notes = Column(VARCHAR(500), nullable=False)


t_expeditiondetails_log = Table(
    'expeditiondetails_log', metadata,
    Column('id', NUMBER(10, 0, False)),
    Column('expid', NUMBER(10, 0, False)),
    Column('expdetailsid', NUMBER(10, 0, False)),
    Column('typetrg', VARCHAR(3)),
    Column('siteid', NUMBER(10, 0, False)),
    Column('puapid', NUMBER(10, 0, False)),
    Column('dnpid', NUMBER(10, 0, False)),
    Column('containerid', RAW),
    Column('statusold', NUMBER(10, 0, False)),
    Column('statusnew', NUMBER(10, 0, False)),
    Column('processdate', DateTime),
    Column('userid', NUMBER(10, 0, False)),
    schema='pre_pluscore'
)


class Expedition(Base):
    __tablename__ = 'expeditions'
    __table_args__ = {'schema': 'pre_pluscore'}

    id = Column(NUMBER(10, 0, False), primary_key=True)
    name = Column(VARCHAR(50))
    truck = Column(VARCHAR(50))
    trailer = Column(VARCHAR(50))
    DATE = Column(TIMESTAMP)
    loadlistdate = Column(TIMESTAMP)
    status = Column(NUMBER(10, 0, False), nullable=False, server_default=text("(0) "))
    actoridcarrier = Column(NUMBER(10, 0, False))
    features = Column(NUMBER(10, 0, False))
    comments = Column(Text)
    trucktype = Column(NUMBER(10, 0, False))
    trailertype = Column(NUMBER(10, 0, False))
    traveldate = Column(TIMESTAMP)
    expeditiondate = Column(TIMESTAMP)
    destionation = Column(VARCHAR(250))
    partnerexpedition = Column(ForeignKey('pre_pluscore.expeditions.id'))
    expeditiontype = Column(NUMBER(10, 0, False))
    ttupdated = Column(NUMBER(1, 0, False), server_default=text("(0)"))
    reportsent = Column(NUMBER(10, 0, False))
    woid = Column(NUMBER(10, 0, False))
    siteid = Column(NUMBER(10, 0, False))
    commentsplanning = Column(Text)
    woidpedido = Column(NUMBER(10, 0, False))

    parent = relationship('Expedition', remote_side=[id])


class Expeditiontransmission(Base):
    __tablename__ = 'expeditiontransmissions'
    __table_args__ = {'schema': 'pre_pluscore'}

    id = Column(NUMBER(10, 0, False), primary_key=True)
    expeditiondetailid = Column(NUMBER(10, 0, False))
    borderdate = Column(DateTime)


class Fare(Base):
    __tablename__ = 'fare'
    __table_args__ = {'schema': 'pre_pluscore'}

    id = Column(NUMBER(10, 0, False), primary_key=True)
    name = Column(VARCHAR(50), nullable=False)
    description = Column(VARCHAR(200), nullable=False)
    classname = Column(VARCHAR(200), nullable=False)


class Farezone(Base):
    __tablename__ = 'farezones'
    __table_args__ = {'schema': 'pre_pluscore'}

    id = Column(NUMBER(10, 0, False), primary_key=True)
    name = Column(VARCHAR(50), nullable=False)
    description = Column(VARCHAR(200))
    isactive = Column(NUMBER(1, 0, False), nullable=False)


class Field(Base):
    __tablename__ = 'fields'
    __table_args__ = {'schema': 'pre_pluscore'}

    id = Column(NUMBER(10, 0, False), primary_key=True)
    name = Column(VARCHAR(50))
    description = Column(VARCHAR(250))
    isactive = Column(NUMBER(1, 0, False), nullable=False)


t_kk_duns = Table(
    'kk_duns', metadata,
    Column('duns', VARCHAR(20)),
    Column('prov', VARCHAR(100)),
    Column('krias', VARCHAR(10)),
    schema='pre_pluscore'
)


t_layout_kk = Table(
    'layout_kk', metadata,
    Column('id', NUMBER(asdecimal=False)),
    Column('nombre', VARCHAR(50)),
    schema='pre_pluscore'
)


t_layouts_sds_bk = Table(
    'layouts_sds_bk', metadata,
    Column('id', NUMBER(10, 0, False), nullable=False),
    Column('name', VARCHAR(200), nullable=False),
    Column('isactive', NUMBER(1, 0, False)),
    Column('height', NUMBER(18, 2, True)),
    Column('width', NUMBER(18, 2, True)),
    Column('depth', NUMBER(18, 2, True)),
    Column('featuresid', NUMBER(10, 0, False), nullable=False),
    Column('warehouseid', NUMBER(10, 0, False), nullable=False),
    Column('farezoneid', NUMBER(10, 0, False)),
    Column('parentid', NUMBER(10, 0, False)),
    Column('operationtypeid', NUMBER(10, 0, False)),
    schema='pre_pluscore'
)


class Loadlist(Base):
    __tablename__ = 'loadlists'
    __table_args__ = {'schema': 'pre_pluscore'}

    id = Column(NUMBER(10, 0, False), primary_key=True)
    name = Column(VARCHAR(50))
    truck = Column(VARCHAR(50))
    trailer = Column(VARCHAR(50))
    DATE = Column(TIMESTAMP)
    loadlistdate = Column(TIMESTAMP)
    status = Column(NUMBER(10, 0, False))
    actoridcarrier = Column(NUMBER(10, 0, False))
    features = Column(NUMBER(10, 0, False), nullable=False, server_default=text("0 "))
    comments = Column(VARCHAR(200))
    trucktype = Column(NUMBER(10, 0, False))
    trailertype = Column(NUMBER(10, 0, False))
    traveldate = Column(TIMESTAMP)
    ttupdated = Column(NUMBER(1, 0, False), nullable=False, server_default=text("0 "))
    partnerloadlist = Column(NUMBER(10, 0, False))
    axonid = Column(NUMBER(10, 0, False))
    woidpedido = Column(NUMBER(10, 0, False))
    commentsplanning = Column(Text)


class Logisticzone(Base):
    __tablename__ = 'logisticzones'
    __table_args__ = {'schema': 'pre_pluscore'}

    id = Column(NUMBER(10, 0, False), primary_key=True)
    name = Column(VARCHAR(50), unique=True)
    description = Column(VARCHAR(200))
    international = Column(NUMBER(1, 0, False), nullable=False, server_default=text("0 "))


t_man_fare = Table(
    'man_fare', metadata,
    Column('id', NUMBER(10, 0, False), nullable=False),
    Column('faretype', NUMBER(1, 0, False), nullable=False),
    Column('km_from', NUMBER(5, 0, False), nullable=False),
    Column('km_to', NUMBER(5, 0, False), nullable=False),
    Column('kg_from', NUMBER(5, 0, False), nullable=False),
    Column('kg_to', NUMBER(5, 0, False), nullable=False),
    Column('unit', NUMBER(1, 0, False), nullable=False),
    Column('quantity_unit', NUMBER(3, 0, False), nullable=False),
    Column('valid_from', TIMESTAMP, nullable=False),
    Column('valid_to', TIMESTAMP, nullable=False),
    Column('rate', NUMBER(12, 6, True), nullable=False),
    schema='pre_pluscore'
)


t_man_fare_diesel = Table(
    'man_fare_diesel', metadata,
    Column('id', NUMBER(10, 0, False), nullable=False),
    Column('faretype', NUMBER(1, 0, False), nullable=False),
    Column('amount_from', NUMBER(6, 4, True)),
    Column('amount_to', NUMBER(6, 4, True)),
    Column('fare_pct', NUMBER(5, 2, True)),
    Column('amount', NUMBER(7, 5, True)),
    Column('fare_date', TIMESTAMP),
    schema='pre_pluscore'
)


class Membership(Base):
    __tablename__ = 'memberships'
    __table_args__ = {'schema': 'pre_pluscore'}

    id = Column(NUMBER(10, 0, False), primary_key=True)
    password = Column(VARCHAR(50), nullable=False)
    passwordsalt = Column(VARCHAR(50))
    passwordformat = Column(NUMBER(10, 0, False))
    passwordquestion = Column(VARCHAR(200))
    passwordanswer = Column(VARCHAR(50))
    isapproved = Column(NUMBER(1, 0, False), nullable=False)
    islockedout = Column(NUMBER(1, 0, False), nullable=False)
    failedpasswordattemptcount = Column(NUMBER(10, 0, False))
    failedpasswordattemptstart = Column(TIMESTAMP)
    failedpasswordanswercount = Column(NUMBER(10, 0, False))
    failedpasswordanswerstart = Column(TIMESTAMP)
    isroot = Column(NUMBER(1, 0, False), nullable=False)


class Partfamily(Base):
    __tablename__ = 'partfamilies'
    __table_args__ = {'schema': 'pre_pluscore'}

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    code = Column(VARCHAR(50), unique=True)
    description = Column(VARCHAR(100))
    isfifo = Column(NUMBER(1, 0, False), nullable=False, server_default=text("0 "))
    productivetime = Column(NUMBER(18, 2, True))


class Permission(Base):
    __tablename__ = 'permissions'
    __table_args__ = {'schema': 'pre_pluscore'}

    id = Column(NUMBER(10, 0, False), primary_key=True)
    name = Column(VARCHAR(200), nullable=False)
    description = Column(VARCHAR(1000), nullable=False)
    isactive = Column(NUMBER(1, 0, False), nullable=False)
    parentid = Column(ForeignKey('pre_pluscore.permissions.id'))
    area = Column(NUMBER(1, 0, False))
    issiterequired = Column(NUMBER(1, 0, False), server_default=text("0"))

    parent = relationship('Permission', remote_side=[id])
    useraccess = relationship('Useracces', secondary='pre_pluscore.useraccess_permissions')


class Planner(Base):
    __tablename__ = 'planners'
    __table_args__ = {'schema': 'pre_pluscore'}

    id = Column(NUMBER(10, 0, False), primary_key=True)
    name = Column(VARCHAR(50))
    truck = Column(VARCHAR(50))
    trailer = Column(VARCHAR(50))
    DATE = Column(TIMESTAMP, nullable=False)
    plannerdate = Column(TIMESTAMP)
    status = Column(NUMBER(10, 0, False))
    actoridcarrier = Column(NUMBER(10, 0, False))
    features = Column(NUMBER(10, 0, False))
    comments = Column(VARCHAR(200))
    trailertype = Column(NUMBER(10, 0, False))
    trucktype = Column(NUMBER(10, 0, False))
    traveldate = Column(TIMESTAMP)


class Project(Base):
    __tablename__ = 'projects'
    __table_args__ = {'schema': 'pre_pluscore'}

    id = Column(NUMBER(10, 0, False), primary_key=True)
    name = Column(VARCHAR(200), nullable=False)
    description = Column(VARCHAR(100))
    isactive = Column(NUMBER(1, 0, False), nullable=False)

    vehicletypes = relationship('Vehicletype', secondary='pre_pluscore.projects_vehicletypes')


class Region(Base):
    __tablename__ = 'regions'
    __table_args__ = {'schema': 'pre_pluscore'}

    id = Column(NUMBER(10, 0, False), primary_key=True)
    postalcode = Column(VARCHAR(50))
    name = Column(VARCHAR(50))


t_reporting_distances = Table(
    'reporting_distances', metadata,
    Column('id', NUMBER(10, 0, False)),
    Column('actoridorigin', NUMBER(10, 0, False)),
    Column('actoriddestination', NUMBER(10, 0, False)),
    Column('kilometers', NUMBER(10, 0, False)),
    schema='pre_pluscore'
)


t_reporting_fares = Table(
    'reporting_fares', metadata,
    Column('id', NUMBER(10, 0, False)),
    Column('km_from', NUMBER(5, 0, False)),
    Column('km_to', NUMBER(5, 0, False)),
    Column('kg_from', NUMBER(10, 0, False)),
    Column('kg_to', NUMBER(10, 0, False)),
    Column('importe', NUMBER(10, 0, False)),
    Column('userid', NUMBER(10, 0, False)),
    Column('updatedate', TIMESTAMP),
    schema='pre_pluscore'
)


class Rule(Base):
    __tablename__ = 'rules'
    __table_args__ = {'schema': 'pre_pluscore'}

    id = Column(NUMBER(10, 0, False), primary_key=True)
    name = Column(VARCHAR(200), nullable=False)
    description = Column(VARCHAR(1000), nullable=False)


class Scheduled(Base):
    __tablename__ = 'scheduleds'
    __table_args__ = {'schema': 'pre_pluscore'}

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    name = Column(VARCHAR(250), nullable=False)
    description = Column(VARCHAR(500), nullable=False)
    is_active = Column(NUMBER(1, 0, False), nullable=False, server_default=text("0 "))
    interval_time = Column(Integer)
    interval_type = Column(Integer)
    last_execution = Column(DateTime)
    hours = Column(Integer, nullable=False, server_default=text("0 "))
    days = Column(Integer, nullable=False, server_default=text("0 "))
    force_execution = Column(NUMBER(1, 0, False), nullable=False, server_default=text("0 "))
    insert_date = Column(DateTime)
    update_date = Column(DateTime)


class SdsActore(Base):
    __tablename__ = 'sds_actores'
    __table_args__ = {'schema': 'pre_pluscore'}

    id_vw = Column(NUMBER(asdecimal=False), primary_key=True)
    codigo = Column(VARCHAR(11))
    planta = Column(VARCHAR(3))
    duns = Column(VARCHAR(11))
    nombre = Column(VARCHAR(80))
    tipo = Column(NUMBER(1, 0, False))
    grupo_cliente = Column(NUMBER(2, 0, False))
    pais = Column(VARCHAR(2))
    cp = Column(VARCHAR(10))
    localizacion = Column(VARCHAR(40))
    distrito = Column(VARCHAR(40))
    numero_planta_cliente = Column(VARCHAR(3))
    indicador_zwv = Column(NUMBER(1, 0, False))
    valido_desde = Column(DateTime)
    valido_hasta = Column(DateTime)
    operacion = Column(NUMBER(asdecimal=False))
    en_uso = Column(NUMBER(1, 0, False))
    grupo_cliente_nombre = Column(VARCHAR(10))


class SdsEmbalaje(Base):
    __tablename__ = 'sds_embalajes'
    __table_args__ = {'schema': 'pre_pluscore'}

    id_vw = Column(NUMBER(asdecimal=False), primary_key=True)
    codigo = Column(VARCHAR(10))
    descripcion = Column(VARCHAR(50))
    longitud = Column(NUMBER(asdecimal=False))
    ancho = Column(NUMBER(asdecimal=False))
    alto = Column(NUMBER(asdecimal=False))
    alto_vacio = Column(NUMBER(asdecimal=False))
    tara = Column(NUMBER(10, 3, True))


t_sds_fares = Table(
    'sds_fares', metadata,
    Column('zip', VARCHAR(10)),
    Column('zone', VARCHAR(10)),
    schema='pre_pluscore'
)


t_sds_puertas = Table(
    'sds_puertas', metadata,
    Column('codigo', VARCHAR(15)),
    Column('planta', VARCHAR(3)),
    Column('cp', VARCHAR(10)),
    Column('country', VARCHAR(2)),
    schema='pre_pluscore'
)


class ServicebusMessagesPending(Base):
    __tablename__ = 'servicebus_messages_pending'
    __table_args__ = {'schema': 'pre_pluscore'}

    id = Column(NUMBER(10, 0, False), primary_key=True)
    messageid = Column(RAW, nullable=False)
    messagetype = Column(NUMBER(10, 0, False), nullable=False)
    message = Column(Text, nullable=False)
    created = Column(DateTime, nullable=False)
    sent = Column(NUMBER(1, 0, False), nullable=False)
    processed = Column(DateTime)
    response = Column(Text)
    exception = Column(Text)
    exceptiontype = Column(NUMBER(10, 0, False))


class ServicebusMessagesProcessed(Base):
    __tablename__ = 'servicebus_messages_processed'
    __table_args__ = {'schema': 'pre_pluscore'}

    id = Column(NUMBER(10, 0, False), primary_key=True)
    messageid = Column(RAW, nullable=False)
    messagetype = Column(NUMBER(10, 0, False), nullable=False)
    message = Column(Text, nullable=False)
    created = Column(DateTime, nullable=False)
    sent = Column(NUMBER(1, 0, False), nullable=False)
    processed = Column(DateTime)
    response = Column(Text)
    exception = Column(Text)
    exceptiontype = Column(NUMBER(10, 0, False))


class Unit(Base):
    __tablename__ = 'units'
    __table_args__ = {'schema': 'pre_pluscore'}

    id = Column(NUMBER(10, 0, False), primary_key=True)
    name = Column(VARCHAR(100), nullable=False)
    acronym = Column(VARCHAR(100), nullable=False)
    concept = Column(NUMBER(1, 0, False), nullable=False)


t_v_vda_pegasus_error = Table(
    'v_vda_pegasus_error', metadata,
    Column('site', CHAR(1)),
    Column('file_date', DateTime),
    Column('txtdeses', VARCHAR(200)),
    Column('nom_proveedor', VARCHAR(250), nullable=False),
    Column('puerta', VARCHAR(45)),
    Column('cliente', VARCHAR(50)),
    Column('albaran_tr_error', VARCHAR(8)),
    Column('pieza_tr_error', VARCHAR(41)),
    Column('cod_proveedor', VARCHAR(50)),
    Column('valinf', VARCHAR(50)),
    Column('file_name', VARCHAR(200)),
    Column('nomvir', VARCHAR(500)),
    Column('feresi', DateTime),
    Column('tds_date', DateTime),
    Column('brd', VARCHAR(4)),
    schema='pre_pluscore'
)


class VdaPegasusFileError(Base):
    __tablename__ = 'vda_pegasus_file_errors'
    __table_args__ = {'schema': 'pre_pluscore'}

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    rvs = Column(VARCHAR(100))
    file_date = Column(DateTime)
    file_name = Column(VARCHAR(200))
    project_id = Column(NUMBER(asdecimal=False))
    site_id = Column(NUMBER(asdecimal=False))


class Vehicletype(Base):
    __tablename__ = 'vehicletypes'
    __table_args__ = {'schema': 'pre_pluscore'}

    id = Column(NUMBER(10, 0, False), primary_key=True)
    name = Column(VARCHAR(50))
    isactive = Column(NUMBER(1, 0, False))
    drag = Column(VARCHAR(1))
    autonomous = Column(VARCHAR(1))


class ViajesWoSinIdentificar(Base):
    __tablename__ = 'viajes_wo_sin_identificar'
    __table_args__ = {'schema': 'pre_pluscore'}

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    site_global = Column(NUMBER(asdecimal=False))
    ide = Column(NUMBER(3, 0, False))
    bordero = Column(VARCHAR(20))
    albaran = Column(VARCHAR(20))
    resultado = Column(VARCHAR(300))
    ultimo_procesado = Column(DateTime)
    pendiente_procesado = Column(NUMBER(1, 0, False))
    fecha_creacion = Column(DateTime)
    usuario_creacion = Column(VARCHAR(100))
    tractora = Column(VARCHAR(20))
    remolque = Column(VARCHAR(20))
    hojaderuta = Column(NUMBER(asdecimal=False))


class Conversion(Base):
    __tablename__ = 'conversions'
    __table_args__ = {'schema': 'pre_pluscore'}

    id = Column(NUMBER(10, 0, False), primary_key=True)
    unitidorigin = Column(ForeignKey('pre_pluscore.units.id'), nullable=False)
    unitiddestination = Column(ForeignKey('pre_pluscore.units.id'), nullable=False)
    change = Column(NUMBER(18, 10, True))

    unit = relationship('Unit', primaryjoin='Conversion.unitiddestination == Unit.id')
    unit1 = relationship('Unit', primaryjoin='Conversion.unitidorigin == Unit.id')


class Day(Base):
    __tablename__ = 'days'
    __table_args__ = (
        Index('days_uq', 'daydate', 'calendarid', unique=True),
        {'schema': 'pre_pluscore'}
    )

    id = Column(NUMBER(10, 0, False), primary_key=True)
    daydate = Column(TIMESTAMP, nullable=False)
    features = Column(NUMBER(10, 0, False), nullable=False)
    calendarid = Column(ForeignKey('pre_pluscore.calendars.id'), nullable=False)

    calendar = relationship('Calendar')


class Expeditiondetail(Base):
    __tablename__ = 'expeditiondetails'
    __table_args__ = (
        Index('ind_expeditiondetail_id_siteid', 'siteid', 'id'),
        {'schema': 'pre_pluscore'}
    )

    id = Column(NUMBER(10, 0, False), primary_key=True)
    expid = Column(ForeignKey('pre_pluscore.expeditions.id'), nullable=False, index=True)
    siteid = Column(NUMBER(10, 0, False), nullable=False, index=True)
    puapid = Column(NUMBER(10, 0, False))
    dnpid = Column(NUMBER(10, 0, False), index=True)
    containerid = Column(RAW, unique=True)
    transportorder = Column(VARCHAR(50))
    bordero = Column(VARCHAR(50))
    amount = Column(NUMBER(18, 2, True))
    status = Column(NUMBER(10, 0, False))
    transmitted = Column(NUMBER(1, 0, False), nullable=False, server_default=text("0 "))
    cmr = Column(VARCHAR(10))
    borderodate = Column(TIMESTAMP)
    transmissionfailed = Column(NUMBER(1, 0, False), nullable=False, server_default=text("0 "))
    processdate4913 = Column(DateTime)
    processdate4921 = Column(DateTime)
    userid = Column(NUMBER(10, 0, False))

    expedition = relationship('Expedition')


class Farezonepostcode(Base):
    __tablename__ = 'farezonepostcodes'
    __table_args__ = {'schema': 'pre_pluscore'}

    id = Column(NUMBER(10, 0, False), primary_key=True)
    farezoneid = Column(ForeignKey('pre_pluscore.farezones.id'), nullable=False)
    postcode = Column(VARCHAR(50), nullable=False)
    isactive = Column(NUMBER(1, 0, False), nullable=False)
    countryid = Column(ForeignKey('pre_pluscore.countries.id'), nullable=False)

    country = relationship('Country')
    farezone = relationship('Farezone')


class Fieldproject(Base):
    __tablename__ = 'fieldprojects'
    __table_args__ = {'schema': 'pre_pluscore'}

    id = Column(NUMBER(10, 0, False), primary_key=True)
    fieldid = Column(ForeignKey('pre_pluscore.fields.id'), nullable=False)
    projectid = Column(ForeignKey('pre_pluscore.projects.id'), nullable=False)
    isactive = Column(NUMBER(1, 0, False), nullable=False)

    field = relationship('Field')
    project = relationship('Project')


class Globalization(Base):
    __tablename__ = 'globalizations'
    __table_args__ = {'schema': 'pre_pluscore'}

    id = Column(NUMBER(10, 0, False), primary_key=True)
    name = Column(VARCHAR(200), nullable=False)
    locale = Column(VARCHAR(50), nullable=False)
    calendarid = Column(ForeignKey('pre_pluscore.calendars.id'))
    isactive = Column(NUMBER(1, 0, False), nullable=False)

    calendar = relationship('Calendar')


class Loadlistpickup(Base):
    __tablename__ = 'loadlistpickups'
    __table_args__ = (
        Index('loadlistpickups_uq', 'pickupadviceid', 'siteid', unique=True),
        {'schema': 'pre_pluscore'}
    )

    id = Column(NUMBER(10, 0, False), primary_key=True)
    loadlistid = Column(ForeignKey('pre_pluscore.loadlists.id'), nullable=False, index=True)
    pickupadviceid = Column(NUMBER(10, 0, False), nullable=False)
    amount = Column(NUMBER(18, 2, True), nullable=False)
    faregroup = Column(NUMBER(10, 0, False), nullable=False)
    siteid = Column(NUMBER(10, 0, False), nullable=False)
    overtruck = Column(NUMBER(1, 0, False), nullable=False, server_default=text("0 "))
    empty = Column(NUMBER(1, 0, False), nullable=False, server_default=text("0 "))

    loadlist = relationship('Loadlist')


t_man_fare_logisticzones = Table(
    'man_fare_logisticzones', metadata,
    Column('id', NUMBER(10, 0, False), nullable=False),
    Column('faretype', NUMBER(1, 0, False), nullable=False),
    Column('logisticzoneid', ForeignKey('pre_pluscore.logisticzones.id'), nullable=False),
    Column('fare_pct', NUMBER(5, 2, True), nullable=False),
    schema='pre_pluscore'
)


class Part(Base):
    __tablename__ = 'parts'
    __table_args__ = {'schema': 'pre_pluscore'}

    id = Column(NUMBER(10, 0, False), primary_key=True)
    code = Column(VARCHAR(200), nullable=False, unique=True)
    weight = Column(NUMBER(18, 10, True))
    length = Column(NUMBER(18, 10, True))
    width = Column(NUMBER(18, 10, True))
    height = Column(NUMBER(18, 10, True))
    heightfold = Column(NUMBER(18, 10, True))
    isactive = Column(NUMBER(1, 0, False), nullable=False)
    description = Column(VARCHAR(100))
    features = Column(NUMBER(10, 0, False), nullable=False)
    containertype = Column(NUMBER(2, 0, False))
    familyid = Column(ForeignKey('pre_pluscore.partfamilies.id'))
    jittype = Column(VARCHAR(1))
    minstock = Column(NUMBER(asdecimal=False))
    maxstock = Column(NUMBER(asdecimal=False))
    sequencequantity = Column(NUMBER(asdecimal=False))
    subfeatures = Column(NUMBER(10, 0, False))

    partfamily = relationship('Partfamily')
    projects = relationship('Project', secondary='pre_pluscore.projects_parts')


class Plannerpickup(Base):
    __tablename__ = 'plannerpickups'
    __table_args__ = (
        Index('uq_plannerpickup', 'pickupadviceid', 'siteid', unique=True),
        {'schema': 'pre_pluscore'}
    )

    id = Column(NUMBER(10, 0, False), primary_key=True)
    plannerid = Column(ForeignKey('pre_pluscore.planners.id'), nullable=False)
    pickupadviceid = Column(NUMBER(10, 0, False), nullable=False)
    amount = Column(NUMBER(18, 2, True), nullable=False)
    faregroup = Column(NUMBER(10, 0, False), nullable=False)
    siteid = Column(NUMBER(10, 0, False))

    planner = relationship('Planner')


t_projects_vehicletypes = Table(
    'projects_vehicletypes', metadata,
    Column('projectid', ForeignKey('pre_pluscore.projects.id'), primary_key=True, nullable=False),
    Column('vehicletypeid', ForeignKey('pre_pluscore.vehicletypes.id'), primary_key=True, nullable=False),
    schema='pre_pluscore'
)


class Ruleversion(Base):
    __tablename__ = 'ruleversions'
    __table_args__ = {'schema': 'pre_pluscore'}

    mayorversion = Column(NUMBER(10, 0, False), primary_key=True, nullable=False)
    minorversion = Column(NUMBER(10, 0, False), primary_key=True, nullable=False)
    ruleid = Column(ForeignKey('pre_pluscore.rules.id'), primary_key=True, nullable=False)
    code = Column(Text, nullable=False)
    notes = Column(VARCHAR(1000))

    rule = relationship('Rule')


class VdaPegasusErrorLine(Base):
    __tablename__ = 'vda_pegasus_error_lines'
    __table_args__ = {'schema': 'pre_pluscore'}

    id = Column(NUMBER(asdecimal=False), primary_key=True, nullable=False)
    file_id = Column(ForeignKey('pre_pluscore.vda_pegasus_file_errors.id'), primary_key=True, nullable=False)
    result = Column(VARCHAR(50))
    linalb = Column(VARCHAR(50))
    proveedor = Column(VARCHAR(50))
    cliente = Column(VARCHAR(50))
    coderr = Column(VARCHAR(50))
    linvda = Column(VARCHAR(50))
    tipreg = Column(VARCHAR(50))
    posvda = Column(VARCHAR(50))
    poscamp = Column(VARCHAR(50))
    loncamp = Column(VARCHAR(50))
    txtdeses = Column(VARCHAR(200))
    txtdesin = Column(VARCHAR(200))
    txtdesal = Column(VARCHAR(200))
    valinf = Column(VARCHAR(50))
    validated = Column(VARCHAR(1))

    file = relationship('VdaPegasusFileError')


class VdaPegasusTransmissionInfo(Base):
    __tablename__ = 'vda_pegasus_transmission_info'
    __table_args__ = {'schema': 'pre_pluscore'}

    id = Column(NUMBER(asdecimal=False), primary_key=True, nullable=False)
    file_id = Column(ForeignKey('pre_pluscore.vda_pegasus_file_errors.id'), primary_key=True, nullable=False)
    cliente = Column(VARCHAR(50))
    feresi = Column(DateTime)
    horesi = Column(VARCHAR(50))
    feemrvs = Column(VARCHAR(50))
    hoemrvs = Column(VARCHAR(50))
    estrvs = Column(VARCHAR(50))
    nomvir = Column(VARCHAR(500))
    codresul = Column(VARCHAR(50))
    resultado = Column(VARCHAR(600))
    oldtrnnumber = Column(VARCHAR(50))
    newtrnnumber = Column(VARCHAR(50))

    file = relationship('VdaPegasusFileError')


class Actor(Base):
    __tablename__ = 'actors'
    __table_args__ = {'schema': 'pre_pluscore'}

    id = Column(NUMBER(10, 0, False), primary_key=True)
    name = Column(VARCHAR(250), nullable=False)
    vatnumber = Column(VARCHAR(50), nullable=False)
    alias = Column(VARCHAR(50), unique=True)
    features = Column(NUMBER(10, 0, False), nullable=False)
    isactive = Column(NUMBER(1, 0, False), nullable=False)
    web = Column(VARCHAR(200))
    globalizationid = Column(ForeignKey('pre_pluscore.globalizations.id'))
    logisticzoneid = Column(NUMBER(10, 0, False))
    calendarid = Column(ForeignKey('pre_pluscore.calendars.id'))

    calendar = relationship('Calendar')
    globalization = relationship('Globalization')
    users = relationship('User', secondary='pre_pluscore.actors_users')
    projects = relationship('Project', secondary='pre_pluscore.projects_actors')


class Partfield(Base):
    __tablename__ = 'partfields'
    __table_args__ = {'schema': 'pre_pluscore'}

    id = Column(NUMBER(10, 0, False), primary_key=True)
    partid = Column(ForeignKey('pre_pluscore.parts.id'), nullable=False)
    fieldprojectid = Column(ForeignKey('pre_pluscore.fieldprojects.id'), nullable=False)
    name = Column(VARCHAR(100))

    fieldproject = relationship('Fieldproject')
    part = relationship('Part')


class Partmatched(Base):
    __tablename__ = 'partmatched'
    __table_args__ = (
        Index('partmatched_part_partuq', 'partid', 'matchedpartid', unique=True),
        {'schema': 'pre_pluscore'}
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    partid = Column(ForeignKey('pre_pluscore.parts.id'), nullable=False, index=True)
    matchedpartid = Column(ForeignKey('pre_pluscore.parts.id'))
    features = Column(NUMBER(asdecimal=False))
    levelstatus = Column(NUMBER(asdecimal=False), server_default=text("0"))

    part = relationship('Part', primaryjoin='Partmatched.matchedpartid == Part.id')
    part1 = relationship('Part', primaryjoin='Partmatched.partid == Part.id')


t_projects_parts = Table(
    'projects_parts', metadata,
    Column('projectid', ForeignKey('pre_pluscore.projects.id'), primary_key=True, nullable=False),
    Column('partid', ForeignKey('pre_pluscore.parts.id'), primary_key=True, nullable=False),
    schema='pre_pluscore'
)


class Trigger(Base):
    __tablename__ = 'triggers'
    __table_args__ = (
        ForeignKeyConstraint(['mayorversion', 'minorversion', 'ruleid'], ['pre_pluscore.ruleversions.mayorversion', 'pre_pluscore.ruleversions.minorversion', 'pre_pluscore.ruleversions.ruleid']),
        {'schema': 'pre_pluscore'}
    )

    entityid = Column(ForeignKey('pre_pluscore.entities.id'), primary_key=True, nullable=False)
    mayorversion = Column(NUMBER(10, 0, False), primary_key=True, nullable=False)
    minorversion = Column(NUMBER(10, 0, False), primary_key=True, nullable=False)
    ruleid = Column(NUMBER(10, 0, False), primary_key=True, nullable=False)
    validfrom = Column(TIMESTAMP)
    validto = Column(TIMESTAMP)
    isenabled = Column(NUMBER(1, 0, False))
    fireevents = Column(NUMBER(10, 0, False))
    siteid = Column(NUMBER(10, 0, False), primary_key=True, nullable=False)

    entity = relationship('Entity')
    ruleversion = relationship('Ruleversion')


class Actorfield(Base):
    __tablename__ = 'actorfields'
    __table_args__ = {'schema': 'pre_pluscore'}

    id = Column(NUMBER(10, 0, False), primary_key=True)
    actorid = Column(ForeignKey('pre_pluscore.actors.id'), nullable=False)
    fieldprojectid = Column(ForeignKey('pre_pluscore.fieldprojects.id'), nullable=False)
    name = Column(VARCHAR(100))

    actor = relationship('Actor')
    fieldproject = relationship('Fieldproject')


class Addres(Base):
    __tablename__ = 'address'
    __table_args__ = {'schema': 'pre_pluscore'}

    id = Column(NUMBER(10, 0, False), primary_key=True)
    name = Column(VARCHAR(200), nullable=False)
    city = Column(VARCHAR(200))
    postcode = Column(VARCHAR(50))
    province = Column(VARCHAR(200))
    countryid = Column(ForeignKey('pre_pluscore.countries.id'), nullable=False)
    isactive = Column(NUMBER(1, 0, False), nullable=False)
    farezoneid = Column(ForeignKey('pre_pluscore.farezones.id'))
    actorid = Column(ForeignKey('pre_pluscore.actors.id'))
    features = Column(NUMBER(10, 0, False), nullable=False)

    actor = relationship('Actor')
    country = relationship('Country')
    farezone = relationship('Farezone')


class Expeditiondestinationdate(Base):
    __tablename__ = 'expeditiondestinationdates'
    __table_args__ = {'schema': 'pre_pluscore'}

    id = Column(NUMBER(10, 0, False), primary_key=True)
    expeditionid = Column(ForeignKey('pre_pluscore.expeditions.id'))
    actoriddestination = Column(ForeignKey('pre_pluscore.actors.id'))
    edd_date = Column(DateTime)

    actor = relationship('Actor')
    expedition = relationship('Expedition')


class PartsActor(Base):
    __tablename__ = 'parts_actors'
    __table_args__ = (
        Index('parts_actors_uq', 'partid', 'actorid', unique=True),
        {'schema': 'pre_pluscore'}
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    partid = Column(ForeignKey('pre_pluscore.parts.id'), nullable=False)
    actorid = Column(ForeignKey('pre_pluscore.actors.id'), nullable=False)

    actor = relationship('Actor')
    part = relationship('Part')


t_projects_actors = Table(
    'projects_actors', metadata,
    Column('projectid', ForeignKey('pre_pluscore.projects.id'), primary_key=True, nullable=False),
    Column('actorid', ForeignKey('pre_pluscore.actors.id'), primary_key=True, nullable=False),
    schema='pre_pluscore'
)


class Contact(Base):
    __tablename__ = 'contacts'
    __table_args__ = {'schema': 'pre_pluscore'}

    id = Column(NUMBER(10, 0, False), primary_key=True)
    name = Column(VARCHAR(200), nullable=False)
    phone = Column(VARCHAR(50))
    mobile = Column(VARCHAR(50))
    fax = Column(VARCHAR(50))
    email = Column(VARCHAR(50))
    job = Column(VARCHAR(200))
    department = Column(VARCHAR(50))
    actorid = Column(ForeignKey('pre_pluscore.actors.id'))
    addressid = Column(ForeignKey('pre_pluscore.address.id'))
    isactive = Column(NUMBER(1, 0, False), nullable=False)
    featuresid = Column(NUMBER(10, 0, False))

    actor = relationship('Actor')
    addres = relationship('Addres')


class Warehouse(Base):
    __tablename__ = 'warehouses'
    __table_args__ = {'schema': 'pre_pluscore'}

    id = Column(NUMBER(10, 0, False), primary_key=True)
    name = Column(VARCHAR(200), nullable=False)
    addressid = Column(ForeignKey('pre_pluscore.address.id'))
    actorid = Column(ForeignKey('pre_pluscore.actors.id'))
    isactive = Column(NUMBER(1, 0, False), nullable=False)
    calendarid = Column(ForeignKey('pre_pluscore.calendars.id'))
    logisticzoneid = Column(NUMBER(10, 0, False))

    actor = relationship('Actor')
    addres = relationship('Addres')
    calendar = relationship('Calendar')


class Layout(Base):
    __tablename__ = 'layouts'
    __table_args__ = (
        Index('uq_layout_name', 'name', 'warehouseid', unique=True),
        {'schema': 'pre_pluscore'}
    )

    id = Column(NUMBER(10, 0, False), primary_key=True)
    name = Column(VARCHAR(200), nullable=False)
    isactive = Column(NUMBER(1, 0, False))
    height = Column(NUMBER(18, 2, True))
    width = Column(NUMBER(18, 2, True))
    depth = Column(NUMBER(18, 2, True))
    featuresid = Column(NUMBER(10, 0, False), nullable=False, index=True)
    warehouseid = Column(ForeignKey('pre_pluscore.warehouses.id'), nullable=False, index=True)
    farezoneid = Column(ForeignKey('pre_pluscore.farezones.id'), index=True)
    parentid = Column(ForeignKey('pre_pluscore.layouts.id'))
    operationtypeid = Column(NUMBER(10, 0, False))
    status = Column(NUMBER(1, 0, False), nullable=False, server_default=text("0 "))
    multipart = Column(NUMBER(1, 0, False), nullable=False, server_default=text("1 "))
    capacity = Column(NUMBER(10, 0, False), nullable=False, server_default=text("-1 "))
    useraccess = Column(NUMBER(1, 0, False))
    receptorid = Column(NUMBER(10, 0, False))
    dockcustomer = Column(VARCHAR(10))

    farezone = relationship('Farezone')
    parent = relationship('Layout', remote_side=[id])
    warehouse = relationship('Warehouse')


class ReportingemailContact(Base):
    __tablename__ = 'reportingemail_contact'
    __table_args__ = {'schema': 'pre_pluscore'}

    id = Column(NUMBER(10, 0, False), primary_key=True, nullable=False)
    reportingemailid = Column(NUMBER(10, 0, False), primary_key=True, nullable=False)
    contactid = Column(ForeignKey('pre_pluscore.contacts.id'), primary_key=True, nullable=False)

    contact = relationship('Contact')


class Site(Base):
    __tablename__ = 'sites'
    __table_args__ = {'schema': 'pre_pluscore'}

    id = Column(NUMBER(10, 0, False), primary_key=True)
    connectionstring = Column(VARCHAR(200), nullable=False)
    warehouseid = Column(ForeignKey('pre_pluscore.warehouses.id'), nullable=False)
    projectid = Column(ForeignKey('pre_pluscore.projects.id'), nullable=False)
    isactive = Column(NUMBER(1, 0, False), nullable=False)
    logoname = Column(VARCHAR(200))
    sitereportingid = Column(NUMBER(asdecimal=False))

    project = relationship('Project')
    warehouse = relationship('Warehouse')


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'pre_pluscore'}

    id = Column(NUMBER(10, 0, False), primary_key=True)
    name = Column(VARCHAR(200), nullable=False)
    alias = Column(VARCHAR(50), nullable=False, unique=True)
    isactive = Column(NUMBER(1, 0, False), nullable=False)
    comments = Column(VARCHAR(200))
    globalizationid = Column(ForeignKey('pre_pluscore.globalizations.id'))
    actorid = Column(ForeignKey('pre_pluscore.actors.id'), nullable=False)
    contactid = Column(ForeignKey('pre_pluscore.contacts.id'))
    membershipid = Column(ForeignKey('pre_pluscore.memberships.id'))
    lastsiteid = Column(NUMBER(10, 0, False))
    featuresid = Column(NUMBER(10, 0, False), server_default=text("1"))
    alerts = Column(NUMBER(1, 0, False), nullable=False, server_default=text("0 "))

    actor = relationship('Actor')
    contact = relationship('Contact')
    globalization = relationship('Globalization')
    membership = relationship('Membership')


class LoadType(Base):
    __tablename__ = 'LoadTypes'
    __table_args__ = {'schema': 'pre_pluscore'}

    Id = Column(NUMBER(10, 0, False), primary_key=True)
    Name = Column(Text, nullable=False)
    Description = Column(Text)
    SiteId = Column(ForeignKey('pre_pluscore.sites.id'))
    IsActive = Column(NUMBER(1, 0, False), nullable=False)

    site = relationship('Site')


t_actors_users = Table(
    'actors_users', metadata,
    Column('userid', ForeignKey('pre_pluscore.users.id'), primary_key=True, nullable=False),
    Column('actorid', ForeignKey('pre_pluscore.actors.id'), primary_key=True, nullable=False),
    schema='pre_pluscore'
)


class DockcustomerTransmissionCfg(Base):
    __tablename__ = 'dockcustomer_transmission_cfg'
    __table_args__ = (
        Index('dockcustomer_trans_cfg_uq', 'dockcustomer', 'tranmissionmovement', 'siteid', unique=True),
        {'schema': 'pre_pluscore'}
    )

    id = Column(NUMBER(10, 0, False), primary_key=True)
    siteid = Column(ForeignKey('pre_pluscore.sites.id'))
    dockcustomer = Column(VARCHAR(10))
    tranmissionmovement = Column(NUMBER(2, 0, False))
    erp_idc = Column(VARCHAR(10))
    erp_gf = Column(NUMBER(2, 0, False))
    erp_subtipo = Column(NUMBER(4, 0, False))
    erp_delegacion = Column(CHAR(2))
    erp_gestor = Column(VARCHAR(10))

    site = relationship('Site')


class Reportingemail(Base):
    __tablename__ = 'reportingemails'
    __table_args__ = {'schema': 'pre_pluscore'}

    id = Column(NUMBER(10, 0, False), primary_key=True)
    siteid = Column(ForeignKey('pre_pluscore.sites.id'), nullable=False)
    reportid = Column(NUMBER(10, 0, False))
    typeid = Column(NUMBER(10, 0, False))
    parameter = Column(VARCHAR(200))
    frequency = Column(NUMBER(10, 0, False))
    time = Column(TIMESTAMP)
    title = Column(VARCHAR(100), server_default=text("null"))

    site = relationship('Site')


class Sitefareconfiguration(Base):
    __tablename__ = 'sitefareconfiguration'
    __table_args__ = {'schema': 'pre_pluscore'}

    id = Column(NUMBER(10, 0, False), primary_key=True)
    fareid = Column(ForeignKey('pre_pluscore.fare.id'), nullable=False)
    siteid = Column(ForeignKey('pre_pluscore.sites.id'), nullable=False)
    validfrom = Column(TIMESTAMP, nullable=False)
    validto = Column(TIMESTAMP, nullable=False)
    faredate = Column(Text, nullable=False)

    fare = relationship('Fare')
    site = relationship('Site')


class Siteparam(Base):
    __tablename__ = 'siteparams'
    __table_args__ = (
        Index('siteparams_uq', 'key', 'siteid', unique=True),
        {'schema': 'pre_pluscore'}
    )

    id = Column(NUMBER(10, 0, False), primary_key=True)
    key = Column(VARCHAR(250))
    value = Column(VARCHAR(250))
    siteid = Column(ForeignKey('pre_pluscore.sites.id'), nullable=False)
    comments = Column(VARCHAR(100))

    site = relationship('Site')


class Siterelationship(Base):
    __tablename__ = 'siterelationships'
    __table_args__ = (
        Index('siterelationships_uq', 'childsiteid', 'parentsiteid', unique=True),
        {'schema': 'pre_pluscore'}
    )

    parentsiteid = Column(ForeignKey('pre_pluscore.sites.id'), nullable=False)
    childsiteid = Column(ForeignKey('pre_pluscore.sites.id'), nullable=False)
    id = Column(NUMBER(asdecimal=False), primary_key=True)

    site = relationship('Site', primaryjoin='Siterelationship.childsiteid == Site.id')
    site1 = relationship('Site', primaryjoin='Siterelationship.parentsiteid == Site.id')


class Useracces(Base):
    __tablename__ = 'useraccess'
    __table_args__ = {'schema': 'pre_pluscore'}

    id = Column(NUMBER(10, 0, False), primary_key=True)
    userid = Column(ForeignKey('pre_pluscore.users.id'), nullable=False)
    siteid = Column(ForeignKey('pre_pluscore.sites.id'))
    isactive = Column(NUMBER(1, 0, False), nullable=False)
    isuserdefault = Column(NUMBER(1, 0, False), nullable=False)

    site = relationship('Site')
    user = relationship('User')


class Useralert(Base):
    __tablename__ = 'useralerts'
    __table_args__ = {'schema': 'pre_pluscore'}

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    userid = Column(ForeignKey('pre_pluscore.users.id'), nullable=False)
    alert = Column(VARCHAR(500), nullable=False)
    checked = Column(NUMBER(1, 0, False), nullable=False)
    insertdate = Column(DateTime, nullable=False)
    checkeddate = Column(DateTime)
    teamalert = Column(NUMBER(1, 0, False), nullable=False)

    user = relationship('User')


class UsersPickup(Base):
    __tablename__ = 'users_pickups'
    __table_args__ = {'schema': 'pre_pluscore'}

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    userid = Column(ForeignKey('pre_pluscore.users.id'))
    puapid = Column(NUMBER(asdecimal=False))
    siteid = Column(ForeignKey('pre_pluscore.sites.id'))

    site = relationship('Site')
    user = relationship('User')


t_useraccess_permissions = Table(
    'useraccess_permissions', metadata,
    Column('permissionid', ForeignKey('pre_pluscore.permissions.id'), primary_key=True, nullable=False),
    Column('useraccessid', ForeignKey('pre_pluscore.useraccess.id'), primary_key=True, nullable=False),
    schema='pre_pluscore'
)
