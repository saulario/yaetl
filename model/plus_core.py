# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Index, TIMESTAMP, Text, VARCHAR, text
from sqlalchemy.dialects.oracle import NUMBER, RAW
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Expedition(Base):
    __tablename__ = 'expeditions'

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
    partnerexpedition = Column(ForeignKey('expeditions.id'))
    expeditiontype = Column(NUMBER(10, 0, False))
    ttupdated = Column(NUMBER(1, 0, False), server_default=text("(0)"))
    reportsent = Column(NUMBER(10, 0, False))
    woid = Column(NUMBER(10, 0, False))
    siteid = Column(NUMBER(10, 0, False))
    commentsplanning = Column(Text)
    woidpedido = Column(NUMBER(10, 0, False))

    parent = relationship('Expedition', remote_side=[id])


class Expeditiondetail(Base):
    __tablename__ = 'expeditiondetails'
    __table_args__ = (
        Index('ind_expeditiondetail_id_siteid', 'siteid', 'id'),
        Index('ind_expe_puapid', 'puapid', 'siteid')
    )

    id = Column(NUMBER(10, 0, False), primary_key=True)
    expid = Column(ForeignKey('expeditions.id'), nullable=False, index=True)
    siteid = Column(NUMBER(10, 0, False), nullable=False)
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
