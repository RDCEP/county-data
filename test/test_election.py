from election import main

def test_load():
    db = main.load()
    print db.get_variables()
    print db.get_data('x20082012.PCT_DEM', 2008)[-10:]
    print db.get_data('x20082012.PCT_DEM', 2012)[-10:]
    print db.get_data('x20122016.per_dem', 2012)[-10:]
    print db.get_data('x20122016.per_dem', 2016)[-10:]
