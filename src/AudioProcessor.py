import Utils
import Graphing
import NoteGenerator
from ProcessedAudioData import ProcessedAudioData
import ui.UI as UI

import librosa
import scipy
import numpy as np
import scipy.stats





SPECTRUM_DB_CUTOFF = -50
CHROMA_CUTOFF = 0.2#0.9
ONSET_TEMPORAL_LAG = 0

TEMPO_BOUNDRY = 140

N_FFT = 2048#4096*4

samplingRate = 0




def network_process(audioPath):
    print("Starting audio network process")
    y, samplingRate = librosa.load(audioPath,offset=0,duration=50)

    spectrum = __get_spectrum(y,samplingRate)
    frameCount = spectrum.shape[1]
    rowCount = spectrum.shape[0]
    onsets = __get_onset(y, samplingRate,frameCount)

    return (spectrum,onsets,spectrum.shape)
    

def process_audio(audioPath):
    """Takes the audio at the path and returns a spectrum, chroma classification, onsets, 
       estimated tempo and the duration of the file."""
    global samplingRate
    UI.progress("Processing {}".format(audioPath),prefixNewline=False)

    y, samplingRate = librosa.load(audioPath)

    duration = librosa.get_duration(y=y, sr=samplingRate)


    spectrum = __get_spectrum(y,samplingRate)

    frameCount = spectrum.shape[1]

    chroma = __get_chroma(y,samplingRate)
    onsets = __get_onset(y, samplingRate,frameCount)

    pointDuration = duration/frameCount

    tempo = __get_tempo(y,samplingRate)
    
    UI.diagnostic("Frame Count",frameCount)
    UI.diagnostic("Duration",duration, "s")
    UI.diagnostic("Frame Duration",pointDuration * 1000, "ms")
    UI.diagnostic("Softest",spectrum.min(), "db")
    UI.diagnostic("Loudest",spectrum.max(),"db")



    UI.stop_spinner()

    processedAudioData = ProcessedAudioData(spectrum=spectrum,
                                            chroma=chroma,
                                            onsets=onsets,
                                            tempo=tempo,
                                            duration=duration,
                                            frameCount=frameCount,
                                            frameDuration=pointDuration,
                                            loudest=spectrum.max())



    return processedAudioData







def __get_spectrum(y,samplingRate):
    X = librosa.stft(y,n_fft=N_FFT)

    spectrum = librosa.amplitude_to_db(abs(X))

    #spectrum = np.minimum(spectrum,
    #                       librosa.decompose.nn_filter(spectrum,
    #                                                   aggregate=np.median,
     #                                                  metric='cosine'))

    #spectrum[spectrum < SPECTRUM_DB_CUTOFF] = 0


    Graphing.specshow(spectrum,samplingRate,location=0,xType="s",yType="log")

    return spectrum
def __get_chroma(y, samplingRate):

    chroma = librosa.feature.chroma_stft(y=y,sr=samplingRate)

    #chroma[chroma < CHROMA_CUTOFF] = 0
   # chroma = np.minimum(chroma,
   #                        librosa.decompose.nn_filter(chroma,
    #                                                   aggregate=np.median,
    #                                                   metric='cosine'))

    #chroma = scipy.ndimage.median_filter(chroma, size=(1, 9))

    Graphing.specshow(chroma,samplingRate,location=1,xType="s",yType="chroma",yLabel="Note")

    return chroma




def __get_tempo(y,sampleRate):
    """Estimate tempo"""
    onset_env = librosa.onset.onset_strength(y=y, sr=sampleRate)
    rawTempo = librosa.feature.tempo(onset_envelope=onset_env, sr=sampleRate)
    

    tempo = round(rawTempo[0])
    UI.diagnostic("Est. Tempo",tempo, "bpm")
    #return tempo

    while tempo > TEMPO_BOUNDRY:
        tempo //= 2
    
    UI.diagnostic("Corrected Tempo",tempo, "bpm")    

    return tempo




## Gets the onsets
def __get_onset(y,sampleRate,frameCount):

    D = np.abs(librosa.stft(y))
    D[D < SPECTRUM_DB_CUTOFF] = 0
    times = librosa.times_like(D,sr=sampleRate)
    onset_env = librosa.onset.onset_strength(y=y, sr=sampleRate)
    onset_frames = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sampleRate)
    Graphing.onset(times,onset_env,onset_frames,location=2)
    Graphing.vLine(times,onset_frames,onset_env,location=2,colour="b")


    for x in range(len(onset_frames)):
        val = onset_frames[x] + ONSET_TEMPORAL_LAG
        if val < frameCount:
            onset_frames[x] = val

    
    Graphing.vLine(times,onset_frames,onset_env,location=2,colour="r")
    
    return onset_frames





