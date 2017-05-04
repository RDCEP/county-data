import os
import database

def get_dictline(variable):
    infopath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "DataDict.txt")
    with open(infopath, 'r') as fp:
        header = fp.next()
        columns = header.split()

        for line in fp:
            if line[:9] == variable:
                return line, header

def get_description(variable):
    line, header = get_dictline(variable)
    description = line[10:header.index('Unit')].strip()
    source = line[header.index('Source'):]
    others = line[header.index('Unit'):header.index('Source')].split()

    return "%s (%s; US total: %s).  Source: %s" % (description, others[0], others[2], source)

def get_unit(variable):
    line, header = get_dictline(variable)
    unit = line[header.index('Unit')+1:header.index('Decimal')-1]
    if unit == 'PCT':
        return 'percent'
    if unit == 'SQM':
        return 'mi^2'

    return "unknown"

def load():
    census = database.MatrixCSVDatabase(database.localpath('census/DataSet.csv'), 'fips',
                                        get_varyears=lambda df, var: [2000 + int(var[-2:])])
    census.set_metainfo(database.FunctionalMetainfo(get_description, get_unit))
    return census
