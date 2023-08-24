import Utils
from Note import Note
import ui.UI as UI

import pretty_midi
import librosa




def __get_orig_notes(filePath,tempo):
    midi_data = pretty_midi.PrettyMIDI(filePath)
    #print("duration:",midi_data.get_end_time())
    bpm = midi_data.estimate_tempo()
    #print(f'{"note":>10} {"start":>10} {"end":>10}')
    
    bps = tempo/60.0
    notes = []
    for instrument in midi_data.instruments:
        for note in instrument.notes:


            pitch = librosa.midi_to_note(note.pitch,unicode=False)
            start = Utils.snap_to_beat(note.start*bps)
            end = Utils.snap_to_beat(note.end*bps)

            notes.append(f"{pitch} {start} {end}")

    return notes



def score(notes,filePath,tempo):
    generatedNotes = __generated_note_list_parser(notes)
    originalNotes = __get_orig_notes(filePath,tempo)

    lengthScore = __length_score(generatedNotes,originalNotes)
    generatedOrignalScore = __match_generated_original(generatedNotes,originalNotes)
    orignalGeneratedScore = __match_original_generated(generatedNotes,originalNotes)

    UI.diagnostic("Length Score", round(lengthScore,2), "%")
    UI.diagnostic("Generated-Orignal Score", round(generatedOrignalScore,2), "%")
    UI.diagnostic("Original-Generated Score", round(orignalGeneratedScore,2), "%")


    total = lengthScore+generatedOrignalScore + orignalGeneratedScore
    score = round(total / 3.0,2)
    UI.diagnostic("SCORE", score, "%")
    

def __generated_note_list_parser(notes):
    result = []
    for note in notes:
        result.append(f"{note.note} {note.start} {note.start+note.duration}")
    return result


def __length_score(generated,original):
    ratio = len(generated)/len(original)
    result = 1 - abs(-ratio + 1)
    return result * 100


def __match_original_generated(generated, original):
    score = 0
    for i in original:
        if i in generated:
            score += 1
        else:
            print("COULDNT FIND", i, "IN GENERATED")

    return score / len(original) * 100

    


def __match_generated_original(generated,original):
    score = 0
    for i in generated:
        if i in original:
            score += 1
        else:
            print("COULDNT FIND", i, "IN ORIGNAL")

    return score / len(generated) * 100