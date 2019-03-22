# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, ForeignKeyConstraint, VARCHAR
from sqlalchemy.dialects.oracle import NUMBER
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Vda4921Message(Base):
    __tablename__ = 'vda_4921_messages'

    id = Column(NUMBER(10, 0, False), primary_key=True)
    receiver = Column(VARCHAR(20))
    sender = Column(VARCHAR(20))
    previoustransmission = Column(NUMBER(9, 0, False))
    currenttransmission = Column(NUMBER(9, 0, False))
    transmissiondate = Column(DateTime)
    processidentification = Column(VARCHAR(100))
    server = Column(VARCHAR(50))
    filedate = Column(DateTime)
    filename = Column(VARCHAR(200))
    insertdate = Column(DateTime)
    businesscaseid = Column(NUMBER(9, 0, False))
    businesscasename = Column(VARCHAR(200))


class Vda4921TransportIdentific(Base):
    __tablename__ = 'vda_4921_transport_identific'

    messageid = Column(ForeignKey('vda_4921_messages.id'), primary_key=True, nullable=False)
    transportvehicleid = Column(NUMBER(10, 0, False), primary_key=True, nullable=False)
    transportkey = Column(VARCHAR(5))
    transportnumber = Column(VARCHAR(30))
    bordero = Column(VARCHAR(20))
    borderodate = Column(DateTime)
    borderocorrectionkey = Column(VARCHAR(1))
    specialtransportnumber = Column(VARCHAR(10))
    shipmentvolume = Column(NUMBER(8, 3, True))
    shipmentlinearmetres = Column(NUMBER(8, 3, True))
    specialtransporttype = Column(VARCHAR(10))
    currentlocationdate = Column(DateTime)
    deliveringforwarder = Column(VARCHAR(50))
    estimatedtimeofarrival = Column(DateTime)
    informationcorrectionkey = Column(VARCHAR(1))

    vda_4921_message = relationship('Vda4921Message')


class Vda4921FwdAgentDatum(Base):
    __tablename__ = 'vda_4921_fwd_agent_data'
    __table_args__ = (
        ForeignKeyConstraint(['messageid', 'transportvehicleid'], ['vda_4921_transport_identific.messageid', 'vda_4921_transport_identific.transportvehicleid']),
    )

    messageid = Column(NUMBER(10, 0, False), primary_key=True, nullable=False)
    transportvehicleid = Column(NUMBER(10, 0, False), primary_key=True, nullable=False)
    forwardingagentdataid = Column(NUMBER(10, 0, False), primary_key=True, nullable=False)
    supplierid = Column(VARCHAR(10))
    shipmentnumber = Column(VARCHAR(10))
    freightforwarderorderid = Column(VARCHAR(20))
    freightfrwrdrregistrationdate = Column(DateTime)
    shipmentkey = Column(VARCHAR(1))
    shipmentgrossweight = Column(NUMBER(9, 0, False))
    shipmentnetweight = Column(NUMBER(9, 0, False))
    numberofhandlingunits = Column(NUMBER(9, 0, False))
    unloadingpoint = Column(VARCHAR(10))
    supplierplant = Column(VARCHAR(10))
    customerplant = Column(VARCHAR(10))
    sendercountry = Column(VARCHAR(10))
    senderzip = Column(VARCHAR(10))
    receivercountry = Column(VARCHAR(10))
    receiverzip = Column(VARCHAR(10))
    incotermfrankatur = Column(VARCHAR(10))
    positionnumber = Column(NUMBER(9, 0, False))
    volume = Column(NUMBER(8, 3, True))
    linearmetres = Column(NUMBER(8, 3, True))
    chargeableweight = Column(NUMBER(9, 0, False))

    vda_4921_transport_identific = relationship('Vda4921TransportIdentific')


class Vda4921DeliveryNote(Base):
    __tablename__ = 'vda_4921_delivery_notes'
    __table_args__ = (
        ForeignKeyConstraint(['messageid', 'transportvehicleid', 'forwardingagentdataid'], ['vda_4921_fwd_agent_data.messageid', 'vda_4921_fwd_agent_data.transportvehicleid', 'vda_4921_fwd_agent_data.forwardingagentdataid']),
    )

    messageid = Column(NUMBER(10, 0, False), primary_key=True, nullable=False)
    transportvehicleid = Column(NUMBER(10, 0, False), primary_key=True, nullable=False)
    forwardingagentdataid = Column(NUMBER(10, 0, False), primary_key=True, nullable=False)
    deliverynoteindexid = Column(NUMBER(10, 0, False), primary_key=True, nullable=False)
    deliveynotenumber1 = Column(VARCHAR(8))
    deliveynotenumber2 = Column(VARCHAR(8))
    deliveynotenumber3 = Column(VARCHAR(8))
    deliveynotenumber4 = Column(VARCHAR(8))
    deliveynotenumber5 = Column(VARCHAR(8))
    deliveynotenumber6 = Column(VARCHAR(8))
    deliveynotenumber7 = Column(VARCHAR(8))
    deliveynotenumber8 = Column(VARCHAR(8))
    deliveynotenumber9 = Column(VARCHAR(8))
    deliveynotenumber10 = Column(VARCHAR(8))
    deliveynotenumber11 = Column(VARCHAR(8))
    deliveynotenumber12 = Column(VARCHAR(8))
    deliveynotenumber13 = Column(VARCHAR(8))
    deliveynotenumber14 = Column(VARCHAR(8))
    deliveynotenumber15 = Column(VARCHAR(8))

    vda_4921_fwd_agent_datum = relationship('Vda4921FwdAgentDatum')
