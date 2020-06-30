# csvplot_covid19

- [csvplot_covid19](#csvplot_covid19)
  - [Python sources](#python-sources)
  - [/data](#data)
  - [/input](#input)
  - [/ouput](#ouput)

## Python sources

| Filename | Contents | Status | TODO |
| :------- | :------: | :----: | :---: |
| lib_world_pop.py | Library providing world population data per country, UN-region and Continent. | Stable  | Add feature get_pop(continent, UN_region) |
| lib_covid.py | Main library including all analysis and plotting functions. Plots timeline for 6 figures: cumulative cases (netto and normalized), active cases (normalized), delta cumulative cases (normlaized), death count and death rate. | Stable  | plot regions/continent/country-lists as single sum data |
| covid_main.py | Main script, manages user arguments and parses the input file if used to identify the desired countries. For usage details see below | stable | improve input file parsing to support regions/continents and custom country lists |
| covid_world_stats.py | Analyses covid-19 data to identify the countries with the most critical statistics. Plots each UN region in a separate graph  | only basic function implemented | write a file with the country statistics (prepare input for next script?) |

## /data
world_pop: Data taken from Wikipedia: https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations).
JHU/COVID-19: local copy (subtree) of John Hopkins Covid-19 data. https://github.com/CSSEGISandData/COVID-19 master 

## /input
country-list: sample file showing how to select the countries/regions/continent to plot.

## /ouput
When using the option (--save_output / -so) a figure and text file is stored here.

