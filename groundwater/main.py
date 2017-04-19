import database


def load():
    masterpath = database.localpath("awash/counties.csv")
    fipsdb = database.StaticCSVDatabase(masterpath, 'fips')

    return database.OrderedVectorDatabase.read_text(database.localpath("groundwater/drawdown0.txt"), 'drawdown', 2010, fipsdb)

if __name__ == '__main__':
    gw = load()
    print gw.get_variables()
    print gw.get_data('drawdown', 2010)[:10]
