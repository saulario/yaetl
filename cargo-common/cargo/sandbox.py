

import sqlalchemy as sa

import cargo.bl.inf.sus
import cargo.bl.inf.uss
import cargo.bl.inf.usu

from cargo.bl.basedal import Filter, Query

def compile_filters(metadata, filters):

    ff = []
    for f in filters:
        column = metadata.tables[f.column[0:3]].c[f.column]
        ff.append(column == f.value)

    retval = sa.and_(*ff)
    print(stmt)
    return retval


if __name__ == "__main__":
    
    engine = sa.create_engine("mssql+pymssql://sa:mssql!123@localhost/C000000")
    metadata = sa.MetaData(bind=engine)
    conn = engine.connect()


    usuBL = cargo.bl.inf.usu.UsuBL(metadata)
    ussBL = cargo.bl.inf.uss.UssBL(metadata)
    sesBL = cargo.bl.inf.ses.SesBL(metadata)
    susBL = cargo.bl.inf.sus.SusBL(metadata)

    filters = []
    filters.append(Filter("sesact", "eq", 1))
    filters.append(Filter("sesact", "ne", 9))
    filters.append(Filter("sescre", "ge", "2020-01-01"))
    filters.append(Filter("sesususeq", "ge", 0))
    filters.append(Filter("sessusseq", "bw", "0:10"))
    filters.append(Filter("susnom", "lk", "EMPRESA"))
    j1 = sesBL.t.join(susBL.t, susBL.c.susseq == sesBL.c.sessusseq)
    stmt = sa.select([sesBL.t, susBL.t]).select_from(j1). \
            where(Query.compile(metadata, filters))

    rows = conn.execute(stmt).fetchall()




    
    conn.close()