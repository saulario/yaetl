#!/usr/bin/python3
# -*- coding: utf-8 -*-

from sqlalchemy import and_, MetaData, Table

import datetime

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
    """
    Clase base para los artefactos de acceso a base de datos
    """

    def __init__(self, metadata, nombre):
        self._metadata = metadata
        self._t = Table(nombre, metadata, autoload = True)


    def read(self, conn, id):
        stmt = self._t.select().where(self._t.c.id == id)
        return self._execute_read(conn, stmt)


    def insert(self, conn, entity): 
        stmt = self._t.insert(None).values(entity.__dict__)
        return conn.execute(stmt)


    def update(self, conn, entity):
        if entity is None:
            return None
        id = entity.id
        d = entity.__dict__
        d.pop("id")
        stmt = self._t.update(None).values(d). \
            where(self._t.c.id == id)
        return conn.execute(stmt)

    def query(self, conn, stmt):
        retval = []
        results = conn.execute(stmt).fetchall()
        for result in results:
            retval.append(Entity.fromProxy(result))
        return retval


    def _execute_read(self, conn, stmt):
        return Entity.fromProxy(conn.execute(stmt).fetchone())


    def select(self):
        return self._t.select()


    def getTable(self):
        return self._t


    def getEntity(self):
        return Entity.fromTable(self._t)
