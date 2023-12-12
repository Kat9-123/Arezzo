import pretty_midi
from midiutil.MidiFile import *
import librosa
import transcription.KeyFinder as KeyFinder
import mido

def get_midi(path):
    midi_data = pretty_midi.PrettyMIDI(path)
    allNotes = []
    for instrument in midi_data.instruments:
        allNotes += instrument.notes
    return allNotes






class TemporaryMIDIMessage():

    def __init__(self,type,note,time) -> None:
        self.type = type
        self.note = note
        self.time = time


def write_midi(notes,tempo,path,key,timeSig) -> None:
    """Takes a list of note objects, and a tempo and creates a MIDI file."""


    earliestStartTime = __get_earliest_start_time(notes)

    velocity = 100

    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)

    timeNumerator = int(timeSig[0])
    timeDenominator = 4

    midiTempo = mido.bpm2tempo(tempo,(timeNumerator,timeDenominator))

    track.append(mido.Message('program_change', program=1, time=0))
    track.append(mido.MetaMessage('set_tempo', tempo=midiTempo))


    midoKey = KeyFinder.convert_to_mido_key(key)
    track.append(mido.MetaMessage('key_signature', key=midoKey))

    track.append(mido.MetaMessage('time_signature', numerator=timeNumerator,denominator=timeDenominator))


    temporaryMIDIMessages = []


    for note in notes:
        


        midi = librosa.note_to_midi(note.note)
        start = (note.start - earliestStartTime) / (tempo/60)
        end = start + (note.duration / (tempo/60))
        
        start = mido.second2tick(start,mid.ticks_per_beat,midiTempo)
        end = mido.second2tick(end,mid.ticks_per_beat,midiTempo)

        temporaryMIDIMessages.append(TemporaryMIDIMessage("note_on",midi,start))
        temporaryMIDIMessages.append(TemporaryMIDIMessage("note_off",midi,end))
    currentTime = 0
    while len(temporaryMIDIMessages) != 0:
        
        smallestDeltaTime = 1_000_000_000
        message = None

        for temporaryMIDIEvent in temporaryMIDIMessages:
            if temporaryMIDIEvent.time - currentTime < smallestDeltaTime:
                smallestDeltaTime = temporaryMIDIEvent.time - currentTime
                message = temporaryMIDIEvent

        track.append(mido.Message(message.type, note=message.note, velocity=velocity, time=max(message.time - currentTime,0)))
        currentTime += max(message.time - currentTime,0)
        temporaryMIDIMessages.remove(message)



    # write it to disk
    mid.save(path)


    

def __get_earliest_start_time(notes) -> float:
    earliest = 10_000

    for note in notes:
        if note.start < earliest:
            earliest = note.start
    return earliest