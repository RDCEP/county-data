from agriculture import main

def test_load():
    ag = main.load()
    print ag.get_variables()
