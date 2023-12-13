import misc.Graphing as Graphing
from core.ProcessedAudioData import ProcessedAudioData
import cui.CUI as CUI
from core.Configurator import CONFIG

import librosa
import numpy as np




ONSET_TEMPORAL_LAG = 3#4

TEMPO_BOUNDRY = 140

N_FFT = 2048*8#4096*
WINDOW_LENGTH = 2048*2
HOP_LENGTH=2048//4

samplingRate = 0




def frames_to_time(frames):
    return librosa.frames_to_time(frames,sr=samplingRate,hop_length=HOP_LENGTH)


def time_to_frames(time):
    return librosa.time_to_frames(time,sr=samplingRate,hop_length=HOP_LENGTH,n_fft=N_FFT)


def process_audio(audioPath,tempoOverride=-1):
    """Takes the audio at the path and returns a spectrum, chroma classification, onsets, 
       estimated tempo and the duration of the file."""
    global samplingRate
    Graphing.create_plot(rows=3)
    CUI.progress(f"Loading {audioPath}",spin=True)

    y, samplingRate = librosa.load(audioPath)
   # y *= 1.1

    CUI.progress("Processing audio",spin=True)

    duration = librosa.get_duration(y=y, sr=samplingRate)
    

    stft = np.abs(librosa.stft(y,n_fft=N_FFT,win_length=WINDOW_LENGTH,hop_length=HOP_LENGTH))

    



    spectrum = __get_spectrum(stft,samplingRate)

    
    frameCount = spectrum.shape[1]


    onsets = __get_onset(y,stft, samplingRate,frameCount)

    frameDuration = duration/frameCount


    tempo = __get_tempo(y,samplingRate)


    CUI.force_stop_progress()
    CUI.diagnostic("Tempo",tempo, "bpm")    
    CUI.diagnostic("Frame Count",frameCount)
    CUI.diagnostic("Duration",duration, "s")
    CUI.diagnostic("Frame Duration",frameDuration * 1000, "ms")
    CUI.diagnostic("Softest",spectrum.min(), "db")
    CUI.diagnostic("Loudest",spectrum.max(),"db")
    CUI.diagnostic("MEAN",spectrum.mean(), "db")



    origTempo = tempo
    if tempoOverride != -1:
        tempo = tempoOverride


    processedAudioData = ProcessedAudioData(spectrum=spectrum,
                                            onsets=onsets,
                                            tempo=tempo,
                                            duration=duration,
                                            frameCount=frameCount,
                                            frameDuration=frameDuration,
                                            loudest=spectrum.max(),
                                            origTempo=origTempo)



    return processedAudioData







def __get_spectrum(stft,samplingRate):

    spectrum = librosa.amplitude_to_db(stft)


    Graphing.specshow(spectrum,samplingRate,xType="s",yType="log")

    return spectrum




def __get_tempo(y,sampleRate):
    """Estimate tempo"""

    tempo, beats = librosa.beat.beat_track(y=y,sr=sampleRate)
    first_beat_time, last_beat_time = librosa.frames_to_time((beats[0],beats[-1]),sr=sampleRate,n_fft=N_FFT)

    tempoBeat = 60/((last_beat_time-first_beat_time)/(len(beats)-1))
    CUI.debug(f"Beat track tempo: {tempo}")
    CUI.debug(f"Delta tempo: {tempoBeat}")

    
    tempo = round(tempoBeat)



    
    #return tempo

    while tempo > TEMPO_BOUNDRY:
        tempo //= 2
    
    

    return tempo



def __get_onset(y,stft,sampleRate,frameCount):

    D = stft
    times = librosa.times_like(D,sr=sampleRate)
    onsetEnv = librosa.onset.onset_strength(y=y, sr=sampleRate)
    onsetFrames = librosa.onset.onset_detect(onset_envelope=onsetEnv, sr=sampleRate)


    Graphing.polygon(times,2 + onsetEnv / onsetEnv.max(),xLabel="",yLabel="Strength & Onsets")
    

    Graphing.vLines(times[onsetFrames],0,onsetEnv.max(),colour="b")



    for x in range(len(onsetFrames)):
        val = onsetFrames[x] + CONFIG["ADVANCED_OPTIONS"]["onset_frame_lag"]
        # Don't add lag if the result would be greater than the frame count
        if val >= frameCount:
            continue
        onsetFrames[x] = val

    Graphing.vLines(times[onsetFrames],0,onsetEnv.max(),colour="r")
    

    
    return onsetFrames





