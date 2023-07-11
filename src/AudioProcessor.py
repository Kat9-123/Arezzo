import librosa
import matplotlib.pyplot as plt


# Turns a path to an audio file into spectrum and chroma
def process_audio():
    y, samplingRate = librosa.load()


def __get_spectrum(y,samplingRate):
    X = librosa.stft(y)
    Xdb = librosa.amplitude_to_db(abs(X))

    #plt.figure(figsize = (10, 5))
    Xdb[Xdb <= 15] = 0	
    img = librosa.display.specshow(Xdb, sr = samplingRate, x_axis = 'time', y_axis = 'hz')
    plt.colorbar()
    plt.show()

def __get_chroma(y, samplingRate):
    #librosa.filters.chroma(samplingRate,
    chromafb = librosa.feature.chroma_cqt(y=y,sr=samplingRate)

    #chromafb[chromafb <= 0.6] = 0

    fig, ax =  plt.subplots()
    img = librosa.display.specshow(chromafb, y_axis='chroma')
    ax.set(ylabel='Chroma filter', title='Chroma filter bank')
    fig.colorbar(img, ax=ax)
    plt.show()








