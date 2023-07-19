import librosa
import Utils
import numpy as np


SPECTRUM_DB_CUTOFF = 5
CHROMA_CUTOFF = 0.9

## Turns a path to an audio file into spectrum and chroma
def process_audio(audioPath):
    Utils.debug("Processing {}".format(audioPath))

    y, samplingRate = librosa.load(audioPath)

    ax = Utils.create_plot(rows=3)

    __get_spectrum(y,samplingRate,ax)
    __get_chroma(y,samplingRate,ax)
    Utils.debug(__get_pulse(y, samplingRate,ax))

    Utils.show_plot()


def __get_spectrum(y,samplingRate,ax):
    X = librosa.stft(y)
    Xdb = librosa.amplitude_to_db(abs(X))


    Xdb[Xdb < SPECTRUM_DB_CUTOFF] = 0	
    img = librosa.display.specshow(Xdb, sr = samplingRate, y_axis = 'log',ax=ax[0],x_axis="s")

    ax[0].set(xlabel="")

def __get_chroma(y, samplingRate,ax):
    #librosa.filters.chroma(samplingRate,
    chromafb = librosa.feature.chroma_cqt(y=y,sr=samplingRate)

    chromafb[chromafb < CHROMA_CUTOFF] = 0


    img = librosa.display.specshow(chromafb, y_axis='chroma',ax=ax[1],x_axis="s")
    #ax.set(ylabel='Chroma filter', title='Chroma filter bank')
    ax[1].set(xlabel="",ylabel="Note")


## Gets the onsets
def __get_pulse(y,sampleRate,ax):

    D = np.abs(librosa.stft(y))
    times = librosa.times_like(D,sr=sampleRate)
    onset_env = librosa.onset.onset_strength(y=y, sr=sampleRate)
    ax[2].plot(times, 2 + onset_env / onset_env.max(), alpha=0.8,
            label='Mean (mel)',color='r')
    onset_frames = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sampleRate)

    ax[2].vlines(times[onset_frames], 0, onset_env.max(), color='g', alpha=0.9,
           linestyle='dotted', label='Onsets')
    ax[2].set(ylabel='Strength & Onsets', yticks=[],xlabel="Time (seconds)")
    
    return onset_frames





