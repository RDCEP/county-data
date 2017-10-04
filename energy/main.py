import database

def load():
    get_fips = lambda df: map(lambda ii: df[ii, 'NHGISST'] * 100 + df[ii, 'NHGISCTY'] / 10)
    variable_filter = lambda cols: filter(lambda col: 'NHGIS' in col or 'mean' in col or 'sum' in col or col == 'STATENAM', cols)
    return database.StaticCSVDatabase(database.localpath("energy/repotential.csv"), get_fips, variable_filter)
