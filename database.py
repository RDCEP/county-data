import csv, pandas

class Database(object):
    def get_variables(self):
        """Return a list of variables."""
        raise NotImplementedError()

    def describe_variable(self, variable):
        """Text description of a variable."""
        raise NotImplementedError()

    def get_fips(self):
        """Return an ordered list of FIPS codes for the data."""
        raise NotImplementedError()

    def get_data(self, variable):
        """Return an ordered list of data values, in the same order as the FIPS codes."""
        raise NotImplementedError()

class YearVariableDatabase(Database):
    def get_year(self, variable):
        """Return the year associated with the given variable."""
        raise NotImplementedError()

class CSVDatabase(Database):
    def __init__(self, filepath, fips_column, get_description):
        """
        get_description: get_description(variable) returns the description of that variable.
        """
        self.filepath = filepath
        self.get_description = get_description

        with open(filepath, 'r') as fp:
            reader = csv.reader(fp)
            header = reader.next()

        self.df = pandas.read_csv(filepath, index_col=header.index(fips_column))

    def get_variables(self):
        return list(self.df)

    def describe_variable(self, variable):
        return self.get_description(variable)

    def get_fips(self):
        return self.df.index.values

    def get_data(self, variable):
        return self.df[variable]
