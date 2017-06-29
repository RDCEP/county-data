import database, metainfo
import re

def load():
    filepath = database.localpath("labor/lab_cty_00_05_sum.csv")
    db = database.StaticCSVDatabase(filepath, 'fips', year=2002)
    db.set_metainfo(metainfo.StoredMetainfo.load_csv(database.localpath("labor/info.csv"), 'variable', 'description', 'unit'))
    return db
