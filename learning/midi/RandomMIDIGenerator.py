import librosa
from midiutil.MidiFile import MIDIFile
import random

NAME = "MONO-36-R.midi"

BEAT_COUNT = 2500
NOTES_PER_ONSET = 1


durations = [
    2,
    1.75,
    1.5,
    1.25,
    1,
    0.75,
    0.5,
    0.25,


]


def generate_random_midi():





    midiFile = MIDIFile()

    track = 0
    time = 0
    channel = 0
    volume = 100

    midiFile.addTrackName(track, time, "Track")
    midiFile.addTempo(track, time, 120) 


    
    for i in range(BEAT_COUNT):
        duration = durations[random.randint(0,len(durations)-1)]
        for note in range(NOTES_PER_ONSET):
            
            # 60,72
            # 48,84
            # 21,109
            midiFile.addNote(track, channel, random.randint(0,88-1), time, duration, volume)
        time += duration

    # write it to disk

    midiPath = NAME


    with open(midiPath, 'wb') as outf:
        midiFile.writeFile(outf)



generate_random_midi()