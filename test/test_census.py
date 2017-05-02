from census import main

def test_load():
    census = main.load()
    print census.get_variables()
    print census.describe_variable('POP010210')
    print census.get_fips()[:10]
    print census.get_years('POP010210')
