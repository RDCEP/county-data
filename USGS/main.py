import database

filepath = database.localpath("USGS/USGS_gw_sw_use.xlsx")

def load():
    dbs = []

    dbs.append(database.StaticCSVDatabase(filepath, 'FIPS', sheetname='1985', year=1985))
    dbs.append(database.StaticCSVDatabase(filepath, 'FIPS', sheetname='1990', year=1990))
    dbs.append(database.StaticCSVDatabase(filepath, 'FIPS', sheetname='1995', year=1995))
    dbs.append(database.StaticCSVDatabase(filepath, 'FIPS', sheetname='2000', year=2000))
    dbs.append(database.StaticCSVDatabase(filepath, 'FIPS', sheetname='2005', year=2005))
    dbs.append(database.StaticCSVDatabase(filepath, 'FIPS', sheetname='2010', year=2010))

    return database.CombinedYearsDatabase(dbs, dbs[-1].get_fips())
