# Parse population python module
__author__ = 'Jose Cubero'
__version__ = '1.0.0'

#import os.path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def get_world_pop(country_list=None):
    file_worldpop = './input/world_pop_wikipedia.csv'

    # fields: Country_Area,Continent,UN_Region,Population_2018,Population_2019,Change

    df = pd.read_csv(file_worldpop)
    df.to_csv('./tmp/clean_world_pop_all.csv', columns=['Country_Area'], index=False, header=False)

    df = df.loc[:,['Country_Area', 'UN_Region', 'Population_2019']]
    if (country_list != None):
        df = df[df['Country_Area'].isin(country_list)]
    # DEBUG
    df.sort_values('Country_Area').to_csv( './tmp/clean_world_pop_selected.csv', columns=['Country_Area'], index=False, header=False )

    df = df.rename(columns={'Country_Area': 'Country'}).set_index('Country')
    return df

def get_clean_covid_data(data_set):

    # TODO: add arg check for validity ['confirmed', 'deaths', 'recovered']
    file_name = './input/time_series_covid19_' + data_set + '_global.csv'
    df = pd.read_csv(file_name, parse_dates=True)
    # print(df)
    # exit(0)
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
    df.drop(df[ (df['Country/Region'].isin(['Denmark', 'France', 'Netherlands', 'United Kingdom'])) &
                 (df['Province/State'].notna()) ].index, axis=0, inplace=True)

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

    # print(df) #DEBUG
    df.sort_index().to_csv('./tmp/clean_covid.csv', columns=[], header=False)
    return df

# Preparation: close matplotlib windows..
plt.close('all')
# User args
# TODO: merge with command line args
country_list = ['Germany', 'France', 'Spain', 'Italy']

# Load data into the DFs
confirmed_df = get_clean_covid_data('confirmed')
deaths_df    = get_clean_covid_data('deaths')
recovered_df = get_clean_covid_data('recovered')
population_df = get_world_pop(country_list)

# DEBUG, get full dictionary to compare names..
#mylist = confirmed_df['Country'].astype(str).tolist()
#world_pop_df = get_world_pop(mylist)

# PLOT 1: Net confirmed cases
confirmed_net = confirmed_df.loc[ country_list , : ]
# TODO: remove # confirmed_net.set_index('Country', inplace=True)
# print("DF1: confirmed_net")
# print(confirmed_net)
# print("\n\n")
confirmed_net.T.plot(title='Confirmed Cases, Netto')

#PLOT 2: Normalized confirmed cases (per 100 inhabitants)
population_df = population_df.loc[ : , ['Population_2019'] ]
# print("DF2: population_df")
# print(population_df)
# print(population_df.dtypes)
# print("\n\n")
confirmed_pop = confirmed_net.div(population_df['Population_2019'], axis=0)
# print("DF3: confirmed_pop")
# print(confirmed_pop)
# print("\n\n")
confirmed_pop.T.plot(title='Confirmed Cases, per 1000 inhabitants')


#PLOT 3: Daily Increase of confirmed cases
daily_increase = confirmed_net.diff(axis=1)
# print(death_rate)
daily_increase.T.plot(title='Confirmed Cases, Daily Increase')

#PLOT 4: Net deaths
deaths_net = deaths_df.loc[ country_list , : ]
deaths_net.T.plot(title='Deaths, Netto')

#PLOT 5: Deaths per confirmed cases. (Death Rate)
death_rate = (deaths_net / confirmed_net) *100
death_rate.T.plot(title='Death-rate (%) = Net Deaths / Net Cases')

# DataFrame.nsmallest(self, n, columns[, keep])

# Plot
plt.show()
exit(0)