#simpleplot.py
import matplotlib
import numpy as np
from matplotlib import pyplot as plt

mylist = ['16', '17', '27', '46', '48', '79', '130']
#data = [0, 0, 0, 0, 0, 1, 4, 4, 4, 5, 8, 10, 12, 12, 12, 12, 13, 13, 14, 14, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 17, 27, 46, 48, 79, 130, 159, 196, 262, 482, 670, 799, 1040, 1176, 1457, 1908, 2078, 3675, 4585, 5795, 7272, 9257, 12327, 15320, 19848, 22213, 24873, 29056, 32986, 37323, 43938, 50871, 57695, 62095, 66885, 71808, 77872, 84794, 91159, 96092, 100123, 103374]
# converting list to array 

intlist = list(map(int, mylist)) 
nparray1 = np.asarray(intlist) 

#nparray1 = np.array(list(map(int, mylist)))

# displaying list 
print ("mylist: ", mylist) 
print ("intlist: ", intlist) 
print ("nparray1: ", nparray1) 
  
# displaying array 
#print ("Array: ", arr) 

plt.plot(nparray1, 'ro')
plt.plot(intlist)
plt.show()