import os, glob, re
import database

pathhere = os.path.dirname(os.path.realpath(__file__))
masterpath = os.path.join(pathhere, "Master_Spreadsheet_All.csv")

class MatrixDatabase(database.IDReferenceCSVDatabase):
    def __init__(self, filepath, crop, unit, variable):
        super(MatrixDatabase, self).__init__(filepath, 'cnty_FID', masterpath, 'FID', 'FIPS',
                                             variable_filter=lambda vars: [variable],
                                             get_varyears=lambda df, var: [int(vv[-4:]) for vv in df if vv[:len(variable)] == variable] if var == variable else None,
                                             get_datarows=lambda df, var, yr: df['%s_%d' % (var, yr)])
        self.crop = crop
        self.unit = unit
        self.variable = variable

    def describe_variable(self, variable):
        """Text description of a variable."""
        if variable != self.variable:
            return None
        if variable == 'AREA_PLANTED':
            return "%s area planted" % self.crop
        if variable == 'AREA_HARVESTED':
            return "%s area harvested" % self.crop
        if variable == 'AREA_HARVESTED':
            return "%s area harvested" % self.crop
        if variable == 'PRODUCTION':
            return "%s production" % self.crop

    def get_unit(self, variable):
        """Canonical unit for variable."""
        if variable != self.variable:
            return None
        return self.unit

class USDADatabase(database.ObservationsCSVDatabase):
    def __init__(self, filepath, crop, isirr, report):
        super(USDADatabase, self).__init__(filepath, None, 'Year',
                                           variable_filter=lambda vars: ['Value'])
        self.crop = crop
        self.isirr = isirr
        self.report = report

        self.make_index_column(lambda row: row['State ANSI'] + row['County ANSI'])
        self.fips_column = 'index'

    def describe_variable(self, variable):
        if variable == 'Value':
            return self.df['Data Item'][0]

    def get_unit(self, variable):
        if variable == 'Value':
            if self.report == 'planted' or self.report == 'harvested':
                return 'acre'
            if self.report == 'production':
                if crop == 'cotton':
                    return '480 LB BALES'
                if crop in ['maize', 'wheat']:
                    return 'BU'

def load():
    dbs = []
    prefixes = []

    dbs.append(database.MatrixCSVDatabase(masterpath, 'FIPS'))
    prefixes.append('agmaster')

    for filename in glob.glob(os.path.join(pathhere, "allyears/*.csv")):
        filename = os.path.basename(filename)
        areamatch = re.match(r'([a-z]+)_area_([a-z]+)_in_acre\.csv', filename)
        if areamatch:
            crop = areamatch.group(1)
            measured = areamatch.group(2)

            db = MatrixDatabase(os.path.join(pathhere, "allyears", filename), crop, 'acre', 'AREA_%s' % measured.upper())
            dbs.append(db)
            prefixes.append('%s-area' % crop)
            continue

        prodmatch = re.match(r'([a-z]+)_production_in_([a-z]+)\.csv', filename)
        if prodmatch:
            crop = prodmatch.group(1)
            unit = prodmatch.group(2)

            db = MatrixDatabase(os.path.join(pathhere, "allyears", filename), crop, unit, 'PRODUCTION')
            dbs.append(db)
            prefixes.append('%s-production' % crop)
            continue

        usdamatch = re.match(r'([a-z]+)-([a-z]+)-([a-z]+)\.csv', filename)
        if usdamatch:
            crop = usdamatch.group(1)
            isirr = usdamatch.group(2)
            report = usdamatch.group(3)

            db = USDADatabase(os.path.join(pathhere, "allyears", filename), crop, isirr, report)
            dbs.append(db)
            prefixes.append('%s-%s-%s' % (crop, isirr, report))
            continue

        usda2007match = re.match(r'([a-z]+)-total-([a-z]+)-2007\.csv', filename)
        if usda2007match:
            crop = usda2007match.group(1)
            isirr = 'total'
            report = usda2007match.group(2)

            db = USDADatabase(os.path.join(pathhere, "allyears", filename), crop, isirr, report)
            dbs.append(db)
            prefixes.append('%s-%s-%s' % (crop, isirr, report))
            continue

    return database.CombinedDatabase(dbs, prefixes, '.')

if __name__ == '__main__':
    ag = load()
    print ag.get_variables()
    print ag.get_data('soybeans-production.PRODUCTION', 2000)[:10]
    print ag.get_data('soybeans-production.PRODUCTION', 2001)[:10]
    print ag.get_data('wheat-nonirrigated-production.Value', 2000)[:10]
    print ag.get_data('wheat-nonirrigated-production.Value', 2001)[:10]
