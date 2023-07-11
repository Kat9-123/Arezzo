import matplotlib.pyplot as plt



def debug(x):
    print(x)


def create_plot(rows=2,sharex=True):
    fig, ax = plt.subplots(nrows=rows,sharex=True)

    return ax

#def add_colourbar(fig,img,ax):
 #   return
#    cb = fig.colorbar(img, ax=[ax], orientation='horizontal')






def show_plot():
    plt.show()