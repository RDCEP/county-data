from groundwater import main

def test_load():
    gw = main.load()
    print gw.get_variables()
    print gw.get_data('drawdown0', 2010)[:10]
