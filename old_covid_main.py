# Covid19 Plot confirmed cases of covid-19
__author__ = "Jose Cubero"
__version__ = "1.0.0"

#Standard library imports
import argparse
import os.path
import csv
import matplotlib.pyplot as plt
import numpy as np
#---import pandas as pd
from pandas import read_csv

#--- Project local imports
#---- import parse_population

def get_dict():
    file_worldpop = "./input/world_pop_wikipedia.csv"
    countryPop = read_csv(file_worldpop, index_col= "Country_Area")
    countryPop = countryPop["Population_2019"]
    # print (countryPop)
    # print (type(countryPop))  # <#pandas.core.series.Series'
    return countryPop

def main(args):

    dfile_confirmed = "./input/time_series_covid19_confirmed_global.csv"
    # dfile_deaths    = "./input/time_series_covid19_deaths_global.csv"
    # dfile_recovered = "./input/time_series_covid19_recovered_global.csv"
    verbose = args.verbose
    countryList = []
    plotDataDict = {}
    popDict = get_dict()
    #countryPop_dict = pd.read_csv("./input/population_per_country_wkipedia.csv")

    #1 Get the county list
    #1a. Single country, name given as argument
    if (args.country != None):
        countryList.append(args.country)
    #1b. Using list of countries
    else:
        with open(args.countrylist) as clf:
            countryList = [line.rstrip() for line in clf]

    if(args.verbose):
        print("Selected countries: ")
        print(countryList)
        print("\n")

    #TODO: read parameter for data to plot: --data [conf, death, rec, all] 
    with open(dfile_confirmed) as f:
        for country in countryList:
            f.seek(0,0)
            reader = csv.reader(f)
            header_row = next(reader)
            # if verbose:
            #     print("Header row is:\n")
            #     print(header_row)
            #     print("\n")
            dailyCases = np.zeros(len(header_row)-4,dtype=int)
            counter = int(0)

            for row in reader:
                if row[1] != country:
                    continue

                #special case 1, skip "overseas territories" of selected countries
                if (country == "Denmark" or
                    country == "France" or
                    country == "Netherlands" or
                    country == "United Kingdom"):
                    if (row[0] != ''):
                        continue

                #general case and special case 2 (countries shown as several sub-regions)
                dailyCases += np.asarray(list(map(int,row[4:])))
                counter+=1

            if counter == 0:
                print("Did not find any data for the country " + country)
                exit(1)

            plotDataDict[country] = dailyCases

            num_points = len(dailyCases)
            if verbose:
                print("Found " + str(counter) + " lines and " + str(num_points) +  " date records for the country: " + country)

            # Plot Data
            if verbose:
                print("Data to plot:")
                print(dailyCases)

    fig, axs = plt.subplots(2, 1, sharex=True,
                        gridspec_kw={'hspace': 0.3, 'wspace': 0.2},
                        figsize = (10,8))

    line_labels = []
    for x in plotDataDict:
        axs[0].plot(plotDataDict[x], label=x)
        axs[0].set_title('Confirmed cases (Netto)')
        line_labels.append(str(x))

        popx = popDict[x]
        if (args.verbose):
            print(str(x) + "'s population is: " + str(popx))
        plotdata_norm = [dailytotal*1000/popx for dailytotal in plotDataDict[x]]
        axs[1].plot(plotdata_norm, label=x)
        axs[1].set_title('Confirmed cases (per 1K inhabitants)')

    # Create the legend
    fig.legend( labels= line_labels,   # The labels for each line
        loc="upper left",   # Position of legend
        # borderaxespad=5,    # Small spacing around legend box
        title="Country Key"  # Title for the legend
        )

    # create space for the legend
    # topspace = 1- (0.05 * len(lines) + 0.07)
    # plt.subplots_adjust(top=topspace)
    plt.show()

    print("Finished succesfully!")
    #input("done, press enter to end")
    exit(0)

# Arg Parser. This is executed when run from the command line
if __name__ == "__main__":
    # Create the parser
    my_parser = argparse.ArgumentParser(prog='covid_main',
        #usage='%(prog)s -i input [-o output]',
        description='Read latest data and print top 5')

    my_parser.add_argument('-v',
        '--verbose',
        action='store_true')
    
    group = my_parser.add_mutually_exclusive_group(required=True)

    group.add_argument('-c',
        '--country',
        metavar='Country',
        type=str,
        action='store',
        help='Name of the desired country')
    
    group.add_argument('-cl',
        '--countrylist',
        metavar='PathToListFile',
        type=str,
        action='store',
        help='File containing a list of countries, one per line')

    # my_parser.add_argument('oFilePath',
    #     metavar='outputFilePath',
    #     type=str,
    #     #required=True,
    #     #action='store',
    #     #default="output.txt",
    #     help='the path to new output file')
    

#Run Argument parser
args = my_parser.parse_args()
if args.verbose:
    print("Arguments:\n")
    print(vars(args))
    print("\n")

#Run Mian
main(args)
exit(0)