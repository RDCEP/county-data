import importlib

def all_modules():
    return ['USGS', 'acra', 'agriculture', 'ccimpacts', 'census', 'climate', 'crime', 'election', 'energy', 'ers', 'groundwater', 'labor', 'mortality', 'AHRF']

loaded_dbs = {}

def all_variables():
    for modname in all_modules():
        print(modname)
        
        if modname in loaded_dbs:
            db = loaded_dbs[modname]
        else:
            main = importlib.import_module("%s.main" % modname)
            db = main.load()
            loaded_dbs[modname] = db
        
        for variable in db.get_variables():
            yield db, modname, variable
