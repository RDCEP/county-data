from AHRF import main

def test_load():
    ahrf = main.load()
    print ahrf.get_variables()[:10]
    print ahrf.describe_variable('f0081176')
    print ahrf.get_fips()[:10]
    print ahrf.get_data('f0081176', 2010)[:10]
