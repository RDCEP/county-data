import os
import database

def get_description(variable):
    infopath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "DataDict.txt")
    with open(infopath, 'r') as fp:
        header = fp.next()
        columns = header.split()

        for line in fp:
            if line[:9] == variable:
                description = line[10:header.index('Unit')].strip()
                source = line[header.index('Source'):]
                others = line[header.index('Unit'):header.index('Source')].split()

                return "%s (%s; US total: %s).  Source: %s" % (description, others[0], others[2], source)

def load():
    census = database.MatrixCSVDatabase(database.localpath('census/DataSet.csv'), 'fips',
                                        get_varyears=lambda df, var: [2000 + int(var[-2:])])
    census.set_metainfo(database.FunctionalMetainfo(get_description, lambda var: "unknown"))
    return census

if __name__ == '__main__':
    census = load()
    print census.get_variables()
    print census.describe_variable('POP010210')
    print census.get_fips()[:10]
    print census.get_years('POP010210')
