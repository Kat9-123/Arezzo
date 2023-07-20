import Main

import matplotlib.pyplot as plt
import time




def debug(x):
    print(x)


def create_plot(rows=2,sharex=True):
    fig, ax = plt.subplots(nrows=rows,sharex=True)

    return ax

#def add_colourbar(fig,img,ax):
 #   return
#    cb = fig.colorbar(img, ax=[ax], orientation='horizontal')




def save_plot():
    plt.savefig("screenshots\\{}_{}.png".format(str(int(time.time())),Main.AUDIO_TO_ANALYSE))

def show_plot():
    plt.show()