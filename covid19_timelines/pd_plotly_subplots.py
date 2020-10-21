import pandas as pd
pd.options.plotting.backend = "plotly"

# Original backend.
# import matplotlib.pyplot as plt

# def plot_multi_column(df_in, mask=False):

#     grouped_data = df_in.groupby(axis=1, level=0)

#     for var, dfx in grouped_data:
#         dfx.columns = dfx.columns.droplevel(level=0)
#         print(dfx)
#         fig = dfx.plot(title=var)
#         fig.show()

from plotly.subplots import make_subplots
import plotly.graph_objs as go

from covid19_timelines.pd_parser import covid_JHU

def plot_multi_column(df1, df2, df3):

    fig = make_subplots(rows=2, cols=2)

    data1 = go.Scatter(
        x = df1.index,
        y = df1['Mexico']
        )
    

    data2 = go.Scatter(
        x = df2.index,
        y = df2['Mexico']
        )

    data3 = go.Scatter(
        x = df3.index,
        y = df3['Mexico']
        )

    fig.add_trace(
                  data1,
                  row=1, col=1
                )
    fig.add_trace(
                  data2,
                  row=1, col=2
                )
    fig.add_trace(
                  data3,
                  row=2, col=1
                )

    fig.show()

df1 = covid_JHU.world_confirmed_df
df2 = covid_JHU.world_deaths_df
df3 = covid_JHU.world_recovered_df
plot_multi_column(df1.T, df2.T, df3.T)

