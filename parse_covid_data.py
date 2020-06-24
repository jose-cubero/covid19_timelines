# Parse population python module
__author__ = 'Jose Cubero'
__version__ = '1.0.0'

#import os.path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

debug_lib = False

def get_world_pop(country_list=None):
    file_worldpop = './input/world_pop_wikipedia.csv'
    # fields: Country_Area,Continent,UN_Region,Population_2018,Population_2019,Change

    df = pd.read_csv(file_worldpop)
    df = df.loc[:,['Country_Area', 'Continent', 'UN_Region', 'Population_2019']]
    df = df.rename(columns={'Country_Area': 'Country'}).set_index('Country')

    # region_list = ["Northern America",
    #            "Central America",
    #            "Caribbean",
    #            "South America",
    #            "Northern Europe",
    #            "Western Europe",
    #            "Southern Europe",
    #            "Eastern Europe",
    #            "Northern Africa",
    #            "Western Africa",
    #            "Eastern Africa",
    #            "Middle Africa",
    #            "Southern Africa",
    #            "Western Asia",
    #            "Central Asia",
    #            "Eastern Asia",
    #            "Southern Asia",
    #            "South-eastern Asia",
    #            "Australia and New Zealand",
    #            "Melanesia",
    #         ]

    # cat_reg_type = pd.CategoricalDtype(categories=region_list, ordered=True)

    # df['UN_Region'] = df['UN_Region'].astype(cat_reg_type)
    # #df['Continent'] = df['Continent'].astype(cat_type)

    if (debug_lib):
        df.sort_index().to_csv('./tmp/clean_world_pop_all.csv', columns=[], header=False)

    if (country_list != None):
        df = df.loc[ country_list, :]
    return df

def get_clean_covid_data(data_set, country_list=None):

    valid_names = {'confirmed', 'deaths', 'recovered'}
    if (data_set not in valid_names):
        print("error, data_set" + data_set + "does not exist")
        exit(5)

    file_name = './input/time_series_covid19_' + data_set + '_global.csv'
    df = pd.read_csv(file_name, parse_dates=True)
    df = df.drop(columns= ['Lat','Long'])

    # Clean data s1: get rid of colony data :D ()
    # Applies for= 'Denmark', 'France', 'Netherlands', 'United Kingdom'
    # examples: Province/State,Country/Region,
    #   keep: ',Denmark,'
    #   drop: 'Greenland,Denmark,'
    #   keep: 'Beijing,China', Chongqing,China, ...

    df = df[ ~(df['Country/Region'].isin(['Denmark', 'France', 'Netherlands', 'United Kingdom'])) |
              (df['Province/State'].isna()) ]
    ## Less efficient, drop..
    # df.drop(df[ (df['Country/Region'].isin(['Denmark', 'France', 'Netherlands', 'United Kingdom'])) &
    #             (df['Province/State'].notna()) ].index, axis=0, inplace=True)

    # Clean data s4: to be dropped:
    # * Diamond Princess
    # * MS Zaandam
    df = df[ ~(df['Country/Region'].isin(['Diamond Princess', 'MS Zaandam']) )]
    # using drop
    # df.drop( df[ df['Country/Region'].isin(['Diamond Princess', 'MS Zaandam']) ].index, axis=0, inplace=True)

    # Clean data s2: merge multi-region countries
    df = df.drop(columns= ['Province/State'])
    df = df.rename(columns={'Country/Region': 'Country'})
    # df = df.groupby('Country', as_index=False).sum()
    df = df.groupby('Country').sum() # IMPLICIT INDE CHANGE TO Country

    # Clean data s3: Modify some particular names...
    # to be fixed:    
    fix_these = {
        'US' : 'USA',
        'Korea, South' : 'South Korea',
        'Taiwan*' : 'Taiwan',
        'West Bank and Gaza' : 'Palestine'
    }

    df = df.rename(index=fix_these)

    if (debug_lib):
        df.sort_index().to_csv('./tmp/clean_covid.csv', columns=[], header=False)

    if (country_list != None):
        df = df.loc[ country_list, :]

    return df

