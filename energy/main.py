import database

def load():
    get_fips = lambda df: map(lambda ii: df[ii, 'NHGISST'] * 100 + df[ii, 'NHGISCTY'] / 10)
    variable_filter = lambda cols: filter(lambda col: 'NHGIS' in col or 'mean' in col or 'sum' in col or col == 'STATENAM', cols)

    metainfo = database.StoredMetainfo({'NHGISNAM': dict(unit="name"), 'NHGISST': dict(unit="code"), 'NHGISCTY': dict(unit="code"), 'STATENAM': dict(unit="name"), 'solarsum': dict(unit="W"), 'solarmean': dict(unit="W/m^2"), 'windsum': dict(unit="m^3/s"), 'windmean': dict(unit="m/s"), 'windpowerm' : dict(unit="W"), 'windpowers' : dict(unit="W/m^2")})
    
    db = database.StaticCSVDatabase(database.localpath("energy/repotential.csv"), get_fips, variable_filter)
    db.set_metainfo(metainfo)
    return db
