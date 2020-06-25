# Parse population python module
__author__ = 'Jose Cubero'
__version__ = '1.0.0'

#import os.path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

debug_lib = False

# def get_region_country_dict():

#     dictX = {}
#     grouped_data = world_population_df.groupby(by= "UN_Region")
    
#     # Find countries with more infections, per region
#     for region, dfx in grouped_data:

#         dictX[region] = dfx.index.tolist()
    
#     return dictX

def get_region_list():

    UN_region_list = ["Northern America",
                "Central America",
                "Caribbean",
                "South America",
                "Northern Europe",
                "Western Europe",
                "Southern Europe",
                "Eastern Europe",
                "Northern Africa",
                "Western Africa",
                "Eastern Africa",
                "Middle Africa",
                "Southern Africa",
                "Western Asia",
                "Central Asia",
                "Eastern Asia",
                "Southern Asia",
                "South-eastern Asia",
                "Australia and New Zealand",
                "Melanesia",
            ]    
    return UN_region_list

def get_world_pop(country_list=None):
    file_worldpop = './input/world_pop_wikipedia.csv'
    # fields: Country_Area,Continent,UN_Region,Population_2018,Population_2019,Change

    df = pd.read_csv(file_worldpop)
    df = df.loc[:,['Country_Area', 'Continent', 'UN_Region', 'Population_2019']]
    df = df.rename(columns={'Country_Area': 'Country'}).set_index('Country')

    cat_reg_type = pd.CategoricalDtype(categories=(get_region_list()), ordered=True)

    df['UN_Region'] = df['UN_Region'].astype(cat_reg_type)
    #df['Continent'] = df['Continent'].astype(cat_type)

    if (debug_lib):
        df.sort_index().to_csv('./tmp/clean_world_pop_all.csv', columns=[], header=False)

    if (country_list != None):
        df = df.loc[ country_list, :]
    return df



