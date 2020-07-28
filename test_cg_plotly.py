# local libs
import lib_covid_nomidx as lc
import pandas as pd
pd.options.plotting.backend = "plotly"

import lib_world_pop as lwp
# import matplotlib.pyplot as plt

# mega_df = lc.create_mega_df() # has the desired structure.
# # Multi-column:
# # level-0 : var
# # level-1 : country/region/continent



# print(mega_df)


# plot_DF = mega_df.loc[:, (slice(None), country_list)]
# # plot_DF = mega_df.loc[:, (["mega_conf", "mega_deaths"], country_list)]




# print(lwp.get_mega_world_pop())

# print(lc.create_primary())

#full_df = lc.get_full_df(my_list)
# my_list = lwp.get_country_list(["Northern America"])
# my_list.append(["Northern America", "Asia"]

my_dict = {"group1": ["Mexico", "Argentina"],
           "group2": ["Germany", "France"]}

my_list = ["Mexico", "Northern Europe", "Asia", "group1", "group2"]

primary_df = lc.create_primary(my_dict, my_list)
# primary_df = lc.create_primary(my_dict, my_list)
print(primary_df)

key_list = ["Confirmed Cases", "Deaths", "Recovered", "Confirmed Cases Norm", "Deaths Norm", "Confirmed Cases Delta", "Deaths Rate"]

for keyx in key_list:
    print_DF = primary_df.loc[:,keyx]
    fig = print_DF.plot(title=keyx)
    fig.show()

# print_DF = primary_df.loc[:,"Confirmed Cases"]
# fig = print_DF.plot()
# fig.show()

exit(0)