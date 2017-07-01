import pytest
from labor import main

@pytest.fixture(scope="module")
def db():
    return main.load()

def test_load(db):
    allvars = db.get_variables()
    print sum([sum(db.get_data(var, 2002)) for var in allvars if var != 'fips'])

def test_units(db):
    for variable in db.get_variables():
        assert db.get_unit(variable) and db.get_unit(variable) != "unknown"

if __name__ == '__main__':
    mydb = db()
    for variable in mydb.get_variables():
        print variable, mydb.get_unit(variable)
    test_load(mydb)
    test_units(mydb)
