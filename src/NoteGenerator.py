import Graphing
import AudioProcessor
from NoteObj import NoteObj
import Main
import cui.CUI as CUI

import librosa
import numpy as np
import copy
import network.Manager as netManager


#https://en.wikipedia.org/wiki/Chroma_feature
# {C, C♯, D, D♯, E , F, F♯, G, G♯, A, A♯, B} => chroma
# 1, 5, 2, 7 => octave
# C4, A5, Db2 => note


# Rows, Frames


SHOW_OCTAVE_INFO = False



CHROMA = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]

LOWEST_OCTAVE_DB = 5

HARMONIC_OCTAVE_MAX_DIFFERENCE_DB = 2


MAX_NOTE_DURATION = 4






freqs = np.ndarray


def get_notes(processedAudioData):
    """Takes in spectrum, chroma, onsets and tempo and returns all of the voices with their respective notes."""
    global cachedNoteRows
    freqs = np.arange(0, 1 + AudioProcessor.N_FFT / 2) * AudioProcessor.samplingRate / AudioProcessor.N_FFT
    print(processedAudioData.onsets)
    cachedNoteRows = {}

    for octave in range(0,8):
        for chroma in CHROMA:
            note = chroma + str(octave)
            cachedNoteRows[note] = __note_to_row(note,freqs)

   # freqs = librosa.fft_frequencies(sr=AudioProcessor.samplingRate,n_fft=AudioProcessor.N_FFT)
    CUI.progress("Generating Notes")
    #print(__note_to_row("C9"))

    #spectrumRowCache = __cache_note_to_spectrum_row()
    #UI.diagnostic("Cached Spectrum Rows", str(spectrumRowCache))
    CUI.diagnostic("Onsets", str(processedAudioData.onsets))


    frameCount = processedAudioData.spectrum.shape[1]

    #start = onsets[0]
   # for x in range(len(onsets)):
    #    onsets[x] -= start


    notes = []
    currentNotes = []
    for frame in range(processedAudioData.onsets[0],processedAudioData.onsets[-1]+1):
        notes = __process_frame(currentNotes,notes,frame,processedAudioData)
        #__model_get_notes(processedAudioData,currentFrame)

    CUI.stop_spinner()
    return notes

















def __delete_queued_notes(notes: list,queue: list):
    for qNote in queue:
        notes.remove(qNote)

    queue = []
    return notes


def __get_volume(note,frame,processedAudioData):
    return processedAudioData.spectrum[cachedNoteRows[note],frame]

def __process_frame(currentNotes: list,finishedNotes: list,frame: int,processedAudioData):
    
    if frame in processedAudioData.onsets:
        return __get_notes_at_frame(currentNotes,finishedNotes,frame,processedAudioData)

    for noteObj in currentNotes:
        strength = __get_volume(noteObj.note,frame-AudioProcessor.ONSET_TEMPORAL_LAG,processedAudioData)
        noteObj.add_strength(strength)

    return finishedNotes



def __get_notes_at_frame(currentNotes: list,finishedNotes: list,frame: int,processedAudioData) -> list:
    playingNotes = __model_get_notes(processedAudioData,frame)


    noteDeletionQueue = []


    for curNoteObj in currentNotes:


        if curNoteObj.note in playingNotes:
            
            newStrength = __get_volume(curNoteObj.note,frame-AudioProcessor.ONSET_TEMPORAL_LAG,processedAudioData)
            
            avgStrength = curNoteObj.get_average_strength()
            print(newStrength,avgStrength, (newStrength - avgStrength))


            # Not a repeat note 
            if (newStrength - avgStrength) < -8:
                playingNotes.remove(curNoteObj.note)
                continue

        
        # curNote wasnt found, and should be ended
        curNoteObj.finish_note(frame)
        print(curNoteObj, curNoteObj.get_average_strength())
        finishedNotes.append(curNoteObj)
        noteDeletionQueue.append(curNoteObj)
            

    currentNotes = __delete_queued_notes(currentNotes,noteDeletionQueue)

    for newNote in playingNotes:
        currentNotes.append(NoteObj(newNote,frame,processedAudioData))


    # Final note check
    if frame != processedAudioData.onsets[-1]:
        return finishedNotes
    

    for note in currentNotes:
        note.finish_note(frame,isFinal=True)
        finishedNotes.append(note)

    return finishedNotes
    
        

    





def __model_get_notes(processedAudioData,frame):
    data = processedAudioData.spectrum[0:6222,frame]
    modelOutput = netManager.get_model_output(data)


    notes = []
    #print(modelOutput.tolist())
    for x,i in enumerate((modelOutput.tolist())):
        if i == 0:
            continue
        octave, chroma = divmod(x + 9,12)
        chroma = CHROMA[chroma]
        note = chroma + str(octave)
        CUI.print_colour(note,CUI.RED,end="\n")
        notes.append(note)

    return notes




def __note_to_row(note,freqs):
    
    hz = librosa.note_to_hz(note)
    smallestDist = 10000
    smallestRow = -1

    for x,freq in enumerate(freqs):
        dist = abs(freq - hz)
        
        if dist < smallestDist:
            smallestRow = x
            smallestDist = dist
    
    if smallestRow == -1:
        CUI.warning("Row corresponding to note not found!")
        return 0

   # UI.diagnostic("NOTE_TO_ROW","{} => {}".format(note,smallestRow))
    return smallestRow
  