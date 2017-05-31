import database

def load():
    census = database.StaticCSVDatabase(database.localpath('census/DataSet.csv'), 'fips',
                                        get_varyears=lambda df, var: [2000 + int(var[-2:])])
    census.set_metainfo(database.FunctionalMetainfo(get_description, lambda var: "unknown"))
    return census
