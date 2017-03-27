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

class CensusDatabase(database.CSVDatabase, database.YearVariableDatabase):
    def get_year(self, variable):
        """Return the year associated with the given variable."""
        return 2000 + int(variable[-2:])

def load():
    datapath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "DataSet.txt")
    return CensusDatabase(datapath, 'fips', get_description, lambda var: "unknown")

if __name__ == '__main__':
    census = load()
    print census.get_variables()
    print census.get_description('POP010210')
