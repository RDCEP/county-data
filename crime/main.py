import os
import database

descriptions = dict(violent="Murder, rape, and assault", property="Robbery, burglary, larceny, and vehicle theft")

def load():
    datapath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "baseline.csv")
    return database.MatrixCSVDatabase(datapath, 'county', lambda var: descriptions[var], lambda var: "crimes",
                                      get_varyears=lambda df, var: [2005])

if __name__ == '__main__':
    crime = load()
    print crime.get_variables()
    print crime.get_description('violent')
    print crime.get_fips()[:10]

    import numpy as np
    print np.nanmean(crime.get_data('violent', 2005)), np.nanmean(crime.get_data('property', 2005))
