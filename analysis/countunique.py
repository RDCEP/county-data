import hashlib
import numpy as np
import lib

allvars = {} # {name: set()}
for db, modname, variable in lib.all_variables():
    years = db.get_years(variable)
    if years is None:
        years = ['']

    if variable in allvars:
        allvars[variable].update(years)
    else:
        allvars[variable] = set(years)

print "Initial count: ", len(allvars), np.sum(map(lambda name: len(allvars[name]), allvars))

allvars = {} # hash: [variables]
for db, modname, variable in lib.all_variables():
    years = db.get_years(variable)
    if years is None:
        years = ['']

    for year in years:
        name = "%s.%s:%s" % (modname, variable, year)
        data = db.get_data(variable, year)

        myhash = hashlib.sha224(str(data))
        if myhash in allvars:
            print variable, year, "same as", allvars[myhash][0]
            allvars[myhash].append(name)
        else:
            allvars[myhash] = [name]
            
print "Total count: ", len(allvars)
