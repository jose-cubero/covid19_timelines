# Plot COVID-19  
__author__ = 'Jose Cubero'
__version__ = '1.0.0'

# python libs
import argparse
import pandas as pd
import matplotlib.pyplot as plt

# local libs
import lib_world_pop

debug_lib = True

def get_clean_covid_data(data_set, country_list=None):

    valid_names = {'confirmed', 'deaths', 'recovered'}
    if (data_set not in valid_names):
        print("error, data_set" + data_set + "does not exist")
        exit(5)

    # file_name = './input/time_series_covid19_' + data_set + '_global.csv'
    file_name = './data/JHU/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_' + data_set + '_global.csv'
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

world_population_df = lib_world_pop.world_population_df
world_confirmed_df = get_clean_covid_data('confirmed')
world_deaths_df    = get_clean_covid_data('deaths')
world_recovered_df = get_clean_covid_data('recovered')

# TODO: explore decorators?
# def check_country()

def plot_covid_6vars(country_list=[], region=""):

    if (region != ""):
        print("selected region: " + region)
        country_list += lib_world_pop.UN_region_dict[region]
        print(country_list)
        
    country_list[:] = [x for x in country_list if x in world_confirmed_df.index]

    if(country_list == []):
        print("plot_covid_6vars: no valid country list..")
        exit(1)

    if(debug_lib):
        print("Selected countries: ")
        print(country_list)
        print("\n")

    # Filter World population info
    # population_df = pcov.get_world_pop(country_list)
    population_df = world_population_df.loc[ country_list, :]

    ##### Fill in Covid-19 raw data frames
    # confirmed_df = pcov.get_clean_covid_data('confirmed', country_list)
    confirmed_df = world_confirmed_df.loc[ country_list, :]
    # deaths_df    = pcov.get_clean_covid_data('deaths', country_list)
    deaths_df = world_deaths_df.loc[ country_list, :]
    #recovered_df = pcov.get_clean_covid_data('recovered', country_list)
    recovered_df = world_recovered_df.loc[ country_list, :]

    ##### Create derived Covid-19 data 
    # Normalized confirmed cases (per 1000 inhabitants)
    confirmed_norm_df = (confirmed_df.div(population_df['Population_2019'], axis=0))*1000
    # Active cases, (per 1000 inhabitants)
    active_norm_df = confirmed_df - recovered_df - deaths_df
    active_norm_df = (active_norm_df.div(population_df['Population_2019'], axis=0))*1000
    # Daily Increase of confirmed cases (per 1000 inhabitants, moving average)
    # confirmed_delta_df = confirmed_df.diff(axis=1)
    # confirmed_norm_delta_df = confirmed_norm_df.diff(axis=1)
    confirmed_norm_delta_df = confirmed_norm_df.diff(axis=1).rolling(axis=1, window=8).mean()
    # Deaths per confirmed cases. (Mortality Rate %)
    death_rate_df = (deaths_df / confirmed_df) *100

    #### Plotting the data 
    fig, axs = plt.subplots(2, 3, sharex=True,
                            figsize = (17,10),
                            constrained_layout=True)
                        #  gridspec_kw={'hspace': 0.15, 'wspace': 0.15},

    # Plot the data-frames
    confirmed_df.T.plot(ax=axs[0,0], title='Total Confirmed Cases')
    confirmed_norm_df.T.plot(ax=axs[1,0], title='Confirmed Cases norm (per 1k inhabitants)')
    
    active_norm_df.T.plot(ax=axs[0,1], title='Active Cases norm')
    confirmed_norm_delta_df.T.plot(ax=axs[1,1], title='Daily New Confirmed norm, Smoothed')

    deaths_df.T.plot(ax=axs[0,2], title='Total Deaths')
    death_rate_df.T.plot(ax=axs[1,2], title='Death-rate (%) = Net Deaths / Net Cases')
    
    return fig
