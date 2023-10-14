import Main
import cui.CUI as CUI

import librosa
import matplotlib.pyplot as plt
import time

ax = None

SHOW_PLOT = True

def specshow(data,samplingRate:int, location:int, xType:str = None, yType:str = None,xLabel:str ="",yLabel:str = ""):
    """Uses Librosa specshow to display a two dimensional numpy array. See Librosa documentation for xType and yType."""

    if not SHOW_PLOT:
        return

   # if ax == None:
   #     raise Exception("Attempting specshow w/o a plot")

    img = librosa.display.specshow(data, sr = samplingRate, x_axis = xType,ax=ax[location],y_axis=yType)
    ax[location].set(xlabel=xLabel,ylabel=yLabel)



def create_plot(rows):
    "Initialise the matplotlib plot"
    global ax
    if not SHOW_PLOT:
        return
    fig, ax = plt.subplots(nrows=rows,sharex=True)
    #wm = plt.get_current_fig_manager()
    #wm.window.state('zoomed')



def onset(times,onset_env,onset_frames,location):
    if not SHOW_PLOT:
        return
    ax[location].plot(times, 2 + onset_env / onset_env.max(), alpha=0.8,
            color='r')
    


    

    ax[location].set(xlabel="", ylabel='Strength & Onsets', yticks=[])



def vLine(times, onset_frames,onset_env,location,colour):
    if not SHOW_PLOT:
        return

    ax[location].vlines(times[onset_frames], 0, onset_env.max(), color=colour, alpha=0.9,
       linestyle='dotted')
    





def save_plot(name):
    if not SHOW_PLOT:
        return
    
    
    path = f"screenshots\\{name}.png"
    CUI.diagnostic("Saving screenshot to",path)
    plt.savefig(path,dpi=1200)

def show_plot():
    if not SHOW_PLOT:
        return

    plt.show()