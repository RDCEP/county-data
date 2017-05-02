from acra import main

def test_load():
    db = main.load()
    print db.get_variables()
    print db.get_data('elevation.elevation', 2010)[:10]
    print db.describe_variable('elevation.elevation')
    print db.get_unit('elevation.elevation')
