
import cui.CUI as CUI

import librosa
import matplotlib.pyplot as plt
from core.Configurator import CONFIG

plot = None



SPECTRUM = 0
ONSETS = 1

SIZE = 2

def specshow(data,samplingRate:int, xType:str = None, yType:str = None,xLabel:str ="",yLabel:str = ""):
    """Uses Librosa specshow to display a two dimensional numpy array. See Librosa documentation for xType and yType."""

    if not CONFIG["DEBUG"]["graphing"]:
        return

   # if ax == None:
   #     raise Exception("Attempting specshow w/o a plot")

    img = librosa.display.specshow(data, sr = samplingRate, x_axis = xType,ax=plot[SPECTRUM],y_axis=yType)
    plot[SPECTRUM].set(xlabel=xLabel,ylabel=yLabel)



def create_plot(rows):
    "Initialise the matplotlib plot"
    global plot
    if not CONFIG["DEBUG"]["graphing"]:
        return
    fig, plot = plt.subplots(nrows=SIZE,sharex=True)
    #wm = plt.get_current_fig_manager()
    #wm.window.state('zoomed')



def polygon(x,y,xLabel,yLabel):
    if not CONFIG["DEBUG"]["graphing"]:
        return
    plot[ONSETS].plot(x,y, alpha=0.8,
            color='r')
    

    plot[ONSETS].set(xlabel=xLabel, ylabel=yLabel, yticks=[])




    

    
def vLines(values,min,max,colour):
    if not CONFIG["DEBUG"]["graphing"]:
        return
    plot[ONSETS].vlines(values, min, max, color=colour, alpha=0.9,
       linestyle='dotted')


def save_plot(name):
    if not CONFIG["DEBUG"]["graphing"]:
        return
    
    
    path = f"screenshots\\{name}.png"
    CUI.diagnostic("Saving screenshot to",path)
    plt.savefig(path,dpi=1200)

def show_plot():
    if not CONFIG["DEBUG"]["graphing"]:
        return

    plt.show()