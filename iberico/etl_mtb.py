import configparser
import os

import sqlalchemy

if __name__ == "__main__":
    cp = configparser.ConfigParser()
    cp.read(os.path.expanduser("~") + "/etc/config.ini")

    mtbp_engine = sqlalchemy.create_engine(cp.get("DATASOURCES", "mtb_process"))
    mtbp_metadata = sqlalchemy.MetaData(bind=mtbp_engine, schema="MTB_PROCESS")

    ib_engine = sqlalchemy.create_engine(cp.get("DATASOURCES", "iberico"))
    ibcore_metadata = sqlalchemy.MetaData(bind=ib_engine, schema="PRE_PLUSCORE")
    ibsite_metadata = sqlalchemy.MetaData(bind=ib_engine)

