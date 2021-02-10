#!/usr/bin/python3

import sqlalchemy

class Context():

    def __init__(self, cp):

        self.wo_engine = sqlalchemy.create_engine(cp.get("DATASOURCES", "wo"))
        self.wo_metadata = sqlalchemy.MetaData(bind=self.wo_engine, schema="GT")
