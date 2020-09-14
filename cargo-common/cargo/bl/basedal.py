#!/usr/bin/python3
# -*- coding: utf-8 -*-

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

    def __init__(self, metadata, nombre, pk=None):
        self._metadata = metadata
        self._t = Table(nombre, metadata, autoload = True)
        self._pk = pk if pk is not None else (nombre + BaseDAL.SEQ_SUFFIX)
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


    def getTable(self):
        return self._t


    def c(self):
        return self._t.c


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

    def __init__(self, metadata, nombre, pk=None):
        super().__init__(metadata, nombre, pk)


    def read(self, conn, id, upi=None):
        return self._read(conn, id)


    def _before_insert(self, conn, entity, upi):
        pass

    def _after_insert(self, conn, entity, upi):
        pass

    def insert(self, conn, entity, upi=None):
        self._before_insert(conn, entity, upi)
        result = self._insert(conn, entity)
        self._after_insert(conn, entity, upi)
        return result


    def _before_update(self, conn, entity, upi):
        pass

    def _after_update(self, conn, entity, upi):
        pass

    def update(self, conn, entity, upi=None):
        self._before_update(conn, entity, upi)
        retval = self._update(conn, entity)
        self._after_update(conn, entity, upi)
        return retval


    def _before_delete(self, conn, entity, upi):
        pass

    def _after_delete(self, conn, entity, upi):
        pass

    def delete(self, conn, id, upi=None):
        self._before_delete(conn, id, upi)
        retval = self._delete(conn, id)
        self._after_delete(conn, id, upi)
        return retval


    def select(self):
        return self.getTable().select()

