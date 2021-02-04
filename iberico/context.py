
import sqlalchemy

class Context():

    def __init__(self, cp):

        self.cf_engine = sqlalchemy.create_engine(cp.get("DATASOURCES", "controlfac"))
        self.cf_metadata = sqlalchemy.MetaData(bind=self.cf_engine)        

        self.ib_engine = sqlalchemy.create_engine(cp.get("DATASOURCES", "iberico"))
        self.ibcore_metadata = sqlalchemy.MetaData(bind=self.ib_engine, schema="PRE_PLUSCORE")
        self.ibsite_metadata = sqlalchemy.MetaData(bind=self.ib_engine)

        self.mtbp_engine = sqlalchemy.create_engine(cp.get("DATASOURCES", "mtb_process"))
        self.mtbp_metadata = sqlalchemy.MetaData(bind=self.mtbp_engine, schema="MTB_PROCESS")

        self.wo_engine = sqlalchemy.create_engine(cp.get("DATASOURCES", "wo"))
        self.wo_metadata = sqlalchemy.MetaData(bind=self.wo_engine, schema="GT")
