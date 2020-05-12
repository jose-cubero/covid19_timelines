# Parse population python module
__author__ = "Jose Cubero"
__version__ = "1.0.0"

#import os.path
from pandas import read_csv

#countryPop_dict = {}

def get_dict():
    

    # file_worldpop = "./input/population_per_country_wkipedia.csv"

    countryPop = read_csv("./input/population_per_country_wkipedia.csv", index_col= "Country_area")
    countryPop = countryPop["Population_2019"]
    print (countryPop)

    return countryPop

get_dict()