import Graphing
import AudioProcessor
import Note
import Main
import ui.UI as UI

import librosa
import numpy as np



TEMPO_BOUNDRY = 140

NOTES = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]


def get_notes_voices(spectrum, chroma, onsets,rawTempo):
    """Takes in spectrum, chroma and onsets and returns a list of (pitch,duration) tuples, in the MIDI format"""


    tempo = __fix_tempo(rawTempo)


    octaves =__get_octaves(spectrum,onsets)


    #start = onsets[0]
   # for x in range(len(onsets)):
    #    onsets[x] -= start

    voices = []


    for x,onset in enumerate(onsets):
        octave = octaves[:,onset].argmax(axis=0)
        
        



        start = onset * AudioProcessor.pointDuration * (tempo/60)

        if x == len(onsets) -1:
            duration = 4
        else:
            duration = (onsets[x+1]-onsets[x]) * AudioProcessor.pointDuration * (tempo/60)

        notes = np.argsort(chroma[:,onset])[::-1][:Main.voiceCount]
        for i in range(Main.voiceCount):
            voices.append([])

            
            note = Note.Note(NOTES[notes[i]],octave,start,duration)

            voices[i].append(note)
        #note = Note()


        #print((onsets[x+1]-onsets[x]) * AudioProcessor.pointDuration * (tempo/60))
   # print(4)
    
    



    return (voices,tempo)



def __fix_tempo(rawTempo):
    tempo = rawTempo

    while tempo > TEMPO_BOUNDRY:
        tempo //= 2
    
    UI.diagnostic("Corrected Tempo",tempo, "bpm")
    return tempo


def __get_octaves(spectrum,onsets):
    spectrum = spectrum.argmax(axis=0)
    freqs = np.arange(0, 1 + 2048 / 2) * AudioProcessor.samplingRate / 2048
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
    freqs = np.arange(0, 1 + 2048 / 2) * AudioProcessor.samplingRate / 2048
    

    arr = np.zeros(shape=[10,len(onsets)])
    for x,i in enumerate(bins):
        if i == 0:
            continue
        arr[int(librosa.hz_to_note(freqs[i])[-1:]),x] = 1
        #print()

    return arr
    #img = librosa.display.specshow(arr,ax=ax[3],x_axis="s")
   # 



def __get_notes(chroma,onsets):
    pass




def __get_key_signature():
    pass

def __get_time_signature():
    pass



