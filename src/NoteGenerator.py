import Graphing
import AudioProcessor
import Note
import Main

import librosa
import numpy as np
from midiutil.MidiFile import MIDIFile


NOTES = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]


def get_midi(spectrum, chroma, onsets,tempo):
    """Takes in spectrum, chroma and onsets and returns a list of (pitch,duration) tuples, in the MIDI format"""


    octaves =__get_octaves(spectrum,onsets)
    print(chroma.shape)

    #start = onsets[0]
   # for x in range(len(onsets)):
    #    onsets[x] -= start


    notes = []
    for x,onset in enumerate(onsets):
        octave = octaves[:,onset].argmax(axis=0)
        note = NOTES[chroma[:,onset].argmax(axis=0)]

        start = onset * AudioProcessor.pointDuration * (tempo/60)

        if x == len(onsets) -1:
            duration = 4
        else:
            duration = (onsets[x+1]-onsets[x]) * AudioProcessor.pointDuration * (tempo/60)

        note = Note.Note(note,octave,start,duration)

        notes.append(note)
        #note = Note()


    MIDI(notes,tempo)

        #print((onsets[x+1]-onsets[x]) * AudioProcessor.pointDuration * (tempo/60))
   # print(4)
    
    



    return




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



def MIDI(notes,tempo):
    

    # create your MIDI object
    mf = MIDIFile(1)     # only 1 track
    track = 0   # the only track

    time = 0    # start at the beginning
    mf.addTrackName(track, time, "Sample Track")
    mf.addTempo(track, time, tempo)

    # add some notes
    channel = 0
    volume = 100

    for note in notes:
        mf.addNote(track, channel, note.midi, note.start, note.duration, volume)

    # write it to disk

    with open("output/{}.mid".format(Main.outputName), 'wb') as outf:
        mf.writeFile(outf)