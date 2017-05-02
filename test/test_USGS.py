from USGS import main

def test_load():
    weather = main.load()
    print weather.get_variables()
    print weather.get_years("IR_GW")
    print weather.get_data("IR_GW", 1990)[:10]
