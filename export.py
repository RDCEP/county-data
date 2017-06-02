import os, importlib, csv
from cmd import Cmd
import numpy as np

class Exporter(Cmd):
    prompt = "> "

    loaded = {} # prefix: db
    variables = []

    def do_available(self, line):
        """List all available databases.
        Usage: available
        """
        for root, dir, files in os.walk("."):
            if '__init__.py' in files:
                print root[2:]

    def do_load(self, module):
        """Load an available database.
        Usage: available [DB name]
        """
        print "Loading " + module + "..."
        try:
            db = importlib.import_module(module + '.main').load()
            self.loaded[module] = db
            print self.loaded.keys()
        except Exception as ex:
            print "Failed to load " + module
            print ex

    def do_describe(self, variable):
        """Describe a variable.
        Usage: describe [variable]
        """
        try:
            # Look for this variable
            db = self.get_database()
            print db.describe_variable(variable)
            print "Years: " + str(db.get_years(variable))
        except:
            print "Could not find variable " + variable

    def do_list(self, line):
        """List the available variables across all loaded databases.
        Usage: list
        """
        db = self.get_database()
        if db is None:
            print "None."
        else:
            print db.get_variables()

    def do_add(self, variable):
        """Add a variable to the export list.
        Usage: add [variable]
        """
        try:
            # Look for this variable
            db = self.get_database()
            print db.describe_variable(variable)
            print "Years: " + str(db.get_years(variable))
            self.variables.append(variable)
        except:
            print "Could not find variable " + variable

    def do_export(self, filepath):
        """Export all variables on the export list to a file.
        Usage: export [file path]
        """
        # Collect all data
        data = {}
        db = self.get_database()
        for variable in self.variables:
            years = db.get_years(variable)
            if years is None:
                data[variable] = np.array(db.get_data(variable, None))
            else:
                for year in years:
                    data[variable + ':' + str(year)] = np.array(db.get_data(variable, year))

        with open(filepath, 'w') as fp:
            writer = csv.writer(fp)
            writer.writerow(['fips'] + data.keys())
            for ii in range(len(db.get_fips())):
                row = [db.get_fips()[ii]] + [data[key][ii] for key in data.keys()]
                writer.writerow(row)

    def get_database(self):
        if not self.loaded:
            return None

        if self.loaded and len(self.loaded) == 1:
            return self.loaded.values()[0]

        return CombinedDatabase(self.loaded.values(), self.loaded.keys(), '.')

    def do_bye(self, line):
        """Close the interface.
        Usage: bye
        """
        return True

print "Welcome to the County Data Exporter."
print "For help, type `help`.\n"
Exporter().cmdloop()
