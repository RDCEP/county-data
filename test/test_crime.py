from crime import main

def test_load():
    crime = main.load()
    print crime.get_variables()
    print crime.describe_variable('violent')
    print crime.get_fips()[:10]

    import numpy as np
    print np.nanmean(crime.get_data('violent', 2005)), np.nanmean(crime.get_data('property', 2005))
