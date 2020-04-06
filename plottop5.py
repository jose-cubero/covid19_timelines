# Covid19 Plot top 5 countries
__author__ = "Jose Cubero"
__version__ = "0.1.0"

import argparse
import os.path
import csv
import matplotlib
from matplotlib import pyplot as plt



def main(args):

    filename = args.iFilePath

    with open(filename) as f:
        reader = csv.reader(f)
        header_row = next(reader)
        if args.verbose:
            print("Header row is:\n")
            print(header_row)
            print("\n")
        highs = []
        for row in reader:
            if row[8]=='':
                continue
            high = int(row[8],10)
            highs.append(high)  #appending high temperatures   
        
        #Plot Data
        fig = plt.figure(dpi = 128, figsize = (10,6))
        plt.plot(highs, c = 'red') #Line 1
        #Format Plot
        plt.title("Daily High Temperatures, 2018", fontsize = 24)
        plt.xlabel('',fontsize = 16)
        plt.ylabel("Temperature (F)", fontsize = 16)
        plt.tick_params(axis = 'both', which = 'major' , labelsize = 16)
        plt.savefig('foo.png')
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
    my_parser.add_argument('iFilePath',
        metavar='inputFilePath',
        type=str,
        #required=True,
        #action='store',
        help='the path to existing input file')
    
    # my_parser.add_argument('oFilePath',
    #     metavar='outputFilePath',
    #     type=str,
    #     #required=True,
    #     #action='store',
    #     #default="output.txt",
    #     help='the path to new output file')
    
<<<<<<< HEAD
    #Plot Data
    #fig = plt.figure(dpi = 128, figsize = (10,6))
    plt.figure(dpi = 128, figsize = (10,6))
    plt.plot(highs, c = 'red') #Line 1
    #Format Plot
    plt.title("Daily High Temperatures, 2018", fontsize = 24)
    plt.xlabel('',fontsize = 16)
    plt.ylabel("Temperature (F)", fontsize = 16)
    plt.tick_params(axis = 'both', which = 'major' , labelsize = 16)
    plt.savefig('foo.png')
    plt.show()

#input("done, press enter to end")
exizt(0)
=======
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

# Check input file
if os.path.isfile(args.iFilePath):
    print ("Input file exist")
else:
    print ("Input file does not exist")

#Run Mian
main(args)
>>>>>>> add_paseargs
