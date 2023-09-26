import pretty_midi
import librosa
import Utils
def get_midi(path,tempo):
    midi_data = pretty_midi.PrettyMIDI(path)
    #print("duration:",midi_data.get_end_time())
    #tempo = __get_original_tempo(filePath)
   # tempo = round(midi_data.estimate_tempo())
    #UI.diagnostic("Original tempo", tempo, "bpm")
    #print(f'{"note":>10} {"start":>10} {"end":>10}')
    
    bps = tempo/60.0
    notes = []
    for instrument in midi_data.instruments:
        for note in instrument.notes:


            start = Utils.snap_to_beat(note.start*bps)
            end = Utils.snap_to_beat(note.end*bps)

            notes.append([note.pitch, start, end])

    return notes