#!/bin/bash

# wget https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv -P ./data/
# wget https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv -P ./data/
# wget https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv -P ./data/

# [ -f ./data/time_series_covid19_recovered_global.csv.1 ] && mv ./data/time_series_covid19_recovered_global.csv.1 ./data/time_series_covid19_recovered_global.csv
# [ -f ./data/time_series_covid19_deaths_global.csv.1 ] && mv ./data/time_series_covid19_deaths_global.csv.1 ./data/time_series_covid19_deaths_global.csv
# [ -f ./data/time_series_covid19_confirmed_global.csv.1 ] && mv ./data/time_series_covid19_confirmed_global.csv.1 ./data/time_series_covid19_confirmed_global.csv

## declare an array variable
JHU_url="https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/"
declare -a arr=("time_series_covid19_confirmed_global.csv"
                "time_series_covid19_deaths_global.csv"
                "time_series_covid19_recovered_global.csv")

cd data

## now loop through the above array
for i in "${arr[@]}"
do
    # Delete older file if existant
    [ -f $i ] && rm $i
    # Download the latest csv files
    wget ${JHU_url}$i
done

touch datestamp
echo $(date +%Y-%m-%d_%H%M) > datestamp
