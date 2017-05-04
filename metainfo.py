import yaml, re

class Metainfo(object):
    def describe_variable(self, variable):
        """Text description of a variable."""
        raise NotImplementedError()

    def get_unit(self, variable):
        """Canonical unit for variable."""
        raise NotImplementedError()

    def get_tags(self, variable):
        """Return a list of tags for each variable."""
        return NotImplementedError()

class UniformMetainfo(Metainfo):
    def __init__(self, description, unit):
        self.description = description
        self.unit = unit

    def describe_variable(self, variable):
        """Text description of a variable."""
        return self.description

    def get_unit(self, variable):
        """Canonical unit for variable."""
        return self.unit

class StoredMetainfo(Metainfo):
    VARFINDER = re.compile(r'^(?P<desc>[^\[]+)\s+(?P<unit>\[([^\]]+)\])')

    def __init__(self, catalog):
        self.catalog = catalog

    def describe_variable(self, variable):
        """Text description of a variable."""
        return self.catalog.get(variable, dict(description="Missing information")).get('description', None)

    def get_unit(self, variable):
        """Canonical unit for variable."""
        return self.catalog.get(variable, dict(unit="unknown")).get('unit', "unknown")

    @staticmethod
    def load(filepath):
        catalog = yaml.load(file(filepath, 'r'))
        for variable in catalog:
            catalog[variable] = StoredMetainfo.parse(catalog[variable])

        return StoredMetainfo(catalog)

    @staticmethod
    def parse(defn):
        matchstr = re.search(StoredMetainfo.VARFINDER, defn)
        if matchstr is None:
            return dict(description=clean(defn))
        return dict(description=matchstr.group('desc').strip(), unit=matchstr.group('unit').strip(' []'))

class FunctionalMetainfo(Metainfo):
    def __init__(self, get_description, get_unitstr):
        """
        get_description: get_description(variable) returns the description of that variable.
        """
        self.get_description = get_description
        self.get_unitstr = get_unitstr

    def describe_variable(self, variable):
        return self.get_description(variable)

    def get_unit(self, variable):
        return self.get_unitstr(variable)
