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

def plot_multi_column(df_in, mask=False):
    rows = 2
    cols = len(mask)//2 + ( len(mask)%2 >0 )    # round up

    fig = make_subplots(rows=rows, cols=cols)
    rowx=1
    colx=1

    for var, dfx in df_in.groupby(axis=1, level=0):
        dfx.columns = dfx.columns.droplevel(level=0)
        print(dfx)
        fig.add_trace(
            dfx,
            mode="lines",
            row=rowx, col=colx
        )
        if (colx < cols):
            colx = colx+1
        else:
            colx = colx+1
            rowx = rowx+1
    fig.show()