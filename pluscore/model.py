# coding: utf-8
from sqlalchemy import Column, DateTime, Text
from sqlalchemy.dialects.oracle.base import NUMBER, RAW
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class ServicebusMessagesPending(Base):
    __tablename__ = 'servicebus_messages_pending'

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
