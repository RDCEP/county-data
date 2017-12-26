import pytest
from census import main

@pytest.fixture(scope="module")
def db():
    return main.load()

def test_load(db):
    print db.get_variables()
    print db.describe_variable('POP010210')
    print db.get_fips()[:10]
    print db.get_years('POP010210')

def test_units(db):
    known = 0
    for variable in db.get_variables():
        if db.get_unit(variable) and db.get_unit(variable) != "unknown":
            known += 1

    assert known == len(db.get_variables()), "Units only known for %d < %d" % (known, len(db.get_variables()))

if __name__ == '__main__':
    mydb = db()
    for variable in mydb.get_variables():
        print variable, mydb.get_unit(variable)
