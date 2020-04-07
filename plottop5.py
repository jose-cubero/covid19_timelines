# Covid19 Plot top 5 countries
__author__ = "Jose Cubero"
__version__ = "0.2.0"

import argparse
import os.path
import csv
import matplotlib.pyplot as plt
import numpy as np
#from matplotlib import pyplot

def main(args):

    #filename = args.iFilePath
    filename = "./input/time_series_covid19_confirmed_global.csv"
    verbose = args.verbose
    country = 'Germany'

    with open(filename) as f:
        reader = csv.reader(f)
        header_row = next(reader)
        if verbose:
            print("Header row is:\n")
            print(header_row)
            print("\n")
        dailyCases = []
        #np.empty(len(header_row-4),dtype=int)

        for row in reader:
            if row[1] != country:
                continue
            else:
                if (row[0] != ''):
                    continue
                #print(len(row))
                dailyCases = row[4:]
                #print(dailyCases)
        
        num_points = len(dailyCases)

        if num_points == 0:
            print("Did not find any data points")
            exit(1)
        if verbose:
            print("Found " + str(num_points) + "data points")

        dailyCases = np.asarray(list(map(int, dailyCases)))

        # Plot Data
        if verbose:
            print("Data to plot:")
            print(dailyCases)
        fig = plt.figure(figsize = (10,6))
        plt.plot(dailyCases, 'bo')
        #plt.yscale('linear')
        
        # Format Plot
        #plt.yscale('symlog', linthreshy=0.01)
        title = f'Daily Confirmed Cases in {country}'
        #plt.title(title, fontsize = 16)
        plt.title(title)
        #plt.xlabel('date',fontsize = 8)
        plt.ylabel("Cases (#)", fontsize = 8)
        #plt.tick_params(axis = 'both', which = 'major' , labelsize = 8)
        plt.savefig('output/sample.png')
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

    # Add the arguments
    # my_parser.add_argument('iFilePath',
    #     metavar='inputFilePath',
    #     type=str,
    #     #required=True,
    #     #action='store',
    #     help='the path to existing input file')
    
    # my_parser.add_argument('oFilePath',
    #     metavar='outputFilePath',
    #     type=str,
    #     #required=True,
    #     #action='store',
    #     #default="output.txt",
    #     help='the path to new output file')
    
    my_parser.add_argument('-v',
        '--verbose',
        action='store_true')
    
    # Specify output of "--version"
    my_parser.add_argument('-vn',
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

#Run Argument parser
args = my_parser.parse_args()
if args.verbose:
    print("Arguments:\n")
    print(vars(args))
    print("\n")

# # Check input file
# if os.path.isfile(args.iFilePath):
#     print ("Input file exist")
# else:
#     print ("Input file does not exist")

#Run Mian
main(args)
exit(0)