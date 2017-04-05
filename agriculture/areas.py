import os, glob
import database

pathhere = os.path.dirname(os.path.realpath(__file__))
masterpath = os.path.join(pathhere, "../awash/counties.csv")

def load():
    dbs = []
    prefixes = []

    dbs.append(database.StaticCSVDatabase(os.path.join(pathhere, "irrigatedareas.csv"), 'FIPS'))
    prefixes.append('irrigatedareas')

    dbs.append(database.StaticCSVDatabase(os.path.join(pathhere, "rainfedareas.csv"), 'FIPS'))
    prefixes.append('rainfedareas')

    dbs.append(database.StaticCSVDatabase(os.path.join(pathhere, "knownareas.csv"), 'fips'))
    prefixes.append('knownareas')

    dbs.append(database.StaticCSVDatabase(os.path.join(pathhere, "totalareas.csv"), 'FIPS'))
    prefixes.append('totalareas')

    return database.CombinedDatabase(dbs, prefixes, '.')

if __name__ == '__main__':
    weather = load()
    print weather.get_variables()
    print weather.get_years("irrigatedareas.Otherhay")
    print weather.get_data("irrigatedareas.Otherhay", None)[:10]
    print weather.get_data("rainfedareas.Otherhay", None)[:10]
