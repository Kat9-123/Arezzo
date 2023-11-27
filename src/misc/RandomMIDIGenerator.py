import librosa
from midiutil.MidiFile import MIDIFile
import random

NAME = "MONO-36-R.midi"

BEAT_COUNT = 2500


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


def generate_random_midi(lower,upper,randomDurations,notesPerOnset,beatCount=2500):





    midiFile = MIDIFile()

    track = 0
    time = 0
    channel = 0
    volume = 100

    midiFile.addTrackName(track, time, "Track")
    midiFile.addTempo(track, time, 120) 


    
    for i in range(BEAT_COUNT):
        duration = 1 if not randomDurations else durations[random.randint(0,len(durations)-1)]
        for note in range(notesPerOnset):
            
            volume = random.randint(0,127)
            midiFile.addNote(track, channel, random.randint(lower,upper-1), time, duration, volume)
        time += duration

    # write it to disk

    type = "MONO" if notesPerOnset == 1 else f"HOMO{notesPerOnset}"
    noteRange = upper - lower

    name = f"{type}-{noteRange}" + ("-R" if randomDurations else "")

    name += ".midi"


    with open(name, 'wb') as outf:
        midiFile.writeFile(outf)

# 60,72
# 48,84
# 21,109

#generate_random_midi(21,109,False,1)


#generate_random_midi(21,109,True,1)

generate_random_midi(21,109,True,4,beatCount=2500)

#generate_random_midi(60,72,True,2)
#generate_random_midi(48,84,True,2)
#generate_random_midi(21,109,True,2)


#generate_random_midi(60,72,True,4)
#generate_random_midi(48,84,True,4)
#generate_random_midi(21,109,True,4)
