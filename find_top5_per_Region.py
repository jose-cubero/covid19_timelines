# Parse population python module
__author__ = 'Jose Cubero'
__version__ = '1.0.0'

# import os.path
# import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# local libs
import pandas_main as covid_data

# Load data into the DFs
cases_net_df     = covid_data.world_confirmed_df
deaths_net_df    = covid_data.world_deaths_df
recovered_net_df = covid_data.world_recovered_df
population_df    = covid_data.world_confirmed_df

cases_norm_df    = cases_net_df.div(population_df['Population_2019'], axis=0) * 1000 # (per 1000)
# drops countries without data..
cases_norm_df.dropna(inplace=True)

cases_delta_df   = cases_net_df.diff(axis=1).rolling(axis=1, window=8).mean()
# TODO: apply a moving average to smooth the curve
death_rate_df    = (deaths_net_df / cases_net_df).rolling(axis=1, window=8).mean() *100

# Join region information as first column.
#cases_norm_df = population_df.loc[: , ["UN_Region"]].join(cases_norm_df, how='inner')

cases_net_df = pd.merge(population_df.loc[: , ["UN_Region"]], cases_net_df, left_index=True, right_index=True, how='inner')

region_list = ["Northern America",
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

cat_type = pd.CategoricalDtype(categories=region_list, ordered=True)

#cases_norm_df['UN_Region'] = cases_norm_df['UN_Region'].astype('category')
cases_net_df['UN_Region'] = cases_net_df['UN_Region'].astype(cat_type)
#pd.set_option("display.max_columns", 101)
#print(cases_norm_df['UN_Region'].unique())

grouped_data = cases_net_df.groupby("UN_Region")
# print(a_group)
# for name, group in a_group:
#  	print(name)
#  	print(group)
# 	print("\n")

# Find countries with more infections, per region
for region, dfx in grouped_data:
    print("********" + region + "********")
    # my_list= dfx.nlargest(5, columns=dfx.columns[-1], keep='all')
    my_list= dfx
    print(my_list)
    print(my_list.iloc[:,-1])
    my_list = my_list.iloc[:,1:].div(population_df['Population_2019'], axis=0) * 1000 # (per 1000)
    my_list.dropna(inplace=True)
    (my_list.iloc[:, 1:]).T.plot(title=region)

    # TODO Create a row of totals
    print("total cases = ", dfx.iloc[:, -1].sum())


    print ("\n")

# my_list= cases_norm_df.nlargest(20, columns=cases_norm_df.columns[-1], keep='all')
#mylist = confirmed_df['Country'].astype(str).tolist()
# print(my_list)

plt.show()

exit(0)