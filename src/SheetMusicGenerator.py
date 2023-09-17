from midiutil.MidiFile import MIDIFile
import Main
import os
import subprocess
import time
import ui.UI as UI
import Utils
import time

from Config import CONFIG



def generate_midi_file(notes,tempo,audioPath) -> None:
    """Takes a list of note objects, and a tempo and creates a MIDI file."""

    if not CONFIG["DEBUG"]["generate_sheet_music"]:
        return
    

    UI.progress("Generating MIDI")
    print(notes)


    outputName = f"{str(int(time.time()))}_{os.path.basename(audioPath)}"

    earliestStartTime = __get_earliest_start_time(notes)


    midiFile = MIDIFile(len(notes))

    track = 0
    time = 0
    channel = 0
    volume = 100

    midiFile.addTrackName(track, time, "Track")
    midiFile.addTempo(track, time, tempo)



    for note in notes:
        midiFile.addNote(track, channel, note.midi, note.start - earliestStartTime, note.duration, volume)

    # write it to disk

    midiPath = "output\\midi\\{}.mid".format(outputName)

    UI.diagnostic("MIDI:",midiPath)


    with open(midiPath, 'wb') as outf:
        midiFile.writeFile(outf)


    __generate_sheetmusic_musescore(midiPath)


def __generate_sheetmusic_musescore(midiPath: str) -> None:
    """Uses musescore to generate a pdf, given a midi file path."""
    UI.progress("Generating Sheet music")
    
    # Help
    command = f'src\\MusescoreCaller.bat "{Main.MUSECORE4_PATH}" "output\\sheet music\\{Main.outputName}.{Main.EXPORT_TYPE}" "{midiPath}"'
  

    Utils.sys_call(command)






def __get_earliest_start_time(notes) -> float:
    earliest = 10_000

    for note in notes:
        if note.start < earliest:
            earliest = note.start
    return earliest