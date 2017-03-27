import os
import numpy as np
import database

fields = {} # {code: {start:, length:, decimals:, ftype:, year:, tags:, description:}}
awashstarts = [1, 91, 497, 21683, 21729, 21735, 25782, 32307, 32167, 32183, 32199]

class AHRFDatabase(database.Database, database.YearVariableDatabase, database.TaggedVariableDatabase):
    def get_variables(self):
        """Return a list of variables."""
        return fields.keys()

    def describe_variable(self, variable):
        """Text description of a variable."""
        return fields[variable].get('description', None)

    def get_unit(self, variable):
        """Canonical unit for variable."""
        return "unknown"

    def get_fips(self):
        """Return an ordered list of FIPS codes for the data."""
        fipses = self.get_data('f00002')
        return map(lambda fips: str(int(fips)), fipses)

    def get_data(self, variable):
        """Return an ordered list of data values, in the same order as the FIPS codes."""
        start = fields[variable]['start']
        end = fields[variable]['start'] + fields[variable]['length']
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "DATA/AHRF2014.asc"), 'r') as fp:
            data = [line[start:end] for line in fp]
            if fields[variable]['ftype'] == float:
                return map(lambda datum: float(datum.strip()) if datum.strip() != '.' else np.nan, data)
            return data

    def get_year(self, variable):
        """Return the year associated with the given variable."""
        return fields[variable].get('year', None)

    def get_tags(self, variable):
        """Return a list of tags for each variable."""
        return fields[variable]['tags']

def load():
    # Lines: @line+1 code ($) length.
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "DOC/AHRF2014.sas"), 'r') as fp:
        for line in fp:
            if len(line.strip()) == 0:
                continue

            if line.lstrip()[0] == '@':
                chunks = line.split()
                start = int(chunks[0][1:]) - 1
                code = chunks[1]
                if chunks[2] == '$':
                    ftype = str
                    digits = chunks[3].split('.')
                else:
                    ftype = float
                    digits = chunks[2].split('.')

                length = int(digits[0])
                decimals = int(digits[1]) if digits[1] else 0

                fields[code] = dict(start=start, length=length, ftype=ftype, tags=[])
                if start in awashstarts:
                    fields[code]['tags'].append('AWASH')

            if line.lstrip()[0] == 'f':
                chunks = line.strip().split('="')
                code = chunks[0]
                try:
                    year = int(chunks[1][-5:-1])
                    fields[code]['year'] = year
                except:
                    pass

                fields[code]['description'] = chunks[1][:-1]

    return AHRFDatabase()

if __name__ == '__main__':
    ahrf = load()
    print ahrf.get_variables()[:10]
    print ahrf.describe_variable('f0081176')
    print ahrf.get_fips()[:10]
    print ahrf.get_data('f0081176')[:10]
