#!/usr/bin/bash

DATA_LOCATION=/home/josec/sandbox/data/COVID-19/csse_covid_19_data/csse_covid_19_time_series/
cd $DATA_LOCATION
git pull
cd -

cp $DATA_LOCATION/time_series_covid19*global.csv .

exit

