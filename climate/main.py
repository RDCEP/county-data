import os, glob
import database

def load():
    metainfo = database.StoredMetainfo({'NHGISNAM': dict(unit="name"), 'NHGISST': dict(unit="code"), 'NHGISCTY': dict(unit="code"), 'STATENAM': dict(unit="name")})
    
    get_fips = lambda df: map(lambda ii: df[ii, 'NHGISST'] * 100 + df[ii, 'NHGISCTY'] / 10)
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
