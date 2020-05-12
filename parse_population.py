# Parse population python module
__author__ = "Jose Cubero"
__version__ = "1.0.0"

import os.path
from pandas import read_csv

countryPop_dict = {}

def init_dict():
    countryPop_dict = {}

def get_population_from(country):
    """return di.

    Args:
        filename (path-like object): The pathname of the file from which to
                                      load the pchip unit conversions.

    Returns:
        dict: A dictionary of the unit conversions.
    """
    unitconvs = {}
    data = collections.defaultdict(list)
    with open(filename) as pchip:
        csv_reader = csv.DictReader(pchip)
        for item in csv_reader:
            data[(int(item['uc_id']))].append((float(item['eng']),
                                               float(item['phy'])))
    # Create PchipUnitConv for each item and put in the dict
    for uc_id in data:
        eng = [x[0] for x in sorted(data[uc_id])]
        phy = [x[1] for x in sorted(data[uc_id])]
        u = units.PchipUnitConv(eng, phy, name=uc_id)
        unitconvs[uc_id] = u
    return unitconvs 