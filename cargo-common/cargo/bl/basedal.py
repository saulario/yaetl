#!/usr/bin/python3
# -*- coding: utf-8 -*-

from enum import Enum
from sqlalchemy import and_, MetaData, Table

class Entity():

    @staticmethod
    def fromProxy(proxy):
        if proxy is None:
            return
        e = Entity()
        for key in proxy.iterkeys():
            setattr(e, key, proxy[key])
        return e


    @staticmethod
    def fromTable(table):
        if table is None:
            return
        e = Entity()
        for c in table.c:
            setattr(e, c.key, None)
        return e


class BaseDAL():

    SEQ_SUFFIX = "seq"
    VERSION_SUFFIX = "ver"
    ACTIVE_SUFFIX = "act"

    def __init__(self, metadata, nombre, pk=None, schema=None):
        self._metadata = metadata
        self._t = Table(nombre, metadata, autoload = True)
        self._pk = pk if pk is not None else (nombre + BaseDAL.SEQ_SUFFIX)
        self._schema = schema
        self._version = nombre + BaseDAL.VERSION_SUFFIX
        self._active = nombre + BaseDAL.ACTIVE_SUFFIX


    def _read(self, conn, id):
        if id is None:
            return None
        stmt = self._t.select().where(self._t.columns[self._pk] == id)
        return Entity.fromProxy(conn.execute(stmt).fetchone())


    def _insert(self, conn, entity): 
        if entity is None:
            return None
        if self._version in entity.__dict__:
            entity.__dict__[self._version] = 0
        d = entity.__dict__.copy()
        if self._pk.endswith(BaseDAL.SEQ_SUFFIX) and self._pk in d:
            d.pop(self._pk)
        stmt = self._t.insert(None).values(d)
        result = conn.execute(stmt)
        if self._pk.endswith(BaseDAL.SEQ_SUFFIX):
            setattr(entity, self._pk, result.inserted_primary_key[0])
        return result


    def _update(self, conn, entity):
        if entity is None:
            return None
        d = entity.__dict__.copy()
        if self._pk.endswith(BaseDAL.SEQ_SUFFIX) and self._pk in d:
            d.pop(self._pk)
        stmt = self._t.update(None).values(d).\
                where(self._t.columns[self._pk] == entity.__dict__[self._pk])
        return conn.execute(stmt)


    def _delete(self, conn, id):
        if id is None:
            return None
        stmt = self._t.delete(None).\
                where(self._t.columns[self._pk] == id)
        return conn.execute(stmt)


    def _query(self, conn, stmt):
        retval = []
        results = conn.execute(stmt).fetchall()
        for result in results:
            retval.append(Entity.fromProxy(result))
        return retval


    def __select(self):
        return self._t.select()


    @property
    def c(self):
        return self._t.c


    @property
    def t(self):
        return self._t


    def getEntity(self):
        return Entity.fromTable(self._t)


class AuthorizationException(Exception):

    def __init__(self, *args, **kwargs):
        super().__init__(args)


class IllegalStateException(Exception):

    def __init__(self, *args, **kwargs):
        super().__init__(args)


class OptimisticLockException(Exception):

    def __init__(self, *args, **kwargs):
        super().__init__(args)


class BaseBL(BaseDAL):

    def __init__(self, metadata, nombre, pk=None, schema=None):
        super().__init__(metadata, nombre, pk, schema)


    def _after_read(self, conn, entity, **kwargs):
        pass

    def read(self, conn, id, **kwargs):
        entity = self._read(conn, id)
        self._after_read(conn, entity, **kwargs)
        return entity


    def _before_insert(self, conn, entity, **kwargs):
        pass

    def _after_insert(self, conn, entity, **kwargs):
        pass

    def insert(self, conn, entity, **kwargs):
        self._before_insert(conn, entity, **kwargs)
        result = self._insert(conn, entity)
        self._after_insert(conn, entity, **kwargs)
        return result


    def _before_update(self, conn, entity, **kwargs):
        pass

    def _after_update(self, conn, entity, **kwargs):
        pass

    def update(self, conn, entity, **kwargs):
        self._before_update(conn, entity, **kwargs)
        retval = self._update(conn, entity)
        self._after_update(conn, entity, **kwargs)
        return retval


    def _before_delete(self, conn, entity, **kwargs):
        pass

    def _after_delete(self, conn, entity, **kwargs):
        pass

    def delete(self, conn, id, **kwargs):
        self._before_delete(conn, id, **kwargs)
        retval = self._delete(conn, id)
        self._after_delete(conn, id, **kwargs)
        return retval


    def select(self):
        return self.t.select()


class Operator(Enum):
    EQUALS = "eq"
    GREATER = "gt"
    GREATER_OR_EQUALS = "ge"
    LOWER = "lt"
    LOWER_OR_EQUALS = "le"
    IN = "in"
    BETWEEN = "bw"
    STARTS_WITH = "sw"
    ENDS_WITH = "ew"
    LIKE = "lk"        


class Filter:

    def __init__(self, column, operator, value):
        self.column = column
        self.operator = operator
        self.value = value

class Query:

    @classmethod
    def compile(self, metadata, filters):
        ff = []
        for f in filters:
            column = metadata.tables[f.column[0:3]].c[f.column]
            if f.operator == Operator.EQUALS.value:
                ff.append(column == f.value)
            elif f.operator == Operator.GREATER.value:
                ff.append(column > f.value)
            elif f.operator == Operator.GREATER_OR_EQUALS.value:
                ff.append(column >= f.value)
            elif f.operator == Operator.LOWER.value:
                ff.append(column < f.value)
            elif f.operator == Operator.LOWER_OR_EQUALS.value:
                ff.append(column <= f.value)                
            elif f.operator == Operator.IN.value:
                ff.append(column.in_(f.value.split(",")))                
            elif f.operator == Operator.BETWEEN.value:
                v = f.value.split(":")
                ff.append(between(column, v[0], v[1]))
            elif f.operator == Operator.STARTS_WITH.value:
                ff.append(column.like(f.value + "%"))
            elif f.operator == Operator.ENDS_WITH.value:
                ff.append(column.like("%" + f.value))
            elif f.operator == Operator.LIKE.value:
                ff.append(column.like("%" + f.value + "%"))
        return and_(*ff)
