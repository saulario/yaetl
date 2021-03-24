#!/usr/bin/python3

import sqlalchemy

class Context():

    def __init__(self, cp):

        self.wo_engine = sqlalchemy.create_engine(cp.get("DATASOURCES", "wo"))
        self.wo_metadata = sqlalchemy.MetaData(bind=self.wo_engine, schema="GT")

        self.ib_engine = sqlalchemy.create_engine(cp.get("DATASOURCES", "iberico"))
        self.ibcore_metadata = sqlalchemy.MetaData(bind=self.ib_engine, schema="PRE_PLUSCORE")
        self.ibsite_metadata = sqlalchemy.MetaData(bind=self.ib_engine)        