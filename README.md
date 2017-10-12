# county-data

Manager of arbitrary collected data on US counties.

This is a general system, for anyone who has county-level data and
wants to include joint analyses.  The subdirectories in this
repository contain county-level datasets and the logic for exposing
it.

# Installation

The county-data tool requires numpy, pandas, pyyaml, xlrd, and prompt_toolkit.

```
pip install numpy pandas pyyaml xlrd prompt_toolkit
```

# The export tool

The export tool allows variables to be extracted from the datasets,
merged with variables from other datasets, and exported into new
files.  You can run the export tool at the terminal with:
```
python export.py
```

This will then give you a prompt, which includes the following
commands (amongst others, in order of example usage):

 - `help`: Provide a list of commands or help on a particular command
   with `help [command]`.

 - `available`: List the datasets that are avaialable to load.

 - `load [dataset]`: Load a dataset and prepare it for additional processing.

 - `list`: List the variables that are available across all loaded datasets.

 - `add [variable]`: Add one of the available variables to the export file.

 - `export [filename]`: Create a new file with just the added variables.

 - `bye`: Exit.

# Adding new datasets

To include a new CSV file, do the following:

1. Create a new subdirectory and place the data files there.
2. Create an empty `__init__.py` file in that directory.
3. Create a file `main.py` in that directory and include the following:
```
import os
import database

def get_description(variable):
    return "Ask YOURNAME about %s." % variable

def load():
    datapath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "DATAFILE.csv")
    return database.CSVDatabase(datapath, 'FIPS', get_description)
```

Fill in `DATAFILE` with the filename, `FIPS` with the name of the FIPS
code column, and `YOURNAME` with your name.

Currently this returns no useful information about the variables in
the `get_description` function, but you are encouraged to add
variable-specific descriptions.
