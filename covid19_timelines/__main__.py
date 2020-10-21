# Plot COVID-19  
__author__ = 'Jose Cubero'
__version__ = '1.0.0'

# python libs
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# local libs
# from covid19_timelines.pd_parser import world_pop
from covid19_timelines.pd_parser import covid_JHU

def main_func():
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
    
    group.add_argument('-r',
        '--region',
        metavar='Region',
        type=str,
        action='store',
        help='Desired "UN Region"')

    group.add_argument('-cl',
        '--country_list',
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

    # Run Argument parser
    args = my_parser.parse_args()

    if args.verbose:
        print("Argument parser done")
        print("Arguments:\n")
        print(vars(args))
        # debug_lib = True
        print("\n")
    
    my_country_list = []
    my_region = ""
    if (args.country != None):
        my_country_list.append(args.country)

    if (args.region != None):
        my_region = args.region      

    if (args.country_list != None):
        with open(args.country_list) as clf:
            my_country_list = [line.rstrip() for line in clf]

    # Preparation: close matplotlib windows..
    plt.close('all')
    # TODO: check if this would be a better approach
    # load_covid_world_data()

    #Run Main function (generates plots)
    covid_JHU.plot_covid_6vars(country_list=my_country_list, region=my_region)

    #Show the plots
    plt.show()



# This is executed when run from the command line
if __name__ == "__main__":
    main_func()

    #Exit, no errors
    exit(0)
