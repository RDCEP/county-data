import os, csv, pandas
import numpy as np
from metainfo import *

def standardize_fips(fips):
    if isinstance(fips, list) or isinstance(fips, np.ndarray) or isinstance(fips, pandas.core.series.Series):
        return map(standardize_fips, fips)

    if isinstance(fips, str):
        return '0' + fips if len(fips) < 5 else fips

    return standardize_fips(str(int(fips)))

def localpath(relative):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), relative)

class Database(object):
    def __init__(self):
        self.metainfo = Metainfo()

    def set_metainfo(self, metainfo):
        self.metainfo = metainfo

    def get_variables(self):
        """Return a list of variables."""
        raise NotImplementedError()

    def describe_variable(self, variable):
        """Text description of a variable."""
        return self.metainfo.describe_variable(variable)

    def get_unit(self, variable):
        """Canonical unit for variable."""
        return self.metainfo.get_unit(variable)

    def get_tags(self, variable):
        """Return a list of tags for each variable."""
        return self.metainfo.get_tags(variable)

    def get_fips(self):
        """Return an ordered list of FIPS codes for the data.  FIPS should always be 5 character strings."""
        raise NotImplementedError()

    def get_years(self, variable):
        """Return a list of years available."""
        raise NotImplementedError()

    def get_data(self, variable, year):
        """Return an ordered list of data values, in the same order as the FIPS codes."""
        raise NotImplementedError()

class CSVDatabase(Database):
    def __init__(self, filepath, variable_filter=lambda vars: vars, index_col=False):
        super(CSVDatabase, self).__init__()

        self.filepath = filepath
        self.variable_filter = variable_filter
        self.df = pandas.read_csv(filepath, index_col=index_col)

    def get_variables(self):
        return self.variable_filter(list(self.df))

    def make_index_column(self, id_func, indexcol='index'):
        self.df[indexcol] = self.df.apply(id_func, axis=1)
        self.df.set_index(indexcol)

class StaticCSVDatabase(CSVDatabase):
    def __init__(self, filepath, fips_column, variable_filter=lambda vars: vars):
        super(StaticCSVDatabase, self).__init__(filepath, variable_filter=variable_filter)
        self.fips_column = fips_column

    def get_fips(self):
        return self.df[self.fips_column]

    def get_years(self, variable):
        return None

    def get_data(self, variable, year):
        return self.df[variable]

class MatrixCSVDatabase(CSVDatabase):
    def __init__(self, filepath, fips_column,
                 variable_filter=lambda vars: vars, get_varyears=lambda df, var: None,
                 get_datarows=lambda df, var, yr: df[var]):

        if fips_column is not None:
            with open(filepath, 'rU') as fp:
                reader = csv.reader(fp)
                header = reader.next()
                index_col = header.index(fips_column)

            super(MatrixCSVDatabase, self).__init__(filepath, variable_filter=variable_filter, index_col=index_col)
        else:
            super(MatrixCSVDatabase, self).__init__(filepath, variable_filter=variable_filter)

        self.standard_fips = None
        self.get_varyears = get_varyears
        self.get_datarows = get_datarows

    def get_fips(self):
        if self.standard_fips is None:
            self.standard_fips = standardize_fips(self.df.index.values)

        return self.standard_fips

    def get_years(self, variable):
        return self.get_varyears(self.df, variable)

    def get_data(self, variable, year):
        return self.get_datarows(self.df, variable, year)

class ObservationsCSVDatabase(CSVDatabase):
    def __init__(self, filepath, fips_column, year_column,
                 variable_filter=lambda vars: vars):
        super(ObservationsCSVDatabase, self).__init__(filepath, variable_filter=variable_filter)
        self.fips_column = fips_column
        self.year_column = year_column

    def get_fips(self):
        return self.df[self.fips_column].unique()

    def get_years(self, variable):
        return self.df[self.year_column].unique()

    def get_data(self, variable, year):
        ## This would be very slow because of constant re-ordering.  Use get_fipsdata(variable, year)
        raise NotImplementedError()

    def get_fipsdata(self, variable, year):
        rows = self.df[self.year_column] == year
        return self.df[self.fips_column][rows], self.df[variable][rows]

class IDReferenceCSVDatabase(MatrixCSVDatabase):
    def __init__(self, filepath1, id_column1, filepath2, id_column2, fips_column2, *args, **kwargs):
        super(IDReferenceCSVDatabase, self).__init__(filepath1, id_column1, *args, **kwargs)

        idref = pandas.read_csv(filepath2)
        self.idorder = idref[id_column2]
        self.fipsorder = standardize_fips(idref[fips_column2])

    def get_fips(self):
        return self.fipsorder

    def get_data(self, variable, year):
        data = super(IDReferenceCSVDatabase, self).get_data(variable, year)
        return data.loc[self.idorder]

class OrderedDatabase(Database):
    def __init__(self, fips, db):
        super(OrderedDatabase, self).__init__()

        self.fips = fips
        self.db = db
        self.set_metainfo(db.metainfo)

    def get_variables(self):
        return self.db.get_variables()

    def get_fips(self):
        return self.fips

    def get_years(self, variable):
        return self.db.get_years(variable)

    def get_data(self, variable, year):
        return self.db.get_data(variable, year)

    @staticmethod
    def use_fips(fipsdb, db):
        return OrderedDatabase(fipsdb.get_fips(), db)

class ConcatenatedDatabase(Database):
    """All database must have the same order of fips."""

    def __init__(self, dbs):
        super(ConcatenatedDatabase, self).__init__()

        self.dbs = dbs
        assert not isinstance(dbs[0], ObservationsCSVDatabase), "Cannot use randomly indexed data for master dataset."

        catalog = {} # variable -> db
        for db in dbs:
            assert np.all(db.get_fips() == dbs[0].get_fips())
            for variable in db.get_variables():
                catalog[variable] = db

        self.catalog = catalog

    def get_variables(self):
        """Return a list of variables."""
        return self.catalog.keys()

    def describe_variable(self, variable):
        """Text description of a variable."""
        return self.catalog[variable].describe_variable(variable)

    def get_unit(self, variable):
        """Canonical unit for variable."""
        return self.catalog[variable].get_unit(variable)

    def get_fips(self):
        """Return an ordered list of FIPS codes for the data."""
        return self.dbs[0].get_fips()

    def get_years(self, variable):
        return self.catalog[variable].get_years(variable)

    def get_data(self, variable, year):
        """Return an ordered list of data values, in the same order as the FIPS codes."""
        return self.catalog[variable].get_data(variable, year)

class CombinedDatabase(Database):
    """Always uses first database for fips codes."""

    def __init__(self, dbs, prefixes, infix):
        super(CombinedDatabase, self).__init__()

        self.dbs = dbs
        self.prefixes = prefixes
        self.infix = infix
        self.indices = {} # {db: [indices]}

        assert not isinstance(dbs[0], ObservationsCSVDatabase), "Cannot use randomly indexed data for master dataset."

    def get_variables(self):
        """Return a list of variables."""
        variables = []
        for ii in range(len(self.dbs)):
            dbvars = ["%s%s%s" % (self.prefixes[ii], self.infix, variable) for variable in self.dbs[ii].get_variables()]
            variables.extend(dbvars)

        return variables

    def get_database(self, variable):
        chunks = variable.split(self.infix)
        return self.dbs[self.prefixes.index(chunks[0])], chunks[1]

    def get_indices_byfips(self, dbfips, values):
        fips = self.dbs[0].get_fips()
        result = np.empty(len(fips))
        for ii in range(len(fips)):
            try:
                result[ii] = values[dbfips.index(fips[ii])]
            except:
                result[ii] = np.nan

        return result

    def get_indices(self, db, values):
        if db not in self.indices:
            fips = self.dbs[0].get_fips()
            dbfips = db.get_fips()
            indices = np.empty(len(fips), dtype=int)
            for ii in range(len(fips)):
                try:
                    indices[ii] = dbfips.index(fips[ii])
                except:
                    indices[ii] = -1
            self.indices[db] = indices

        return [values.iloc[index] if index != -1 else np.nan for index in self.indices[db]]

    def describe_variable(self, variable):
        """Text description of a variable."""
        db, dbvar = self.get_database(variable)
        return db.describe_variable(dbvar)

    def get_unit(self, variable):
        """Canonical unit for variable."""
        db, dbvar = self.get_database(variable)
        return db.get_unit(dbvar)

    def get_fips(self):
        """Return an ordered list of FIPS codes for the data."""
        return self.dbs[0].get_fips()

    def get_years(self, variable):
        db, dbvar = self.get_database(variable)
        return db.get_years(dbvar)

    def get_data(self, variable, year):
        """Return an ordered list of data values, in the same order as the FIPS codes."""
        db, dbvar = self.get_database(variable)
        if db == self.dbs[0]:
            return db.get_data(dbvar, year)

        if 'get_fipsdata' in dir(db):
            fips, data = db.get_fipsdata(dbvar, year)
            return self.get_indices_byfips(fips, data)

        data = db.get_data(dbvar, year)

        # Match up the data along the fips
        return self.get_indices(db, data)
