import os, glob
import numpy as np
import database

def load():
    metainfo = database.StoredMetainfo({'NHGISNAM': dict(unit="name"), 'NHGISST': dict(unit="code"), 'NHGISCTY': dict(unit="code"), 'STATENAM': dict(unit="name"), 'bio1_mean': dict(unit='dC'), 'bio2_mean': dict(unit='dC'), 'bio5_mean': dict(unit='dC'), 'bio6_mean': dict(unit='dC'), 'bio7_mean': dict(unit='dC'), 'bio8_mean': dict(unit='dC'), 'bio9_mean': dict(unit='dC'), 'bio10_mean': dict(unit='dC'), 'bio11_mean': dict(unit='dC'), 'bio12_mean': dict(unit='mm'), 'bio13_mean': dict(unit='mm'), 'bio14_mean': dict(unit='mm'), 'bio16_mean': dict(unit='mm'), 'bio17_mean': dict(unit='mm'), 'bio18_mean': dict(unit='mm'), 'bio19_mean': dict(unit='mm')})
    
    get_fips = lambda df: np.array(df['NHGISST']) * 100 + np.array(df['NHGISCTY']) / 10
    variable_filter = lambda cols: filter(lambda col: 'NHGIS' in col or '_mean' in col or col == 'STATENAM', cols)
    current = database.StaticCSVDatabase(database.localpath("climate/bioclims-current.csv"), get_fips, variable_filter)
    current.set_metainfo(metainfo)

    dbs = [current]
    prefixes = ['current']
    for filepath in glob.glob(database.localpath("climate/bioclims-2050/*.csv")):
        db = database.StaticCSVDatabase(filepath, get_fips, variable_filter, year=2050)
        db.set_metainfo(metainfo)
        dbs.append(db)
        prefixes.append(filepath[filepath.rindex('/')+1:filepath.rindex('/')+3])
        
    return database.CombinedDatabase(dbs, prefixes, '.')
