# Parse population python module
__author__ = 'Jose Cubero'
__version__ = '1.0.0'

# import os.path
# import numpy as np
import pandas as pd
pd.options.plotting.backend = "plotly"
#import matplotlib.pyplot as plt

# local libs
# local libs
# from covid19_timelines.pd_parser import world_pop
from covid19_timelines.pd_parser import covid_JHU

# import lib_covid as lcovid
# import lib_world_pop as lwpop

# Load data into the DFs
cases_net_df     = covid_JHU.world_confirmed_df
# deaths_net_df    = lcovid.world_deaths_df
# recovered_net_df = lcovid.world_recovered_df
# population_df    = lwpop.get_world_pop()

# cases_norm_df    = cases_net_df.div(population_df['Population_2019'], axis=0) * 1000 # (per 1000)
# # drops countries without data..
# cases_norm_df.dropna(inplace=True)

# # applying a moving average (8 days) to smooth the curves
# cases_delta_df   = cases_net_df.diff(axis=1).rolling(axis=1, window=8).mean()
# death_rate_df    = (deaths_net_df / cases_net_df).rolling(axis=1, window=8).mean() *100

# # Join region information as first column.
# #cases_norm_df = population_df.loc[: , ["UN_Region"]].join(cases_norm_df, how='inner')

# cases_net_df = pd.merge(population_df.loc[: , ["UN_Region", "Continent"]], cases_net_df, left_index=True, right_index=True, how='inner')
# region_list = lwpop.get_region_list()
# cat_type = pd.CategoricalDtype(categories=region_list, ordered=True)

# #cases_norm_df['UN_Region'] = cases_norm_df['UN_Region'].astype('category')
# cases_net_df['UN_Region'] = cases_net_df['UN_Region'].astype(cat_type)
# #pd.set_option("display.max_columns", 101)
# #print(cases_norm_df['UN_Region'].unique())

# # grouped_data = cases_net_df.groupby("UN_Region")
# merged_data = cases_net_df.groupby("UN_Region").sum()
# print(a_group)
# for name, group in a_group:
#  	print(name)
#  	print(group)
# 	print("\n")

# Find countries with more infections, per region
# for region, dfx in grouped_data:
#     print("********" + region + "********")
    # my_list= dfx.nlargest(5, columns=dfx.columns[-1], keep='all')
    # my_list= dfx
    # print(my_list)
    # print(my_list.iloc[:,-1])
    # my_list = my_list.iloc[:,1:].div(population_df['Population_2019'], axis=0) * 1000 # (per 1000)
    # my_list.dropna(inplace=True)
    # (my_list.iloc[:, 1:]).T.plot(title=region)

    # # TODO Create a row of totals
    # print("total cases = ", dfx.iloc[:, -1].sum())

    #
    # pcovid.plot_covid_6vars(dfx.index.tolist())

    # print ("\n")


fig = cases_net_df.T.plot()


# my_list= cases_norm_df.nlargest(20, columns=cases_norm_df.columns[-1], keep='all')
#mylist = confirmed_df['Country'].astype(str).tolist()
# print(my_list)

fig.show()

exit(0)