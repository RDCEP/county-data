import os
import database

def load():
    crime = database.MatrixCSVDatabase(database.localpath('crime/baseline.csv'), 'county',
                                       get_varyears=lambda df, var: [2005])
    crime.set_metainfo(database.StoredMetainfo.load(database.localpath('crime/fields.fgh')))
    return crime
