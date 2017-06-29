import pytest
from ccimpacts import main

@pytest.fixture(scope="module")
def db():
    return main.load()

def test_load(db):
    print db.get_variables()[:10]
    print db.describe_variable('totaldamage')
    print db.get_fips()[:10]
    print db.get_data('totaldamage', 2090)[:10]

def test_units(db):
    for variable in db.get_variables():
        assert db.get_unit(variable) and db.get_unit(variable) != "unknown"

if __name__ == '__main__':
    mydb = db()
    for variable in mydb.get_variables():
        print variable, mydb.get_unit(variable)

