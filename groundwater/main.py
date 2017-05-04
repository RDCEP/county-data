import os, glob
import database

def load():
    masterpath = database.localpath("awash/counties.csv")
    fipsdb = database.StaticCSVDatabase(masterpath, 'fips')

    dbs = []
    for filepath in glob.glob(database.localpath("groundwater/*.txt")):
        db = database.OrderedVectorDatabase.read_text(filepath, os.path.basename(filepath[:-4]), 2010, fipsdb)
        if os.path.basename(filepath[:-4]) == 'aquifer_depth':
            db.set_metainfo(database.UniformMetainfo("Depth to groundwater table", "m"))
        dbs.append(db)

    return database.ConcatenatedDatabase(dbs)
