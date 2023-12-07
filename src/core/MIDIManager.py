import pretty_midi
from midiutil.MidiFile import MIDIFile
import librosa


def get_midi(path):
    midi_data = pretty_midi.PrettyMIDI(path)
    allNotes = []
    for instrument in midi_data.instruments:
        allNotes += instrument.notes
    return allNotes


def write_midi(notes,tempo,path) -> None:
    """Takes a list of note objects, and a tempo and creates a MIDI file."""




    earliestStartTime = __get_earliest_start_time(notes)


    midiFile = MIDIFile(len(notes),deinterleave=False)

    track = 0
    time = 0
    channel = 0
    volume = 100

    midiFile.addTrackName(track, time, "Track")
    midiFile.addTempo(track, time, tempo)



    for note in notes:
        midi = librosa.note_to_midi(note.note)
        print(note.duration)
        midiFile.addNote(track, channel, midi, note.start - earliestStartTime, note.duration, volume)

    # write it to disk


    with open(path, 'wb') as outf:
        midiFile.writeFile(outf)

def __get_earliest_start_time(notes) -> float:
    earliest = 10_000

    for note in notes:
        if note.start < earliest:
            earliest = note.start
    return earliest