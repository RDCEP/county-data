import os, importlib, csv
from cmd import Cmd

class Exporter(Cmd):
    loaded = {} # prefix: db
    variables = []
    
    def do_available(self, line):
        for root, dir, files in os.walk("."):
            if '__init__.py' in files:
                print root[2:]

    def do_load(self, module):
        print "Loading " + module + "..."
        try:
            db = importlib.import_module(module + '.main').load()
            self.loaded[module] = db
            print self.loaded.keys()
        except Exception as ex:
            print "Failed to load " + module
            print ex
            
    def do_list(self, line):
        db = self.get_database()
        if db is None:
            print "None."
        else:
            print db.get_variables()

    def do_add(self, variable):
        try:
            # Look for this variable
            print self.get_database().describe_variable(variable)
            print "Years: " + str(variable.get_years(variable))
            self.variables.append(variable)
        except:
            print "Could not find variable " + variable
        
    def do_export(self, filepath):
        # Collect all data
        data = {}
        db = self.get_database()
        for variable in self.variables:
            years = db.get_years(variable)
            if years is None:
                data[variable] = db.get_data(variable, None)
            else:
                for year in years:
                    data[variable + ':' + str(year)] = db.get_data(variable, year)

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
        self.close()
        bye()
        return True
    
Exporter().cmdloop()
