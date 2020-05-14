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
    
    return df

def get_clean_covid_data(data_set):

    # TODO: add arg check for validity ['confirmed', 'deaths', 'recovered']
    file_name = './input/time_series_covid19_' + data_set + '_global.csv'
    df = pd.read_csv(file_name)
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
    ## df.drop(df[ (df['Country/Region'].isin(['Denmark', 'France', 'Netherlands', 'United Kingdom'])) &
    ##             (df['Province/State'].notna()) ].index, axis=0, inplace=True)

    # Clean data s4: to be dropped:
    # * Diamond Princess
    # * MS Zaandam
    df = df[ ~(df['Country/Region'].isin(['Diamond Princess', 'MS Zaandam']) )]
    # using drop
    # df.drop( df[ df['Country/Region'].isin(['Diamond Princess', 'MS Zaandam']) ].index, axis=0, inplace=True)

    # Clean data s2: merge multi-region countries
    df = df.drop(columns= ['Province/State'])
    df = df.groupby('Country/Region', as_index=False).sum()

    # Clean data s3: Modify some particular names...
    # to be fixed:    
    fix_these = {
        'US' : 'USA',
        'Korea, South' : 'South Korea',
        'Taiwan*' : 'Taiwan',
        'West Bank and Gaza' : 'Palestine'
    }

    for item in fix_these:
        df.loc[ df['Country/Region'] == item, 'Country/Region'] = fix_these[item]

    #df.to_csv(('./tmp/clean_' + data_set + '.csv'))
    df.sort_values('Country/Region').to_csv('./tmp/clean_covid.csv', columns=['Country/Region'], index=False, header=False)

    # print(df) #DEBUG

    return df

# Load data into the DFs
confirmed_df = get_clean_covid_data('confirmed')
deaths_df    = get_clean_covid_data('deaths')
recovered_df = get_clean_covid_data('recovered')

mylist = confirmed_df['Country/Region'].astype(str).tolist()
world_pop_df = get_world_pop(mylist)

# Print all 3 series for country_x
country_list = ['Germany', 'France', 'Spain', 'Italy']

# confirmed_x = confirmed_df[ confirmed_df['Country/Region'] == country_x ].T.reset_index()
confirmed_x = confirmed_df[ confirmed_df['Country/Region'].isin(country_list) ]
confirmed_x.set_index('Country/Region', inplace=True)
print(confirmed_x)
print(confirmed_x.columns)
print(confirmed_x.index)

confirmed_x.T.plot()

# plot_df = confirmed_x.iloc[: , 1: ]
# plot_df = confirmed_x.T

# print("AFTER \n\n\n")
# # print(plot_df.columns)
# print("AFTER \n\n\n")
# print(plot_df.index)
# #print(confirmed_x)
# Date format used in csv: 1/26/20

# Plot
# plt.close('all')
# plot_df.plot()

plt.show()
# exit(0)