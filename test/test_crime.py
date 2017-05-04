import pytest
from crime import main

@pytest.fixture(scope="module")
def db():
    return main.load()

def test_load(db):
    print db.get_variables()
    print db.describe_variable('violent')
    print db.get_fips()[:10]

    import numpy as np
    print np.nanmean(db.get_data('violent', 2005)), np.nanmean(db.get_data('property', 2005))

def test_units(db):
    known = 0
    for variable in db.get_variables():
        if db.get_unit(variable) and db.get_unit(variable) != "unknown":
            known += 1

    assert float(known) / len(db.get_variables()) > .1, "Units only known for %f%%" % (100 * float(known) / len(db.get_variables()))

if __name__ == '__main__':
    mydb = db()
    for variable in mydb.get_variables():
        print variable, mydb.get_unit(variable)
