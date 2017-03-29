import os
import database

def load():
    crime = database.MatrixCSVDatabase(database.localpath('crime/baseline.csv'), 'county',
                                       get_varyears=lambda df, var: [2005])
    crime.set_metainfo(database.StoredMetainfo.load(database.localpath('crime/fields.fgh')))
    return crime

if __name__ == '__main__':
    crime = load()
    print crime.get_variables()
    print crime.describe_variable('violent')
    print crime.get_fips()[:10]

    import numpy as np
    print np.nanmean(crime.get_data('violent', 2005)), np.nanmean(crime.get_data('property', 2005))
