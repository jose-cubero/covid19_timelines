# Parse population python module
__author__ = 'Jose Cubero'
__version__ = '1.0.0'

#import os.path
import pandas as pd

debug_lib = False

def get_continent_list():

    UN_continent_list = ["Americas",
                "Europe",
                "Africa",
                "Asia",
                "Oceania",
            ]
    
    return UN_continent_list

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

def get_country_list(region_list=[], continent_list=[]):

    df = world_population_df

    #Apply optional filters
    if(region_list!= []):
        df = df[ (df['UN_Region'].isin(region_list) )]
    elif(continent_list != []):
        df = df[ (df['Continent'].isin(continent_list) )]

    return df.index.tolist()


def get_world_pop(country_list=[], region_list=[], continent_list=[]):
    file_worldpop = './data/world_pop_wikipedia.csv'
    # fields: Country_Area,Continent,UN_Region,Population_2018,Population_2019,Change

    df = pd.read_csv(file_worldpop)
    df = df.loc[:,['Country_Area', 'Continent', 'UN_Region', 'Population_2019']]
    df = df.rename(columns={'Country_Area': 'Country'}).set_index('Country')

    cat_reg_type = pd.CategoricalDtype(categories=(get_region_list()), ordered=True)
    df['UN_Region'] = df['UN_Region'].astype(cat_reg_type)

    cat_cont_type = pd.CategoricalDtype(categories=(get_continent_list()), ordered=True)
    df['Continent'] = df['Continent'].astype(cat_cont_type)

    if (debug_lib):
        df.sort_index().to_csv('./tmp/clean_world_pop_all.csv', columns=[], header=False)

    #Apply optional filters
    if (country_list != []):
        df = df.loc[ country_list, :]
    elif(region_list!= []):
        df = df[ (df['UN_Region'].isin(region_list) )]
    elif(continent_list!= []):
        df = df[ (df['Continent'].isin(continent_list) )]
    return df


def get_extended_world_pop(cg_dict = {}, filter_list =[]):
    df0 = get_world_pop()
    df_country = df0.loc[:, ['Population_2019'] ].sort_index()
    df_region = df0.groupby('UN_Region').sum()
    df_continent = df0.groupby('Continent').sum()

    df_out = pd.concat([df_country, df_region, df_continent])

    if (debug_lib):
        df_out.sort_index().to_csv('./tmp/clean_world_pop_extended.csv', columns=[], header=False)

    # Add custom groups
    if (cg_dict != {}):
        for cg in cg_dict:
            df_out.loc[cg, :] = df_out.loc[ cg_dict[cg], :].sum(axis=0)

    #Apply optional filters
    if (filter_list != []):
        df_out = df_out.loc[filter_list, :]

    return df_out

# def get_region_country_dict():

#     dictX = {}
#     grouped_data = world_population_df.groupby(by= "UN_Region")
    
#     # Find countries with more infections, per region
#     for region, dfx in grouped_data:
#         dictX[region] = dfx.index.tolist()
#     return dictX

# world_population_df = get_world_pop()
# UN_region_dict = get_region_country_dict()

# TODO: create a proper lib, with read-only internal objects- getter/setter functions.