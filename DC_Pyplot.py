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

    ax1.axis("on")
    ax2.axis("on")
    ax3.axis("on")
    
    
    ax3.set_yticklabels([])
    #ax3.locator_params(axis="y", nbins=4)
    ax3.locator_params(axis="x", nbins=6)
    
    
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
    #plt.tight_layout(pad=0, h_pad=0, w_pad=0)


    #fig.subplots_adjust(hspace=0.01,wspace=0.1)
    
       
def clearplots():
    ax1.clear()        
    ax2.clear()
    ax3.clear()
    
    ax1.axis("off")
    ax2.axis("off")
    ax3.axis("off")
    
    
def histogram(ravel,mean,stdev,treslow,tresup,lb,ub):
    #     #Create histogram and determine treshold and plot
    ax3.hist(ravel,256,[0,256],color='C0')    
    count,bins =np.histogram(ravel,bins=256, density=False)
    
    lim=1.1*np.max(count)
    
    text="stat range: " + str(np.round(lb,0)) + "-" + str(np.round(ub,0))
    ax3.fill_between([lb,ub],[lim,lim], facecolor="none", hatch="//",alpha=0.5, edgecolor='gray', label=text)
 
    #ax3.plot([0,0],[0,lim],color="black",linewidth=1)  
    #ax3.plot([255,255],[0,lim],color="black",linewidth=1)
    
    
    text="mean: " + str(np.round(mean,0))
    ax3.plot([mean,mean],[0,lim],color="black",label=text)
 
    text="black $ " + str(treslow) +  " \sigma$: " + str(np.round(stdev*treslow,0))
    ax3.plot([mean-treslow*stdev,mean-treslow*stdev],[0,lim],color="green",label=text)
    
    text="white $" + str(tresup) +  " \sigma$: " + str(np.round(stdev*tresup,0))
    ax3.plot([mean+tresup*stdev,mean+tresup*stdev],[0,lim],color="red",label=text)
    
    ax3.legend(loc="upper left",fontsize=8)   
    
    ax3.set_xlabel("grayscale value", fontsize=10)
    ax3.set_ylabel("density", fontsize=10)

    ax3.set_ylim([0, lim])
    ax3.yaxis.set_ticks(np.linspace(0,lim, 4))
    
    ax3.set_xlim([0, 255])
    ax3.xaxis.set_ticks(np.arange(0,300, 50))
    
    asp =1024/1360 * np.diff(ax3.get_xlim())[0] / np.diff(ax3.get_ylim())[0]
    #asp =1024/1360 * np.diff([0, 255]) / np.diff(ax3.set_ylim())[0]
     
    
    ax3.set_aspect(asp)
    #ax3.set_aspect(1024/1360)
    
  
    
#Pyplot
fig= plt.figure(figsize = (10,4))
#fig= plt.figure()

gs1 = gridspec.GridSpec(1, 3)
#gs1.update(wspace=0.1, hspace=0.1)

ax1 = fig.add_subplot(gs1[0,0])
ax2 = fig.add_subplot(gs1[0,1])
ax3 = fig.add_subplot(gs1[0,2])

plt.tight_layout(pad=0.5, w_pad=1, h_pad=1.0)
#fig.subplots_adjust(hspace=0,wspace=1)
#plt.tight_layout(pad=0, h_pad=0, w_pad=0)
#plt.tight_layout()
#f, axs = plt.subplots(2,2,figsize=(2.5,5))



ax1.axis("off")
ax2.axis("off")
ax3.axis("off")


#plt.subplots(constrained_layout=True)

#plt.tight_layout()