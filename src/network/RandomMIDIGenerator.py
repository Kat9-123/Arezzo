"""Messy helper script that generate random midi files. Not connected to the project"""
from midiutil.MidiFile import MIDIFile
import random
import numpy as np

NAME = "MONO-36-R.midi"

BEAT_COUNT = 5000


durations = [
    2,
    1.75,
    1.5,
    1.25,
    1,
    0.75,
    0.5,
    0.25


]


def get_volume():
    return random.randint(5,127)

def get_note():
    note = (np.random.default_rng().normal(0,1.2) + 2.5)/5
    if note < 0 or note > 1:
        note = random.random()

    note = round(note * 87)

    return note + 21

def get_duration():
    return durations[random.randint(0,len(durations)-1)]  

def generate_random_midi(lower,upper,randomDurations,notesPerOnset,beatCount=2500):





    midiFile = MIDIFile(deinterleave=False)

    track = 0
    time = 0


    midiFile.addTrackName(track, time, "Track")
    midiFile.addTempo(track, time, 120) 





# 60,72
# 48,84
# 21,109

#generate_random_midi(21,109,False,1)

def write(name,file):
    with open(name, 'wb') as outf:
        file.writeFile(outf)

#generate_random_midi(21,109,True,1)
def mono(midiFile):
    time = 0
    while time < BEAT_COUNT:
        duration = get_duration()

        midiFile.addNote(0, 0, get_note(), time, duration, get_volume())
        time += duration
    write("MONO-FF.midi",midiFile)
    

def homo(midiFile):
    time = 0
    while time < BEAT_COUNT:
        duration = get_duration()
        for i in range(4):
            if random.random() < 0.06:
                continue

            midiFile.addNote(0, i, get_note(), time, duration, get_volume())
        time += duration

    write("HOMO-FF.midi",midiFile)

def poly(midiFile):

    for i in range(4):
        time = 0
        while time < BEAT_COUNT:
            duration = get_duration()
            
            if random.random() < 0.06:
                time += duration
                continue

            midiFile.addNote(0, i, get_note(), time, duration, get_volume())
            time += duration

    write("POLY-FF.midi",midiFile)


#generate_random_midi(60,72,True,2)
#generate_random_midi(48,84,True,2)
#generate_random_midi(21,109,True,2)


#generate_random_midi(60,72,True,4)
#generate_random_midi(48,84,True,4)
#generate_random_midi(21,109,True,4)
