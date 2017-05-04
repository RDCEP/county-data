import os, glob
import database

pathhere = os.path.dirname(os.path.realpath(__file__))
masterpath = os.path.join(pathhere, "../awash/counties.csv")

class SingleVariableDatabase(database.MatrixCSVDatabase):
    def __init__(self, filepath, variable):
        self.variable = variable
        variable_filter = lambda vars: [self.variable]
        get_varyears = lambda df, var: map(int, list(df))
        get_datarows = lambda df, var, yr: df[str(yr)]

        super(SingleVariableDatabase, self).__init__(filepath, None, variable_filter,
                                                     get_varyears, get_datarows)

def load():
    fipsdb = database.StaticCSVDatabase(masterpath, 'fips')

    dbs = []

    for filename in glob.glob(os.path.join(pathhere, "edds/*.csv")):
        filename = os.path.basename(filename)

        filepath = os.path.join(pathhere, "edds", filename)
        db = database.OrderedDatabase.use_fips(fipsdb, SingleVariableDatabase(filepath, filename[:-4]))
        db.set_metainfo(database.UniformMetainfo(None, 'C day'))
        dbs.append(db)

    return database.ConcatenatedDatabase(dbs)

if __name__ == '__main__':
    weather = load()
    print weather.get_variables()
    print weather.get_years("Barley-gdd")
    print weather.get_data("Barley-gdd", 1990)[:10]
    print weather.get_data("Barley-gdd", 1991)[:10]
