import core.Utils as Utils
from transcription.NoteObj import NoteObj
import cui.CUI as CUI
from testing.Scores import Scores
import transcription.KeyFinder as KeyFinder

import pretty_midi
import librosa



def __get_orig_notes(filePath,originalTempo):
    midi_data = pretty_midi.PrettyMIDI(filePath)
    #print("duration:",midi_data.get_end_time())
   # tempo = round(midi_data.estimate_tempo())

    bps = originalTempo/60.0 
    notes = []
    for instrument in midi_data.instruments:
        for note in instrument.notes:


            pitch = librosa.midi_to_note(note.pitch,unicode=False)
            start = Utils.snap_to_beat(note.start*bps)
            end = Utils.snap_to_beat(note.end*bps)

            notes.append(f"{pitch} {start} {end}")

    return (notes)


def __tempo_score(original,generated):
    ratio = generated/original
    result = 1 - abs(-ratio + 1)
    return result * 100





def __generated_note_list_parser(notes):
    result = []
    for note in notes:
        result.append(f"{note.note} {note.start} {note.start+note.duration}")
    return result





def __match_original_generated(generated, original):
    score = 0
    for i in original:
        if i in generated:
            score += 1
        else:
            print("COULDNT FIND", i, "IN GENERATED")

    return score / len(original) * 100

    


def __time_sig_score(generated,original):
    if generated[0] == original[0]:
        return 100
    

    return 0

def __match_generated_original(generated,original):
    score = 0
    for i in generated:
        if i in original:
            score += 1
        else:
            print("COULDNT FIND", i, "IN ORIGNAL")

    return score / len(generated) * 100



def __key_sig_score(generatedKeySig,originalKeySig):
    original = originalKeySig.lower()
    generated = generatedKeySig.lower()


    # Correct
    if  generated == original:
        return 100
    
    # Correct number of flats and sharps, wrong root. (Relative key)
    if KeyFinder.relative_key_check(originalKeySig,generatedKeySig):
        return 75

    # Correct root, wrong mode (Parallel key)
    if generated[:-5] == original[:-5]:
        return 50
    

    
    # Incorrect
    return 0
 


def score(generatedMusic,originalTempo, origKeySig,origTimeSig,filePath) -> float:
    generatedNotes = __generated_note_list_parser(generatedMusic.notes)
    originalNotes = __get_orig_notes(filePath,originalTempo)



    generatedOrignalScore = __match_generated_original(generatedNotes,originalNotes)
    orignalGeneratedScore = __match_original_generated(generatedNotes,originalNotes)

    noteScore = (generatedOrignalScore + orignalGeneratedScore) / 2

    tempoScore = __tempo_score(originalTempo,generatedMusic.tempo)
    keyScore = __key_sig_score(generatedMusic.key,origKeySig)
    timeScore = __time_sig_score(generatedMusic.timeSig,origTimeSig)


    
    
    CUI.diagnostic("Generated-Orignal Score", round(generatedOrignalScore,2), "%")
    CUI.diagnostic("Original-Generated Score", round(orignalGeneratedScore,2), "%")
    CUI.diagnostic("Total Note Score", round(noteScore,2), "%")
    CUI.newline()
    CUI.diagnostic("Tempo Score", round(tempoScore,2), "%")
    CUI.diagnostic("Key Signature Score", round(keyScore,2), "%")
    CUI.diagnostic("Time Signature Score", round(timeScore,2), "%")





    total = noteScore * 8 +  \
            tempoScore * 1 + \
            keyScore * 0.5 + \
            timeScore * 0.5
            
    score = round(total / (10.0),2)
    CUI.diagnostic("SCORE", score, "%")
    
    return Scores(noteScore=round(noteScore),
                  tempoOrig=round(originalTempo),
                  tempoGen=round(generatedMusic.tempo),
                  tempoScore=round(tempoScore),

                  keyOrig=origKeySig,
                  keyGen=generatedMusic.key,
                  keyScore=round(keyScore),

                  timeOrig=origTimeSig,
                  timeGen=generatedMusic.timeSig,
                  timeScore=round(timeScore),
                  totalScore=round(score))