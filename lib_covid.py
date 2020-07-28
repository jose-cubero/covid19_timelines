# Plot COVID-19  
__author__ = 'Jose Cubero'
__version__ = '1.0.0'

# python libs
import argparse
import pandas as pd
import matplotlib.pyplot as plt

# local libs
import lib_world_pop as lwp

debug_lib = True

def get_clean_covid_data(data_set, country_list=None):

    valid_names = {'confirmed', 'deaths', 'recovered'}
    if (data_set not in valid_names):
        print("error, data_set" + data_set + "does not exist")
        exit(5)

    file_name = './data/JHU/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_' + data_set + '_global.csv'
    df = pd.read_csv(file_name, parse_dates=True)
    df = df.drop(columns= ['Lat','Long'])

    # Clean data s1: For simplicity, data from "overseas territories" will not be used. 
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

    # Clean data s2: Drop following entries:
    # * Diamond Princess
    # * MS Zaandam
    df = df[ ~(df['Country/Region'].isin(['Diamond Princess', 'MS Zaandam']) )]
    # using drop
    # df.drop( df[ df['Country/Region'].isin(['Diamond Princess', 'MS Zaandam']) ].index, axis=0, inplace=True)

    # Clean data s3: merge multi-region countries
    df = df.drop(columns= ['Province/State'])
    df = df.rename(columns={'Country/Region': 'Country'})
    # df = df.groupby('Country', as_index=False).sum()
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

    if (debug_lib):
        df.sort_index().to_csv('./tmp/clean_covid.csv', columns=[], header=False)

    #Apply optional filters
    if (country_list != None):
        df = df.loc[ country_list, :]
    return df

# Internal objects
world_population_df = lwp.world_population_df
world_confirmed_df = get_clean_covid_data('confirmed')
world_deaths_df    = get_clean_covid_data('deaths')
world_recovered_df = get_clean_covid_data('recovered')
# TODO: create a proper python lib and hide the internal objects
# def check_country()

def create_flat_df(country_df):
    reg_df = pd.merge(world_population_df.loc[: , ["UN_Region"]], country_df, left_index=True, right_index=True, how='inner').groupby("UN_Region").sum()
    con_df = pd.merge(world_population_df.loc[: , ["Continent"]], country_df, left_index=True, right_index=True, how='inner').groupby("Continent").sum()
    merged_df = pd.concat([country_df, reg_df, con_df], axis=0)
    return merged_df

def create_primary(cg_dict = {}, filter_list =[]):

    # Var1: Confirmed cases
    conf      = create_flat_df(world_confirmed_df)

    # Var2: Confirmed deaths
    deaths    = create_flat_df(world_deaths_df)

    # Var3: Recovered deaths
    recovered    = create_flat_df(world_recovered_df)

    # Add custom groups
    if (cg_dict != {}):
        for cg in cg_dict:
            # for dfx in concat_list:
            #     dfx.loc[cg, :] = dfx.loc[ cg_dict[cg], :].sum(axis=0)
            conf.loc[cg, :] = conf.loc[ cg_dict[cg], :].sum(axis=0)
            deaths.loc[cg, :] = deaths.loc[ cg_dict[cg], :].sum(axis=0)
            recovered.loc[cg, :] = recovered.loc[ cg_dict[cg], :].sum(axis=0)

    # TODO: understand this behaviour!
    # # Apply filter
    # if (filter_list != []):
    #     for dfx in concat_list:
    #         dfx = dfx.loc[filter_list, :].dropna()
    #         print(dfx) # -> prints the subset df.

    # print(conf) -> prints the full df! (the append using loc worked, but overwriting to smaller df didnt.)
    # print(concat_list[0]) -> same as previous.
    # TODO: try with drop
    # TODO: understand references to objects in a list.

    if (filter_list != []):
        conf = conf.loc[filter_list, :]
        deaths = deaths.loc[filter_list, :]
        recovered = recovered.loc[filter_list, :]

    #AuxVar: Population for the custom list
    ext_world_pop = lwp.get_extended_world_pop(cg_dict, filter_list)

    #Var4: Confirmed cases norm
    conf_norm = (conf.div(ext_world_pop['Population_2019'], axis=0))*1000

    #Var5: Confirmed deaths norm
    deaths_norm = (deaths.div(ext_world_pop['Population_2019'], axis=0))*1000

    #Var6: conf norm delta (1 week smooth)
    conf_norm_delta = conf_norm.diff(axis=1).rolling(axis=1, window=7).mean()

    #Var7: death rate (1 week smooth)
    # Deaths per confirmed cases. (Mortality Rate %)
    #TODO: confirm rolling works
    death_rate = ((deaths / conf) *100).rolling(axis=1, window=7).mean()

    # Append al dfs (with multi-index? or with list?)
    concat_list = [conf, deaths, recovered, conf_norm, deaths_norm, conf_norm_delta, death_rate]
    key_list = ["Confirmed Cases", "Deaths", "Recovered", "Confirmed Cases Norm", "Deaths Norm", "Confirmed Cases Delta", "Deaths Rate"]

    primary = pd.concat(concat_list, keys=key_list, axis=0)

    if(debug_lib):
        primary.loc[(slice(None), "group1"), :].to_csv('./tmp/primary.csv', columns=[], header=False)

    # TRANSPOSE. (and convert the index to date_time)
    primary = primary.T
    primary.index.rename('Date', inplace=True)
    primary.index = pd.to_datetime(primary.index, format='%m/%d/%y', errors='coerce')
    # multi-columns are used as shown below
    # level 0: variable
    # level 1: country/region/continent    
    # Sample: 
    #          Confirmed Cases                          Total Deaths                        Recovered                         
    #          Mexico Northern Europe     Asia       Mexico Northern Europe   Asia    Mexico Northern Europe     Asia
    # 1/22/20      0               0      554            0               0     17         0               0       28
    # 1/23/20      0               0      653            0               0     18         0               0       30
    return primary

# def add_derived_vars(primary_df, cg_dict):

#     filter_list = primary_df.index.get_level_values(level=1).tolist()
#     print(filter_list)
#     ext_world_pop = lwp.get_extended_world_pop(cg_dict, filter_list)
#     print(ext_world_pop)
#     print(type(ext_world_pop))

#     #Var4: Confirmed cases norm
#     world_conf_norm = (world_confirmed_df.div(ext_world_pop['Population_2019'], axis=0))*1000
#     mega_conf_norm = create_flat_df(world_conf_norm)
# # TODO FIX this crap    mega_conf_norm = 

#     #Var4: Confirmed deaths norm
#     world_death_norm = (world_deaths_df.div(world_population_df['Population_2019'], axis=0))*1000
#     mega_death_norm = create_flat_df(world_death_norm)

#     #Var5: conf norm delta (1 week smooth)
#     world_conf_norm_delta = world_conf_norm.diff(axis=1).rolling(axis=1, window=7).mean()
#     mega_conf_norm_delta = create_flat_df(world_conf_norm_delta)

#     #Var6: death rate (1 week smooth)
#     # Deaths per confirmed cases. (Mortality Rate %)
#     #TODO: confirm rolling works
#     world_death_rate = ((world_deaths_df / world_confirmed_df) *100).rolling(axis=1, window=7).mean()
#     mega_death_rate = create_flat_df( world_death_rate )

#     concat_list = [mega_conf, mega_deaths, mega_death_norm, mega_conf_norm, mega_conf_norm_delta, mega_death_rate]
#     key_list = ["mega_conf", "mega_deaths", "mega_death_norm", "mega_conf_norm", "mega_conf_norm_delta", "mega_death_rate"]

# ##########

#     mega_all = pd.concat(concat_list, axis=0, keys=key_list)
#     mega_all.to_csv('./tmp/mega.csv', columns=[], header=False)

#     # # TRANSPOSE. (and convert the index to date_time)
#     mega_all = mega_all.T
#     mega_all.index.rename('Date', inplace=True)
#     mega_all.index = pd.to_datetime(mega_all.index, format='%m/%d/%y', errors='coerce')

#     return mega_all

# def plot_covid_6vars(country_list=[], region=""):

#     if (region != ""):
#         print("selected region: " + region)
#         country_list += lwp.UN_region_dict[region]
#         print(country_list)
        
#     country_list[:] = [x for x in country_list if x in world_confirmed_df.index]

#     if(country_list == []):
#         print("plot_covid_6vars: no valid country list..")
#         exit(1)

#     if(debug_lib):
#         print("Selected countries: ")
#         print(country_list)
#         print("\n")

#     # Filter World population info
#     # population_df = pcov.get_world_pop(country_list)
#     population_df = world_population_df.loc[ country_list, :]

#     ##### Fill in Covid-19 raw data frames
#     # confirmed_df = pcov.get_clean_covid_data('confirmed', country_list)
#     confirmed_df = world_confirmed_df.loc[ country_list, :]
#     # deaths_df    = pcov.get_clean_covid_data('deaths', country_list)
#     deaths_df = world_deaths_df.loc[ country_list, :]
#     #recovered_df = pcov.get_clean_covid_data('recovered', country_list)
#     recovered_df = world_recovered_df.loc[ country_list, :]

#     ##### Create derived Covid-19 data 
#     # Normalized confirmed cases (per 1000 inhabitants)
#     confirmed_norm_df = (confirmed_df.div(population_df['Population_2019'], axis=0))*1000
#     # Active cases, (per 1000 inhabitants)
#     active_norm_df = confirmed_df - recovered_df - deaths_df
#     active_norm_df = (active_norm_df.div(population_df['Population_2019'], axis=0))*1000
#     # Daily Increase of confirmed cases (per 1000 inhabitants, moving average)
#     # confirmed_delta_df = confirmed_df.diff(axis=1)
#     # confirmed_norm_delta_df = confirmed_norm_df.diff(axis=1)
#     confirmed_norm_delta_df = confirmed_norm_df.diff(axis=1).rolling(axis=1, window=8).mean()
#     # Deaths per confirmed cases. (Mortality Rate %)
#     death_rate_df = (deaths_df / confirmed_df) *100

#     #### Plotting the data 
#     fig, axs = plt.subplots(2, 3, sharex=True,
#                             figsize = (17,10),
#                             constrained_layout=True)
#                         #  gridspec_kw={'hspace': 0.15, 'wspace': 0.15},

#     # Plot the data-frames
#     confirmed_df.T.plot(ax=axs[0,0], title='Total Confirmed Cases')
#     confirmed_norm_df.T.plot(ax=axs[1,0], title='Confirmed Cases norm (per 1k inhabitants)')
    
#     active_norm_df.T.plot(ax=axs[0,1], title='Active Cases norm')
#     confirmed_norm_delta_df.T.plot(ax=axs[1,1], title='Daily New Confirmed norm, Smoothed')

#     deaths_df.T.plot(ax=axs[0,2], title='Total Deaths')
#     death_rate_df.T.plot(ax=axs[1,2], title='Death-rate (%) = Net Deaths / Net Cases')
    
#     return fig
