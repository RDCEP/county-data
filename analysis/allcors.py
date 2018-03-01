import csv
import numpy as np
import database, lib
#import database
#from analysis import lib

def all_data():
    for db, modname, variable in lib.all_variables():
        years = db.get_years(variable)
        if years is None:
            years = ['']
        # Just choose one year
        if len(years) > 1:
            if 2000 in years:
                year = 2000
            else:
                year = years[0]
        else:
            year = years[0]
        # Don't load the data
        yield db, modname, variable, year
        
knowns = {}
with open("results.csv", 'r') as fp:
    reader = csv.reader(fp)
    header = next(reader)
    for row in reader:
        if row[-1] != 'nan':
            knowns[tuple(row[:-1])] = float(row[-1])
        else:
            knowns[tuple(row[:-1])] = np.nan

with open("results.csv", 'w') as fp:
    writer = csv.writer(fp)
    writer.writerow(['db1', 'var1', 'year1', 'db2', 'var2', 'year2', 'corr'])
    
    for db1, modname1, variable1, year1 in all_data():
        data1 = np.array(db1.get_data(variable1, year1))
        
        for db2, modname2, variable2, year2 in all_data():
            knownkey = (modname1, variable1, str(year1), modname2, variable2, str(year2))
            if knownkey in knowns:
                corr = knowns[knownkey]
            else:
                if not db1.get_unit(variable1) or db1.get_unit(variable1) == "unknown" or not db2.get_unit(variable2) or db2.get_unit(variable2) == "unknown":
                    continue

                data2 = np.array(db2.get_data(variable2, year2))
                if isinstance(data1[0], str) or isinstance(data1[0], unicode) or isinstance(data2[0], str) or isinstance(data2[0], unicode):
                    continue
                if np.all(data1 == data1[0]) or np.all(data2 == data2[0]):
                    continue
                if (modname1, variable1, year1) == (modname2, variable2, year2):
                    corr = 1.0
                else:
                    if modname1 != modname2:
                        db = database.CombinedDatabase([db1, db2], [modname1, modname2], '.')
                        data1 = np.array(db.get_data(modname1 + '.' + variable1, year1))
                        data2 = np.array(db.get_data(modname2 + '.' + variable2, year2))
                    
                    valid = np.isfinite(data1) * np.isfinite(data2)
                    if sum(valid) < 3 or np.all(data1[valid] == data1[valid][0]) or np.all(data2[valid] == data2[valid][0]):
                        print "No values"
                        print data2
                        corr = np.nan
                    else:
                        corr = np.corrcoef(data1[valid], data2[valid])[0,1]
                        assert not np.isnan(corr)
                    ## print "Failed on", modname1, variable1, year1, modname2, variable2, year2
                
            row = [modname1, variable1, year1, modname2, variable2, year2, corr]
            print row
            writer.writerow(row)
            
