import Utils
import Graphing
import NoteGenerator

import librosa
import numpy as np



samplingRate = 0

SPECTRUM_DB_CUTOFF = 5
CHROMA_CUTOFF = 0.9


pointCount = 0
pointDuration = 0


## Turns a path to an audio file into spectrum and chroma
def process_audio(audioPath):
    global samplingRate,pointDuration,pointCount
    Utils.debug("Processing {}...".format(audioPath))

    y, samplingRate = librosa.load(audioPath)

    duration = librosa.get_duration(y=y, sr=samplingRate)

    #print(duration/y.sha1])
    #print(round(duration * ))

    spectrum, pointCount = __get_spectrum(y,samplingRate)
    chroma = __get_chroma(y,samplingRate)
    onset = __get_onset(y, samplingRate)

    print(pointCount,duration/pointCount)
    pointDuration = duration/pointCount

    tempo = __get_tempo(y,samplingRate) //2 
    print(tempo)

    NoteGenerator.get_midi(spectrum,chroma,onset,tempo)

   # ax[3].set(xlabel="Time (seconds)",ylabel="Octave")
    #ax[3].set_yticks([0,1,2,3,4,5,6,7,8,9])






def __get_spectrum(y,samplingRate):
    X = librosa.stft(y)
    spectrum = librosa.amplitude_to_db(abs(X))


    spectrum[spectrum < SPECTRUM_DB_CUTOFF] = 0



    #print(librosa.hz_to_note(freqs[bin]))
    Graphing.specshow(spectrum,samplingRate,location=0,xType="s",yType="log")

    return (spectrum,spectrum.shape[1])
def __get_chroma(y, samplingRate):

    chroma = librosa.feature.chroma_cqt(y=y,sr=samplingRate)
    print(chroma.shape)

    chroma[chroma < CHROMA_CUTOFF] = 0


    Graphing.specshow(chroma,samplingRate,location=1,xType="s",yType="chroma",yLabel="Note")

    return chroma




def __get_tempo(y,sampleRate):
    """Estimate tempo"""
    onset_env = librosa.onset.onset_strength(y=y, sr=sampleRate)
    tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sampleRate)
    
    return round(tempo[0])

## Gets the onsets
def __get_onset(y,sampleRate):

    D = np.abs(librosa.stft(y))
    times = librosa.times_like(D,sr=sampleRate)
    onset_env = librosa.onset.onset_strength(y=y, sr=sampleRate)
    onset_frames = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sampleRate)

    Graphing.onset(times,onset_env,onset_frames,location=2)
    
    return onset_frames





