import os, glob
import database

def load():
    masterpath = database.localpath("awash/counties.csv")
    fipsdb = database.StaticCSVDatabase(masterpath, 'fips')

    dbs = []
    for filepath in glob.glob(database.localpath("groundwater/*.txt")):
        db = database.OrderedVectorDatabase.read_text(filepath, os.path.basename(filepath[:-4]), 2010, fipsdb)
        dbs.append(db)

    return database.ConcatenatedDatabase(dbs)

if __name__ == '__main__':
    gw = load()
    print gw.get_variables()
    print gw.get_data('drawdown0', 2010)[:10]
