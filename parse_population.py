# Parse population python module
__author__ = "Jose Cubero"
__version__ = "1.0.0"

#import os.path
import numpy as np
import pandas as pd

def get_world_pop(country_list=None):
    file_worldpop = "./input/world_pop_wikipedia.csv"

    # fields: Country_Area,Continent,UN_Region,Population_2018,Population_2019,Change

    df = pd.read_csv(file_worldpop)
    df.to_csv("./tmp/clean_world_pop_all.csv", columns=['Country_Area'], index=False, header=False)

    df = df.loc[:,['Country_Area', 'UN_Region', 'Population_2019']]
    if (country_list != None):
        df = df[df['Country_Area'].isin(country_list)]
    df.to_csv("./tmp/clean_world_pop_selected.csv", columns=['Country_Area'], index=False, header=False)
    return df

def get_clean_covid_data(data_set):

    # TODO: add arg check for validity ['confirmed', 'deaths', 'recovered']
    file_name = "./input/time_series_covid19_" + data_set + "_global.csv"
    df = pd.read_csv(file_name)
    df = df.drop(columns= ['Lat','Long'])

    # Clean data s1: get rid of colony data :D ()
    # Applies for= "Denmark", "France", "Netherlands", "United Kingdom"
    df = df[ ~(df['Country/Region'].isin(['Denmark', 'France', 'Netherlands', 'United Kingdom'])) |
              (df['Province/State'].isna()) ]

    df = df.drop(columns= ['Province/State'])

    # Less efficient, drop..
    # df.drop(df[ (df['Country/Region'].isin(['Denmark', 'France', 'Netherlands', 'United Kingdom'])) &
    #             (df['Province/State'].notna()) ].index, axis=0, inplace=True)

    # Clean data s2: merge multi-region countries
    df = df.groupby('Country/Region').sum()

    # Clean data s3: Change some stupid names...
    # df.loc[df[['Country/Region'] == 'US'] , 'Country/Region'] = 'USA'

    #df.to_csv(("./tmp/clean_" + data_set + ".csv"))
    df.to_csv("./tmp/clean_covid.csv", columns=[], header=False)
    # print(df) #DEBUG

    return df

confirmed_df = get_clean_covid_data('confirmed')
deaths_df = get_clean_covid_data('deaths')
recovered_df = get_clean_covid_data('recovered')

mylist = recovered_df.index.astype(str).tolist()
#print(mylist)

get_world_pop(mylist)

# list(confirmed_df['Country/Region'])

# germany_all