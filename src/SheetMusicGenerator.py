from midiutil.MidiFile import MIDIFile
import Main


SAVE_AUDIO = True

def midi(voices,tempo):
    if not SAVE_AUDIO:
        return
    
    earliestStartTime = __get_earliest_start_time(voices)

    # create your MIDI object
    mf = MIDIFile(len(voices))     # only 1 track
    track = 0   # the only track

    time = 0    # start at the beginning
    mf.addTrackName(track, time, "Track")
    mf.addTempo(track, time, tempo)

    # add some notes
    channel = 0
    volume = 100
    for x,voice in enumerate(voices):
        for note in voice:
            mf.addNote(x, channel, note.midi, note.start -  earliestStartTime, note.duration, volume)

    # write it to disk

    with open("output/{}.mid".format(Main.outputName), 'wb') as outf:
        mf.writeFile(outf)




def __get_earliest_start_time(voices):
    earliest = 1000
    for voice in voices:
        for note in voice:
            if note.start < earliest:
                earliest = note.start
    return earliest