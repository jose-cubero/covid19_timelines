# Covid19 Plot confirmed cases of covid-19
__author__ = "Jose Cubero"
__version__ = "2.0.0"

#Standard library imports
import argparse
import os.path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#Project local imports
import parse_population

def main(args):

    countryList = []
    #TODO: add normalize parameter
    normalize = False
 
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

    ##### GET DATA for selected countries
    popDF = parse_population.get_world_pop()
    popDF = popDF.loc[countryList,'Population_2019']

    plotDataDF = parse_population.get_clean_covid_data('confirmed')
    plotDataDF = plotDataDF.loc[countryList,]

    ##### change to dict (temporary!!!)
    popDict = popDF.to_dict()
    plotDataDict = plotDataDF.T.to_dict()

    print(popDict)
    print(plotDataDict)

    ##### Print data
    fig = plt.figure(figsize = (10,6))

    #plt.plot(plotDataDict[country], 'bo')

    print(plotDataDict)

    ax = plt.subplot(111)
    for x in plotDataDict:
        if (normalize):
            popx = popDict[x]
            print("IMHEREEE")
            if (args.verbose):
                print("" + str(x) + "the population is" + str(popx))
            plotdata = [dailytotal*1000/popx for dailytotal in plotDataDict[x]]
        else:
            plotdata = plotDataDict[x]
        print(plotdata)
        lists = sorted(plotdata.items()) # sorted by key, return a list of tuples
        tx, ty = zip(*lists) # unpack a list of pairs into two tuples
        plt.plot(tx, ty, 'o', label=x)
        #exit(0)
        # plt.plot(plotDataDict[x], 'o', label=x)
        #plt.plot(plotdata, 'o', label=x)

    leg = plt.legend(fancybox=True)
    leg.get_frame().set_alpha(0.5)

    #plt.yscale('linear')
    
    # Format Plot
    #plt.yscale('symlog', linthreshy=0.01)
    title = f'Daily Confirmed Cases per 1K inhabitants'
    #plt.title(title, fontsize = 16)
    plt.title(title)
    #plt.xlabel('date',fontsize = 8)
    plt.ylabel("Cases (#)", fontsize = 8)
    #plt.tick_params(axis = 'both', which = 'major' , labelsize = 8)
    #TODO: use better name for output file
    #plt.savefig('output/sample.png')
    #ax = plt.gca()
    #ax.ticklabel_format(useOffset=False)
    #ax.set_aspect('equal', adjustable='box')
    #plt.draw()
    plt.show()

    print("Finished succesfully!")
    #input("done, press enter to end")
    exit(0)

# Arg Parser. This is executed when run from the command line
if __name__ == "__main__":
    # Create the parser
    my_parser = argparse.ArgumentParser(prog='plottop5',
        #usage='%(prog)s -i input [-o output]',
        description='Read latest data and print top 5')

    my_parser.add_argument('-v',
        '--verbose',
        action='store_true')
    
    # Specify output of "--version"
    my_parser.add_argument('-vn',
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    group = my_parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--foo', action='store_true')
    group.add_argument('--bar', action='store_false')

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