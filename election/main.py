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
    if year:
        yearcolumn = "x%d_%s" % (int(year), variable)
        
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
    if year:
        yearcolumn = "%s_%d" % (variable, int(year))
        if yearcolumn in list(df):
            return df[yearcolumn]

    return df[variable]

def get_description(variable):
    known = dict(OBJECTID="Shapefile ID", AREA="County area", PERIMETER="County perimeter")
    return known.get(variable, None)

def get_unit(variable):
    known = dict(OBJECTID="name", DEM="votes", REP="votes", OTH="votes")
    return known.get(variable, None)

def load():
    metainfo = database.FunctionalMetainfo(get_description, get_unit)

    x20082012 = database.MatrixCSVDatabase(database.localpath("election/2008-2012.csv"), 'FIPS',
                                           database.variable_filtermap(column2variable_2008), get_varyears_2008, get_datarows_2008)
    x20082012.set_metainfo(metainfo)

    x20122016 = database.MatrixCSVDatabase(database.localpath("election/US_County_Level_Presidential_Results_12-16.csv"), 'combined_fips',
                                           database.variable_filtermap(column2variable_2016), get_varyears_2016, get_datarows_2016)
    x20122016.set_metainfo(metainfo)

    return database.CombinedDatabase([x20082012, x20122016], ['x20082012', 'x20122016'], '.')
