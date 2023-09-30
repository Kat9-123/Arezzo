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
    global freqs
    freqs = np.arange(0, 1 + AudioProcessor.N_FFT / 2) * AudioProcessor.samplingRate / AudioProcessor.N_FFT

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
    for currentFrame in processedAudioData.onsets:
        notes = __get_notes_at_frame(currentNotes,notes,currentFrame,processedAudioData)
        #__model_get_notes(processedAudioData,currentFrame)

    CUI.stop_spinner()
    return notes












currentNotes = {}
finishedNotes = []





def __delete_queued_notes(notes: list,queue: list):
    for qNote in queue:
        notes.remove(qNote)

    queue = []
    return notes


def __get_notes_at_frame(currentNotes: list,finishedNotes: list,frame: int,processedAudioData) -> list:
    playingNotes = __model_get_notes(processedAudioData,frame)


    noteDeletionQueue = []


    for curNote in currentNotes:


        if curNote.note in playingNotes:
            playingNotes.remove(curNote.note)
            continue
        
        # curNote wasnt found, and should be ended
        curNote.finish_note(frame)
        print(curNote)
        finishedNotes.append(curNote)
        noteDeletionQueue.append(curNote)
            

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




def __note_to_row(note):
    
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
  