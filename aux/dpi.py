#dpi.py
import matplotlib.pyplot as plt
#%matplotlib inline

def plot(fs,dpi):
    fig, ax=plt.subplots(figsize=fs, dpi=dpi)
    ax.set_title("Figsize: {}, dpi: {}".format(fs,dpi))
    ax.plot([2,4,1,5], label="Label")
    ax.legend()

figsize=(2,2)
for i in range(1,4):
    plot(figsize, i*72)

dpi=72
for i in [2,4,6]:
    plot((i,i), dpi)

plt.show()