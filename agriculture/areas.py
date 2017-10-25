import os, glob
import database

pathhere = os.path.dirname(os.path.realpath(__file__))
masterpath = os.path.join(pathhere, "../awash/counties.csv")

def load():
    dbs = []
    prefixes = []

    metainfo = database.StoredMetainfo({'FIPS': dict(unit="name"), 'Alfalfa': dict(unit="acre"), 'Otherhay': dict(unit="acre"), 'Barley': dict(unit="acre"), 'Barley.Winter': dict(unit="acre"), 'Maize': dict(unit="acre"), 'Sorghum': dict(unit="acre"), 'Soybean': dict(unit="acre"), 'Wheat': dict(unit="acre"), 'Wheat.Winter': dict(unit="acre"), 'fips': dict(unit="name"), 'known': dict(unit="acre"), 'total': dict(unit="acre"), 'barley': dict(unit="acre"), 'corn': dict(unit="acre"), 'sorghum': dict(unit="acre"), 'soybeans': dict(unit="acre"), 'wheat': dict(unit="acre"), 'hay': dict(unit="acre")})

    db = database.StaticCSVDatabase(os.path.join(pathhere, "irrigatedareas.csv"), 'FIPS', year=2010)
    db.set_metainfo(metainfo)
    dbs.append(db)
    prefixes.append('irrigatedareas')

    db = database.StaticCSVDatabase(os.path.join(pathhere, "rainfedareas.csv"), 'FIPS', year=2010)
    db.set_metainfo(metainfo)
    dbs.append(db)
    prefixes.append('rainfedareas')

    db = database.StaticCSVDatabase(os.path.join(pathhere, "knownareas.csv"), 'fips', year=2010)
    db.set_metainfo(metainfo)
    dbs.append(db)
    prefixes.append('knownareas')

    db = database.StaticCSVDatabase(os.path.join(pathhere, "totalareas.csv"), 'FIPS', year=2010)
    db.set_metainfo(metainfo)
    dbs.append(db)
    prefixes.append('totalareas')

    return database.CombinedDatabase(dbs, prefixes, '.')

if __name__ == '__main__':
    weather = load()
    print weather.get_variables()
    print weather.get_years("irrigatedareas.Otherhay")
    print weather.get_data("irrigatedareas.Otherhay", None)[:10]
    print weather.get_data("rainfedareas.Otherhay", None)[:10]
