import lib_covid as lc
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

def plot_multi_column(df_in, mask=False):
    rows = 2
    cols = len(mask)//2 + ( len(mask)%2 >0 )    # round up

    # fig = make_subplots(rows=rows, cols=cols)
    # fig = make_subplots(rows=rows, cols=cols)
    rowx=1
    colx=1

    df2 = df_in.loc[:, (slice("Confirmed Cases"), slice(None))]
    df2.columns = df2.columns.droplevel(level=0)
    print(df2)
#     exit()

    data = [ go.Scatter(
        x = df2.index,
        y = df2['Mexico'],
        name='collisions',
        # line = dict(
        # color = color1
        # )
        )
    ]

    fig = go.Figure(data=data)

    # for var, dfx in df_in.groupby(axis=1, level=0):
    #     dfx.columns = dfx.columns.droplevel(level=0)
    #     print(dfx)
    #     fig.add_trace(
    #         dfx,
    #         mode="lines",
    #         row=rowx, col=colx
    #     )
    #     if (colx < cols):
    #         colx = colx+1
    #     else:
    #         colx = colx+1
    #         rowx = rowx+1
    fig.show()