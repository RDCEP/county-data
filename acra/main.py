import os
import database

def load():
    centroid = database.MatrixCSVDatabase(database.localpath("acra/centroids.csv"), 'fips',
                                          get_varyears=lambda df, var: [None])
    centroid.set_metainfo(database.StoredMetainfo.load(database.localpath("acra/fields.fgh")))

    elevation = database.MatrixCSVDatabase(database.localpath("acra/elevation.csv"), 'fips',
                                           get_varyears=lambda df, var: [None])
    elevation.set_metainfo(database.StoredMetainfo.load(database.localpath("acra/fields.fgh")))

    name = database.MatrixCSVDatabase(database.localpath("acra/us-county-names.csv"), 'fips',
                                      get_varyears=lambda df, var: [None])
    name.set_metainfo(database.StoredMetainfo.load(database.localpath("acra/fields.fgh")))

    dbs = [centroid, elevation, name]
    prefixes = ['centroid', 'elevation', 'name']
    return database.CombinedDatabase(dbs, prefixes, '.')
