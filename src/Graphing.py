import Main


import librosa
import matplotlib.pyplot as plt
import time

ax = None

def specshow(data,samplingRate:int, location:int, xType:str = None, yType:str = None,xLabel:str ="",yLabel:str = ""):
    """Uses Librosa specshow to display a two dimensional numpy array. See Librosa documentation for xType and yType."""

   # if ax == None:
   #     raise Exception("Attempting specshow w/o a plot")

    img = librosa.display.specshow(data, sr = samplingRate, x_axis = xType,ax=ax[location],y_axis=yType)
    ax[location].set(xlabel=xLabel,ylabel=yLabel)



def create_plot(rows=2,sharex=True):
    global ax

    fig, ax = plt.subplots(nrows=rows,sharex=True)
    wm = plt.get_current_fig_manager()
    wm.window.state('zoomed')



def onset(times,onset_env,onset_frames,location):
    ax[location].plot(times, 2 + onset_env / onset_env.max(), alpha=0.8,
            color='r')
    

    ax[location].vlines(times[onset_frames], 0, onset_env.max(), color='g', alpha=0.9,
           linestyle='dotted')
    

    ax[location].set(xlabel="", ylabel='Strength & Onsets', yticks=[])



def save_plot():

    plt.savefig("screenshots\\{}_{}.png".format(str(int(time.time())),Main.AUDIO_TO_ANALYSE),dpi=1200)

def show_plot():

    plt.show()