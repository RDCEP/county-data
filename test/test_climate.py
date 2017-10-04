import pytest
from climate import main

@pytest.fixture(scope="module")
def db():
    return main.load()

def test_load(db):
    print db.get_variables()

if __name__ == '__main__':
    mydb = db()
    print mydb.get_variables()
