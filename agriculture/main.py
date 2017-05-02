import database
import fields, weather, areas

def load():
    dbs = []
    prefixes = []

    fielddb = fields.load()
    dbs.append(fielddb)
    prefixes.append("field")

    weatherdb = weather.load()
    dbs.append(weatherdb)
    prefixes.append("weather")

    areadb = areas.load()
    dbs.append(areadb)
    prefixes.append("area")

    return database.CombinedDatabase(dbs, prefixes, '.')
