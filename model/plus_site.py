# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, TIMESTAMP, VARCHAR, text
from sqlalchemy.dialects.oracle import NUMBER
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Deliverynote(Base):
    __tablename__ = 'deliverynotes'

    id = Column(NUMBER(10, 0, False), primary_key=True)
    status = Column(NUMBER(10, 0, False))
    deliverynotedate = Column(TIMESTAMP)
    receptiondate = Column(TIMESTAMP)
    actoridorigin = Column(NUMBER(10, 0, False))
    addressidorigin = Column(NUMBER(10, 0, False))
    layoutidorigin = Column(NUMBER(10, 0, False))
    contactidorigin = Column(NUMBER(10, 0, False))
    truck = Column(VARCHAR(50))
    trailer = Column(VARCHAR(50))
    trailertype = Column(NUMBER(10, 0, False))
    trucktype = Column(NUMBER(10, 0, False))
    manual = Column(NUMBER(1, 0, False), nullable=False, server_default=text("'0' "))
    deliveryreceptiondate = Column(TIMESTAMP)
    internalslb = Column(NUMBER(asdecimal=False))
    userid = Column(NUMBER(10, 0, False))
    insertdate = Column(TIMESTAMP)


class Pickupadvice(Base):
    __tablename__ = 'pickupadvices'

    id = Column(NUMBER(10, 0, False), primary_key=True)
    status = Column(NUMBER(10, 0, False), server_default=text("0"))
    pickupdate = Column(TIMESTAMP)
    receptiondate = Column(TIMESTAMP)
    actoridorigin = Column(NUMBER(10, 0, False))
    addressidorigin = Column(NUMBER(10, 0, False))
    layoutidorigin = Column(NUMBER(10, 0, False))
    contactidorigin = Column(NUMBER(10, 0, False))
    isactive = Column(NUMBER(1, 0, False), nullable=False)
    inputworkdate = Column(TIMESTAMP)
    outputworkdate = Column(TIMESTAMP)
    comments = Column(VARCHAR(200))
    updatedate = Column(TIMESTAMP)
    consignmentreferencenumber = Column(VARCHAR(100))


class Pickupadvicepackage(Base):
    __tablename__ = 'pickupadvicepackages'

    id = Column(NUMBER(10, 0, False), primary_key=True)
    actoriddestination = Column(NUMBER(10, 0, False), nullable=False)
    addressiddestination = Column(NUMBER(10, 0, False), nullable=False)
    layoutiddestination = Column(NUMBER(10, 0, False))
    weight = Column(NUMBER(18, 10, True), nullable=False)
    length = Column(NUMBER(18, 10, True))
    width = Column(NUMBER(18, 10, True))
    height = Column(NUMBER(18, 10, True))
    quantity = Column(NUMBER(10, 0, False), nullable=False)
    adrtype = Column(NUMBER(10, 0, False))
    stackingfactor = Column(NUMBER(10, 0, False))
    deliverynote = Column(VARCHAR(50))
    deliverynotedate = Column(TIMESTAMP)
    comments = Column(VARCHAR(200))
    CGId = Column(NUMBER(10, 0, False))
    puaid = Column(ForeignKey('pickupadvices.id'), nullable=False, index=True)
    isactive = Column(NUMBER(1, 0, False), nullable=False)
    urgency = Column(NUMBER(1, 0, False), nullable=False)
    deliverydateorigin = Column(TIMESTAMP)
    delverydate = Column(TIMESTAMP)
    status = Column(NUMBER(10, 0, False))
    Layout_Id = Column(NUMBER(10, 0, False))
    Actor_Id = Column(NUMBER(10, 0, False))
    warehousegroup = Column(VARCHAR(50))
    features = Column(NUMBER(10, 0, False), nullable=False, server_default=text("0 "))
    ordered = Column(NUMBER(10, 0, False))
    foldedheight = Column(NUMBER(18, 10, True))
    volume = Column(NUMBER(18, 10, True), server_default=text("0"))
    ordercomments = Column(VARCHAR(200))
    mainpartcode = Column(VARCHAR(200))
    receptiondatecc = Column(TIMESTAMP)
    departuredatecc = Column(TIMESTAMP)

    pickupadvice = relationship('Pickupadvice')


class Deliverynotepackage(Base):
    __tablename__ = 'deliverynotepackages'

    id = Column(NUMBER(10, 0, False), primary_key=True)
    dnid = Column(ForeignKey('deliverynotes.id'), nullable=False, index=True)
    actoriddestiny = Column(NUMBER(10, 0, False), nullable=False)
    addressiddestiny = Column(NUMBER(10, 0, False))
    layoutiddestiny = Column(NUMBER(10, 0, False))
    weight = Column(NUMBER(18, 10, True))
    length = Column(NUMBER(18, 10, True))
    width = Column(NUMBER(18, 10, True))
    height = Column(NUMBER(18, 10, True))
    puapid = Column(ForeignKey('pickupadvicepackages.id'), index=True)
    quantity = Column(NUMBER(10, 0, False))
    adrtypeid = Column(NUMBER(10, 0, False))
    stackingfactor = Column(NUMBER(10, 0, False))
    deliverynoteorigin = Column(VARCHAR(50))
    deliverynotedateorigin = Column(TIMESTAMP)
    comments = Column(VARCHAR(50))
    deliverydateorigin = Column(TIMESTAMP)
    deliverydate = Column(TIMESTAMP, server_default=text("sysdate"))
    urgency = Column(NUMBER(1, 0, False), server_default=text("0"))
    transportorder = Column(VARCHAR(100))
    bordero = Column(VARCHAR(100))
    receiptquantity = Column(NUMBER(10, 0, False))
    warehousegroup = Column(VARCHAR(50))
    features = Column(NUMBER(asdecimal=False))
    foldedheight = Column(NUMBER(18, 10, True))
    sofa = Column(VARCHAR(10))
    ordered = Column(NUMBER(10, 0, False))
    groupnumber = Column(NUMBER(10, 0, False))
    manufacturetype = Column(NUMBER(10, 0, False))
    mainpartcode = Column(VARCHAR(200))
    loadlistid = Column(NUMBER(10, 0, False), index=True)
    overtruck = Column(NUMBER(1, 0, False), nullable=False, server_default=text("0 "))
    bordero2 = Column(VARCHAR(100))
    transportorder2 = Column(VARCHAR(100))
    transmitted = Column(NUMBER(1, 0, False), nullable=False, server_default=text("0 "))
    borderodate = Column(TIMESTAMP)
    borderodate2 = Column(TIMESTAMP)
    transmissionfailed = Column(NUMBER(1, 0, False), nullable=False, server_default=text("0 "))
    bordercustom = Column(NUMBER(1, 0, False), nullable=False, server_default=text("0 "))
    receptiondatecc = Column(TIMESTAMP)
    departuredatecc = Column(TIMESTAMP)
    factweight_type = Column(NUMBER(1, 0, False))
    receptorid = Column(NUMBER(10, 0, False))
    dockcustomer = Column(VARCHAR(10))
    national = Column(NUMBER(1, 0, False))
    erp_idc_pickup = Column(VARCHAR(10))
    erp_idc_delivery = Column(VARCHAR(10))
    processdate4921 = Column(DateTime)

    deliverynote = relationship('Deliverynote')
    pickupadvicepackage = relationship('Pickupadvicepackage')
