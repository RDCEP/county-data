import database, metainfo

infos = {'County': dict(description="Full county name and state abbr.", unit="none"),
         'County Code': dict(description="5 digit FIPS code", unit="none"),
         'Age Group Code': dict(description="Code for age group", unit="int"),
         'Notes': dict(description="Notes for given entry", unit="none"),
         'Deaths': dict(description="Deaths summed over 1999 - 2010", unit="people"),
         'Population': dict(description="Population summed over 1999 - 2010", unit="people"),
         'Crude Rate': dict(description="Average death rate", unit="deaths / 100k people")}

def load():
    allage = database.StaticCSVDatabase(database.localpath('mortality/cmf-1999-2010.txt'),
                                        'County Code', year=2004, sep='\t')
    allage.set_metainfo(metainfo.StoredMetainfo(infos))

    byage = database.InterlevedCSVDatabase(database.localpath("mortality/cmf-age-1999-2010.txt"),
                                           'County Code', 'Age Group', 2004, sep='\t')
    byage.set_metainfo(metainfo.StoredMetainfo(infos))
                                                 
    return database.CombinedDatabase([allage, byage], ['all', 'age'], '.')
