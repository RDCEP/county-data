import database

def column2variable_2008(column):
    if column in ['x2008_SYMBOL', 'x2012_GROUP']:
        return None
    if column[:6] in ['x2008_', 'x2012_']:
        return column[6:]
    return column

def get_varyears_2008(df, variable):
    years = []
    if 'x2008_' + variable in list(df):
        years.append(2008)
    if 'x2012_' + variable in list(df):
        years.append(2012)

    if years:
        return years
    else:
        return None

def get_datarows_2008(df, variable, year):
    yearcolumn = "x%d_%s" % (year, variable)
    if yearcolumn in list(df):
        return df[yearcolumn]

    return df[variable]

def column2variable_2016(column):
    if column[-5:] in ['_2012', '_2016']:
        return column[:-5]
    return column

def get_varyears_2016(df, variable):
    years = []
    if variable + '_2012' in list(df):
        years.append(2012)
    if variable + '_2016'  in list(df):
        years.append(2016)

    if years:
        return years
    else:
        return None

def get_datarows_2016(df, variable, year):
    yearcolumn = "%s_%d" % (variable, year)
    if yearcolumn in list(df):
        return df[yearcolumn]

    return df[variable]

def load():
    x20082012 = database.MatrixCSVDatabase(database.localpath("election/2008-2012.csv"), 'FIPS',
                                           database.variable_filtermap(column2variable_2008), get_varyears_2008, get_datarows_2008)

    x20122016 = database.MatrixCSVDatabase(database.localpath("election/US_County_Level_Presidential_Results_12-16.csv"), 'combined_fips',
                                           database.variable_filtermap(column2variable_2016), get_varyears_2016, get_datarows_2016)

    return database.CombinedDatabase([x20082012, x20122016], ['x20082012', 'x20122016'], '.')

if __name__ == '__main__':
    db = load()
    print db.get_variables()
    print db.get_data('x20082012.PCT_DEM', 2008)[-10:]
    print db.get_data('x20082012.PCT_DEM', 2012)[-10:]
    print db.get_data('x20122016.per_dem', 2012)[-10:]
    print db.get_data('x20122016.per_dem', 2016)[-10:]