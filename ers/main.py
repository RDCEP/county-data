import re
import numpy as np
import pandas as pd
from database import Database, ConcatenatedDatabase, localpath

class ERSDatabase(Database):
    def __init__(self, crop, includeus=True, includecrop=False):
        self.crop = crop
        self.includeus = includeus
        self.includecrop = includecrop
        
        data = pd.read_csv(localpath("ers/ers.csv"))
        self.data = data[data["crop"] == crop]
        
        self.link = pd.read_csv(localpath("ers/reglink.csv"))
    
    def get_variables(self):
        """
        List all available ERS information items.
        """
        if self.includecrop:
            return map(lambda x: self.crop + '.' + x, self.data["item"].unique())
        else:
            return self.data["item"].unique()

    def get_fips(self):
        """Return an ordered list of FIPS codes for the data.  FIPS should always be 5 character strings."""
        return self.link["FIPS"]

    def get_years(self, variable):
        """Return a list of years available."""
        return self.data["year"][self.data["item"] == variable].unique()

    def get_data(self, variable, year):
        """Return an ordered list of data values, in the same order as the FIPS codes."""
        if variable[:5] == self.crop + '.':
            variable = variable[5:]
        
        subdf = self.data[(self.data["item"] == variable) & (self.data["year"] == year)]

        result = np.array([np.nan] * self.link.shape[0])
        for region in self.link["ABBR"].unique():
            value = subdf.loc[subdf["region"] == region, "value"].tolist()
            if len(value) == 0:
                continue
            
            result[self.link["ABBR"] == region] = value[0]

        if self.includeus:
            value = subdf.loc[subdf["region"] == "us", "value"].tolist()
            result[np.isnan(result)] = value[0]

        return result

    def get_unit(self, variable):
        m = re.search(r'\((.*)\)$', variable)
        if m:
            return m.group(1)
        else:
            return "USD"
    
def load():
    dbs = []
    for crop in ["corn", "soyb", "whea", "sorg", "barl", "cott", "rice", "oats", "pean"]:
        dbs.append(ERSDatabase(crop, includecrop=True))

    return ConcatenatedDatabase(dbs)

