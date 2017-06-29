import database, metainfo
import re

metas = dict(state=dict(description="State Code"),
             county=dict(description="County Name"),
             fips=dict(description="County FIPS code"),
             pop2012=dict(description="County Population (in 2012)", unit="people"),
             yieldchange=dict(description="Agricultural Damage (4 major crops)", unit="%"),
             mortchange=dict(description="Mortality", unit="deaths per 100k"),
             energychange=dict(description="Energy Expenditures", unit="%"),
             laborlowchange=dict(description="Labor, Low-risk", unit="%"),
             laborhighchange=dict(description="Labor, High-risk", unit="%"),
             coastaldamage=dict(description="Coastal damage", unit="log10(% county income)"),
             crimepropertychange=dict(description="Property Crime", unit="%"),
             crimeviolentchange=dict(description="Violent Crime", unit="%"),
             totaldamage=dict(description="Total damages", unit="% county income"))
                
def load():
    filepath = database.localpath("ccimpacts/county_damage_mapping_data.csv")
    db = database.StaticCSVDatabase(filepath, 'fips', year=2090)
    db.set_metainfo(metainfo.StoredMetainfo(metas))
    return db
