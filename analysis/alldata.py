import csv
import numpy as np
#import database, lib
import database
from analysis import lib

def all_data():
    for db, modname, variable in lib.all_variables():
        years = db.get_years(variable)
        if years is None:
            years = ['']
        # Just choose one year
        if len(years) > 1:
            year = years[-1]
        else:
            year = years[0]
        # Don't load the data
        yield db, modname, variable, year

allfips = set()
for db, modname, variable, year in all_data():
    allfips.update(db.get_fips())
        
with open("results.csv", 'w') as fp:
    writer = csv.writer(fp)
    writer.writerow(['module', 'variable', 'year'] + list(allfips))
    
    for db, modname, variable, year in all_data():
        fips = list(db.get_fips())
        data = np.array(db.get_data(variable, year))
                        
        row = [modname, variable, year] + [data[fips.index(ff)] if ff in fips else np.nan for ff in allfips]
        print(row[:3])
        writer.writerow(row)
