from midiutil.MidiFile import MIDIFile
import Main
import os
import subprocess
import time
import ui.UI as UI

SAVE_AUDIO = False

def midi(voices,tempo):
    
    if not SAVE_AUDIO:
        return
    UI.progress("Generating MIDI")
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

    midiPath = "output\\midi\\{}.mid".format(Main.outputName)
    UI.diagnostic("MIDI:",midiPath)
    with open(midiPath, 'wb') as outf:
        mf.writeFile(outf)


    musescore(midiPath)


def musescore(midiPath):
    UI.progress("Generating Sheet music")
    
    # Help
    command = 'src\\MusescoreCaller.bat "{}" "output\\sheet music\\{}.{}" "{}"'.format(Main.MUSECORE4_PATH,Main.outputName,Main.EXPORT_TYPE,midiPath)
    UI.diagnostic("MuseScore Call",command)

    os.system(command)





def __get_earliest_start_time(voices):
    earliest = 1000
    for voice in voices:
        for note in voice:
            if note.start < earliest:
                earliest = note.start
    return earliest