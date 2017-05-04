import database
import re

filepath = database.localpath("USGS/USGS_gw_sw_use.xlsx")

def get_description(variable):
    chunks = variable.split('_')
    if len(chunks) == 1:
        return "unknown"

    source = dict(SW="surface water", GW="groundwater", To="total extractions")[chunks[1]]
    demand = dict(PS="public supply", PT="thermoelectric generation", DO="domestic use",
                  IR="irrigation", IN="industrial use", MI="mining", LI="livestock", TO="total use")[chunks[0]]

    return "%s for %s" % (source, demand)

def get_unit(variable):
    if re.match(r"^[A-Z]{2}_[GSWTo]{2}$", variable):
        return "Mgal/day"
    elif variable == 'TP_TotPop':
        return "1e3 people"
    elif variable == 'YEAR':
        return "year"
    else:
        return "name"

def load():
    dbs = []

    dbs.append(database.StaticCSVDatabase(filepath, 'FIPS', sheetname='1985', year=1985))
    dbs.append(database.StaticCSVDatabase(filepath, 'FIPS', sheetname='1990', year=1990))
    dbs.append(database.StaticCSVDatabase(filepath, 'FIPS', sheetname='1995', year=1995))
    dbs.append(database.StaticCSVDatabase(filepath, 'FIPS', sheetname='2000', year=2000))
    dbs.append(database.StaticCSVDatabase(filepath, 'FIPS', sheetname='2005', year=2005))
    dbs.append(database.StaticCSVDatabase(filepath, 'FIPS', sheetname='2010', year=2010))

    for db in dbs:
        db.set_metainfo(database.FunctionalMetainfo(get_description, get_unit))

    return database.CombinedYearsDatabase(dbs, dbs[-1].get_fips())
