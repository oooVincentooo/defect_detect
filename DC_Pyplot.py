#import PyQt5

#from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
#from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar



from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FigureCanvas
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk as NavigationToolbar






# Implement the default Matplotlib key bindings.
#from matplotlib.backend_bases import key_press_handler
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np


        
def setplots():

    #ax1.axis("off")
    #ax2.axis("off")
    ax3.set_yticklabels([])
    
    
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['bottom'].set_visible(False)
    ax1.spines['left'].set_visible(False)
    
    
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['bottom'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    
    
    ax1.xaxis.set_ticks([])
    ax2.xaxis.set_ticks([])
    ax1.yaxis.set_ticks([])
    ax2.yaxis.set_ticks([])
    
       
def clearplots():
    ax1.clear()        
    ax2.clear()
    ax3.clear()
    
def histogram(ravel,mean,stdev,treslow,tresup):
    #     #Create histogram and determine treshold and plot
    ax3.hist(ravel,256,[0,256],color="gray")    
    count,bins =np.histogram(ravel,bins=256, density=False)
    
    text="mean: " + str(np.round(mean,0))
    ax3.plot([mean,mean],[0,1.1*np.max(count)],color="blue",label=text)
    
    text="black $ " + str(treslow) +  " \sigma$: " + str(np.round(stdev*treslow,0))
    ax3.plot([mean-treslow*stdev,mean-treslow*stdev],[0,1.1*np.max(count)],color="green",label=text)
    
    text="white $" + str(tresup) +  " \sigma$: " + str(np.round(stdev*tresup,0))
    ax3.plot([mean+tresup*stdev,mean+tresup*stdev],[0,1.1*np.max(count)],color="red",label=text)
    
    ax3.legend(loc="upper left")   
    
    ax3.set_xlabel("grayscale value")
    ax3.set_ylabel("density")

    asp =1024/1360 * np.diff(ax3.set_xlim())[0] / np.diff(ax3.get_ylim())[0]
    ax3.set_aspect(asp)


    
    
#Pyplot
fig= plt.figure(figsize = (8,2))

gs1 = gridspec.GridSpec(1, 3)
#gs1.update(wspace=0.1, hspace=0.1)

ax1 = fig.add_subplot(gs1[0,0])
ax2 = fig.add_subplot(gs1[0,1])
ax3 = fig.add_subplot(gs1[0,2])
#fig.subplots_adjust(hspace=0.05,wspace=0.05)
plt.tight_layout(pad=0.25)
#plt.tight_layout()
#f, axs = plt.subplots(2,2,figsize=(2.5,5))



ax1.axis("off")
ax2.axis("off")
ax3.axis("off")


#plt.subplots(constrained_layout=True)

#plt.tight_layout()