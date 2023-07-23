import Graphing
import AudioProcessor
import Note
import Main
import ui.UI as UI

import librosa
import numpy as np


#https://en.wikipedia.org/wiki/Chroma_feature
# {C, C♯, D, D♯, E , F, F♯, G, G♯, A, A♯, B} => chroma
# C4, A5, Db2 => note


TEMPO_BOUNDRY = 140

CHROMA = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]

LOWEST_OCTAVE_DB = 10

HARMONIC_OCTAVE_MAX_DIFFERENCE_DB = 2

def get_notes_voices(spectrum, chroma, onsets, rawTempo):
    """Takes in spectrum, chroma, onsets and tempo and returns all of the voices with their respective notes."""

    spectrumRowCache = __cache_note_to_spectrum_row()
    UI.diagnostic("Cached Spectrum Rows", str(spectrumRowCache))
    UI.diagnostic("Onsets", str(onsets))
    tempo = __fix_tempo(rawTempo)


    octaves = __get_octaves(spectrum,onsets)


    #start = onsets[0]
   # for x in range(len(onsets)):
    #    onsets[x] -= start

    voices = []


    for x,onset in enumerate(onsets):
        #octave = octaves[:,onset].argmax(axis=0)
        
        
        # Find doubled octaves



        start = onset * AudioProcessor.pointDuration * (tempo/60)

        if x == len(onsets) -1:
            duration = 4
        else:
            duration = (onsets[x+1]-onsets[x]) * AudioProcessor.pointDuration * (tempo/60)

        strongestChroma = np.argsort(chroma[:,onset])[::-1][:Main.voiceCount]
        for i in range(Main.voiceCount):
            voices.append([])

            octave = __get_octave(CHROMA[strongestChroma[i]],onset,spectrum,spectrumRowCache)
            note = Note.Note(CHROMA[strongestChroma[i]],octave,start,duration)

            voices[i].append(note)
        #note = Note()


        #print((onsets[x+1]-onsets[x]) * AudioProcessor.pointDuration * (tempo/60))
   # print(4)
    
    



    return (voices,tempo)


def __fix_tempo(rawTempo):
    """Correctly reduces tempo, based on TEMPO_BOUNDRY."""
    tempo = rawTempo

    while tempo > TEMPO_BOUNDRY:
        tempo //= 2
    
    UI.diagnostic("Corrected Tempo",tempo, "bpm")
    return tempo






def __cache_note_to_spectrum_row():
    freqs = np.arange(0, 1 + AudioProcessor.N_FFT / 2) * AudioProcessor.samplingRate / AudioProcessor.N_FFT
    cache = {}
    for x in range(1,len(freqs)):
        freq = freqs[x]
        cache[librosa.hz_to_note(freq,unicode=False)] = x

    return cache



def __get_octave(note,onset,spectrum,spectrumRowCache):
    strongest = -1000
    strongestI = -1
    for i in range(4,9):
        val = spectrum[spectrumRowCache[note + str(i)],onset]
        if val > strongest:
            strongest = val
            strongestI = i
       # print(val)
       # if val > LOWEST_OCTAVE_DB:
        #    return i

    if strongestI == -1:
        UI.warning("Octave not found!")
        return 0
    return strongestI
        #if val > strongest:
        #    strongest = val
        #   strongestI = i
        
    #return strongestI


def __get_octaves(spectrum,onsets):
    """Deprecated"""
    spectrum = spectrum.argmax(axis=0)
    freqs = np.arange(0, 1 + AudioProcessor.N_FFT / 2) * AudioProcessor.samplingRate / AudioProcessor.N_FFT
    print(freqs)
    octaves = np.zeros(shape=[10,AudioProcessor.pointCount])
    for x,i in enumerate(spectrum):
        if i == 0:
            continue
        octaves[int(librosa.hz_to_note(freqs[i])[-1:]),x] = 1
        #print()
    Graphing.specshow(octaves,AudioProcessor.samplingRate,location=3,xType="s",yLabel="Octave")


    return octaves
    bins = spectrum.argmax(axis=0)
    print(bins)
    freqs = np.arange(0, 1 + AudioProcessor.N_FFT / 2) * AudioProcessor.samplingRate / AudioProcessor.N_FFT
    

    arr = np.zeros(shape=[10,len(onsets)])
    for x,i in enumerate(bins):
        if i == 0:
            continue
        arr[int(librosa.hz_to_note(freqs[i])[-1:]),x] = 1
        #print()

    return arr
    #img = librosa.display.specshow(arr,ax=ax[3],x_axis="s")
   # 








def __harmonic_octave_detection():
    pass

def __get_key_signature():
    pass

def __get_time_signature():
    pass



def __process_info_at_onset():
    pass