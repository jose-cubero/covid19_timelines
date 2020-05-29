# csvplot_covid19

## Python scripts

| Filename | Contents | Status | TODO |
| :------- | :------: | :----: | :---: |
| parse_population.py | contains helper functions (current main, plots 5 graphs (cases, cases_norm, cases_delta, deaths, death_rate, ) for the selected countries) | works  | keep existing helper functions, add new, delete main |
| find_top5_per_Region.py | identifies top 5 countries per UN region based on cases and prints each UN region in a separate graph  | works  | write a file with the country statistics (prepare input for next script?), remove redundant def of helpers |
| pandas_plot0.py | should be the Main script (pandas version of the plottop5) , contains args management | broken usage of dicts | improve dependencies |
| plottop5.py | Orginal with pyplot and subplot (no pandas) | broken | reset back to working version! |
| aux/sample1.py | shows usage of pandas .loc for data selection (series vs df) | works | nothing
| aux/simpleplot.py | basic pyplot example, no pandas | works | nothing
| aux/dpi.py | Shows usage of figsize and dpi for matplotlib.pyplot | Runs | nothing

## Data folders

### input
Time series summary (csse_covid_19_time_series)
This folder contains daily time series summary tables, including confirmed, deaths and recovered. All data are from the daily case report.

### ouput

- [csvplot_covid19](#csvplot_covid19)
  - [Python scripts](#python-scripts)
  - [Data folders](#data-folders)
    - [input](#input)
    - [ouput](#ouput)