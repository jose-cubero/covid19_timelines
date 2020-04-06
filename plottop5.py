import csv
import matplotlib
from matplotlib import pyplot as plt
filename = 'sample_input.csv'
with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)
    highs = []
    for row in reader:
        if row[8]=='':
            continue
        high = int(row[8],10)
        highs.append(high)  #appending high temperatures   
    
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