#!/bin/bash

wget https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv -P data/covid-19/JHU/
wget https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv -P data/covid-19/JHU/
wget https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv -P data/covid-19/JHU/

mv data/covid-19/JHU/time_series_covid19_recovered_global.csv.1 data/covid-19/JHU/time_series_covid19_recovered_global.csv
mv data/covid-19/JHU/time_series_covid19_deaths_global.csv.1 data/covid-19/JHU/time_series_covid19_deaths_global.csv
mv data/covid-19/JHU/time_series_covid19_confirmed_global.csv.1 data/covid-19/JHU/time_series_covid19_confirmed_global.csv

