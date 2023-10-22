import Utils
import Graphing
import NoteGenerator
from ProcessedAudioData import ProcessedAudioData
import cui.CUI as CUI

import librosa
import scipy
import numpy as np
import scipy.stats





SPECTRUM_DB_CUTOFF = -50
CHROMA_CUTOFF = 0.2#0.9
ONSET_TEMPORAL_LAG = 0

TEMPO_BOUNDRY = 140

N_FFT = 2048*8#4096*
WINDOW_LENGTH = 2048*2
HOP_LENGTH=2048//4

samplingRate = 0




def frames_to_time(frames):
    return librosa.frames_to_time(frames,sr=samplingRate,hop_length=HOP_LENGTH)


def time_to_frames(time):
    return librosa.time_to_frames(time,sr=samplingRate,hop_length=HOP_LENGTH)


def process_audio(audioPath,tempoOverride=-1):
    """Takes the audio at the path and returns a spectrum, chroma classification, onsets, 
       estimated tempo and the duration of the file."""
    global samplingRate
    CUI.progress("Processing {}".format(audioPath),prefixNewline=False)

    y, samplingRate = librosa.load(audioPath)

    duration = librosa.get_duration(y=y, sr=samplingRate)


    stft = np.abs(librosa.stft(y,n_fft=N_FFT,win_length=WINDOW_LENGTH,hop_length=HOP_LENGTH))

    spectrum = __get_spectrum(stft,samplingRate)

    print(spectrum.shape)
    frameCount = spectrum.shape[1]

    chroma = __get_chroma(y,samplingRate)
    onsets = __get_onset(y,stft, samplingRate,frameCount)

    pointDuration = duration/frameCount


    if tempoOverride == -1:
        tempo = __get_tempo(y,samplingRate)
    else:
        tempo = tempoOverride
    
    CUI.diagnostic("Frame Count",frameCount)
    CUI.diagnostic("Duration",duration, "s")
    CUI.diagnostic("Frame Duration",pointDuration * 1000, "ms")
    CUI.diagnostic("Softest",spectrum.min(), "db")
    CUI.diagnostic("Loudest",spectrum.max(),"db")


   # onsetTimes = librosa.frames_to_time(onsets,sr=samplingRate,hop_length=HOP_LENGTH,n_fft=N_FFT)  * (120/60)
   # onsetTimes -= onsetTimes[0]

   # for i in onsetTimes:
   #     print(Utils.snap_to_beat(i))

    CUI.stop_spinner()

    processedAudioData = ProcessedAudioData(spectrum=spectrum,
                                            chroma=chroma,
                                            onsets=onsets,
                                            tempo=tempo,
                                            duration=duration,
                                            frameCount=frameCount,
                                            frameDuration=pointDuration,
                                            loudest=spectrum.max())



    return processedAudioData







def __get_spectrum(stft,samplingRate):

    spectrum = librosa.amplitude_to_db(stft)

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
    tempo, beats = librosa.beat.beat_track(y=y,sr=sampleRate)
    print(tempo)
    first_beat_time, last_beat_time = librosa.frames_to_time((beats[0],beats[-1]),sr=sampleRate,n_fft=N_FFT)

    print("Tempo 2:", 60/((last_beat_time-first_beat_time)/(len(beats)-1)))

    
    tempo =round(rawTempo[0])


    #tempo = (60/((last_beat_time-first_beat_time)/(len(beats)-1)))//1

    CUI.diagnostic("Est. Tempo",tempo, "bpm")
    #return tempo

    while tempo > TEMPO_BOUNDRY:
        tempo //= 2
    
    CUI.diagnostic("Corrected Tempo",tempo, "bpm")    

    return tempo



def __get_onset(y,stft,sampleRate,frameCount):

    D = stft
    D[D < SPECTRUM_DB_CUTOFF] = 0
    times = librosa.times_like(D,sr=sampleRate)
    onset_env = librosa.onset.onset_strength(y=y, sr=sampleRate)
    onset_frames = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sampleRate)
    Graphing.onset(times,onset_env,onset_frames,location=2)
    Graphing.vLine(times,onset_frames,onset_env,location=2,colour="b")

    onset_frames += ONSET_TEMPORAL_LAG
  ##  for x in range(len(onset_frames)):
    #    val = onset_frames[x] + ONSET_TEMPORAL_LAG
   #     if val < frameCount:
    #        onset_frames[x] = val

    
    Graphing.vLine(times,onset_frames,onset_env,location=2,colour="r")
    
    return onset_frames





