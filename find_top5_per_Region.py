# Parse population python module
__author__ = 'Jose Cubero'
__version__ = '1.0.0'

# import os.path
# import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def get_world_pop(country_list=None):
    file_worldpop = './input/world_pop_wikipedia.csv'
    # original fields: Country_Area,Continent,UN_Region,Population_2018,Population_2019,Change

    df = pd.read_csv(file_worldpop)
    # DEBUG
    # df.to_csv('./tmp/clean_world_pop_all.csv', columns=['Country_Area'], index=False, header=False)

    df = df.loc[:,['Country_Area', 'UN_Region', 'Population_2019']]
    if (country_list != None):
        df = df[df['Country_Area'].isin(country_list)]
    # DEBUG
    # df.sort_values('Country_Area').to_csv( './tmp/clean_world_pop_selected.csv', columns=['Country_Area'], index=False, header=False )

    df = df.rename(columns={'Country_Area': 'Country'}).set_index('Country')
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
    # df.drop(df[ (df['Country/Region'].isin(['Denmark', 'France', 'Netherlands', 'United Kingdom'])) &
    #              (df['Province/State'].notna()) ].index, axis=0, inplace=True)

    # Clean data s2: to be dropped:
    # * Diamond Princess
    # * MS Zaandam
    df = df[ ~(df['Country/Region'].isin(['Diamond Princess', 'MS Zaandam']) )]
    # using drop
    # df.drop( df[ df['Country/Region'].isin(['Diamond Princess', 'MS Zaandam']) ].index, axis=0, inplace=True)

    # Clean data s2: merge multi-region countries
    df = df.drop(columns= ['Province/State'])
    df = df.rename(columns={'Country/Region': 'Country'})
    df = df.groupby('Country').sum() # IMPLICIT INDEX CHANGE TO Country

    # Clean data s3: Modify some particular names...
    # to be fixed:    
    fix_these = {
        'US' : 'USA',
        'Korea, South' : 'South Korea',
        'Taiwan*' : 'Taiwan',
        'West Bank and Gaza' : 'Palestine'
    }

    df = df.rename(index=fix_these)
    # df.sort_index().to_csv('./tmp/clean_covid.csv', columns=[], header=False)
    return df

# Load data into the DFs
cases_net_df     = get_clean_covid_data('confirmed')
deaths_net_df    = get_clean_covid_data('deaths')
recovered_net_df = get_clean_covid_data('recovered')
population_df    = get_world_pop()

cases_norm_df    = cases_net_df.div(population_df['Population_2019'], axis=0) * 1000 # (per 1000)
cases_delta_df   = cases_net_df.diff(axis=1)
death_rate_df    = (deaths_net_df / cases_net_df) *100 # (%)

sample_print = cases_norm_df.loc[ ['Costa Rica'] , :].T
sample_print.plot(title='Death-rate (%) = Net Deaths / Net Cases')

# DataFrame.nsmallest(self, n, columns[, keep])

# GENERATE PLOTS
# Preparation: close matplotlib windows..
# plt.close('all')
# PLOT 5: Deaths per confirmed cases. (Death Rate)
# death_rate.T.plot(title='Death-rate (%) = Net Deaths / Net Cases')
# Plot
plt.show()

exit(0)