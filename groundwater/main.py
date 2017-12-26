import os, glob
import database

def load():
    masterpath = database.localpath("awash/counties.csv")
    fipsdb = database.StaticCSVDatabase(masterpath, 'fips')

    dbs = []
    for filepath in glob.glob(database.localpath("groundwater/*.txt")):
        if os.path.basename(filepath) == 'notes.txt':
            continue
        db = database.OrderedVectorDatabase.read_text(filepath, os.path.basename(filepath[:-4]), 2010, fipsdb)
        if os.path.basename(filepath[:-4]) == 'aquifer_depth':
            db.set_metainfo(database.UniformMetainfo("Depth to groundwater table", "m"))
        if os.path.basename(filepath[:-4]) == 'piezohead0':
            db.set_metainfo(database.UniformMetainfo("piezohead", "m"))
        if os.path.basename(filepath[:-4]) == 'county_area':
            db.set_metainfo(database.UniformMetainfo("county area", "m^2"))
        if os.path.basename(filepath[:-4]) == 'county_elevation':
            db.set_metainfo(database.UniformMetainfo("county elevation", "m"))
        if os.path.basename(filepath[:-4]) == 'drawdown0':
            db.set_metainfo(database.UniformMetainfo("draw down", "m"))
        if os.path.basename(filepath[:-4]) == 'vector_storativity':
            db.set_metainfo(database.UniformMetainfo(" ", "None"))
        dbs.append(db)

    return database.ConcatenatedDatabase(dbs)
