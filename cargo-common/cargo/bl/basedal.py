#!/usr/bin/python3
# -*- coding: utf-8 -*-

from sqlalchemy import and_, MetaData, Table

class Entity():

    @staticmethod
    def fromProxy(proxy):
        """
        Construye una entidad a partir de un proxy  
        param:      proxy: ResultProxy
        returns:    entity: obtenido el resultproxy
        """
        if proxy is None:
            return
        e = Entity()
        for key in proxy.iterkeys():
            setattr(e, key, proxy[key])
        return e


    @staticmethod
    def fromTable(table):
        """
        Construye una entidad a partir de los metadatos de una tabla
        param:      table: Tabla
        returns:    entity: obtenida a partir de los metadatos
        """
        if table is None:
            return
        e = Entity()
        for c in table.c:
            setattr(e, c.key, None)
        return e


class BaseDAL():

    def __init__(self, metadata, nombre):
        self._metadata = metadata
        self._t = Table(nombre, metadata, autoload = True)


    def _read(self, conn, id):
        if id is None:
            return None
        stmt = self._t.select().where(self._t.c.id == id)
        return Entity.fromProxy(conn.execute(stmt).fetchone())


    def _insert(self, conn, entity): 
        if entity is None:
            return None
        if "version" in entity.__dict__:
            entity.__dict__["version"] = 0
        d = entity.__dict__.copy()
        d.pop("id")
        stmt = self._t.insert(None).values(d)
        result = conn.execute(stmt)
        entity.id = result.inserted_primary_key[0]
        return result


    def _update(self, conn, entity):
        if entity is None:
            return None
        id = entity.id
        d = entity.__dict__
        d.pop("id")
        stmt = self._t.update(None).values(d).where(self._t.c.id == id)
        return conn.execute(stmt)


    def _delete(self, conn, id):
        if id is None:
            return None
        stmt = self._t.delete(None).where(self._t.c.id == id)
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

    def __init__(self, metadata, nombre):
        super().__init__(metadata, nombre)


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

