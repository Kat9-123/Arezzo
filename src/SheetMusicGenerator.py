from midiutil.MidiFile import MIDIFile
import Main
import os
import subprocess
import time
import ui.UI as UI
import Utils

SAVE_AUDIO = True

def midi(notes,tempo):
    
    if not SAVE_AUDIO:
        return
    UI.progress("Generating MIDI")
    print(notes)
    earliestStartTime = __get_earliest_start_time(notes)

    # create your MIDI object
    mf = MIDIFile(len(notes))     # only 1 track
    track = 0   # the only track

    time = 0    # start at the beginning
    mf.addTrackName(track, time, "Track")
    mf.addTempo(track, time, tempo)

    # add some notes
    channel = 0
    volume = 100

    for note in notes:
        mf.addNote(0, channel, note.midi, note.start - earliestStartTime, note.duration, volume)

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
  

    Utils.sys_call(command)
    #os.system(f'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe "output\\sheet music\\{Main.outputName}.{Main.EXPORT_TYPE}"')





def __get_earliest_start_time(notes):
    earliest = 10_000

    for note in notes:
        if note.start < earliest:
            earliest = note.start
    return earliest