import pytest
from mortality import main

@pytest.fixture(scope="module")
def db():
    return main.load()

def test_load(db):
    print db.get_variables()
    print db.describe_variable('all.Crude Rate')
    print db.describe_variable('age.< 1 year.Crude Rate')

def test_units(db):
    for variable in db.get_variables():
        assert db.get_unit(variable) and db.get_unit(variable) != "unknown"

if __name__ == '__main__':
    mydb = db()
    for variable in mydb.get_variables():
        print variable, mydb.get_unit(variable)
